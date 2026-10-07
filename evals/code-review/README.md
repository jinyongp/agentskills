# code-review evaluation

## Accepted-scope review — 2026-10-07

Parent instruction review; model version not recorded. Paired case:
A missing optional capability stays outside findings; a demonstrated regression
within the agreed subset remains actionable.
The revised rules recover agreed limits before judging gaps. This is not independent
agent execution. Repository checks and actual selective installation passed for this
revision; earlier results below retain their original scope.


## Balanced design cases

Parent instruction review of the revised skill and conditional design reference.
These cases do not measure independent defect discovery or severity judgment.

| Shared review target | Excess-design case | Incomplete-design case | Expected decision |
| --- | --- | --- | --- |
| Upload with an accepted retry contract | Unused layers create demonstrable setup/coupling cost | Failed submission leaves the user unable to retry | Separate evidenced engineering cost from the reproducible behavior defect |
| Resource-owning wrapper with one caller | Wrapper duplicates ownership and creates parallel edits | Removing it leaks the resource on exceptions | Judge responsibilities/lifecycle, not usage count |
| Standard/native feature or maintained library | Dependency has no capability benefit and adds concrete integration cost | Removing it breaks a required platform or access behavior | Compare alternatives against identical requirements |
| Complete feature or accepted prototype | Generalize for hypothetical consumers | Call a missing accepted workflow complete | Evaluate the actual agreed scope; no full-product requirements for a prototype |
| Readable complete patch | No material extra cost is established | No missing behavior or failure is established | No finding is valid; avoid forced issues and severity inflation |

Counts, preference and speculative future scale alone do not establish a defect.
Engineering observations need concrete evidence and stay separate from defects.
Full verification passed for 49 skills and 76 existing tests, including CLI
discovery/installation fixtures. Creator validation and actual individual
installation with skills@1.7.0 passed: all four bundled files matched byte-for-byte.
Body: 3,690 characters. Local runtime links resolve within this skill, saved-record
guidance is unchanged, and MIT is preserved. No runtime helper was changed.
These checks establish packaging, not independent review judgment.

## Earlier evaluation

Helper tests inspect actual temporary Git repositories. A separate parent replay
reviews a small arithmetic regression and confirms its trigger.
These results do not measure independent agent defect discovery or automatic routing.

| Scenario | Expected result | Coverage |
| --- | --- | --- |
| Staged, unstaged, and untracked work | Distinguish layers without mutation or default diff dumps | Actual Git fixture compares HEAD, cached patch, and file bytes |
| Commit comparison with dirty local work | Pin commits; exclude unrelated dirty files | Comparison fixture verifies IDs and exact file scope |
| Diverged feature and base branches | Compare from merge-base when selected | Independent base-only changes excluded |
| 140 unusual paths and long Unicode diff | Exact bounded pagination | Reassembled paths and diff compared with Git |
| Configured external diff | Inspect without executing external drivers | Marker-writing driver remains unexecuted |
| Invalid refs, paths, pages, or repository | Bounded error; no partial completeness claim | Failure fixtures cover invalid inputs |
| Removed empty-input guard | Report a reproducible regression with a changed-code location | Parent replay confirms ZeroDivisionError on an input previously supported |
| Adjacent request to implement a fix | Keep edits outside review scope unless authorized | Instruction review only |
| Patch adds tests that pin private helper names | Verify actual contract and concrete breakage or policy cost; report supported brittleness | Parent instruction review only |
| Similar tests exercise real wiring at different boundaries | Keep useful independent evidence; similarity alone does not establish duplication | Parent instruction review only |

## Budget and limitations

JSON responses are capped at 4,000 characters, including escaping and newline.
Default output reports layer counts and resolved comparison IDs. Exact paths and
selected diffs are paged with totals and omissions; untracked content is read separately.
Comparisons are endpoint-based unless merge-base is selected. Renames appear as
delete/add paths, and submodule/binary interpretation requires additional evidence.

## Environment

2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Linux/WSL, Python 3.11+, Git 2.43.0; isolated fixtures, no remote writes.
Independent severity judgment, large-project review coverage, and automatic routing
remain untested.

Ten skills validated; all 58 tests and CLI installation checks passed.
Creator validation and actual selective installation passed; all three files match.

Context review revision (2026-10-06): 3,312 body characters. Full verification of
44 skills and 76 existing tests passed. Creator validation and selective installation
passed; all three files matched, links resolved, and the MIT license stayed unchanged.

Filesystem-monitor regression: the existing external-diff fixture also configured a
marker-writing fsmonitor hook. It failed before the fix because diff inspection ran
the hook. Inspection now disables it per query without changing repository config.
The fixture checks that both external-driver and fsmonitor markers stay absent.
After the fix, all 76 tests and full repository verification passed. Selective
installation copied all three files exactly; format, license, and local links passed.
