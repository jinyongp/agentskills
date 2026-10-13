# debug evaluation

## Evidence and proportional workflow — 2026-10-13

Parent instruction review in Codex; model version not exposed. No independent
diagnosis, review or live PR operation was executed for these cases.

| Scenario | Expected decision |
| --- | --- |
| Successful exit hides wrong business output | Reproducer verdict checks the exact symptom |
| Minimization changes the failure to a setup error | Keep the original failure case; do not diagnose the substitute symptom |
| Temporary logs isolate a cause | State probe prediction, verify original unreduced case after fixing, remove owned instrumentation |
| Production-only issue cannot reproduce locally | Keep hypotheses explicit and evidence gaps visible; no invented reproduction |

Two fixture tests replay reproduction and a scoped correction through the standalone
runner. They do not evaluate independent agent diagnosis or automatic selection.

| Scenario | Expected result | Observed coverage |
| --- | --- | --- |
| Empty input fails an arithmetic function | Capture the actual failure without changing source | Baseline log contains ZeroDivisionError; source bytes unchanged |
| Correct the demonstrated cause | Original reproducer passes; unrelated work preserved | Corrected fixture passes and user note remains byte-identical |
| Arguments contain spaces and shell syntax | Pass arguments literally | Log contains the original argument; shell side effect absent |
| Symptom does not reproduce or cause remains uncertain | Keep the gap explicit rather than claiming a fix | Instruction review only |
| Diagnosis-only request | Report cause and proposal without editing source | Scope review only |
| Large output, timeout, launch failure, or existing log | Bounded report and recoverable evidence | Bundled runner uses the same standalone implementation exercised by verify execution tests; debug-specific replay also runs it |

## Input budget

The runner caps JSON reports at 4,000 characters including escaping and newline.
Full output remains in a new log; detail pages expose byte offsets and omissions.
The script is bundled locally and needs no other installed skill.
Selecting useful hypotheses, log excerpts, and regression checks remains an agent task.

## Environment and limits

2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Linux/WSL, Python 3.11+; isolated fixture files, no user repository or remote changes.
Independent root-cause discovery, intermittent failures, and large-context diagnosis
remain unevaluated.

Eleven skills validated; all 60 tests and CLI installation checks passed.
Creator validation and actual selective installation passed; all three bundled files match.
