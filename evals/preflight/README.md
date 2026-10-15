# preflight evaluation

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

- Request: Identify rollout work for a new queued payload and configuration key while old workers may remain active.
- Independent expectation: Inspect deployment ownership, distinguish pre-activation prerequisites from rollout/post-rollout work, account for version coexistence, and avoid claiming a new key is absent without environment evidence.
- Evidence: Parent review confirmed timing, automation ownership, recovery limitations, and execution boundaries. Scripted comparison inspection passed; no deployment or independent operational review was performed.

### Adjacent request

- Request: Apply a specified migration to an identified staging database.
- Expected boundary: Use the authorized migration workflow; a release-preparation list alone does not apply the migration.
- Parent review: scope and index summaries distinguish these tasks. Actual implicit
  activation by a fresh agent was not measured.

### Missing evidence or failure

- Request/condition: The target environment, current worker version, or externally managed configuration is unknown.
- Expected response: Give supported candidate actions and verification gaps; do not issue an unconditional ready verdict or perform live operations.
- Parent review checked this written rule; runtime judgment remains untested.

### Large input and output budget

The bundled change inspector executes from an isolated directory containing only its copied script. Four test methods cover each of the four new inspector bundles: pinned lock-only comparisons, index/worktree separation without mutation, complete recovery of 120 Unicode/space paths through bounded pages, and failed-reference handling.

The new inspectors reuse this repository's existing MIT change inspector. Its
broader regression suite also covers merge-base semantics, exact diff recovery,
and disabled external diff/hooks. Those are mechanical inspection results, not
evidence that an agent produced a correct specification, map, trace, or checklist.

## Input budget

- SKILL.md body: 3002 characters; entrypoints remain below 4,000.
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
