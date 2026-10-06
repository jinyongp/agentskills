---
name: ui-design
description: "Create, revise, or review interface composition using actual content, user tasks, and product identity. Use for layout, visual hierarchy, components, and meaningful UI states while respecting the requested edit scope."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Ui Design

## Scope

Create, revise, or review the requested interface using its real tasks, content,
and product identity. Reuse existing components and design conventions. A review
returns recommendations; requested edits authorize only the named scope.
Resolve consequential missing direction from evidence or a focused question.

## Design decisions

- Establish the user's primary action and information needs before choosing a
  composition. Read relevant screens, content, and design guidance selectively;
  report omitted areas and inspect necessary detail before drawing conclusions.
- Let content determine sections, grouping, density, and navigation. Include a
  chart for a real question, a metric with a defined meaning, and a section with
  useful information. A familiar pattern is valid when it serves the task.
- Tie hierarchy, typography, color, spacing, imagery, and motion to readability,
  interaction, or product identity. Evaluate techniques in context; cards,
  gradients, icons, and minimal layouts are choices, not automatic defects.
  Preserve requested visual direction while identifying concrete usability costs.
- Use supplied or verified facts. Keep demonstration data visibly identified.
  Customer logos, testimonials, statistics, security claims, and product screenshots
  need real evidence; expose missing material instead of manufacturing credibility.
- Make controls fulfill their stated action. Where an integration is outside scope,
  provide an honest preview or clearly unavailable state and report the limitation.
  Describe prototype behavior accurately; local simulation is not a live integration.
- Design reachable empty, loading, error, success, and unavailable states with useful
  explanation or recovery. Avoid adding states or controls without a current need.
- Keep essential information and actions usable across supported widths, input
  methods, zoom, and themes. Prefer established accessible primitives. Decoration
  and motion should preserve legibility, focus, and reduced-motion needs.
- Preserve recognizable product character. Removing unnecessary decoration should
  leave a deliberate composition; distinctiveness does not justify unfamiliar
  interaction or ignoring the user's design system.

## Verify and report

Inspect the rendered result when a browser or preview is available. Exercise the
affected actions and relevant states, including narrow and intermediate widths.
Reuse project tooling; report unavailable runtime access and untested interactions.
Source inspection or a static screenshot cannot establish functional completeness.

Review findings identify the element, concrete effect, and supported improvement.
Separate functional defects from optional aesthetic recommendations. For edits,
report the resulting behavior, checks actually performed, and material gaps.
Use sufficient existing checks; stylistic choices do not need literal-presence tests.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
