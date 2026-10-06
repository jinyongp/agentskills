# Symptom-directed probes

Read only the matching section. These are hypotheses, not automatic fixes. Confirm
the installed engine's behavior and target environment.

## Jump or flicker

Inspect the first changed frame: did position jump, identity change, or opacity reset?
Check mount keys, initial values, transform ownership, and geometry before tuning.
Compare coordinates in the relevant scroll/fixed container. Late images or fonts can
change geometry independently of the animation engine.

For retained exits, confirm the presence owner remains mounted and an old completion
cannot remove new content. Reproduce rapid reopen and interrupted teardown.
[Motion presence](https://motion.dev/docs/react-animate-presence) and
[layout documentation](https://motion.dev/docs/react-layout-animations) cover engine
semantics; use APIs for the installed version.

## Drag lags, snaps, or dismisses incorrectly

Compare pointer position with the driven value during tracking; then inspect release
direction and relevant velocity. Distinguish a transition applied during tracking
from slow processing. Check active-pointer identity, capture loss, cancellation,
nested scrolling, and stale settling controllers. On native, inspect gesture ownership
and runtime boundaries. Preserve explicit alternate controls and dismissal behavior.

## Feels slow or robotic

Locate the delay: before acknowledgement, during travel, or during final settling.
If frames are regular, compare distance, origin, easing, and settling with the intended
interaction and local tokens. Test repeated use. A duration outside a preferred range
alone does not establish a defect.

## Stutters under load

Record the reproducible interval using project-approved tools. On web, distinguish
scripting, layout, paint, and composition. On native, distinguish JS from UI/rendering
load in a representative release build. Investigate framework renders, synchronous
measurement, expensive surfaces, or boundary crossings where evidence points.
Property choice alone cannot establish acceleration.
See [browser profiling](https://developer.chrome.com/docs/devtools/performance) and
[React Native performance](https://reactnative.dev/docs/performance).

## Stuck after cancellation or reduced motion

Inspect semantic state independently of visual playback. Completion callbacks may
not run after cancellation, removal, or disabled motion. Reproduce setting changes
mid-transition, cleanup, and reopening. Preserve final state and required controls
without decorative playback; avoid masking a race with a timer.
