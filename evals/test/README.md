# test evaluation

Instruction review covers test-admission decisions and their exceptions.
Independent agent execution, automatic routing, and suite-pruning quality were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Add another test for existing-log preservation | Reuse sufficient coverage rather than duplicate it | Parent inspected test_existing_log_is_preserved in tests/test_check_execution.py; it already checks rejection and unchanged log content |
| Add a regression test for every edit | Identify a meaningful gap before adding lasting coverage | Principle review; no blanket per-change requirement |
| Check a class name, private helper name, or source literal | Require an observable contract; preserve refactoring freedom | Principle review; source-layout assertions have no automatic justification |
| Verify a static disabled attribute or accessible name | Test the required interaction or accessibility semantics at a suitable boundary | Principle review; literal/attribute checks remain valid when contract-relevant |
| Assert every key and nesting level in a DSL file | Reuse a suitable schema for shape and check missing consumer semantics | Principle review; no hand-written duplicate schema required |
| Protect a public error code or protocol shape | Retain exact compatibility assertions where consumers depend on them | Principle review; stable contracts are not weakened for convenience |
| Test every input combination across all layers | Choose distinct failure mechanisms and additional integration evidence | Principle review; exhaustive/repeated coverage needs a supported risk |
| Enforce current file layout without a project rule | Preserve implementation freedom | Principle review; an explicit dependency or architecture policy can justify static enforcement |
| Copy current implementation output into expected results | Establish an independent expected contract | Principle review; observed output alone is insufficient |
| Remove a failing check or relax an assertion | Investigate the cause and retain meaningful coverage within requested scope | Principle review; passing alone does not justify expectation changes |
| Run existing checks only | Execute applicable validation without manufacturing test additions | Repository verification uses existing tests |
| Missing requirement or failed tool setup | Resolve expectations or report blocked validation accurately | Instruction review only; independent clarification not executed |

## Concrete reuse decision

The existing log-preservation test creates prior evidence, attempts to reuse its path,
checks the error exit, and checks that the original contents remain unchanged.
That test already protects the requested preservation behavior; no duplicate test was added.
The repository suite executes it as part of normal verification.

## Budget and limits

SKILL.md body at initial evaluation: 3,708 characters including surrounding whitespace,
before adding the integration and suite-maintenance scope distinction.
No helper or additional testing dependency is bundled: selecting worthwhile assertions
depends on requirements, existing coverage, and failure mechanisms rather than a universal
mechanical scan. Instructions request targeted inspection and bounded execution reports.
Large-suite selection and maintenance savings were not measured.

The skill includes the shared saved-records convention and works independently.
Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.

All 14 skills validated; all 67 existing tests and CLI installation checks passed.
Creator validation and actual selective installation of test passed; both bundled
files match their installed copies byte for byte. Local links and the MIT copy passed.
No runtime helper, testing dependency, or new assertion-only test was added.
