# test-integration evaluation

Instruction review covers boundary selection and maintenance cost. Existing native CLI
installation checks provide a parent-executed integration example. Independent agent
test writing and automatic routing were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Check that the installation CLI copies a standalone skill correctly | Exercise actual CLI and consuming filesystem, not just mocked calls | Reused scripts/smoke_install.py and the actual selective installation check |
| Add tests for every calculation branch through a real database | Reuse isolated coverage unless the database adds distinct evidence | Instruction review; no new database branch matrix required |
| Assert a JSON key exists in a static document | Prefer appropriate schema validation; identify missing consumer semantics | Instruction review; schema presence alone is not an integration scenario |
| Verify committed persistence | Trigger through a stable entrypoint and read the consumer-visible result | Instruction review; no database experiment performed |
| Mock the entire dependency being tested | State that the actual boundary remains unverified | Instruction review; mocked success cannot establish real integration |
| Existing integration already protects the failure | Reuse it and add nothing redundant | Parent reviewed the existing CLI smoke check; no duplicate permanent test added |
| Missing service or tool | Report blocked integration, not a passing substituted test | Instruction review only |
| Shared resources or a failing test | Isolate owned data and preserve unrelated resources during cleanup | Policy review; service lifecycle not executed |
| Very large suite/log | Select relevant cases and bounded reports | Policy review; independent large-suite behavior not measured |

## Existing integration evidence

scripts/smoke_install.py invokes actual skills@1.7.0 against categorized fixtures,
checks discovery, selectively installs a skill into a temporary project, compares
the installed bundled files byte for byte, and rejects installation of the unselected
skill. This exercises the CLI and filesystem boundary without recreating the CLI.
TemporaryDirectory cleans up only the owned fixture project.

The new skill also receives actual selective installation verification.
These checks establish repository distribution behavior, not quality of agent-authored
integration tests for arbitrary products.

## Budget and environment

SKILL.md body: 3,476 characters including surrounding whitespace.
No bundled measurement, test-runner, or inspection script is needed: dependency setup
and native runner reports belong to the selected project and tooling. Instructions
require bounded selection; tool-specific limits must be verified when used.

Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11 and pinned skills@1.7.0 installation tooling.
Database, network, alternate frameworks, and cross-process failure cases were not run.

All 15 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files
match their installed copies byte for byte. Local links and the MIT copy were checked.
