# Skill evaluations

Evaluate whether instructions produce the intended results separately from format validation.
When adding a skill, record inputs and expected results in `evals/<skill-name>/`.
Keep each skill's cases and results in its own folder.

| Skill | Evaluation record |
| --- | --- |
| retro | [Observed workflow failures, existing controls, scope and proportional improvements](retro/README.md) |
| domain-modeling | [Business terms, scenario probes, contextual rules and scoped records](domain-modeling/README.md) |
| ci-fix | [Revision-specific CI, stable Actions, gates and bounded log recovery](ci-fix/README.md) |
| security-review | [Attacker control, authorization, defenses, evidence and coverage](security-review/README.md) |
| research | [Primary evidence, version conflicts, inference, coverage and research scope](research/README.md) |
| close | [Completion evidence, accepted deferrals, work scope and commit readiness](close/README.md) |
| queue | [Queue scope, grouping, registration, duplicates and partial outcomes](queue/README.md) |
| api-design | [Consumer semantics, compatibility, errors, retries, and protocol scope](api-design/README.md) |
| db-migrate | [Data preservation, engine semantics, mixed versions, interruption, and recovery](db-migrate/README.md) |
| optimize | [Demonstrated costs, correctness, matched measurements, and tradeoffs](optimize/README.md) |
| dependency-update | [Target versions, coupled migrations, resolution failures, and verification](dependency-update/README.md) |
| dev-docs | [Reader tasks, public behavior, examples, version boundaries, and delivery](dev-docs/README.md) |
| readme | [Package consumer setup, first-use evidence, release identity, and scoped review](readme/README.md) |
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

### Agent instruction writing — 2026-10-13

#### Revision verification

Added domain-modeling and retro; reinforced plan, queue, prototype, write, rewrite,
dev-docs, debug, code-review and git-pr. Authoring guidance lives in CONTRIBUTING.md.
All documentation and evaluation cases are English. Matt Pocock adaptations pin
commit `49dd158d1076134a641b33efb035946536778336`; standalone skills retain their
own upstream license and attribution outside runtime instructions. The maintainer
guide's attribution/license is in the root NOTICE.md.

Actual `uv run --locked check.py` passed: 58 skill formats/catalogs, 133 tests,
and skills@1.7.0 fixture discovery/selective installation. Local runtime-reference
links, saved-record fragments, copyright notices and body limits passed for all
11 added/changed skills. Bodies range from 3,159 to 3,982 characters.

An actual npm tarball was installed through npx into an isolated temporary project
for Codex and Claude. All files of the 11 selected skills matched source bytes;
Codex read the shared project directory and Claude linked to the same content.
Tarball checks found all selected resources and no Python caches. Actual
skills@1.7.0 installation of domain-modeling, retro and prototype also matched
every source file and installed no unselected skills. The first package replay
used an incorrect expected Codex project path; the harness was corrected to the
declared `.agents/skills` destination and rerun successfully, without source edits.

These checks establish format and distribution, not independent agent behavior
or comparative skill benefit. Decision cases are parent instruction reviews.
No package publication, personal installation, or live tracker/PR operation was run.

#### Authoring decisions

Parent instruction review in Codex; model version not exposed. The authoring
guide now defines reading conditions, co-located decisions, observable completion,
repository lookups and evidence-based pruning. No independent authoring run or
causal improvement was measured.

| Case | Expected decision |
| --- | --- |
| UI-only reference and logic-only reference | Load the branch relevant to the actual question, not both by default |
| Rule and its exception appear in distant sections | Co-locate them and state their resulting action |
| Current command/version is cheap to retrieve | Point to its source instead of maintaining a prompt copy |
| A standalone skill needs a safety boundary | Retain it locally even when maintainers share a canonical fragment |
| One session did not exercise a constraint | Non-use does not establish redundancy; evaluate relevant cases before pruning |
| A coined term supposedly improves agent behavior | Treat the benefit as unverified until realistic execution supports it |

### Research, security and CI additions — 2026-10-07

Attribution layout was corrected afterward: upstream provenance and license notices
now live in the affected skills' NOTICE.md files, including the pre-existing Git
commit reference. Task references retain their useful technical source links.
The existing implement notice was extended without replacing earlier attribution.
Format/catalog validation and actual tarball/selected-skill installation passed;
the complete resource comparisons included the new notice files.

Added research, security-review and ci-fix; reinforced review-loop feedback handling,
plan/implement structural decisions, and dependency-update supply-chain checks.
Guidance is independently written with source links; upstream scripts and
OWASP-derived reference text are not bundled. Existing original MIT log-runner code
is included inside ci-fix so individual installation retains its runtime.

Full verification passed: 55 skill formats/catalog entries and 131 tests, including
the bounded log execution suite applied to the CI helper. Actual npm tarball help
and full-catalog installation passed with all bundled resources compared byte-for-byte.
Actual skills@1.7.0 selective installation of the three new skills and standalone
execution of the installed CI helper passed. Creator validation of all three skills
and local Markdown-link checks for all seven changed skills passed.

Body lengths excluding frontmatter: research 2,964; security-review 3,229;
ci-fix 3,668; review-loop 3,977; plan 3,534; implement 3,967;
dependency-update 3,988 characters. New references load only for stated conditions.

Decision cases are parent instruction reviews. Mechanical results do not establish
independent agent selection, security coverage, live CI repair, research synthesis
quality, or comparative skill benefit. No npm publication or personal installation
was performed for these additions.

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
