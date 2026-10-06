# Motion review criteria

Read only the applicable section when judging a candidate.

## Timing and continuity

Existing tokens and accepted product behavior govern. Frequent interactions need
prompt acknowledgement; long distance or explanation may justify more time.
A numerical duration or chosen curve alone is not a defect. Observe repeated use,
interruption, and whether the user can act while motion settles.

When an interaction changes again, preserve current position and relevant velocity,
and prevent stale completion from changing new state. Keyframes and transitions
can both be correct when ownership, cancellation, and restart behavior are explicit.
Entry/exit symmetry can clarify spatial continuity, but task-driven asymmetry is valid.

## Gestures and accessible behavior

Check direct manipulation, settling after release, cancellation, and nested scrolling.
A swipe dismiss action also needs a reachable alternative. A visually smooth sheet
still fails if focus or its required action becomes inaccessible. Reduced motion
should preserve the same information and actions, with suitable instant or gentler
feedback; its existence in source does not prove every path uses it.

## Performance and platform

Use traces or runtime measurements for performance findings. On web, inspect actual
layout/paint, compositing, and main-thread contention. On React Native, determine the
animation execution path, JS/UI-thread load, rendering, and supported device behavior.
Property choice and moving work off JS help only part of the pipeline.

Device-specific gestures, keyboard behavior, and native feedback need relevant
platform evidence. A web screenshot or native simulator cannot establish all
physical-device behavior. Keep conclusions inside measured builds and environments.
