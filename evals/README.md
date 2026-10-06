# Skill evaluations

Evaluate whether instructions produce the intended results separately from format validation.
When adding a skill, record inputs and expected results in `evals/<skill-name>/`.
Keep each skill's cases and results in its own folder.

| Skill | Evaluation record |
| --- | --- |
| responsive | [Content-driven reflow, intentional scrolling, input access, and verification limits](responsive/README.md) |
| ui-design | [Content-driven composition, honest claims, visual judgment, and functioning controls](ui-design/README.md) |
| rewrite | [Factual fidelity, natural voice, compression, and edit scope](rewrite/README.md) |
| implement | [Material ambiguity, simple design, scoped changes, and sufficient checks](implement/README.md) |
| summarize | [Delivery, fidelity, and scope](summarize/README.md) |
| brief | [Delivery, fidelity, and scope](brief/README.md) |
| terse | [Delivery, fidelity, and scope](terse/README.md) |
| clear | [Attention-aware delivery, complete detail, and scope](clear/README.md) |
| git-commit | [Request scope, commit grouping, excluded changes](git-commit/README.md) |
| git-branch | [Branch operations and index/worktree preservation](git-branch/README.md) |
| git-sync | [Remote synchronization, divergence, tags, local work](git-sync/README.md) |
| git-conflict | [Merge, rebase, and cherry-pick conflict procedures](git-conflict/README.md) |
| git-pr | [PR scope, body preparation, and validation limits](git-pr/README.md) |
| handoff | [Missing context, targeted lookups, and work preservation](handoff/README.md) |
| verify | [Bounded execution, log recovery, failures, and timeout handling](verify/README.md) |
| survey | [Read-only directory mapping and bounded manifest discovery](survey/README.md) |
| plan | [Scoped work units, material decisions, and completion evidence](plan/README.md) |
| code-review | [Review scope, bounded comparisons, and reproducible findings](code-review/README.md) |
| debug | [Reproduction, scoped correction, and preserved unrelated work](debug/README.md) |
| git-worktree | [Registry paging, checkout lifecycle, locks, and local data](git-worktree/README.md) |
| benchmark | [Tool selection, matched measurements, noise, and retained raw results](benchmark/README.md) |
| test | [Meaningful coverage, stable contracts, reuse, and maintenance cost](test/README.md) |
| test-integration | [Real boundaries, consumer outcomes, isolation, and coverage reuse](test-integration/README.md) |
| test-maintenance | [Cost evidence, justified assertions, and retained protection](test-maintenance/README.md) |
| test-unit | [Stable logic boundaries, meaningful cases, and isolated state](test-unit/README.md) |
| test-contract | [Consumer expectations, provider conformance, and version scope](test-contract/README.md) |
| test-e2e | [Real entrypoints, observable completion, isolation, and system scope](test-e2e/README.md) |
| test-property | [Justified invariants, generated domains, shrinking, and failure replay](test-property/README.md) |

Cover at least these cases:

- Typical request: the skill applies and produces the requested result.
- Adjacent request: an out-of-scope request does not invoke the skill.
- Missing input or tool failure: request necessary information or explain the failure.
- Input budget: measure default and follow-up output sizes. Verify limits and omission
  reporting with large inputs, and recover required information page by page.

Record the request, expected result, agent and version, and actual result.
For skills with scripts, also verify normal and failure inputs.

## Authoring policy verification

See [saved-records verification](saved-records/README.md) for the shared artifact
location, individual installation, generation, and file preservation checks.

On 2026-10-03, the Git skills were revised to start with summaries and use input budgets.
Repository limits are 300 characters for descriptions and 4,000 for SKILL.md bodies,
separate from the official format limits.
All 40 tests in `uv run check.py test` passed, covering accepted boundary values,
rejected overflows, preservation on generation failure, bounded inspection output,
and information recovery. These results do not measure automatic skill selection
or independent agent judgment.

The five Git skill bodies decreased from 23,042 characters at initial commit `6669a64`
to 12,429 characters, about 46%. This comparison excludes frontmatter and conditional references.
The final `uv run --locked check.py`, individual installation and execution of the inspection
helper, local documentation links, and per-skill MIT notices all passed verification.
