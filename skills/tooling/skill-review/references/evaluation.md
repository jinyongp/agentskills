# Behavioral evidence

Read when planning a behavioral evaluation or assessing claims about activation,
task quality, token savings, or productivity. Reviewing instructions can identify
a supported failure mechanism; it cannot establish that an agent exhibited it.

## Choose a useful case

Ground the expected result in the user contract, project evidence, or independently
justified properties before seeing the candidate output. Use realistic requests:

- A typical task that needs the skill's distinctive guidance.
- A nearby task owned by another workflow, plus a valid alternative that should
  remain possible under the instructions.
- Missing evidence, a failed tool, or a consequential authorization boundary.
- Large input and recoverable omissions when the skill performs inspection.

When evaluating a reviewer, mix planted defects with healthy targets and justified
strict rules. Keep expected findings outside its input; grade supported misses and
false-positive defects separately. Suggestions and honest gaps are not defects.
Do not let reviewing target instructions become executing their workflows.

Choose cases for the suspected decision or uncovered contract. No fixed case count
or mandatory independent run applies to every skill. Reuse sufficient evidence;
run a changed helper against normal, large, and failure inputs when relevant.

## Separate the questions

- **Format/distribution:** Do checks pass and does a standalone install retain
  required resources? This says nothing about task judgment.
- **Instruction review:** Does a written rule plausibly change a decision under
  the stated condition? Label this as parent review, even with concrete examples.
- **Scripted replay:** Does an authored fixture exercise the claimed contract?
  This is not spontaneous agent behavior.
- **Independent execution:** Can another agent complete the realistic task from
  the skill and minimum raw artifacts? Give no intended answer or prior findings
  unless the task itself needs them. Delegate only when available and authorized.
- **Comparative benefit:** Does a suitable with/without-skill comparison support
  improvement? Match tasks, environment, and outcomes; include review/check cost.
  Character counts are not measured tokens or proof of savings.

## Subagent dry runs

Use an independent subagent when behavioral evidence would add useful confidence
and delegation is available and authorized. Do not spawn one for every review.
Start without conversation history containing expected answers. Supply only the
realistic request, the selected skill or discovery context, and necessary raw
artifacts; keep ground truth and prior conclusions outside its input.

Run the workflow on isolated copies. Review-only work remains read-only; workflows
that mutate use explicitly permitted disposable targets or test doubles. Define
allowed effects and stopping conditions before execution. Do not assume a subagent
has filesystem isolation: it may share the parent's workspace and permissions.
Compare file snapshots and observable outputs afterward. If safe execution is
unavailable, return a static rehearsal and label the unexecuted behavior.

Grade required outcomes, unsupported findings, scope, and failure handling against
expectations prepared before the run. Keep actual output and revision evidence.
Reported reads are weaker than captured tool traces; unavailable usage counters
remain unknown. A scripted helper replay and a proposed plan are not independent
agent completion. Record failed attempts rather than silently replacing them.

## Compare quality and cost

Establish the same required outcome before comparing variants. A cheaper run that
misses a finding or breaks scope is not an equivalent-outcome saving. Record loaded
entrypoints/references, successful and failed tool calls, elapsed time, and actual
usage when available. Separate cached and uncached input, output, and reasoning
counts; total input across turns includes reused context. Do not infer billing from
counts without verified pricing, or label returned characters as measured tokens.
Include evaluation/review overhead when claiming net productivity.

For instruction changes, use matched before/after requests and environment; a
with/without-skill comparison addresses the skill's added benefit. Neither a single
pair nor unknown model/context controls establishes causality or general savings.
Report unavailable metrics explicitly; judge correctness before efficiency.

Test selection separately from performance after explicit invocation. Providing
the skill or naming it in a prompt bypasses the discovery question. A model's claim
that it used the skill is weaker than a recorded read and subsequent task evidence.

## Record limits honestly

Use permitted isolated workspaces and avoid production side effects. Record target
revision, request, independent expectation, supplied context, actual output,
checks, failures, and unknown environment/model details. Preserve enough evidence
to reproduce the conclusion without dumping unrelated logs into agent input.
Retain earlier results with their revisions; they do not certify changed content.
Propose an unevaluated case as pending rather than inventing an observed result.
