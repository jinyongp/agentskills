"""Validate the Agent Skills format and this repository's catalog layout."""

import argparse
import os
from pathlib import Path
import re

from skills_ref import read_properties, validate


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}
MAX_DESCRIPTION_CHARS = 300
MAX_BODY_CHARS = 4000


def validate_repository(root: Path) -> tuple[int, list[str]]:
    root = root.resolve()
    errors: list[str] = []
    count = 0
    seen: dict[str, Path] = {}
    skills = root / "skills"
    if not skills.is_dir():
        return 0, ["Missing skills/ directory"]

    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        for filename in sorted(files):
            if filename.lower() != "skill.md":
                continue
            path = Path(directory) / filename
            relative = path.relative_to(root)
            if filename != "SKILL.md":
                errors.append(f"{relative}: use the exact filename SKILL.md")
                continue
            if len(relative.parts) != 4 or relative.parts[0] != "skills":
                errors.append(f"{relative}: expected skills/<category>/<name>/SKILL.md")
                continue

            count += 1
            category, name = relative.parts[1:3]
            for label, value in (("category", category), ("skill name", name)):
                if not SLUG.fullmatch(value) or len(value) > 64:
                    errors.append(f"{relative}: invalid {label} '{value}'")

            try:
                problems = validate(path.parent)
                errors.extend(f"{relative}: {problem}" for problem in problems)
                if problems:
                    continue
                properties = read_properties(path.parent)
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{relative}: cannot read skill: {exc}")
                continue

            if properties.name in seen:
                errors.append(
                    f"{relative}: duplicate name '{properties.name}' "
                    f"(also in {seen[properties.name]})"
                )
            else:
                seen[properties.name] = relative

            metadata = properties.metadata
            if not isinstance(metadata, dict) or metadata.get("category") != category:
                errors.append(f"{relative}: metadata.category must equal '{category}'")

            if len(properties.description) > MAX_DESCRIPTION_CHARS:
                errors.append(f"{relative}: description exceeds {MAX_DESCRIPTION_CHARS} characters")
            body = re.split(r"(?m)^---[ \t]*$", content, maxsplit=2)[-1].strip()
            if len(body) > MAX_BODY_CHARS:
                errors.append(f"{relative}: body exceeds {MAX_BODY_CHARS} characters; move conditional detail to references")

    for category in sorted(skills.iterdir()):
        if not category.is_dir():
            continue
        if not SLUG.fullmatch(category.name) or len(category.name) > 64:
            errors.append(f"skills/{category.name}: invalid category name")
        for skill in sorted(category.iterdir()):
            if skill.is_dir() and not (skill / "SKILL.md").is_file():
                errors.append(f"{skill.relative_to(root)}: missing SKILL.md")

    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    count, errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed: {len(errors)} error(s), {count} skill(s) checked.")
        return 1
    print(f"Validation passed: {count} skill(s) checked.")
    if count == 0:
        print("No installable skills yet; the empty scaffold is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
