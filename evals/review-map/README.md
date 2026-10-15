# review-map evaluation

## Current coverage

- Revision/date: Uncommitted changes based on 4d972c2103595674f2d84d7552da861b9a66e4b0; 2026-10-15.
- Evidence: parent instruction review, format/distribution checks, and scripted inspection tests.
- All 65 skills passed format/catalog validation. Full verification completed 160
  tests with one Windows-only skip, skills CLI smoke checks, and package checks.
- The packed CLI installed all six new workflows and four enriched skills alongside
  survey/index for Codex and Claude in isolated project/global scopes. Every bundled
  file was compared with its source and each entrypoint reference resolved locally.
- Not established: independent agent selection, task-quality improvement, token
  savings, or Windows runtime behavior for this change.

## Cases

### Typical request

- Request: Prepare a human reading map for changes spanning permissions, notification delivery, tests, and a lockfile. Do not report defects.
- Independent expectation: Group by behavior, describe priority based on changed consequences, retain relevant generated/lock content, and link a useful reading sequence without a correctness verdict.
- Evidence: Parent review confirmed descriptive scope and evidence-based priority. The bundled standalone inspector passed pinned comparison, paging, layer, and failure tests; map quality itself was not independently exercised.

### Adjacent request

- Request: Find and fix defects in this branch.
- Expected boundary: Use a review/fix workflow; a descriptive map alone is insufficient.
- Parent review: scope and index summaries distinguish these tasks. Actual implicit
  activation by a fresh agent was not measured.

### Missing evidence or failure

- Request/condition: The base branch is unknown or the specified comparison reference does not exist.
- Expected response: Establish the intended target or report failure. Do not assume main or interpret a failed comparison as an empty diff.
- Parent review checked this written rule; runtime judgment remains untested.

### Large input and output budget

The bundled change inspector executes from an isolated directory containing only its copied script. Four test methods cover each of the four new inspector bundles: pinned lock-only comparisons, index/worktree separation without mutation, complete recovery of 120 Unicode/space paths through bounded pages, and failed-reference handling.

The new inspectors reuse this repository's existing MIT change inspector. Its
broader regression suite also covers merge-base semantics, exact diff recovery,
and disabled external diff/hooks. Those are mechanical inspection results, not
evidence that an agent produced a correct specification, map, trace, or checklist.

## Input budget

- SKILL.md body: 2767 characters; entrypoints remain below 4,000.
- Conditional references: {'references/change-inspection.md': 1518}.
- Inspector responses, when used: at most 4,000 characters including JSON escaping
  and newline. Counts, offsets, and explicit continuation support recovery.
- Index catalogs are generated automatically, contain all 65 entries, and split
  at 2,500 characters. Character counts are not measured token counts.

## Environment and commands

- Linux/WSL; Python 3.14.8, uv 0.12.22, Node.js 26.10.0, npm 11.19.1.
- Evaluator: Codex parent session; exact app build/model version unknown.
- `uv run check.py`: passed using a writable temporary npm/uv cache.
- `uv run python -m unittest discover -s tests -p test_workflow_inspectors.py -v`:
  four methods passed across four standalone helper bundles.
- `git diff --check`: passed.

## Provenance

These are original requirements-based instructions. The public Unlearn overview
informed task-role selection; unlicensed upstream skill text/templates/resources
were not copied. LICENSE and NOTICE.md are bundled distribution metadata.
