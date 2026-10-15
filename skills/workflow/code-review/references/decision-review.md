# Review against recorded decisions

Use when the requested review checks architecture decisions, ADRs, or explicit
project rules. Apply the requested criteria without appending a general design
audit or inventing new standards.

1. Locate the applicable decision sources, their status, and relevant exceptions.
   Use the project's paths; no particular filename is required. Recover accepted
   prototype limits and current user decisions. A production rule may not apply
   to an intentionally isolated prototype. Missing or conflicting criteria remain
   explicit rather than being replaced with the reviewer's preference.
2. Pin the selected change and inspect affected boundaries, callers, and context.
   For each applicable rule, identify the changed code or file set that satisfies
   or violates it. A familiar pattern alone is not evidence of compliance.
3. Separate an explicit rule violation from a demonstrated runtime defect and
   from an engineering concern. A written structural requirement can be violated
   without an immediate crash; explain its stated purpose without fabricating a
   failure or inflating severity. Respect accepted exceptions and applicability.
4. Report the decision identifier/title, exact locations, observed deviation,
   supported consequence or rationale, and a concrete way to comply. Group by
   decision when useful, consolidate one underlying cause, and preserve unknowns.

Report reviewed decisions and gaps. No violations in the checked scope does not
prove every architecture property holds. Recommendations do not authorize fixes
or editing the decisions to match the patch.
