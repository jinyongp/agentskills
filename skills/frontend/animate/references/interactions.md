# Web interaction motion

Read the relevant section when implementing its interaction.

## Gestures and sheets

Track the active pointer and gesture state using the project's component or gesture
primitives. For custom handling, pointer capture can retain events outside the
element; handle cancellation and lost capture. Choose touch-action for the gesture
without disabling required page scrolling or pinch zoom. Preserve position during
a grab and pass relevant velocity into settling; avoid a transition lagging behind
the user's finger. Provide explicit, keyboard-operable alternatives.
See [Pointer events](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events).

A sheet also needs dialog semantics where modal, focus handling, background behavior,
and a reachable dismiss action. Keep nested scrolling distinct from dismissal.
Check safe-area and keyboard occlusion with the actual mobile browser where possible.
A desktop-sized preview does not exercise a mobile keyboard.

## Route and keyboard coordination

Coordinate outgoing and incoming content with the project's router and state
ownership. Restore or place focus and handle back navigation as required. Cancel
obsolete transitions when navigation changes again; an exit completion must not
remove new content. Keep meaningful loading/error states accessible.

When a keyboard changes the visible viewport, preserve access to focused fields
and actions. Use supported viewport or platform mechanisms only where necessary;
avoid adding scroll jumps or a new dependency to a working layout.
Haptic or other device feedback is an optional enhancement when requested and
supported; visual and semantic feedback still carry the outcome.
