"""Check scaffold creation, catalog updates, and protection of existing content."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from skills_ref import read_properties

from new_skill import prepare_skill
from scripts.validate_skills import validate_repository


ROOT = Path(__file__).resolve().parents[1]


class NewSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copyfile(ROOT / "README.md", self.root / "README.md")
        shutil.copytree(ROOT / "templates", self.root / "templates")
        (self.root / "evals").mkdir()
        for category in (ROOT / "skills").iterdir():
            if category.is_dir():
                target = self.root / "skills" / category.name
                target.mkdir(parents=True)
                shutil.copyfile(category / "README.md", target / "README.md")

    def snapshot(self):
        return {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def test_creates_valid_skill_evaluation_and_catalog_links(self):
        skill = prepare_skill(self.root, "frontend", "solid-review")
        properties = read_properties(skill)
        self.assertEqual(properties.name, "solid-review")
        self.assertEqual(properties.metadata["category"], "frontend")
        self.assertEqual(validate_repository(self.root), (1, []))
        self.assertTrue((self.root / "evals" / "solid-review" / "README.md").is_file())
        row = next(
            row for row in (self.root / "README.md").read_text().splitlines()
            if row.startswith("| [frontend](skills/frontend/README.md) |")
        )
        self.assertEqual(int(row.split("|")[3].strip()), 1)
        self.assertIn("[solid-review](solid-review/SKILL.md)", (skill.parent / "README.md").read_text())
        self.assertEqual(list(skill.iterdir()), [skill / "SKILL.md"])

    def test_description_round_trips_yaml_and_does_not_break_catalog_blocks(self):
        description = 'Review Solid: "state" | rendering.\nUse for <!-- skills:end --> examples and C:\\code.'
        skill = prepare_skill(self.root, "frontend", "solid-review", description)
        self.assertEqual(read_properties(skill).description, description)
        prepare_skill(self.root, "frontend", "solid-debug")
        self.assertEqual(validate_repository(self.root), (2, []))
        catalog = (skill.parent / "README.md").read_text()
        self.assertEqual(catalog.count("<!-- skills:start -->"), 1)
        self.assertEqual(catalog.count("<!-- skills:end -->"), 1)
        self.assertIn("&lt;!-- skills:end --&gt;", catalog)

    def test_first_skill_replaces_empty_catalog_without_losing_install_guidance(self):
        category = self.root / "skills" / "tooling" / "README.md"
        category.write_text(category.read_text() + "\nLocal installation notes.\n")
        skill = prepare_skill(self.root, "tooling", "setup-check")
        content = category.read_text()
        self.assertIn("[setup-check](setup-check/SKILL.md)", content)
        self.assertNotIn("No skills yet.", content)
        self.assertIn("Local installation notes.", content)
        self.assertEqual(read_properties(skill).name, "setup-check")
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_multiple_additions_preserve_catalogs_and_refresh_counts(self):
        category = self.root / "skills" / "workflow" / "README.md"
        catalog = self.root / "README.md"
        original_row = next(
            row for row in catalog.read_text().splitlines()
            if row.startswith("| [workflow](skills/workflow/README.md) |")
        )
        cells = original_row.split("|")
        cells[3] = " 999 "
        catalog.write_text(catalog.read_text().replace(original_row, "|".join(cells)))
        other_rows = [
            row for row in catalog.read_text().splitlines()
            if row.startswith("| [") and row != "|".join(cells)
        ]
        previous_entries = category.read_text()
        category.write_text(category.read_text() + "\nMaintainer notes to preserve.\n")
        prepare_skill(self.root, "workflow", "repo-survey")
        prepare_skill(self.root, "workflow", "repo-plan")
        content = category.read_text()
        self.assertIn("Maintainer notes to preserve.", content)
        for name in ("repo-survey", "repo-plan"):
            self.assertIn(f"[{name}]({name}/SKILL.md)", content)
        root_row = next(
            row for row in catalog.read_text().splitlines()
            if row.startswith("| [workflow](skills/workflow/README.md) |")
        )
        self.assertEqual(int(root_row.split("|")[3].strip()), 2)
        self.assertEqual(root_row.split("|")[1:3], original_row.split("|")[1:3])
        for row in other_rows:
            self.assertIn(row, catalog.read_text())
        for row in previous_entries.splitlines():
            if row.startswith(("- [", "## ")):
                self.assertIn(row, content)

    def test_invalid_names_and_unknown_categories_do_not_mutate_files(self):
        before = self.snapshot()
        for category, name in (
            ("workflow", "../outside"),
            ("workflow", "Bad--Name"),
            ("workflow", "x" * 65),
            ("../outside", "my-skill"),
            ("unknown", "my-skill"),
        ):
            with self.subTest(category=category, name=name):
                with self.assertRaises(ValueError):
                    prepare_skill(self.root, category, name)
                self.assertEqual(self.snapshot(), before)

    def test_duplicate_names_in_other_categories_do_not_overwrite_files(self):
        prepare_skill(self.root, "workflow", "my-skill")
        before = self.snapshot()
        for category in ("workflow", "git"):
            with self.subTest(category=category):
                with self.assertRaisesRegex(ValueError, "already exists"):
                    prepare_skill(self.root, category, "my-skill")
                self.assertEqual(self.snapshot(), before)

    def test_existing_evaluation_is_preserved(self):
        evaluation = self.root / "evals" / "my-skill"
        evaluation.mkdir()
        (evaluation / "README.md").write_text("User evaluation notes.\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Evaluation path already exists"):
            prepare_skill(self.root, "workflow", "my-skill")
        self.assertEqual(self.snapshot(), before)

    def test_missing_catalog_markers_fail_before_creation(self):
        category = self.root / "skills" / "workflow" / "README.md"
        category.write_text("Custom category documentation.\n")
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "catalog block"):
            prepare_skill(self.root, "workflow", "my-skill")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((category.parent / "my-skill").exists())

    def test_invalid_descriptions_fail_before_creation(self):
        before = self.snapshot()
        for description in (" ", "x" * 301, "x" * 1025):
            with self.subTest(description_length=len(description)):
                with self.assertRaisesRegex(ValueError, "Description"):
                    prepare_skill(self.root, "workflow", "my-skill", description)
                self.assertEqual(self.snapshot(), before)

    def test_invalid_generated_skill_is_removed(self):
        template = self.root / "templates" / "skill.md.tmpl"
        template.write_text(template.read_text().replace("name: my-skill", "name: invalid-name"))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, "Generated skill is invalid"):
            prepare_skill(self.root, "workflow", "my-skill")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "skills" / "workflow" / "my-skill").exists())
        self.assertFalse((self.root / "evals" / "my-skill").exists())

    def test_catalog_write_failure_restores_prior_state(self):
        before = self.snapshot()
        category = self.root / "skills" / "workflow" / "README.md"
        original_write = Path.write_text
        failed = False

        def fail_once(path, text, *args, **kwargs):
            nonlocal failed
            if path == category and not failed:
                failed = True
                raise OSError("Injected write failure")
            return original_write(path, text, *args, **kwargs)

        with patch.object(Path, "write_text", fail_once):
            with self.assertRaisesRegex(OSError, "Injected write failure"):
                prepare_skill(self.root, "workflow", "my-skill")
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.root / "skills" / "workflow" / "my-skill").exists())
        self.assertFalse((self.root / "evals" / "my-skill").exists())

    def test_cli_creates_skill_from_another_working_directory(self):
        shutil.copyfile(ROOT / "new_skill.py", self.root / "new_skill.py")
        scripts = self.root / "scripts"
        scripts.mkdir()
        for name in ("validate_skills.py", "generate_index.py", "skill_routes.py"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)
        result = subprocess.run(
            [sys.executable, str(self.root / "new_skill.py"), "git", "git-review"],
            cwd=self.root.parent,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(validate_repository(self.root), (1, []))


if __name__ == "__main__":
    unittest.main()
