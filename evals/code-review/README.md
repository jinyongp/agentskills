# code-review evaluation

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
