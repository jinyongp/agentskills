"""Verify bounded, read-only Git inspection against real temporary repositories."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/git/git-commit/scripts/inspect_worktree.py"
ENV = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}


class GitInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Inspection Test")
        self.git("config", "user.email", "inspection@example.invalid")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args, ok=True):
        result = subprocess.run(["git", "-C", str(self.repo), *args], env=ENV, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def inspect(self, *args, repo=None, success=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args, "--repo", str(repo or self.repo)],
            env=ENV, capture_output=True, text=True,
        )
        self.assertLessEqual(len(result.stdout), 4000)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.returncode == 0, success, result.stdout)
        return json.loads(result.stdout)

    def seed(self):
        (self.repo / "tracked.txt").write_text("base\n")
        self.git("add", ".")
        self.git("commit", "-m", "feat: initialize fixture")

    def test_unborn_and_unset_template_are_normal(self):
        data = self.inspect()
        self.assertEqual(data["head"], "(initial)")
        self.assertEqual(data["recent_subjects"], [])
        self.assertFalse(data["template_present"])
        self.assertIsNone(data["ahead"])
        self.assertIsNone(data["behind"])
        self.assertEqual(self.inspect("template"), {"mode": "template", "present": False})

    def test_summary_is_read_only_and_excludes_contents(self):
        self.seed()
        path = self.repo / "tracked.txt"
        path.write_text("STAGED_PRIVATE_VALUE\n")
        self.git("add", "--", "tracked.txt")
        path.write_text("UNSTAGED_PRIVATE_VALUE\n")
        (self.repo / ".env").write_text("DO_NOT_PRINT_THIS_VALUE\n")
        hook = self.repo / '.git/fsmonitor-test'
        hook.write_text('#!/bin/sh\n: > "$0.marker"\nprintf "token\\0/\\0"\n')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', str(hook))
        index = (self.repo / ".git/index").read_bytes()
        head = self.git("rev-parse", "HEAD")
        data = self.inspect()
        self.assertFalse(Path(str(hook) + '.marker').exists())
        self.assertEqual(data["counts"], {"staged": 1, "unstaged": 1, "untracked": 1, "conflicted": 0})
        self.assertNotIn("PRIVATE_VALUE", json.dumps(data))
        self.assertNotIn("DO_NOT_PRINT", json.dumps(data))
        self.assertEqual((self.repo / ".git/index").read_bytes(), index)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertEqual(path.read_text(), "UNSTAGED_PRIVATE_VALUE\n")

    def test_large_file_list_is_complete_through_pages(self):
        for i in range(140):
            (self.repo / f"{i:03}-{'한' * 30}.txt").touch()
        summary = self.inspect()
        self.assertEqual(summary["counts"]["untracked"], 140)
        self.assertIsNotNone(summary["files"]["next_offset"])
        seen, offset = [], 0
        while offset is not None:
            page = self.inspect("files", "--offset", str(offset), "--limit", "100")["files"]
            seen.extend(item["path"] for item in page["items"])
            offset = page["next_offset"]
        self.assertEqual(len(seen), 140)
        self.assertEqual(len(set(seen)), 140)

    def test_selected_diff_pages_reassemble_exactly(self):
        self.seed()
        text = "".join(f"line {i}: 한글\\\"\n" for i in range(400))
        (self.repo / "tracked.txt").write_text(text)
        expected = self.git("diff", "--no-ext-diff", "--no-textconv", "--no-color", "--", "tracked.txt").decode()
        chunks, offset = [], 0
        while offset is not None:
            page = self.inspect("diff", "--path", "tracked.txt", "--offset", str(offset))
            chunks.append(page["text"])
            offset = page["next_offset"]
        self.assertEqual("".join(chunks), expected)
        self.assertIn("requires --path", self.inspect("diff", success=False)["error"])
        self.assertIn("relative", self.inspect("diff", "--path", ".", success=False)["error"])

    def test_staged_diff_does_not_absorb_working_changes(self):
        self.seed()
        (self.repo / "tracked.txt").write_text("staged\n")
        self.git("add", "--", "tracked.txt")
        (self.repo / "tracked.txt").write_text("working\n")
        page = self.inspect("diff", "--path", "tracked.txt", "--staged")
        self.assertIn("+staged", page["text"])
        self.assertNotIn("+working", page["text"])

    def test_rename_and_unusual_names_keep_exact_paths(self):
        self.seed()
        unusual = "space 한글\n[bracket]*.txt"
        self.git("mv", "--", "tracked.txt", unusual)
        data = self.inspect()
        entry = data["files"]["items"][0]
        self.assertEqual(entry["path"], unusual)
        self.assertEqual(entry["from"], "tracked.txt")
        page = self.inspect("diff", "--staged", "--path", unusual)
        self.assertTrue(page["text"])

    def test_conflict_and_operation_are_visible(self):
        self.seed()
        self.git("switch", "-c", "feature")
        (self.repo / "tracked.txt").write_text("feature\n")
        self.git("commit", "-am", "feat: feature")
        self.git("switch", "main")
        (self.repo / "tracked.txt").write_text("main\n")
        self.git("commit", "-am", "feat: main")
        self.git("merge", "feature", ok=False)
        data = self.inspect()
        self.assertEqual(data["counts"]["conflicted"], 1)
        self.assertIn("merge", data["operations"])
        self.assertTrue(data["files"]["items"][0]["conflict"])

    def test_linked_worktree_and_detached_head(self):
        self.seed()
        linked = Path(self.temp.name) / "linked"
        self.git("worktree", "add", "--detach", str(linked), "HEAD")
        data = self.inspect(repo=linked)
        self.assertEqual(data["branch"], "(detached)")
        self.assertEqual(Path(data["repository"]), linked)
        self.assertEqual(data["operations"], [])

    def test_template_is_opt_in_and_paged(self):
        self.seed()
        template = self.repo / "message.tmpl"
        template.write_text("# omit comment\nRequired footer\n" + "x" * 8000)
        self.git("config", "commit.template", str(template))
        summary = self.inspect()
        self.assertTrue(summary["template_present"])
        self.assertNotIn("Required footer", json.dumps(summary))
        page = self.inspect("template")
        self.assertNotIn("omit comment", page["text"])
        self.assertIn("Required footer", page["text"])
        self.assertIsNotNone(page["next_offset"])
        template.unlink()
        self.assertIn("unreadable", self.inspect("template", success=False)["error"])

    def test_long_history_is_explicitly_truncated(self):
        self.seed()
        self.git("commit", "--allow-empty", "-m", "docs: " + "한" * 1000)
        summary = self.inspect()
        self.assertTrue(summary["recent_subjects"][0]["truncated"])
        self.assertIsNotNone(self.inspect("history")["next_offset"])

    def test_invalid_repository_and_offsets_fail_cleanly(self):
        self.assertIn("failed", self.inspect(repo=Path(self.temp.name), success=False)["error"])
        self.assertIn("offset", self.inspect("files", "--offset", "10", success=False)["error"])
        self.assertIn("offset", self.inspect("--offset", "-1", success=False)["error"])
        self.assertIn("invalid", self.inspect("x" * 10000, success=False)["error"])


if __name__ == "__main__":
    unittest.main()
