---
name: animation-opportunities
description: "Identify a few places where motion would improve feedback, orientation, or continuity in a web or native interface. Use for motion opportunity discovery; return recommendations without implementing or expanding product scope."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Opportunities

## Scope

Find worthwhile motion opportunities in the selected web or native interface.
Return recommendations; source edits or a broader redesign need an implementation
request. Follow product direction, current flows, tools, and platform requirements.
Inspect relevant journeys and component states rather than scanning syntax for
missing animation. An interface can be complete with no added motion.

## Discovery

1. Identify important user actions and moments of uncertainty: what changed, where
   content went, whether an action registered, or how a gesture will settle.
   Inspect selected screens, state transitions, and existing feedback with bounded
   project tooling. State omitted areas; retrieve necessary detail before conclusions.
2. Consider feedback, spatial continuity, progressive disclosure, and direct
   manipulation. Gestures, sheets, route changes, and keyboard-aware positioning
   are useful candidates on web as well as native; none require motion by default.
3. For each candidate, name the user problem and the information motion adds.
   Compare with an instant update, clearer text, stable layout, or existing platform
   behavior. Prefer the cheaper sufficient solution; preserve an already good flow.
4. Consider frequency, urgency, distance, repetition, and attention cost. A frequent
   action may benefit from subtle feedback but should remain promptly operable.
   Decorative motion is appropriate only for a requested identity or experience
   goal with understood cost. Avoid background motion that competes with the task.
5. Check interruption, cancellation, nested scrolling, focus, keyboard alternatives,
   reduced motion, and supported environments. A proposal must preserve the outcome
   for users who cannot or choose not to perform its gesture.
6. Reuse current primitives and tokens. Account for performance and implementation
   cost; describe suspected constraints as hypotheses until traced or measured.
   Surface missing capabilities without automatically installing tools or expanding
   product behavior.

## Result

Recommend the few opportunities with a demonstrated benefit. For each, give the
location/trigger, user benefit, proposed behavior, reduced-motion or instant
alternative, relevant implementation constraints, and a useful acceptance check.
Reference existing code for recoverable details; include essential new decisions.

Explain why a plausible candidate should stay instant when it materially informs
the recommendation, without an exhaustive rejected-candidate catalog. An empty
recommendation set is valid. Report inspected scope, source versus runtime evidence,
and gaps; discovery alone does not prove that a proposal will improve usability.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
