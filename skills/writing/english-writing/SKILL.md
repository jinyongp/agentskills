---
name: english-writing
description: "Create, edit, or review English reader-facing prose for clear syntax, appropriate register, and natural voice. Use for English writing or translationese concerns; ordinary English conversation alone does not require this skill."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# English writing

## Scope and composition

Create, edit, or review the requested English passages. Follow the user's mode,
audience, medium, and degree of intervention. This skill works alone; when a
drafting or editing workflow is also loaded, refine its language within that
workflow and return one result. Review-only requests produce findings, not edits.
Select by deliverable language; preserve other-language quotations, code, and names.

## Meaning and voice

Use supplied or verified evidence. Preserve attribution, negation, quantities,
conditions, uncertainty, commitments, and intentional personality. Editing does
not authorize invented facts or translation. Inspect relevant adjacent context;
for large sources, state inspected sections and material omissions. Ask only about
ambiguities that materially affect meaning or the requested voice.

## English expression

- Match vocabulary, rhythm, and directness to the reader and genre. Follow requested
  spelling and usage conventions, or an established publication style; use them
  consistently. Retain exact quotations, identifiers, and proper names.
- Keep subjects, verbs, and modifiers close enough to make relationships clear.
  Resolve ambiguous pronouns and misplaced qualifiers. Split or reshape a sentence
  when relationships become hard to follow, not because it exceeds a fixed length.
- Prefer concrete verbs when noun-heavy phrasing obscures the action:
  "conduct an assessment of" can become "assess". Keep established technical nouns
  and useful abstractions; scientific or legal prose may need greater precision.
- Use active voice when the actor matters. Use passive voice when the process,
  recipient, or unknown actor is the point. "The samples were stored at -20°C"
  need not acquire an invented researcher merely to avoid a passive construction.
- Preserve modal strength and scope: may, can, should, and must are not interchangeable.
  Keep distinctions such as some versus all, association versus cause, and estimate
  versus measured result. Check that a moved only or not still modifies the same claim.
- Replace stock praise, inflated significance, and vague implications with the
  actual point. Give transitions a real logical role. Keep intentional repetition,
  idioms, humor, contractions, or restrained formality when they suit the voice.
- Use parallelism and punctuation to clarify relationships. Lists should group
  comparable items; paragraphs need connected thought. Em dashes, sentence fragments,
  and words such as "robust" are contextual choices, not proof of poor writing or
  AI authorship. Avoid mechanical synonym swaps or a forced conversational tone.

## Result

Return the requested draft, revision, or supported review findings. In editing,
compare source and result for meaning and register changes; retain passages that
already work. Keep explanations separate and brief unless requested.
Use relevant spelling or terminology checks when available; distinguish linguistic
judgment from verified facts and claims about AI authorship.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
