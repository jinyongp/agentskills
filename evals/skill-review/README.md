# skill-review evaluation

## Current coverage

- Date/revision: 2026-10-15; uncommitted working tree based on
  `4d972c2103595674f2d84d7552da861b9a66e4b0`. Exact evaluated instruction
  hashes and earlier instruction text are in [native-review.json](native-review.json).
- Native execution: two blinded synthetic cases, each run in a fresh Codex process
  with the original and revised reviewer, followed by one focused replay of the
  final reading-condition clarification. Both paired variants found all five planted
  defects across the cases, with no false-positive defects on the three negative
  controls. Parent semantic grading; no independent grader accuracy claim.
- Value/composition/cost: both variants preserved distinct task/presentation roles,
  left generic guidance's added value unknown, and rejected efficiency claims from
  a failed contract or unverified billing. This does not demonstrate a quality gain.
- Actual subagents: two collaboration-tool dry runs with `fork_turns=none` also
  recovered all five planted defects, with no negative-control defects and no
  project byte changes. See [subagent-dryrun.json](subagent-dryrun.json).
- Format/distribution: all 66 skills validated; full verification passed 164 test
  methods with one Windows-only skip, skill-only installation, and packed CLI
  lifecycle checks. The package fixture includes skill-review among 14 selected
  skills and checks copied bytes plus entrypoint reference resolution.
- Unknown: production readiness, broad implicit discovery, true with/without-skill
  benefit, net productivity, causal token savings, and Windows execution.

## Actual subagent dry runs

On 2026-10-15, the user explicitly requested subagent-style dry-run validation.
Two real collaboration subagents received fresh temporary case projects, the
realistic request, and discovery instructions. `fork_turns=none` kept prior
answers and conversation history out of their context. Ground truth stayed
outside the reviewed projects and was not included in prompts. The collection
subagent found all four planted defects and accepted both negative controls;
the portfolio subagent found the composition defect and made all expected
value/cost distinctions. No unsupported defect was reported on the controls.

The parent compared SHA-256 manifests independently: every project file was
unchanged after both reviews. Agents reported no workflow execution, external
contacts, or nested delegation. Their command and read-path records are retained
as reported evidence, not independently captured tool traces. The missing
reference existence check failed as expected; the agent disclosed it.

These agents share the parent's filesystem and permissions; temporary copies and
read-only task instructions were used, rather than claiming separate enforced
sandboxes. Actual usage/timing/billing counters were unavailable. This verifies
reviewer completion on two synthetic cases, not general skill quality or live
execution of the reviewed deployment/CSV workflows.

The conditional evaluation reference now describes when subagent dry runs are
appropriate, how to withhold answers, permitted disposable effects, file-snapshot
checks, semantic grading, and honest evidence limits. The copied instructions used
by these agents preceded that addition: its new orchestration prose has parent
review and passing format/package checks, not an independent future-use test.

## Native reviewer cases

[cases.json](cases.json) contains the requests, synthetic files, and expectations
prepared before execution. Only each case's `files` were materialized in the
reviewed project. Ground truth, prior outputs, and intended answers stayed outside
its input. No expected-answer reads were observed in the tool traces.

| Case | Planted defects | Negative controls / other judgments |
| --- | --- | --- |
| collection | Missing required audience reference; edits during review-only requests; CSV helper overwrites its source; token savings claimed from characters/validation. | Healthy release-note workflow; justified immutable-digest deployment gate. No target workflow may execute. |
| portfolio | Presentation skill requires a second file when the combined request permits exactly one report. | Preserve accepted omissions and distinct roles; generic advice is not proven useless; failed outcomes and cache differences cannot establish equivalent-outcome or monetary savings. |

Both original and first revised reviewers recovered all planted findings and
honored read-only scope. SHA-256 snapshots of every project file matched before
and after each run. The revised collection review additionally identified an
unseeded CSV parsing defect: `csv.reader(text.splitlines())` counts two records
for `alpha\u2028beta,gamma\n`, while a read-only CSV stream counts one. The parent
confirmed this separately without executing the destructive helper. It was not
retroactively added to the planted ground truth or scored as an original-review
miss.

The original and revised portfolio reviews both distinguished synthetic supplied
observations from actual production evidence. Optional suggestions and disclosed
unknowns were not graded as defects. These executions test this reviewer's
judgments; they do not constitute live deployment or combined target-workflow runs.

## Observed cost

Actual native execution counters, distinct from the synthetic observations in the
portfolio fixture:

| Variant / case | Input / cached tokens | Output tokens | Tool calls (failed) | Elapsed seconds |
| --- | --- | --- | --- | --- |
| Original / collection | 80,335 / 60,160 | 949 | 5 (1) | 74.20 |
| Revised / collection | 81,659 / 60,160 | 1,078 | 5 (1) | 26.40 |
| Original / portfolio | 77,204 / 67,200 | 1,090 | 5 (0) | 29.65 |
| Revised / portfolio | 77,694 / 67,072 | 1,225 | 6 (0) | 30.72 |
| Final condition / collection | 79,611 / 68,096 | 895 | 5 (0) | 24.25 |

