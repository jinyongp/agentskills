---
name: test-e2e
description: "Add or revise end-to-end tests for a critical user journey through the actual application or CLI. Verify observable completion with isolated data and bounded execution, without repeating lower-level case matrices."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Test E2E

## Scope

- Verify a critical user journey from an actual application or CLI entrypoint to
  observable completion. Name the system boundary and what remains outside it.
- Use the user's tools and project harness within the requested environment. Keep
  relevant application components real; disclosed external substitutes limit the claim.

## Admission

- Name the user outcome and failure that cheaper existing checks cannot expose.
  Reuse adequate coverage; a feature edit does not automatically need a new E2E case.
- Keep representative journeys and distinct system failures. Do not repeat all unit
  branches, input combinations, or static/schema rules through the whole system.
- Assert behavior, accessibility, and required compatibility. Exact text, attributes,
  snapshots, ordering, or layout need a concrete contract rather than current source.
- Keep setup, dependencies, execution, and upkeep proportional to added confidence.

## Procedure

1. Identify the user, entrypoint, meaningful actions, completion evidence, existing
   checks, and required components. Resolve missing expected behavior before choosing
   assertions; state the intended test environment and unavailable dependencies.
2. Create owned accounts/data/resources or an isolated fixture using project tooling.
   Setup may bypass unrelated journeys, but the behavior under test must follow the
   actual entrypoint and relevant real components. Preserve unrelated data and work.
3. Drive the journey like its user. For UI, prefer semantic roles, accessible names,
   or a stable automation contract over incidental DOM structure and CSS classes.
   For CLI, use the actual command and relevant exit/output or resulting artifacts.
4. Wait for observable readiness/completion with bounded conditions. Avoid fixed sleeps
   and retries that hide failures or repeat unsafe actions. Keep each case independent
   of execution order and prior test state.
5. Verify the user-visible result and consequential state needed by the journey, not
   merely a mocked call or successful HTTP status. Check persistence after reload or
   a new read when required. Retain exact protocol or accessibility constraints where
   meaningful; omit incidental rendering details.
6. For a known defect, confirm the scenario exposes it when the prior faulty state is
   available. Run the selected journey and required checks; distinguish application,
   harness, and infrastructure failures. A substituted component leaves its actual
   integration unverified.
7. Capture native failure evidence when useful: selected logs, trace, screenshot, or
   output artifact. Return a bounded summary first and inspect relevant details only.
   Clean up owned resources; do not broaden the suite to meet test-count targets.

## Result

Report the journey, completion evidence, actual tested environment/components,
substitution limits, executed results and tested state, cleanup, and gaps.
A passing narrow or mocked scenario is not proof of unexercised system behavior.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
