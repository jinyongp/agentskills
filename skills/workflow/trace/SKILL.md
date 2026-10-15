---
name: trace
description: "Explain one codebase journey by following its actual trigger, calls, data effects, and outcome with source citations. Use for how-it-works questions, not defect diagnosis."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Trace

## Scope

Explain one journey through a codebase: its trigger, control/data flow, side
effects, and outcome. Use for how-it-works questions. Diagnosing a failing journey,
proposing fixes, or changing code requires that task scope; tracing alone is read-only.

## Procedure

1. Translate the question into a specific action and outcome. Narrow a broad topic
   to a representative journey and disclose that choice; ask when choosing a path
   would answer a materially different question.
2. Locate an actual caller or entry point: a UI action, route, command, event,
   scheduled invocation, or configured integration. Search relevant registrations
   and callers before declaring code unreachable. If no trigger is found, report
   the searched scope and explain the hypothetical path separately.
3. Follow calls and values toward the answer, including relevant guards, validation,
   persistence, async handoffs, and error/recovery branches. Trace across folders;
   stop following unrelated callers once the question is answered.
4. Read the lines supporting each hop. A symbol search is a lead, not a verified
   edge. For framework conventions, generated dispatch, database effects, or
   vendor behavior, identify the configuration/version and implementation evidence
   available. Cite the app reliance separately from proof of the implicit mechanism.
5. Record preconditions that change the route or outcome, such as flags, caller
   identity, queue context, or external state. Mark unresolved dispatch and service
   behavior as unknown rather than inventing implementation details. Do not load
   credential values to explain configuration keys.

## Result

Explain the journey in execution order with exact file/line citations and names
the reader can search. Use a diagram or table when it clarifies relationships;
collapse incidental internals while retaining consequential branches. Preserve
exact paths instead of shortening them to fit a diagram. List material unknowns
and the evidence that would resolve them. Static tracing does not prove a run
occurred or establish runtime state. Save an explanation only when requested.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
