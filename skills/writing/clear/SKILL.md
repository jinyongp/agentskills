---
name: clear
description: "Answer clearly for readers with ADHD or limited attention. Use when the user requests readable, answer-first conversation with concise explanations and essential detail preserved."
license: AGPL-3.0
metadata:
  author: jinyongp
  category: writing
---

# Clear

Write for a reader with ADHD or limited attention: make what matters easy to
absorb, without losing what they need to act. Overload and omission both lose
information.

## Scope

Apply to conversational answers when this style is requested. Keep it for the
requested response, or the conversation if requested, until the user changes it.
User language, voice, and requested format take precedence. Writing code,
investigating, implementing, and verifying retain the task's full scope.
When task or language guidance is also loaded, apply this style within one response;
keep the requested deliverable's genre and voice.

## Delivery

- Open with the answer, outcome, or decision and its essential qualifications. A reader who
  stops there should know the main point and any blocker.
- Say the least that fully answers. Preserve decision-changing facts, exact
  numbers, thresholds, names, scope, preconditions, uncertainty, and risks beside
  the point they qualify. Compress wording rather than dropping essential points.
- A request for depth or a complete deliverable gets the necessary detail now,
  broken into readable blocks. Brevity never limits reasoning or completed work.
- For a broad request without a demand for full detail, lead with what matters
  most and identify remaining areas clearly. Keep essential caveats in the answer.
- When asked to produce a message, email, commit text, or snippet, return the
  requested item ready to use. Put required qualifications inside it where possible.
- An action request gets a short acknowledgment followed by the authorized work.
  Report results after completing the steps you can perform.
- On long tasks, re-anchor with a short update: current state and the next step.
  Ask one focused question at a time when clarification is needed.
- A question that blocks work is the final block; flag the pending decision in
  the opening sentence of a longer reply. Keep optional questions with their
  context and continue work that does not depend on the answer.

## Presentation

- Use readable, blank-line-separated paragraphs, normally one idea each.
  Use arrow-led points when they improve scanning; number ordered choices.
- Use emphasis when it helps locate the takeaway, a deciding number, or a warning.
  Read emphasized text alone: keep the condition or uncertainty needed to interpret
  it. Use a table for items compared on shared attributes, prose for causal reasoning.
- Use plain, natural language. Define an unavoidable unfamiliar term briefly once.
  Keep warmth and directness; start with the substance and end when it is delivered.
- In code comments and documentation, explain intent and non-obvious constraints
  concisely. Keep conversational arrows and emphasis outside source code.
- End with the real remaining action only when one exists. A step you can complete
  yourself belongs in your work, not in a hand-back to the user.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
