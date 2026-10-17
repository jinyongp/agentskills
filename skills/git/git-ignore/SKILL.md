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

1. Identify the root, requested paths, and changes. Start with counts and filenames.
   Read applicable ancestor/nested `.gitignore` files; identify effective sources
   with `git check-ignore -v` and tracking with `git ls-files -- <paths>`.
   Limit pages to 100 paths or 150 lines; report omitted counts and next offset.
   Recover relevant pages before claiming complete coverage.
2. Identify generated, private, and required files from project evidence. Generated
   does not mean disposable: lockfiles, fixtures, shared settings, and agent
   instructions may need tracking. Resolve ambiguity; omit unused stack templates.
3. Use `.gitignore` for shared policy, Git's `info/exclude` for repository-local
   personal exclusions, and `core.excludesFile` for cross-project personal rules.
   Resolve metadata with `git rev-parse --git-path info/exclude`, including in
   worktrees. Honor requested destinations; explain scope conflicts. Personal
   rules do not replace shared policy needed by other clones.
4. Check existing coverage before adding rules. Distinguish duplicates from overlap:
   equal text in different directories has different scope; repeated rules after
   `!` exceptions can exclude again. Within one precedence level the last match
   wins; deeper `.gitignore` files override ancestors. Do not sort, deduplicate,
   or broaden mechanically. Remove redundant rules within scope only when excluded
   and retained paths, including exceptions, keep their behavior. Preserve uncertain overlaps.
5. Match intended scope, not automatically the root. For names with the same
   excluded role across subprojects, omit leading `/` (`node_modules/`,
   `*.log`); a trailing `/` restricts matches to directories. Use `/build/` for
   only the ignore file's direct build directory; `build/` covers nested names.
   Interior slashes also anchor paths relative to that ignore file. Before
   widening scope, check nested names: `bin/` may contain authored scripts and
   `dist/` may hold required distribution files. Do not enumerate subproject
   copies when one recursive rule expresses the policy. Keep ancestors traversable
   for `!` exceptions; excluded parents prevent restoring children. Preserve
   templates such as `.env.example`, order, escaping, line endings, and
   an append separator. Report tracked files instead of untracking them.
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
