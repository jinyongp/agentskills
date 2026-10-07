# Repository instruction clarity review

Parent instruction review on 2026-10-07; model version not recorded. Reviewed all
49 skill entrypoints and their 33 bundled Markdown references. Scripts were assessed
through their documented interfaces; this was not a fresh source audit of each helper.

## Criteria

Read each rule with its surrounding procedure and conditionally routed references.
Revise when the agent still lacks evidence to inspect or a resulting decision.
Retain concise guidance when that context already supplies the action. Pair a case
needing intervention with a valid case that should remain unchanged; preserve user
scope, contracts, genre, and implementation freedom. Concrete examples illustrate
decisions rather than establishing universal recipes or output templates.

## Coverage and disposition

| Category | Revised in this review | Retained after review |
| --- | --- | --- |
| Writing (9) | clear, english-writing, korean-writing, rewrite, write | brief, dev-docs, summarize, terse |
| Frontend (15) | prototype, ui-design | accessibility, animate, animate-native, animation-audit, animation-debug, animation-opportunities, animation-performance, animation-review, animation-vocabulary, mobile-web, responsive, ui-library, ui-stress |
| Git (6) | None | git-branch, git-commit, git-conflict, git-pr, git-sync, git-worktree |
| Workflow (19) | handoff, implement, test-maintenance, test-unit, verify | api-design, benchmark, code-review, db-migrate, debug, dependency-update, optimize, plan, survey, test, test-contract, test-e2e, test-integration, test-property |

The 12 revised skills have paired cases recorded in their own evaluation notes.
Writing rules now identify misplaced answers, ambiguous relationships, unsupported
evaluations, and loss of qualifications in emphasis. UI decisions use task priority,
actual identity evidence, and the comparison question. Workflow decisions specify
changed-path evidence, fault-equivalent coverage, recoverable handoff inputs, and
the responsibility that earns a design layer's cost.

Retained Git instructions already name queries, operations, refusal conditions,
and preservation checks. Retained motion guidance identifies state transitions,
runtime probes, and source-versus-measurement limits. Remaining workflow guidance
identifies interfaces, inputs, contracts, failure evidence, or operation-specific
references; remaining presentation guidance identifies source fidelity and status
conditions. Dev-docs received its main-path revision immediately before this review.
Retention means no supported instruction-clarity change emerged in this pass; it is
not a guarantee of correct future agent decisions.

## Verification and limits

Full `uv run --locked check.py` passed: 49 skill formats/catalogs, 76 existing tests,
and categorized CLI discovery/selective-installation fixtures. Creator validation
passed for all 12 revised skills. Across all 49 skills, body budgets, canonical
saved-record fragments, and 33 bundled Markdown links passed. No runtime helpers,
catalog entries, dependency declarations, or permanent tests were added or changed.

After the full run, a final UI wording adjustment clarified that new identity cues
may be proposed when source branding is absent. Format/catalog, creator, link/body,
and whitespace checks were repeated for the final state; runtime checks were reused.

Paired cases are parent rule review, not independent agent executions, reader
studies, or evidence of a measured quality improvement. Individual real-skill CLI
installations were not repeated; the full run used the repository's installation
fixtures. Earlier per-skill verification records remain historical.
