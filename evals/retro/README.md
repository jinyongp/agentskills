# Retro evaluation

## Decision cases — 2026-10-13

Parent instruction review in Codex; model version not exposed. No independent
agent execution or comparative improvement is claimed.

| Session evidence / request | Expected result | Review result |
| --- | --- | --- |
| Agent repeatedly searches for an existing check command | Improve the relevant pointer, not invent another check | Navigation and reuse rules apply |
| Existing CI check is defined but never invoked; missed error matches it | Propose fixing wiring and replay the failure if edits authorized | Existing mechanism inspected first |
| Small project has no pre-commit hook; no related failure observed | No finding based on hook absence alone | Evidence threshold retained |
| Test already detects the reported failure | Reuse it; no duplicate regression test | Named uncovered failure required |
| Reviewer filled a deliberately excluded feature | Preserve scope; clarify the decision source rather than build the feature | Tradeoff and instruction rules apply |
| One session did not need a safety instruction | No removal based solely on non-use | No-op evidence bounded |
| Review session; do not change global settings | Inline proposals only | Authorization boundary explicit |
| Old session log inaccessible or huge | Recover relevant spans if available; report missing evidence and redact secrets | No whole-log dump or invented timing |

## Input budget and limits

No new inspection helper or fixed external log format. Use available indexes,
filters and bounded pages, with coverage gaps explicit. Large-log retrieval, live
configuration edits, agent selection and productivity effects remain unmeasured.
Repository checks verify format/packaging separately; no wording test is added.
