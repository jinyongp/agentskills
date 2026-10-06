---
name: animate-native
description: "Build or adjust React Native and Expo motion for gestures, screens, sheets, press feedback, keyboards, and optional haptics. Use for native implementation with project-compatible tools, reduced motion, and device-aware verification."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animate Native

## Scope

Implement requested motion in React Native or Expo. Inspect relevant components,
navigation, platform requirements, installed versions, architecture, and local motion
tokens with bounded project tooling. Preserve current user tool choices and reuse a
capable existing animation/gesture system. New dependencies need a concrete gap and
project-compatible versions; a simple effect does not require a stack migration.

Read [references/runtime.md](references/runtime.md) for driver/worklet selection,
gesture coordination, navigation, keyboard behavior, or haptics. Read only its
applicable section. Web has the same interaction concerns with different mechanisms;
a React Native web build also requires verification of its web-specific behavior.

## Implement

- Define the state change, user benefit, trigger, and completion criteria. Frequent
  actions need prompt acknowledgement, not a universal animation ban. Tune distance,
  duration, easing, or a spring using local conventions and observed interaction.
- Model entry, exit, interruption, reversal, and cancellation. Preserve current
  position and relevant release velocity. Clean up subscriptions and stale callbacks;
  animation completion must not overwrite a newer navigation or interaction state.
- For drag/swipe/sheets, resolve nested scrolling, gesture ownership, release outcomes,
  safe areas, and alternate controls. Use established accessible primitives. Restore
  focus or accessibility focus where appropriate and respect platform back/dismiss
  behavior rather than introducing competing navigation handlers.
- Keep focused fields and essential controls reachable around keyboard and viewport
  changes. Coordinate with existing keyboard handling and navigation; measure the
  actual platform behavior before adding compensation or another library.
- Choose the execution path from the workload. High-frequency updates should avoid
  unnecessary React rerenders and JS/UI-thread crossings. A suitable native driver
  or worklet may help; layout and rendering still have cost. Profile a concrete
  problem instead of asserting every JS animation or layout property is wrong.
- Respect reduced-motion settings, including changes during use when supported.
  Preserve information and actions through instant or gentler alternatives. Haptics
  are optional, semantic feedback with a supported platform path; success and
  accessibility must not depend on a vibration happening.
- Preserve hit targets, accessible names/states, and input alternatives throughout
  motion. Core interactions should remain usable if a gesture, haptic capability,
  or nonessential animation is unavailable.

## Verify and report

Exercise repeated input, cancellation, screen removal, reduced motion, nested scroll,
and relevant keyboard/back behavior. Use available supported-platform tooling and
representative devices/builds for the changed behavior. Performance conclusions need
appropriate release-build evidence under relevant load; simulator/debug previews
have explicit limits. Reuse sufficient checks and add tests only for uncovered
state or interaction behavior. Report tool/version choices, checks, and unverified
platforms. Source inspection does not establish device smoothness or working haptics.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
