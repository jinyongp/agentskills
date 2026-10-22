---
name: ui-design
description: "Create, revise, or review interface composition using actual content, user tasks, and product identity. Use for layout, visual hierarchy, components, and meaningful UI states while respecting the requested edit scope."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Ui Design

Create, revise, or review the requested interface using its real tasks, content,
and product identity. Reuse existing components and design conventions. A review
returns recommendations; requested edits authorize only the named scope.
Recover agreed scope and simplifications before judging completeness; retain their
rationale. Resolve consequential missing direction from evidence or a focused question.

## Core rules

- **Real evidence.** Use supplied or verified facts; identify demo data. Logos,
  testimonials, statistics, security claims, and product screenshots need evidence.
  Expose missing material instead of manufacturing credibility.
- **Honest actions.** Controls must fulfill their stated action. If an integration
  is outside scope, provide an honest preview or clearly unavailable state and
  report its limits. Local simulation is not a live integration.
- **Usable states.** Keep essential information and actions usable across supported
  widths, input, zoom, and themes. Use accessible primitives; decoration and motion
  must preserve legibility, focus, and reduced-motion needs.

Read [references/craft.md](references/craft.md) for content grouping, hierarchy,
component defaults, spatial feedback, layers, or typography. Read the matching section.
Read [references/purpose.md](references/purpose.md) when choosing priorities for
a landing page, task interface, reading surface, or showcase.

## Design decisions

- **Primary task.** Establish action and information needs before choosing a
  layout. Inspect relevant screens, content, and guidance selectively; report
  omissions and recover necessary detail before drawing conclusions.
- **Relationships.** Group by task role: peers, label/value, state/action, sequence, or
  claim/qualification. Keep labels and qualifications with what they describe.
  Use these relationships for grouping, order, density, and navigation; charts
  and metrics need a defined question or meaning.
- **Hierarchy.** Locate next action, current state, and decisive facts in the rendered view.
  When uniform styling obscures roles, regroup, label, reorder, or change emphasis;
  swapping separators alone cannot repair the relationship. Compact metadata and
  equal-weight peers can be valid. Preserve product identity; judge cards,
  gradients, icons, and minimal layouts by concrete usability effects.
- **Reachability.** Design empty, loading, error, success, and unavailable states with useful
  explanation or recovery. Avoid adding states or controls without a current need.
- **Identity.** Resolve product character from screens, tokens, assets, or a voice sample.
  Carry those cues into the changed surface; explain departures tied to a user task.
  Label proposed cues as design choices when identity evidence is absent.

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
