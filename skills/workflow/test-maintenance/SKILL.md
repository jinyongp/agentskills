---
name: test-maintenance
description: "Audit or improve an existing test suite for redundancy, brittle implementation coupling, excessive strictness, flakiness, and cost. Preserve meaningful failure detection when refactoring or pruning tests."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test Maintenance

## Scope

- Audit or improve existing tests in the requested area. An audit returns findings;
  editing or pruning follows the user's maintenance scope. Preserve unrelated work.
- Follow current tooling and project constraints. Optimize useful failure detection
  against setup, runtime, failure-analysis, and change costs; test count is not a target.

## Principles

- Judge a test by its protected failure and contract, not its size, name, age,
  assertion count, or overlap in executed lines.
- Keep independently justified behavior, accessibility, compatibility, and explicit
  project-policy checks. Literal, HTML attribute, JSON shape, snapshot, and architecture
  assertions are incidental only when those details have no required meaning.
- Preserve refactoring freedom. Internal names, call order, file layout, and broad
  output equality should constrain changes only when part of a required contract.
- Retain cross-layer checks when they add evidence, such as actual wiring or persistence.
  Reuse existing static/schema tools rather than rebuilding them in runtime assertions.

## Procedure

1. Establish the requested area and observed cost: recurring harmless breakage,
   slow setup, unstable execution, or redundant coverage. Use existing runner reports
   and a bounded inventory of relevant files/cases; inspect only selected tests and
   callers. For large inventories, report selected/total/omitted counts and page detail.
   Use native tooling or a tested reducer when mechanical output needs reduction.
2. Map each candidate to its input/state, failure mechanism, contract, and assertions.
   Check requirements and actual consumers before classifying a detail as incidental.
   Similar text, covered lines, or passing results alone do not establish duplication.
   Compare the trigger, failed outcome, and real boundary: consolidation fits when
   the retained case detects the same fault under the required conditions. A shared
   assertion across mock and real storage can protect different failures.
3. Choose keep, refactor, consolidate, move to an existing static check, or remove.
   For each reduction, identify the retained check and its covered failure, or explain
   why the asserted constraint is no longer required. Clarify missing contracts before
   changes that could remove needed protection.
4. Apply only authorized changes. Narrow overstrict comparisons to required properties;
   preserve meaningful failure cases. Consolidate shared scenarios without introducing
   a test framework or obscuring distinct behavior. Fix isolation, clock, or readiness
   causes of flakiness rather than masking them with arbitrary sleeps or retry counts.
5. Run affected checks and required project validation. When useful and inexpensive,
   confirm retained checks detect a representative fault in an isolated copy. A green
   reduced suite alone does not prove retained coverage. Compare measured cost only
   when relevant and available; label estimates and unmeasured benefits honestly.
6. Report unresolved gaps and remaining candidates. Stop when the requested area is
   addressed; do not broaden pruning or relax required checks just to reduce counts.

## Result

Give each material candidate's location, problem, contract, disposition, retained
protection, and executed evidence. Include gaps and measured cost changes when available.
Keeping useful tests unchanged is a valid result.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
