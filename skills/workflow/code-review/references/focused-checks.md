# Focused behavior checks

Use when the user requests a limited boundary, failure, state, or dependency review.
Keep the selected checks and coverage explicit; a clean targeted pass is not a
complete review of an otherwise uninspected change.

- Follow accepted inputs into their consumers. Check parsing, validation, ownership,
  and meaningful limits where the changed path relies on them. A missing local
  validator is not a defect if the actual trusted boundary enforces the contract.
- Trace fallible operations through recovery. Account for global handlers, queue
  retry semantics, and caller-visible failure outcomes. Flag a lost outcome or
  unsupported recovery assumption, not every absent local catch statement.
- Verify external interfaces against the receiver, installed version, and actual
  registration/dispatch. Inheritance, generated code, and dynamic extensions can
  supply a method; a failed text search alone cannot prove it is nonexistent.
- Trace durable mutations into dependent readers, concurrent writers, and async
  consumers. Establish the violated invariant and trigger before claiming data
  loss or demanding a new transaction/recovery mechanism.
- Check referenced symbols, configuration, routes, assets, and services in their
  effective context. Distinguish missing requirements from inactive optional paths
  and incomplete environment evidence.

For a finding, establish the introduced expectation violation and code evidence.
Keep hypotheses separate when runtime dispatch or environment cannot be verified.
Reuse appropriate existing static/runtime checks instead of replacing uncertainty
with a fabricated conclusion or a new requirement.
