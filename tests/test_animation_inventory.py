"""Exercise inventory recovery, omissions, failure bounds, and read-only behavior."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/frontend/animation-audit/scripts/inventory.py'


class AnimationInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)

    def call(self, *args):
        p = subprocess.run([sys.executable, str(HELPER), '--root', str(self.root), *map(str, args)],
                           capture_output=True, text=True)
        self.assertLessEqual(len(p.stdout), 4000)
        self.assertEqual(p.stderr, '')
        return p.returncode, json.loads(p.stdout)

    def test_candidates_are_inert_hints_with_exact_locations(self):
        path = self.root / 'component.tsx'
        source = '// motion.div is documentation, not a proven animation\nconst x = "motion.div";\n'
        path.write_text(source)
        (self.root / 'unused.ts').write_text('const x = 1;')
        code, result = self.call('--mode', 'candidates')
        self.assertEqual(code, 0)
        self.assertTrue(result['heuristic_only'])
        self.assertEqual(result['items'], [{'path': path.name, 'first_line': 1, 'matching_lines': 2}])
        self.assertEqual(path.read_text(), source)

    def test_large_unicode_pages_recover_all_paths_across_scan_windows(self):
        names = [f'파일-{i:03d}-with space\n.ts' for i in range(140)]
        for name in names:
            (self.root / name).write_text('withSpring(1)')
        found, scan_offset = [], 0
        while True:
            offset = 0
            while True:
                code, result = self.call('--mode', 'candidates', '--scan-offset', scan_offset,
                                         '--scan-limit', 40, '--offset', offset)
                self.assertEqual(code, 0)
                found.extend(r['path'] for r in result['items'])
                self.assertEqual(result['omitted_before'] + len(result['items']) + result['omitted_after'], result['total'])
                if result['next_offset'] is None:
                    break
                self.assertGreater(result['next_offset'], offset)
                offset = result['next_offset']
            if result['next_scan_offset'] is None:
                break
            self.assertGreater(result['next_scan_offset'], scan_offset)
            scan_offset = result['next_scan_offset']
        self.assertEqual(sorted(found), sorted(names))
        summary = self.call('--scan-limit', 40)[1]
        self.assertEqual(summary['unscanned_after'], 100)
        self.assertEqual(summary['window_files'], 40)

    def test_skipped_files_remain_visible_without_following_external_links(self):
        (self.root / 'large.css').write_bytes(b'a' * 1_000_001)
        (self.root / 'binary.js').write_bytes(b'animation:\x00')
        (self.root / 'encoding.ts').write_bytes(b'\xff')
        (self.root / 'outside.css').symlink_to('/tmp/does-not-belong-to-this-root')
        code, result = self.call('--mode', 'skipped')
        self.assertEqual(code, 0)
        self.assertEqual(result['skipped_files'], 4)
        self.assertEqual({r['path'] for r in result['items']}, {'large.css', 'binary.js', 'encoding.ts', 'outside.css'})
        self.assertEqual(result['scanned_files'], 0)

    def test_invalid_root_offsets_and_unknown_arguments_fail_bounded(self):
        for args in [('--root', self.root/'missing'), ('--scan-offset', -1), ('--scan-offset', 1),
                     ('--scan-limit', 0), ('--offset', -1, '--mode', 'candidates'),
                     ('--limit', 0), ('--unknown-'+'x'*10000,)]:
            code, result = self.call(*args)
            self.assertEqual(code, 2)
            self.assertIn('error', result)
        self.assertEqual([p.name for p in self.root.iterdir()], ['.git'])

    def test_oversized_exact_path_fails_without_silent_shortening(self):
        target = self.root
        for i in range(12):
            target = target / ('가' * 55 + str(i))
        target.mkdir(parents=True)
        (target / 'motion.ts').write_text('withTiming(1)')
        self.assertEqual(self.call()[0], 0)
        code, result = self.call('--mode', 'candidates')
        self.assertEqual(code, 2)
        self.assertIn('exceeds', result['error'])

    def test_missing_discovery_tool_fails_with_a_bounded_error(self):
        import os
        p = subprocess.run([sys.executable, str(HELPER), '--root', str(self.root)],
                           env={**os.environ, 'PATH': ''}, capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertLessEqual(len(p.stdout), 4000)
        self.assertIn('error', json.loads(p.stdout))
        self.assertEqual(p.stderr, '')

    def test_git_ignore_and_selected_subdirectory_define_discovery_scope(self):
        (self.root / '.gitignore').write_text('ignored/\n')
        (self.root / 'ignored').mkdir()
        (self.root / 'ignored/noise.css').write_text('transition: all 1s;')
        selected = self.root / 'app'
        selected.mkdir()
        (selected / 'screen.tsx').write_text('motion.div')
        (self.root / 'other.tsx').write_text('withSpring(1)')
        code, summary = self.call()
        self.assertEqual(code, 0)
        self.assertEqual(summary['eligible_files'], 2)
        code, page = self.call('--root', selected, '--mode', 'candidates')
        self.assertEqual(code, 0)
        self.assertEqual([r['path'] for r in page['items']], ['screen.tsx'])


if __name__ == '__main__':
    unittest.main()
