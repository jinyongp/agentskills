"""Replay a failing symptom and its correction through the standalone debug runner."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'skills/workflow/debug/scripts/reproduce.py'


class DebugReproductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_case(self, name, program, *arguments):
        log = self.root / name
        result = subprocess.run([sys.executable, str(HELPER), 'run', '--cwd', str(self.root), '--log', str(log), '--', sys.executable, '-c', program, *arguments], capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, '')
        return result.returncode, json.loads(result.stdout), log

    def test_reproduce_then_correct_without_touching_unrelated_work(self):
        source = self.root / 'sample.py'
        source.write_text('def average(values):\n    return sum(values) / len(values)\n')
        before = source.read_bytes()
        note = self.root / 'user-note.txt'
        note.write_bytes(b'preserve user work')
        program = 'from pathlib import Path; ns = {}; exec(Path("sample.py").read_text(), ns); assert ns["average"]([]) == 0'
        code, result, log = self.run_case('baseline.log', program)
        self.assertEqual(code, 1)
        self.assertEqual(result['result'], 'fail')
        self.assertIn('ZeroDivisionError', log.read_text())
        self.assertEqual(source.read_bytes(), before)
        source.write_text('def average(values):\n    return sum(values) / len(values) if values else 0\n')
        code, result, _ = self.run_case('corrected.log', program)
        self.assertEqual(code, 0)
        self.assertEqual(result['result'], 'pass')
        self.assertEqual(note.read_bytes(), b'preserve user work')

    def test_reproduction_arguments_are_literal(self):
        literal = '$(touch shell-side-effect) with space'
        code, result, log = self.run_case('literal.log', 'import sys; print(sys.argv[1])', literal)
        self.assertEqual(code, 0)
        self.assertEqual(log.read_text(), literal + '\n')
        self.assertFalse((self.root / 'shell-side-effect').exists())


if __name__ == '__main__':
    unittest.main()
