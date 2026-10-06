---
name: db-migrate
description: "Prepare, review, or run scoped database schema changes and data migrations with engine-aware execution, preserved data, staged compatibility, and recovery. Use for migrations or backfills; live execution requires the identified target and task authorization."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Db Migrate

## Scope

Prepare, review, or execute the requested schema change, backfill, or data transfer.
Identify the engine/version, migration tool, target environment, and affected data.
Authoring or review alone does not authorize live execution. Reuse existing execution
authorization for the identified target; destructive loss needs explicit scope.
Preserve user work, credentials, applied migration history, and unrelated records.

Read [references/rollout.md](references/rollout.md) for mixed application versions,
schema transitions, constraints, or deployment order. Read
[references/data-recovery.md](references/data-recovery.md) for backfills, concurrent
writes, interruption, retry, irreversible changes, or recovery planning.

## Procedure

1. Establish the required final contract and current schema/data/migration state.
   Inspect relevant consumers, writers, constraints, volume estimates, and pending
   migrations through bounded queries. Keep sensitive rows and full dumps outside
   default input; report selection/omissions and recover necessary evidence.
2. Verify engine/version and tool behavior for the proposed operations: locks,
   transactions, implicit commits, rewrites, online/concurrent features, and failure
   state. Use official documentation where semantics matter; one engine's behavior
   is not portable SQL. Resolve material unknowns before dependent execution.
3. Choose a proportional sequence. For mixed deployments, maintain old/new reader
   and writer compatibility, backfill safely, switch consumers, and remove obsolete
   structures only when no required consumer remains. A new empty database may need
   no staged rollout. Preserve already-applied history; follow tool policy for new
   corrective migrations rather than silently rewriting ledger entries or checksums.
4. Define data mapping, invariants, rejected/conflicting records, concurrent-write
   policy, execution budget, and stopping conditions. Use bounded batches and durable
   progress when scale requires them. Establish recovery before destructive execution;
   a reverse schema change is not proof that deleted or transformed data is recoverable.
5. Prepare scoped migrations using project tooling. Rehearse on an isolated fixture
   with relevant existing, empty, invalid, and partially migrated states. Verify required
   results, consumer compatibility, and interruption/retry where relevant. Reuse
   existing checks; add coverage only for a meaningful uncovered migration contract.
6. For authorized execution, confirm the exact target and preconditions. Run the
   supported sequence with appropriate timeouts and observability. Bound operational
   load; stop on violated invariants or budget. On partial, timed-out, or uncertain
   outcomes, inspect actual schema, ledger, job, and data state before retrying.
7. Verify final invariants and affected consumers, not only command success or row
   count. Record applied/pending steps, rejected records, and recovery status. Preserve
   partial evidence and unrelated data; repairs or restoration follow their own scope.

## Result

Return the plan or actual applied state, engine/tool assumptions, compatibility order,
data checks, execution evidence, and remaining steps. Distinguish fixture rehearsal
from target execution and recovery from a proposed reverse script. Report irreversible
effects and untested engine/load conditions; never imply safe production operation
from a small fixture or an unverified backup.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
