---
name: spec-generator
description: "Create or revise product requirements, roles, constraints, and feature flows from an idea or evidence. Use for product specifications; implementation plans remain separate."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Spec Generator

## Scope

Create or revise a product specification from an idea, notes, sketches, research,
or an existing document. Capture the intended product behavior and limits;
implementation scheduling, code changes, and publication need their own request.
Follow the requested language, structure, and destination. Return inline unless
a file is requested or an existing specification is being updated.

Read [references/feature-flows.md](references/feature-flows.md) when expanding a
specification into feature flows or reconciling changes across product documents.

## Procedure

1. Recover the product goal, actors, current evidence, and accepted exclusions.
   For an existing product, inspect relevant behavior and definitions rather than
   treating a sketch or today's implementation as the whole requirement.
2. Separate confirmed requirements, proposed defaults, and unresolved decisions.
   Resolve ambiguity that changes permissions, data lifecycle, external effects,
   or acceptance. Reuse known project constraints; ask about technology only when
   it changes a product decision or the user requests a technical specification.
3. Describe important journeys: who starts them, required state, observable
   outcomes, and relevant rejection or recovery behavior. Include background,
   API, or staff journeys when required; a feature need not have a screen.
4. Make shared rules explicit: ownership and access, meaningful state transitions,
   data retention/deletion, integrations, and limits that affect a journey.
   Preserve agreed omissions. Missing evidence is an open question, not permission
   to invent another feature, audience, or reliability requirement.
5. Organize around the reader's decisions. Useful sections include purpose,
   actors, journeys, constraints, acceptance, exclusions, and open questions;
   adapt them to the product instead of imposing a universal document layout.
   Keep technical choices separate from product behavior when either is unsettled.
6. Check each promised outcome against a concrete acceptance example. Distinguish
   a requirement from an illustrative scenario or optional extension. When editing,
   update affected passages and references while preserving unrelated content.

## Result

Return the specification with assumptions and blocking questions visible. Link
source evidence when useful. State which decisions remain before implementation;
a well-written draft is not user acceptance or proof the product already works.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
