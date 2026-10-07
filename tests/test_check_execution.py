"""Verify bounded check results, full log recovery, failure, and timeout cleanup."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/workflow/verify/scripts/run_check.py'


class CheckExecutionTests(unittest.TestCase):
    helper = HELPER
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.log = self.root / 'check.log'

    def call(self, *args):
        result = subprocess.run([sys.executable, str(self.helper), *map(str, args)], capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout)

    def execute(self, code, *options):
        return self.call('run', '--cwd', self.root, '--log', self.log, *options, '--', sys.executable, '-c', code)

    def test_success_and_large_output_are_logged_without_dumping(self):
        code, result = self.execute("print('large output' * 10000)")
        self.assertEqual(code, 0)
        self.assertEqual(result['result'], 'pass')
        self.assertNotIn('large output', json.dumps(result))
        self.assertEqual(result['output_bytes'], len(self.log.read_bytes()))

    def test_failed_check_is_not_reported_as_pass(self):
        code, result = self.execute("import sys; print('failure'); sys.exit(7)")
        self.assertEqual(code, 1)
        self.assertEqual(result['returncode'], 7)
        self.assertEqual(result['result'], 'fail')
        self.assertEqual(self.log.read_text(), 'failure\n')

    def test_pages_recover_unicode_control_and_invalid_bytes(self):
        raw = ('가나다\\\n' * 1000).encode() + b'\xff\x00'
        self.log.write_bytes(raw)
        recovered, offset = b'', 0
        while True:
            code, page = self.call('log', '--log', self.log, '--offset', offset)
            self.assertEqual(code, 0)
            recovered += page['text'].encode('utf-8', 'surrogateescape')
            if page['next_offset'] is None:
                break
            self.assertGreater(page['next_offset'], offset)
            offset = page['next_offset']
        self.assertEqual(recovered, raw)

    def test_existing_log_is_preserved(self):
        self.log.write_text('existing evidence')
        code, result = self.execute("print('new output')")
        self.assertEqual(code, 2)
        self.assertIn('error', result)
        self.assertEqual(self.log.read_text(), 'existing evidence')

    def test_timeout_is_not_a_pass_and_kills_descendants(self):
        marker = self.root / 'late-write'
        child = f"import time; from pathlib import Path; time.sleep(0.5); Path({str(marker)!r}).write_text('late')"
        program = f"import subprocess, sys, time; subprocess.Popen([sys.executable, '-c', {child!r}]); time.sleep(30)"
        code, result = self.execute(program, '--timeout', '0.1')
        self.assertEqual(code, 124)
        self.assertEqual(result['result'], 'timeout')
        subprocess.run([sys.executable, '-c', 'import time; time.sleep(0.6)'], check=True)
        self.assertFalse(marker.exists())

    def test_missing_command_and_invalid_offsets_are_bounded(self):
        code, result = self.call('run', '--cwd', self.root, '--log', self.log, '--', '/missing/check')
        self.assertEqual(code, 2)
        self.assertIn('error', result)
        for offset in (-1, 100):
            self.log.write_bytes(b'short')
            self.assertEqual(self.call('log', '--log', self.log, '--offset', offset)[0], 2)
        self.assertEqual(self.call('--unknown-' + 'x' * 10000)[0], 2)


class CiCaptureTests(CheckExecutionTests):
    helper = HELPER.parents[2] / 'ci-fix/scripts/capture.py'


if __name__ == '__main__':
    unittest.main()
