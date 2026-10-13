# Choose a testing skill

Choose by the work requested. Each skill works independently; loading the entire
set is unnecessary. Reuse existing checks when sufficient. Adding no new test is
a valid outcome.

| Skill | Use when | Required justification |
| --- | --- | --- |
| [test](../skills/workflow/test/SKILL.md) | Decide whether and where to add coverage | A named failure, an observable contract, and a meaningful coverage gap |
| [test-integration](../skills/workflow/test-integration/SKILL.md) | Exercise a real dependency or module boundary | Evidence that isolated/static checks cannot supply |
| [test-maintenance](../skills/workflow/test-maintenance/SKILL.md) | Audit or improve existing tests | A concrete maintenance cost and preserved failure detection |
| [test-unit](../skills/workflow/test-unit/SKILL.md) | Check isolated calculations, decisions, or state transitions | An uncovered logic failure at a stable interface |
| [test-contract](../skills/workflow/test-contract/SKILL.md) | Verify consumer/provider compatibility | Independently justified expectations and provider conformance |
| [test-e2e](../skills/workflow/test-e2e/SKILL.md) | Exercise a critical journey from the actual entrypoint | A user outcome whose failure cheaper checks cannot expose |
| [test-property](../skills/workflow/test-property/SKILL.md) | Explore generated inputs or state transitions | An independently justified invariant and meaningful domain |

Property testing is a technique that can use unit or integration boundaries.
Contract testing focuses on compatibility rather than a required execution layer.

[Back to the collection](../README.md#testing-workflows)
