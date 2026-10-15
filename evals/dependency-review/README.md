# dependency-review evaluation

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

- Request: Review an added dependency and a direct dependency whose resolved version changes only in the lockfile.
- Independent expectation: Inspect both declarations and resolution changes, consumers and relevant compatibility/maintenance/advisory facts; give scoped recommendations without installing packages.
- Evidence: Parent review confirmed maintenance/popularity distinctions, version-specific advice, and review-only authorization. Scripted fixtures verified lock-only change visibility, not real package resolution or advisory accuracy.

### Adjacent request

- Request: Upgrade the selected framework to the requested version and migrate its callers.
- Expected boundary: Use an update workflow; adoption advice does not perform the requested migration.
- Parent review: scope and index summaries distinguish these tasks. Actual implicit
  activation by a fresh agent was not measured.

### Missing evidence or failure

- Request/condition: An advisory source is unavailable, or only the previous version is known to be affected.
- Expected response: Keep the lookup gap explicit and evaluate candidate/previous versions separately. No unqualified safe verdict follows from missing information.
- Parent review checked this written rule; runtime judgment remains untested.

### Large input and output budget

The bundled change inspector executes from an isolated directory containing only its copied script. Four test methods cover each of the four new inspector bundles: pinned lock-only comparisons, index/worktree separation without mutation, complete recovery of 120 Unicode/space paths through bounded pages, and failed-reference handling.

The new inspectors reuse this repository's existing MIT change inspector. Its
broader regression suite also covers merge-base semantics, exact diff recovery,
and disabled external diff/hooks. Those are mechanical inspection results, not
evidence that an agent produced a correct specification, map, trace, or checklist.

## Input budget

- SKILL.md body: 3307 characters; entrypoints remain below 4,000.
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
