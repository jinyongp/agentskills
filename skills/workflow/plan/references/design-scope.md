# Choosing enough design

Use this comparison only when scope or design is consequential.

- A usable path includes the requested outcome and relevant failure/recovery states.
  For an upload, file handling alone may leave users unable to tell whether it
  completed or recover from failure. Match states to the actual product contract.
- Existing and native features are candidates, not automatic winners. A native date
  control may suffice; range selection, supported browsers, or accessibility needs
  can establish a concrete gap that justifies a maintained component.
- Evaluate abstraction, configuration, dependencies and infrastructure by current
  responsibilities, resource ownership, and change/operation cost. A cleanup wrapper
  can be worthwhile with one caller. A plugin registry needs an actual extension need.
- Compare the simplest complete alternative with added design only where it changes
  the decision. List a material limitation or cost, not speculative future features.
  A small reversible edit can need no alternatives document.
- User-selected behavior remains part of completion. A reduced prototype is appropriate
  when requested or accepted; an unfinished happy path is not a completed feature.
