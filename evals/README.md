# Evaluate a skill

Check whether instructions support the intended decisions and outcomes. Format and
installation checks establish different evidence from an actual agent completing a task.

## Record a task

1. State the request, intended result, and an expectation grounded independently of
   the candidate output. Record the skill revision, date, agent/model, and tool versions
   when known; preserve unknown values explicitly.
2. Exercise the case within its authorized environment. For scripts, check normal
   and failure inputs. Keep expected and observed results separate.
3. Record pass/fail or pending status, issues, corrections, and remaining gaps.
   An instruction review is evidence about written rules; label it accordingly.

Cover the cases relevant to the skill:

- **Typical request:** the skill applies and produces the requested result.
- **Adjacent request:** an out-of-scope request does not invoke the skill.
- **Missing input or tool failure:** necessary input is requested or the failure explained.
- **Input budget:** measure default and follow-up output; exercise large inputs,
  omission reporting, paging, and recovery where inspection tools are involved.

Use the generated `evals/<skill-name>/README.md` to record these cases and results.

## Make current coverage findable

Start each record with the evaluated revision, evidence obtained, and open gaps.
Separate environment, executed checks, and untested behavior into short labeled items.
Keep earlier results in dated sections or a linked history; an older pass applies
only to its recorded code, configuration, and environment.

Distinguish the evidence you obtained:

- **Format/distribution:** structure, dependencies, packaging, and installed bytes.
- **Instruction review:** a parent checks the written decision rules.
- **Scripted replay:** an authored fixture exercises a declared behavior.
- **Independent execution:** another agent performs the task from the supplied inputs.
- **Comparative benefit:** an appropriate with/without-skill study supports a causal claim.

## Find evaluation records

- [Skill records by category](index.md)
- [Workflow sequence replay](workflow-sequence/README.md)
- [Authored task execution](task-execution/README.md)
- [Repository context review](context-review/README.md)
- [Instruction clarity review](instruction-clarity/README.md)
- [Saved-record convention checks](saved-records/README.md)

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

[Historical authoring-policy checks](history/authoring-policy.md) retain their
original dates, tested revisions, results, attribution, and limitations.
