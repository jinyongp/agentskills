# git-commit evaluation

The instructions' Git procedures were replayed by scripts in temporary repositories.
Checks compare commit contents, HEAD, cached binary patches, and working-file bytes.
These results do not measure independent agent selection or judgment.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Typical request | "Split changes into task-based commits." Feature, test, new fixture, and independent documentation changes | Feature, test, and fixture in one commit; documentation in another | Replay passed. Two commits contain only their designated files; worktree clean |
| Restricted scope | "Commit only feature.txt." Excluded text, binary, and new files already staged; some have additional unstaged changes | Commit only feature.txt; preserve excluded index entries and working files | Replay passed. Excluded cached binary patch and working-file bytes unchanged |
| Staging only | "Stage feature.txt." | Change the index without creating a commit | Replay passed. HEAD unchanged; only the requested file staged |
| Message only | "Draft a commit message for staged changes." | Prepare a message through read-only inspection; preserve HEAD, index, and files | All three states unchanged after status, diff, and history inspection. Message quality not evaluated |
| Staged changes only | "Commit staged changes only." Same file also has unstaged changes | Commit the staged snapshot and preserve additional changes | Replay passed. Commit matches the original index snapshot; working-file bytes preserved |
| Hook failure | Scoped commit with a pre-commit hook that exits 1 | Report failure without bypassing the hook; restore excluded staging | Replay passed. HEAD unchanged, requested changes still staged, excluded patch and files unchanged |
| Missing input | "Commit changes" outside a Git repository | Fail repository detection without making changes | `git rev-parse --show-toplevel` failed; no staging or commit attempted |
| Out of scope | "Create a branch" or "Push to the remote" | Handle the requested operation without invoking this skill | Description and scope boundaries reviewed; automatic selection not evaluated |
| Repository message style | Commit in a repository using non-imperative subjects | Follow the established convention rather than imposing English imperative grammar | Parent instruction review only; message generation not independently evaluated |

## Replay setup

Separate temporary repositories covered commit grouping, restricted scope, hook failure,
and preparation. Each started with an initial commit on `main`.
The preparation fixture exercised staging, message inspection, and a staged-only commit
in sequence. Author identity and disabled signing were configured only in these fixtures.
Global and system Git configuration were excluded from the check process.

The restricted-scope fixture staged excluded files, then modified text and binary files again
so the index and working files differed. The replay followed these steps:

1. Save `git diff --cached --binary -- <paths>` and working-file bytes for excluded paths.
2. Temporarily unstage only those paths with `git restore --staged -- <paths>`.
3. Stage the requested file and run `git diff --cached --check`.
4. Commit using a temporary message file with `git commit -F <message-file>`.
5. Restore excluded staging with `git apply --cached <saved-patch>` after success or failure.
6. Compare excluded patches and files, and verify committed paths.

The hook-failure fixture used `exit 1` in its temporary `.git/hooks/pre-commit`.

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: instruction review and scripted replay in the current Codex session.
  Model version not recorded; independent agent evaluation not run.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, Node.js 22.22.2, skills CLI 1.7.0.

## Results

### Inspection helper verification

Conventional Commits guidance was added as a conditional reference for explicit requests
or repository conventions. Review against specification 1.0.0 covered feat/fix,
optional types, scopes, breaking changes, and footers. Imperative phrasing and the
72-character recommendation were distinguished from specification requirements.
This was document review; independent agent message classification and drafting were not evaluated.

Default inspection now runs `scripts/inspect_worktree.py`.
All 11 tests in `tests/test_git_inspection.py` passed against real temporary Git repositories
on Python 3.11.17 and 3.14.8. Individual CLI installation also verified byte-identical
references and scripts, and execution without extra dependencies.

- Default output excludes file contents and full diffs; HEAD, index, and files remain unchanged.
- Each JSON response stays within 4,000 characters with 140 Korean filenames and long diffs, history, and templates.
- Reading every file page recovers all 140 exact paths without duplicates or omissions.
- Concatenating selected diff pages reproduces Git's diff and distinguishes staged from unstaged changes.
- Rename source paths, spaces, newlines, glob characters, conflicts, and active merge state are preserved.
- Unborn and detached HEAD, linked worktrees, unset templates, and bounded errors for invalid inputs are handled.

These later helper checks are separate from the initial replay below.
Automatic selection and message quality still require independent evaluation.

### Initial replay

- `uv run --locked check.py`: format validation, the then-existing 27 tests, and CLI installation check passed.
- skill-creator's `quick_validate.py`: passed.
- Actual repository used as a local installation source; `--list` discovered `git-commit`.
- Installation into a temporary project with `--skill git-commit --agent codex --copy --yes`
  produced byte-identical `SKILL.md` and `LICENSE`.
- Git procedure replays passed. Automatic selection, message quality, and agent judgment
  with overlapping scopes require later independent evaluation.

Context review revision (2026-10-06): 3,381 body characters. Full verification of
44 skills and 76 existing tests passed. Creator validation and selective installation
passed; all six files matched, links resolved, and the MIT license stayed unchanged.

Filesystem-monitor regression: the existing read-only summary fixture configured a
marker-writing fsmonitor hook. It failed before the fix because inspection ran the
hook. Disabling it per query preserves the marker's absence, HEAD, index, worktree
content, and accurate change counts. Commit hooks are unaffected.
After the fix, all 76 tests and full repository verification passed. Selective
installation copied all six files exactly; format, license, and local links passed.
