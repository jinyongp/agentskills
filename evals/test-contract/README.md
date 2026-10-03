# test-contract evaluation

Instruction review covers consumer expectations and provider verification. No real
API/message provider or independent agent test authoring was exercised.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Verify consumer/provider compatibility | Identify interface and supported versions; verify both expectation and conformance | Instruction review; no provider verification was run |
| Snapshot every provider field | Require independently justified consumer constraints | Instruction review; observed current output alone is insufficient |
| Verify a declarative JSON shape | Reuse an adequate existing schema check | Instruction review; no duplicate runtime schema assertions required |
| A mock or generated pact file passes | State that actual provider verification remains pending | Instruction review; no false compatibility claim |
| A required field/error code changes | Retain the exact consumer contract and relevant version checks | Instruction review |
| A provider adds a field | Check the actual consumer compatibility rules | Instruction review; extra fields are not assumed universally safe |
| Infrastructure is missing or version scope is unknown | Report unverified combinations and resolve blocking expectations | Policy review only |
| Large verification reports | Inspect bounded summaries and selected mismatches | Policy review; large-contract behavior not measured |

## Basis and limits

[Pact's consumer/provider explanation](https://docs.pact.io/getting_started/how_pact_works)
informed the distinction between consumer expectations and provider conformance.
The skill is tool-neutral and does not require Pact, brokers, publication, or a new service.

SKILL.md body: 3,505 characters including surrounding whitespace.
No universal contract generator or inspection script is bundled: the project selects its
authoritative interface and native verifier. Format validation is not compatibility proof.
Protocol evolution, real consumer parsing, provider state, and independent routing
remain unexecuted. No new permanent test or testing dependency was added.
Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11 and skills@1.7.0 are maintenance verification tools only.

All 18 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files
match their installed copies byte for byte. Local links and the MIT copy were checked.
