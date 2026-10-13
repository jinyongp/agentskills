# Inspect a Git worktree

Use Python 3.11+ and Git. Execute these commands from the installed skill;
`repo`, `file`, and offsets below are placeholders for the selected target and page.
Script paths are relative to the skill, not the target repository.

## Start with a summary

Get branch/HEAD, cached upstream counts, active operations, all change counts,
the first file page, three recent subjects, and template presence:

```bash
python3 scripts/inspect_worktree.py --repo <repo>
```

## Read file pages

Use the returned offset for status, exact paths, rename sources, conflicts, and
submodule state:

```bash
python3 scripts/inspect_worktree.py files --repo <repo> --offset <next_offset>
```

## Inspect one file's diff

Read the selected file's index diff. Omit `--staged` for its working-tree diff:

```bash
python3 scripts/inspect_worktree.py diff --repo <repo> --path <file> --staged
```

New files need a separate bounded content read; diff queries require exact
repository-relative paths.

## Read more history

Get the last five subjects when the summary's sample is insufficient:

```bash
python3 scripts/inspect_worktree.py history --repo <repo>
```

## Read a configured template

Get its non-comment text:

```bash
python3 scripts/inspect_worktree.py template --repo <repo>
```

## Recover complete output

Successful stdout is JSON of at most 4,000 characters, including escaping and newline.

- **File pages:** `total`, `offset`, `items`, and `next_offset`.
- **Text pages:** `total_chars`, `offset`, `text`, and `next_offset`.
- Follow non-null offsets for information needed by the task. They belong to the
  current query; refresh after repository changes.
- Counts cover all files, including omitted pages. A long recent subject has
  `truncated: true`; request history if needed.

## Preserve scope and handle failures

- The helper never fetches, stages, commits, or prints file contents in its summary.
  Inspection disables filesystem-monitor hooks; actual commit hooks remain enabled.
- Diffs and templates can contain sensitive data. Request only needed scope, inspect
  locally, and keep secrets out of shared output.
- Errors are JSON with a nonzero exit code. Missing history on an unborn branch and
  an unset template are normal.
- Stop affected work when Git, required inspection, or a required template is unavailable.
  Incomplete output does not establish a clean worktree.
- Extremely large path metadata needs targeted tooling; never silently shorten paths.
