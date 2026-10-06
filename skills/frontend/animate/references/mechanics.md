# Motion mechanics

Read when choosing timing, handling interruption, or investigating performance.

## Timing and state

Start with existing duration/easing tokens. For a small web control, roughly
150-250ms can be a useful first trial, then judge distance, frequency, and perceived
delay. Larger transitions and explanation may need different timing. Do not flag
a chosen curve or duration solely for differing from this range.

Use transitions or a retargetable animation controller for frequently reversed
states. Keyframes can work when playback and cancellation are managed. Use a spring
when continuous velocity or physical settling helps. Keep position and relevant
velocity coherent across interruption; protect new state from stale callbacks.
The [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
provides playback controls; verify availability and behavior in target browsers.

## Performance and accessibility

Transform and opacity often avoid layout work, but compositing is not guaranteed.
Profile suspected layout/paint, large surfaces, filters, excessive promotion, and
main-thread updates. Reserve will-change for demonstrated needs and release it when
appropriate. Do not claim 60fps from property choice or a single screenshot.

Respect [reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
with an alternative that preserves the same information and controls. Essential
feedback can be instant; opacity is not automatically comfortable for every pattern.
Check the user's preference during runtime if it can change.
