"""Check review layers, pinned comparisons, paging, and absence of inspection side effects."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/workflow/code-review/scripts/inspect_changes.py'


class ReviewInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null'}
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Evaluation')
        self.git('config', 'user.email', 'evaluation@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        (self.repo / 'feature.txt').write_text('initial\n')
        self.git('add', '--', 'feature.txt')
        self.git('commit', '-m', 'test: initial review fixture')

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.repo, env=self.env, stderr=subprocess.DEVNULL).decode()

    def call(self, *args):
        result = subprocess.run([sys.executable, str(HELPER), '--repo', str(self.repo), *map(str, args)], env=self.env, capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def test_layers_and_summary_preserve_work(self):
        (self.repo / 'feature.txt').write_text('staged\n')
        self.git('add', '--', 'feature.txt')
        (self.repo / 'feature.txt').write_text('staged\nextra\n')
        (self.repo / 'new.txt').write_text('untracked')
        before = (self.git('rev-parse', 'HEAD'), self.git('diff', '--cached', '--binary'), (self.repo / 'feature.txt').read_bytes())
        code, result = self.call()
        self.assertEqual(code, 0)
        self.assertEqual(result['counts'], {'staged': 1, 'working': 1, 'untracked': 1})
        self.assertNotIn('text', result)
        records = self.call('--mode', 'files')[1]['items']
        self.assertEqual({(r['layer'], r['path']) for r in records}, {('staged', 'feature.txt'), ('working', 'feature.txt'), ('untracked', 'new.txt')})
        self.assertEqual(before, (self.git('rev-parse', 'HEAD'), self.git('diff', '--cached', '--binary'), (self.repo / 'feature.txt').read_bytes()))

    def test_comparison_excludes_dirty_files_and_pins_refs(self):
        base = self.git('rev-parse', 'HEAD').strip()
        (self.repo / 'feature.txt').write_text('committed\n')
        self.git('commit', '-am', 'test: feature change')
        head = self.git('rev-parse', 'HEAD').strip()
        (self.repo / 'dirty.txt').write_text('not in comparison')
        result = self.call('--base', base, '--head', head)[1]
        self.assertEqual(result['comparison'], {'base': base, 'head': head, 'merge_base': False})
        self.assertEqual(result['distinct_paths'], 1)
        self.assertEqual(self.call('--base', base, '--mode', 'files')[1]['items'], [{'layer': 'comparison', 'path': 'feature.txt'}])

    def test_merge_base_excludes_independent_base_branch_changes(self):
        initial = self.git('rev-parse', 'HEAD').strip()
        self.git('switch', '-c', 'feature')
        (self.repo / 'feature.txt').write_text('feature change\n')
        self.git('commit', '-am', 'test: feature branch')
        self.git('switch', 'main')
        (self.repo / 'base-only.txt').write_text('independent base change')
        self.git('add', '--', 'base-only.txt')
        self.git('commit', '-m', 'test: base branch')
        page = self.call('--base', 'main', '--head', 'feature', '--merge-base', '--mode', 'files')[1]
        self.assertEqual(page['comparison']['base'], initial)
        self.assertEqual(page['items'], [{'layer': 'comparison', 'path': 'feature.txt'}])

    def test_pages_recover_paths_and_diff_exactly(self):
        names = [f'파일-{i:03d} space\n.txt' for i in range(140)]
        for name in names:
            (self.repo / name).write_text('untracked')
        records, offset = [], 0
        while True:
            page = self.call('--mode', 'files', '--offset', offset)[1]
            records.extend(page['items'])
            if page['next_offset'] is None:
                break
            offset = page['next_offset']
        self.assertEqual(sorted(r['path'] for r in records), sorted(names))
        (self.repo / 'feature.txt').write_text('가나다\\\n' * 1000)
        text, offset = '', 0
        while True:
            page = self.call('--mode', 'diff', '--path', 'feature.txt', '--offset', offset)[1]
            text += page['text']
            if page['next_offset'] is None:
                break
            offset = page['next_offset']
        self.assertEqual(text, self.git('diff', '--no-ext-diff', '--no-textconv', '--no-color', '--no-renames', '--ignore-submodules=none', '--', 'feature.txt'))

    def test_external_diff_is_not_executed(self):
        marker = self.repo / 'must-not-exist'
        script = self.repo / 'external.py'
        script.write_text(f'from pathlib import Path\nPath({str(marker)!r}).write_text("bad")\n')
        self.git('config', 'diff.external', f'{sys.executable} {script}')
        hook = self.repo / '.git/fsmonitor-test'
        hook.write_text('#!/bin/sh\n: > "$0.marker"\nprintf "token\\0/\\0"\n')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', str(hook))
        (self.repo / 'feature.txt').write_text('changed\n')
        self.assertEqual(self.call('--mode', 'diff', '--path', 'feature.txt')[0], 0)
        self.assertFalse(marker.exists())
        self.assertFalse(Path(str(hook) + '.marker').exists())

    def test_invalid_refs_paths_and_arguments_fail_bounded(self):
        for args in (('--base', 'missing'), ('--head', 'HEAD'), ('--base', '--output=evil'), ('--mode', 'diff'), ('--mode', 'diff', '--path', '../outside'), ('--mode', 'files', '--offset', '-1')):
            self.assertEqual(self.call(*args)[0], 2)
        self.assertEqual(self.call('--repo', self.repo / 'missing')[0], 2)
        self.assertEqual(self.call('--unknown-' + 'x' * 10000)[0], 2)


if __name__ == '__main__':
    unittest.main()
