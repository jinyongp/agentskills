---
name: proposal
description: "Prepare self-contained proposals for problems, opportunities, or decisions, preserving the context, evidence, constraints, and open questions needed for independent assessment."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Proposal

Prepare or revise a proposal for a problem, opportunity, or decision, including
software, design, operations, and process changes. Preserve the requested audience,
language, format, and destination. Use for assessment by another party, rather than
a product specification or a packet for resuming the same task.

## Core rules

- **Write for the recipient.** Include context that changes validity, approach,
  impact, or verification. Omit incidental consumer project names, internal task
  aliases, and work history; describe their roles when needed. Keep domain rules
  and reasons that affect the decision. Exact source-bound evidence stays exact.
- **Separate claims.** Distinguish observations, expectations, decisions, causal
  hypotheses, and suggested solutions. Give material claims precise sources and
  tested states. Code behavior does not establish a documented guarantee; an
  inconvenient behavior alone does not establish a defect.
- **Propose outcomes.** Separate required outcomes and preservation conditions
  from preferred mechanisms. Uninvestigated areas are gaps, not agreed exclusions.
  Root-cause proof and exhaustive impact analysis are not prerequisites.
- **Drafting only.** A proposal does not authorize implementation, submission,
  messages, or commitments on the recipient's behalf.

For technical evidence, inaccessible sources, or transfer across teams/repositories,
read [references/proposal-contract.md](references/proposal-contract.md). It defines
the portable contract and conditional evidence without imposing a document layout.

## Prepare and review

1. **Recover the need.** Establish recipient, target/baseline, decisions, limits,
   and available evidence. Establish the outcome behind a requested mechanism.
   Inspect relevant sources before asking for available facts; ask only when missing
   context changes the proposal's meaning.
2. **Explain the problem.** Give the use case, triggering scenario, actual
   consequences, and desired outcome.
   Define unfamiliar terms, preconditions, important exceptions, and why a rule or
   constraint exists. Separate consumer requirements from target guarantees.
3. **Transfer evidence.** Attach accessible, precise sources and tested states.
   Supply permitted excerpts or examples when access differs. Reduce examples while
   preserving the triggering conditions and meaningful results. Keep observed
   behavior separate from suspected causes. Name missing artifacts, unfinished
   investigation, and recovery needs. An inaccessible link does not transfer content.
4. **Frame the decision.** State observable success, preservation conditions,
   relevant workarounds, alternatives, tradeoffs, exclusions, and unknowns.
5. **Review the actual draft.** Read [references/reader-review.md](references/reader-review.md)
   and review the draft from the recipient's available context. Revise supported
   gaps, then check changes against sources. Identify the passage and the decision
   each gap obstructs; repeating the rules does not evaluate the draft. Keep
   unperformed checks pending and preserve reasons and accepted deferrals.

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
