# Validation cadence

Read for multiple work units or an expensive final check.

- For each meaningful outcome, choose a targeted check against a plausible failure.
  Reuse adequate coverage and applicable evidence. File count, save frequency and
  a quota of regression tests do not determine the cadence.
- For required final integration checks, identify the command, scope, environment,
  fixtures and setup prerequisites before they are needed. Record this information
  in an existing plan or inline; preparing a command does not mean executing it.
- Defer expensive integrated checks until affected units are ready when later work
  does not depend on their result. Run earlier when a result gates the next unit,
  targeted evidence exposes a shared failure, or project rules require it.
- Distinguish implementation-ready from complete while required final checks remain
  pending. Do not waive required checks because the implementation is small.
- After a failure, reopen the affected completion criterion. Fix only within current
  authorization, rerun affected checks and the failed required integration check,
  and reuse unrelated evidence while its tested inputs still match.

Example: independent parser cases can be checked after their work units, with a
required CLI integration run after wiring is complete. A migration result consumed
by the next deployment step must be checked before that step. Neither case requires
a permanent test for each edit or repeated full-suite runs without a new reason.
