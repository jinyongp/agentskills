# Attribution and matched measurement

Read when selecting metrics, interpreting a profile, or evaluating a candidate.

## Attribution is not a benchmark

Use the project's supported profiler and a workload that reproduces the relevant
cost. Sampling, tracing, allocation instrumentation, and full-call profiling have
different overhead and visibility. Profile totals can hide short critical stalls;
inspect the interval or request that matters to the user.

The [Python profiler documentation](https://docs.python.org/3/library/profile.html)
explicitly distinguishes profiling from benchmarking and describes overhead bias.
The general decision is to attribute cost with suitable instrumentation, then compare
representative execution separately where instrumentation changes the question.
This reference does not require Python or a particular profiler.

## Compare the actual objective

Match workload, output requirements, concurrency, environment, build mode, cache
state, and startup/warmup policy. Alternate or randomize candidate order when supported;
avoid unintended competing load. Consume results so measured work actually happens.
Retain raw samples and invalid-run warnings; inspect odd values before dropping them.

Use suitable estimates and variability for the metric. Throughput, elapsed time,
tail latency, allocations, retained memory, and peak process usage are different
quantities. Declare the measured boundary and units. An allocation reduction is
not automatically reduced resident memory, and more throughput can worsen latency.

Use an established practical threshold when gating; statistical significance alone
does not establish usefulness. Label relative-change direction and formula, and
handle a zero baseline without division. Mixed workloads or small improvements amid
noise require qualified conclusions, not a universal percentage target.

Missing devices, services, traces, or permissions leave specific evidence gaps.
A local fixture can guide investigation without proving production performance.
Preserve useful native exports and link selected evidence instead of pasting full traces.
