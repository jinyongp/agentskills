# Active contract and finding eligibility

Read when a compromise, unknown intent, or proposed new behavior changes a decision.

- Recover current user choices and applicable project requirements before evaluating
  completeness. Link their sources; retain only rationale not recoverable there.
  Code shows behavior, but absent code does not prove a feature was forgotten.
- Explicitly scoped prototypes, local simulations, manual steps, supported subsets,
  and accepted limitations can be complete under their actual contract. A review
  does not promote them to a larger maturity level. User changes can revise scope;
  a reviewer preference cannot. Required final checks remain required.
- For a proposed finding, name the accepted requirement or prior in-scope behavior
  it violates and trace a reachable failure. Missing automatic retries, persistence,
  provider fallbacks, or extension points are not defects merely because they could
  be useful. A requested design audit may discuss evidenced costs within its scope.
- Unknown intent is a decision gap. Inspect available decisions and direct contracts;
  ask only when the answer changes eligibility or the fix. Review unaffected areas
  meanwhile. Keep optional enhancements separate and only include them when requested.
- Concrete safety concerns include a bypass of a claimed access boundary, exposure
  of private data handled by the flow, unintended code execution, or destructive
  effects outside explicit intent. Show the actual path; a lack of speculative
  hardening is not such a violation. If correction would revise an accepted contract,
  surface the conflict and resolve it before that edit.
- Example: a user chose a local preview with simulated payment. Preserve simulation;
  do not add a payment provider. A preview labeled as real payment completion can
  still violate the agreed disclosure. Review that existing promise and repair it
  within scope, or resolve conflicting instructions.

Use review coverage and fix impact separately. If areas A, B, and C are requested,
a clean A leaves B and C pending. A fix in B that changes a contract consumed by A
reopens A; C still needs its first review. Complete only after all requested areas
have current evidence and the required final checks are resolved. No fixed cycle
count or number of findings substitutes for these conditions.
