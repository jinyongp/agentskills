---
name: animate
description: "Build or adjust web motion for transitions, gestures, sheets, drawers, and feedback. Use when implementation is requested; choose tools from the project and preserve interruption, keyboard access, and reduced-motion behavior."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animate

## Scope

Implement the requested web motion in its authorized area. Gestures, route
transitions, sheets, drawers, and keyboard-aware interactions belong here too.
Inspect local tokens, components, dependencies, and browser requirements first.
Reuse the simplest capable existing mechanism; follow user tool requirements.

Read [references/interactions.md](references/interactions.md) for gestures, sheets,
route transitions, or viewport/keyboard coordination. Read
[references/mechanics.md](references/mechanics.md) when choosing timing, interruption,
or profiling a performance issue. Each is optional until its condition applies.

## Decisions and implementation

- Establish the state change and user benefit: orientation, continuity, feedback,
  or explanation. Frequent actions need especially prompt feedback. Keep an instant
  response when animation would delay work; a request for motion still warrants
  explaining a concrete usability conflict.
- Reuse product motion tokens and supported primitives. Choose easing or a spring
  from the interaction, distance, and existing conventions, then tune the rendered
  result. Starting values are proposals, not universal acceptance thresholds.
- Model resting, entering, exiting, interrupted, and cancelled states as needed.
  Retarget from the current visual state; release must respect the intended gesture
  outcome and relevant velocity. Clean up listeners, timers, and stale completions.
- Prefer transform/opacity for cheap motion, while preserving layout and appearance.
  Layout animation can be justified by a real need; measure relevant cost instead of
  banning a property. Browser compositing and frame rate require evidence.
- Preserve hit targets, source order, names, focus, and operability during transitions.
  Use accessible component primitives for dialogs and menus; an animated shell
  does not supply their behavior. Keyboard and explicit controls must reach the
  same required outcome as gestures.
- Implement a reduced-motion alternative that retains information and actions.
  Reduce nonessential travel, parallax, looping, and overshoot; choose instant
  updates or gentler feedback as appropriate. Pointer-driven hover is optional;
  essential actions remain available to touch and keyboard users.

## Verify and deliver

Exercise rapid retriggering, reversal, cancellation, and unmounting; check affected
states, input methods, reduced motion, and narrow viewports. Use project browser
tooling and representative load when relevant. Inspect the final implementation
and reuse sufficient existing checks; add tests only for uncovered behavior.
Report the behavior, tool choice, checks, and unverified conditions. If runtime
access is unavailable, distinguish source inspection from observed motion.
Keep unrelated cleanup and automatic dependency installation outside task scope.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
