---
name: benchmark
description: "Measure code performance and compare a baseline with a candidate using matched workloads, suitable tools, repeated samples, and preserved raw results."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Benchmark

## Scope

- Measure code latency, throughput, or memory; compare implementations or revisions.
  Agent quality evaluation and correctness-only checks have different criteria.
- Follow current user instructions and repository requirements when selecting tools.
  Prefer a suitable existing harness. Explain missing capabilities before substituting
  a tool; use its supported version and measurement method.
- Benchmarking does not authorize optimization, production load, paid services, or
  host-wide tuning. Preserve unrelated work and existing result files.

## Procedure

1. Define the question, baseline and candidate, representative workload, metric/unit,
   and direction of improvement. Resolve missing inputs that change the comparison;
   choose routine harness details from the project. Set a run/time budget and stopping
   condition. Use an existing acceptance threshold or agree on one before gating.
2. Confirm both versions produce equivalent required results. Identify exact revisions
   and relevant uncommitted changes. Record commands, tool/runtime versions, build
   settings, hardware, workload parameters, concurrency, and measured boundaries in
   the result artifact; link existing sources for recoverable details.
3. Match inputs, environment, and build mode. Account for setup, startup, caches,
   JIT, and warmup according to the question: cold-start costs belong in a cold-start
   measurement. Ensure timed work executes and its result is consumed. Keep harness
   overhead outside the timed region unless measuring the whole command.
4. Use the chosen tool's calibration and repeated sampling. Run competing versions
   without unintended concurrent load; alternate or randomize order when supported.
   Keep raw samples and warnings in fresh result files. A failed, partial, or timed-out
   run is not a valid sample. Avoid deleting outliers merely to improve the result.
5. Compare matched metrics using the tool's analysis. Report sample count, central
   estimate and spread or uncertainty. Label percent change with its direction and
   formula; a zero baseline has no defined relative change. Preserve instability
   warnings. A single run or small difference amid noise is inconclusive. Statistical
   significance, when supported, does not establish practical benefit.
6. Measure memory with a supported memory method and state whether it measures peak
   process usage, allocations, or retained memory. Keep intrusive instrumentation and
   profiling separate from representative timing unless the question includes them.
7. Start with a selected-metric summary and raw-result locations. Use native filters
   and aggregate views rather than loading full logs or samples. For a large suite,
   report selected/total/omitted case counts and fetch relevant cases in bounded pages.
   If native output cannot be bounded, use a deterministic reducer with explicit
   limits, omission counts, and recoverable detail; test large inputs and failures.
   Read official documentation only when the selected tool's flags or semantics need
   confirmation. Stop at the run budget and state remaining uncertainty.

## Result

Return the comparison scope, tool, workload, baseline/candidate values and units,
change, variability, conclusion, and artifact paths. Distinguish improvement,
regression, and inconclusive results. Limit claims to the measured environment and
workload; list skipped metrics and comparison gaps.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
