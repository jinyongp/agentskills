---
name: git-conflict
description: Resolve existing merge, rebase, or cherry-pick conflicts when requested. Inspect both sides, preserve unrelated work, validate the result, and continue the authorized operation.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Conflict

## Scope

- Use Git, an editor, and repository checks. Resolve an existing conflict;
  inspection-only stays read-only. Starting integration and pushing are separate.
- Identify the active operation with status and Git-aware paths
  (`git rev-parse --git-path <state>` works with linked worktrees). Without an active
  operation, establish unresolved entries' origin before choosing continuation.
- Abort, skip, hook bypass, and discarding changes need authorization.

## Procedure

1. Start with operation/unmerged-path summaries and bounded queries; read relevant
   paths/commits next. Preserve unrelated working and staged changes. Continuation
   must not commit unrelated staging; separate it reversibly or pause.
2. Where present, inspect `git show :1:<path>` (base), `:2:<path>` (current), and
   `:3:<path>` (incoming) with bounded reads. Added/deleted paths may lack stages.
   During rebase, current means upstream plus replayed commits; incoming means
   the replayed feature commit. Never assume ours always means the original feature.
3. Reconcile both intended behaviors and relevant tests/call sites. If requirements
   are mutually exclusive and evidence cannot settle them, ask for that decision
   while preserving the conflict. Removing markers alone is not correctness.
4. Edit only affected paths. Choose rename/delete/binary versions from evidence.
   For generated files or lockfiles, resolve inputs then use the project generator;
   inspect output and preserve dependency intent. Do not blanket-select a side.
5. Stage explicit resolved paths via `git add -- <path>` or `git rm -- <path>`.
   Inspect their cached diff, automatically merged changes, and
   `git diff --cached --check`; ensure no unresolved index entries remain and run
   focused checks. Preserve the resolution on failure; inspect hook edits before retry.
6. For authorized completion, use the matching merge/rebase/cherry-pick
   `--continue`; resolve-only can stop at validated staging. Reinspect each later
   conflict in a replay sequence. Inspect empty commits before any skip decision.
7. Verify status, unmerged entries, resulting behavior/history, ended operation
   when applicable, and preservation of unrelated work.

## Result

Report operation, resolved paths and reconciliation, checks actually run,
staged-only or completed state, and unresolved decisions. No implied push.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
