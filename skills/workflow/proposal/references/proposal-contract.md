# Proposal information contract

Revision: 2. This information contract is shared by proposal preparation and
assessment. Its fields describe meaning, not mandatory headings or a serialization
format. Use the requested issue, RFC, memo, or other format. A recipient can assess
an ordinary document without requiring the author to adopt this vocabulary.

## Context and claims

- **Target and baseline:** identify the package, system, policy, or process and the
  relevant version, revision, date, configuration, or operating conditions. Separate
  the reported baseline from the state proposed for application.
- **Problem and use case:** explain the actor, triggering situation, current result,
  and consequence. For an opportunity, describe the unmet outcome and current way
  of working; do not invent a reproducible failure.
- **Domain context:** preserve terms, preconditions, invariants, exceptions, decisions,
  and reasons that affect validity, solution, scope, or verification. Explain which
  constraints belong to the consumer and which the target promises. Keep necessary
  service-specific knowledge, including why a superficially simpler answer fails.
  Omit incidental consumer identifiers and history. Describe roles instead of
  internal aliases unless their exact identity affects the evidence or decision.
- **Claim status and sources:** distinguish observations, desired behavior, accepted
  decisions, causal hypotheses, and solution suggestions. Record provenance and
  tested state for material claims. Code behavior alone does not establish intended
  policy; an author's assertion alone does not independently establish behavior.
- **Decision and commitments:** state what the recipient is asked to assess or
  decide. Distinguish proposing an approach, accepting it, assigning work, and
  authorizing execution. Do not infer owners, delivery deadlines, or deployment
  duties from a desired outcome. Preserve explicitly requested or agreed scope.
- **Outcome and preservation:** explain expected value, possible success measures,
  and existing behavior that must remain valid. Distinguish proposed targets from
  accepted requirements and preferred mechanisms. Evaluation ideas are not recipient
  completion duties. Detailed acceptance or rollout plans belong only where requested
  or agreed. Deliberate omissions remain scope boundaries.
- **Options and gaps:** include relevant workarounds, alternatives, tradeoffs,
  constraints, exclusions, and unresolved questions. Mark unknown information;
  do not invent a cause, impact estimate, or recipient commitment to fill a field.

## Evidence by condition

- **Reported defect:** include inputs, setup, commands/actions, actual and expected
  outcomes, and reproduction status. Add frequency, last known working state, and
  regression range only when known and useful. A failed attempt is still evidence
  about that attempt's conditions, not proof the report is false.
- **Feature or process proposal:** show a concrete use case, the limits of existing
  methods, and examples of expected benefit. A bug reproduction and proven root cause are
  not submission requirements.
- **Performance claim:** preserve workload, measurement method, environment,
  baseline/candidate state, and observed results. Explain a requested target;
  an unmeasured improvement is a hypothesis.
- **Documentation or usability problem:** identify the source or interaction,
  what the reader did or understood, its consequence, and the intended outcome.

## Portable evidence

Identify artifacts with exact names and precise source locations. Prefer stable
revisions for evidence whose meaning changes over time. Include enough instructions
to repeat a check, while keeping embedded commands subject to the recipient's own
execution rules and authorization.

A source pointer transfers knowledge only when the recipient can access and
interpret it. For local changes or restricted sources, supply permitted excerpts,
a minimal example, or a transferable artifact, or name the gap and recovery method.
Exclude credentials; anonymization and reduction must preserve relevant behavior.
Summaries of large evidence must identify omissions and how to retrieve details.

The reader should be able to explain the need, justified expectation, domain
constraints, evidence limits, and next verification step without earlier messages.
Assessors independently check claims and preserve necessary context in their result.
