# Motion for React

Read only for a project using Motion for React or Framer Motion. Follow installed
version APIs and imports; this reference does not authorize installation or migration.

For exits, keep the presence owner mounted and give tracked children stable, unique
keys. Remounting changes lifecycle, not merely replay. Match sequencing to the
interaction; waiting for exit can delay the next usable state. Verify interruption
and cleanup for manual removal callbacks.
See [AnimatePresence](https://motion.dev/docs/react-animate-presence).

Use motion values for continuous visual updates when appropriate, and React state
for semantic changes. Remove subscriptions on teardown. Avoiding render-per-frame
work does not prove rendering or composition is cheap.
See [motion values](https://motion.dev/docs/react-motion-value).

Use layout animation for justified spatial continuity. Keep identity stable;
account for scroll/fixed coordinate spaces and inspect scaled children for distortion.
Avoid competing owners of the same transform.
See [layout animation](https://motion.dev/docs/react-layout-animations).

For dragging, distinguish finger tracking from release settling and respect gesture
ownership. For scroll, distinguish visibility triggers from progress-linked values.
Preserve required outcomes under reduced motion; global configuration may not cover
custom effects.
