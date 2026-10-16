---
name: git-ignore
description: "Create, review, or refine Git ignore rules using project evidence, scope-aware duplicate handling, and checks for excluded and retained paths. Preserve tracking and unrelated configuration."
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Ignore

## Scope

- Create, review, debug, or simplify Git ignore rules using Git and project evidence.
  Review alone makes no edits. Preserve unrelated work.
- Ignore edits do not authorize untracking, deletion, history rewriting, force-add,
  or unrelated user/global configuration changes. Ignore is not an access control
  or removal of secrets from existing history.

## Procedure

1. Identify the root, requested paths, and current changes. Start with counts and
   filenames. Read applicable ancestor/nested `.gitignore`
   files and inspect effective exclude sources with `git check-ignore -v`.
   Use `git ls-files -- <paths>` for tracking; do not infer ignore sources. Limit pages
   to 100 paths or 150 lines; report omitted counts and the next offset. Recover
   all relevant pages before claiming complete coverage.
2. Identify generated, private, and required files from project commands and
   conventions. Do not copy unused templates or assume generated means disposable: lockfiles,
   fixtures, shared settings, and agent instructions may need tracking.
   Resolve ambiguity before excluding them.
3. Choose scope: shared project policy belongs in `.gitignore`; repository-local
   personal exclusions belong in Git's `info/exclude`; personal cross-project
   exclusions belong in `core.excludesFile`. Resolve Git metadata paths with
   `git rev-parse --git-path info/exclude`, including in worktrees. Follow the
   requested destination; explain scope conflicts. Personal rules do not replace
   shared policy needed by other clones.
4. Before adding a rule, check whether the intended paths are already excluded.
   Distinguish literal duplicates from overlapping coverage. Equal text in
   different directories has different scope; equal rules separated by `!`
   exceptions can intentionally exclude a path again. Within a precedence level,
   the last match wins; deeper `.gitignore` files override ancestor rules.
   Do not sort, deduplicate, or broaden rules mechanically. Remove redundant
   rules only within the requested scope and with preserved behavior for excluded
   and retained paths, including exceptions. Leave uncertain overlaps intact.
5. Make the smallest edit. Patterns are relative to their ignore file: `/build/`
   selects its direct build directory; `build/` also selects nested names.
   Trailing `/` restricts matches to directories. An excluded parent prevents
   `!` from restoring a child; keep required ancestors traversable. Preserve
   `.env.example` or other intended templates when excluding local variants.
   Preserve rule order, escaping, line endings, and a separating newline when
   appending. Tracked files remain tracked; report them instead of untracking.
6. Check representative excluded AND retained paths, nested same-name paths,
   and affected exceptions with `git check-ignore -v -n -- <paths>`.
   Verbose output for a `!` pattern means inclusion, not exclusion. Default checks
   omit tracked files; use `--no-index` only to inspect hypothetical matching,
   never as proof tracking stopped. Compare cleanup outcomes before/after.
   Inspect the scoped diff and status; report failed checks and unchecked paths.

## Result

Report changed rules and scope, overlap decisions, excluded/retained path checks,
and remaining tracked files or uncertainty. For syntax disputes, consult the
[Git ignore manual](https://git-scm.com/docs/gitignore) and
[check-ignore manual](https://git-scm.com/docs/git-check-ignore).

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
