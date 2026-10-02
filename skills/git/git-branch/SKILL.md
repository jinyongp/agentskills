---
name: git-branch
description: "Create, switch, rename, or delete local Git branches when the user requests branch management. Preserve staged and unstaged changes and verify the starting point and worktree usage."
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Branch

Manage local branch references and the current checkout without losing work.

## When to use

Use when the user asks to create, switch, rename, delete, or inspect local branches.
Identify the requested action, branch name, and starting point. Follow the user's
name or repository naming convention; do not impose a universal prefix.
Remote publication, remote deletion, history rewriting, and conflict resolution
are separate actions and require the corresponding request.

## Prerequisites

Use Git and a shell in the requested worktree. Follow its repository instructions.
If there is no worktree or an unresolved merge, rebase, or cherry-pick, report the
state before attempting a branch switch. Listing branches can still be read-only.

## Procedure

1. Inspect the branch, index, working files, and other worktrees:

   ```bash
   git status --short --branch
   git branch -vv
   git worktree list --porcelain
   git diff
   git diff --cached
   git ls-files --others --exclude-standard
   ```

2. Resolve the starting point for creation. Use a named base when supplied; use
   current HEAD for a request to branch from the current work. If the user needs
   an updated remote base, establish that explicitly before fetching. Validate
   the name with `git check-ref-format --branch <name>` and check for an existing
   local branch. Existing names must not be reset to make creation succeed.
3. Choose the smallest action:
   - Create and switch: `git switch -c <name> <start-point>`.
   - Create without switching: `git branch <name> <start-point>`.
   - Switch to an existing local branch: `git switch --no-guess <name>`.
   - Create a tracking branch only for the identified remote branch:
     `git switch -c <name> --track <remote>/<branch>`.
   - Rename a local branch: `git branch -m <old-name> <new-name>`.
   - Delete a requested local branch: inspect its unique commits and the intended
     integration target, then use `git branch -d <name>` only when no needed work
     will be lost. Git's merged check alone does not prove it reached that target.
4. Preserve staged, unstaged, and untracked work. A normal switch may carry local
   changes when safe; verify their content and staging after the switch. If Git
   refuses due to overwritten work or a branch used by another worktree, stop that
   action and explain the path or worktree. Do not automatically stash, commit,
   force a switch, reset a branch, or delete an occupied worktree.
5. Forced deletion or replacement requires explicit authorization for that named
   branch and its lost commits. Inspect first; a generic cleanup request does not
   authorize dropping unmerged work. Leave remote branches unchanged.

Substitute user-controlled names as quoted command arguments, not shell code.

## Output

Report the action, resulting branch, starting commit or tracking branch, and any
remaining blocker. State whether the checkout changed and whether existing work
was carried into it. For listing requests, show branches without mutating them.

## Verification

Check `git status --short --branch`, `git branch -vv`, and the relevant branch
reference. Compare affected staged and unstaged changes with the inspected state.
For deletion or rename, verify the exact old and new references rather than
assuming success from a message. No unrelated branch or global config may change.

Command reference: [git switch](https://git-scm.com/docs/git-switch),
[git branch](https://git-scm.com/docs/git-branch).
