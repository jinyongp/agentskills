---
name: animation-vocabulary
description: "Name or explain motion effects from a visual description, reference, or vague terminology. Use for animation vocabulary and disambiguation on web or native; naming alone does not authorize implementation."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Vocabulary

## Scope

Name or explain the motion described or shown by the user, on web or native.
A vocabulary question calls for terminology, not code edits or a motion audit.
Use the user's language and preserve any requested depth or format.

Read only the relevant section of [references/glossary.md](references/glossary.md)
when mapping an effect or distinguishing close terms: appearance, continuity,
scroll/gesture, timing, or implementation technique. The glossary is a compact
aid, not an exhaustive authority or a closed vocabulary.

## Map the effect

1. Extract observable behavior: which object changes, which property appears to
   change, what triggers it, and whether it follows input continuously or plays
   afterward. Use selected relevant evidence; a single frame cannot reveal timing.
2. Name the recognized term that best fits. Separate a visual effect from its easing,
   physical behavior, orchestration, and implementation. A spring can drive a slide;
   an implementation technique is not necessarily the visible effect's name.
3. When multiple terms fit, give the key observable distinction. Ask one short
   question or request the needed observation only when that distinction matters.
   Keep uncertainty explicit instead of assigning a precise name to missing evidence.
4. Describe a compound effect using its actual parts when no single term fits.
   Acknowledge common aliases and tool-specific naming. Do not invent an official
   label or restrict a valid term merely because it is absent from the glossary.
5. Keep the answer proportional: lead with the term and a brief explanation tied
   to the user's example. Add close alternatives or implementation hints only when
   they help the request; tool/library selection remains a separate decision.

## Result

Return a usable name and meaning, with a disambiguating detail or caveat where
needed. For a requested implementation brief, include trigger, start/end state,
interaction, and essential constraints; reference recoverable project facts.
Keep definitions accurate without copying a long glossary into the conversation.
An approximate label is acceptable when clearly identified as approximate.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
