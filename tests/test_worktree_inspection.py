"""Check read-only worktree queries, exact registry pages, and safe lifecycle fixtures."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/git/git-worktree/scripts/inspect_worktrees.py'


class WorktreeInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'main'
        self.repo.mkdir()
        self.env = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null'}
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Evaluation')
        self.git('config', 'user.email', 'evaluation@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        (self.repo / 'feature.txt').write_text('initial\n')
        self.git('add', '--', 'feature.txt')
        self.git('commit', '-m', 'test: initial worktree fixture')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, env=self.env, stderr=subprocess.DEVNULL).decode()

    def call(self, *args):
        result = subprocess.run([sys.executable, str(HELPER), '--repo', str(self.repo), *map(str, args)], env=self.env, capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def test_lifecycle_and_parent_work_are_preserved(self):
        (self.repo / 'feature.txt').write_text('staged\n')
        self.git('add', '--', 'feature.txt')
        (self.repo / 'feature.txt').write_text('staged\nunstaged\n')
        (self.repo / 'new.txt').write_text('untracked')
        before = (self.git('rev-parse', 'HEAD'), self.git('diff', '--cached', '--binary'), (self.repo / 'feature.txt').read_bytes())
        work = self.root / 'feature'
        self.git('worktree', 'add', '-b', 'feature', str(work), 'HEAD')
        self.assertEqual(self.call()[1]['linked'], 1)
        self.assertEqual(self.call('--mode', 'state', '--path', work)[1]['dirty'], False)
        result = self.call('--mode', 'state', '--path', self.repo)[1]
        self.assertEqual(result['counts'], {'staged': 1, 'unstaged': 1, 'untracked': 1, 'conflicted': 0})
        self.git('worktree', 'remove', str(work))
        self.assertFalse(work.exists())
        self.git('show-ref', '--verify', 'refs/heads/feature')
        self.assertEqual(before, (self.git('rev-parse', 'HEAD'), self.git('diff', '--cached', '--binary'), (self.repo / 'feature.txt').read_bytes()))
        self.assertEqual((self.repo / 'new.txt').read_text(), 'untracked')

    def test_locked_detached_and_unusual_paths_are_exact(self):
        work = self.root / '공간 with\nnewline'
        self.git('worktree', 'add', '--detach', str(work), 'HEAD')
        reason = 'preserve this\nexternal task'
        self.git('worktree', 'lock', '--reason', reason, str(work))
        result = self.call('--mode', 'list')[1]
        entry = next(r for r in result['items'] if not r['main'])
        self.assertEqual(entry['worktree'], str(work))
        self.assertEqual(entry['locked'], reason)
        self.assertTrue(entry['detached'])
        self.assertEqual(self.call()[1]['locked'], 1)
        with self.assertRaises(subprocess.CalledProcessError):
            self.git('worktree', 'remove', str(work))
        self.assertTrue(work.exists())

    def test_registry_pages_recover_all_paths(self):
        paths = {str(self.repo)}
        for index in range(20):
            work = self.root / (f'{index:02d}-' + '가' * 25 + ' space')
            self.git('worktree', 'add', '--detach', str(work), 'HEAD')
            paths.add(str(work))
        records, offset = [], 0
        while True:
            result = self.call('--mode', 'list', '--offset', offset)[1]
            records.extend(result['items'])
            if result['next_offset'] is None:
                break
            self.assertGreater(result['next_offset'], offset)
            offset = result['next_offset']
        self.assertEqual({r['worktree'] for r in records}, paths)
        self.assertEqual(len(records), 21)
        self.assertEqual(sum(r['main'] for r in records), 1)

    def test_dirty_removal_refuses_without_discarding_files(self):
        work = self.root / 'dirty'
        self.git('worktree', 'add', '-b', 'dirty', str(work), 'HEAD')
        (work / 'new.txt').write_bytes(b'preserve dirty work')
        self.assertTrue(self.call('--mode', 'state', '--path', work)[1]['dirty'])
        with self.assertRaises(subprocess.CalledProcessError):
            self.git('worktree', 'remove', str(work))
        self.assertEqual((work / 'new.txt').read_bytes(), b'preserve dirty work')

    def test_unregistered_paths_and_bad_queries_fail_bounded(self):
        for args in (('--mode', 'state'), ('--mode', 'state', '--path', self.root), ('--mode', 'list', '--offset', '-1'), ('--repo', self.root / 'missing'), ('--unknown-' + 'x' * 10000,)):
            self.assertEqual(self.call(*args)[0], 2)
        self.assertEqual(self.call()[1]['total'], 1)

    def test_rename_counts_and_active_operation_are_detected(self):
        self.git('mv', 'feature.txt', 'renamed.txt')
        git_dir = Path(self.git('rev-parse', '--absolute-git-dir').strip())
        (git_dir / 'MERGE_HEAD').write_text(self.git('rev-parse', 'HEAD'))
        result = self.call('--mode', 'state', '--path', self.repo)[1]
        self.assertEqual(result['counts']['staged'], 1)
        self.assertEqual(result['operations'], ['merge'])

    def test_ignored_local_data_is_visible_without_becoming_git_dirty(self):
        (self.repo / '.gitignore').write_text('private.note\n')
        self.git('add', '--', '.gitignore')
        self.git('commit', '-m', 'test: ignored local data')
        work = self.root / 'ignored'
        self.git('worktree', 'add', '-b', 'ignored', str(work), 'HEAD')
        (work / 'private.note').write_bytes(b'valuable local data')
        result = self.call('--mode', 'state', '--path', work)[1]
        self.assertFalse(result['dirty'])
        self.assertEqual(result['ignored_files'], 1)
        self.assertEqual(self.call('--mode', 'ignored', '--path', work)[1]['items'], [{'path': 'private.note'}])
        self.assertEqual((work / 'private.note').read_bytes(), b'valuable local data')


if __name__ == '__main__':
    unittest.main()
