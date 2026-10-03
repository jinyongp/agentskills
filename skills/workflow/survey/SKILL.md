---
name: survey
description: Inspect a repository or working directory before implementation. Find relevant structure, project commands, ownership boundaries, and risks through read-only inspection without running project code.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Survey

## Scope

- Map the selected repository or directory for the current task; cwd is the default.
  Keep inspection read-only; save a report only when requested.
  Implementing changes, installing dependencies, and starting
  services are separate actions.
- Inspect manifests as data. Their scripts and hooks are not authorization to run
  code. Preserve existing files and avoid loading credentials.

## Procedure

1. Read applicable repository instructions, then execute the bundled helper without
   reading its source: `python3 scripts/inspect_repo.py --root <directory>`.
   Python 3.11+ is required. The default reports directory counts and project markers;
   it runs no Git or project commands and does not scan recursively.
2. Request only needed detail:
   - `--mode entries` lists direct children, with exact names and kinds.
   - `--mode commands --manifest package.json` lists package scripts.
   - `--mode commands --manifest pyproject.toml` lists Python entrypoints,
     which are not automatically test commands.
   Reports stay within 4,000 characters. Use `--offset <next_offset>` for required
   pages; total and omissions are explicit. An oversized item fails visibly.
   Narrow `--root` to a relevant package instead of dumping a monorepo.
3. Resolve toolchain and command conventions from manifests, lockfiles, CI, and
   relevant docs. A marker is a clue, not proof of the active manager or version.
   Inspect other formats through targeted reads; the helper only parses JSON/TOML.
4. Locate likely source, tests, fixtures, generated files, public contracts, and
   ownership boundaries through scoped searches. Inspect only paths that affect
   the task. Check relevant Git state only when it informs preservation or scope.
5. Identify concrete risks: shared modules, data migrations, required services,
   generated outputs, or unclear ownership. Separate observations from assumptions.
   Recommend the smallest next checks without claiming they have run.

## Result

Return a short map: project shape, relevant commands with sources, likely paths,
material risks, and next checks. Link existing instructions rather than copying
them. Missing manifests or tools are findings, not reasons to invent a setup.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
