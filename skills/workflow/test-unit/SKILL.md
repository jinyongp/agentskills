---
name: test-unit
description: "Add or revise focused tests for calculations, decisions, and state transitions at a stable boundary. Target meaningful logic failures without coupling tests to internal structure or real infrastructure."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test Unit

## Scope

- Test calculations, decisions, and state transitions through a stable interface in
  the requested scope. A unit may include cooperating helpers; one test per function
  or class is not a requirement.
- Use the user's tools and existing project harness. Preserve unrelated work.
  Real service wiring and full user journeys need other evidence.

## Admission

- Name the uncovered failure and independently justified expected behavior.
  Reuse existing coverage; a code change or coverage quota alone does not justify a test.
- Prefer existing type, lint, or schema checks for declarative constraints. Runtime
  validation of external inputs still needs evidence when static checks cannot prove it.
- Exact values, attributes, shapes, ordering, and structural rules constrain tests
  only when required by behavior, accessibility, compatibility, or explicit policy.
- Keep setup, dependencies, runtime, and future edits proportional to added confidence.

## Procedure

1. Identify the stable input/output or state contract, existing cases, and missing
   failure mechanism. Ask only when missing requirements prevent a valid expectation.
2. Choose representative cases and meaningful boundaries. Extend a suitable existing
   test instead of creating a separate fixture for every edit. Parameterize similar
   scenarios when it improves clarity; retain distinguishable failure reports.
3. Exercise behavior without asserting helper names, internal object layout, or an
   algorithm choice. Derive expectations from requirements or checked examples,
   rather than duplicating production calculations or copying current output.
4. Use real lightweight collaborators when practical. Substitute time, randomness,
   I/O, or expensive dependencies only as needed; state unverified real semantics.
   Check returned results or observable state. Call counts/order need their own
   required interaction contract.
5. For a reproducible defect, show that the check detects the prior faulty state when
   available and passes after correction. Make cases independent of execution order
   and shared mutable fixtures. A passing mock does not prove the actual dependency.
6. Run affected and required project checks. Inspect bounded reports and relevant
   failure detail. Distinguish setup failures from behavioral failures; report gaps
   rather than expanding the suite to reach an arbitrary percentage.

## Result

State the protected behavior and failure, reused or changed checks, substitution
limits, executed results and tested state, and remaining gaps. No new test is a
valid result when existing checks are sufficient.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
