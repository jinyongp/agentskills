# proposal evaluation

## Current update: decision and commitment boundaries

- Revision/date: working tree based on `19be008`; 2026-10-28.
- Scope: distinguish the requested decision, proposed success measures, accepted
  requirements, and execution authority. Keep both standalone contract copies at
  revision 2 and add recipient review for unsupported commitments.
- Synthetic case A: a library coordinator asks for a proposal to review late book
  returns, with no implementation or staffing decision authorized. Expected:
  request assessment of reminder options, explain possible reduction in overdue
  items, and retain uncertainty. Do not assign staff, mandate launch, or turn a
  suggested measurement into a recipient completion checklist.
- Synthetic case B: the coordinator explicitly requests a pilot proposal with an
  agreed two-week review period and candidate acceptance checks. Expected: preserve
  that scope and useful checks; do not remove them under a blanket ban on criteria.
  Proposal acceptance alone must not be described as permission to launch the pilot.
- Evidence: parent instruction review against both cases. The entrypoint now asks
  for the recipient's decision, distinguishes goals from duties, and permits detailed
  plans and rollout scope when requested or agreed. The reader pass checks the same
  boundary. This is written-rule review, not independent author execution or proof
  of improved generated proposals. Both case executions remain pending.
- Validation: `uv run check.py validate` passed for 69 skills; index refresh changed
  no files. Entrypoint body: 3,973 characters. Revision-2 contract copies are byte
  identical; Git whitespace checks passed. Initial validation exceeded the body
  limit; prose was tightened and validation rerun. A read-only default uv cache
  required a temporary cache. Shell initialization also reported an fnm state-path
  warning; the final validation command exited successfully.
  No scripts, metadata, catalog entries, or installed skill copies were changed.

## Earlier coverage: recipient context

- Update/date: working tree based on `fa3fa9c`; 2026-10-21. Added a mandatory
  recipient-context pass, conditional reader delegation, and general examples.
- New-case expectation, set before execution: using
  [equipment request notes](cases/equipment-review-notes.md), produce a proposal
  understandable without those notes. Remove or explain the staff nickname and
  omit unrelated move history. Preserve Tuesday review, two business days for a
  decision/status update, same-day urgent escalation, budget/availability limits,
  the four-week approval request, and unmeasured benefits. Do not imply delivery
  guarantees, completed trials, or agreed staffing changes.
- Actual result: an independent author, given the skill and notes without parent
  history or expected conclusions, produced
  [this proposal](results/equipment-review-proposal.md). Parent comparison with
  the prepared expectations found the nickname and move history omitted, with
  material deadlines, exceptions, limits, and the requested decision preserved.
  The author reported reading the reader-review reference, using self-review,
  and checking against notes. These are agent reports, not captured read traces;
  no before-review draft was captured to establish what self-review changed.
- A separate reader received only that proposal, the reader-review reference,
  the intended audience (operations manager familiar with the coordinator role),
  and the approval decision. It reported no consequential ambiguities and limited
  its conclusion to recipient comprehension, without verifying source evidence or
  feasibility. It received no notes, expected findings, or parent history. Neither
  agent edited files, ran project tooling, or contacted external services.
- Checks: 69 skill formats passed; 184 tests completed with one Windows-only skip;
  selective installation/bundled-file checks and packed CLI lifecycle checks passed.
  Index freshness, creator quick validation, and Git whitespace checks passed.
  Initial attempts hit read-only shell/uv/npm caches; writable temporary caches
  allowed checks to complete. A combined `smoke package` invocation was rejected
  by the CLI; those checks then passed as separate invocations.
- Current entrypoint body: 3,895 characters. SHA-256:
  `37f7f04c2151621e3d5be36e73a2bed972b0d607af4235b20c86b2392fd4d495`.
  Reader-review reference SHA-256:
  `242c6a8d41540d4343efbd1012249a30d1cb173d009bc4d5e450e4541ffc0d9e`.
- Environment: Linux/WSL, Codex; exact agent model/build and usage unknown.
  Author self-review and a separate recipient pass were exercised. Automatic
  delegation by an author, technical-case transfer under the revised instructions,
  implicit discovery, and comparative benefit remain untested. Previous runs below
  apply only to their recorded revision. That update clarified the repository-wide
  general-example rule; the subsequent [collection example audit](../instruction-clarity/README.md)
  records coverage of other skills.

## Earlier coverage

- Revision/date: working tree based on `2c41dad2b4ac97e737a6e15c865e02e10d108596`;
  2026-10-21. New original skill and bundled contract revision 1.
