# Optimization tradeoffs

Read only the section matching a candidate mechanism. These are decision questions,
not instructions to apply every technique.

## Algorithms and repeated work

Use actual input scale and operations to justify an algorithm or data structure.
Check ordering, duplicates, precision, overflow, and failure behavior where relevant.
Precomputation or indexing shifts cost to construction and maintenance; include that
cost when it is part of the workload. A tiny isolated win may not affect the end task.

## Caching and memory

Define ownership, keys, freshness, invalidation, eviction, and resource bounds from
the required contract. Account for tenant/user separation and concurrent updates.
Caching must not silently expose another user's result, hide errors, or preserve
invalid state. Treat retained memory and warm/cold behavior as distinct evidence.
A TTL is a product consistency choice, not a substitute for an invalidation policy.

## Concurrency and batching

Choose concurrency from the workload and resource limits. Preserve cancellation,
timeouts, backpressure, ordering, transaction boundaries, and required failure
semantics. More workers can increase contention or tail latency. Batching can save
per-item cost while delaying completion; measure the effect on the actual objective.

## Database and I/O

Trace query/request counts and wait intervals before changing indexes or combining
calls. Keep transaction isolation, locks, retry semantics, connection ownership,
and compatibility in scope. A plan estimate is not an observed execution result.
Confirm the selected inspection tool's side effects before running it against live
data; an execution-analysis command may actually execute its query.

## Resource and semantic changes

Compression, reduced precision, pagination, approximate results, and fewer retries
can change observable behavior. Establish an accepted tradeoff rather than relaxing
correctness to satisfy a performance target. Dependency or architecture changes need
a demonstrated capability gap and proportional migration cost.
