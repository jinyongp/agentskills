# CSS motion

Read for CSS implementation; check target browsers before adopting newer syntax.

Use a transition between styled states; use keyframes for an explicit sequence.
List intended properties so later style edits do not animate accidentally. Choose a
transform origin that fits the spatial relationship, such as an anchored popover.
Separate wrappers when layout positioning and an effect would overwrite one transform.

Entry and exit need lifecycle handling: immediate DOM removal prevents an exit.
Reuse the component's presence mechanism. Completion events can be skipped by
cancellation, zero duration, or removal; keep semantic state correct in those paths.
A retained exiting surface must have appropriate input and focus behavior.

Intrinsic-size transitions depend on browser support and the primitive in use. If
measurement is needed, account for content changes and avoid repeated synchronous
layout reads mixed with writes. Evaluate cost against the actual interaction.

For reduced motion, override affected properties and preserve their final state.
Keep application state independent of animation completion; blanket near-zero timing
can break event-dependent controls. JS-driven effects need their own preference handling.

See [CSS transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions/Using_CSS_transitions)
for property and lifecycle semantics.
