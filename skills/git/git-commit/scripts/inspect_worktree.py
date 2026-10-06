"""Read-only Git worktree inspection with bounded JSON output; Python 3.11+."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

OUTPUT_LIMIT = 4000  # Characters, including JSON escaping and the final newline.


class InspectionError(Exception):
    pass


def encoded(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")) + "\n"


class BoundedParser(argparse.ArgumentParser):
    def error(self, message):
        print(encoded({"error": message[:200]}), end="")
        raise SystemExit(2)


def git(repo, *args, optional=False):
    try:
        result = subprocess.run(
            ["git", "--no-optional-locks", "--literal-pathspecs", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            capture_output=True, timeout=30,
        )
    except FileNotFoundError as exc:
        raise InspectionError("Git is unavailable.") from exc
    except subprocess.TimeoutExpired as exc:
        raise InspectionError("Git inspection timed out; no mutation attempted.") from exc
    if optional and result.returncode == 1:
        return b""
    if result.returncode:
        # Git stderr can contain credentials or user-controlled content.
        raise InspectionError(f"git {args[0]} failed (exit {result.returncode}).")
    return result.stdout


def decode(value):
    return value.decode("utf-8", "surrogateescape")


def status(repo):
    records = iter(git(repo, "status", "--porcelain=v2", "--branch", "-z", "--untracked-files=all").split(b"\0"))
    branch, files = {}, []
    for raw in records:
        if not raw:
            continue
        text = decode(raw)
        if text.startswith("# branch."):
            key, value = text[9:].split(" ", 1)
            branch[key] = value
        elif text.startswith("? "):
            files.append({"xy": "??", "path": text[2:]})
        elif text[0] in "12u":
            kind = text[0]
            parts = text.split(" ", {"1": 8, "2": 9, "u": 10}[kind])
            entry = {"xy": parts[1], "path": parts[-1]}
            if kind == "2":
                entry["from"] = decode(next(records))
            if kind == "u":
                entry["conflict"] = True
            if parts[2] != "N...":
                entry["submodule"] = parts[2]
            files.append(entry)
        else:
            raise InspectionError("Unsupported Git status record; inspect with targeted tooling.")
    return branch, files


def file_page(payload, files, offset, limit):
    if offset > len(files):
        raise InspectionError("File offset exceeds the current file count; refresh the summary.")
    shown = files[offset:offset + limit]
    while True:
        next_offset = offset + len(shown)
        payload["files"] = {
            "total": len(files), "offset": offset, "items": shown,
            "next_offset": next_offset if next_offset < len(files) else None,
        }
        if len(encoded(payload)) <= OUTPUT_LIMIT:
            if not shown and offset < len(files):
                raise InspectionError("A file entry exceeds the output budget; use targeted tooling.")
            return payload
        if not shown:
            raise InspectionError("Repository metadata exceeds the output budget; use targeted tooling.")
        shown.pop()


def text_page(mode, content, offset, **extra):
    if offset > len(content):
        raise InspectionError("Text offset exceeds the current output length; refresh the query.")

    def payload(size):
        end = offset + size
        return {**extra, "mode": mode, "total_chars": len(content), "offset": offset,
                "text": content[offset:end], "next_offset": end if end < len(content) else None}

    low, high = 0, min(OUTPUT_LIMIT, len(content) - offset)
    while low < high:
        middle = (low + high + 1) // 2
        if len(encoded(payload(middle))) <= OUTPUT_LIMIT:
            low = middle
        else:
            high = middle - 1
    return payload(low)


def inspect(args):
    repo = Path(decode(git(args.repo, "rev-parse", "--show-toplevel")).removesuffix("\n"))
    branch, files = status(repo)
    if args.mode == "files":
        return file_page({"mode": "files"}, files, args.offset, args.limit)
    if args.mode == "diff":
        if not args.path:
            raise InspectionError("diff requires --path for the file(s) to inspect.")
        for path in args.path:
            relative = Path(path)
            if relative.is_absolute() or ".." in relative.parts or path in ("", ".") or (repo / path).is_dir():
                raise InspectionError("--path must name a file relative to the repository root.")
        options = ["--cached"] if args.staged else []
        content = decode(git(repo, "diff", "--no-ext-diff", "--no-textconv", "--no-color", *options, "--", *args.path))
        return text_page("staged_diff" if args.staged else "diff", content, args.offset)
    unborn = branch.get("oid") == "(initial)"
    if args.mode == "history":
        content = "" if unborn else decode(git(repo, "log", "-n", "5", "--format=%s"))
        return text_page("history", content, args.offset)
    template = decode(git(repo, "config", "--path", "--get", "commit.template", optional=True)).removesuffix("\n")
    if args.mode == "template":
        if not template:
            return {"mode": "template", "present": False}
        path = Path(template).expanduser()
        if not path.is_absolute():
            path = repo / path
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise InspectionError("Configured commit template is unreadable.") from exc
        content = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
        return text_page("template", content, args.offset, present=True)
    git_dir = Path(decode(git(repo, "rev-parse", "--absolute-git-dir")).removesuffix("\n"))
    operations = [label for name, label in (
        ("MERGE_HEAD", "merge"), ("rebase-merge", "rebase"), ("rebase-apply", "rebase-or-am"),
        ("CHERRY_PICK_HEAD", "cherry-pick"), ("REVERT_HEAD", "revert"), ("sequencer", "sequencer"),
    ) if (git_dir / name).exists()]
    counts = {"staged": 0, "unstaged": 0, "untracked": 0, "conflicted": 0}
    for entry in files:
        if entry.get("conflict"):
            counts["conflicted"] += 1
        elif entry["xy"] == "??":
            counts["untracked"] += 1
        else:
            counts["staged"] += entry["xy"][0] != "."
            counts["unstaged"] += entry["xy"][1] != "."
    recent = [] if unborn else decode(git(repo, "log", "-n", "3", "--format=%s")).splitlines()
    subjects = [{"text": value[:120], "truncated": len(value) > 120} for value in recent]
    ahead, behind = (int(value[1:]) for value in branch["ab"].split()) if "ab" in branch else (None, None)
    payload = {"mode": "summary", "repository": str(repo), "branch": branch.get("head"),
               "head": branch.get("oid"), "upstream": branch.get("upstream"),
               "ahead": ahead, "behind": behind, "operations": operations,
               "counts": counts, "recent_subjects": subjects, "template_present": bool(template)}
    return file_page(payload, files, args.offset, args.limit)


def main():
    parser = BoundedParser(description=__doc__)
    parser.add_argument("mode", nargs="?", choices=("summary", "files", "diff", "history", "template"), default="summary")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--path", action="append", help="Exact file path relative to repository root; repeatable")
    parser.add_argument("--staged", action="store_true", help="Read index diff instead of worktree diff")
    parser.add_argument("--offset", type=int, default=0, help="File index or decoded text character offset")
    parser.add_argument("--limit", type=int, default=20, help="Maximum file entries per page (1-100)")
    args = parser.parse_args()
    try:
        if args.offset < 0 or not 1 <= args.limit <= 100:
            raise InspectionError("Use offset >= 0 and a file limit between 1 and 100.")
        if (args.staged or args.path) and args.mode != "diff":
            raise InspectionError("--staged and --path apply only to diff mode.")
        payload = inspect(args)
        output = encoded(payload)
        if len(output) > OUTPUT_LIMIT:
            raise InspectionError("Output exceeds budget; use a narrower query.")
    except (InspectionError, OSError) as exc:
        print(encoded({"error": str(exc)[:200]}), end="")
        return 1
    print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
