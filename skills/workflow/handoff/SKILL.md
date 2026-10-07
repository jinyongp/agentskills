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

1. Identify the goal, user decisions and rationale, material assumptions and sources,
   accepted deferrals, temporary constraints, blockers, and next action. Preserve only
   context unavailable from the repository, including agreed limits and why the
   selected scope is sufficient. Read
   [references/current-context.md](references/current-context.md) when corrections
   or changed decisions affect the packet.
2. For recoverable facts, give a precise lookup: file and section, narrow search,
   or scoped command. Include only lookups needed to resume. Repository instructions,
   plans, code, Git state, environment setup, and durable logs stay at their sources.
3. Use the requested or established language; preserve exact identifiers and quotes.
   Omit empty fields. Use an inline packet unless a file or target was requested.
   Include relevant lookups without broad inspections just to fill the packet.
4. Preserve otherwise unavailable evidence that changes the next decision: command,
   result, tested scope/state, or a failed approach's observed cause. Keep audit
   history separate from active instructions. Current queries cannot prove past
   success; pending checks and blockers remain pending.
5. Check that the next action has its target, current decision, and required input
   in the packet or a specific lookup. Confirm referenced files exist and selectors
   locate the needed section; keep broad or mutating commands as pending work.
   If another checkout lacks local changes or an attachment,
   identify the missing artifact and its transfer method. Exclude credentials.

## Packet

Use only the fields needed for this task:

- **Context:** missing intent, decisions and reasons, assumptions and sources,
  deferrals, constraints, authorization boundaries, and unresolved choices.
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

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
