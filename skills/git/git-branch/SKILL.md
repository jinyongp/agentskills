---
name: git-branch
description: Create, switch, rename, delete, or inspect local Git branches when requested. Verify the starting point and worktree usage while preserving existing changes.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Branch

## Scope

- Use Git in the target worktree; follow repository instructions and branch names.
- Manage only requested local references. Remote publication/deletion and history
  rewriting need their own scope. Listing is read-only.
- Preserve staged, unstaged, and untracked work. Forced replacement/deletion needs
  authorization for the named branch and commits that would be lost.

## Procedure

1. Inspect current/target refs, dirty/index state, active operations, and target
   worktree usage with bounded queries. Start with status, not all file contents.
   Pause a switch during an unrelated merge/rebase/cherry-pick.
2. Resolve the requested starting point; current HEAD is appropriate for branching
   from current work. A fresh remote base needs an authorized fetch. Validate
   `git check-ref-format --branch <name>`; an existing name must not be reset.
3. Use the smallest action, substituting quoted arguments:
   - Create and switch: `git switch -c <name> <start-point>`.
   - Create only: `git branch <name> <start-point>`.
   - Switch local: `git switch --no-guess <name>`.
   - Track a verified remote: `git switch -c <name> --track <remote>/<branch>`.
   - Rename: `git branch -m <old> <new>`.
   - Delete: inspect unique commits and their intended integration target before
     `git branch -d <name>`; Git's merged check alone does not establish that target.
4. A normal switch can carry compatible local work; verify its content and staging.
   If Git rejects an overwrite or a branch occupied by another worktree, stop and
   report it. Do not automatically stash, commit, discard work, or delete a worktree.
5. Verify resulting refs/checkout and preserved changes. Leave other branches,
   remote refs, and global configuration unchanged.

## Result

Report the action, branch/start commit or tracking target, carried work, and blockers.
Listing requests report only the relevant branches.
