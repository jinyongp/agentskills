---
name: qa-checklist
description: "Prepare manual verification steps with preconditions, actions, and expected results for changed behavior. Use for human QA plans; execution and results are separate."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# QA Checklist

## Scope

Prepare a manual verification plan for changed behavior. The result is for a
person using the selected application, API, CLI, or other observable surface.
Writing a plan does not execute tests or authorize mutations in a live system.
Honor the requested environment and language; deployment is not a prerequisite.

When inspecting a Git change, use Git and Python 3.11+. Execute the bundled
`python3 scripts/inspect_changes.py --repo <root>` without reading its source.
Read [references/change-inspection.md](references/change-inspection.md) for
target selection, layer distinctions, and bounded file/diff pages.

## Procedure

1. Establish changed behavior, the comparison target, and intended acceptance.
   Read relevant requirements, existing contracts, and touched callers; code output
   alone does not settle what should happen. Pin commit comparisons for detail.
2. Select observable scenarios for the change and adjacent flows affected by its
   dependencies. Cover meaningful success, rejection, access, state, or recovery
   behavior. A refactor can merit checking preserved behavior when coupling changes;
   a formatting-only change can have no useful manual steps.
3. State necessary setup: environment/build, suitable test data/accounts, permissions,
   flags, and prior state. Identify destructive steps and use owned test data or
   a suitable isolated target. Do not turn this plan into instructions to alter
   production configuration or bypass access controls.
4. Write actionable steps in a practical order. Pair each action with the visible
   expected outcome and relevant persisted/async effects. Make waits observable
   where timing matters; arbitrary sleeps are not evidence of completion.
5. Keep internal classes, implementation-only details, and developer chores out of
   the walkthrough. Use technical names when the person must use them, such as an
   API endpoint or CLI option. If intended behavior or setup is unresolved, surface
   that dependency instead of fabricating a pass criterion.

## Result

Return setup followed by a focused checklist of actions and expected results.
Separate unavailable scenarios and open expectations. Scale to changed behavior,
not a fixed checkbox quota. Mark steps as planned; do not imply they were run.
If execution is also requested, preserve the plan and report actual results under
that separate task authorization.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
