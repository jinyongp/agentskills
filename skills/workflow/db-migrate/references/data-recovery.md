# Data transformation and recovery

Read for backfills, concurrent writes, resume behavior, or irreversible operations.

## Mapping and progress

Define source-to-target meaning, canonical representation, and required invariants.
Handle nulls, duplicates, invalid encodings, and conflicting existing target values
explicitly; do not invent defaults or silently skip records to make a migration finish.
Protect sensitive values in logs and use synthetic rehearsal data where possible.

At scale, use a stable traversal key and bounded batches rather than offsets whose
membership can change under writes. Define transaction boundaries and persist progress
only with the work it represents. A cursor alone may miss inserts, updated rows,
or retry gaps; choose a watermark, reconciliation pass, or supported tool mechanism
that matches the actual writer contract. Keep ownership and concurrent modifications
safe through an appropriate snapshot, conditional update, version check, or write policy.

Idempotence means repeating an operation preserves its intended effect, not ignoring
every error. Inspect partially populated targets and schema/ledger state before rerun.
Timeouts and lost connections can leave committed work or a running job; verify the
outcome instead of blindly issuing the operation again.

## Failure and operational bounds

Use meaningful lock/query/job timeouts, cancellation paths, and load budgets. Account
for transaction length, log growth, storage, replicas, and concurrent writer impact
where relevant. Stop on violated invariants, unexpected target state, or exhausted
budget. Preserve job IDs, checkpoints, rejected-record counts, and recovery evidence.

## Recovery

Separate application rollback, schema rollback, corrective forward migration, and
data restoration. A generated down migration cannot restore dropped rows or reverse
a lossy mapping. Verify required backups and restoration capability before relying
on them for destructive operations; a backup file's existence alone is insufficient.
Account for writes after the backup and cross-store consistency when restoration matters.

Recovery should match the data and operation. An owned disposable fixture can simply
be recreated; valuable live records need an established preservation path. Restore
or repair only within the identified target and current authorization. Recheck actual
data invariants and consumer behavior after recovery rather than assuming success.
