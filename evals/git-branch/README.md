# git-branch evaluation

The Git procedures were replayed by scripts in isolated temporary repositories.
Automatic selection and independent agent judgment were not evaluated.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Create | "Create and switch to feature/example from the current work." Staged, additional unstaged, and new files provided | Create the branch while preserving HEAD and existing work | Replay passed. HEAD, cached binary patch, and working files unchanged |
| Rename and delete | Rename the new branch, return to main, and delete the local branch | Change only the requested refs; preserve work | Replay passed. Rename, deletion, and staging preservation verified |
| Duplicate name | "Create a branch with the same name." Branch already exists | Stop without overwriting the existing branch | `git switch -c` failed; HEAD preserved |
| Other worktree | "Switch to occupied." Branch is checked out in another worktree | Report switch failure; preserve work | Switch rejected. Current branch and cached patch unchanged |
| Out of scope | "Push this branch to the remote." | Handle as remote synchronization | Boundaries reviewed; automatic selection not evaluated |
| Missing input | "Create a branch from a different base." Base unspecified | Ask for the base before creating | Independent agent evaluation not run |

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: current Codex session, model version not recorded; scripted replay.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, skills CLI 1.7.0.

## Results

`uv run check.py validate` and skill-creator's `quick_validate.py` passed.
CLI discovery and selective installation from the actual local repository produced
byte-identical `SKILL.md` and `LICENSE`.

The fixture exercised creation at HEAD, switching, renaming, and deletion of a merged
local branch, plus duplicate creation and switching to a branch occupied by another worktree.
Checks verified work preservation and Git failure results.
Remote changes, forced deletion, and independent agent evaluation were not run.
