---
name: test-contract
description: "Add or revise compatibility checks between consumers and providers of APIs, messages, or serialized data. Verify independently justified expectations against the provider rather than snapshotting its current output."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test Contract

## Scope

- Verify compatibility between a named consumer and provider of an API, message,
  command output, or serialized data. Identify the interface and relevant versions.
- Use the user's tools and existing contract/schema checks. Stay within requested
  changes and local verification; publishing contracts needs its own authorization.

## Admission

- Name the consumer expectation and uncovered incompatibility. Reuse existing checks;
  current provider output alone is not an independent contract.
- Shape validation belongs to a suitable existing schema tool. Add runtime evidence
  only for missing provider conformance or consumer interpretation.
- Exact field names, values, ordering, and errors are justified when consumers depend
  on them. Match only the documented constraint; allow variation only where permitted.
- Keep fixtures, dependencies, and version combinations proportional to actual support
  obligations. Contract checks do not prove the full deployment or user journey.

## Procedure

1. Find the authoritative agreement: consumer usage, approved interface specification,
   supported version policy, and existing contract fixtures. Resolve conflicts before
   choosing expectations; do not infer requirements by snapshotting all current output.
2. Select representative interactions and distinct compatibility risks: required
   fields, types, units, encoding, absent/null values, error semantics, or evolution.
   Test only relevant supported combinations; avoid an arbitrary Cartesian matrix.
3. Verify that the real consumer can produce or interpret contract-conforming samples.
   For consumer-driven tools, verify recorded expectations against the actual provider.
   A mock that matches its own setup or an unverified generated file is insufficient.
4. Exercise real provider behavior through a stable interface with controlled provider
   state. Isolate owned test data. Record the provider version/revision and exact
   contract/consumer version tested; report unavailable verification as a gap.
5. Use semantic matchers for permitted variability and retain exact constraints where
   necessary. Check additive or breaking changes against actual compatibility rules;
   an extra field is not automatically compatible with every consumer.
6. Confirm a reproducible incompatible state fails when available, then verify the
   corrected state and required project checks. Keep schema checks centralized and
   avoid duplicating internal business branches or complete user flows.
7. Inspect bounded verification summaries and selected mismatch details. Review
   contract updates against changed requirements; do not auto-accept new snapshots
   or broaden matchers solely to make verification pass.

## Result

Report interface, consumer/provider and contract versions, protected incompatibility,
verified interactions, real versus substituted components, executed results, and gaps.
A schema pass or generated contract alone is not verified provider compatibility.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
