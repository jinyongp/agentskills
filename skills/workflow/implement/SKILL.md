---
name: implement
description: "Implement requested code changes with explicit completion criteria, proportionate clarification, simple design, and scoped verification. Use for features, fixes, or refactors when source edits are authorized."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Implement

## Scope

Implement the user's requested feature, fix, or refactor when edits are authorized.
Follow current instructions, repository requirements, and existing tool choices.
Planning and read-only review retain their stated scope. Publication, deployment,
and history changes need authorization.

## Think before changing

- Define the observable outcome and completion criteria from the request and actual
  contracts. Inspect relevant code, callers, checks, and local changes first.
- Separate established facts, reversible assumptions, and unresolved choices.
  Ask a focused question only when missing information materially changes behavior,
  data, permissions, compatibility, cost, or an expensive-to-reverse decision.
  Continue independent work while waiting; settle the choice before dependent edits.
- Resolve routine details from repository conventions and evidence. State assumptions
  that affect the result. Surface a simpler viable approach and relevant tradeoffs
  before committing to a consequential design.
- Start with bounded summaries, then selected files or diffs. Use existing tools or
  bounded helpers for repeated inspection. Report omissions and retrieve relevant
  detail before drawing conclusions.

## Choose a simple design

- Use the smallest coherent change that meets the accepted requirements, measured
  by responsibilities and maintenance cost rather than line count.
- Reuse established interfaces and patterns. Introduce an abstraction, dependency,
  configuration option, or extension point only for a concrete current requirement.
  A single-use abstraction can be justified by a real boundary or resource lifecycle.
- Handle reachable failure states and enforce actual contracts at appropriate
  boundaries. Preserve required safety and compatibility; avoid speculative guards.

## Keep edits scoped

- Connect each changed line to the requested outcome or a necessary dependency.
  Match local style and preserve user changes, meaningful comments, and unrelated code.
- Comments explain intent, constraints, or non-obvious behavior. Omit code narration;
  preserve license notices, tool directives, and useful issue or version references.
- Refactor an affected area when needed for the outcome. Keep adjacent cleanup and
  pre-existing dead code outside the patch; mention material discoveries separately.
- Remove imports, variables, and functions made obsolete by this change after checking
  remaining consumers. Keep documentation and configuration aligned where behavior
  actually changes.

## Verify completion

- For multi-step work, order meaningful units and their checks.
- Reuse sufficient tests, lint, types, and schema checks. Add or extend a test only for
  a named uncovered failure or contract, with independently justified expectations
  and stable behavior assertions.
- Reproduce a reported failure when possible and confirm the correction. For a
  behavior-preserving refactor, use relevant before/after evidence when available.
  Run affected checks and required project checks; preserve meaningful protection.
- Investigate failures before changing expectations. Continue scoped fixes until the
  criteria are met. Stop repeated failing attempts when new evidence or access is
  needed; report the actual blocker, skipped checks, and unverified behavior.
- Review the final diff for scope. Report outcomes, actual checks, and material gaps;
  green checks alone do not prove every requirement.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
