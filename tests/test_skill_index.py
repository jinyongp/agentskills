"""Exercise complete, bounded catalogs and automatic scaffold synchronization."""

from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from new_skill import prepare_skill
from scripts.generate_index import END, GENERATED, INDEX, MAX_PAGE_CHARS, START, index_errors, snapshot_index, update_index
from scripts.validate_skills import validate_repository


ROOT = Path(__file__).resolve().parents[1]


class SkillIndexTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")
        shutil.copytree(ROOT / "lib", self.root / "lib")
        (self.root / "evals").mkdir()
        (self.root / "README.md").write_text(
            "# Skills\n\n| [workflow](skills/workflow/README.md) | Plan, review, and verify changes | 0 |\n"
            "| [tooling](skills/tooling/README.md) | Select local skills | 1 |\n"
        )
        self.rows = {"tooling": [("Selection", "index", "Select applicable installed skills.")], "workflow": []}
        manifest = self.root / INDEX / "SKILL.md"
        manifest.parent.mkdir(parents=True)
        body = (ROOT / INDEX / "SKILL.md").read_text()
        before, rest = body.split(START)
        _, after = rest.split(END)
        manifest.write_text(before + START + "\n\n" + END + after)
        self.write_catalogs()
        update_index(self.root)

    def add(self, name, summary, section="Review", category="workflow"):
        self.rows.setdefault(category, []).append((section, name, summary))
        manifest = self.root / "skills" / category / name / "SKILL.md"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            f"---\nname: {name}\ndescription: Test skill.\nlicense: MIT\n"
            f"metadata:\n  category: {category}\n---\n\n# Test\n"
        )

    def write_catalogs(self):
        for category, rows in self.rows.items():
            directory = self.root / "skills" / category
            directory.mkdir(parents=True, exist_ok=True)
            lines, previous = [], None
            for section, name, summary in rows:
                if section != previous:
                    lines.append(f"\n## {section}\n")
                    previous = section
                lines.append(f"- [{name}]({name}/SKILL.md) — {summary}")
            if not rows:
                lines.append("No skills yet.")
            (directory / "README.md").write_text(
                f"# {category.title()}\n\n<!-- skills:start -->\n" + "\n".join(lines) + "\n<!-- skills:end -->\n"
            )

    def snapshot(self):
        return {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}

    def test_catalog_preserves_distinct_intents_without_loading_bodies(self):
        intentions = {"code-review": "Find defects; report only.", "review-loop": "Review and fix the requested scope.", "verify": "Run checks and report evidence."}
        for name, summary in intentions.items():
            self.add(name, summary)
            # Generation needs names and catalog intent, not valid/readable bodies.
            (self.root / "skills/workflow" / name / "SKILL.md").write_bytes(b"private body\xff" * 100_000)
        self.write_catalogs()
        update_index(self.root)
        text = (self.root / INDEX / "references/catalog/workflow.md").read_text()
        for name, summary in intentions.items():
            self.assertIn(f"`{name}` — {summary}", text)
        self.assertNotIn("private body", text)
        self.assertEqual(index_errors(self.root), [])
        before = self.snapshot()
        self.assertEqual(update_index(self.root), 0)
        self.assertEqual(self.snapshot(), before)

    def test_large_catalog_pages_recover_every_entry_with_exact_next_paths(self):
        expected = [f"skill-{n:03d}" for n in range(180)]
        for name in expected:
            self.add(name, "Understand " + "가" * 220 + "; preserve the selected scope.")
        self.write_catalogs()
        update_index(self.root)
        page, seen, page_count = "workflow.md", [], 0
        while page:
            text = (self.root / INDEX / "references/catalog" / page).read_text()
            self.assertLessEqual(len(text), MAX_PAGE_CHARS)
            self.assertIn("of 180;", text)
            seen.extend(re.findall(r"^- `([^`]+)` —", text, re.MULTILINE))
            match = re.search(r"Next page: `([^`]+)`", text)
            if match:
                target = self.root / INDEX / match[1]
                self.assertTrue(target.is_file())
                page = target.name
            else:
                page = None
            page_count += 1
        self.assertGreater(page_count, 1)
        self.assertEqual(seen, expected)
        self.assertEqual(index_errors(self.root), [])

    def test_changed_summaries_are_rejected_by_validation_until_refreshed(self):
        self.add("verify", "Run checks.")
        self.write_catalogs()
        update_index(self.root)
        self.assertEqual(validate_repository(self.root)[1], [])
        self.rows["workflow"] = [("Review", "verify", "Run checks; report skipped coverage.")]
        self.write_catalogs()
        before = self.snapshot()
        self.assertTrue(any("stale" in error for error in validate_repository(self.root)[1]))
        self.assertEqual(self.snapshot(), before)
        update_index(self.root)
        self.assertEqual(validate_repository(self.root)[1], [])

    def test_read_only_freshness_survives_autocrlf_checkout(self):
        self.add("verify", "Run checks.")
        self.write_catalogs()
        update_index(self.root)
        attributes = ROOT / ".gitattributes"
        if attributes.exists():
            shutil.copyfile(attributes, self.root / attributes.name)
        (self.root / "control.txt").write_bytes(b"one\ntwo\n")
        env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}

        def git(*args):
            result = subprocess.run(["git", *args], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

        git("-C", str(self.root), "init", "-q")
        git("-C", str(self.root), "add", "--", ".")
        git("-C", str(self.root), "-c", "user.name=Index Fixture", "-c",
            "user.email=index@example.invalid", "commit", "-qm", "test(index): seed checkout fixture")
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            git("clone", "--quiet", "--config", "core.autocrlf=true", str(self.root), str(checkout))
            self.assertEqual((checkout / "control.txt").read_bytes(), b"one\r\ntwo\r\n")
            before = {p: p.read_bytes() for p in (checkout / INDEX).rglob("*") if p.is_file()}
            self.assertEqual(index_errors(checkout), [])
            self.assertEqual({p: p.read_bytes() for p in before}, before)
            page = checkout / INDEX / "references/catalog/workflow.md"
            page.write_bytes(page.read_bytes().replace(b"Run checks.", b"Changed intent."))
            changed = page.read_bytes()
            self.assertTrue(any("stale" in error for error in index_errors(checkout)))
            self.assertEqual(page.read_bytes(), changed)

    def test_missing_duplicate_and_removed_catalog_entries_do_not_change_index(self):
        self.add("verify", "Run checks.")
        self.write_catalogs()
        update_index(self.root)
        original = snapshot_index(self.root)
        catalog = self.root / "skills/workflow/README.md"
        content = catalog.read_text()
        entry = "- [verify](verify/SKILL.md) — Run checks."
        for replacement in (content.replace(entry, ""), content.replace(entry, entry + "\n" + entry), content.replace("verify](verify/", "missing](missing/")):
            catalog.write_text(replacement)
            with self.assertRaises(ValueError):
                update_index(self.root)
            self.assertEqual(snapshot_index(self.root), original)
        catalog.write_text(content)

    def test_refresh_removes_obsolete_pages_after_category_shrinks(self):
        for n in range(50):
            self.add(f"skill-{n}", "Long intent " + "x" * 220)
        self.write_catalogs()
        update_index(self.root)
        directory = self.root / INDEX / "references/catalog"
        self.assertTrue((directory / "workflow-2.md").exists())
        for _, name, _ in self.rows["workflow"][1:]:
            shutil.rmtree(self.root / "skills/workflow" / name)
        self.rows["workflow"] = self.rows["workflow"][:1]
        self.write_catalogs()
        update_index(self.root)
        self.assertEqual(list(directory.glob("workflow-*.md")), [])
        self.assertEqual(index_errors(self.root), [])

    def test_prepare_skill_updates_index_and_restores_failed_work(self):
        prepare_skill(self.root, "workflow", "new-check", "Check the selected behavior.")
        text = (self.root / INDEX / "references/catalog/workflow.md").read_text()
        self.assertIn("`new-check` — Check the selected behavior.", text)
        self.assertEqual(index_errors(self.root), [])
        before = self.snapshot()
        original = Path.write_bytes
        failed = False

        def fail_once(path, content):
            nonlocal failed
            if path == self.root / INDEX / "references/catalog/workflow.md" and not failed:
                failed = True
                raise OSError("injected index write failure")
            return original(path, content)

        with patch.object(Path, "write_bytes", fail_once):
            with self.assertRaises(OSError):
                prepare_skill(self.root, "workflow", "failed-check", "Another check.")
        self.assertTrue(failed)
        self.assertEqual(self.snapshot(), before)

    def test_unmanaged_files_and_output_symlinks_are_preserved(self):
        directory = self.root / INDEX / "references/catalog"
        manual = directory / "manual.md"
        manual.write_text("Keep my notes.\n")
        before = self.snapshot()
        with self.assertRaises(ValueError):
            update_index(self.root)
        self.assertEqual(self.snapshot(), before)
        manual.unlink()
        target = self.root / "outside.md"
        target.write_text("Keep outside content.\n")
        manual.symlink_to(target)
        with self.assertRaises(ValueError):
            update_index(self.root)
        self.assertEqual(target.read_text(), "Keep outside content.\n")

    def test_oversized_heading_fails_before_writing_any_output(self):
        self.add("verify", "Run checks.", section="x" * 3000)
        self.write_catalogs()
        before = snapshot_index(self.root)
        with self.assertRaises(ValueError):
            update_index(self.root)
        self.assertEqual(snapshot_index(self.root), before)

    def test_cli_large_failure_and_check_mode_are_bounded_and_read_only(self):
        script = self.root / "scripts/generate_index.py"
        script.parent.mkdir()
        shutil.copyfile(ROOT / "scripts/generate_index.py", script)
        shutil.copyfile(ROOT / "scripts/skill_routes.py", script.with_name("skill_routes.py"))
        catalog = self.root / "skills/workflow/README.md"
        catalog.write_text(catalog.read_text().replace("No skills yet.", "unsupported " + "x" * 10_000))
        before = self.snapshot()
        for args in ([], ["--check"]):
            result = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertLessEqual(len(result.stdout), 4000)
            self.assertEqual(result.stderr, "")
            self.assertEqual(self.snapshot(), before)

    def test_task_routes_cover_distributed_skills_and_filter_partial_sources(self):
        from scripts.skill_routes import read_routes
        authored = {choice["skill"] for route in read_routes(ROOT) for choice in route["choices"]}
        distributed = {p.parent.name for p in (ROOT / "skills").glob("*/*/SKILL.md")} - {"index"}
        self.assertEqual(authored, distributed)
        expected = {"spec-generator", "plan", "code-review", "review-loop"}
        for name in expected:
            self.add(name, "Selected task.")
        self.add("new-task", "An additional task available through the catalog.")
        self.write_catalogs()
        update_index(self.root)
        route_pages = list((self.root / INDEX / "references/routes").glob("*.md"))
        combined = "\n".join(p.read_text() for p in route_pages)
        self.assertEqual(set(re.findall(r"Skill: `([^`]+)`", combined)), expected)
        for target in re.findall(r"Source: `([^`]+)`", combined):
            self.assertTrue((self.root / INDEX / target).is_file())
        self.assertIn("1 skill(s) have no authored decision route", (self.root / INDEX / "SKILL.md").read_text())
        self.assertIn("`new-task`", (self.root / INDEX / "references/catalog/workflow.md").read_text())
        self.assertEqual(index_errors(self.root), [])

    def test_route_pagination_preserves_all_decisions_and_rejects_invalid_data_read_only(self):
        expected = [f"skill-{n:03d}" for n in range(100)]
        for name in expected:
            self.add(name, "Task summary.")
        self.write_catalogs()
        route = {"id": "decide", "title": "Choose work", "when": "Choose a matching task.",
                 "choices": [{"skill": name, "when": "Investigate " + "x" * 220} for name in expected]}
        source = self.root / "lib/skill-routes.json"
        source.write_text(json.dumps([route]))
        update_index(self.root)
        next_page, found = "references/routes/decide.md", []
        while next_page:
            text = (self.root / INDEX / next_page).read_text()
            self.assertLessEqual(len(text), MAX_PAGE_CHARS)
            self.assertIn("of 100;", text)
            found.extend(re.findall(r"Skill: `([^`]+)`", text))
            match = re.search(r"Next page: `([^`]+)`", text)
            next_page = match[1] if match else None
        self.assertEqual(found, expected)
        original = snapshot_index(self.root)
        for broken in (None, [route, route], [{**route, "id": "../outside"}],
                       [{**route, "choices": [{"skill": "skill-000", "when": "bad\ncondition"}]}],
                       [{**route, "id": f"route-{n}", "when": "x" * 300} for n in range(20)]):
            source.write_text(json.dumps(broken))
            with self.assertRaises(ValueError):
                update_index(self.root)
            self.assertEqual(snapshot_index(self.root), original)

    def test_route_files_are_owned_rolled_back_and_removed_when_empty(self):
        self.add("spec-generator", "Define behavior.")
        self.write_catalogs()
        update_index(self.root)
        route_file = self.root / INDEX / "references/routes/define.md"
        original = snapshot_index(self.root)
        self.add("plan", "Plan implementation.")
        self.write_catalogs()
        write_bytes = Path.write_bytes
        failed = False

        def fail_once(path, content):
            nonlocal failed
            if path == route_file and not failed:
                failed = True
                raise OSError("injected decision route write failure")
            return write_bytes(path, content)

        with patch.object(Path, "write_bytes", fail_once):
            with self.assertRaises(OSError):
                update_index(self.root)
        self.assertTrue(failed)
        self.assertEqual(snapshot_index(self.root), original)
        update_index(self.root)
        manual = route_file.with_name("manual.md")
        manual.write_text("Preserve local notes.")
        with self.assertRaises(ValueError):
            update_index(self.root)
        self.assertEqual(manual.read_text(), "Preserve local notes.")
        manual.unlink()
        for name in ("spec-generator", "plan"):
            shutil.rmtree(self.root / "skills/workflow" / name)
        self.rows["workflow"] = []
        self.write_catalogs()
        update_index(self.root)
        self.assertFalse(route_file.exists())
        self.assertEqual(index_errors(self.root), [])


if __name__ == "__main__":
    unittest.main()
