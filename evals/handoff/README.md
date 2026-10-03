# handoff evaluation

Instruction review and scripted snapshot replay were performed in this Codex session.
A fresh Python process inspected only a prepared packet and its shared fixture workspace.
This verifies mechanical state checks, not independent agent summarization, automatic
skill selection, or autonomous continuation.

| Scenario | Request | Expected result | Actual result |
| --- | --- | --- | --- |
| Typical handoff | "Prepare this feature task for another session." Staged and unstaged edits, an untracked file, and an unrelated user note | Carry intent, decisions, permissions, pending validation, exact state, and the next action | Packet fields reviewed; fresh-process snapshot checks passed without changing HEAD, index, or files |
| Resume stale state | "Continue from this packet." Feature file changed after preparation | Detect mismatch before editing and preserve newer work | Scripted mismatch detection passed; newer file bytes preserved |
| Separate workspace | "Resume elsewhere." Uncommitted changes exist only on the source machine | Require accessible worktree or patch/file snapshot; identify missing inputs | Portability instructions reviewed; cross-machine transfer not run |
| Out of scope | "Show task progress." No continuation requested | Give a progress update without a handoff or agent launch | Scope reviewed; automatic selection not evaluated |
| Missing context | Required attachment or artifact is inaccessible | Include essential content if available, otherwise identify the gap and obtain it before dependent work | Instructions reviewed; independent agent failure handling not run |
| Long context | Conversation includes superseded proposals, long logs, current decisions, and unresolved questions | Keep current decisions, necessary rationale, scope, and next action; retrieve bulky evidence only when needed | Canonical-state and targeted-inspection instructions reviewed; large-conversation agent evaluation not run |
| Pending external action | Source reports an unfinished remote operation | Confirm its outcome before retrying within current authorization | Resume instructions reviewed; live external actions not run |

## Replay setup

A temporary repository contained an initial commit on main, a staged feature edit,
additional unstaged edits in the same file, an untracked file, and an unrelated user note.
The packet recorded the repository, branch, HEAD, staged and unstaged binary patches,
untracked paths, and file contents as a small fixture snapshot. It also recorded intent,
a selected decision, local-only authorization, validation not yet run, and the next action.

A separate Python process read the packet and compared it with the actual repository.
The sender then confirmed unchanged staged content and working-file bytes.
After the feature file changed again, the receiver rejected the stale snapshot,
and the new contents remained unchanged. No historical conversation was supplied
to the checking process. No model inferred or executed the next action.

## Input budget

- Description: 177 characters; SKILL.md body: 3,680 characters.
- No bundled inspection helper or references: the task requires synthesizing current
  intent and evidence, rather than repeating a fixed mechanical inspection.
- Instructions require bounded, targeted checks and conditionally accessed evidence.
  They do not impose an arbitrary packet limit that could discard essential context.
- No runtime output cap or pagination contract applies to this skill.
  Default packet length and preservation under large conversations remain unmeasured.
- Replay verified preservation and stale-state detection in a small shared workspace.
  It does not establish complete context transfer across machines or agents.

## Environment

- Evaluation date: 2026-10-03 (Asia/Seoul).
- Agent and version: current Codex session; model version not recorded.
- Tools: Linux/WSL, Git 2.43.0, Python 3.11.17, Node.js 22.22.2, skills CLI 1.7.0.
- Replay used isolated temporary repositories; no user repository state or external services changed.

## Results

- `uv run --locked check.py`: six skills validated, all 40 tests and CLI installation checks passed.
- skill-creator's `quick_validate.py`, local documentation links, and the bundled MIT license passed checks.
- Actual repository discovery with skills CLI 1.7.0 found `handoff`.
- Selective installation with `--skill handoff --agent codex --copy --yes`
  produced byte-identical `SKILL.md` and `LICENSE`; an unselected skill was absent.
- Snapshot inspection and stale-state replay passed.
- Independent sender/receiver agent behavior, automatic selection, large-context
  fidelity, and live cross-session delivery remain unevaluated.
