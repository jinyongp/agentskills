---
name: responsive
description: "Implement or review responsive web layouts across supported widths, content sizes, zoom, and input conditions. Use for reflow, overflow, mobile navigation, and viewport or on-screen keyboard problems."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Responsive

## Scope

Implement or review layout behavior in the requested area. Follow the supported
browsers, sizes, component system, and existing breakpoints. Change a breakpoint
when content demonstrates a failure, not merely to match a device list.
Review-only work returns findings; source changes follow the user's edit scope.

## Procedure

1. Inspect the affected layout, real content, and local sizing conventions. Begin
   with selected components and rendered states; disclose omitted areas and inspect
   relevant detail before claiming a page-wide conclusion.
2. Reproduce the failure at its width and content conditions. Sweep narrow,
   intermediate, and wide widths, especially either side of an affected breakpoint.
   Use as many layout states as the content needs; a working two-state layout is valid.
3. Preserve information priority and logical source order when stacking or relocating
   content. Keep navigation and essential actions discoverable. Hiding secondary
   presentation must retain access to its information when the task requires it.
4. Find the actual overflow source: intrinsic sizing, fixed tracks, unbroken text,
   media, or viewport constraints. Allow appropriate wrapping and shrinking; keep
   meaningful content and focus visible. Intentional cropping is valid for decorative
   media. Do not mask a broken layout by clipping required text or controls.
5. Keep genuinely two-dimensional tables, diagrams, and code usable through localized
   scrolling or another appropriate presentation. Distinguish intended scrolling
   from accidental page overflow. Preserve labels and keyboard access.
6. Exercise long labels, realistic data extremes, enlarged text, and relevant empty
   or failure states. Fixed pixel values and existing sizing rules may remain when
   behavior works; reflow does not require a universal CSS unit or a new dependency.
7. On mobile, check orientation, browser chrome, safe areas, sticky elements, and
   on-screen keyboard effects where relevant. Focused inputs and submission controls
   must remain reachable; do not force scroll or add padding without an actual need.
   Verify touch affordances and alternatives to hover for required actions.

## Verify and report

Use project browser or preview tooling to confirm relevant content and actions remain
usable across the affected range. Check zoom or text enlargement as well as narrow
widths; viewport resizing alone does not exercise mobile browser chrome or a keyboard.
Use a real device when that behavior matters, or report the exact emulation limit.

Reuse sufficient checks. Add coverage only for a concrete layout or interaction failure
that existing evidence misses, asserting user access rather than CSS literals.
For review, identify width/state, affected element, user effect, and evidence.
For changes, report verified conditions, intentional scrolling, and remaining gaps.
Keep conclusions within inspected pages and states; screenshots alone do not prove
that controls work.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
