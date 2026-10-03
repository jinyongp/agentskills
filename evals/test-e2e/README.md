# test-e2e evaluation

Instruction review covers journey scope and user-visible outcomes. Existing native CLI
installation verification provides a limited parent-executed command journey.
Independent agent E2E authoring and browser journeys were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Discover and selectively install a standalone skill | Use the actual command entrypoint and inspect the completed installation | Reused actual skills@1.7.0 discovery and selected-file verification |
| Run every logic edge case through the complete system | Reuse lower-level coverage; choose meaningful system failures | Instruction review; no full branch matrix required |
| Find a browser button by a private CSS class | Prefer its semantics or an explicit stable automation contract | Instruction review; browser execution not performed |
| Pass after mocked internal calls only | State the actual unverified system boundary | Instruction review; mocked calls are not completion evidence |
| Read an artifact or persisted result after the action | Verify consequential state required by the journey | Real selected installation checks compare delivered files at the destination |
| Missing environment or shared data | Report gaps and isolate owned resources | Temporary installation fixtures are isolated; live environments were not used |
| Flaky timing or unsafe retries | Use bounded conditions and diagnose causes | Policy review; browser readiness and retry behavior not executed |
| Large failure logs | Start with a bounded summary and selected native evidence | Policy review; independent large-output behavior not measured |

## Executed example and limits

The existing smoke script invokes the actual installation CLI, discovers categorized
skills, selects one, and checks destination files and absence of the unselected skill.
The new skill receives actual selective installation too. This is a limited CLI
distribution journey and cannot establish browser, deployment, or application behavior.

SKILL.md body: 3,519 characters including surrounding whitespace.
No new browser framework, fixture service, or universal runner is bundled.
The selected project supplies its harness and output limits; saved records follow the
shared convention. No duplicate permanent journey test was added.
Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11 and skills@1.7.0 are maintenance verification tools.
Browser semantics, authentication, reload persistence, and live service cleanup were not run.

All 19 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files
match their installed copies byte for byte. Local links and the MIT copy were checked.
