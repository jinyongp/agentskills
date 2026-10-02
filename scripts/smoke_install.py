"""Check categorized discovery and selective installation in a temporary project."""

import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CLI_PACKAGE = "skills@1.7.0"


def run_cli(project: Path, source: Path, *options: str) -> str:
    result = subprocess.run(
        ["npx", "--yes", CLI_PACKAGE, "add", str(source), *options],
        cwd=project,
        env={**os.environ, "DISABLE_TELEMETRY": "1", "CI": "1"},
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="agentskills-smoke-") as directory:
        temp = Path(directory)
        source, project = temp / "source", temp / "project"
        project.mkdir()
        template = (ROOT / "templates" / "skill.md.tmpl").read_text()
        selected = "scaffold-smoke-a"
        other = "scaffold-smoke-b"
        bundles = {
            "references/guide.md": "# Smoke reference\n",
            "scripts/example.py": 'print("smoke fixture")\n',
            "assets/example.txt": "Smoke asset\n",
        }
        for category, name in (("workflow", selected), ("git", other)):
            skill = source / "skills" / category / name
            skill.mkdir(parents=True)
            content = template.replace("name: my-skill", f"name: {name}")
            content = content.replace("category: workflow", f"category: {category}")
            (skill / "SKILL.md").write_text(content)
            for relative, value in bundles.items():
                path = skill / relative
                path.parent.mkdir(exist_ok=True)
                path.write_text(value)

        listing = run_cli(project, source, "--list")
        if selected not in listing or other not in listing:
            raise RuntimeError(f"CLI did not discover both categorized skills:\n{listing}")
        print(f"{CLI_PACKAGE}: categorized discovery passed.")

        run_cli(
            project, source, "--skill", selected, "--agent", "codex", "--copy", "--yes"
        )
        installed = project / ".agents" / "skills" / selected
        expected = source / "skills" / "workflow" / selected
        for relative in ("SKILL.md", *bundles):
            path = installed / relative
            if not path.is_file() or path.read_bytes() != (expected / relative).read_bytes():
                raise RuntimeError(f"Installed file missing or changed: {relative}")
        if (installed.parent / other).exists():
            raise RuntimeError("Unselected skill was installed.")
        print(f"{CLI_PACKAGE}: selective install and bundled files passed.")


if __name__ == "__main__":
    main()
