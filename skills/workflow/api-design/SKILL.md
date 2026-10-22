---
name: api-design
description: "Design or review API contracts with resource-oriented HTTP defaults and concrete rules for methods, status codes, validation, retries, and compatibility. Also supports RPC, SDK, and message contracts while preserving their protocols."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Api Design

Design, revise, or review a consumer-facing HTTP, RPC, SDK,
or message contract.

## Core rules

- **Preserve the contract.** Keep chosen protocols, tools, supported consumers,
  and project conventions. Default new HTTP APIs to resource-oriented design;
  preserve established contracts. Recover agreed scope/omissions and resolve
  unclear intent before adding semantics or recovery flows.
- **Consumer compatibility.** Evaluate changes against supported versions
  and actual consumers. Additive fields or optional parameters can break strict
  decoders, generated clients, exhaustive handling, or defaults. Choose compatible
  evolution, explicit version transition, or scoped migration from actual policy.
- **Match the request.** Design returns a contract/proposal; review returns findings.
  Implementation, publication, and live client/server changes need task scope.

For HTTP, apply [references/http.md](references/http.md); distinguish protocol
constraints from design defaults.
Read [references/compatibility.md](references/compatibility.md) for evolution,
serialization, defaults, versions, or consumer migration. Read
[references/operations.md](references/operations.md) for errors, authorization,
retries, concurrency, pagination, asynchronous work, or protocol semantics.

## Define and verify

1. **Baseline.** Establish consumer task, current interface, outcomes, versions,
   and contracts. Inspect callers, specifications, examples, and tests.
   Separate usage, promises, and assumptions.
2. **Operations.** Define only needed concepts and operations. Prefer existing
   interface patterns and schema tools over a new protocol or framework. Choose names
   and boundaries from consumer meaning rather than internal database layout.
   Resolve consequential unknowns; settle routine naming directly.
3. **Values and effects.** Specify inputs, outputs, units/encoding, required/optional values, defaults,
   absence/null semantics, side effects, and observable state changes. Identify who
   can act on which resources. Cover relevant success, invalid input, authorization,
   conflict, unavailable dependency, and partial-completion outcomes.
4. **Failure and recovery.** Define operation-specific error meaning, retry
   eligibility, duplicate requests, uncertain outcomes, concurrency, cancellation,
   and ordering where required. Add pagination, batch, streaming, or asynchronous
   semantics only when the task needs them. Keep resource limits explicit and
   grounded in requirements; do not invent fixed counts or reliability guarantees.
5. **Conformance.** Verify with representative independent examples and existing
   schema/generation/consumer checks. When implementation is authorized, inspect and
   exercise actual provider behavior; a mock or schema pass alone does not prove
   conformance. Reuse sufficient coverage; add tests for meaningful compatibility gaps.
6. **Coverage.** Keep changes and conclusions within inspected scope. Begin with operation/
   consumer summaries; retrieve relevant detail with omission counts and recovery queries.
   Keep full schemas/clients out of default input; verify reducer limits/failures.

## Result

Return contract/findings, rationale, compatibility impact, examples, checks, and
unresolved assumptions. Distinguish designed, implemented, generated,
and provider-verified behavior. Preserve uncertainty and requested language; report
unavailable consumers/environments without claiming complete compatibility.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
