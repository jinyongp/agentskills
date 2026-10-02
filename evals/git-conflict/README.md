# git-conflict evaluation

Merge, rebase, and cherry-pick conflicts were replayed in separate temporary repositories.
Two branches changed the same line differently; a planned resolution combining both meanings
was written manually. Automatic selection and agent resolution judgment were not evaluated.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Merge conflict | "Resolve the conflict preserving both sides and finish the merge." | Inspect base/current/other versions, apply the planned result, complete merge | Replay passed. Result contents and two parent commits verified |
| Rebase conflict | "Resolve and finish this rebase onto main." | Identify stage 2 as main and stage 3 as the feature commit being replayed | Replay passed. Stage contents and result verified; main is an ancestor of feature |
| Cherry-pick conflict | "Resolve this cherry-pick conflict and continue." | Resolve the commit and continue only the cherry-pick | Replay passed. Planned result and one parent commit verified |
| Unresolved state | Attempt each operation's --continue before resolving | Fail while preserving conflicts and HEAD | All three operations rejected continuation; HEAD and unmerged paths unchanged |
| Unrelated file | Untracked file present during each conflict | Preserve the file through resolution and completion | Bytes unchanged; file remains untracked |
| Out of scope | "Pull the latest main" without a conflict | Handle as synchronization | Boundaries reviewed; automatic selection not evaluated |
| Ambiguous meaning | Mutually exclusive requirements without user intent | Ask for the necessary decision and retain the conflict | Independent agent evaluation not run |

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: current Codex session, model version not recorded; scripted replay.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, skills CLI 1.7.0.

## Results

`uv run check.py validate` and skill-creator's `quick_validate.py` passed.
CLI discovery and selective installation of the actual skill produced byte-identical
`SKILL.md` and `LICENSE`.

Each fixture compared :1, :2, and :3 contents and verified that unresolved continuation
failed. Resolution then used file editing, explicit staging, `git diff --cached --check`,
and the matching operation's `--continue`. Final files, commit structure, and unrelated
untracked files were checked.

Binary, rename, deletion, repeated multi-commit conflicts, project-generated files,
unrelated pre-existing staging, and independent agent judgment were not evaluated.
