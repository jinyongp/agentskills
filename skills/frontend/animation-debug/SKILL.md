---
name: animation-debug
description: "Diagnose and fix web or React Native motion that jumps, flickers, feels delayed, or breaks under interruption. Use for a concrete symptom; distinguish lifecycle, geometry, timing, and frame-performance causes."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Debug

## Scope

Diagnose a concrete web or React Native motion symptom. Preserve diagnosis-only
requests; apply a correction when requested or implied by a fix task. Keep the
interaction and project tool choices intact. A general motion audit or unrelated
backend performance task is outside this scope.

Start with the affected interaction, expected behavior, reproduction sequence,
platform/build, and relevant code. Inspect selected components and their state owners
through bounded project tooling; request exact detail only for a plausible cause.
Read the matching section of [references/causes.md](references/causes.md) when a
symptom needs a diagnostic probe. Full repositories and traces stay outside default input.

## Diagnose and correct

- Reproduce at normal speed and identify the first incorrect transition. Slow playback
  can expose ordering or geometry, but does not establish normal-speed performance.
  Include rapid reversal, cancellation, or concurrent input when it triggers the issue.
- Separate discontinuity, delayed acknowledgement, poor timing, and missed frames.
  A smooth but slow curve is not frame jank. A static screenshot cannot establish
  either. State the leading hypothesis and the observation that distinguishes it
  from alternatives; source-only hypotheses stay explicitly unverified.
- Trace ownership of visual values, layout, mounting, and semantic state. Look for
  competing transforms, remounts, stale completion, changed measurements, and gesture
  arbitration before changing easing. Check preference changes and skipped playback
  when controls depend on an animation event.
- Test a small discriminating change or instrument the affected interval. Preserve
  baseline behavior and remove temporary instrumentation afterward. For missed frames,
  inspect the relevant rendering/runtime trace before asserting the bottleneck.
- Correct the demonstrated cause within authorized scope. Retarget from current
  state where needed, preserve relevant release velocity, and keep input/focus and
  final state valid after cancellation. Tune timing against local conventions when
  timing is the cause. A library migration needs evidence of a capability gap.

## Verify and report

Replay the original failure and affected adjacent states under the same conditions.
Check relevant reversal, teardown, reduced motion, and input methods. Reuse sufficient
checks; add a regression test only for meaningful uncovered behavior, not preferred
curves or incidental literals. Match performance claims to measured device/build data.

Report symptom, supported cause, correction or next discriminating probe, validation,
and remaining gaps. Return selected locations and evidence intervals, not full logs.
For paged project output, retain omission counts and next-page positions; recover
required pages before conclusions. If runtime access is missing, give a reproducible
probe and separate source findings from observed results.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
