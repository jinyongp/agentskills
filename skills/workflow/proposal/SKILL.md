---
name: proposal
description: "Prepare self-contained proposals for problems, opportunities, or decisions, preserving the context, evidence, constraints, and open questions needed for independent assessment."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Proposal

## Scope

Prepare or revise a proposal for a problem, opportunity, or decision, including
software, design, operations, and process changes. Preserve the requested audience,
language, format, and destination. Drafting does not authorize implementation,
submission, or messages. Use when someone needs a proposal to assess, rather than
a product specification or a packet for resuming the same task.

## Information contract

Carry the target/baseline, problem/use case, domain rules and reasons, evidence,
desired outcome, success and preservation conditions, scope/alternatives, and
unknowns. Label observations, expectations, hypotheses, and suggested solutions
separately. Include context whose absence could change validity, approach, impact,
or verification. Keep necessary service-specific context; generalizing it must
preserve its conditions and meaning.

For technical evidence, inaccessible sources, or transfer across teams/repositories,
read [references/proposal-contract.md](references/proposal-contract.md). It defines
the portable contract and conditional evidence without imposing a document layout.

## Procedure

1. Recover the actual need, recipient, target, current decisions, accepted limits,
   and available evidence. Establish the outcome behind a requested mechanism.
   Inspect relevant sources before asking for available facts; ask only when missing
   context changes the proposal's meaning.
2. Explain the triggering scenario, actual consequences, and desired outcome.
   Define unfamiliar terms, preconditions, important exceptions, and why a rule or
   constraint exists. Separate a consumer's requirement from the target's documented
   guarantees; an inconvenient behavior alone does not establish a defect.
3. Attach evidence with its source and tested state. Reduce examples only while
   preserving the triggering conditions and meaningful results. Keep observed
   behavior separate from suspected causes. Root-cause proof and exhaustive impact
   analysis are not prerequisites for proposing; name unfinished investigation.
4. Express observable success and behavior that must remain valid. Separate required
   outcomes from suggested mechanisms. Include relevant workarounds, alternatives,
   tradeoffs, and exclusions without inventing decisions or commitments for recipients.
   Uninvestigated or unmentioned areas are coverage gaps, not agreed exclusions.
5. Make the packet usable without this conversation or private memory. Include
   necessary rationale and accessible, precise source pointers; supply permitted
   excerpts or examples when access differs. Name missing artifacts and recovery
   needs. Never claim an inaccessible link transfers its contents.
6. Before delivery, read [references/reader-review.md](references/reader-review.md)
   and review the draft from the recipient's available context. Revise supported
   gaps, then check changes against sources. Unperformed checks remain pending;
   preserve reasons and accepted deferrals when updating dependent statements.

## Result

Return the proposal inline unless a file/update was requested. Adapt its structure
to the recipient; omit irrelevant fields, not consequential unknowns. Distinguish
supported claims, recommendations, blocking questions, and optional investigation.
State evidence limits; a complete draft does not establish independent validation
or recipient acceptance.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
