---
name: index
description: "Select installed skills before starting a task. Read a compact catalog by category, then load only the applicable skill instructions."
license: MIT
metadata:
  author: jinyongp
  category: tooling
---

# Index

## Scope

Choose relevant installed skills before starting a new substantive task. This is
a compact catalog of this collection, not an external search or installer.
Each listed skill remains usable alone. A listing does not prove installation.

## Procedure

1. Choose categories below from the requested outcome: explain, plan, implement,
   review, fix, or execute. Read relevant category pages before opening candidate
   SKILL.md files. Pages stay within 2,500
   characters and give counts and exact continuation paths. Inspect further pages
   as needed; a partial list cannot prove that no relevant skill exists.
2. Match candidates to the session's available skills and exact paths, or inspect
   known local skill locations. This collection's catalog includes skills that
   may not be installed. Selection does not authorize installation.
3. Read selected SKILL.md files before work: the task workflow plus relevant
   platform, language, or presentation guidance. Preserve the requested scope:
   code-review reports defects; review-loop also fixes them. Summaries do not
   replace instructions, and repository paths are not installed paths.
4. Reuse loaded instructions during the same task; reconsider when scope changes.
   If no available skill fits, proceed within the user's scope.

## Choose a catalog

<!-- index:catalog:start -->

- [Frontend](references/catalog/frontend.md) — UI, accessibility, responsive layouts, and motion (15 skills; 1 page).
- [Git](references/catalog/git.md) — Commits, branches, synchronization, conflicts, PRs, and worktrees (6 skills; 1 page).
- [Tooling](references/catalog/tooling.md) — Skill selection, skill review, and development tool operation (2 skills; 1 page).
- [Workflow](references/catalog/workflow.md) — Planning, implementation, review, debugging, testing, and research (33 skills; 2 pages).
- [Writing](references/catalog/writing.md) — Documentation, drafting, editing, summaries, and conversation styles (10 skills; 1 page).

<!-- index:catalog:end -->

## Result

Continue the requested task using the selected instructions. Mention selected
skills briefly when useful; do not produce a separate selection report or saved
record for every task. Missing required instructions remain an explicit gap.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
