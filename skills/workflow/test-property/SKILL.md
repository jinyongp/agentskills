---
name: test-property
description: "Design property-based checks for justified invariants across generated inputs or state transitions. Choose a meaningful domain, preserve failure reproduction, and control cost without weakening required behavior."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test Property

## Scope

- Check independently justified invariants over generated inputs or state transitions.
  This is an input/assertion technique usable at unit or integration boundaries.
- Use the user's tools and existing property framework when suitable. Choose the
  smallest stable boundary that exposes the risk; preserve unrelated work.

## Admission

- Name the invariant, valid input domain, and failure mechanism missed by adequate
  existing examples or static checks. Generation alone is not additional confidence.
- Derive the property from requirements or independent reasoning. Round trips,
  idempotence, or equivalent implementations need a real contract; two components
  sharing the same wrong assumption can agree and still violate it.
- Exact values, shapes, ordering, or architecture constraints need a concrete contract.
  Reuse static/schema validation for declarative constraints.
- Keep generation, setup, execution, and future maintenance proportional to the added
  evidence. A property need not be asserted again at every system layer.

## Procedure

1. Identify the meaningful domain, permitted states, invariant, expected rejection
   behavior, and existing coverage. Resolve an unknown contract before inventing a law.
   Choose properties that distinguish plausible bad implementations from valid ones.
2. Generate the domain directly, including relevant boundaries and relationships
   between fields. Separate valid and intentionally invalid cases when their contracts
   differ. Avoid excessive filtering or exclusions that discard the defect-triggering
   region merely to obtain a passing or faster test.
3. Exercise a stable interface and assert the required invariant, not current internal
   layout or a reimplementation of the production algorithm. Control nondeterminism
   and reset owned state between cases; generation must not leak live side effects.
4. Use native search and shrinking when supported. Set a run/time budget using framework
   controls; report limits that restrict the explored domain. Prefer reducing execution
   budget over silently weakening the required input domain. Passing sampled cases is
   evidence, not a proof over all possible inputs.
5. Capture the smallest reported failing input and replay information: relevant state,
   framework/runtime versions, and native replay token or seed when applicable.
   A seed alone is not necessarily portable across versions. Confirm reproduction
   without depending on the local example cache or previous cases.
6. Confirm a known faulty behavior violates the property when available, then verify
   correction and affected project checks. Retain a minimized example when it protects
   a useful regression, preferably in existing coverage rather than a duplicate suite.
7. Inspect bounded native summaries first; fetch only relevant counterexample/shrink
   detail. Keep original failure evidence in a saved record when needed. Explain setup
   failures, unstable reproduction, omitted domains, and remaining uncertainty.

## Result

Report invariant and domain, justification, tested boundary, generation budget,
executed results, counterexample and replay method if any, and exploration gaps.
Do not equate sample counts with completeness or require a new framework by default.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
