---
name: preflight
description: "Identify deployment prerequisites and operational actions implied by a change. Use for release preparation; distinguish before, during, and after rollout without executing it."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Preflight

Identify release prerequisites and operational actions implied by a change.
Use for deployment preparation, including rolling or staged releases. This
checklist does not deploy, migrate data, provision services, or change credentials.
Explicit execution requests retain their own authorization and target requirements.

## Core rules

- **Trace requirements.** Include only actions supported by changed paths and
  consumers; do not append a universal release checklist.
- **Timing depends on compatibility.** Separate before, during, and after activation.
  Account for old/new code, workers, payloads, and schema where order matters;
  do not prescribe migrations before or after code universally.
- **Unknown is verification work.** Missing environment evidence is not proof
  of missing setup. Resolve target-specific gaps before an unconditional ready verdict.

Use Git and Python 3.11+. Execute the bundled
`python3 scripts/inspect_changes.py --repo <root>` without reading its source.
Read [references/change-inspection.md](references/change-inspection.md) for
comparison arguments, layer selection, and bounded file/diff inspection.

## Assess rollout needs

1. **Target.** Establish release/change and environment. Pin comparison
   IDs. Inspect changed code/configuration and relevant deployment definitions;
   a new environment key may already be configured or supplied by automation.
2. **Operational effects.** Trace schema/data compatibility,
   required config, workers/schedules, external integrations, assets/builds,
   permissions, and service versions.
3. **Order.** Determine timing and compatibility dependencies for the needed actions.
4. **Ownership.** Check automation responsibilities. Distinguish required work from
   confirmation of existing setup and from optional operational advice. Name the
   evidence and consequence for each item, with exact source locations.
5. **Recovery and readiness.** Identify consequential gaps, supported recovery constraints, and
   observable post-rollout checks. A reverted code release may not undo persisted
   data or an external effect; record that limitation without promising a rollback.

## Result

Return a concise list grouped by rollout timing and useful operational area.
Include action, requirement/verification status, evidence, and dependency or owner
when known. Distinguish prepared tasks from actions already performed. Follow
the project's deployment tools if execution is separately authorized; preflight
alone starts no command with operational side effects.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
