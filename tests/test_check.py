"""Verify check selection and failure propagation through real subprocesses."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[1] / "check.py"


class CheckRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copyfile(RUNNER, self.root / "check.py")
        scripts = self.root / "scripts"
        scripts.mkdir()
        (self.root / "catalog.md").write_text("Current source\n")
        (self.root / "index.md").write_text("Old generated index\n")
        (scripts / "generate_index.py").write_text(
            'from pathlib import Path\n'
            'Path("index.md").write_text(Path("catalog.md").read_text())\n'
            'print("INDEX_OK")\n'
        )
        (scripts / "validate_skills.py").write_text(
            'from pathlib import Path\nimport sys\n'
            'if Path("index.md").read_text() != Path("catalog.md").read_text(): sys.exit(9)\n'
            'print("VALIDATE_OK")\n'
        )
        (scripts / "smoke_install.py").write_text('print("SMOKE_OK")\n')
        (scripts / "smoke_package.py").write_text('print("PACKAGE_OK")\n')
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_fixture.py").write_text(
            "import unittest\n"
            "class Fixture(unittest.TestCase):\n"
            "    def test_example(self):\n"
            '        print("TEST_OK")\n'
        )

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "check.py"), *args],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
        )

    def test_all_checks_run_from_repository_root(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("INDEX_OK"), result.stdout.index("VALIDATE_OK"))
        self.assertLess(result.stdout.index("VALIDATE_OK"), result.stdout.index("TEST_OK"))
        self.assertLess(result.stdout.index("TEST_OK"), result.stdout.index("SMOKE_OK"))
        self.assertLess(result.stdout.index("SMOKE_OK"), result.stdout.index("PACKAGE_OK"))

    def test_validate_does_not_run_tests_or_installation(self):
        result = self.run_check("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("VALIDATE_OK", result.stdout)
        self.assertNotIn("TEST_OK", result.stdout)
        self.assertNotIn("SMOKE_OK", result.stdout)

    def test_failure_preserves_exit_code_and_stops_later_checks(self):
        (self.root / "scripts" / "validate_skills.py").write_text(
            "import sys\nsys.exit(7)\n"
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 7)
        self.assertNotIn("TEST_OK", result.stdout)
        self.assertNotIn("SMOKE_OK", result.stdout)

    def test_unknown_check_is_rejected_before_execution(self):
        result = self.run_check("unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)
        self.assertNotIn("VALIDATE_OK", result.stdout)

    def test_read_only_index_check_rejects_stale_output_without_repair(self):
        before = (self.root / "index.md").read_bytes()
        result = self.run_check("validate", "--check-index")
        self.assertEqual(result.returncode, 9)
        self.assertEqual((self.root / "index.md").read_bytes(), before)
        self.assertNotIn("INDEX_OK", result.stdout)
        (self.root / "index.md").write_bytes((self.root / "catalog.md").read_bytes())
        result = self.run_check("--check-index")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("INDEX_OK", result.stdout)

    def test_generation_failure_stops_validation_and_later_checks(self):
        (self.root / "scripts/generate_index.py").write_text("import sys\nsys.exit(8)\n")
        result = self.run_check()
        self.assertEqual(result.returncode, 8)
        self.assertNotIn("VALIDATE_OK", result.stdout)
        self.assertNotIn("TEST_OK", result.stdout)

    def test_read_only_flag_requires_a_validation_check(self):
        result = self.run_check("test", "--check-index")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("TEST_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
