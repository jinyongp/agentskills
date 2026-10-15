# trace evaluation

## Current coverage

- Revision/date: Uncommitted changes based on 4d972c2103595674f2d84d7552da861b9a66e4b0; 2026-10-15.
- Evidence: parent instruction review, format/distribution checks.
- All 65 skills passed format/catalog validation. Full verification completed 160
  tests with one Windows-only skip, skills CLI smoke checks, and package checks.
- The packed CLI installed all six new workflows and four enriched skills alongside
  survey/index for Codex and Claude in isolated project/global scopes. Every bundled
  file was compared with its source and each entrypoint reference resolved locally.
- Not established: independent agent selection, task-quality improvement, token
  savings, or Windows runtime behavior for this change.

## Cases

### Typical request

- Request: Explain what happens when a user removes an item: trace the actual caller, ownership guard, durable effects, and response.
- Independent expectation: Follow the real entry point and relevant call/data edges, cite source lines, preserve consequential branches, and distinguish static evidence from runtime state.
- Evidence: Parent review confirmed caller evidence, vendor/convention uncertainty, exact paths, and limited scope. No independent end-to-end tracing run was performed.

### Adjacent request

- Request: Fix an intermittent removal failure and verify the correction.
- Expected boundary: Use diagnosis/fix guidance; an explanation alone does not satisfy the requested repair.
- Parent review: scope and index summaries distinguish these tasks. Actual implicit
  activation by a fresh agent was not measured.

### Missing evidence or failure

- Request/condition: A handler exists but no trigger or framework registration is visible in the inspected scope.
- Expected response: Report searched scope and unresolved dispatch; explain a hypothetical execution separately without claiming proven unreachability.
- Parent review checked this written rule; runtime judgment remains untested.

### Large input and output budget

No runtime inspection script is bundled. Targeted source/document reading remains agent behavior; no automated parser or agent input-budget measurement was performed.

The new inspectors reuse this repository's existing MIT change inspector. Its
broader regression suite also covers merge-base semantics, exact diff recovery,
and disabled external diff/hooks. Those are mechanical inspection results, not
evidence that an agent produced a correct specification, map, trace, or checklist.

## Input budget

- SKILL.md body: 2635 characters; entrypoints remain below 4,000.
- Conditional references: none.
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
