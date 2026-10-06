# Resolution and recovery

Read for workspaces, changed locks, install failures, or reproducibility concerns.

## Manifest and lock ownership

Find the canonical manager and version from project instructions, lockfiles, runtime
pins, and CI. Multiple manifests or locks may belong to separate packages; a file's
presence alone does not authorize deleting it. Choose the workspace/root that owns
the selected package, and use native filtered operations where appropriate.

Lockfile churn can come from manager changes, registry configuration, platform
dependencies, or unrelated drift. Trace it before accepting a broad diff. Preserve
integrity data and legitimate transitive updates; do not hand-edit resolved records
or remove integrity fields merely to make resolution appear successful.

## Execution and failed attempts

Package operations can execute lifecycle hooks, code generators, and native builds.
Follow current execution policy and inspect material side effects; do not assume
an install command is read-only. Selective suppression can be appropriate in a
controlled check, but does not establish that the skipped setup works in production.

On failure, distinguish network/authentication, unsupported platform, conflicting
constraints, corrupt integrity, and consumer migration problems. Keep useful logs and
the current patch. Retry only when new evidence or state changes support it; resolve
uncertain outcomes before repeating external actions. Restore only owned changes
when recovery is requested, preserving pre-existing files and staging.

## Verification

Use the supported clean/frozen install mode in an isolated workspace when it adds
useful evidence. Confirm the intended resolved versions and relevant application
behavior, not just an installer exit code. Native or browser support requires its
relevant build/runtime environment. Record unavailable checks without claiming
every supported target works. Reuse existing migration and integration coverage.
