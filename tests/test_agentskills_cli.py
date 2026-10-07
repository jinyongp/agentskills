"""Exercise CLI installation ownership and updates through real Node subprocesses."""

import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AgentskillsCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.project = self.root / "project"
        self.home = self.root / "home"
        for directory in (self.source, self.project, self.home):
            directory.mkdir()
        shutil.copyfile(ROOT / "agentskills.js", self.source / "agentskills.js")
        shutil.copyfile(ROOT / "package.json", self.source / "package.json")
        (self.source / "rules").mkdir()
        (self.source / "rules/base.md").write_text("# Shared rules\nRespect agreed scope.\n")
        for name in ("alpha", "beta"):
            skill = self.source / "skills/workflow" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text(f"---\nname: {name}\n---\nInitial guidance.\n")
            (skill / "LICENSE").write_text("Fixture license\n")
            (skill / "references").mkdir()
            (skill / "references/detail.md").write_text("Bundled detail\n")
        self.cli = self.source / "agentskills.js"

    def run_cli(self, command, *args, success=True, env_extra=None):
        result = subprocess.run(
            ["node", str(self.cli), command, *args, *(["--yes"] if command in ("add", "update", "remove") else [])],
            cwd=self.project,
            env={**os.environ, "HOME": str(self.home), **(env_extra or {})},
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def skill(self, name, global_scope=False):
        return (self.home / ".codex/skills" if global_scope else self.project / ".agents/skills") / name

    def test_help_examples_execute_with_current_catalog_and_package_entrypoint(self):
        package_file = self.source / "package.json"
        package = json.loads(package_file.read_text())
        package["bin"] = {"fixture-skills": "agentskills.js"}
        package_file.write_text(json.dumps(package))
        for old, new in (("alpha", "delta"), ("beta", "epsilon")):
            directory = self.source / "skills/workflow" / old
            directory.rename(directory.with_name(new))
        for topic in (None, "add", "update", "remove", "list"):
            result = self.run_cli(topic, "--help") if topic else self.run_cli("--help")
            examples = result.stdout.split("Examples:\n", 1)[1].split("\n\n", 1)[0].splitlines()
            for example in examples:
                with self.subTest(topic=topic, example=example):
                    self.run_cli("add", "--agent", "codex")
                    self.run_cli("add", "--agent", "codex", "--global")
                    binary, command, *args = shlex.split(example)
                    self.assertEqual(binary, "fixture-skills")
                    if command == "add" and "--agent" not in args:
                        args += ["--agent", "codex"]
                    self.run_cli(command, *args)
                    state = json.loads((self.project / ".agents/agentskills.json").read_text())
                    expected = {"epsilon"} if command == "remove" and "--skill" in args else {"delta", "epsilon"}
                    self.assertEqual(set(state["agents"]["codex"]["skills"]), expected)
                    self.run_cli("remove")
                    if command != "remove" or "--global" not in args:
                        self.run_cli("remove", "--global")

    def test_noninteractive_retry_preserves_scope_selection_and_shell_quoting(self):
        project = self.root / "project's retry space"
        project.mkdir()
        for scope_args, base in ((["--global"], self.home), (["--project", str(project)], project)):
            with self.subTest(scope=scope_args):
                result = subprocess.run(
                    ["node", str(self.cli), "add", "-a", "claude", *scope_args, "-s", "beta", "--no-rules"],
                    cwd=self.project, env={**os.environ, "HOME": str(self.home)},
                    capture_output=True, text=True, timeout=20,
                )
                self.assertNotEqual(result.returncode, 0)
                advice = result.stderr.split("Retry with ", 1)[1].split(", or run in a terminal", 1)[0]
                _, command, *args = shlex.split(advice)
                self.run_cli(command, *args)
                installed = base / ".claude/skills"
                self.assertEqual({entry.name for entry in installed.iterdir()}, {"beta"})
                rules = base / (".claude/CLAUDE.md" if base == self.home else "CLAUDE.md")
                self.assertFalse(rules.exists())
                self.assertFalse((self.project / ".claude").exists())

    def test_aliases_install_selected_global_skill_and_list_rejects_mutation_flags(self):
        self.run_cli("add", "-a", "codex", "-g", "-s", "beta", "-y", "--no-rules")
        self.assertTrue(self.skill("beta", global_scope=True).exists())
        self.assertFalse(self.skill("alpha", global_scope=True).exists())
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())
        for args in (("--yes",), ("--skill", "beta"), ("--rules-only",)):
            self.run_cli("list", *args, success=False)
        self.run_cli("list", "-a", "codex", "-g")

    def confirm_after(self, args, mutate, response=b"y\n", wait_for=b"Apply? [y/N]"):
        import pty
        import select

        master, slave = pty.openpty()
        process = subprocess.Popen(
            ["node", str(self.cli), *args], cwd=self.project,
            stdin=slave, stdout=slave, stderr=slave,
        )
        os.close(slave)
        try:
            output = b""
            deadline = time.monotonic() + 10
            while wait_for not in output:
                self.assertLess(time.monotonic(), deadline, output)
                if select.select([master], [], [], 0.1)[0]:
                    output += os.read(master, 65536)
            mutate()
            os.write(master, response)
            return process.wait(timeout=10)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            os.close(master)

    def test_round_trip_updates_saved_selections_and_preserves_project_prose(self):
        original = b"# Project instructions\n\nPreserve this exact text, without a final newline."
        rules = self.project / "AGENTS.md"
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        self.assertFalse(self.skill("beta").exists())
        self.assertEqual((self.skill("alpha") / "LICENSE").read_text(), "Fixture license\n")
        self.run_cli("add", "--agent", "codex", "--skill", "beta")
        source = self.source / "skills/workflow/alpha"
        (source / "references/detail.md").unlink()
        (source / "references/new.md").write_text("Changed public guidance\n")
        (self.source / "rules/base.md").write_text("New shared rules\n")
        self.run_cli("update")
        self.assertFalse((self.skill("alpha") / "references/detail.md").exists())
        self.assertEqual((self.skill("alpha") / "references/new.md").read_text(), "Changed public guidance\n")
        self.assertIn("New shared rules", rules.read_text())
        self.run_cli("remove", "--skill", "alpha", "--no-rules")
        self.assertTrue(self.skill("beta").exists())
        self.assertIn("New shared rules", rules.read_text())
        self.run_cli("remove")
        self.assertFalse(self.skill("beta").exists())
        self.assertEqual(rules.read_bytes(), original)

    def test_preflight_conflict_preserves_all_selected_skills(self):
        self.run_cli("add", "--agent", "codex")
        modified = self.skill("beta") / "references/detail.md"
        modified.write_text("User edit\n")
        before = (self.skill("alpha") / "SKILL.md").read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New alpha version\n")
        self.run_cli("update", success=False)
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_bytes(), before)
        self.run_cli("remove", success=False)
        self.assertEqual(modified.read_text(), "User edit\n")
        modified.write_text("Bundled detail\n")
        (self.skill("beta") / "user-note.txt").write_text("Additional user file\n")
        self.run_cli("remove", success=False)
        self.assertTrue(self.skill("alpha").exists())

    def test_unowned_skill_and_rules_blocks_are_never_adopted(self):
        target = self.skill("alpha")
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("Someone else's skill\n")
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
        self.assertEqual((target / "SKILL.md").read_text(), "Someone else's skill\n")
        self.assertFalse((self.project / "AGENTS.md").exists())
        original = "<!-- agentskills:rules:start -->\nExisting rules\n<!-- agentskills:rules:end -->\n"
        (self.project / "AGENTS.md").write_text(original)
        self.run_cli("add", "--agent", "codex", "--rules-only", success=False)
        self.assertEqual((self.project / "AGENTS.md").read_text(), original)

    def test_rules_edits_and_damaged_markers_block_updates_and_removal(self):
        self.run_cli("add", "--agent", "codex", "--rules-only")
        rules = self.project / "AGENTS.md"
        original = rules.read_text()
        for modified in (
            original.replace("Respect agreed scope.", "User's rules."),
            original.replace("<!-- agentskills:rules:end -->", ""),
            original + "<!-- agentskills:rules:start -->",
        ):
            with self.subTest(modified=modified):
                rules.write_text(modified)
                self.run_cli("update", success=False)
                self.run_cli("remove", success=False)
                self.assertEqual(rules.read_text(), modified)

    def test_global_and_agent_scopes_are_isolated(self):
        self.run_cli("add", "--agent", "codex", "--global", "--skill", "alpha")
        self.run_cli("add", "--agent", "claude", "--rules-only")
        self.assertTrue(self.skill("alpha", global_scope=True).exists())
        self.assertFalse(self.skill("alpha").exists())
        self.assertTrue((self.home / ".codex/AGENTS.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").exists())
        self.run_cli("update", "--global")
        self.run_cli("remove", "--global")
        self.assertFalse((self.home / ".codex/AGENTS.md").exists())
        self.assertTrue((self.project / "CLAUDE.md").exists())
        self.run_cli("remove")
        self.assertFalse((self.project / "CLAUDE.md").exists())

    def test_symlinked_parents_and_installed_files_are_left_untouched(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        self.run_cli("add", "--agent", "codex", success=False)
        self.assertEqual(list(outside.iterdir()), [])
        (self.project / ".agents").unlink()
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        target = self.skill("alpha") / "references/detail.md"
        target.unlink()
        external = outside / "detail.md"
        external.write_text("Outside the installation\n")
        target.symlink_to(external)
        self.run_cli("update", success=False)
        self.run_cli("remove", success=False)
        self.assertEqual(external.read_text(), "Outside the installation\n")

    def test_invalid_selection_and_busy_lock_do_not_install(self):
        self.run_cli("add", "--agent", "codex", "--skill", "unknown", success=False)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertFalse((self.project / ".agents/skills").exists())
        self.run_cli("add", "--agent", "codex", "--skill", "../escape", success=False)
        lock = self.project / ".agents/agentskills.json.lock"
        lock.write_text("Another operation\n")
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
        self.assertEqual(lock.read_text(), "Another operation\n")
        lock.unlink()
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        state = json.loads((self.project / ".agents/agentskills.json").read_text())
        self.assertEqual(set(state["agents"]["codex"]["skills"]), {"alpha"})

    @unittest.skipUnless(os.name == "posix", "Interactive PTY checks require POSIX")
    def test_changes_during_confirmation_abort_before_mutating_any_item(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        installed = self.skill("alpha") / "SKILL.md"
        rules = self.project / "AGENTS.md"
        state = self.project / ".agents/agentskills.json"
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New version\n")
        for edited in (installed, rules, state):
            with self.subTest(edited=edited.name):
                originals = {file: file.read_bytes() for file in (installed, rules, state)}
                try:
                    result = self.confirm_after(["update"], lambda: edited.write_bytes(originals[edited] + b"\nUser edit while pending\n"))
                    self.assertNotEqual(result, 0)
                    for file, original in originals.items():
                        self.assertEqual(file.read_bytes(), original + (b"\nUser edit while pending\n" if file == edited else b""))
                finally:
                    for file, original in originals.items():
                        file.write_bytes(original)

    @unittest.skipUnless(os.name == "posix", "Interactive PTY checks require POSIX")
    def test_parent_redirect_during_confirmation_does_not_touch_outside_files(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        outside = self.root / "outside"
        outside.mkdir()
        lock = outside / "agentskills.json.lock"
        lock.write_text("Unrelated lock\n")
        original = (self.skill("alpha") / "SKILL.md").read_bytes()

        def redirect():
            (self.project / ".agents").rename(self.project / ".agents-original")
            (self.project / ".agents").symlink_to(outside, target_is_directory=True)

        self.assertNotEqual(self.confirm_after(["update"], redirect), 0)
        self.assertEqual({file.name for file in outside.iterdir()}, {"agentskills.json.lock"})
        self.assertEqual(lock.read_text(), "Unrelated lock\n")
        self.assertEqual((self.project / ".agents-original/skills/alpha/SKILL.md").read_bytes(), original)

    def test_record_write_failure_rolls_back_install_update_and_removal(self):
        state = self.project / ".agents/agentskills.json"
        preload = self.root / "fail-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))})"
            "{throw new Error('Injected record write failure');}"
            "return rename.apply(this,arguments);};\n"
        )
        injected = {"NODE_OPTIONS": f"--require={preload}"}
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules", success=False, env_extra=injected)
        self.assertFalse(self.skill("alpha").exists())
        self.assertFalse(state.exists())
        self.run_cli("add", "--agent", "codex", "--skill", "alpha", "--no-rules")
        installed = self.skill("alpha") / "SKILL.md"
        original = installed.read_bytes()
        original_state = state.read_bytes()
        (self.source / "skills/workflow/alpha/SKILL.md").write_text("New guidance\n")
        self.run_cli("update", "--no-rules", success=False, env_extra=injected)
        self.assertEqual(installed.read_bytes(), original)
        self.assertEqual(state.read_bytes(), original_state)
        self.run_cli("update", "--no-rules")
        self.assertEqual(installed.read_text(), "New guidance\n")
        before_remove = state.read_bytes()
        self.run_cli("remove", "--no-rules", success=False, env_extra=injected)
        self.assertEqual(installed.read_text(), "New guidance\n")
        self.assertEqual(state.read_bytes(), before_remove)
        self.run_cli("remove", "--no-rules")
        self.assertFalse(self.skill("alpha").exists())

    def test_record_failure_restores_shared_rules_and_retry_succeeds(self):
        state = self.project / ".agents/agentskills.json"
        preload = self.root / "fail-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))})"
            "{throw new Error('Injected record write failure');}"
            "return rename.apply(this,arguments);};\n"
        )
        injected = {"NODE_OPTIONS": f"--require={preload}"}
        rules = self.project / "AGENTS.md"
        original = b"# Keep project instructions\n"
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--rules-only", success=False, env_extra=injected)
        self.assertEqual(rules.read_bytes(), original)
        self.run_cli("add", "--agent", "codex", "--rules-only")
        installed = rules.read_bytes()
        before_remove = state.read_bytes()
        self.run_cli("remove", success=False, env_extra=injected)
        self.assertEqual(rules.read_bytes(), installed)
        self.assertEqual(state.read_bytes(), before_remove)
        self.run_cli("remove")
        self.assertEqual(rules.read_bytes(), original)

    def test_non_utf8_rules_are_rejected_before_install_and_bom_is_preserved(self):
        rules = self.project / "AGENTS.md"
        for original in ("# Existing instructions\n".encode("utf-16"), b"# Existing\n\xff\xfe"):
            with self.subTest(original=original):
                rules.write_bytes(original)
                self.run_cli("add", "--agent", "codex", "--skill", "alpha", success=False)
                self.assertEqual(rules.read_bytes(), original)
                self.assertFalse(self.skill("alpha").exists())
        original = b"\xef\xbb\xbf" + "# Project instructions\nNon-ASCII: café\n".encode()
        rules.write_bytes(original)
        self.run_cli("add", "--agent", "codex", "--rules-only")
        self.run_cli("remove")
        self.assertEqual(rules.read_bytes(), original)

    def test_prototype_name_is_an_exact_selection_not_an_inherited_entry(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        rules = self.project / "AGENTS.md"
        original = rules.read_bytes()
        self.run_cli("remove", "--skill", "constructor", success=False)
        self.run_cli("add", "--agent", "codex", "--skill", "constructor", success=False)
        self.assertEqual(rules.read_bytes(), original)
        extra = self.skill("alpha") / "__proto__"
        extra.write_text("Additional user file\n")
        self.run_cli("update", "--no-rules", success=False)
        self.run_cli("remove", "--no-rules", success=False)
        self.assertEqual(extra.read_text(), "Additional user file\n")
        extra.unlink()
        source = self.source / "skills/workflow/constructor"
        shutil.copytree(self.source / "skills/workflow/alpha", source)
        unowned = self.skill("constructor")
        unowned.mkdir()
        self.run_cli("add", "--agent", "codex", "--skill", "constructor", success=False)
        unowned.rmdir()
        self.run_cli("add", "--agent", "codex", "--skill", "constructor")
        self.assertTrue((unowned / "SKILL.md").exists())
        self.run_cli("remove", "--skill", "constructor", "--no-rules")
        self.assertFalse(unowned.exists())
        self.assertTrue(self.skill("alpha").exists())
        self.assertEqual(rules.read_bytes(), original)

    def test_help_aliases_are_side_effect_free_and_support_each_command(self):
        root_help = self.run_cli("--help")
        self.assertTrue(root_help.stdout.strip())
        self.assertEqual(root_help.stderr, "")
        for args in (("-h",), ("help",), ("help", "--help")):
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(*args).stdout, root_help.stdout)
        for command in ("add", "update", "remove", "list"):
            with self.subTest(command=command):
                by_flag = self.run_cli(command, "--help", "--project", str(self.root / "missing"), "--agent", "invalid")
                by_command = self.run_cli("help", command)
                self.assertTrue(by_flag.stdout.strip())
                self.assertEqual(by_flag.stdout, by_command.stdout)
                self.assertEqual(by_flag.stderr, "")
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])

    @unittest.skipUnless(os.name == "posix", "Interactive PTY checks require POSIX")
    def test_cancelling_confirmation_does_not_leave_a_lock_or_change_files(self):
        self.run_cli("add", "--agent", "codex", "--skill", "alpha")
        state = self.project / ".agents/agentskills.json"
        original = state.read_bytes()
        for response, expected in ((b"n\n", 0), (b"\x03", 130)):
            with self.subTest(response=response):
                self.assertEqual(self.confirm_after(["remove"], lambda: None, response=response), expected)
                self.assertEqual(state.read_bytes(), original)
                self.assertTrue(self.skill("alpha").exists())
                self.assertFalse((self.project / ".agents/agentskills.json.lock").exists())
        self.run_cli("update")

    @unittest.skipUnless(os.name == "posix", "Interactive PTY checks require POSIX")
    def test_invalid_interactive_scope_cannot_fall_back_to_project_install(self):
        result = self.confirm_after(["add", "--agent", "codex"], lambda: None, response=b"globla\n", wait_for=b"Scope [")
        self.assertNotEqual(result, 0)
        self.assertEqual(list(self.project.iterdir()), [])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_failure_after_one_completed_item_preserves_that_progress_and_can_retry(self):
        self.run_cli("add", "--agent", "codex", "--no-rules")
        state = self.project / ".agents/agentskills.json"
        for name in ("alpha", "beta"):
            (self.source / "skills/workflow" / name / "SKILL.md").write_text(f"Updated {name}\n")
        preload = self.root / "fail-second-record.cjs"
        preload.write_text(
            "const fs=require('node:fs');const rename=fs.renameSync;let count=0;"
            f"fs.renameSync=function(a,b){{if(b==={json.dumps(str(state))}&&++count===2)"
            "{throw new Error('Injected second record write failure');}"
            "return rename.apply(this,arguments);};\n"
        )
        result = self.run_cli("update", "--no-rules", success=False, env_extra={"NODE_OPTIONS": f"--require={preload}"})
        self.assertEqual((self.skill("alpha") / "SKILL.md").read_text(), "Updated alpha\n")
        self.assertNotEqual((self.skill("beta") / "SKILL.md").read_text(), "Updated beta\n")
        self.assertIn(str(state), result.stderr)
        self.run_cli("update", "--no-rules")
        self.assertEqual((self.skill("beta") / "SKILL.md").read_text(), "Updated beta\n")