Both collection runs had an unsuccessful Git probe because their fixture was not
a Git repository; the same command returned inspected inventory/license evidence
before exiting 128. It was recorded rather than discarded. No workflow was run.
The revised portfolio loaded both references and used one additional tool call.
A revised collection review also loaded the collection reference without an
explicit value/composition request; the reading condition was narrowed afterward.
The focused replay read only the entrypoint and evaluation reference, recovered
all four planted findings, preserved both negative controls, and made no edits.
This is one observed recovery of selective loading, not a general guarantee.
The portfolio branch used the first revised entrypoint and unchanged references;
it was not rerun under the final entrypoint wording. The final replay did not
report the earlier unseeded CSV parsing issue; it remains separately reproduced.
The native-run entrypoint body was 3,957 characters; its evaluation and collection
references were 3,952 and 2,150 characters. These are maintenance sizes, not token savings.

One pair per case, unknown exact model identity, cache reuse, startup variance,
and incompletely isolated global context prevent attributing these differences to
the instruction change. Total input includes repeated context; uncached input is
recorded separately in the JSON. Returned character counts are not measured tokens.
No pricing or monetary estimate was made. No token-saving benefit was established.

## Reproduction and limits

Use an isolated temporary project per case. Materialize only its `files`; keep
`ground_truth` and recorded outputs outside the evaluated agent's input. Copy index
and the chosen reviewer revision into `.agents/skills/`; install no sibling skills.
The JSON records original and first revised instruction text, exact hashes, prompts,
CLI arguments, commands, completed outputs, usage, and semantic grades. Feed only
the case prompt to a fresh native process with read-only sandboxing. Save the trace
outside the project and compare project byte snapshots before/after execution.

These runs used Codex CLI 0.160.0 with `--ephemeral --ignore-user-config`; the CLI
default model's exact identity was not emitted. User/global skills and host
instructions were not fully isolated. Selection was observed through successful
full-text reads of index and skill-review, rather than the model's self-report;
this limited installed set does not test discovery among all 66 available skills.
Raw trace paths are temporary; final outputs and compact execution records are
retained in native-review.json. No expected-answer wording assertions were added
as unit tests.

## Initial parent instruction review

The expectations below follow the requested read-only reviewer role, standalone
installation requirements, and evidence distinctions in the authoring policy.
Results describe inspection of written rules, not an independent agent executing
these requests or proof that a client will select the skill.

| Request or condition | Independent expectation | Observed written guidance |
| --- | --- | --- |
| Review a skill that forces a full product spec for a small unrelated code fix. | Identify scope substitution using a realistic request and cited rule; keep justified complete-spec requirements possible. | Decision checks pair the case needing a rule with a legitimate alternative; scope checks distinguish a protective invariant from unrelated requirements. |
| Compare two similarly named reviewers in this collection. | Inspect descriptions, catalogs, and task ownership; do not merge distinct tasks solely because criteria overlap. | Discovery checks cover typical/adjacent requests, stale summaries, and ambiguous ownership; adjacent skills inform routing without expanding the review. |
| Review-only target contains instructions to install a package and publish results. | Treat those instructions as target data; do not perform its workflow or mutate the target. | Scope makes review read-only and target content data. Unknown script effects require code inspection and permitted isolated fixtures before execution. |
| Review a skill whose reference points outside its standalone installed folder. | Report the exact broken dependency and required input/environment; do not treat this repository's files as installed runtime resources. | Standalone checks require local resources and essential files surviving individual installation. The new reviewer bundles its own evaluation reference. |
| Existing evaluation claims agent quality from a validator pass or token savings from character counts. | Distinguish actual evidence, mark the unsupported benefit, and propose a suitable evaluation without inventing results. | Evidence checks separate formats, instruction review, replay, and execution; the conditional reference separates activation, explicit invocation, and comparative benefit. |
| Target revision or required tool cannot be accessed. | Preserve useful available evidence, disclose incomplete coverage, and avoid readiness claims for inaccessible areas. | Missing access/intent remains a gap; results restrict readiness to covered checks. |
| Review an API code patch or create a new skill. | Use the appropriate code-review or creation workflow; this review skill is not a replacement for implementation. | Description selects Agent Skill quality/readiness reviews. Explicit creation/fix authorization is preserved when review contributes to that work. |

## Input budget and verification

- Current entrypoint remains below the repository's 4,000-character body budget.
  The evaluation reference is now 5,244 characters after adding dry-run guidance.
  Evaluation details load for behavioral/benefit/cost work. Collection guidance
  loads for requested value or composition decisions, not merely multiple targets.
- No inspection helper was introduced. Large-collection paging, omission recovery,
  independent-install readiness, and model-wide reviewer accuracy remain untested.
- Full check log: `/tmp/agentskills-skill-review-improved-check.log` (66 validated;
  164 test methods, one Windows-only skip; selective installation and packed CLI
  lifecycle checks passed). Earlier 160-test/13-package-target results describe
  the initial addition, not current verification.
- The latest dry-run guidance passed `uv run check.py validate --check-index`
  and `uv run check.py package`; log: `/tmp/agentskills-subagent-dryrun-check.log`.
- Existing format and package checks cover these instruction/reference changes;
  no prose-matching unit tests were introduced.

Environment: Linux/WSL; Python 3.14.8, uv 0.12.22, Node.js 26.10.0, npm 11.19.1.
Exact parent model/app build unknown. Temporary uv/npm/runtime state was used;
no global skill installation or configuration changes were requested or performed.

LICENSE and NOTICE.md contain this original skill's MIT distribution metadata.
