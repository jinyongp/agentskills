---
name: implement
description: "Implement requested code changes with explicit completion criteria, proportionate clarification, simple design, and scoped verification. Use for features, fixes, or refactors when source edits are authorized."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Implement

Implement authorized features, fixes or refactors with current instructions and
project tools. Planning/review keep their scope; publication, deployment, and
history changes need authorization.

## Core rules

- **Preserve accepted behavior.** Complete the usable flow and reachable failure/
  recovery states. Enforce contracts at appropriate boundaries; preserve required
  safety, compatibility, and access. Reduced scope needs agreement.
- **Simple design.** Meet accepted requirements with low maintenance
  cost and readable responsibilities. File count, line count, and diff size alone
  do not establish simplicity.
- **Scoped changes.** Tie edits to the outcome or a necessary dependency. Follow
  local style; preserve user changes, meaningful comments, and unrelated code.

Read [references/design-fit.md](references/design-fit.md) when simplifying a solution,
choosing added structure, or judging whether implementation is complete.

## Think before changing

- **Completion.** Tie each criterion to an observable result and useful evidence.
  Inspect relevant code, callers, checks and local changes. Recover agreed omissions
  and tradeoffs; preserve their limits through implementation and verification.
- **Uncertainty.** Separate facts, reversible assumptions, and unresolved choices.
  Ask a focused question only when missing information materially changes behavior,
  data, permissions, compatibility, cost, or an expensive-to-reverse decision.
  Continue independent work while waiting; settle the choice before dependent edits.
- **Design choices.** Settle routine details from evidence. State material assumptions and
  compare a simpler viable approach before a consequential design choice.
- **Inspection.** Start with bounded summaries, then relevant files/diffs; report omissions and
  recover required detail before concluding.

- **Existing tools.** Check code, standard/platform features and installed tools for fit.
  Add structure or dependencies for a current need or concrete maintenance benefit.
  One caller can justify a boundary or lifecycle abstraction.

## Keep edits scoped

- **Comments.** Explain intent/constraints, not code narration. Preserve license notices,
  tool directives, and useful issue/version references.
- **Cleanup.** Refactor affected code when needed. Keep adjacent cleanup and pre-existing dead
  code outside the patch; report material discoveries separately.
- **Consumers.** Check remaining consumers before removing newly obsolete code.
  Align documentation and configuration with changed behavior.

## Verify completion

- **Cadence.** Order work units/checks; reuse matching evidence for unaffected criteria.
- **Coverage.** Reuse sufficient tests, lint, types, and schema checks. Add or extend a test only for
  a named uncovered failure or contract, with independently justified expectations
  and stable behavior assertions.
- **Behavior.** Reproduce a reported failure when possible and confirm the correction. For a
  behavior-preserving refactor, use relevant before/after evidence when available.
  Run affected checks and required project checks; preserve meaningful protection.
- **Failures.** Investigate against the agreed criteria; changing them is a scope decision,
  not a way to pass. Stop retries without new evidence and report the gap.
- **Final review.** Check missing behavior and excess complexity in the diff.
  Report outcomes, actual checks, and material gaps; green checks alone are insufficient.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
