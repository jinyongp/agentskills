---
name: retro
description: "Review a specified work session for observed process friction and propose proportionate improvements to navigation, checks, instructions, and tool output. Retrospective analysis does not change code or agent settings."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Retro

Review the specified session, or the current session when none is named, for
observed friction in how work was done. This is process analysis, not another
code audit. Return proposals by default; apply only explicitly requested or
already authorized improvements within their selected project/settings scope.

## Core rules

- **Observed friction.** Tie each candidate to an event, consequence, and smallest
  preventive change. Distinguish recurring patterns from a single high-impact
  failure. A missing hook or large file alone is no finding. Do not invent elapsed
  time, token savings, or agent motives.
- **Proportionate correction.** Reuse existing mechanisms and preserve accepted
  tradeoffs. A session does not automatically justify another permanent rule.

## Investigate and propose

1. **Evidence.** Recover goal, accepted limits, and primary session evidence:
   failed commands, repeated searches, corrections, retries, or missed checks.
   Start with an index/summary and inspect only relevant log spans; redact secrets.
   Name unavailable logs and narrow conclusions to the inspected evidence.
2. **Candidates.** Apply the event/consequence criteria before proposing a change.
3. **Existing mechanisms.** Check before adding:
   - Repeated navigation: improve the relevant pointer or query, retaining one
     maintained definition instead of duplicating repository facts.
   - Mechanical mistake: reuse a suitable existing check; repair its wiring when
     that caused the miss. Add a check only for a named uncovered failure with
     justified maintenance cost, not automatically another test, hook, or CI job.
   - Judgment failure: clarify the applicable decision and evidence in the narrow
     instruction that owns it. Reviewers still need relevant contracts and callers.
   - Expensive output: use existing filters or bounded summaries with recoverable
     omissions. Introduce a helper only for repeated mechanical work.
   - Missing access: identify the needed evidence and least access that supplies it;
     access grants, credentials, and service changes retain their own authorization.
4. **Priority.** Rank by observed impact, recurrence evidence, implementation cost,
   and uncertainty. Keep accepted tradeoffs intact; do not reopen excluded features
   or recommend deleting an instruction solely because this session did not use it.
   When instructions conflict, express the current choice at its authoritative
   source and preserve only necessary decision history separately.
5. **Authorized changes.** Apply selected improvements when requested and verify the
   motivating failure where practical. Report expected benefit separately from
   observed recovery; one successful replay does not establish general productivity.

## Result

Return supported proposals with event/source, consequence, change, and a check for
success. State evidence gaps and any changes actually applied. No findings is valid;
do not manufacture a new permanent rule for every session.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
