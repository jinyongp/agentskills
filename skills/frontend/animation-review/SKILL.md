---
name: animation-review
description: "Review a selected animation, component, or motion diff on web or React Native for supported behavioral defects and usability costs. Return evidence and scoped recommendations; implementation and repository-wide audits are separate tasks."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Review

## Scope

Review the selected motion or changed component on web or React Native. Resolve
the target, platform, intended behavior, and applicable product conventions.
Keep source edits, dependency changes, and publication within separate user
authorization. Repository-wide inventory is outside a selected review's coverage.
Recover agreed interaction limits and their rationale before reporting missing
behavior; resolve unknown intent rather than proposing an expanded interaction.

Read [references/criteria.md](references/criteria.md) when assessing timing,
gesture continuity, performance, or platform-specific evidence.

## Review

1. Begin with counts and relevant paths, then inspect selected code, callers, and
   states. Use available bounded inspection tools; report omissions and recover
   required detail before conclusions. Pin comparison revisions where applicable.
2. Establish what the motion communicates and how often the action occurs. Respect
   intentional brand motion, local tokens, and documented tradeoffs. Judge observed
   delay and lost usability, not departure from a preferred preset.
3. Exercise or trace entry, exit, rapid retrigger, reversal, cancellation, and
   unmounting. Check stale completions, remount flashes, jumps, and continuity of
   position or velocity. Separate a real failure path from a theoretical preference.
4. For gestures, sheets, and screen transitions, verify scroll/gesture arbitration,
   alternate controls, dismissal, focus, and navigation behavior as applicable.
   On web, include pointer cancellation and keyboard/viewport access. On native,
   include system back, platform gestures, safe areas, and on-screen keyboard behavior.
5. Check reduced motion and meaningful feedback: actions and state remain perceivable
   and operable. Essential controls must work without hover, dragging, or haptics.
   Avoid treating an attribute or preference hook as proof of correct behavior.
6. Investigate suspected frame drops with appropriate profiling. Web properties do
   not guarantee compositing; native worklet/native-driver use does not guarantee
   smoothness. Report release/debug build, environment, and load for measurements.
7. Confirm each candidate against surrounding behavior and task requirements.
   Merge shared causes; distinguish functional/accessibility defects, evidenced
   usability costs, and optional aesthetic suggestions. A clean review is valid.

## Result

Lead with supported findings, each giving location, trigger/state, affected user
outcome, evidence, and a scoped recommendation. Name a violated contract or concrete
cost; fixed duration, easing, CSS, or library checks alone are insufficient.
Report target, observed versus inferred behavior, checks, and material gaps.
No supported findings does not prove every state or device is correct.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
