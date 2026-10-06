---
name: ui-stress
description: "Exercise a selected interface with realistic content extremes, missing data, localization, and state boundaries. Use to find UI failures beyond demo data; reuse fixtures and previews without requiring permanent tests for every finding."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Ui Stress

## Scope

Exercise a selected web or native UI with realistic content and state boundaries.
This is UI resilience inspection, not a service load test or visual redesign.
Review requests return findings; corrections follow the user's authorized scope.

Map only relevant rendered fields, sources, consumer contracts, and local fixtures.
Use existing stories, previews, mocks, or data boundaries. Read the matching section
of [references/cases.md](references/cases.md) when selecting stress inputs.

## Exercise meaningful cases

- Choose plausible values and supported contract limits: long and short labels,
  missing optional fields, counts near meaningful boundaries, and supported locales.
  A limit not found is unknown; it is not proof that the product accepts arbitrary
  input. Invalid values belong in error-path checks when that boundary can receive them.
- Include relevant empty, single-item, loading, failure, partial, permission, and
  collection-boundary states. Vary cases independently when combinations would hide
  the cause. Use synthetic data and reserved example domains; preserve real records.
- Feed cases through the existing data boundary rather than editing markup to force
  a break. An existing story or fixture may suffice; a new toggle/harness is optional.
  Keep disposable controls outside shipped behavior. Do not call live mutating APIs
  merely to populate a fixture.
- Render at actual container widths and affected narrow/wide ranges. Exercise text
  enlargement, supported themes/locales, and relevant input methods. Inspect clipped
  required text, unreachable actions, ambiguous formatting, fallback behavior, and
  loss of information. Intentional scrolling or truncation can be correct if the
  required information and task remain accessible.
- Distinguish a plausible hypothesis from an observed failure. Record the smallest
  reproduction, affected element/state, user effect, and suggested correction.
  Runtime access limits the conclusion; source inspection is not rendered verification.

## Fix, coverage, and report

Apply corrections when authorized; otherwise return findings and design choices.
Preserve product decisions about wrapping, truncation, precision, and fallback content.
Replay the original case and affected adjacent states after a fix.

Reuse existing coverage and previews. Add a permanent test only for a stable,
meaningful uncovered behavior whose protection justifies its maintenance cost.
A one-off inspection does not need a matching snapshot, literal, or CSS assertion.
Remove temporary wiring created for the run unless retention is requested;
preserve shared project fixtures.

Report inspected surfaces/cases, observed defects, recommendations or fixes, checks,
and remaining gaps. Keep output to selected findings and exact fixture/preview paths.
For large surfaces, use selected fields and states, disclose omitted areas, and recover
relevant paged evidence before claiming comprehensive coverage.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
