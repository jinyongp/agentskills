---
name: git-conflict
description: "Resolve existing Git merge, rebase, or cherry-pick conflicts when the user asks to fix conflicts. Inspect the base and both sides, preserve unrelated work, validate the resolution, and continue only the authorized operation."
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Conflict

Resolve an existing conflict according to the intended behavior of both changes.

## When to use

Use when asked to resolve conflicts in an ongoing merge, rebase, or cherry-pick.
A request to inspect conflicts can remain read-only. Starting a new integration,
choosing a synchronization strategy, rewriting published history, and pushing
are separate actions. Do not initiate a merge to manufacture a conflict.

## Prerequisites

Use Git, a file editor, and the repository's relevant validation tools. Read its
instructions and establish which operation is active with `git status` and Git's
operation state. Use Git-aware paths such as `git rev-parse --git-path MERGE_HEAD`
rather than assuming `.git` is a directory; linked worktrees may use a file.
If no operation is active, inspect unresolved index entries and establish their
origin before editing or issuing a continuation command.

## Procedure

1. Inspect `git status`, `git diff --name-only --diff-filter=U`,
   `git ls-files -u`, the staged diff, and unrelated local changes. Record the
   operation and affected paths. Keep unrelated staged and working changes
   outside resolution edits. Before continuing, every staged change must belong
   to the operation; preserve unrelated staging separately or pause continuation
   if its exact restoration cannot be assured.
2. For each unresolved path, read the surrounding code and the source commits.
   Where index stages exist, inspect:

   ```bash
   git show :1:<path>
   git show :2:<path>
   git show :3:<path>
   ```

   Stage 1 is the common base, 2 is the current side, and 3 is the incoming side.
   Some stages are absent for added or deleted files. During rebase, the current
   side is the upstream plus commits already replayed, while the incoming side
   is the commit being replayed. Do not equate `ours` with the user's original
   feature branch in every operation.
3. Reconcile the behavior each side intended. Preserve independent changes from
   both sides and adapt tests or call sites when the conflict affects their
   contract. If mutually exclusive requirements cannot be inferred from the
   request, source, or tests, ask about that exact decision and keep the path
   unresolved. Removing markers alone is not evidence of a correct resolution.
4. Resolve only the affected paths. For rename/delete and binary conflicts,
   explicitly choose the intended path or version from evidence. For generated
   files or lockfiles, resolve their source inputs and use the project's generator
   or package manager; inspect resulting changes and preserve dependency intent.
   Do not blanket-select a side or regenerate unrelated files.
5. Stage resolved paths explicitly with `git add -- <path>` or `git rm -- <path>`
   as appropriate. Inspect their diff and `git diff --cached --check`, confirm
   unresolved index entries are gone, and run focused repository checks. Include
   automatically merged changes when reviewing the overall integration result.
   A marker scan is a supporting check, not a substitute for index and behavior
   checks. If validation fails, keep the resolution available and report the failure.
6. If the user authorized finishing the active operation and validation passes,
   run the matching `git merge --continue`, `git rebase --continue`, or
   `git cherry-pick --continue`. A resolve-only request can stop at verified staged
   resolutions. A rebase or cherry-pick may stop at another conflict: repeat the
   inspection for that commit and report completion only when the operation ends.

Abort, skip, hook bypass, and discarding changes require the corresponding user
authorization. An empty replayed commit needs inspection and a decision about its
intent; do not automatically skip it. Keep normal hooks enabled and inspect any
changes they make before retrying. Never push as part of conflict resolution alone.

## Output

Report the operation, resolved paths, how the competing behavior was reconciled,
checks run, and whether the operation is finished or waiting for continuation.
State unresolved decisions and preserved unrelated changes without claiming
that all conflicts are fixed when only one replayed commit was handled.

## Verification

Check `git status` and `git ls-files -u`, inspect the final diff or resulting
commit, and verify the expected behavior with relevant tests. For an authorized
continuation, confirm the active operation ended and the intended branch/history
was produced. Check unrelated work against its initial state.

Command reference: [git merge](https://git-scm.com/docs/git-merge),
[git rebase](https://git-scm.com/docs/git-rebase),
[git cherry-pick](https://git-scm.com/docs/git-cherry-pick).
