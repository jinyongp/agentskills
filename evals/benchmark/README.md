# benchmark evaluation

Instruction review and a parent-executed native benchmark replay cover the cases below.
Independent agent execution, automatic routing, and performance gains for real projects
were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Compare two implementations on the same input | Check correctness, match conditions, repeat measurements, retain raw results | Both returned 2,646,700; three worker processes collected nine measured values per version after warmup |
| Use a specified tool | Follow the user's tool and explain unsupported metrics before substitution | Instruction review; replay used pyperf explicitly, not a required skill dependency |
| Tool reports instability despite a significant comparison | Preserve warnings and limit the conclusion | Both runs warned about insufficient samples; observed difference is a fixture demonstration, not an established stable improvement |
| Compare a large suite but inspect one case | Select the case and state omitted counts; retain the rest | Native filtering returned one of 201 cases; 200 omitted cases remain in each complete result file |
| Baseline result is missing | Fail visibly; keep existing results intact | Native comparison failed with a nonzero exit; original result files remained available |
| Memory measurement, a zero baseline, or mismatched workloads | Use the actual memory definition; avoid undefined percentages or invalid comparisons | Instruction review only; these modes were not executed |
| Evaluate agent answer quality or check correctness only | Use criteria appropriate to that task | Scope review; automatic selection not tested |

## Replayed measurement

Baseline: `sum(i*i for i in range(200))`.
Candidate: `sum([i*i for i in range(200)])`.
Both use the same Python runtime, input, host, and measurement configuration.
Each was run with pyperf `timeit --name sum-squares --processes 3 --values 3
--warmups 1 --min-time 0.01 --output <fresh-result.json>` and its statement.
This short run is for procedure verification, not a production benchmark.

Native `compare_to --verbose --benchmark sum-squares` reported means of
4.05 microseconds and 3.16 microseconds, with standard deviations of 0.36 and
0.13 microseconds. Its significance test reported a difference, while both measurement
logs warned that more samples were needed for stability. Stable practical improvement
remains inconclusive. No system tuning or implementation change was performed.

## Input budget

- SKILL.md body: 3,464 characters including surrounding whitespace.
- Native selected comparison: 116 characters; complete measurement files: 3,458 and
  3,461 bytes. Run warnings remain in the original logs and are included in the conclusion.
- Synthetic large-suite files: 76,086 and 81,284 bytes, each with 201 cases. The additional
  cases reuse fixture samples solely to test selection; they are not new measurements.
  A selected comparison used 128 characters, with one selected / 201 total / 200 omitted.
- Large files remained outside default agent input. Native result loading recovered
  all nine measured values for each real case. Selected cases retain their exact names.
- These measured sizes are fixture results, not a guaranteed output cap for pyperf or
  other tools. The skill requires bounded selection or a tested reducer when needed.

There is no bundled measurement wrapper or universal result schema. The selected
tool supplies timing, calibration, export, and comparison. Native capabilities and
output limits must be checked for each tool; a future reducer needs its own tests.

## Environment and verification

Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11.17, pyperf 2.10.0, WSL2 Linux x86_64, AMD Ryzen 7 9800X3D.
pyperf was supplied through an isolated uv invocation; repository dependencies were unchanged.
Memory, throughput, cold starts, other harnesses, and complete pagination were not executed.

All 13 skills validated; all 67 repository tests and CLI installation checks passed.
Creator validation and actual selective installation passed; both bundled files match
their installed copies byte for byte. Documentation links and the MIT notice were checked.
