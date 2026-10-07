---
name: close
description: "Assess completion and commit readiness from existing scope, validation evidence and worktree changes. Use for requested closeout; report gaps without starting new implementation or checks."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Close

## Scope

- Assess whether the requested work can be called complete or ready to commit.
  Recover the current contract, accepted limits and required completion evidence.
- Closeout inspects existing evidence. It starts no new implementation, test run,
  review cycle or task mutation. Explicit additional requests retain their own
  authorization; report gaps instead of treating closeout as that authorization.
- Use available plans, records and relevant worktree summaries; work outside Git
  can still be assessed. Do not require a new plan or report file to finish.

## Procedure

1. Match delivered behavior to the agreed completion criteria. Separate completed
   work, explicitly accepted deferrals and unresolved items. An accepted manual
   step or supported subset is not a missing feature. Unknown intent stays unknown.
2. Inspect required check results and their tested code, configuration and execution
   conditions. Reuse results while affected inputs still match; unrelated later
   edits do not invalidate them. Missing, stale, failed or blocked required evidence
   prevents an unqualified completion claim. A scheduled check is not a result.
3. Distinguish a check adding no useful signal (not-needed) from an unavailable
   required check (blocked). Preserve exact commands, prerequisites and affected
   criteria for unresolved checks; identify the next action without executing it.
4. If Git applies, start with a bounded status/diff summary using existing project
   tooling. Inspect only candidate changes needed to assess scope. Account for
   staged, unstaged and untracked work; avoid dumping diffs or secret contents.
   Unrelated edits need preservation and explicit exclusion, not cleanup.
5. Assess commit readiness separately from task completion. Pending commits can
   coexist with completed implementation. Candidate changes need clear scope and
   relevant required evidence; mixed work is ready only with a reviewed selection.
   Explicit acceptance of a validation gap permits qualified readiness, not a claim
   that the check passed. Closeout alone stages, commits and publishes nothing.

## Result

Give completion status, validation evidence/gaps, relevant worktree scope and commit
readiness when applicable. Include only material residual risks and the next actual
action. Link existing records; no duplicate checklist or new quality work is needed.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
