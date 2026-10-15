"""Verify standalone change inspectors preserve comparison scope and local work."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ("review-map", "dependency-review", "qa-checklist", "preflight")


class WorkflowInspectorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "project"
        self.repo.mkdir()
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Workflow fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        (self.repo / "package.json").write_text('{"dependencies":{"demo":"^1.0.0"}}\n')
        (self.repo / "package-lock.json").write_text('{"version":"1.0.0"}\n')
        self.git("add", "--", ".")
        self.git("commit", "-m", "test: fixture baseline")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("switch", "-c", "candidate")
        (self.repo / "package-lock.json").write_text('{"version":"1.0.1"}\n')
        self.git("commit", "-am", "test: lock-only upgrade")
        self.head = self.git("rev-parse", "HEAD").strip()
        self.helpers = {}
        for name in WORKFLOWS:
            # Only the inspector is present, so sibling/repository imports cannot work.
            destination = self.root / "standalone" / name / "inspect_changes.py"
            destination.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "skills/workflow" / name / "scripts/inspect_changes.py", destination)
            self.helpers[name] = destination

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, env=self.env, stderr=subprocess.DEVNULL).decode()

    def call(self, name, *args):
        result = subprocess.run([sys.executable, str(self.helpers[name]), "--repo", str(self.repo), *args],
                                cwd=self.root, env=self.env, capture_output=True, text=True)
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, "")
        return result.returncode, json.loads(result.stdout)

    def test_lock_only_upgrade_is_visible_in_each_pinned_comparison(self):
        (self.repo / "unrelated.txt").write_text("Not committed\n")
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                code, page = self.call(name, "--base", self.base, "--head", self.head, "--mode", "files")
                self.assertEqual(code, 0)
                self.assertEqual(page["comparison"]["base"], self.base)
                self.assertEqual(page["comparison"]["head"], self.head)
                self.assertEqual([item["path"] for item in page["items"]], ["package-lock.json"])
                code, detail = self.call(name, "--base", self.base, "--head", self.head, "--mode", "diff", "--path", "package-lock.json")
                self.assertEqual(code, 0)
                self.assertIn('1.0.1', detail["text"])
                self.assertNotIn("unrelated.txt", detail["text"])

    def test_index_and_working_content_are_distinct_and_inspection_is_read_only(self):
        path = self.repo / "setup.txt"
        path.write_text("Worker enabled\n")
        self.git("add", "--", "setup.txt")
        path.write_text("Worker disabled\n")
        before = (self.git("diff", "--cached", "--binary"), path.read_bytes())
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                code, result = self.call(name, "--mode", "diff", "--layer", "staged", "--path", "setup.txt")
                self.assertEqual(code, 0)
                self.assertIn("Worker enabled", result["text"])
                self.assertNotIn("Worker disabled", result["text"])
                self.assertEqual(before, (self.git("diff", "--cached", "--binary"), path.read_bytes()))

    def test_large_path_pages_recover_all_untracked_items(self):
        paths = [f"data-{n:03d}-한글 space.txt" for n in range(120)]
        for name in paths:
            (self.repo / name).write_text("Local data\n")
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                items, offset, pages = [], 0, 0
                while True:
                    code, page = self.call(name, "--mode", "files", "--offset", str(offset))
                    self.assertEqual(code, 0)
                    items.extend(item["path"] for item in page["items"])
                    pages += 1
                    if page["next_offset"] is None:
                        break
                    self.assertGreater(page["next_offset"], offset)
                    offset = page["next_offset"]
                self.assertGreater(pages, 1)
                self.assertEqual(sorted(items), sorted(paths))

    def test_failure_is_bounded_and_does_not_claim_an_empty_change(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                code, result = self.call(name, "--base", "nonexistent-reference", "--head", "HEAD")
                self.assertNotEqual(code, 0)
                self.assertIn("error", result)
                self.assertNotIn("counts", result)
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.head)


if __name__ == "__main__":
    unittest.main()
