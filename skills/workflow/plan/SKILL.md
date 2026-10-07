---
name: plan
description: Turn a requested change into a scoped implementation plan with dependencies, decisions, completion criteria, and validation. Clarify material ambiguity before execution.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Plan

## Scope

- Plan the user's requested outcome. Planning alone authorizes relevant inspection,
  not implementation, task creation, or external writes.
- Reuse current repository facts and accepted decisions; link their sources instead
  of copying them. Keep the plan proportional to the work.

Read [references/design-scope.md](references/design-scope.md) when comparing a
simpler alternative, added infrastructure, or the completeness of a proposed solution.
Read [references/work-units.md](references/work-units.md) when splitting a larger
plan or drafting tasks from settled work items.

## Procedure

1. State the outcome, scope, constraints, and observable completion criteria.
   Inspect only facts needed to identify the affected behavior and dependencies.
   Preserve agreed limits, deliberate omissions, and rationale at their source or
   in the plan. Define success and recovery within that contract; distinguish required
   behavior from optional extensions. Absence alone is not an unmet requirement.
2. Separate accepted decisions, reversible assumptions, and unresolved choices.
   Ask when several viable options materially affect behavior, contracts, data,
   permissions, or cost and existing context cannot settle the choice.
   Routine implementation details and optional preferences are not approval gates.
3. For a necessary decision, explain the impact and recommend a supported option.
   Keep the question visible in conversation. Resolve dependent decisions before
   committing to affected steps; independent preparation can continue.
4. Compare viable approaches by requirement coverage, readability, and maintenance
   cost. Check existing code, standard/platform features, and installed tools for fit.
   Justify added structure by a current need or concrete maintenance benefit; name
   where a simpler option falls short. Keep accepted behavior intact when simplifying.
   Give each work unit an outcome, relevant paths, and completion evidence. Add a
   dependency when it needs another unit's output or state, not merely a preferred
   order. Include migration/recovery when needed.
5. Tie each plausible failure to a useful check. Distinguish per-unit checks from
   required final integration checks; a scheduled check remains pending.
   Use not-needed when a check would add no useful signal.
6. Review the plan against the latest request. Express current choices positively;
   keep necessary rationale and unresolved questions distinct. Read
   [references/current-context.md](references/current-context.md) when a correction
   or changed decision affects the plan or dependent records.
7. Return a short inline plan unless a destination was requested. If implementation
   is also authorized, continue once blocking choices are resolved; otherwise stop
   after the plan.

## Result

Give ordered work units, dependencies, completion criteria, checks, and only material
remaining decisions. Mark assumptions clearly. Plans describe intended work, not
completed implementation or passing validation.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
