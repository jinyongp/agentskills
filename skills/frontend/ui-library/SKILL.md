---
name: ui-library
description: "Choose frontend components or libraries for a concrete capability gap. Compare current project tools, framework and platform compatibility, accessibility, maintenance, and integration cost; preserve explicit user choices."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Ui Library

## Scope

Choose a frontend library or component for a concrete capability question. Honor a
specified tool; evaluate its fit and limitations rather than replacing it with a
favorite. Ordinary implementation does not require a dependency-selection exercise.
A recommendation alone does not authorize installation or migration.

Inspect the relevant manifest/lockfile entries, framework, platform, rendering model,
supported browsers, design system, and dependency policy through targeted project
tools. Keep unrelated dependency lists outside default input.
Read [references/selection.md](references/selection.md) when comparing capability
or integration tradeoffs.

## Decide

- Identify the required outcome and hard constraints: accessible interaction,
  SSR/hydration, native/web support, rendering scale, licensing, or bundle limits.
  Distinguish required behavior from optional convenience.
- Prefer a capable existing dependency or platform primitive. For a simple effect,
  CSS or native APIs may be sufficient. A complex accessible interaction can justify
  an established primitive; assess the actual gap instead of assuming hand-written
  code or a new package is always wrong.
- Check candidate facts against official documentation, repository/release evidence,
  and relevant license files. Verify current versions and compatibility before
  recommending APIs or commands. Recent release frequency alone does not prove
  reliability, abandonment, or fitness. Mark unavailable or uncertain evidence.
- Compare only credible candidates that meet the constraints. Evaluate integration
  cost, API stability, accessibility behavior, customization, performance evidence,
  maintenance, and replacement cost where relevant. React-specific tools do not
  automatically fit Solid, Vue, Astro boundaries, or React Native.
- Recommend a preferred path and its reason, including staying with the existing
  tool when adequate. Explain material tradeoffs or remaining uncertainty; an
  exhaustive catalog and forced menu add little when one choice clearly fits.
  Keep the user's requested comparison breadth.

## Integrate and verify

When implementation is authorized, use the project's package manager, supported
versions, and local conventions. Limit dependency/lockfile changes to the selected
integration; retain existing ownership and rendering boundaries.
A capability limitation may require clarification or a proposal before a larger
migration; do not treat a recommendation as permission for it.

Exercise the behavior that motivated selection, plus relevant accessibility and
rendering/build conditions. Reuse existing checks; a small representative preview
may settle an uncertain fit without a full migration.
Return the decision, source links, relevant version assumptions, checks performed,
and unresolved gaps. Source claims or library reputation do not establish the
integrated component's correctness or measured performance.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
