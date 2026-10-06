# Review completeness and design cost

- Establish accepted behavior before judging a shortcut. Show the actual user/caller
  path that loses output, compatibility, access or recovery. An authorized prototype
  has different completion criteria from a production feature.
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
