"""Cover catalog failures that would prevent reliable CLI discovery."""

from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import MAX_BODY_CHARS, MAX_DESCRIPTION_CHARS, validate_repository


TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "skill.md.tmpl"


class ValidateSkillsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "skills").mkdir()

    def add_skill(self, category="workflow", name="my-skill") -> Path:
        path = self.root / "skills" / category / name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        content = TEMPLATE.read_text().replace("name: my-skill", f"name: {name}")
        content = content.replace("category: workflow", f"category: {category}")
        path.write_text(content)
        return path

    def test_empty_scaffold_is_valid(self):
        self.assertEqual(validate_repository(self.root), (0, []))

    def test_description_budget_accepts_boundary_and_rejects_excess(self):
        path = self.add_skill()
        content = path.read_text()
        start, rest = content.split("description:", 1)
        _, tail = rest.split("license:", 1)
        for length in (MAX_DESCRIPTION_CHARS, MAX_DESCRIPTION_CHARS + 1):
            path.write_text(start + "description: " + "x" * length + "\nlicense:" + tail)
            errors = validate_repository(self.root)[1]
            self.assertEqual(any("description exceeds" in e for e in errors), length > MAX_DESCRIPTION_CHARS)

    def test_body_budget_keeps_conditional_references_separate(self):
        path = self.add_skill()
        header = path.read_text().split("\n---\n", 1)[0] + "\n---\n"
        references = path.parent / "references"
        references.mkdir()
        (references / "detail.md").write_text("d" * (MAX_BODY_CHARS * 2))
        for length in (MAX_BODY_CHARS, MAX_BODY_CHARS + 1):
            path.write_text(header + "b" * length + "\n")
            errors = validate_repository(self.root)[1]
            self.assertEqual(any("body exceeds" in e for e in errors), length > MAX_BODY_CHARS)

    def test_missing_catalog_is_rejected(self):
        (self.root / "skills").rmdir()
        self.assertIn("Missing skills/ directory", validate_repository(self.root)[1])

    def test_template_and_bundled_resources_are_valid(self):
        path = self.add_skill()
        (path.parent / "references").mkdir()
        (path.parent / "references" / "guide.md").write_text("# Guide\n")
        self.assertEqual(validate_repository(self.root), (1, []))

    def test_duplicate_names_across_categories_are_rejected(self):
        self.add_skill()
        self.add_skill(category="git")
        count, errors = validate_repository(self.root)
        self.assertEqual(count, 2)
        self.assertTrue(any("duplicate name" in error for error in errors))

    def test_invalid_name_and_directory_mismatch_are_rejected(self):
        path = self.add_skill()
        path.write_text(path.read_text().replace("name: my-skill", "name: Bad--Name"))
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("must be lowercase" in error for error in errors))
        self.assertTrue(any("must match skill name" in error for error in errors))

    def test_malformed_frontmatter_is_rejected(self):
        path = self.add_skill()
        path.write_text("---\nname: [broken\n---\n")
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("Invalid YAML" in error for error in errors))

    def test_wrong_metadata_category_is_rejected(self):
        path = self.add_skill()
        path.write_text(path.read_text().replace("category: workflow", "category: git"))
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("metadata.category" in error for error in errors))

    def test_scalar_metadata_is_rejected_without_crashing(self):
        path = self.add_skill()
        path.write_text(
            "---\nname: my-skill\ndescription: Test skill.\nmetadata: workflow\n---\n"
        )
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("metadata.category" in error for error in errors))

    def test_misplaced_skills_are_rejected(self):
        for relative in (
            "SKILL.md",
            "skills/workflow/SKILL.md",
            "skills/workflow/nested/my-skill/SKILL.md",
        ):
            with self.subTest(relative=relative):
                path = self.root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(TEMPLATE.read_text())
                errors = validate_repository(self.root)[1]
                self.assertTrue(any("expected skills/" in error for error in errors))
                path.unlink()

    def test_unfinished_skill_directory_is_rejected(self):
        (self.root / "skills" / "workflow" / "unfinished").mkdir(parents=True)
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("missing SKILL.md" in error for error in errors))

    def test_lowercase_filename_is_rejected(self):
        path = self.add_skill()
        path.rename(path.with_name("skill.md"))
        errors = validate_repository(self.root)[1]
        self.assertTrue(any("exact filename" in error for error in errors))

    def test_templates_and_local_dependencies_are_not_discovered(self):
        template = self.root / "templates" / "skill.md.tmpl"
        template.parent.mkdir()
        template.write_text(TEMPLATE.read_text())
        dependency = self.root / ".venv" / "example" / "SKILL.md"
        dependency.parent.mkdir(parents=True)
        dependency.write_text(TEMPLATE.read_text())
        self.assertEqual(validate_repository(self.root), (0, []))


if __name__ == "__main__":
    unittest.main()
