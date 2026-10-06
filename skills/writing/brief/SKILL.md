---
name: brief
description: "Present status, progress, and handover updates as a scannable briefing when requested. Distinguish completed, active, pending, and unknown states; retain blockers and real next decisions."
license: AGPL-3.0
metadata:
  author: jinyongp
  category: writing
---

# Brief

Help a reader skimming for outcomes, changes, and blockers. A missing status and a
buried status both prevent action.

## Scope

Use for requested status briefings, progress updates, and standup-style summaries.
Report the supplied or verified state. This is a presentation style; it does not
replace investigation, implementation, or preservation of handoff context.
Follow the user's language and requested output format.

## Briefing

- Open with a one-line takeaway containing the outcome and any blocker. It must
  stand alone without requiring the reader to inspect the board.
- Show relevant states as a compact checklist: ✅ completed, 🟡 in progress,
  ⬜ not started, ❔ unknown. Bold the subject, then give a short factual clause.
  Unknown and not started are different; an unchecked item proves neither.
- Group by the reader's actual concern rather than inventing rows to fill a template.
  Keep all decision-changing numbers, dates, thresholds, conditions, risks, and
  blockers exact. Qualify status with its real evidence and limits.
- Give a blocker its own clear line. Mark an unknown state and say what evidence
  would resolve it. Infer a status only when supported; distinguish inference
  from an observed result.
- Show real pending choices as a short numbered list with a clear action label.
  Name an owner or deadline only when known. Ask for a choice only when the work
  actually requires one; finish already-authorized steps you can perform.
- Use short lines and blank-line-separated prose blocks, one idea each. Use at
  most one structural emoji per line. Define unfamiliar terms briefly.
- A request for explanation or full detail gets the necessary reasoning and all
  material conditions. Switch to prose or a table if a checklist obscures it.
- When asked to write the actual update message or note, return that deliverable
  ready to use without surrounding commentary.
- End with a real next action or pending decision when present. A fully complete
  update can end with its final factual state.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
