---
name: handoff
description: Prepare or resume work in another session or agent. Preserve context absent from the shared repository and provide targeted ways to find existing facts.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Handoff

## Scope

- Continue the same task in a shared repository. Keep the context needed to decide
  and act; use repository sources for facts the receiver can recover.
- Preparing a handoff uses existing authorization; it does not grant permission
  to send messages, start agents, publish, commit, or expand the task.

## Prepare

1. Identify the active goal, current user decisions and their necessary rationale,
   temporary constraints, unresolved questions, and next action. Preserve only
   context unavailable from the repository. Express current choices positively.
2. For recoverable facts, give a precise lookup: file and section, narrow search,
   or scoped command. Include only lookups needed to resume. Repository instructions,
   plans, code, Git state, environment setup, and durable logs stay at their sources.
3. Keep the handoff short and in English; omit empty fields. Use an inline packet
   unless a file or delivery target was requested. Include only relevant lookup
   commands, without executing broad inspections just to fill the handoff.
4. Record unlogged historical evidence when it affects the next decision: check
   command, result, scope, and tested revision or state. A current repository query
   cannot prove a past test passed. Record pending checks and blockers as such.
5. Verify that the receiver can find the relevant work and take the next step
   without earlier chat. If another checkout lacks local changes or an attachment,
   identify the missing artifact and its transfer method. Exclude credentials.

## Packet

Use only the fields needed for this task:

- **Context:** goal or remaining intent absent from existing plans; current decisions,
  reasons, constraints, authorization boundaries, and unresolved questions.
- **Next:** first concrete action, remaining order where unclear, and blocking input.
- **Lookups:** exact source or bounded query, its purpose, and when it is needed.
  Use task-relevant selectors only; avoid copied file inventories, Git state,
  source text, logs, and instructions already available in the repository.
- **Evidence:** relevant results not stored elsewhere, their tested state, remaining
  checks, and pending external actions with a way to confirm their outcome.

## Resume

1. Read the packet and applicable repository instructions. Follow relevant lookups
   to recover current state; inspect only the paths and refs needed for the next
   action. Preserve staged, unstaged, untracked, and unrelated user work.
2. Resolve material conflicts between the recorded intent and current instructions
   or workspace before affected edits. Ask only for missing context that blocks
   progress; continue independent work when possible.
3. Start with the next action within current authorization. Reuse evidence only
   when its tested scope and state still apply; otherwise rerun the relevant check.
   Confirm pending external outcomes before retrying them.
4. Update the handoff when transferring again. Name inaccessible context and
   required recovery instead of claiming the transfer is complete.
