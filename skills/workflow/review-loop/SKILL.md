---
name: review-loop
description: "Review and fix a requested scope iteratively while preserving accepted tradeoffs. Track coverage, confirm eligible defects, recheck affected areas, and finish only when all requested areas and required validation are resolved."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Review Loop

Use for an explicit review-and-fix or review-until-clean request. Plain review
returns findings without edits. Follow project tools and current authorization;
committing, publishing, deployment, and live data changes keep their own scope.
Apply accompanying guidance within this task.

## Core rules

- **Eligible fixes only.** Confirm trigger, location, violated contract, and effect.
  Fix required behavior, in-scope regressions, or concrete reachable safety/data
  violations. Preserve agreed simplifications. Optional capabilities, general
  hardening, and preferences are not missing requirements.
- **Whole scope.** A clean area does not end work on pending areas.
  Adjacent code informs the contract without expanding the target.

For uncertain scope or finding eligibility, read [contract.md](references/contract.md).
For external review or bot comments, read [feedback.md](references/feedback.md).

## Review, fix, recheck

1. **Contract.** Resolve paths/revisions and recover current user decisions,
   instructions, plans, handoffs, and relevant public promises.
   Record required behavior, agreed limits/omissions and their rationale, accepted
   risks, and checks. Unknown intent does not authorize imagined requirements;
   resolve material uncertainty before affected fixes.
2. **Coverage ledger.** Map scope into areas. Track each as pending, reviewed,
   needs-recheck, or blocked, with target state and evidence. Keep this ledger inline
   unless saving is needed.
3. **Inspect.** Review all areas. Begin with path/count summaries, then
   selected code, callers, contracts, and checks. Report omissions and recover needed
   pages; keep full repositories/diffs/logs outside default input. Use native filters
   or a tested bounded helper for large mechanical output. Delegation is optional;
   a sequential pass must cover the same requested areas.
4. **Confirm.** Apply the finding criteria; merge shared causes and separate
   suspected issues from confirmed defects.
5. **Correct.** Fix confirmed causes within authorization, preserving user work and accepted
   behavior. Keep completion criteria stable; changing them needs a scope decision.
   Reuse checks; add coverage only for a meaningful uncovered failure
   with justified expectations. A fix requiring a new contract or capability needs
   that decision first. Continue independent review while a decision is pending.
6. **Recheck.** Reproduce the failure and inspect affected callers/contracts. Mark affected areas,
   including unchanged callers, as needs-recheck. Keep unaffected work and valid evidence.
   Finish pending areas too. Reopen earlier findings when new evidence invalidates
   them. Refresh the ledger after each pass, including failures and blocked checks.
7. **Completion.** Repeat until all requested areas are reviewed, no eligible findings remain, and
   required checks apply to the final state. A pending reviewer or inaccessible area
   leaves coverage incomplete. Stop blind retries without new evidence; an A-to-B-to-A
   correction requires resolving the conflicting contract or assumption. On missing
   access, unresolved decisions, or an agreed budget limit, report partial coverage
   and the next needed action rather than claiming a clean review.

## Result

Return contract sources/limits, area coverage, fixes, remaining
findings/decisions, actual checks and tested state, and gaps. No findings within
complete scoped coverage is valid, not proof of all possible correctness.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
