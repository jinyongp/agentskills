# proposal-assessment evaluation

## Current update: assessment scope and proposed targets

- Revision/date: working tree based on `19be008`; 2026-10-28. Shared contract
  revision 2 came from the preceding proposal update; this update changes the
  assessment entrypoint, catalog, and selection route.
- Independent expectations for synthetic cases:
  1. A library coordinator requests only a judgment on overdue-book reminders.
     Assess need, evidence, and alternatives; do not require a work plan, launch,
     staffing assignment, or recipient completion checklist.
  2. The proposal demands a 90% reduction within one week without measurements.
     Assess the target's basis and feasibility; do not silently adopt it as a
     requirement or promise a result. Preserve established privacy constraints.
  3. The coordinator requests both assessment and a pilot plan with an agreed
     two-week review period. Include useful ordering and checks within that scope;
     keep launch authority and staffing commitments separate from recommendation.
- Evidence: parent written-rule review. The default result is a justified decision;
  detailed planning is conditional, proposed targets are evaluated, and operational
  risks remain assessable without assigning execution duties. Explicitly requested
  planning remains supported. These cases have not been executed by an independent
  agent; no comparative behavior improvement is claimed.
- Validation: `uv run check.py validate --check-index` passed for 69 skills;
  `test_skill_index.py` passed all 13 tests. Generated route/catalog pages were
  refreshed and reviewed, including catalog repagination. Entrypoint body: 3,970
  characters; the revision-2 contract copies remain byte identical. Git whitespace
  checks passed. Initial format checks exceeded the body budget; wording was
  tightened and checks rerun. A temporary uv cache avoids the read-only default;
  fnm initialization still warns about its state path, but final checks exit zero.

## Earlier coverage

- Revision/date: working tree based on `2c41dad2b4ac97e737a6e15c865e02e10d108596`;
  2026-10-21. New original skill and bundled contract revision 1.
- Evidence: parent instruction review, format/distribution checks, and explicit
  independent recipient execution. Output: [assessment](results/assessment.md).
- Open gaps: implicit discovery, nontechnical agent execution, comparative benefit,
  large-source omission recovery, and Windows behavior are not established.

## Cases

### Typical request

- Request: assess the author run's proposal against `cases/tabletext/`, inspect and
  run safe local checks, and return an assessment and plan without source edits.
- Input: received proposal, fixture documentation, and source only. Author notes,
  prior conversation, and evaluator expectations are withheld.
- Independent contract: `None` exports as blank; every other value uses its string
  representation. CSV/TSV share the rule. Quoting and header behavior are accepted.
- Expected result: reproduce zero loss, distinguish its cause from a delimiter
  guess, trace shared conversion to TSV, and consider `False`. Preserve intentional
  `None` and empty-string behavior. Reject filling every blank with zero while
  supporting the underlying need. Keep localization excluded, provide evidence,
  and propose scoped work with meaningful checks. No source or external writes.
- Actual result: the fresh recipient reproduced the CSV loss, found TSV's shared
  cause, checked `False` and other falsy values, and preserved blank `None`/empty
  strings. It separated reported business consequences from locally verified code
  behavior and proposed the shared correction with preservation checks and a scoped
  plan. No implementation was changed. Parent review found prepared expectations
  satisfied. The recipient first read the initial proposal, then received the revised
  proposal as a normal input update and based its final output on that revision.
  It received neither author notes nor evaluator expectations.

### Valid alternative and accepted restriction

- Condition: a proposal requests a visible `None` placeholder although blank output
  is deliberate and consumers depend on it.
- Expected result: distinguish an extension from a defect; preserve the accepted
  rule and consider opt-in or consumer alternatives without inventing obligations.
- Actual result: written-rule review only; execution pending.

### Out-of-scope request

- Request: implement an accepted fix, or audit the whole repository.
- Expected result: assessment alone does not own implementation or imply a broad
  audit. Related work follows causes, rules, and consumers; optional work stays separate.
- Actual result: parent reviewed scope and route alternatives; implicit selection pending.

### Missing input or tool failure

- Condition: the reported environment is unavailable and a current-version check
  does not reproduce the failure.
- Expected result: report checked state, unresolved environment differences, and
  next evidence. Do not declare the report false or invent a confirmed fix.
- Actual result: written-rule review only; runtime failure handling pending.

### Large input and output budget

- No runtime inspector is bundled. Mechanical pagination checks do not apply.
  Large-source reading, omission recovery, and exhaustive search behavior are untested.

## Input budget

- Current entrypoint body: 3,933 characters; bundled contract: 3,836 characters.
- The contract loads for technical evidence, access gaps, or cross-team/repository
  transfer. No measured token savings or large-input recovery is claimed.

## Environment

- Date: 2026-10-21; Linux/WSL. Parent: Codex; exact build/model unknown.
- Parent tools: Python 3.14.8, uv 0.13.3, Node.js 26.10.0, npm 11.19.1.
- Recipient: a Codex subagent without parent conversation; explicit installed-skill
  invocation. It reported Python 3.15.0 for local checks; exact model/build and usage
  counters were not reported. No claim covers every supported Python version.

## Detailed results

- Final `uv run check.py`: 69 formats passed, 184 tests ran with one Windows-only
  skip, skills@1.7.0 discovery/selective installation passed, and packed CLI
  project/global lifecycle checks passed. No existing check code was changed.
- `uv run check.py validate --check-index` and creator quick validation passed.
  Creator validation used transient `--with pyyaml` after an initial missing-`yaml`
  failure; no project dependency or lockfile changed.
- The local CLI installed this skill and generated index into an isolated `/tmp`
  project, without proposal. All four installed skill files matched source bytes.
- SKILL.md SHA-256:
  `ea71a063beb0a396e8d5068996fba05bdd90b7acbea8989a967997716c7d495d`.
  The identical contract copies have SHA-256
  `97934f271a459666e4f020c7d9427bb7b16fe118834b04fb65ed02257a52d67a`.
- The recipient reported seven documented conversion mismatches per exporter,
  successful baseline quoting/header/order/iterable/empty-input checks, and a
  printable-object truthiness boundary. The artifact records checked inputs,
  commands, results, limitations, and unchanged target hashes. No candidate was tested.
- This single explicit recipient execution supports the observed handoff and
  investigation only. It does not establish implicit discovery, broad audit
  completeness, comparative benefit, or nontechnical execution quality.
