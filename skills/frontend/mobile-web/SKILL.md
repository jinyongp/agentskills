---
name: mobile-web
description: "Diagnose or implement mobile browser behavior for touch, hover, scrolling, viewport sizing, safe areas, and on-screen keyboards. Use for web or PWA platform issues; preserve zoom, accessible controls, and project browser requirements."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Mobile Web

## Scope

Implement or diagnose mobile browser and PWA behavior in the requested area.
This covers touch/hover, scroll ownership, viewport/chrome changes, safe areas,
and keyboards. React Native implementation and general motion design have different
mechanisms; a native web build still needs its browser behavior verified.

Inspect selected controls, containers, viewport configuration, local platform
handling, and supported browsers. Follow project tools and current user choices.
Read only the matching section of [references/platform.md](references/platform.md)
when a platform symptom needs implementation detail.

## Diagnose and implement

- Reproduce the actual symptom and identify the owning layer: control, scroll
  container, viewport, or browser behavior. Check orientation, display mode, and
  keyboard state when relevant. A narrow desktop viewport alone does not reproduce
  a mobile keyboard, browser chrome, or every touch interaction.
- Keep mouse, keyboard, touch, and assistive input usable together. Use platform
  capabilities rather than guessing device type from width or user-agent strings.
  Hover is an enhancement; required actions have reachable alternatives.
- Provide prompt press feedback without committing an action prematurely. Respect
  cancellation and the control's activation semantics. Suppress browser tap feedback
  only where a usable replacement exists; retain visible focus and selection of
  meaningful text. Avoid blanket selection or context-menu suppression.
- Choose viewport sizing from the layout's needs, not a universal height recipe.
  Dynamic browser chrome, scroll containers, and the visual viewport affect different
  regions. Account for safe areas only where necessary and reuse existing insets or
  keyboard avoidance instead of layering duplicate compensation.
- Keep focused fields and essential actions reachable as the keyboard opens,
  orientation changes, and content grows. Preserve user zoom and readable inputs.
  Do not assume a viewport unit alone tracks the keyboard or disabling zoom fixes
  the underlying layout/input problem.
- Configure touch and overscroll behavior at the relevant gesture/scroll boundary.
  Preserve required page scrolling, pinch zoom, browser navigation, and intentional
  pull-to-refresh unless a scoped interaction requires a documented tradeoff.
  Handle cancellation and nested scroll; a custom gesture is not a substitute for
  accessible explicit controls.

## Verify and deliver

Use supported mobile browsers and a real device where the affected platform behavior
needs it. Available emulation can verify some layout or event paths; report exactly
what remains unobserved. Check relevant keyboard, chrome, orientation, safe-area,
hybrid input, and zoom conditions rather than a mandatory device checklist.

Replay the failure and affected adjacent states after changes. Reuse sufficient
project checks; add tests for meaningful uncovered user behavior, not required CSS
literals or viewport attributes. Report symptom, scoped correction, verified browser/
device conditions, and remaining gaps. Keep inspection to selected surfaces and
evidence; disclose omissions before making broader claims.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
