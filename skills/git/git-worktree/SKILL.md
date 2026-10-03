---
name: git-worktree
description: Create, inspect, remove, or maintain requested Git worktrees for parallel work. Verify branch usage, paths, locks, and local changes while preserving existing work.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Worktree

## Scope

- Manage only requested worktree paths and local refs. Worktrees share repository
  refs and most configuration; each checkout has its own HEAD, index, and files.
- Preserve existing work and other worktrees. Creation does not authorize copying
  local changes, installing dependencies, starting services, or publishing branches.
  Removing a worktree does not authorize deleting its branch.

## Procedure

1. Execute the Python 3.11+ helper without reading its source:
   `python3 scripts/inspect_worktrees.py --repo <repository>`.
   Default output gives registry counts without inspecting every checkout.
2. Add `--mode list` for exact paths, refs, and lock/prunable state. Reports stay
   within 4,000 characters including JSON escaping and newline. Follow
   `--offset <next_offset>` for relevant pages; totals and omissions are explicit.
   Refresh if the registry changes; oversized entries fail rather than being shortened.
3. Resolve an explicit base, unused absolute destination, and branch name consistent
   with repository rules. Validate a new branch name and check whether an existing
   branch is already used by another worktree. A fresh remote base needs an
   authorized fetch; do not overwrite an existing path or reset a branch.
4. Use the smallest requested creation, with quoted arguments:
   - New branch: `git worktree add -b <name> <path> <base>`.
   - Existing unused branch: `git worktree add <path> <branch>`.
   - Detached checkout, when requested: `git worktree add --detach <path> <commit>`.
   If Git rejects an occupied branch/path, report it without forced replacement.
5. Before removing a registered linked worktree, inspect
   `--mode state --path <absolute-path>` for local changes and active Git operations.
   Check locks and known jobs using the target. If ignored files exist, inspect
   needed pages with `--mode ignored --path <absolute-path>`; Git-clean alone
   does not establish that valuable local data is absent.
   Preserve valuable work or obtain authorization for the identified loss.
6. Remove the requested clean, unused linked checkout from another worktree using
   `git worktree remove <absolute-path>`. Keep the main checkout and branch.
   Force requires explicit authorization covering the target and loss; do not
   automatically stash, discard, unlock, or delete files to bypass a refusal.
7. For a requested lock/unlock, move, repair, or stale-registry cleanup, read
   [references/registry-care.md](references/registry-care.md).
8. Verify registry, intended branch/HEAD, and preserved original work. Report
   missing paths, locks, or active operations instead of treating cleanup as complete.

## Result

Report action, exact worktree path and branch/base, preserved work, and blockers.
Read-only requests return relevant registry/state findings only.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
