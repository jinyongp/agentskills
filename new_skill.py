"""Prepare a skill, its evaluation notes, and catalog entries."""

import argparse
import html
import json
from pathlib import Path
import re
import shutil

from scripts.validate_skills import MAX_DESCRIPTION_CHARS, SLUG, validate_repository


ROOT = Path(__file__).resolve().parent
START = "<!-- skills:start -->"
END = "<!-- skills:end -->"


def prepare_skill(
    root: Path, category: str, name: str, description: str | None = None
) -> Path:
    root = root.resolve()
    for label, value in (("category", category), ("skill name", name)):
        if not SLUG.fullmatch(value) or len(value) > 64:
            raise ValueError(
                f"Invalid {label}: use 1-64 lowercase letters, digits, and single hyphens."
            )
    if description is not None and (not description.strip() or len(description) > MAX_DESCRIPTION_CHARS):
        raise ValueError(f"Description must contain 1-{MAX_DESCRIPTION_CHARS} characters.")

    category_dir = root / "skills" / category
    if not category_dir.is_dir():
        raise ValueError(f"Unknown category '{category}'; choose an existing skills/ category.")
    if category_dir.resolve().parent != root / "skills":
        raise ValueError("Category must be a directory inside skills/.")
    skill = category_dir / name
    evaluation = root / "evals" / name
    if skill.exists() or any(
        path.parent.name == name for path in (root / "skills").rglob("SKILL.md")
    ):
        raise ValueError(f"Skill '{name}' already exists; names must be unique across categories.")
    if evaluation.exists():
        raise ValueError(f"Evaluation path already exists: evals/{name}")
    if (root / "evals").resolve() != root / "evals":
        raise ValueError("evals/ must be a directory inside the repository.")
    _, errors = validate_repository(root)
    if errors:
        raise ValueError("Fix existing catalog errors before adding a skill:\n" + "\n".join(errors))

    content = (root / "templates" / "skill.md.tmpl").read_text(encoding="utf-8")
    content = content.replace("name: my-skill\n", f"name: {name}\n", 1)
    content = content.replace("category: workflow\n", f"category: {category}\n", 1)
    content = content.replace("# My Skill\n", f"# {name.replace('-', ' ').title()}\n", 1)
    if description is not None:
        content, replacements = re.subn(
            r"^description: >-\n(?:[ \t]+[^\n]*\n)+",
            lambda _: f"description: {json.dumps(description, ensure_ascii=False)}\n",
            content,
            count=1,
            flags=re.MULTILINE,
        )
        if replacements != 1:
            raise ValueError("Skill template is missing its description field.")
    evaluation_content = (
        (root / "templates" / "eval.md.tmpl")
        .read_text(encoding="utf-8")
        .replace("my-skill", name)
    )

    catalog = root / "README.md"
    category_catalog = category_dir / "README.md"
    original_catalog = catalog.read_text(encoding="utf-8")
    original_category = category_catalog.read_text(encoding="utf-8")
    rows = original_catalog.splitlines(keepends=True)
    matching = [
        i for i, row in enumerate(rows)
        if row.startswith(f"| [{category}](skills/{category}/README.md) |")
    ]
    if len(matching) != 1:
        raise ValueError(f"README.md must contain one catalog row for '{category}'.")
    index = matching[0]
    cells = rows[index].strip().split("|")
    if len(cells) != 5:
        raise ValueError(f"Unexpected catalog row format for '{category}'.")
    entry = f"[{name}](skills/{category}/{name}/SKILL.md)"
    previous = cells[3].strip()
    cells[3] = f" {entry if previous == 'None yet' else previous + ', ' + entry} "
    rows[index] = "|".join(cells) + "\n"

    if original_category.count(START) != 1 or original_category.count(END) != 1:
        raise ValueError(f"skills/{category}/README.md needs one skills catalog block.")
    before, block = original_category.split(START)
    table, after = block.split(END)
    if "| Skill | Description | Install |" not in table:
        raise ValueError(f"skills/{category}/README.md is missing its catalog table.")
    table = table.replace("| None yet | | |\n", "")
    summary = (
        html.escape(" ".join(description.split())).replace("|", "\\|")
        if description else "In progress"
    )
    install = f"npx skills add jinyongp/agentskills --skill {name}"
    table = table.rstrip() + f"\n| [{name}]({name}/SKILL.md) | {summary} | `{install}` |\n"
    updated_category = before + START + table + END + after

    skill.mkdir()
    created_evaluation = False
    modified_catalogs: list[Path] = []
    originals = {catalog: original_catalog, category_catalog: original_category}
    try:
        evaluation.mkdir()
        created_evaluation = True
        (skill / "SKILL.md").write_text(content, encoding="utf-8")
        (evaluation / "README.md").write_text(evaluation_content, encoding="utf-8")
        _, errors = validate_repository(root)
        if errors:
            raise ValueError("Generated skill is invalid:\n" + "\n".join(errors))
        for path, updated in ((catalog, "".join(rows)), (category_catalog, updated_category)):
            modified_catalogs.append(path)
            path.write_text(updated, encoding="utf-8")
    except (OSError, ValueError) as exc:
        shutil.rmtree(skill)
        if created_evaluation:
            shutil.rmtree(evaluation)
        restore_errors = []
        for path in modified_catalogs:
            try:
                path.write_text(originals[path], encoding="utf-8")
            except OSError as restore_error:
                restore_errors.append(f"{path}: {restore_error}")
        if restore_errors:
            raise OSError(
                f"{exc}; catalog restoration failed: {'; '.join(restore_errors)}"
            ) from exc
        raise
    return skill


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("category", help="Existing category, e.g. workflow or frontend")
    parser.add_argument("name", help="Unique lowercase, hyphen-separated skill name")
    parser.add_argument("--description", help="What the skill does and when to use it")
    args = parser.parse_args()
    try:
        skill = prepare_skill(ROOT, args.category, args.name, args.description)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")
    print(f"Created {skill.relative_to(ROOT)}/SKILL.md")
    print(f"Created evals/{args.name}/README.md and updated both catalogs.")
    print("Write the instructions and evaluation cases, then run: uv run check.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
