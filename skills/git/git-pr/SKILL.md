---
name: git-pr
description: "Draft, create, or update GitHub pull requests when the user asks for a PR or PR title and description. Inspect the committed base-to-head changes, follow repository templates, and verify the target and existing PR before publishing."
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git PR

Write a reviewable GitHub pull request from the actual committed change.

## When to use

Use for drafting a PR title/body, creating a PR, or editing an identified PR's
title/body. A drafting request authorizes preparation only. A creation or update
request authorizes the corresponding remote write within its stated scope; reuse
existing authorization rather than requesting confirmation for every command.
Commit creation, code review, merge, closing a PR, review requests, and unrelated
labels or assignments need their own requested scope.

## Prerequisites

Use Git in the target repository. GitHub publication also needs the GitHub CLI
(`gh`) or an available authenticated GitHub connector with permission for that
repository. Drafting can proceed without remote access, with that limit stated.
Follow repository instructions and its PR template. Resolve the target repository,
base branch, head branch/owner, and requested draft or ready state from evidence.
For an existing PR, use its verified identity and base/head metadata.

## Procedure

1. Inspect status, branch tracking, repository identity, and any requested PR.
   Distinguish the local commit from the published head; an existing PR may come
   from a fork or a different branch. Inspect staged, unstaged, and untracked
   changes, but do not silently commit them or describe them as published content.
   Verify authentication before remote mutation without printing credentials.
2. Inspect the committed change against the verified base:

   ```bash
   git merge-base <base-ref> <head-ref>
   git log --oneline <base-ref>..<head-ref>
   git diff --stat <base-ref>...<head-ref>
   git diff <base-ref>...<head-ref>
   ```

   Read the full diff, relevant tests, and repository PR template. A base branch's
   independent changes are not part of the proposed change. Refresh stale refs
   when needed, and identify shallow-history or unavailable-fork limits before
   claiming a complete comparison. An empty change needs explanation, not a PR.
3. Write the title and body for a reviewer who has not seen the conversation.
   Lead with the concrete problem and resulting behavior; use a before/after
   example when useful. Follow the template and scale detail to the change.
   Include checks that actually ran, material limitations, and migration details
   when relevant. Exclude abandoned approaches and unsupported claims. For an
   update, preserve relevant context and fields outside the requested edits.
4. For drafting, return the prepared text without pushing or creating a PR.
   For publication, verify the exact repository and published head. Push the
   selected branch only when it is required by and authorized within the PR
   request; otherwise leave the prepared PR text ready and state the missing
   publication step. Never force-push or publish unrelated branches or tags.
5. Before creating, look up open PRs for the verified head owner, branch, and base
   in the target repository. Reuse an applicable existing PR rather than create a
   duplicate; multiple matches need disambiguation. Write the body to a temporary
   file outside the worktree, preserving real newlines and literal shell syntax.
   Use structured connector fields or commands such as:

   ```bash
   gh pr create --repo <repository> --base <base> --head <verified-head> --title <title> --body-file <body-file>
   gh pr edit <pr-url> --repo <repository> --title <title> --body-file <body-file>
   ```

   Substitute quoted arguments or an argument array. Use `--draft` when requested
   or required by repository policy. If required readiness checks remain incomplete,
   state that before publishing as ready. Do not use `gh pr create --dry-run` as a
   read-only preview: it may push changes. Preview the prepared text locally.
6. Read back the created or edited PR and verify its URL, base, head, title, body,
   and draft state. After a timeout or uncertain write result, query GitHub before
   retrying; do not create a duplicate or overwrite a concurrent change blindly.
   Report permission, authentication, or validation failures and preserve the
   prepared body for the requested follow-up.

## Output

For drafting, return the title/body and any verification gap. For publication,
return the PR URL, whether it was created or updated, its base/head and draft state,
and checks run. Report any unpublished local changes affecting the user's intended
scope. Attach the PR to the current task if the host provides an attachment tool.

## Verification

Confirm the description matches the committed diff and actual validation. Verify
the remote result after writing, including the head commit, without changing
reviewers, labels, merge state, or other PRs. A successful command alone does not
prove the intended PR was updated.

Command reference: [gh pr create](https://cli.github.com/manual/gh_pr_create),
[gh pr edit](https://cli.github.com/manual/gh_pr_edit).
