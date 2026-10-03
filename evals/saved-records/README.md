# Saved-records convention verification

Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
This is an authoring-policy and parent-executed fixture check, not an independent
agent evaluation or a new installable skill.

| Case | Expected behavior | Observed result |
| --- | --- | --- |
| Existing skills installed independently | Carry the record convention without a shared runtime dependency | All 13 entrypoints contain the canonical fragment; largest body is 3,949 characters |
| Prepare a new skill | Include the convention; generate no workflow records | Isolated preparation passed; no .agents folder created |
| Install verify and debug separately from other skills | Preserve bundled files; create no task records during installation | Actual skills@1.7.0 selective installation passed; all bundled files match byte for byte; no artifacts folder created |
| Use a shared run ID | Keep separate skill destinations within one run | Installed helpers saved separate verify/check.log and debug/check.log files under one run |
| Spaces and Unicode in the target root | Return exact log paths without shortening | Both reports returned the complete selected path; JSON reports stayed within 4,000 characters |
| Existing log or run directory | Preserve existing records | Re-running each helper refused the existing log without changing its bytes; exclusive directory creation rejected a collision |
| Local artifact records in this repository | Respect the declared ignore rule | git check-ignore confirmed the artifact path is excluded |

The fixture used a fresh temporary project and explicit record paths. It did not
change other projects' ignore rules or commit logs. Python 3.11 and the installed
verify/debug command runners were used; the installation CLI was skills@1.7.0.

All 13 skill formats, 67 repository tests, and CLI smoke checks passed. Existing
generation tests cover valid scaffolding, format budgets, and rollback after failures.
No tests asserting documentation wording were added.

Tool-native benchmark exports, persisted handoff packets, automatic run-ID selection,
cross-agent ID sharing, and independent agent routing were not executed here.
The convention guides the agent; it is not a filesystem enforcement layer.
