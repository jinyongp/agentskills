# Skill evaluations

Evaluate whether instructions produce the intended results separately from format validation.
When adding a skill, record inputs and expected results in `evals/<skill-name>/`.
Keep each skill's cases and results in its own folder.

| Skill | Evaluation record |
| --- | --- |
| api-design | [Consumer semantics, compatibility, errors, retries, and protocol scope](api-design/README.md) |
| db-migrate | [Data preservation, engine semantics, mixed versions, interruption, and recovery](db-migrate/README.md) |
| optimize | [Demonstrated costs, correctness, matched measurements, and tradeoffs](optimize/README.md) |
| dependency-update | [Target versions, coupled migrations, resolution failures, and verification](dependency-update/README.md) |
| dev-docs | [Reader tasks, public behavior, examples, version boundaries, and delivery](dev-docs/README.md) |
| english-writing | [English register, modal scope, contextual style, and fidelity](english-writing/README.md) |
| korean-writing | [Korean syntax, register, contextual judgment, and fidelity](korean-writing/README.md) |
| write | [Evidence-based drafting, language routing, and publication scope](write/README.md) |
| mobile-web | [Touch, browser viewport, keyboard access, safe areas, and platform evidence](mobile-web/README.md) |
| ui-library | [Capability fit, project tool precedence, primary evidence, and integration scope](ui-library/README.md) |
| ui-stress | [Realistic content extremes, state boundaries, evidence, and proportionate coverage](ui-stress/README.md) |
| prototype | [Distinct UI alternatives, isolated previews, selection, and scoped promotion](prototype/README.md) |
| animation-performance | [Frame pacing, runtime attribution, matched comparisons, and measurement limits](animation-performance/README.md) |
| animation-debug | [Symptom-directed probes, lifecycle causes, scoped correction, and evidence limits](animation-debug/README.md) |
| animate-native | [Runtime selection, gestures, keyboard coordination, haptics, and platform evidence](animate-native/README.md) |
| animation-vocabulary | [Observable effects, terminology ambiguity, compound motion, and naming scope](animation-vocabulary/README.md) |
| animation-opportunities | [User benefit, instant alternatives, platform coverage, and discovery scope](animation-opportunities/README.md) |
| animation-audit | [Bounded inventory, recoverable omissions, motion evidence, and improvement plans](animation-audit/README.md) |
| animation-review | [Motion defects, continuity, contextual judgment, and runtime coverage](animation-review/README.md) |
| animate | [Web gestures, transitions, interruption, reduced motion, and runtime limits](animate/README.md) |
| accessibility | [Behavioral access, standards applicability, contrast boundaries, and audit limits](accessibility/README.md) |
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
| review-loop | [Whole-scope coverage, accepted tradeoffs, corrections, and termination](review-loop/README.md) |
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

## Iterative changes and independent expectations

See [workflow sequence replay](workflow-sequence/README.md) for an executed parent
trajectory covering planning, corrections that affect unchanged callers, stale
configuration evidence, and a fresh-process handoff. It is not an agent execution.

For skills that alter evolving code, use an iterative evaluation when it exposes a
material gap in single-task evidence. Keep one workspace through realistic requirement
changes; a fixed stage count or mandatory run for every skill adds no assurance.

1. Define initial public behavior, completion criteria and justified expectations
   separately from candidate code. Keep evaluation-only cases outside agent context
   when measuring independent behavior; provide legitimate project checks normally.
2. Perform the initial task, then a meaningful extension or correction against the
   same result. State which contracts remain and which change. Preserve unrelated
   user edits. Do not reset the workspace or silently improve a candidate between stages.
3. At each stage, exercise new requirements and affected preserved behavior. Reuse
   sufficient checks. For a meaningful detection gap, verify that a named faulty
   behavior fails while legitimate alternatives pass; code/test agreement alone is
   insufficient. A different agent/model does not guarantee oracle independence.
4. Inspect accumulated responsibilities, duplication, stale call sites and temporary
   exceptions only where they impose concrete change or operation costs. Added code
   can be required. File counts, length and abstract complexity scores alone do not
   establish design quality; avoid building speculative extension points for the evaluator.
5. Record requests, artifacts, checks, failures and recoveries by stage. Label planned,
   parent-authored replay and independent-agent results separately. Claim comparative
   skill benefit only with an appropriate with/without-skill study; track review effort
   and verification cost as well as generation time when measuring productivity.

Useful prepared sequences include extending catalog lookup while preserving duplicate
and ordering semantics, evolving an API while keeping a supported consumer usable, or
adding migration resume while preserving old reads and user-owned target values.
These sequences are evaluation proposals, not executed trajectories. Existing
[task execution](task-execution/README.md) exercises selected individual outcomes,
not independent iterative quality or causal skill benefit.

Research basis: [SlopCodeBench v2 (2026)](https://arxiv.org/html/2603.24755v2) examines
quality under repeated extensions; [coding-before-testing (2026)](https://arxiv.org/abs/2607.05139)
examines propagated test-oracle errors. Neither establishes that these repository
instructions eliminate the observed problems.

## Authoring policy verification

See [parent task execution and replay](task-execution/README.md) for five executed
local tasks, fixture contracts, actual package/runtime failures, measurements,
database recovery and an API consumer break. This supplements instruction review
and packaging checks; it does not measure independent selection or causal skill benefit.

Five additions on 2026-10-06 bring the collection to 49 skills: dev-docs,
dependency-update, optimize, db-migrate, and api-design. Their evaluation records
separate parent decision-rule review from mechanical verification and the scoped
SQLite rehearsal. Full verification passed with 76 existing tests. Actual installation
of these five names in one command and wildcard installation of all 49 skills with
skills@1.7.0 passed; all bundled files matched byte-for-byte, with no extra selections.

See the [repository-wide context review](context-review/README.md) for the 44-skill snapshot,
their decision boundaries, corrections, mechanical evidence, and unmeasured behavior.

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
