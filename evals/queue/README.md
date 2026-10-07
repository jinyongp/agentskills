# queue evaluation

## Revision verification — 2026-10-07

Body: 2,688 characters. Format/catalog validation passed for 52 skills; full
verification passed all 96 existing tests and skills@1.7.0 installation fixtures.
After adding the standalone MIT notice, temporary Codex and Claude project installs
copied this skill byte-for-byte. Creator validation passed. No live tracker or
independent agent evaluation was run.

## Decision cases — 2026-10-07

Parent instruction review in Codex; exact model version not recorded. These cases
evaluate the written boundaries, not independent agent or live tracker execution.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Draft a settled plan with headings, coupled steps and an explicit validation item | Group independent outcomes, retain validation, create no records | Parent rule review |
| Register a plan; matching task IDs already exist | Reuse confirmed IDs; create only absent outcomes after relevant records are recovered | Parent rule review |
| Shared files, no consumed output, no supplied priority | Invent neither serial dependencies nor priorities | Parent rule review |
| Implement a feature or revise an unresolved design | Do not substitute queuing for implementation or settle material choices | Parent routing review |
| Register tasks without a destination | Ask for the destination; do not select or install a tracker | Parent rule review |
| A write times out after two tasks were confirmed | Inspect the uncertain outcome before retry; preserve IDs and report partial progress | Parent rule review |
| Existing relevant tasks span several pages | Recover relevant pages before deciding absence; omit unrelated records | Parent rule review; execution not run |

## Input budget

No runtime helper: task formats, matching and pagination depend on the selected
tool. Use its scoped queries and reported omissions; no invented universal output
cap. Live duplicate detection, tracker failures and autonomous selection remain
unmeasured. Repository validation checks formats, catalogs and body limits.

## Environment

Linux/WSL, Codex parent review, 2026-10-07. No tracker selected or invoked.

## Results

Instruction boundaries reviewed. Mechanical verification is recorded after execution;
it does not establish tracker behavior or independent skill effectiveness.
