---
name: test
description: "Assess coverage needs, suggest test cases, or design and implement behavior checks within the requested scope. Reuse existing coverage and static validation before adding tests."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test

Design, add, or revise automated tests within the requested scope.

## Core rules

- **Independent expectations.** Protect an agreed contract and named failure. Preserve scope limits;
  ground expectations in requirements or independent examples, not current output. Read
  [references/oracles.md](references/oracles.md) for coupled code/test generation
  or uncertain expectations.
- **Coverage before additions.** Reuse existing checks. Add a regression only for a meaningful gap;
  a change, commit, or coverage target alone is not a reason to add a test.
- **Stable boundary.** Use the smallest boundary exposing the failure. Preserve
  freedom to rename helpers, reorganize files, or replace algorithms without changing
  tests when the protected behavior remains equivalent.
- **Relevant assertions.** Exact literals, static HTML attributes,
  JSON shapes, ordering, snapshots, and architecture rules need a concrete behavioral,
  accessibility, compatibility, or explicit project-policy reason.
- **Static checks.** Reuse lint, type, schema, or architecture checks for mechanical rules;
  runtime tests cover semantics/integration they cannot establish. Do not duplicate
  validators with ad hoc assertions.
- **Distinct failures.** Choose cases by mechanism and meaningful boundaries. Repeat
  coverage across layers only for additional evidence, such as real wiring or
  serialization. Avoid exhaustive combinations without a supported risk.
- **Proportionate cost.** Keep setup, dependencies, mocks, and runtime proportional to confidence.
  Prefer outcomes over incidental call counts/order. Isolate nondeterminism; use
  interaction assertions when the interaction itself is a required contract.
- **Failures before expectations.** Investigate before revising assertions. Update changed contracts or
  remove incidental constraints while retaining coverage of the intended behavior.

Use user-selected tools and repository conventions; preserve unrelated code/tests/
configuration. Assess lasting coverage before adding it; running checks alone needs
no new tests. Pruning follows maintenance scope. Use this skill when the boundary
is unclear; integration exercises real dependencies, maintenance assesses suite cost.

Read [references/case-ideas.md](references/case-ideas.md) for test-idea requests
or uncovered-case discovery. Ideas-only scope creates and executes no tests.

## Choose and verify coverage

1. **Need.** Identify failure, justified expectation, existing coverage, and useful static
   checks. Resolve missing requirements; current output alone is not an oracle.
2. **Decision.** Choose reuse, extension, a new test, static check,
   one-off validation, or no addition. Explain the coverage gap and cost
   briefly; an adequate existing check is a valid stopping point.
3. **Implementation.** Make only the selected change. For a reproducible defect, confirm
   the chosen check detects it and passes after correction when the prior faulty
   state is available. A check that never detects its target needs investigation.
4. **Validation.** Run affected checks and repository validation. Distinguish test failures
   from setup failures; state unexecuted checks and limits. Read bounded summaries
   first and only relevant failure detail afterward.

## Result

Report the decision, protected contract/failure, changed tests or reused checks,
actual results/state, and gaps. Counts or coverage alone do not establish confidence.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