- Evidence: parent instruction review, format/distribution checks, and two explicit
  independent author executions. Current output: [proposal](results/proposal.md).
- Open gaps: implicit discovery, nontechnical agent execution, comparative benefit,
  large-source omission recovery, and Windows behavior are not established.

## Cases

### Typical request

- Request: prepare a maintainer proposal from `cases/author-notes.md` and the public
  contract in `../proposal-assessment/cases/tabletext/README.md`. No source code,
  implementation, or submission is authorized for this author run.
- Independent expectation: preserve measured zero versus unmeasured count, its
  consequence, and deliberate blank `None` behavior. Include baseline and available
  reproduction, label the delimiter explanation as a hypothesis, and separate the
  fill-with-zero suggestion from the need. Preserve header localization as excluded.
  Transfer the useful private-incident excerpt without claiming full source access.
- Next stage: a fresh recipient gets only the generated proposal and fixture target,
  without these notes, prior conversation, or evaluator expectations.
- Actual result: the first independent author preserved domain meanings, evidence
  limits, and preservation conditions, but turned an uninvestigated area into an
  unsupported scope boundary. [Initial output](results/initial-proposal.md) retains
  that result. The entrypoint now distinguishes coverage gaps from agreed exclusions.
  A fresh author using the revised skill produced [the current proposal](results/proposal.md),
  preserving other exporters as uninvestigated rather than excluded. Parent review
  found the prepared expectations satisfied. Neither author inspected implementation
  or ran reproduction; their reports and artifacts are the execution evidence.

### Broader process opportunity

- Request: propose scheduled equipment-request review windows while preserving
  urgent requests' existing path; no delay measurements are available.
- Expected result: explain goals, urgent exceptions, and observable success; retain
  missing measurements. Do not demand bug reproduction or claim quantified savings.
- Actual result: written-rule review only; nontechnical execution pending.

### Out-of-scope request

- Request: plan implementation of approved behavior, or resume the same task in
  another session sharing a repository.
- Expected result: those outcomes do not require drafting another proposal.
- Actual result: parent reviewed scope and route alternatives; implicit selection pending.

### Missing input or tool failure

- Condition: an unrecoverable business rule changes the expected behavior, and the
  only reported evidence is a private dashboard.
- Expected result: expose the consequential gap, seek clarification, and use permitted
  excerpts or a named recovery path. Do not invent a rule or claim full transfer.
- Actual result: written-rule review only; runtime failure handling pending.

### Large input and output budget

- No runtime inspector is bundled. Mechanical pagination checks do not apply.
  Bounded source reading and omission recovery remain agent behavior; large-input
  execution is pending.

## Input budget

- Current entrypoint body: 3,913 characters; bundled contract: 3,836 characters.
- The contract loads for technical evidence, access gaps, or cross-team/repository
  transfer. No measured token savings or large-input recovery is claimed.

## Environment

- Date: 2026-10-21; Linux/WSL. Parent: Codex; exact build/model unknown.
- Tools: Python 3.14.8, uv 0.13.3, Node.js 26.10.0, npm 11.19.1.
- Two author subagents started without parent conversation or expected conclusions,
  with explicit installed-skill invocation. Exact model/build and usage counters
  were not reported. The recipient receives no author notes or evaluator expectations.

## Detailed results

- `uv run check.py`: 69 formats passed, 184 tests ran with one Windows-only skip,
  skills@1.7.0 discovery/selective installation passed, and packed CLI project/global
  lifecycle checks passed, including a final run after the instruction correction.
- `uv run check.py validate --check-index`: passed after the correction.
- Creator quick validation passed with transient `uv run --with pyyaml`; an initial
  attempt lacked `yaml`. No project dependency or lockfile was changed.
- Each skill was installed separately into an isolated `/tmp` project through the
  local CLI. All four files matched source bytes; the author's project contained
  proposal and generated index, without proposal-assessment.
- Current SKILL.md SHA-256:
  `6ac042489e48a2e25e34c27fbb9e8cea26ce2c99cc4afe3ee08c2c254a405255`.
  The initial author used `9369ecdf09ba30b2a469ac03438b9f3f428982825dbf924512e2edb06f4e21f7`.
- The contract copies were identical, SHA-256
  `97934f271a459666e4f020c7d9427bb7b16fe118834b04fb65ed02257a52d67a`.
- Format and installation do not prove task judgment. This explicit single-case
  correction and recheck do not establish implicit discovery or comparative benefit.
