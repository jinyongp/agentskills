"""Exercise release recovery with real local Git refs and simulated services."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import release


class ServiceCommands(release.Commands):
    """Only remote services are simulated; commits, tags and pushes use local Git."""

    def __init__(self, root, log):
        super().__init__(root, log)
        self.published = None
        self.runs = []
        self.calls = []
        self.check_failure = False
        self.push_failure = False
        self.registry_failure = False
        self.github_auth_failure = False
        self.fail_run = False
        self.dist_tag = "latest"

    def run(self, *argv, **options):
        self.calls.append(argv)
        code, output = 0, ""
        if argv[:3] == ("git", "remote", "get-url"):
            output = "https://github.com/example/skills.git"
        elif argv[:2] == ("git", "push"):
            if self.push_failure:
                raise release.ReleaseError("simulated push failure")
            result = super().run(*argv, **options)
            if not self.runs:
                head = super().text("git", "rev-parse", "HEAD")
                tag = argv[-1].removeprefix("refs/tags/")
                self.runs = [{"databaseId": 42, "headSha": head, "headBranch": tag,
                              "url": "https://example.test/run/42", "attempt": 1,
                              "status": "completed", "conclusion": "failure" if self.fail_run else "success"}]
            return result
        elif argv[:2] == ("uv", "run"):
            if self.check_failure:
                raise release.ReleaseError("simulated validation failure")
        elif argv[:2] == ("npm", "view"):
            if self.registry_failure:
                code, output = 1, '{"error":{"code":"E401"}}'
            elif "dist-tags" in argv:
                output = json.dumps({self.dist_tag: json.loads((self.root / "package.json").read_text())["version"]})
            elif self.published:
                output = json.dumps(self.published)
            else:
                code, output = 1, 'npm error code E404\n{"error":{"code":"E404"}}'
        elif argv[:2] == ("gh", "api"):
            if self.github_auth_failure:
                raise release.ReleaseError("simulated authentication failure")
            if "/releases/tags/" in argv[2]:
                tag = argv[2].split("/")[-1]
                output = json.dumps({"draft": False, "prerelease": "-" in tag,
                                     "html_url": "https://example.test/releases/" + tag})
            else:
                output = json.dumps({"default_branch": "main", "permissions": {"push": True}})
        elif argv[:3] == ("gh", "run", "list"):
            output = json.dumps(self.runs)
        elif argv[:3] == ("gh", "run", "view"):
            if "--log-failed" not in argv:
                output = json.dumps(self.runs[0])
                if self.runs[0]["conclusion"] == "success":
                    version = json.loads((self.root / "package.json").read_text())["version"]
                    self.published = {"version": version, "dist.integrity": "sha512-fixture",
                                      "gitHead": self.runs[0]["headSha"]}
        elif argv[:3] == ("gh", "run", "rerun"):
            self.runs[0].update(attempt=self.runs[0]["attempt"] + 1, conclusion="success")
        else:
            return super().run(*argv, **options)
        if code and options.get("check", True):
            raise release.ReleaseError("simulated service failure")
        return subprocess.CompletedProcess(argv, code, output)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "checkout"
        self.root.mkdir()
        self.remote = base / "remote.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Release Test")
        self.git("config", "user.email", "release@example.test")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        self.git("config", "core.hooksPath", str(base / "no-hooks"))
        self.git("remote", "add", "origin", str(self.remote))
        self.manifest = {"name": "@example/skills", "version": "0.1.0",
                         "repository": {"url": "https://github.com/example/skills.git"},
                         "publishConfig": {"access": "public"}, "files": ["skills/"]}
        self.write_manifest(self.manifest)
        workflow = self.root / ".github/workflows/publish-skills.yaml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("jobs:\n  publish:\n    steps:\n      - uses: releaseway/npm-actions@fixture\n")
        self.git("add", ".")
        self.git("commit", "-m", "Initial fixture")
        self.git("push", "origin", "main")
        self.initial = self.git("rev-parse", "HEAD")
        self.commands = ServiceCommands(self.root, base / "release.log")
        self.pack_patch = patch.object(release, "check_tarball")
        self.pack_check = self.pack_patch.start()
        self.addCleanup(self.pack_patch.stop)
        tools = patch.object(release.shutil, "which", return_value="/fixture/tool")
        tools.start()
        self.addCleanup(tools.stop)

    def git(self, *args):
        result = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def write_manifest(self, manifest):
        (self.root / "package.json").write_text(json.dumps(manifest, indent=2) + "\n")

    def run_release(self, version="0.2.0"):
        with redirect_stdout(io.StringIO()) as output:
            release.release(self.commands, version)
        return output.getvalue()

    def test_release_publishes_only_selected_branch_and_tag_and_retry_is_idempotent(self):
        self.git("tag", "-a", "unrelated-tag", "-m", "Unrelated release")
        self.git("config", "push.followTags", "true")
        output = self.run_release()
        head = self.git("rev-parse", "HEAD")
        self.assertNotEqual(head, self.initial)
        self.assertEqual(self.git("diff", "--name-only", self.initial, head), "package.json")
        self.assertEqual(self.git("status", "--porcelain"), "")
        refs = self.git("ls-remote", "origin")
        self.assertIn("refs/heads/main", refs)
        self.assertIn("refs/tags/v0.2.0", refs)
        self.assertNotIn("unrelated-tag", refs)
        self.assertIn("Released @example/skills@0.2.0 (latest)", output)
        self.assertEqual(release.remote_tag(self.commands, "v0.2.0"), head)
        self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertEqual(self.pack_check.call_count, 1)
        self.assertFalse(any(c[:3] == ("gh", "run", "rerun") for c in self.commands.calls))

    def test_dirty_or_staged_work_is_preserved_and_blocks_before_version_changes(self):
        for staged in (False, True):
            with self.subTest(staged=staged):
                note = self.root / "user-note.txt"
                note.write_text("user work")
                if staged:
                    self.git("add", "user-note.txt")
                with self.assertRaisesRegex(release.ReleaseError, "worktree is not clean"):
                    self.run_release()
                self.assertEqual(note.read_text(), "user work")
                self.assertEqual(json.loads((self.root / "package.json").read_text()), self.manifest)
                self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)
                self.git("reset", "--", "user-note.txt")
                note.unlink()

    def test_failed_checks_leave_only_resumable_manifest_change_and_no_tag(self):
        self.commands.check_failure = True
        with self.assertRaisesRegex(release.ReleaseError, "validation failure"):
            self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)
        self.assertEqual(self.git("tag", "--list", "v0.2.0"), "")
        self.assertEqual(json.loads((self.root / "package.json").read_text())["version"], "0.2.0")
        self.commands.check_failure = False
        self.run_release()
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_retry_after_push_failure_reuses_prepared_commit_and_tag(self):
        self.commands.push_failure = True
        with self.assertRaisesRegex(release.ReleaseError, "push failure"):
            self.run_release()
        prepared = self.git("rev-parse", "HEAD")
        self.assertEqual(self.git("rev-parse", "v0.2.0^{commit}"), prepared)
        self.assertIsNone(release.remote_tag(self.commands, "v0.2.0"))
        self.commands.push_failure = False
        # A previous manual or interrupted non-atomic push may have sent only main.
        self.git("push", "origin", "main")
        self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), prepared)
        self.assertEqual(self.pack_check.call_count, 1)

    def test_failed_run_is_reported_then_next_invocation_resumes_even_after_npm_publish(self):
        self.commands.fail_run = True
        with self.assertRaisesRegex(release.ReleaseError, "ended with failure"):
            self.run_release()
        head = self.git("rev-parse", "HEAD")
        self.commands.published = {"version": "0.2.0", "dist.integrity": "sha512-fixture", "gitHead": head}
        output = self.run_release()
        self.assertIn("Resuming", output)
        self.assertEqual(self.commands.runs[0]["attempt"], 2)
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

    def test_source_changes_after_a_tag_require_new_version(self):
        self.run_release()
        (self.root / "feature.txt").write_text("new work")
        self.git("add", "feature.txt")
        self.git("commit", "-m", "New feature")
        head = self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(release.ReleaseError, "Use a new version"):
            self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), head)

    def test_remote_tag_can_be_resumed_when_the_local_tag_is_missing(self):
        self.run_release()
        tag_object = self.git("rev-parse", "refs/tags/v0.2.0")
        self.git("tag", "-d", "v0.2.0")
        self.run_release()
        self.assertEqual(self.git("rev-parse", "refs/tags/v0.2.0"), tag_object)
        self.assertEqual(self.pack_check.call_count, 1)

    def test_concurrent_work_during_checks_stops_before_commit_or_push(self):
        def add_work(*args):
            (self.root / "user-note.txt").write_text("concurrent user work")
        self.pack_check.side_effect = add_work
        with self.assertRaisesRegex(release.ReleaseError, "worktree is not clean"):
            self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)
        self.assertIsNone(release.remote_tag(self.commands, "v0.2.0"))
        self.assertEqual((self.root / "user-note.txt").read_text(), "concurrent user work")

    def test_preflight_does_not_overwrite_concurrent_manifest_edit(self):
        changed = {**self.manifest, "description": "concurrent user choice"}
        def edit_during_lookup(*args):
            self.write_manifest(changed)
            return None
        with patch.object(release, "published_version", side_effect=edit_during_lookup):
            with self.assertRaisesRegex(release.ReleaseError, "beyond this release"):
                self.run_release()
        self.assertEqual(json.loads((self.root / "package.json").read_text()), changed)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)

    def test_hook_changes_cannot_publish_unvalidated_source(self):
        hooks = self.root / ".git/hooks"
        self.git("config", "core.hooksPath", str(hooks))
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\nprintf 'hook change' > unexpected.txt\ngit add unexpected.txt\n")
        hook.chmod(0o755)
        with self.assertRaisesRegex(release.ReleaseError, "more than release metadata"):
            self.run_release()
        self.assertIsNone(release.remote_tag(self.commands, "v0.2.0"))
        self.assertEqual((self.root / "unexpected.txt").read_text(), "hook change")

    def test_remote_divergence_and_tag_conflicts_stop_without_mutation(self):
        # Two independent descendants model a concurrent maintainer push.
        (self.root / "remote.txt").write_text("remote work")
        self.git("add", ".")
        self.git("commit", "-m", "Remote work")
        self.git("push", "origin", "main")
        self.git("reset", "--hard", self.initial)
        (self.root / "local.txt").write_text("local work")
        self.git("add", ".")
        self.git("commit", "-m", "Local work")
        head = self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(release.ReleaseError, "behind or diverged"):
            self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), head)
        self.assertEqual(json.loads((self.root / "package.json").read_text())["version"], "0.1.0")
        self.git("fetch", "origin", "main")
        self.git("reset", "--hard", "FETCH_HEAD")
        self.git("tag", "v0.2.0", self.initial)
        with self.assertRaisesRegex(release.ReleaseError, "existing release tag"):
            self.run_release()

    def test_registry_and_authentication_failures_are_not_treated_as_absence(self):
        self.commands.registry_failure = True
        with self.assertRaisesRegex(release.ReleaseError, "could not establish"):
            self.run_release()
        self.commands.registry_failure = False
        self.commands.github_auth_failure = True
        with self.assertRaisesRegex(release.ReleaseError, "authentication failure"):
            self.run_release()
        self.assertEqual(json.loads((self.root / "package.json").read_text()), self.manifest)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)

    def test_prerelease_uses_next_and_stable_release_removes_it(self):
        self.commands.dist_tag = "next"
        self.run_release("0.2.0-rc.1")
        self.assertEqual(json.loads((self.root / "package.json").read_text())["publishConfig"], {"access": "public", "tag": "next"})
        self.commands.dist_tag = "latest"
        self.commands.published = None
        self.commands.runs = []
        self.run_release("0.2.0")
        self.assertEqual(json.loads((self.root / "package.json").read_text())["publishConfig"], {"access": "public"})

    def test_ambiguous_preparation_edits_and_published_version_without_tag_are_rejected(self):
        manifest = release.release_manifest(self.manifest, "0.2.0")
        manifest["description"] = "unrelated change"
        self.write_manifest(manifest)
        with self.assertRaisesRegex(release.ReleaseError, "beyond this release"):
            self.run_release()
        self.write_manifest(self.manifest)
        self.commands.published = {"version": "0.2.0", "dist.integrity": "sha512-fixture"}
        with self.assertRaisesRegex(release.ReleaseError, "already published"):
            self.run_release()
        self.assertEqual(self.git("rev-parse", "HEAD"), self.initial)


class ReleaseCommandTests(unittest.TestCase):
    def test_help_and_invalid_versions_have_no_side_effects(self):
        script = Path(release.__file__)
        for version in ("--help", "v0.2.0", "01.2.0", "0.2.0-01", "0.2.0+build", "--bad"):
            with self.subTest(version=version):
                result = subprocess.run([sys.executable, str(script), version], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if version == "--help" else 2)
                self.assertNotIn("Preparing", result.stdout)
        self.assertEqual(release.version_argument("0.2.0-rc.1"), "0.2.0-rc.1")
        self.assertLess(release.version_key("0.2.0-rc.2"), release.version_key("0.2.0-rc.10"))
        self.assertLess(release.version_key("0.2.0-rc.10"), release.version_key("0.2.0"))

    def test_noisy_output_stays_in_log_and_truncated_status_is_never_clean(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            commands = release.Commands(root, root / "release.log")
            noisy = (sys.executable, "-c", "print('x' * 1100000)")
            result = commands.run(*noisy)
            self.assertIsNone(result.stdout)
            self.assertGreater(commands.log.stat().st_size, 1100000)
            with self.assertRaisesRegex(release.ReleaseError, "exceeds 1 MB"):
                commands.text(*noisy)
            with patch.object(commands, "run", return_value=result):
                with self.assertRaisesRegex(release.ReleaseError, "inspection exceeds"):
                    release.working_tree(commands)

    def test_timed_out_command_fails_with_recovery_instruction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(release.ReleaseError, "Rerun the same release command"):
                release.Commands(root, root / "release.log").run(sys.executable, "-c", "import time; time.sleep(10)", timeout=0.05)

    def test_run_discovery_timeout_and_wrong_commit_are_not_success(self):
        commands = unittest.mock.Mock()
        commands.json.return_value = []
        with patch.object(release.time, "monotonic", side_effect=[0, 121]):
            with self.assertRaisesRegex(release.ReleaseError, "has not appeared"):
                release.wait_for_run(commands, "example/skills", "release.yml", "v0.2.0", "expected")
        commands.json.return_value = [{"headSha": "different", "headBranch": "v0.2.0"}]
        with self.assertRaisesRegex(release.ReleaseError, "does not match"):
            release.wait_for_run(commands, "example/skills", "release.yml", "v0.2.0", "expected")

    def test_retry_waits_for_new_attempt_and_an_active_run_is_not_rerun(self):
        for retry in (True, False):
            with self.subTest(retry=retry):
                commands = unittest.mock.Mock()
                run = {"headSha": "expected", "headBranch": "v0.2.0", "databaseId": 42,
                       "url": "https://example.test/run/42", "attempt": 1,
                       "status": "completed" if retry else "in_progress", "conclusion": "failure"}
                finished = {**run, "status": "completed", "conclusion": "success", "attempt": 2 if retry else 1}
                commands.json.side_effect = [[run], run, finished]
                with patch.object(release.time, "sleep"):
                    result = release.wait_for_run(commands, "example/skills", "release.yml", "v0.2.0", "expected", retry_failed=retry)
                self.assertEqual(result["conclusion"], "success")
                reruns = [c for c in commands.run.call_args_list if c.args[:3] == ("gh", "run", "rerun")]
                self.assertEqual(len(reruns), 1 if retry else 0)

    def test_package_allowlist_rejects_maintainer_files_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            commands = unittest.mock.Mock(root=Path(directory))
            commands.json.return_value = [{"name": "@example/skills", "version": "0.2.0",
                                           "files": [{"path": "release.py"}]}]
            with self.assertRaisesRegex(release.ReleaseError, "Unexpected packaged file: release.py"):
                release.check_tarball(commands, {"name": "@example/skills", "version": "0.2.0", "files": ["skills/"]})
            commands.run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
