---
name: queue
description: "Convert settled plans or work items into a task queue draft, or register them in the selected project tool when requested. Preserve scope, meaningful dependencies, and existing task identities."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Queue

## Scope

- Turn settled work into a queue. Resolve material planning decisions before
  registering their dependent work; independent settled items can proceed.
- Drafting a queue creates no task records. Registration requires a user request
  and the destination/tool selected by the user or project; ask only if missing.
  Use that tool's documented commands without installing or switching trackers.

## Procedure

1. Recover the current goal, accepted scope, actionable items and source references.
   Exclude headings, rejected proposals, vague reminders and optional extensions.
2. Group by independently verifiable outcomes. A file or checklist line is not
   automatically a task; keep coupled steps together and consolidate duplicates
   without losing acceptance conditions. Preserve meaningful domain wording.
3. Give each task an action and observable result. Preserve supplied priorities;
   shared files or preferred order alone do not establish dependencies. Connect
   tasks only when later work needs an earlier result or state. Include explicit
   validation/review work; do not append unrequested quality or closeout tasks.
4. For a draft, return the queue with unresolved items clearly separated.
   For registration, inspect existing tasks in the selected scope before writing.
   Start with summaries; use the tool's filters and bounded pages to recover the
   relevant records. Partial listings cannot prove that a duplicate is absent.
5. Reuse matching task IDs; ambiguous matches need resolution, not silent updates.
   Register unambiguous new tasks and wire dependencies using confirmed IDs.
   If a write fails or its outcome is unknown, inspect resulting records before
   retrying. Preserve successful IDs and report remaining work separately.
6. Read back the affected tasks and dependency links. Report a draft as a draft
   and registration as confirmed only for records actually found at the destination.

## Result

Report the destination, drafted or created tasks, reused IDs, dependencies and
unresolved items. Link source work instead of copying the entire plan. No tracker
mutation, completion marking, commit or publication follows from a draft request.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
