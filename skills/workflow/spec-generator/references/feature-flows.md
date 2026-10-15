# Product feature flows and document reconciliation

Use when the user requests a feature inventory, more detail for product journeys,
or synchronization between product documents. This is product behavior definition;
do not silently turn it into implementation tickets or prescribe a build sequence.

- Recover the authoritative requirements, accepted omissions, and documents the
  user wants changed. A specification can have any project-selected filename.
  A missing file is not a reason to require another installed skill.
- Group by coherent outcomes. Record actor/trigger, relevant prerequisites, the
  observable successful outcome, and consequential rejection or recovery behavior.
  Describe UI only for features with UI; include API, scheduled, and background
  outcomes when they belong to the product.
- Link each flow to its requirement and acceptance evidence. Keep proposed behavior
  distinct from accepted scope. Clarify consequential gaps rather than expanding
  a technical-stack choice into an implied feature.
- Dependencies follow required contracts or prior state. Staff-facing features,
  authorization, and rate limits may be prerequisites; do not impose a universal
  foundation/public/admin/cross-cutting ordering.
- When reconciling documents, identify changed requirements and the known baseline.
  If both documents changed, resolve conflicting intent or source authority before
  updating affected passages. The most recently edited file is not automatically
  authoritative. Preserve unrelated text, identifiers, and accepted history.
- Recheck affected flows against the reconciled requirements. Report changes,
  unresolved conflicts, and untouched boundaries; do not claim the product or
  its implementation was verified merely because the documents now agree.
