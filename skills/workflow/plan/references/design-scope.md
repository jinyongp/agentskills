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
- For a proposed structural change, identify actual friction: a recent change had
  to touch the same rule in several places, ownership is unclear, or understanding
  one operation requires chasing fragmented modules. Use relevant history/callers
  as evidence; file size, naming style, or an abstraction count alone is insufficient.
- Compare a concrete current change before and after the proposed boundary. Does
  it reduce coordinated edits or clarify state/resource ownership? Remove or merge
  a layer only if its required behavior and lifecycle remain accounted for.
- Keep the review focused on the named pain point or demonstrably affected area.
  Existing architecture decisions and accepted omissions remain constraints; a
  hypothetical future extension does not justify redesigning the project.
- User-selected behavior remains part of completion. A reduced prototype is appropriate
  when requested or accepted; an unfinished happy path is not a completed feature.
