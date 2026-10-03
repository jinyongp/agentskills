# test-unit evaluation

Instruction review covers admission and stable logic boundaries. Existing validator
cases provide a parent-reviewed example; no independent agent test writing was run.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Test a limit decision at and above its boundary | Use independently justified policy and stable validation results | Reviewed the existing description/body budget cases; required acceptance/rejection is covered |
| Add one test per helper or edit | Identify uncovered behavior rather than source structure | Instruction review; no blanket per-helper requirement |
| Assert an internal algorithm or helper call sequence | Preserve behavior-equivalent refactoring | Instruction review; incidental internals are excluded |
| Test a type error already caught statically | Reuse adequate static checks | Instruction review; external input runtime validation remains a separate risk |
| Existing cases already catch the failure | Reuse them without adding a duplicate | Parent reused existing validator coverage |
| A mock passes but real persistence is unverified | State the missing integration evidence | Instruction review only |
| Missing expectation or shared mutable fixture | Resolve the contract and isolate state | Policy review; independent clarification not tested |
| Large output or matrix | Select distinct mechanisms and bounded detail | Policy review; large-suite behavior not measured |

## Concrete example and limits

Existing tests/test_validate_skills.py budget cases check rejection only above the
published limits. They validate a required decision rather than pinning helper names.
They run within the existing repository suite; no additional assertion-only test was added.

SKILL.md body: 3,131 characters including surrounding whitespace.
No runtime helper or testing dependency is bundled. Framework setup and command output
are project-specific; the skill requests bounded native reports and selected details.
Automatic routing, newly authored defect detection, and maintenance savings are unmeasured.
Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11 and skills@1.7.0 are used only for repository verification and installation.

All 17 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files
match their installed copies byte for byte. Local links and the MIT copy were checked.
