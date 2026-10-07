---
name: korean-writing
description: "Create, edit, or review Korean reader-facing prose for natural syntax, register, and information flow. Use for Korean writing or translationese concerns; ordinary Korean conversation alone does not require this skill."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Korean writing

## Scope and composition

Create, edit, or review the requested Korean passages. Follow the user's mode,
audience, medium, and degree of intervention. This skill works alone; when a
drafting or editing workflow is also loaded, refine its language within that
workflow and return one result. Review-only requests produce findings, not edits.
Select by deliverable language; preserve other-language quotations, code, and names.

Read [references/diagnosis.md](references/diagnosis.md) for ambiguous referents,
noun chains, layered predicates, or connectors; use only the matching examples.

## Meaning and voice

Use supplied or verified evidence. Preserve attribution, negation, quantities,
conditions, uncertainty, commitments, and intentional personality. Editing does
not authorize invented facts or translation. Inspect relevant adjacent context;
for large sources, state inspected sections and material omissions. Ask only about
ambiguities that materially affect meaning or the requested voice.

## Korean expression

- Choose an appropriate speech level from the request, destination, or voice sample.
  Keep sentence endings coherent with that relationship. Vary rhythm through
  sentence construction, not arbitrary switches between polite and plain endings.
  Distinguish honorifics for people from politeness toward the reader.
- Check who acts, what the predicate describes, and which noun a modifier qualifies.
  When a delayed predicate or stacked modifier leaves two plausible readings,
  move the qualifier beside its noun or turn it into a clause. Omit recoverable subjects;
  keep them when omission would confuse who acts. Use pronouns such as "당신" or
  "그것" only when they fit the relationship and referent.
- Check stacked noun modifiers, nominalized predicates, and repetitive "의" chains.
  Turn them into concrete clauses or verbs when that clarifies the relationship.
  Preserve established terminology and meaningful possessives; these forms are
  not errors merely because they occur.
- Prefer direct predicates where they express the intended action:
  "검토를 진행한다" can become "검토한다". Keep meaningful aspect and modality:
  "검토하고 있다" describes an ongoing action; "할 수 있다" may express permission
  or possibility. Shortening must preserve those distinctions.
- Use passive or impersonal constructions when the actor is unknown or irrelevant.
  "결과는 아직 확인되지 않았다" need not invent someone who checked it.
  Repair awkward layered predicates when meaning permits, not every passive.
- Use connectors for a real logical relation. Remove repeated restatements and
  automatic paragraph summaries when they add no information. Check that an
  added "따라서" or "하지만" does not invent causation or opposition.
- Respect genre: dialogue, essays, notices, technical documents, and interface copy
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
