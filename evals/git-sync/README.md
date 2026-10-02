# git-sync evaluation

Procedures were replayed with a local bare remote and two working repositories.
No writes were made to GitHub or user remotes.
Automatic selection and independent agent judgment were not evaluated.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Behind remote | "Pull remote changes." One remote-only commit | Fetch, identify 0 ahead / 1 behind, and fast-forward | Replay passed. Local HEAD matches the remote commit |
| Push | "Push the current branch." Local commit, annotated tag, and push.followTags=true | Update only the requested remote branch; leave tags unchanged | Push with `--no-follow-tags` and an explicit refspec succeeded; remote tag absent |
| Diverged | One independent commit on each side | Identify 1 ahead / 1 behind; stop without unauthorized merge, rebase, or force-push | ff-only update and normal push both failed; local and remote commits unchanged |
| Fetch during work | "Fetch" with local files staged | Update refs while preserving HEAD and index | Replay passed. HEAD and cached binary patch unchanged |
| Out of scope | "Commit current changes." | Handle as commit preparation | Boundaries reviewed; automatic selection not evaluated |
| Authentication or connection failure | "Pull" when the remote is inaccessible | Explain failure; do not integrate using stale refs | Independent agent and network-failure evaluation not run |

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: current Codex session, model version not recorded; scripted replay.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, skills CLI 1.7.0.

## Results

`uv run check.py validate` and skill-creator's `quick_validate.py` passed.
CLI discovery and selective installation of the actual skill produced byte-identical
`SKILL.md` and `LICENSE`.

After pushing an initial commit to main on the temporary bare remote, the two working
repositories exercised remote-only changes, local-only changes, and divergence.
Checks verified that failed normal pushes and ff-only updates preserved existing commits.
Force-push, public remote authentication, network failures, and independent agent evaluation
were not run.
