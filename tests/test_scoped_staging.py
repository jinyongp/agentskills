"""Replay scoped staging across initial commits and failed commit hooks."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ENV = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull}


class ScopedStagingTests(unittest.TestCase):
    def replay(self, seeded, hook_failure):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repo = root / 'repo'
            repo.mkdir()

            def git(*args, input=None, success=True):
                result = subprocess.run(['git', '--literal-pathspecs', '-C', str(repo), *args],
                                        env=ENV, input=input, capture_output=True)
                if success:
                    self.assertEqual(result.returncode, 0, result.stderr)
                return result

            git('init', '-b', 'main')
            git('config', 'user.name', 'Scoped Staging Test')
            git('config', 'user.email', 'staging@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            included = repo / 'included.txt'
            if seeded:
                included.write_bytes(b'old included\n')
                git('add', '--', 'included.txt')
                git('commit', '-m', 'test: initial fixture')
            included.write_bytes(b'new included\n')
            excluded = ['excluded [draft].txt', 'excluded.bin']
            for name, value in zip(excluded, (b'staged text\n', b'\x00staged binary\xff')):
                (repo / name).write_bytes(value)
            git('add', '--', 'included.txt', *excluded)
            for name, value in zip(excluded, (b'working text\n', b'\x00working binary\xfe')):
                (repo / name).write_bytes(value)
            original_head = git('rev-parse', '--verify', 'HEAD', success=False).stdout
            original_patch = git('diff', '--cached', '--binary', '--', *excluded).stdout
            original_entries = git('ls-files', '--stage', '-z', '--', *excluded).stdout
            working = {name: (repo / name).read_bytes() for name in excluded}
            patch = root / 'excluded.patch'
            patch.write_bytes(original_patch)

            # An empty tree supplies the source that unborn HEAD cannot provide.
            source = []
            if not seeded:
                tree = git('hash-object', '-w', '-t', 'tree', '--stdin', input=b'').stdout.decode().strip()
                source = ['--source', tree]
            git('restore', '--staged', *source, '--', *excluded)
            self.assertEqual(git('diff', '--cached', '--name-only').stdout, b'included.txt\n')
            self.assertEqual(working, {name: (repo / name).read_bytes() for name in excluded})
            git('diff', '--cached', '--check')
            if hook_failure:
                hook = repo / '.git/hooks/pre-commit'
                hook.write_text('#!/bin/sh\nexit 1\n')
                hook.chmod(0o755)
            committed = git('commit', '-m', 'test: scoped commit', success=not hook_failure)
            if hook_failure:
                self.assertNotEqual(committed.returncode, 0)
                self.assertEqual(git('rev-parse', '--verify', 'HEAD', success=False).stdout, original_head)
            else:
                self.assertEqual(git('diff-tree', '--root', '--no-commit-id', '--name-only', '-r', 'HEAD').stdout,
                                 b'included.txt\n')
            git('apply', '--cached', str(patch))
            self.assertEqual(git('diff', '--cached', '--binary', '--', *excluded).stdout, original_patch)
            self.assertEqual(git('ls-files', '--stage', '-z', '--', *excluded).stdout, original_entries)
            self.assertEqual(working, {name: (repo / name).read_bytes() for name in excluded})
            self.assertEqual(included.read_bytes(), b'new included\n')

    def test_scoped_commit_preserves_excluded_index_and_working_files(self):
        for seeded in (False, True):
            with self.subTest(seeded=seeded):
                self.replay(seeded, hook_failure=False)

    def test_failed_commit_restores_excluded_index_without_changing_head(self):
        for seeded in (False, True):
            with self.subTest(seeded=seeded):
                self.replay(seeded, hook_failure=True)


if __name__ == '__main__':
    unittest.main()
