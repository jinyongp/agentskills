---
name: write
description: "Draft reader-facing prose from a brief or evidence, with a clear purpose, appropriate voice, and supported claims. Use for new documents, articles, messages, or product copy; use rewrite for editing existing prose."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Write

Create new reader-facing prose in the requested language, medium, and voice.
Use the brief and supplied evidence; ask only for gaps that materially affect the
message. Writing permission covers the selected deliverable; publication has its
own scope. For existing prose, follow the requested editing scope instead.

## Core rules

- **Evidence before specificity.** Distinguish supplied claims, verified facts,
  and interpretation. Preserve conditions, attribution, uncertainty, and exceptions.
  Use evidence for numbers, quotations, results, and concrete examples; label
  hypothetical examples. Expose gaps instead of inventing facts or personal experience.
- **Reader purpose first.** Organize around what the reader should understand or
  do. Keep qualifications beside claims and examples beside their points. Narrative
  may reveal its answer later; instructional and decision prose lead with it.

## Draft and check

1. **Purpose.** Identify what the reader needs to understand or do. Infer structure from
   that purpose and the destination; match a supplied voice sample where available.
2. **Sources.** Read relevant material selectively. For large inputs, track sections
   inspected and material gaps; retrieve context needed for claims before drafting.
   When the brief is raw notes, separate collecting useful material from ordering
   the argument. Preserve supplied anecdotes, quotations and distinctive wording
   as sources; drafting need not consume every fragment or rewrite the source file.
3. **Structure.** Introduce terms before relying on them. Use headings for findable topics
   and lists for comparable items or ordered steps; connect reasoning in prose.
   Check what the audience already knows; establish missing ideas before later
   passages depend on them. Keep a paragraph when removing it loses a needed step,
   reason, qualification or intended effect. Avoid definition-heavy openings.
4. **Substance.** For praise or a conclusion, identify the claim or evidence it adds. Replace an
   unsupported evaluation with the supplied fact; remove a restatement that adds no
   consequence or qualification. Keep intentional personality and repetition. Judge
   wording in context; word bans, sentence quotas, and AI detectors cannot establish
   quality or authorship.
5. **Fidelity.** Check the draft against the brief and evidence for missing context, changed
   certainty, unsupported promises, accidental implications, and register drift.

## Language and composition

This skill works alone across languages. Follow the deliverable's language rather
than the conversation's language; preserve code, quotations, and names as required.
When language-specific guidance is also loaded, apply it to the relevant passages
within this workflow. Produce one deliverable, without repeating the drafting pass.

## Result

Return prose ready for its destination. Explain material assumptions or evidence
gaps only when needed; keep process notes separate from the finished text.
Reuse relevant document checks when available. Report remaining factual or scope
gaps honestly; polish alone does not verify a claim.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
