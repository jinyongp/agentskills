---
name: proposal
description: "Prepare self-contained proposals for problems, opportunities, or decisions, preserving the context, evidence, constraints, and open questions needed for independent assessment."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Proposal

Prepare proposals for another party's assessment across software, design,
operations, and process changes. Preserve requested audience, language, format,
and destination. Product specifications and task handoffs are separate outcomes.

## Core rules

- **Write for the recipient.** Include context that changes validity, approach,
  impact, or verification. Omit incidental consumer project names, internal task
  aliases, and work history. Keep domain rules and reasons that affect the decision.
  Exact source-bound evidence stays exact.
- **Separate claims.** Distinguish observations, expectations, decisions, causal
  hypotheses, and suggested solutions. Give material claims precise sources and
  tested states. Code behavior does not establish a documented guarantee; an
  inconvenient behavior alone does not establish a defect.
- **Propose a decision.** State what the recipient is asked to assess or decide.
  Separate proposed goals, existing constraints, and accepted requirements from
  preferred mechanisms. Uninvestigated areas are gaps, not agreed exclusions.
- **Keep commitments scoped.** Success measures explain expected value; they are
  not recipient completion duties. Do not invent owners, deadlines, implementation
  or deployment commitments. Preserve explicitly requested delivery scope.
  Drafting or accepting a proposal does not itself authorize execution or submission.

For technical evidence, inaccessible sources, or transfer across teams/repositories,
read [references/proposal-contract.md](references/proposal-contract.md) for the
portable contract and conditional evidence, without a fixed layout.

## Prepare and review

1. **Recover the need.** Establish recipient, target/baseline, requested decision,
   limits, evidence, and the outcome behind a requested mechanism. Inspect available
   sources before asking about consequential gaps.
2. **Explain the problem.** Give the use case, triggering scenario, actual
   consequences, and desired outcome.
   Explain terms, preconditions, exceptions, and reasons for constraints.
   Separate consumer requirements from target guarantees.
3. **Transfer evidence.** Attach precise sources and tested states. When access
   differs, supply permitted excerpts or examples preserving triggers and results.
   Separate observations from suspected causes. Name missing artifacts, unfinished
   investigation, and recovery needs; inaccessible links do not transfer content.
4. **Frame the decision.** Explain expected value, preservation conditions,
   alternatives, tradeoffs, and unknowns. Offer success measures as proposed targets
   or evaluation ideas. Include a detailed work plan, acceptance checklist, or rollout
   scope only when requested or already agreed. Proof of cause is not a prerequisite.
5. **Review the actual draft.** Read [references/reader-review.md](references/reader-review.md)
   and review from the recipient's available context. Repair consequential gaps,
   check changes against sources, and preserve accepted deferrals. Keep unperformed
   checks pending; do not present future work as agreed duties.

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
