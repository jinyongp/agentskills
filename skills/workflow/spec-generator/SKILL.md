---
name: spec-generator
description: "Define what a product or feature should do from an idea, notes, or evidence. Use for requirements, roles, scope, and feature flows; implementation plans remain separate."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Spec Generator

Create or revise a product specification from an idea, notes, sketches, research,
or an existing document. Capture the intended product behavior and limits;
implementation scheduling, code changes, and publication need their own request.
Follow the requested language, structure, and destination. Return inline unless
a file is requested or an existing specification is being updated.

## Core rules

- **Separate decisions.** Distinguish confirmed requirements, proposed defaults,
  and unresolved choices. Resolve ambiguity affecting permissions, data lifecycle,
  external effects, or acceptance. Reuse project constraints; ask about technology
  only when it changes a product decision or a technical specification is requested.
- **Preserve scope.** Keep agreed omissions. Missing evidence is an open question,
  not permission to invent features, audiences, or reliability requirements.
- **Observable acceptance.** Every promised outcome needs a concrete acceptance
  example; distinguish requirements from illustrations and optional extensions.

Read [references/feature-flows.md](references/feature-flows.md) when expanding a
specification into feature flows or reconciling changes across product documents.

## Define behavior

1. **Context.** Recover goal, actors, evidence, and accepted exclusions.
   For an existing product, inspect relevant behavior and definitions rather than
   treating a sketch or today's implementation as the whole requirement.
2. **Choices.** Resolve consequential ambiguity under the decision rules.
3. **Journeys.** Describe who starts them, required state, observable
   outcomes, and relevant rejection or recovery behavior. Include background,
   API, or staff journeys when required; a feature need not have a screen.
4. **Shared rules.** Specify ownership/access, meaningful state transitions,
   data retention/deletion, integrations, and limits that affect a journey.
5. **Organization.** Follow the reader's decisions. Useful sections include purpose,
   actors, journeys, constraints, acceptance, exclusions, and open questions;
   adapt them to the product instead of imposing a universal document layout.
   Keep technical choices separate from product behavior when either is unsettled.
6. **Acceptance.** Check promised outcomes against examples. When editing,
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
