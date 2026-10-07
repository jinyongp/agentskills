# Review-loop evaluation

Parent instruction review on 2026-10-07; model version not recorded. These cases
assess decision boundaries, not independent execution or automatic activation.

| Condition | Expected decision supported by the rules |
| --- | --- |
| Plain review request | Return findings without fixes |
| Explicit review-and-fix | Confirm eligible defects and apply authorized corrections |
| Areas A, B, C; A has no findings | Continue B and C; pending areas block completion |
| Fix B changes a contract consumed by A | Reopen A; finish pending C |
| Independent B fix; A evidence still valid | Recheck B without restarting unchanged A |
| Agreed simulated payment preview | Keep simulation; do not install a provider |
| Preview falsely claims real payment success | Trace the disclosure contract; repair within scope or resolve conflict |
| Missing persistence, with no known requirement | Recover decisions; clarify if eligibility depends on the answer |
| Accepted supported subset works | Retain it without generalized extension points |
| Concrete exposure of private data in current flow | Trace the reachable violation and resolve a scoped correction |
| New fallback seems useful | Keep it outside fixes unless requested |
| Fix requires a revised public contract | Resolve that decision before dependent edits |
| A reviewer or required check is pending | Report incomplete coverage or validation |
| A-to-B-to-A correction | Resolve competing assumptions before another edit |
| No delegation capability | Perform sequential coverage |
| Large or inaccessible target | Inspect bounded relevant pages; report missing coverage |

## Input budget

No inspection script is bundled. The workflow coordinates decisions and coverage;
native scoped searches/diffs and existing bounded tools supply mechanical evidence.
Its inline ledger contains only area, status, target state, and useful evidence.
Large-output limits and pagination are tool-specific, not implemented here.
Report omissions and retrieve required detail; unavailable areas remain blocked.
The skill is independently installable with its contract reference.

## Evidence limits

Parent-authored fixtures or rule review cannot establish independent agent behavior,
improvement caused by this skill, or exhaustive defect discovery. No permanent
wording, scenario-quota, or mandatory delegation tests were added. Runtime checks
and installation evidence are recorded after actual execution.

## Parent fixture execution

An authored disposable Python fixture had three requested areas. A was a working
local preview with explicitly accepted manual export; B computed price plus quantity
instead of their required product; C charged shipping at an inclusive free-shipping
threshold. Expectations were derived from a separately written fixture contract.
`python3 check.py A`, `B`, and `C` exited 0, 1, and 1 before correction. Review
continued after clean A; only B's operation and C's comparison were corrected.
Rechecks exited 0 for B, C, and A. A's source remained byte-for-byte unchanged;
no automated export or external integration was added.

Source and before/after logs are disposable at
`/tmp/agentskills-review-scope-fixture/`; that path is not a durable artifact or an
installed dependency. This parent-authored replay illustrates continued coverage and
scope preservation, not independent discovery or an effect caused by the skill.

## Packaging verification

Full `uv run --locked check.py` passed: 50 skill formats/catalogs, 76 existing tests,
and CLI discovery/selective-installation fixtures. All 12 affected skills were
installed individually with skills@1.7.0; bundled file bytes, local links, body
budgets, and saved-record fragments passed. The new skill's MIT file was added
after that run; its final selective installation was repeated separately.
