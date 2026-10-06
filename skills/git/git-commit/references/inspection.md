# Inspection output

Use Python 3.11+ and Git. Execute `scripts/inspect_worktree.py` from the installed skill;
paths below are relative to that skill, not the target repository.

| Query | Information |
| --- | --- |
| `python3 scripts/inspect_worktree.py --repo <repo>` | Branch/HEAD, cached upstream counts, active operations, all change counts, first file page, 3 recent subjects, template presence |
| `python3 scripts/inspect_worktree.py files --repo <repo> --offset <next_offset>` | Next file page; includes status, exact paths, rename source, conflicts and submodule state |
| `python3 scripts/inspect_worktree.py diff --repo <repo> --path <file> --staged` | One selected file's index diff; omit `--staged` for its working diff |
| `python3 scripts/inspect_worktree.py history --repo <repo>` | Last 5 subjects when the initial sample is insufficient |
| `python3 scripts/inspect_worktree.py template --repo <repo>` | Configured template's non-comment text |

Every successful stdout response is JSON of at most 4,000 characters including
escaping and its newline. File pages have `total`, `offset`, `items`, `next_offset`;
text pages have `total_chars`, `offset`, `text`, `next_offset`. Follow every
non-null offset for information needed by the task. Offsets refer to the current
query: refresh after repository changes. Counts cover all files, including omitted
pages. A long recent subject has `truncated: true`; request history if needed.

The helper never fetches, stages, commits, or prints file contents in its summary.
Inspection queries disable filesystem-monitor hooks; actual commit hooks remain enabled.
Diff requests need exact repository-relative files. New files need a separate
bounded content read. Diff and template text may contain sensitive data: request
only the scope needed, inspect locally, and keep secrets out of user-facing output.
An error is JSON with a nonzero exit code. Missing history on an unborn branch
and an unset template are normal. Stop affected work on unavailable Git, failed
inspection, or an unreadable required template; do not treat incomplete output
as proof the worktree is clean. Extremely large path metadata needs targeted
tooling, rather than silently shortened paths.
