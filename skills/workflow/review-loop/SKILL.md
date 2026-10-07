---
name: review-loop
description: "Review and fix a requested scope iteratively while preserving accepted tradeoffs. Track coverage, confirm eligible defects, recheck affected areas, and finish only when all requested areas and required validation are resolved."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Review Loop

## Scope

Use for an explicit review-and-fix or review-until-clean request. Plain review
returns findings without edits. Follow project tools and current authorization;
committing, publishing, deployment, and live data changes keep their own scope.
This skill works alone; accompanying review or validation guidance serves one task.

For uncertain scope or finding eligibility, read [contract.md](references/contract.md).
For external review or bot comments, read [feedback.md](references/feedback.md).

## Procedure

1. Resolve target paths/revisions and recover the active contract from current user
   decisions, applicable instructions, plans, handoffs, and relevant public promises.
   Record required behavior, agreed limits/omissions and their rationale, accepted
   risks, and required checks. Unknown intent is not permission to complete imagined
   requirements; resolve material uncertainty before affected fixes.
2. Map the whole requested scope into review areas. Track each as pending, reviewed,
   needs-recheck, or blocked, with target state and evidence. Keep this ledger inline
   unless saving is needed. A clean area does not end work on pending areas. Adjacent
   code informs the contract; discovering it does not expand the review target.
3. Review all areas progressively. Begin with relevant path/count summaries, then
   selected code, callers, contracts, and checks. Disclose omissions and recover needed
   pages; keep full repositories/diffs/logs outside default input. Use native filters
   or a tested bounded helper for large mechanical output. Delegation is optional;
   a sequential pass must cover the same requested areas.
4. Confirm each finding's trigger, location, violated contract, and effect. Eligible
   fixes address required behavior, an in-scope regression, or a concrete reachable
   safety/data violation. Preserve agreed simplifications; optional capabilities,
   generalized hardening, and preferences are not missing requirements. Merge shared
   causes and separate suspected issues from confirmed defects.
5. Apply authorized fixes to confirmed causes, preserving user work and accepted
   behavior. Use existing checks; add coverage only for a meaningful uncovered failure
   with justified expectations. A fix requiring a new contract or capability needs
   that decision first. Continue independent review while a decision is pending.
6. Reproduce the failure and inspect affected callers/contracts. Mark affected areas,
   including unchanged callers, as needs-recheck; retain unaffected valid evidence.
   Finish pending areas too. Reopen earlier findings when new evidence invalidates
   them. Refresh the ledger after each pass, including failures and blocked checks.
7. Repeat until all requested areas are reviewed, no eligible findings remain, and
   required checks apply to the final state. A pending reviewer or inaccessible area
   leaves coverage incomplete. Stop blind retries without new evidence; an A-to-B-to-A
   correction requires resolving the conflicting contract or assumption. On missing
   access, unresolved decisions, or an agreed budget limit, report partial coverage
   and the next needed action rather than claiming a clean review.

## Result

Return contract sources and material agreed limits, area coverage, fixes, remaining
findings/decisions, actual checks and tested state, and gaps. No findings within
complete scoped coverage is a valid result, not proof of all possible correctness.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
