# test-property evaluation

Instruction review and a parent-executed Hypothesis fixture cover domain selection,
independent invariants, shrinking, replay, and bounded reporting. Independent agent
property design and automatic routing were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Check sorting preserves multiplicity and ascending order | Assert independent properties across a meaningful generated domain | Native fixture generated integer lists and checked counts and adjacent ordering |
| Sort by dropping duplicate values | Find and reduce a defect-triggering input | Hypothesis found the counterexample [0, 0]; the faulty implementation violates multiplicity |
| Verify corrected sorting | Replay the counterexample and explore additional inputs | Corrected implementation passed replay and 100 generated examples |
| Copy production output or assert a law without justification | Establish the required invariant independently | Instruction review; the fixture properties follow the stated sorting contract |
| Restrict the domain merely to avoid a failure | Preserve the relevant failure region and disclose limits | Fixture included duplicates; its bounded illustrative domain was reported explicitly |
| A seed/cache is unavailable | Keep a concrete replay input and required state/version details | Counterexample replay directly invokes the property check; no example database was used |
| Apply properties at different boundaries | Select the cheapest useful boundary without duplicate suite layers | Instruction review; stateful integrations were not executed |
| Large shrink logs or unstable failures | Use bounded reports and preserve reproducible evidence | Fixture summary was 213 characters; large shrink logs and flakiness were not exercised |

## Native fixture

Domain: integer lists of length 0..6 with values -2..2.
Contract: output multiplicities equal the input and adjacent output values are ascending.
The faulty implementation used sorted(set(values)); the corrected implementation used sorted.
Hypothesis 6.168.3 find reduced a multiplicity failure to [0, 0].
The contract failed on that input for the faulty implementation and passed for the corrected
implementation. A separate generated check passed 100 corrected examples.

This demonstrates a selected invariant and replay procedure. It does not prove correctness
over all inputs or measure agent-authored test quality. The report explicitly records that
complete-domain proof is false. The run used a fresh isolated uv dependency environment
without changing repository dependencies; database replay was disabled for the fixture.

## Budget and basis

SKILL.md body: 3,791 characters including surrounding whitespace.
Native framework output limits must be checked for the chosen project; 213 characters
is a fixture measurement, not a universal Hypothesis output cap. No helper or framework
dependency is bundled in the installed skill.

[Hypothesis domain guidance](https://hypothesis.readthedocs.io/en/latest/explanation/domain.html)
and [failure replay guidance](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
informed domain preservation and reproducibility. The skill remains tool-neutral.
Generated state transitions, real integrations, long-running search, and large output
recovery were not executed.
Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.

All 20 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files
match their installed copies byte for byte. Local links and the MIT copy were checked.
