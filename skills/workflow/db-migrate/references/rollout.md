# Schema and application rollout

Read for schema transitions, constraints, mixed versions, or deployment ordering.

## Determine the real execution model

Confirm installed engine and migration-tool versions, transaction wrapping, lock
timeouts, schema-rewrite behavior, and supported online operations. Framework
generation or a successful dry-run is not evidence that the target operation is cheap.

[PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
documents operation-specific locks and rewrite behavior. Its
[concurrent index documentation](https://www.postgresql.org/docs/current/sql-createindex.html)
describes restrictions, including execution outside a transaction block and possible
invalid indexes after failure. Apply these facts only to relevant PostgreSQL versions.

[SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html) has different supported
operations and restrictions. Inspect the target version and project migration path;
a lightweight SQLite rehearsal does not establish another engine's locking or DDL
transaction behavior. Nonrelational stores also need their actual schema/data model
and job consistency guarantees, rather than assumed relational semantics.

## Preserve consumers during transition

Identify readers, writers, generated clients, jobs, replicas, and old releases that
can remain active. An additive schema change can still break strict consumers,
positional reads, defaults, or constraint expectations. Verify relevant contracts.

Choose staged expansion, compatible writes/reads, backfill, consumer switch, and
eventual contraction when mixed versions require it. Dual writes introduce ownership
and failure-consistency questions; use them only with an explicit authoritative source
and reconciliation policy. Removing a field must account for rollback to an old app.

## Constraints and cleanup

Inspect invalid, duplicate, missing, or out-of-range values before enforcing a new
constraint or narrowing a type. Preserve required precision and encoding. Validate
engine-supported deferred/online checks where needed rather than assuming an added
constraint has checked all old data. Drop obsolete structures only within scope and
after required readers/writers are retired. Keep initial empty-database setup simple.
