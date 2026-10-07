# verify evaluation

## Decision clarity review — 2026-10-07

Parent instruction review; model version not recorded.
Paired case: A changed serializer hidden behind mocks needs real-boundary evidence;
matching existing evidence can be reused.
The revised rule states the evidence and resulting decision while preserving the
contrasting valid case. This is rule review, not independent task execution or a
measured quality improvement. Earlier verification results below are historical.

Script checks validate execution and reporting, not independent agent check selection.

| Scenario | Expected result | Observed result |
| --- | --- | --- |
| Successful noisy check | Bounded summary and complete log | Fixture tests cover success and 120,001 bytes of output |
| Check exits 7 | Failure, original exit status, readable evidence | Failure fixture reports fail and preserves output |
| Unicode, control, and invalid bytes | Bounded pages recover the original log | Pagination fixture compares reassembled bytes |
| Timeout with a child process | No pass; process group stopped | Timeout fixture checks absence of delayed child writes |
| Existing log or missing executable | Preserve evidence; report a bounded error | Existing-log and launch-failure fixtures cover both |
| Wrong skill or missing task scope | Keep validation separate from implementation; clarify blocking scope | Instruction review only; routing not evaluated |
| Bug already has sufficient coverage | Reproduce and verify with existing checks; add an edge case only for a distinct gap | Parent instruction review only; no automatic new test requirement |

## Input budget and limits

The optional runner emits at most 4,000 characters per JSON report, including escaping
and newline. Default output contains status, log location, and byte count, without
command output or arguments. Detail pages provide exact byte offsets and omission
counts; surrogateescape preserves non-UTF-8 bytes. Full output remains on disk.
Check commands themselves may mutate their environment; selecting and authorizing
them remains the agent's responsibility.

## Validation

- Six execution tests use actual subprocesses, logs, and an isolated temporary workspace.
- Repository validation of seven skills, all 46 tests, and CLI installation checks passed.
- skill-creator validation and actual selective installation passed; all three bundled files match.
- Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
- Independent check selection, browser/database behavior, and automatic routing remain untested.

Context review revision (2026-10-06): 3,086 body characters. Full verification of
44 skills and 76 existing tests passed. Creator validation and selective installation
passed; all three files matched, links resolved, and the MIT license stayed unchanged.
