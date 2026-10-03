---
name: git-pr
description: Draft, create, or update GitHub PR titles and descriptions when requested. Inspect committed changes, follow the template, and verify target identity and existing PRs before publication.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git PR

## Scope

- Use Git; publishing also needs authenticated gh or a GitHub connector.
  Follow repository instructions/templates. Resolve repository, base, head owner/
  branch, and draft/ready state; use verified metadata for an existing PR.
- Drafting authorizes text only. Reuse authorization for requested creation/update.
  Commits, review, merge/close, reviewers, labels, and assignments need their own scope.
- Keep uncommitted work separate from published contents; preserve it.

## Procedure

1. Inspect identity, branch and local-change summaries first. Distinguish local
   HEAD from the PR's published head, especially for forks. Verify authentication
   before remote writes without printing credentials.
2. Determine the merge base. Start with committed file/commit summaries, then read
   relevant diff in bounded path/hunk queries: `git log <base>..<head>` and
   `git diff <base>...<head> -- <path>`. Independent base changes and uncommitted
   work are excluded. Refresh stale refs when needed; report shallow/fork limits.
   Inspect the complete requested change progressively; an empty change needs no PR.
3. Write for a reviewer new to the task: concrete problem, resulting behavior,
   actual checks, material limitations/migration. Follow the template, omit abandoned
   approaches, and preserve relevant existing context outside the requested edits.
4. Return prepared text for drafting. For publication, verify the exact target/
   published head; push only the selected branch when required and authorized by
   the PR request. No force-push, unrelated branches, or automatic tag publication.
5. Check open PRs by target repository, head owner/branch, and base before creating.
   Reuse the applicable PR; disambiguate multiple matches. Use structured connector
   fields or gh's explicit repo/base/head/title options and `--body-file <file>`;
   editing uses the verified PR identity. Preserve literal text and real newlines
   in a temporary file outside the worktree. Quote arguments or use argument arrays.
6. Honor requested draft/ready state and state missing readiness checks. Preview
   text locally: `gh pr create --dry-run` can push and is not read-only.
   On uncertain write results, query before retrying; avoid duplicate creation or
   blind overwrites of concurrent edits.
7. Read back URL, base/head and head commit, title/body, and draft state. Verify
   the intended PR changed while unrelated fields/PRs stayed intact. Attach its
   URL when the host provides a task attachment tool.

## Result

Return title/body for drafting, or PR URL and created/updated state for publication.
Include actual checks, unpublished in-scope work, and blockers; preserve prepared
text when authentication or publication fails.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
