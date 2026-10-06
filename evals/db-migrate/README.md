# Database migration evaluation

See [parent task execution](../task-execution/README.md) for reproducible SQLite
interruption, resume, reconciliation, preserved targets and backup readback.
Production restoration and concurrent writers remain outside that rehearsal.

## Decision cases

Parent instruction review on 2026-10-06 in the current Codex session; model version
not recorded. These are decision-rule checks, not production migration certification.

| Request or condition | Expected decision | Review result |
| --- | --- | --- |
| Initialize an empty local database | Use the appropriate simple migration | No mandatory multi-release rollout |
| Existing service has old/new application versions | Preserve required readers/writers and stage contraction | No immediate field drop |
| Schema addition breaks a positional consumer | Inspect the real consumer contract | Additive is not automatically compatible |
| Target engine/tool is unknown | Resolve operation semantics before dependent execution | No portable-DDL assumption |
| PostgreSQL concurrent index uses a transaction-wrapping tool | Check documented restrictions and supported execution mode | No generic transaction blanket |
| SQLite rehearsal passes for a PostgreSQL target | Keep engine/load gaps explicit | No inferred production locks or DDL semantics |
| Already-applied migration needs correction | Follow immutable history and tool policy | No silent ledger/checksum rewrite |
| Narrowed type has invalid, null, or duplicate data | Define rejection/conflict policy before enforcement | No fabricated default or hidden skipped record |
| Large backfill has concurrent inserts and updates | Stable traversal, writer policy, durable progress and reconciliation | A cursor alone is insufficient |
| Target row was modified after source was read | Preserve current ownership through suitable concurrency control | No blind stale overwrite |
| Failure interrupts a batch | Inspect committed state and progress before resume | No checkpoint assumed ahead of data |
| Timeout may leave a running job or committed operation | Confirm actual outcome before retry | No duplicate live operation |
| Count matches but transformed values are wrong | Verify mapping invariants and consumer behavior | Count/exit status alone is insufficient |
| Lossy conversion has a generated down script | Distinguish structural rollback from data recovery | No unsupported recoverability claim |
| Backup exists but restoration is unverified | Establish the preservation path before relying on it | File existence is not a recovery proof |
| Review or migration-file authoring only | Return findings or prepared files | No live execution inferred |
| Destructive target or credential is ambiguous | Stop affected execution and resolve identity/scope | No guessed database or secret disclosure |
| Huge data set or failed infrastructure | Bounded aggregate queries, selected synthetic cases, explicit omissions and gaps | No full sensitive-row dump or claim of all-record coverage |

## Input budget and evidence limits

No engine-specific runner is bundled. Use project migration tooling and bounded
aggregate/state queries; fetch only relevant schema, ledger, and rejected-record
detail. Native output varies, so no universal mechanical ceiling is claimed.
A new reducer needs explicit limits and large-input/failure verification.

Engine-specific operational performance, production execution, cross-store recovery,
production backup restoration, independent plan quality, and automatic routing remain unmeasured.
References are original guidance with links to primary engine documentation.

## Parent-guided rehearsal

A disposable SQLite 3.53.1 database used eight synthetic rows, an additive column,
and a progress table. A transaction failed after two updates; row values and progress
matched the pre-batch state after rollback. Committed batches resumed after closing
and reopening the connection. Repeated completion preserved the final state, old
readers retained their columns, and an already populated target value remained intact.
A late row below the saved cursor stayed unfilled after cursor-based completion;
an invariant check detected it and a scoped reconciliation filled it.

This hand-authored replay passed. It illustrates selected decisions in the references,
not independent agent execution, real concurrent writers, restoration, another engine's
DDL semantics, or operational migration safety. That initial replay used a temporary
script; the subsequent linked replay now retains its fixture for reproduction.

Packaging verification passed: 48 skills, 76 existing tests, and CLI fixtures.
Creator validation and actual selective installation with skills@1.7.0 passed;
all four bundled files matched byte-for-byte. MIT notice and local links passed.
Entrypoint body: 3,983 characters, excluding frontmatter.
