---
name: git-commit
description: >-
  Stage or unstage changes, split coherent commits, and draft repository-style
  commit messages when the user asks to commit, stage, unstage, split commits,
  or write a commit message. Inspect the whole worktree and preserve excluded
  changes. Use for commit preparation, not branch management or publishing.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Commit

Prepare repository-style commits while preserving the user's scope and work.

## When to use

Use for committing, staging, unstaging, splitting pending changes into commits,
or drafting commit messages. Match the requested action: a message-only request
leaves both index and worktree unchanged; staging or unstaging alone does not
authorize a commit. A commit request does not authorize a push.

Branch creation, merge, rebase, squash, and publication need their own requested
workflow. Amend, history rewriting, hook bypasses, and force-push require explicit
authorization. Do not edit source files merely to make a commit succeed.

## Prerequisites

Use Git and a shell inside the target worktree. Follow the repository's existing
instructions, validation commands, and execution environment.

Pause the affected commit if Git is unavailable, the directory is not a worktree,
there are unresolved conflicts, or an unrequested merge, rebase, or cherry-pick
is in progress. Accept a detached HEAD only when the user has agreed to it.
For an initial commit, missing history is expected.

## Inspect before staging

Find the repository root, then inspect staged, unstaged, and untracked changes:

```bash
git rev-parse --show-toplevel
git status --short --branch
git diff --stat
git diff --cached --stat
git diff
git diff --cached
git ls-files --others --exclude-standard
git diff --name-only --diff-filter=U
git log --format='%h %s' -n 20
git config --show-origin --get-all commit.template
```

Read the configured commit template if present; its non-comment text can impose
message requirements. An unset template is normal. Inspect untracked files
before staging; names and statistics alone do not establish their contents.

Identify credentials, private keys, local configuration, caches, generated
artifacts, and unexpected large binaries. Keep accidental files out of commits.
If an in-scope file contains a secret, pause that commit and explain the affected
path without reproducing the secret. Stage ignored files only when the user
explicitly includes them and their contents are appropriate.

## Choose scope and groups

An unrestricted commit request covers tracked and untracked changes. Explicit
paths, hunks, concerns, exclusions, or a request for only staged changes override
that default. Treat the existing index as a draft unless the user chose it as
the scope. Inspect the whole worktree to understand context, but mutate only the
requested scope.

Group by behavior rather than file type. Keep code, tests, fixtures, generated
output, configuration, and documentation together when they implement one change.
Split independent concerns, including independent hunks in one file. Commit
prerequisites before dependent groups.

An ordinary `git commit` includes the entire index. Before a scoped commit,
account for every staged hunk. For excluded staged changes on separate paths,
save their binary-capable cached patch outside the worktree, temporarily unstage
only those paths, commit the chosen group, then reapply the patch to the index.
Verify that their staged diff and worktree contents match the saved state. Restore
excluded staging even if validation or the commit fails; keep the saved patch
until restoration is verified. If scopes overlap or exact restoration is unclear,
pause the affected commit instead of guessing or discarding work.

## Stage, validate, and commit

For each group:

1. Compare the index and worktree before staging. Use explicit paths for whole
   files and `git add -p` or `git apply --cached` for selected hunks. Whole-file
   staging must not absorb excluded or later-group changes.
2. Inspect `git diff --cached --stat`, `git diff --cached`, and
   `git diff --cached --check`. Confirm the index contains exactly this group.
3. Run the relevant checks required by the repository. State any skipped checks
   and their reason. If checks fail, preserve the changes and report the failure;
   fixing source files or bypassing hooks needs the corresponding authorization.
4. Follow repository instructions, its commit template, and recent message style.
   When appropriate, use `type(scope): imperative description`. Explain motivation,
   migration, or material side effects in the body only when useful.
5. Write the message to a temporary file and use `git commit -F <message-file>`.
   Keep normal hooks enabled. If a hook fails or modifies files, inspect the new
   state before retrying; do not claim a successful commit until Git confirms it.
6. Restore any temporarily excluded staging. Check status, staged and unstaged
   diffs, and the new commit's actual contents. Continue until the requested
   groups are committed or a specific blocker prevents progress.

For a staging, unstaging, or message-only request, stop after that requested result
and its verification. An empty scope needs a clear explanation, not an empty commit.

## Report the result

List each new commit's hash and subject, why changes were grouped, and checks that
actually ran. Report remaining in-scope changes and their blockers, and confirm
excluded work is preserved. For preparation-only requests, describe the resulting
index state or provide the drafted message without implying a commit was made.
