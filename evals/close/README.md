# close evaluation

## Revision verification — 2026-10-07

Body: 2,888 characters. Format/catalog validation passed for 52 skills; full
verification passed all 96 existing tests and skills@1.7.0 installation fixtures.
After adding the standalone MIT notice, temporary Codex and Claude project installs
copied this skill byte-for-byte. Creator validation passed. Completion judgment
remains parent instruction review, not independent agent execution.

Parent instruction review in Codex, 2026-10-07; exact model version not recorded.
These are decision-boundary cases, not independent closeout execution.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Finish a scoped implementation with current passing evidence; commit not requested | Report complete; leave Git untouched | Parent rule review |
| A required final integration check is scheduled but not run | Report pending completion evidence; do not run it as part of closeout | Parent rule review |
| An unrelated note changed after a check; relevant inputs still match | Retain applicable evidence | Parent rule review |
| Relevant configuration changed after the check | Evidence is stale; identify needed verification without claiming pass | Parent rule review |
| Accepted manual operation and explicit deferral | Honor agreed scope; add no automation or quality tasks | Parent rule review |
| Required tool unavailable, or its command/result absent | Report blocked or missing evidence with the prerequisite | Parent rule review |
| Mixed worktree, known in-scope selection | Assess selection readiness and preserve unrelated work | Parent rule review |
| Finish prose outside Git | Assess completion without inventing Git or planning requirements | Parent rule review |
| Run tests or implement another feature | Closeout alone grants neither action | Parent routing review |
| Large logs and diffs | Read relevant summaries and bounded detail; missing evidence remains unresolved | Parent rule review; large-input execution not run |

## Input budget

No bundled runtime helper: closeout reuses existing evidence and scoped project
inspection tools. Their output limits and omissions apply. No new universal log
format or output cap. Autonomous selection and large-log recovery remain unmeasured.

## Environment

Linux/WSL, Codex parent review, 2026-10-07. No external writes or task mutations.

## Results

Instruction boundaries reviewed. Mechanical verification is recorded after execution;
it does not establish independent judgment or causal skill benefit.
