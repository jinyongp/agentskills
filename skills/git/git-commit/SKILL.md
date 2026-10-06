---
name: git-commit
description: Commit, stage, unstage, split pending commits, or draft commit messages when requested. Inspect changes, preserve excluded work, and follow repository message conventions.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Commit

## Scope

- Match the requested action. Message-only leaves index/worktree unchanged;
  staging alone creates no commit; committing alone does not authorize push.
- Unrestricted commit scope includes tracked and untracked work. Explicit paths,
  hunks, exclusions, or staged-only requests override it; existing staging is a draft.
- Use Git and Python 3.11+. Follow target repository instructions and checks.
  Pause affected commits for conflicts, an unrelated active operation, unsupported
  detached HEAD, secrets, or failed checks. Missing initial history is normal.
- Source edits, amend/history rewriting, force, and hook bypass need authorization.

## Procedure

1. Run `python3 <skill-root>/scripts/inspect_worktree.py --repo <repo>`; execute the bundled
   helper without loading its source. Start with its bounded summary, not full diffs.
2. Inspect all candidate paths, then only their relevant content/diff. Follow
   non-null `next_offset` values before treating a requested scope as reviewed.
   Read [inspection.md](references/inspection.md) for file pages, selected diffs,
   history, or a configured template. Read template text only when present, more
   history only when the sample cannot establish style. Untracked files need bounded
   content reads; protect secrets and accidental local files. Force-add only explicitly
   requested, appropriate ignored files. Failed/incomplete inspection is not a clean state.
3. Group by behavior; keep related code/tests/docs together, split independent
   hunks, and commit prerequisites first. Preserve excluded staged and working
   changes. Read [scoped-staging.md](references/scoped-staging.md) only when an
   excluded staged change needs temporary separation. Pause on unsafe overlap.
4. Stage explicit paths or hunks. Inspect this group's cached diff in bounded
   file pages; never stage unreviewed changes. Run `git diff --cached --check`
   and required relevant checks. Preserve changes on failure; inspect hook edits
   before retrying and keep normal hooks enabled.
5. Follow repository instructions, template, and message style. Read
   [conventional-commits.md](references/conventional-commits.md) only when requested
   or used by the repository. Prefer an imperative subject when it fits those
   conventions, and use a body only for useful
   context. Write a temporary message file,
   then `git commit -F <file>` when committing was requested. Preparation-only
   requests stop at the requested index state or message; do not create empty commits.
6. Restore excluded staging on success or failure. Refresh the summary and verify
   actual commit contents, preserved work, and remaining groups; continue only within scope.

## Result

Report hashes/subjects or the prepared message/index state, checks actually run,
preserved exclusions, and remaining blockers. Do not imply a commit or push occurred.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
