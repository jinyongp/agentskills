# Animation performance evaluation

| Scenario | Request | Expected result | Parent review |
| --- | --- | --- | --- |
| Web stalls | Improve frame pacing in a selected drawer | Capture baseline, attribute cost, compare matched runs | Evidence precedes optimization |
| High refresh rate | Judge a 120Hz interaction | Use actual frame deadlines and slow intervals | No universal 60fps pass |
| Native input delay | UI moves smoothly but taps respond late | Separate JS-owned response from UI/rendering work | Pipeline ownership retained |
| Simulator only | Claim release-device improvement from debug preview | State limits and request relevant evidence | No physical-device claim |
| No runtime | Only source and screenshots available | Return hypotheses and capture plan | No invented measurement |
| Small gain | Change is smaller than run variability | Report inconclusive comparison | Noise governs conclusion |
| Tool choice | Existing profiler already supports the workload | Reuse it and installed APIs | No compulsory profiler installation |
| Measurement only | Profile without implementation changes | Return bottleneck evidence and recommendation | Scope honored |
| Adjacent task | Choose a nicer easing without stalls | Outside performance scope | Taste separated from costs |
| Large trace | Multi-minute export for a brief stall | Select interval, retain omissions and recover needed events | No complete-analysis claim from sample |

## Input budget

No generic trace parser is bundled: formats and metric semantics depend on project
profilers. Use their bounded queries and selected intervals. Read only the applicable
platform reference. Tool-output limits, trace recovery, and failed captures were not
measured; helper size/failure tests do not apply. No tests pin wording or duplicate
existing format validation.

## Environment

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.

## Results

Parent review assesses written decisions, not independent agent execution. No browser
or device performance was measured. Automatic selection, real-project optimization,
and trace handling remain unverified.

Body: 3,734 characters. Full locked verification passed: 37 skills, 76 tests, and
CLI fixtures. Creator validation, exact four-file selective installation, upstream
MIT comparison, saved-record fragment, and local documentation links passed.
