# git-worktree evaluation

Seven tests use real isolated Git repositories and linked worktrees.
They replay lifecycle operations and read-only inspection without touching user remotes.
Independent agent path selection, permission decisions, and routing are not evaluated.

| Scenario | Expected result | Observed coverage |
| --- | --- | --- |
| Create and remove a clean linked checkout | Preserve dirty parent work; retain local branch | HEAD, cached patch, working and untracked files compared before/after |
| Locked detached checkout with newline path/reason | Exact registry fields; normal removal refusal | Path and reason preserved; locked target remains |
| 21 registered worktrees with Unicode paths | Bounded pages recover every exact path | Records reassembled without shortening or duplication |
| Dirty target removal | Git refuses; file bytes preserved | Untracked data remains unchanged |
| Rename and active merge marker | Correct counts and operation signal | Selected-state fixture verifies both |
| Ignored local data in an otherwise clean checkout | Expose data before removal | Count and exact ignored-file page verified; contents unchanged |
| Unregistered path or invalid query | Bounded failure and unchanged registry | Failure cases return errors without mutation |
| Registry prune, move, or repair | Inspect actual targets and applicable scope | Conditional reference reviewed; repair/prune lifecycle not replayed |

## Input budget

Default output contains registry counts only. List, state, and ignored-file reports
are capped at 4,000 characters, including escaping and newline. Paged lists expose
totals, omissions, and next offsets. State queries inspect only a registered checkout.
The helper performs no mutations and does not enable configured filesystem monitor commands.
It reports ignored files separately from Git dirty state.

## Environment and limits

2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Linux/WSL, Python 3.11+, Git 2.43.0; isolated fixtures.
Forced removal, submodule removal, live job detection, and independent agent decisions
remain untested.

Twelve skills validated; all 67 tests and CLI installation checks passed.
Creator validation and actual selective installation passed; all four bundled files match.
Local documentation links, English documentation, and MIT notices passed checks.

## Bisect state regression — 2026-10-15

- Revision: uncommitted working tree based on 4d972c2103595674f2d84d7552da861b9a66e4b0.
- A clean linked checkout running bisect previously reported no active operation.
  A disposable reproduction confirmed that ordinary worktree removal could then
  delete that checkout and its bisect state. Git cleanliness is insufficient here.
- The inspector now recognizes BISECT_START. Instructions treat active operations
  as checkout use and require authorization covering state loss before removal.
- The real-bisect regression failed before the fix and passed afterward. Inspection
  preserves HEAD, index bytes, and BISECT_LOG; reset restores an empty operation list.
- Eight focused worktree tests passed. Full verification passed 66 skill formats,
  164 tests with one Windows-only skip, and skills CLI/packed CLI installation checks.
- This proves operation detection and state preservation, not independent agent
  removal judgment. Forced removal, live jobs, and Windows remain untested here.
