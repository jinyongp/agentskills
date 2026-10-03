# test-maintenance evaluation

Instruction review and parent inspection of two existing checks cover the retention
criteria. Independent agent auditing, pruning, and automatic routing were not evaluated.

| Request | Expected behavior | Observed result |
| --- | --- | --- |
| Remove structure or literal tests categorically | Find the protected contract first | Parent reviewed the body-budget check and retained it: exact acceptance/rejection boundaries implement an explicit repository policy |
| Simplify a full-output equality assertion | Determine whether exact content is required | Parent retained the diff page reassembly check: exact recovery is the helper's public output contract |
| Two tests execute the same lines | Compare failure mechanisms and boundary evidence before consolidation | Instruction review; shared coverage alone does not prove duplication |
| Similar tests at unit and integration layers | Keep additional real wiring evidence when useful | Instruction review; no categorical cross-layer deletion |
| A test blocks a harmless refactor | Replace incidental constraints with required observable properties | Instruction review; no implementation refactor executed |
| A failing test is inconvenient | Investigate the contract and preserve meaningful protection | Instruction review; a green suite is insufficient justification |
| Audit only | Return findings without edits | Evaluation inspection made no changes to existing tests |
| Reduce a slow or flaky suite | Establish concrete cost and cause; verify targeted changes | Instruction review only; no timing savings or flake reduction measured |
| Large inventory or missing ownership/contract | Bound selection; resolve missing justification before risky reductions | Policy review; independent large-suite behavior not measured |
| Existing tests are already useful | Keep them unchanged | Reviewed checks remain in place; no permanent tests added or removed |

## Concrete retention decisions

- tests/test_validate_skills.py::test_body_budget_keeps_conditional_references_separate
  verifies acceptance at the maximum body size and rejection above it, while conditional
  resources remain separately budgeted. The constraint is a stated repository rule.
- tests/test_git_inspection.py::test_selected_diff_pages_reassemble_exactly
  joins paged output and compares it with actual Git output, including escaped and
  Unicode content. Partial matching would lose proof of complete information recovery.

These examples show why literal/structural assertions cannot be rejected just by form.
They are a limited parent review, not an exhaustive assessment of the repository suite.

## Budget and environment

SKILL.md body: 3,688 characters including surrounding whitespace.
The general test entrypoint's scope distinction now uses 3,875 body characters.
No bundled scanner is provided: textual similarity and line coverage cannot establish
semantic redundancy. Instructions use native reports or a tested reducer for mechanical
inventory, then inspect selected contracts and assertions. Large inventories and pages
were not exercised in this instruction-only evaluation.

Evaluation date: 2026-10-03 (Asia/Seoul), current Codex session; model version not recorded.
Python 3.11 and skills@1.7.0 for repository verification and selective installation.
No maintenance savings are claimed, and no existing test assertions were changed.

All 16 skills validated; all 67 existing tests and CLI smoke checks passed.
Creator validation and actual selective installation passed; both bundled files match
their installed copies byte for byte. Local links and the MIT notice were checked.
