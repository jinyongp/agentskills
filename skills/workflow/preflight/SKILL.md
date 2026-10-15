---
name: preflight
description: "Identify deployment prerequisites and operational actions implied by a change. Use for release preparation; distinguish before, during, and after rollout without executing it."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Preflight

## Scope

Identify release prerequisites and operational actions implied by a change.
Use for deployment preparation, including rolling or staged releases. This
checklist does not deploy, migrate data, provision services, or change credentials.
Explicit execution requests retain their own authorization and target requirements.

Use Git and Python 3.11+. Execute the bundled
`python3 scripts/inspect_changes.py --repo <root>` without reading its source.
Read [references/change-inspection.md](references/change-inspection.md) for
comparison arguments, layer selection, and bounded file/diff inspection.

## Procedure

1. Establish the selected release/change and target environment. Pin comparison
   IDs. Inspect changed code/configuration and relevant deployment definitions;
   a new environment key may already be configured or supplied by automation.
   Missing environment evidence stays a verification item, not a claimed omission.
2. Trace changes that affect operational readiness: schema/data compatibility,
   required config, workers/schedules, external integrations, assets/builds,
   permissions, and service versions. Include only requirements supported by the
   changed path and its consumers; do not append a universal release checklist.
3. Determine when actions are needed. Separate prerequisites before activation,
   rollout actions, and checks/cleanup after activation. Reason about coexistence
   of old/new code, workers, payloads, and schema when rollout order matters.
   Do not prescribe migrations before or after code universally.
4. Check which actions automation already owns. Distinguish required work from
   confirmation of existing setup and from optional operational advice. Name the
   evidence and consequence for each item, with exact source locations.
5. Identify consequential readiness gaps, supported recovery constraints, and
   observable post-rollout checks. A reverted code release may not undo persisted
   data or an external effect; record that limitation without promising a rollback.
   Resolve target-specific unknowns before giving an unconditional ready verdict.

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
