---
name: optimize
description: "Improve code performance through demonstrated bottlenecks, scoped changes, correctness checks, and matched before/after measurements. Use for latency, throughput, memory, or resource costs; measurement alone does not authorize optimization."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Optimize

## Scope

Improve the requested code path's latency, throughput, memory, or resource cost.
Follow project tools, supported environments, and required behavior. Diagnosis-only
and measurement-only requests return evidence and proposals. Optimization does not
authorize production load, paid services, deployment, or host-wide tuning.
This skill works alone; accompanying measurement guidance supports the same task.

Read [references/measurement.md](references/measurement.md) when choosing evidence,
interpreting profiles, or comparing results. Read
[references/tradeoffs.md](references/tradeoffs.md) for caching, concurrency, batching,
algorithm changes, or memory/time tradeoffs.

## Procedure

1. Identify the user-visible objective, representative workload, metric/unit,
   correctness contract, baseline state, and relevant limits. Reuse established
   budgets or acceptance criteria; do not invent a universal speedup target.
   Set an investigation/run budget and resolve only consequential missing inputs.
2. Reproduce the cost. Record revisions, uncommitted scope, build/runtime, workload,
   and environment. Match measured boundaries to the question; disclose an unavailable
   baseline before claiming improvement.
3. Attribute the bottleneck with a targeted profile or discriminating experiment:
   algorithmic work, allocations, queries, I/O, scheduling, contention, or rendering.
   Trace only relevant paths. A hot function, large file, or preferred technique is
   not enough; establish its contribution to the objective.
4. Choose the smallest coherent change to the demonstrated cause. Compare benefit
   with complexity, resource cost, and compatibility. Preserve required ordering,
   error semantics, isolation, lifecycle, and output. Changed fidelity, freshness,
   or concurrency semantics need an accepted tradeoff, not silent relaxation.
5. Apply the authorized correction and remove temporary instrumentation. Keep user
   edits and unrelated cleanup intact. Reuse sufficient correctness and integration
   checks; add coverage only for a meaningful new failure or contract gap.
6. Repeat the workload with matched inputs, build, warmup, and environment. Compare
   repeated samples, relevant spread/tails, and resource costs; retain warnings and
   failed runs. A change smaller than observed noise is inconclusive.
7. Retain the change only with supported benefit and preserved requirements, or
   identify it as an unverified candidate when checks are unavailable. Regressions
   need investigation or scoped recovery of owned changes; preserve other work.
   Stop when criteria are met or evidence/access/run budget prevents useful progress.
8. Inspect selected metric summaries and trace intervals first. Report omissions
   and recovery queries; use native filters or a tested bounded reducer for large
   output. Keep full profiles/logs outside default input.

## Result

Report the supported bottleneck, scoped correction or proposal, baseline/candidate
values and units, variability, correctness evidence, resource tradeoffs, and gaps.
Distinguish measured improvement, regression, inconclusive results, and source-only
hypotheses. Link necessary raw evidence and reproduction details without inventing
measurements or generalizing a microbenchmark to untested production workloads.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
