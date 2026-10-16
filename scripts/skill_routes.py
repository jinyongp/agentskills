"""Render authored task decisions without loading skill bodies."""

import json
from pathlib import Path
import re


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def read_routes(root: Path) -> list[dict]:
    routes = json.loads((root / "lib/skill-routes.json").read_text(encoding="utf-8"))
    if not isinstance(routes, list):
        raise ValueError("Skill routes must be a list")
    seen = set()

    def text(value, limit):
        return isinstance(value, str) and 0 < len(value) <= limit and not any(c in value for c in "\r\n")

    for route in routes:
        if not isinstance(route, dict):
            raise ValueError("Invalid skill route")
        name = route.get("id")
        if not text(name, 64) or not SLUG.fullmatch(name) or name in seen:
            raise ValueError("Invalid or duplicate skill route id")
        seen.add(name)
        if not text(route.get("title"), 120) or not text(route.get("when"), 300):
            raise ValueError(f"Invalid route description: {name}")
        choices = route.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError(f"Missing route choices: {name}")
        skills = set()
        for choice in choices:
            if not isinstance(choice, dict):
                raise ValueError(f"Invalid route choice: {name}")
            skill = choice.get("skill")
            if not text(skill, 64) or not SLUG.fullmatch(skill) or skill in skills:
                raise ValueError(f"Invalid or duplicate route skill: {name}")
            if not text(choice.get("when"), 300):
                raise ValueError(f"Invalid route condition: {name}/{skill}")
            skills.add(skill)
    return routes


def render_routes(root: Path, paths: dict[str, str], generated: str, limit: int):
    files, links, covered = {}, [], set()
    for route in read_routes(root):
        rows = []
        for choice in route["choices"]:
            name = choice["skill"]
            if name in paths:
                rows.append(f"- {choice['when']}\n  Skill: `{name}`\n  Source: `{paths[name]}`")
                covered.add(name)
        if not rows:
            continue
        name = route["id"]

        def page_text(chunk, offset, number, count):
            next_page = (f"Next page: `references/routes/{name}.page-{number + 1}.md` "
                         "(relative to this skill).") if number < count else "End of this decision route."
            return "\n".join([generated, f"# {route['title']}", "", route["when"], "",
                              "Choose by the requested outcome and permission; these are alternatives, not a sequence.",
                              f"Page {number} of {count}. Choices {offset + 1}-{offset + len(chunk)} of {len(rows)}; "
                              f"{len(rows) - len(chunk)} on other pages.", "", *chunk, "", next_page, ""])

        groups, current, offset = [], [], 0
        for row in rows:
            candidate = [*current, row]
            if len(page_text(candidate, offset, 999998, 999999)) > limit:
                if not current:
                    raise ValueError(f"Decision route entry exceeds page limit: {name}")
                groups.append(current)
                offset += len(current)
                current = [row]
                if len(page_text(current, offset, 999998, 999999)) > limit:
                    raise ValueError(f"Decision route entry exceeds page limit: {name}")
            else:
                current = candidate
        groups.append(current)
        offset = 0
        for number, chunk in enumerate(groups, 1):
            filename = f"references/routes/{name}{'.page-' + str(number) if number > 1 else ''}.md"
            content = page_text(chunk, offset, number, len(groups))
            if len(content) > limit:
                raise ValueError(f"Decision route page exceeds limit: {name}")
            files[filename] = content
            offset += len(chunk)
        links.append(f"- [{route['title']}](references/routes/{name}.md) — {route['when']}")
    return files, links, set(paths) - covered
