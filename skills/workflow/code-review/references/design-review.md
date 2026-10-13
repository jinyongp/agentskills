# Review completeness and design cost

- Establish accepted behavior before judging a shortcut. Show the actual user/caller
  path that loses output, compatibility, access or recovery. An authorized prototype
  has different completion criteria from a production feature.
  Recover agreed shortcuts and their rationale from current decisions or handoffs.
  An intentional supported subset is not a missing feature. Unknown intent needs
  clarification when it changes the recommendation; keep new capabilities separate.
- For extra abstractions, dependencies or configuration, identify responsibilities
  and concrete costs: duplicated state, coupling, extra setup, ownership or parallel
  changes. Counted files/lines and hypothetical scale do not establish a problem.
- A single-use wrapper can correctly own cleanup; a library can cover real platform
  gaps. Assess the simplest viable alternative against the same requirements before
  recommending removal. Preserve required behavior and useful existing checks.
- Missing behavior is a defect when backed by a trigger and violated contract.
  Maintenance concerns without behavioral failure belong in distinct engineering
  observations, with evidence and a proportionate recommendation. Avoid inflating
  their severity or reporting personal preferences as defects.
- A valid complete design may deserve no finding. Review both extremes without
  requiring an issue, a redesign, a new dependency or a new test in every patch.

When a wrapper or module is hard to use, inspect what callers must know: sequencing,
configuration, error handling and invariants as well as method signatures. Propose
consolidation only when it removes demonstrated caller coordination or duplicated
responsibility; a shorter interface or fewer files alone does not establish benefit.
One implementation can justify a boundary that owns cleanup or protects a contract.

When moving tests to a more stable public interface, map existing meaningful cases
to replacement coverage first. Remove duplicated implementation-coupled checks only
after the behavior they protected remains observable. An outer test passing does not
justify deleting distinct lower-level cases it never exercises.
