---
name: korean-writing
description: "Create, edit, or review Korean reader-facing prose for natural syntax, register, and information flow. Use for Korean writing or translationese concerns; ordinary Korean conversation alone does not require this skill."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Korean writing

Create, edit, or review Korean passages. Follow the user's mode,
audience, medium, and degree of intervention. This skill works alone; with a
drafting/editing workflow, refine its language and return one result within that
scope. Review-only requests produce findings, not edits.
Select by deliverable language; preserve other-language quotations, code, and names.

## Core rules

- **Meaning before brevity.** Preserve attribution, negation, quantities,
conditions, uncertainty, commitments, and intentional personality. Editing does
not authorize invented facts or translation. Use supplied or verified evidence.
- **Context before correction.** Inspect relevant adjacent context;
for large sources, state coverage and material omissions. Ask only about
ambiguities that materially affect meaning or the requested voice.

Read [references/diagnosis.md](references/diagnosis.md) for ambiguous referents,
noun chains, layered predicates, or connectors; use matching examples only.

## Korean expression

- **Speech level.** Choose from the request, destination, or voice sample.
  Keep sentence endings coherent with that relationship. Vary rhythm through
  sentence construction, not arbitrary switches between polite and plain endings.
  Distinguish honorifics for people from politeness toward the reader.
- **Referents.** Check who acts, what the predicate describes, and which noun a modifier qualifies.
  When a delayed predicate or stacked modifier leaves two plausible readings,
  move the qualifier beside its noun or turn it into a clause. Omit recoverable subjects;
  keep them when omission would confuse who acts. Use pronouns such as "당신" or
  "그것" only when they fit the relationship and referent.
- **Noun chains.** Check stacked modifiers, nominalized predicates, and repeated "의".
  Turn them into concrete clauses or verbs when that clarifies the relationship.
  Preserve established terminology and meaningful possessives; these forms are
  not errors merely because they occur.
- **Predicates.** Prefer direct predicates where they express the intended action:
  "검토를 진행한다" can become "검토한다". Keep meaningful aspect and modality:
  "검토하고 있다" describes an ongoing action; "할 수 있다" may express permission
  or possibility. Shortening must preserve those distinctions.
- **Unknown actors.** Use passive or impersonal constructions when the actor is unknown or irrelevant.
  "결과는 아직 확인되지 않았다" need not invent someone who checked it.
  Repair awkward layered predicates when meaning permits, not every passive.
- **Logical links.** Use connectors for a real logical relation. Remove repeated restatements and
  automatic paragraph summaries when they add no information. Check that an
  added "따라서" or "하지만" does not invent causation or opposition.
- **Genre.** Dialogue, essays, notices, technical documents, and interface copy
  need different rhythm and explicitness. Keep idiomatic short sentences, useful
  repetition, and deliberate humor. Evaluate spacing and punctuation in context;
  comma counts, fixed length thresholds, and ending quotas do not measure quality.

## Result

Return the requested draft, revision, or supported review findings. In editing,
compare source and result for meaning and speech-level changes; retain passages
that already work. Keep explanations separate and brief unless requested.
Use relevant spelling or terminology checks when available; distinguish linguistic
judgment from verified facts and claims about AI authorship.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
