---
name: test
description: "Assess coverage needs, suggest test cases, or design and implement behavior checks within the requested scope. Reuse existing coverage and static validation before adding tests."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test

## Scope

- Design, add, or revise automated tests in the requested scope. Reuse user-selected
  tools and repository conventions; preserve unrelated code, tests, and configuration.
- Assess lasting coverage before adding it. Running existing checks alone does not
  require new test code. Test pruning follows the requested maintenance scope.
- Choose coverage here when the boundary is unclear. Integration work exercises real
  dependencies; suite maintenance assesses existing tests and their ongoing cost.

Read [references/case-ideas.md](references/case-ideas.md) for test-idea requests
or uncovered-case discovery. Ideas-only scope creates and executes no tests.

## Principles

- Protect an agreed contract and named failure. Preserve deliberate scope limits;
  ground expectations in requirements or independent examples, not current output. Read
  [references/oracles.md](references/oracles.md) for coupled code/test generation
  or uncertain expectations.
- Reuse existing coverage first. Add a regression case only for a meaningful gap;
  a change, commit, or coverage target alone is not a reason to add a test.
- Test through the smallest stable boundary that can expose the failure. Preserve
  freedom to rename helpers, reorganize files, or replace algorithms without changing
  tests when the protected behavior remains equivalent.
- Assert only contract-relevant details. Exact literals, static HTML attributes,
  JSON shapes, ordering, snapshots, and architecture rules need a concrete behavioral,
  accessibility, compatibility, or explicit project-policy reason.
- Use existing lint, type, schema, or architecture checks for mechanical rules;
  runtime tests cover semantics/integration they cannot establish. Do not duplicate
  validators with ad hoc assertions.
- Choose cases by distinct failure mechanisms and meaningful boundaries. Repeat
  coverage across layers only for additional evidence, such as real wiring or
  serialization. Avoid exhaustive combinations without a supported risk.
- Keep setup, dependencies, mocks, and runtime proportional to the confidence gained.
  Prefer outcomes over incidental call counts/order. Isolate nondeterminism; use
  interaction assertions when the interaction itself is a required contract.
- Investigate failures before revising expectations. Update changed contracts or
  remove incidental constraints while retaining coverage of the intended behavior.

## Procedure

1. Identify the failure, justified expectation, existing coverage, and useful static
   checks. Resolve missing requirements; current output alone is not an oracle.
2. Choose: reuse, extend an existing test, add a test, use a static check, perform
   one-off validation, or add nothing. Explain the material coverage gap and cost
   briefly; an adequate existing check is a valid stopping point.
3. Implement only the selected in-scope change. For a reproducible defect, confirm
   the chosen check detects it and passes after correction when the prior faulty
   state is available. A check that never detects its target needs investigation.
4. Run affected checks and required repository validation. Distinguish test failures
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
