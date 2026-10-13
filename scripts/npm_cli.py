"""Invoke npm's JavaScript entrypoints without a shell or Windows .cmd parsing."""

from pathlib import Path
import shutil


def npm_command(tool="npm"):
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        raise RuntimeError("Node.js and npm must be available in PATH.")
    executable = Path(npm).resolve()
    cli = (executable.parent / "node_modules/npm/bin" / f"{tool}-cli.js"
           if executable.suffix.lower() in (".cmd", ".exe", ".ps1")
           else executable.with_name(f"{tool}-cli.js"))
    if not cli.is_file():
        raise RuntimeError(f"Cannot find npm's {tool} entrypoint: {cli}")
    return [node, str(cli)]
