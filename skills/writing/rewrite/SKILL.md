---
name: rewrite
description: "Revise existing reader-facing prose for clarity and natural voice while preserving facts, intent, qualifications, and author style. Use for editing documents or product copy; conversational brevity alone does not require this skill."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Rewrite

Revise the supplied or selected prose for its intended readers and medium.
Follow the requested language, voice, degree of editing, and publication format.
An editing request authorizes the selected text; publication needs its own scope.
For a review-only request, return supported recommendations without editing files.

## Core rules

- **Preserve claims.** Keep names, numbers, dates, quotations, citations, terms,
  commitments, uncertainty, and exceptions accurate. Distinguish source claims
  from verified facts. Add detail only from supplied or verified evidence within
  scope; expose gaps instead of inventing specificity or strengthening claims.
- **Preserve voice.** Keep intentional humor, formality, unusual phrasing, and
  personality. Judge phrases in context; punctuation or vocabulary alone does not
  establish poor writing or AI authorship. Avoid word bans and mechanical scrubbing.

## Revise and compare

1. **Intent.** Identify message, reader, and constraints from the source and request.
   Ask only when an unresolved choice materially affects meaning or disclosure.
   Use a supplied voice sample as evidence of desired rhythm and vocabulary.
2. **Context.** Read selected text and enough adjacent context to preserve meaning.
   For long documents, select relevant sections and follow references as needed;
   track omitted sections and limit conclusions to what was inspected.
3. **Organization.** Arrange the answer or requested action and supporting passages.
   - **Order:** Put a buried answer before its support in instructional/decision
     prose; preserve deliberate narrative sequencing. Group examples with their
     point and explain needed concepts before relying on them.
   - **Clarity:** Name actors where omission obscures responsibility; keep modifiers
     beside their claims.
   - **Relevance:** Cut praise or repeated conclusions only when they add no supported
     claim or qualification. Retain needed steps, reasons, qualifications, and effects;
     relocate competing topics. Missing examples need evidence, a labeled hypothetical
     illustration, or a narrower claim.
4. **Fidelity.** Compare the revision with the source for changed meaning, lost qualifications,
   invented evidence, and unnecessary edits. A request for substantial compression
   may omit secondary material; preserve decision-changing context and disclose
   material omissions. Resolve clarity problems without flattening the voice.
   Check negation, quantities, causal links, time, and who acts or is obligated;
   a smoother sentence can silently change any of these.

## Language and composition

This skill works alone across languages. Follow the requested output language;
editing alone does not authorize translation. When language-specific guidance is
also loaded, apply it to the relevant passages within this workflow and return one
result. Review-only mode remains read-only regardless of accompanying style guidance.

## Result

Return the revised text ready for its destination. Include a short explanation
only when requested or needed for material changes or unresolved claims. Preserve
the original where required. Use existing spelling, link, or document checks when
useful; word-count or banned-word scores alone do not establish writing quality.

For review-only requests, identify the passage, reader impact, and suggested change;
keep already effective prose. Limit conclusions to the inspected text.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
