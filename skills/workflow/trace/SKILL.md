---
name: trace
description: "Explain one codebase journey by following its actual trigger, calls, data effects, and outcome with source citations. Use for how-it-works questions, not defect diagnosis."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Trace

Explain one journey through a codebase: its trigger, control/data flow, side
effects, and outcome. Use for how-it-works questions. Diagnosing a failing journey,
proposing fixes, or changing code requires that task scope; tracing alone is read-only.

## Core rules

- **Verify each hop.** Read supporting lines; a symbol search is a lead, not an
  edge. For framework conventions, generated dispatch, database effects, or vendor
  behavior, identify configuration/version and implementation evidence. Cite app
  reliance separately from proof of an implicit mechanism.
- **Static is not runtime.** Static tracing proves neither that a run occurred
  nor its runtime state. Keep unresolved dispatch and service behavior unknown.
- **Consequential branches.** Retain preconditions and error/recovery paths that
  change the answer; stop following unrelated callers once it is established.

## Follow the journey

1. **Question.** Define a specific action and outcome. Narrow a broad topic
   to a representative journey and disclose that choice; ask when choosing a path
   would answer a materially different question.
2. **Trigger.** Locate an actual caller/entrypoint: UI action, route, command, event,
   scheduled invocation, or configured integration. Search relevant registrations
   and callers before declaring code unreachable. If no trigger is found, report
   the searched scope and explain the hypothetical path separately.
3. **Flow.** Follow calls and values, including relevant guards, validation,
   persistence, async handoffs, and error/recovery branches. Trace across folders;
   stop following unrelated callers once the question is answered.
4. **Evidence.** Verify each hop under the core evidence rules.
5. **Conditions.** Record flags, caller
   identity, queue context, or external state. Mark unresolved dispatch and service
   behavior as unknown rather than inventing implementation details. Do not load
   credential values to explain configuration keys.

## Result

Explain the journey in execution order with exact file/line citations and names
the reader can search. Use a diagram or table when it clarifies relationships;
collapse incidental internals while retaining consequential branches. Preserve
exact paths instead of shortening them to fit a diagram. List material unknowns
and the evidence that would resolve them. Save an explanation only when requested.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
