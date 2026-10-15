"""Exercise the npm-packed CLI and native shell shims in isolated homes/projects."""

import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

from npm_cli import npm_command


ROOT = Path(__file__).resolve().parents[1]
CONTENT_FIXTURES = (
    ("workflow", "survey"), ("tooling", "index"), ("tooling", "skill-review"),
    ("workflow", "spec-generator"), ("workflow", "trace"),
    ("workflow", "review-map"), ("workflow", "dependency-review"),
    ("workflow", "qa-checklist"), ("workflow", "preflight"),
    ("workflow", "code-review"), ("workflow", "test"),
    ("workflow", "queue"), ("git", "git-commit"), ("git", "git-worktree"),
)


def run(argv, cwd, env):
    result = subprocess.run(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True,
                            text=True, encoding="utf-8", timeout=120)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {argv!r}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main():
    with tempfile.TemporaryDirectory(prefix="agentskills-package-") as directory:
        temp = Path(directory)
        home, project, prefix = (temp / name for name in ("home", "project 한글's space", "tools"))
        for path in (home, project, prefix):
            path.mkdir()
        env = {**os.environ, "HOME": str(home), "USERPROFILE": str(home),
               "npm_config_cache": str(temp / "npm-cache"), "DISABLE_TELEMETRY": "1"}
        resolved = run([shutil.which("node"), "-p", "require('node:os').homedir()"], project, env)
        if Path(resolved.strip()).resolve() != home.resolve():
            raise RuntimeError("Node home was not isolated; refusing to install globally.")
        packed = json.loads(run([*npm_command(), "pack", "--json", "--ignore-scripts",
                                 "--pack-destination", str(temp)], ROOT, env))[0]
        archive = temp / packed["filename"]
        run([*npm_command(), "install", "--prefix", str(prefix), "--ignore-scripts",
             "--no-audit", "--no-fund", str(archive)], project, env)
        package = prefix / "node_modules/@jinyongp/agentskills"
        shim = prefix / "node_modules/.bin" / ("agentskills.cmd" if os.name == "nt" else "agentskills")

        def shell_invoke(shell, *args):
            if shell == "powershell":
                quote = lambda word: "'" + str(word).replace("'", "''") + "'"
                script = temp / "invoke.ps1"
                script.write_text("[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)\n"
                                  "$OutputEncoding = [Console]::OutputEncoding\n& " +
                                  " ".join(map(quote, (shim, *args))) + "\nexit $LASTEXITCODE\n",
                                  encoding="utf-8-sig", newline="\r\n")
                return run(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                            "-File", str(script)], project, env)
            if shell == "cmd":
                # Fixed test arguments; quote every literal and reject cmd expansion.
                words = [str(shim), *args]
                if any(any(c in word for c in '%!^"\r\n') for word in words):
                    raise RuntimeError("Unsupported cmd smoke argument")
                script = temp / "invoke.cmd"
                script.write_text('@echo off\nchcp 65001 >nul\ncall ' +
                                  " ".join('"' + word + '"' for word in words) + '\nexit /b %errorlevel%\n',
                                  encoding="utf-8", newline="\r\n")
                return run(["cmd.exe", "/d", "/c", str(script)], project, env)
            return run([str(shim), *args], project, env)

        shells = ("powershell", "cmd") if os.name == "nt" else ("posix",)
        for shell in shells:
            for global_scope in (False, True):
                scope = ["--global"] if global_scope else ["--project", str(project)]
                base = home if global_scope else project
                original = b"\xef\xbb\xbf# Keep project prose\r\n"
                rules = base / (".codex/AGENTS.md" if global_scope else "AGENTS.md")
                rules.parent.mkdir(parents=True, exist_ok=True)
                rules.write_bytes(original)
                names = [name for _, name in CONTENT_FIXTURES]
                shell_invoke(shell, "add", "--agent", "codex", "--skill", *names, *scope, "--yes")
                shell_invoke(shell, "add", "--agent", "claude", "--skill", *names, *scope, "--yes")
                shared = base / ".agents/skills/survey"
                for category, name in CONTENT_FIXTURES:
                    source_root = ROOT / "skills" / category / name
                    for source in source_root.rglob("*"):
                        if source.is_file():
                            installed = base / ".agents/skills" / name / source.relative_to(source_root)
                            if installed.read_bytes() != source.read_bytes():
                                raise RuntimeError(f"Packaged content differs: {installed}")
                    installed_root = base / ".agents/skills" / name
                    for reference in re.findall(r"\]\((references/[^)]+)\)", (installed_root / "SKILL.md").read_text(encoding="utf-8")):
                        if not (installed_root / reference).is_file():
                            raise RuntimeError(f"Installed reference is missing: {name}/{reference}")
                claude = base / ".claude/skills/survey"
                if claude.resolve() != shared.resolve():
                    raise RuntimeError("Claude connection does not resolve to the shared source")
                if os.name == "nt" and claude.lstat().st_reparse_tag != stat.IO_REPARSE_TAG_MOUNT_POINT:
                    raise RuntimeError("Windows connection must be a junction, not a privileged symlink")
                listing = shell_invoke(shell, "list", *scope)
                if "survey" not in listing or "codex:" not in listing or "claude:" not in listing:
                    raise RuntimeError("Both installed agents must be listed")
                if "Already up to date" not in shell_invoke(shell, "update", *scope, "--yes"):
                    raise RuntimeError("Unchanged update rewrote installed content")
                # Mutate only the isolated installed package, simulating a new bundle.
                bundle = package / "skills/workflow/survey/SKILL.md"
                old = bundle.read_bytes()
                try:
                    bundle.write_bytes(old + b"\nPackage smoke update.\n")
                    shell_invoke(shell, "update", "--agent", "codex", *scope, "--yes")
                    if (claude / "SKILL.md").read_bytes() != bundle.read_bytes():
                        raise RuntimeError("Update did not reach the other agent")
                finally:
                    bundle.write_bytes(old)
                shell_invoke(shell, "remove", "--agent", "codex", *scope, "--yes")
                if not shared.is_dir() or not claude.is_dir() or rules.read_bytes() != original:
                    raise RuntimeError("Partial removal lost shared content or changed project prose")
                shell_invoke(shell, "remove", "--agent", "claude", *scope, "--yes")
                if any((base / ".agents/skills" / name).exists() or os.path.lexists(base / ".claude/skills" / name) for name in names):
                    raise RuntimeError("Final removal left skills or connections")
                print(f"Packed CLI: {shell}, {'global' if global_scope else 'project'} lifecycle passed.")
        print("Packed CLI: bundled bytes, shared updates, rules preservation and shell shims passed.")


if __name__ == "__main__":
    main()
