---
name: api-design
description: "Design or review API contracts with resource-oriented HTTP defaults and concrete rules for methods, status codes, validation, retries, and compatibility. Also supports RPC, SDK, and message contracts while preserving their protocols."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Api Design

## Scope

Design, revise, or review the requested consumer-facing interface: HTTP, RPC, SDK,
or message contract. Preserve chosen protocols, tooling, supported consumers, and
project conventions. Design-only returns a contract/proposal; review-only returns
findings. Implementation, publication, and live client/server changes need task scope.
Default new HTTP APIs to resource-oriented design; preserve established contracts.
Recover agreed scope and omissions; resolve unclear intent before adding semantics
or recovery flows.

Read [references/http.md](references/http.md) for HTTP design or review. Apply its
rules; distinguish protocol constraints from design defaults.
Read [references/compatibility.md](references/compatibility.md) for evolution,
serialization, defaults, versions, or consumer migration. Read
[references/operations.md](references/operations.md) for errors, authorization,
retries, concurrency, pagination, asynchronous work, or protocol semantics.

## Procedure

1. Establish the consumer task, current interface, outcomes, supported versions,
   and contracts. Inspect relevant callers, specifications, examples, and tests.
   Separate usage, promises, and assumptions.
2. Define only the operations and concepts needed for the task. Prefer existing
   interface patterns and schema tools over a new protocol or framework. Choose names
   and boundaries from consumer meaning rather than internal database layout.
   Resolve consequential unknowns; settle routine naming directly.
3. Specify inputs, outputs, units/encoding, required and optional values, defaults,
   absence/null semantics, side effects, and observable state changes. Identify who
   can act on which resources. Cover relevant success, invalid input, authorization,
   conflict, unavailable dependency, and partial-completion outcomes.
4. Define operation-specific failure and recovery behavior: error meaning, retry
   eligibility, duplicate requests, uncertain outcomes, concurrency, cancellation,
   and ordering where required. Add pagination, batch, streaming, or asynchronous
   semantics only when the task needs them. Keep resource limits explicit and
   grounded in requirements; do not invent fixed counts or reliability guarantees.
5. Evaluate the change against real consumer behavior and supported versions.
   Additive fields or optional parameters can still break strict decoders, generated
   clients, exhaustive handling, or changed defaults. Choose compatible evolution,
   an explicit version transition, or a scoped migration from actual policy.
6. Verify the contract with representative independent examples and existing
   schema/generation/consumer checks. When implementation is authorized, inspect and
   exercise actual provider behavior; a mock or schema pass alone does not prove
   conformance. Reuse sufficient coverage; add tests for meaningful compatibility gaps.
7. Keep changes and conclusions within inspected scope. Begin with selected operation/
   consumer summaries; retrieve relevant detail with omission counts and recovery queries.
   Keep full schemas/clients outside default input; verify reducer limits and failures.

## Result

Return the contract or supported findings, rationale, compatibility impact, examples,
checks, and unresolved assumptions. Distinguish designed, implemented, generated,
and provider-verified behavior. Preserve uncertainty and requested language; report
unavailable consumers/environments without claiming complete compatibility.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
