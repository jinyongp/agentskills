# Mobile browser decisions

Read only the section matching the symptom. Check current target-browser support
and the project's existing primitives before adopting an API.

## Viewport, chrome, and keyboard

Use stable small viewport sizing when content must fit with expanded browser chrome;
dynamic sizing can follow chrome changes but may resize content during scrolling.
The layout determines whether height, min-height, or ordinary flow is appropriate.
See [viewport units](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length).

The virtual keyboard and visual viewport require separate verification: dynamic units
do not universally account for keyboard occlusion. Reuse established project keyboard
handling. Add visual-viewport or supported keyboard APIs only for a demonstrated gap,
and clean up subscriptions. Avoid double offsets from independent compensation paths.

Preserve zoom in viewport configuration. For edge-to-edge layouts, confirm whether
viewport-fit and safe-area insets are needed; ordinary pages need no compulsory
configuration changes. Include relevant insets at owning surfaces and avoid duplicating
them on parents and children.
See [viewport metadata](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport).

## Input and feedback

Capability queries can constrain decorative hover, but hybrid devices need touch,
mouse, and keyboard behavior together. Keep essential controls operable without hover.
Keep input text readable under target-browser behavior; investigate focus zoom on
the actual browser rather than enforcing an unexplained font-size literal.

Use press feedback and preserve activation/cancellation semantics. Custom tracking
needs an active-pointer owner, cancellation handling, and an explicit alternative.
Select touch-action before the gesture starts at the relevant surface, preserving
required browser pan/zoom behavior. Changes during an active gesture do not redefine
that gesture's browser policy.
See [touch-action](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action).

## Scroll and browser affordances

Identify the actual scroll container before changing overscroll behavior.
Containment can prevent unwanted scroll chaining but also affect boundary actions
such as browser navigation or refresh. Preserve those capabilities unless the
requested interaction needs a scoped tradeoff. Blanket page-wide disabling can
change unrelated flows. Nested gesture and scroll ownership must be verified.
See [overscroll behavior](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/overscroll-behavior).

Theme/status-bar presentation is optional and browser/display-mode dependent.
Match product requirements and verify the relevant environment; metadata in source
does not establish its appearance on every platform.
