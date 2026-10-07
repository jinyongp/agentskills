"""Exercise CLI installation ownership and updates through real Node subprocesses."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
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

    def run_cli(self, command, *args, success=True):
        result = subprocess.run(
            ["node", str(self.cli), command, *args, "--yes"],
            cwd=self.project,
            env={**os.environ, "HOME": str(self.home)},
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def skill(self, name, global_scope=False):
        return (self.home / ".codex/skills" if global_scope else self.project / ".agents/skills") / name

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
