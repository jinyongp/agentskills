# Workflow

Skills for implementation, inspection, planning, tests, verification, review, debugging,
dependency updates, API design, database migrations, performance work, and handoff.
`research` investigates external evidence; `security-review` traces exploitable
defects; `ci-fix` diagnoses CI failures and verifies current-revision results.
`plan` settles work; `queue` drafts or registers it when requested.
`verify` runs checks; `close` assesses existing completion evidence. These are
independent workflows, not a mandatory sequence for every task.
`benchmark` measures and compares; `optimize` corrects demonstrated costs. `api-design`
defines consumer contracts; `db-migrate` preserves data through scoped transitions.
<!-- skills:start -->
| Skill | Description | Install |
| --- | --- | --- |
| [handoff](handoff/SKILL.md) | Carry missing task context and targeted repository lookups into another session or agent | `npx skills add jinyongp/agentskills --skill handoff` |
| [verify](verify/SKILL.md) | Select useful checks, run them with bounded reports, and record evidence and gaps | `npx skills add jinyongp/agentskills --skill verify` |
| [survey](survey/SKILL.md) | Map relevant structure, commands, and risks through bounded read-only inspection | `npx skills add jinyongp/agentskills --skill survey` |
| [plan](plan/SKILL.md) | Resolve material ambiguity and order scoped work with completion criteria and checks | `npx skills add jinyongp/agentskills --skill plan` |
| [code-review](code-review/SKILL.md) | Inspect selected changes and report supported defects with locations and impact | `npx skills add jinyongp/agentskills --skill code-review` |
| [debug](debug/SKILL.md) | Reproduce symptoms, confirm causes, apply scoped fixes, and verify regressions | `npx skills add jinyongp/agentskills --skill debug` |
| [benchmark](benchmark/SKILL.md) | Compare code performance with matched workloads, repeated samples, and preserved evidence | `npx skills add jinyongp/agentskills --skill benchmark` |
| [test](test/SKILL.md) | Assess coverage gaps and design behavior tests with proportionate maintenance cost | `npx skills add jinyongp/agentskills --skill test` |
| [test-integration](test-integration/SKILL.md) | Protect real boundary behavior and wiring beyond isolated or static checks | `npx skills add jinyongp/agentskills --skill test-integration` |
| [test-maintenance](test-maintenance/SKILL.md) | Reduce concrete suite maintenance costs while preserving meaningful failure detection | `npx skills add jinyongp/agentskills --skill test-maintenance` |
| [test-unit](test-unit/SKILL.md) | Protect isolated logic and state without fixing internal implementation choices | `npx skills add jinyongp/agentskills --skill test-unit` |
| [test-contract](test-contract/SKILL.md) | Verify actual provider behavior against justified consumer compatibility expectations | `npx skills add jinyongp/agentskills --skill test-contract` |
| [test-e2e](test-e2e/SKILL.md) | Verify critical user journeys through actual entrypoints and observable results | `npx skills add jinyongp/agentskills --skill test-e2e` |
| [test-property](test-property/SKILL.md) | Explore meaningful invariants with generated cases and reproducible counterexamples | `npx skills add jinyongp/agentskills --skill test-property` |
| [implement](implement/SKILL.md) | Deliver authorized code changes with clear outcomes, simple design, scoped edits, and sufficient checks | `npx skills add jinyongp/agentskills --skill implement` |
| [dependency-update](dependency-update/SKILL.md) | Update selected dependencies or runtimes with verified target versions, compatibility review, scoped manifest and lockfile changes, and relevant checks. Use for requested upgrades or remediation; recommendations alone do not authorize installation. | `npx skills add jinyongp/agentskills --skill dependency-update` |
| [optimize](optimize/SKILL.md) | Improve code performance through demonstrated bottlenecks, scoped changes, correctness checks, and matched before/after measurements. Use for latency, throughput, memory, or resource costs; measurement alone does not authorize optimization. | `npx skills add jinyongp/agentskills --skill optimize` |
| [db-migrate](db-migrate/SKILL.md) | Prepare, review, or run scoped database schema changes and data migrations with engine-aware execution, preserved data, staged compatibility, and recovery. Use for migrations or backfills; live execution requires the identified target and task authorization. | `npx skills add jinyongp/agentskills --skill db-migrate` |
| [api-design](api-design/SKILL.md) | Design or review consumer-facing APIs and interface changes using explicit semantics, compatibility, errors, retries, and version policy. Use for HTTP, RPC, SDK, or message contracts; preserve project protocols and distinguish design from implementation. | `npx skills add jinyongp/agentskills --skill api-design` |
| [review-loop](review-loop/SKILL.md) | Review and fix agreed scope with complete area coverage, preserved tradeoffs, and scoped rechecks | `npx skills add jinyongp/agentskills --skill review-loop` |
| [queue](queue/SKILL.md) | Convert settled plans or work items into a task queue draft, or register them in the selected project tool when requested. Preserve scope, meaningful dependencies, and existing task identities. | `npx skills add jinyongp/agentskills --skill queue` |
| [close](close/SKILL.md) | Assess completion and commit readiness from existing scope, validation evidence and worktree changes. Use for requested closeout; report gaps without starting new implementation or checks. | `npx skills add jinyongp/agentskills --skill close` |
| [research](research/SKILL.md) | Investigate a specified question using primary sources, reconcile conflicting evidence, and distinguish facts, inference, and unknowns. Use for external technical research or comparisons; repository mapping alone uses survey. | `npx skills add jinyongp/agentskills --skill research` |
| [security-review](security-review/SKILL.md) | Review specified code, configuration, or changes for exploitable security defects. Trace attacker control, trust boundaries, permissions, and existing defenses; report supported findings with confidence and scoped evidence. | `npx skills add jinyongp/agentskills --skill security-review` |
| [ci-fix](ci-fix/SKILL.md) | Diagnose and fix failing CI for an identified revision or PR, verify current checks, and maintain compatible stable GitHub Actions when workflows change. Use for CI failures; preserve project tools, permissions, and release scope. | `npx skills add jinyongp/agentskills --skill ci-fix` |
<!-- skills:end -->

Add skills at `skills/workflow/<skill-name>/SKILL.md`.
[Authoring guide](../../CONTRIBUTING.md) · [All skills](../../README.md)
