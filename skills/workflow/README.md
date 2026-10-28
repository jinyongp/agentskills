# Workflow

Choose a skill for the work you need done. These are independent workflows, not a required sequence.

<!-- skills:start -->

## Understand and plan

- [survey](survey/SKILL.md) — Map a repository without running project code.
- [trace](trace/SKILL.md) — Explain one codebase journey with source citations.
- [research](research/SKILL.md) — Investigate an external question using primary evidence.
- [domain-modeling](domain-modeling/SKILL.md) — Resolve ambiguous business terms and rules.
- [proposal](proposal/SKILL.md) — Prepare proposals with the context and evidence needed for independent assessment.
- [spec-generator](spec-generator/SKILL.md) — Turn an idea or rough notes into product behavior, roles, scope, and feature flows.
- [plan](plan/SKILL.md) — Plan implementation, work order, dependencies, and verification for the requested behavior.
- [queue](queue/SKILL.md) — Draft task queues or preserve plans as local checklists.

## Implement and troubleshoot

- [implement](implement/SKILL.md) — Build an agreed feature, fix, or refactor.
- [debug](debug/SKILL.md) — Reproduce a bug, find its cause, and verify a fix.
- [ci-fix](ci-fix/SKILL.md) — Diagnose failing CI and correct affected checks.
- [dependency-update](dependency-update/SKILL.md) — Update selected dependencies and verify compatibility.
- [api-design](api-design/SKILL.md) — Design or review a consumer-facing interface.
- [db-migrate](db-migrate/SKILL.md) — Prepare or run a scoped schema change or data migration.

## Review and verify

- [proposal-assessment](proposal-assessment/SKILL.md) — Investigate proposal claims, related problems, impact, and alternatives to recommend a justified decision; detailed plans when requested.
- [review-map](review-map/SKILL.md) — Map change risk and reading order for human review.
- [code-review](code-review/SKILL.md) — Review changes for defects or recorded decision compliance.
- [review-loop](review-loop/SKILL.md) — Review and fix agreed scope through completion.
- [dependency-review](dependency-review/SKILL.md) — Assess dependency adoption and changed package tradeoffs.
- [security-review](security-review/SKILL.md) — Trace exploitable defects across a security boundary.
- [qa-checklist](qa-checklist/SKILL.md) — Prepare manual actions, setup, and expected outcomes.
- [verify](verify/SKILL.md) — Run useful checks and report evidence and gaps.
- [preflight](preflight/SKILL.md) — Identify deployment prerequisites and operational actions.
- [close](close/SKILL.md) — Assess completion and commit readiness from existing evidence.

## Test

- [test](test/SKILL.md) — Assess coverage, suggest cases, and choose test boundaries.
- [test-unit](test-unit/SKILL.md) — Check isolated calculations and state transitions.
- [test-integration](test-integration/SKILL.md) — Exercise real dependency and module boundaries.
- [test-contract](test-contract/SKILL.md) — Check consumer and provider compatibility.
- [test-e2e](test-e2e/SKILL.md) — Verify a critical journey through the actual entrypoint.
- [test-property](test-property/SKILL.md) — Explore justified invariants over generated inputs.
- [test-maintenance](test-maintenance/SKILL.md) — Reduce suite cost while preserving failure detection.

## Measure and carry work forward

- [benchmark](benchmark/SKILL.md) — Measure a baseline and candidate with matched workloads.
- [optimize](optimize/SKILL.md) — Improve a demonstrated performance bottleneck.
- [handoff](handoff/SKILL.md) — Prepare or resume work across sessions.
- [retro](retro/SKILL.md) — Review observed workflow friction and propose improvements.

<!-- skills:end -->

## Install

Run from the target project; replace `survey` with one or more names above:

```bash
npx @jinyongp/agentskills@latest add --agent codex --skill survey
```

See [installation requirements and alternatives](../../README.md#quick-start).

[Authoring guide](../../CONTRIBUTING.md) · [All skills](../../README.md)
