---
name: accessibility
description: "Implement or review web accessibility in a scoped interface: semantics, keyboard operation, focus, perceivable states, contrast, and enlargement. Use for accessibility work with behavioral evidence and explicit coverage limits."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Accessibility

## Scope

Implement or review accessibility in the selected web interface. Follow the user's
target standard and repository requirements; otherwise use WCAG 2.2 AA as a review
baseline, not a claim of certification. Review-only requests return findings.
Read [references/criteria.md](references/criteria.md) when measuring contrast,
enlargement, reflow, or target size, or resolving a criterion or widget-pattern question.

## Procedure

1. Identify affected user journeys, components, states, and supported environments.
   Inspect selected markup and rendered behavior, beginning with bounded summaries.
   Track omissions and retrieve relevant detail; partial coverage remains partial.
2. Prefer native elements and established accessible components. Give controls
   meaningful accessible names and accurate roles, values, and states. Preserve
   heading, landmark, form-label, error, and table relationships. Add ARIA only for
   an actual semantic need; an attribute alone does not prove accessibility.
3. Exercise required actions by keyboard: logical focus order, activation, visible
   focus, and entry/exit of composite widgets. Manage focus for dialogs and changed
   content according to the interaction pattern, including restoration where useful.
   Prevent traps and keep focused controls visible. Programmatic focus targets and
   roving tabindex can be valid; judge behavior rather than attribute presence.
4. Make errors, progress, and relevant status changes perceivable without relying
   on color alone. Associate actionable errors with their controls. Announce dynamic
   information appropriately; avoid noisy live announcements for every render.
   Supply useful text alternatives for meaningful media; decorative media may be silent.
5. Measure applicable contrast against actual rendered colors, backgrounds, and
   states. Account for opacity, images, gradients, themes, and exceptions. Use an
   established checker; classify with unrounded values and report what was measured.
   A flat color pair does not establish contrast across a changing image background.
6. Verify text enlargement and reflow, interaction target access, and relevant
   forced-colors or reduced-motion behavior. Check actual loss of information or
   operation; distinguish minimum criteria from optional usability recommendations.
7. Run available project accessibility checks and relevant manual checks. For custom
   semantics or dynamic announcements, verify with the accessibility tree and supported
   assistive technology when available. Automated scans and source inspection leave
   behavioral gaps; report unavailable tools rather than implying a complete audit.

## Result

For each finding, identify the element/state, affected user action, supporting
evidence, and applicable criterion when established. Separate defects from optional
improvements. For authorized changes, use sufficient existing validation; add tests
only for meaningful uncovered behavior, preserving legitimate implementation choices.
Report scope, environments, checks, unresolved issues, and untested interactions.
A clean scan or screenshot alone is not evidence of full WCAG conformance.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
