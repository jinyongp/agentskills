# git-pr evaluation

PR change ranges and body-file preparation were replayed in a temporary repository,
and installed gh options were inspected. Public GitHub PR creation and updates were not run.
Automatic selection and independent agent title/body quality were not evaluated.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Change range | "Prepare the feature PR description." Independent main commit and feature commit | Describe only feature changes from the merge base | Replay passed. main...feature contains only the feature file; main..feature contains only the feature commit |
| Uncommitted changes | Additional unstaged feature edits and a new untracked file | Exclude these changes from the PR description; preserve files | Both excluded from comparisons. HEAD and working files preserved |
| Body preparation | Multiple paragraphs, backticks, and $(...) in the body | Write a file preserving actual newlines and literal characters | Temporary body file preserves newlines and literal characters |
| Publishing options | Explicit create/edit command options | Specify target, base, head, title, and body file where supported | Options verified in local gh create/edit help; no remote writes |
| Existing PR | "Create a PR for this branch" with a matching open PR | Find the existing PR without creating a duplicate | Instructions reviewed; GitHub queries and independent agent evaluation not run |
| Out of scope | "Review this PR's code." | Handle as code review | Boundaries reviewed; automatic selection not evaluated |
| Authentication failure | "Create a PR" without write access | Prepare the body and explain the failure | Actual authentication failure and independent agent evaluation not run |

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: current Codex session, model version not recorded; scripted replay.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, skills CLI 1.7.0, GitHub CLI 2.102.0.

## Results

`uv run check.py validate` and skill-creator's `quick_validate.py` passed.
At initial evaluation, `uv run --locked check.py` passed validation of all five skills,
the then-existing 27 tests, and CLI installation checks.
Local catalog/documentation links and per-skill MIT notices were also checked.
CLI discovery and selective installation of the actual skill produced byte-identical
`SKILL.md` and `LICENSE`.

The fixture branched feature from main, added a feature commit, and added an independent
documentation commit to main. With unstaged and untracked changes on feature, it checked
two-dot log and three-dot diff output. Preparation required no remote access.

GitHub PR creation, editing, duplicate queries, readback, authentication failures,
and independent agent writing quality were not evaluated.
Live write evaluation requires an explicitly requested task in a separate test repository.
