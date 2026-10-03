"""Verify read-only directory summaries, exact pages, and inert manifest inspection."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/workflow/survey/scripts/inspect_repo.py'


class RepoSurveyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def call(self, *args):
        result = subprocess.run([sys.executable, str(HELPER), '--root', str(self.root), *map(str, args)], capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def collect(self, mode, *args):
        records, offset = [], 0
        while True:
            code, result = self.call('--mode', mode, '--offset', offset, *args)
            self.assertEqual(code, 0)
            records.extend(result['items'])
            if result['next_offset'] is None:
                return records
            self.assertGreater(result['next_offset'], offset)
            offset = result['next_offset']

    def test_summary_does_not_execute_manifest_commands(self):
        marker = self.root / 'must-not-exist'
        manifest = self.root / 'package.json'
        original = json.dumps({'scripts': {'test': f'touch {marker}'}})
        manifest.write_text(original)
        (self.root / 'pnpm-lock.yaml').write_text('lock')
        code, result = self.call()
        self.assertEqual(code, 0)
        self.assertIn('package.json', result['markers'])
        self.assertNotIn('scripts', result)
        self.assertEqual(self.collect('commands')[0]['name'], 'test')
        self.assertFalse(marker.exists())
        self.assertEqual(manifest.read_text(), original)

    def test_large_unicode_entry_pages_recover_all_names(self):
        names = [f'파일-{i:03d}-with space\n.txt' for i in range(160)]
        for name in names:
            (self.root / name).write_text('unchanged')
        self.assertEqual(sorted(record['name'] for record in self.collect('entries')), sorted(names))
        self.assertEqual(self.call()[1]['entry_count'], 160)

    def test_command_pages_preserve_all_scripts(self):
        scripts = {f'check-{i}': 'echo ' + '가' * 40 for i in range(120)}
        (self.root / 'package.json').write_text(json.dumps({'scripts': scripts}))
        records = self.collect('commands')
        self.assertEqual({r['name']: r['command'] for r in records}, scripts)

    def test_python_entrypoints_are_not_misclassified_as_tests(self):
        (self.root / 'pyproject.toml').write_text('[project.scripts]\napp = "package.cli:main"\n')
        records = self.collect('commands', '--manifest', 'pyproject.toml')
        self.assertEqual(records, [{'name': 'app', 'command': 'package.cli:main', 'kind': 'python-entrypoint'}])

    def test_malformed_oversized_entries_and_external_symlinks_fail_bounded(self):
        manifest = self.root / 'package.json'
        for content in ('invalid json', '[]', '{"scripts":[]}', json.dumps({'scripts': {'huge': 'x' * 5000}}), 'x' * 1_000_001):
            manifest.write_text(content)
            code, result = self.call('--mode', 'commands')
            self.assertEqual(code, 2)
            self.assertIn('error', result)
        manifest.unlink()
        manifest.symlink_to('/tmp/does-not-belong-to-selected-directory')
        self.assertEqual(self.call('--mode', 'commands')[0], 2)

    def test_invalid_directory_and_offsets_fail_without_changes(self):
        self.assertEqual(self.call('--root', self.root / 'missing')[0], 2)
        for offset in (-1, 1):
            self.assertEqual(self.call('--mode', 'entries', '--offset', offset)[0], 2)
        self.assertEqual(self.call('--unknown-' + 'x' * 10000)[0], 2)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
