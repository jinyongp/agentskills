---
name: test-integration
description: "Add or revise integration tests for real dependency boundaries, adapters, persistence, and serialization. Target wiring failures that existing unit or static checks cannot detect."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test Integration

## Scope

- Exercise a real boundary: adapter, persistence, filesystem, protocol, or cooperating
  modules. Name a wiring or semantic failure isolated tests cannot detect.
- Use the user's tools and existing project harness. Work in the requested scope;
  use disposable resources and preserve unrelated code, tests, and data.

## Admission

- Reuse sufficient existing coverage. A change or coverage percentage alone does not
  justify a new integration test.
- Assert the consumer-visible result from an independently justified contract.
  Exact literals, shapes, attributes, ordering, and architecture need a concrete
  compatibility, behavioral, accessibility, or explicit project-policy reason.
- Use existing static/schema validation for declarative constraints. Keep internal
  algorithms and broad input combinations in cheaper checks when those are sufficient.
- Keep setup, dependencies, runtime, and maintenance proportional to the added evidence.

## Procedure

1. Identify producer, consumer, actual boundary, expected result, and existing checks.
   Select a test only when it adds evidence: real serialization, persistence, transaction
   behavior, registration, error propagation, or resource lifecycle. A schema-only check,
   isolated calculation, or full user journey may require a different boundary.
2. Use the smallest representative real integration. Keep the boundary under test real;
   substitute unrelated expensive or unsafe services only when needed. State what a
   substitute cannot prove, including differences in database or network semantics.
3. Create isolated resources with explicit ownership. Use unique data/paths, bounded
   readiness checks, and cleanup of only resources created by this test. Shared services
   need safe isolation; resolve unavailable prerequisites before dependent execution.
4. Trigger the behavior through a stable entrypoint and verify it at the consuming side.
   For persistence, read through the relevant consumer or a fresh connection when that
   is the contract. Mock call counts alone do not prove committed data or valid messages.
5. Cover representative success and distinct boundary failures needed by the risk.
   Keep exact protocol values when required, but omit incidental formatting, internal
   call order, and repeated unit-level branches. A mocked boundary is not evidence
   about the actual dependency.
6. For a reproducible defect, confirm the check detects the prior faulty state when
   available and passes after correction. Run affected and required project checks;
   distinguish missing infrastructure from product failure. Inspect bounded reports
   and selected failure detail; record skipped real integrations accurately.

## Result

Report the protected boundary and failure, added or reused coverage, real versus
substituted dependencies, executed results and tested state, cleanup, and gaps.
If existing coverage is adequate, report reuse without adding a duplicate test.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
