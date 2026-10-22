---
name: animation-opportunities
description: "Identify a few places where motion would improve feedback, orientation, or continuity in a web or native interface. Use for motion opportunity discovery; return recommendations without implementing or expanding product scope."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Opportunities

Find worthwhile motion opportunities in the selected web or native interface.
Return recommendations; source edits or a broader redesign need an implementation
request. Follow product direction, current flows, tools, and platform requirements.
Inspect relevant journeys and component states rather than scanning syntax for
missing animation. An interface can be complete with no added motion.

## Core rules

- **Benefit before motion.** Name the user problem and information motion adds.
  Compare with instant updates, clearer text, stable layout, or platform behavior.
  Prefer the cheaper sufficient solution and preserve an already good flow.
- **Preserve alternatives.** The outcome must remain available to users who cannot
  or choose not to perform the proposed gesture.

## Discovery

1. **User uncertainty.** Identify important actions: what changed, where
   content went, whether an action registered, or how a gesture will settle.
   Inspect selected screens, state transitions, and existing feedback with bounded
   project tooling. State omitted areas; retrieve necessary detail before conclusions.
2. **Candidates.** Consider feedback, spatial continuity, progressive disclosure, and direct
   manipulation. Gestures, sheets, route changes, and keyboard-aware positioning
   are useful candidates on web as well as native; none require motion by default.
3. **Attention cost.** Consider frequency, urgency, distance, repetition, and attention. A frequent
   action may benefit from subtle feedback but should remain promptly operable.
   Decorative motion is appropriate only for a requested identity or experience
   goal with understood cost. Avoid background motion that competes with the task.
4. **Access.** Check interruption, cancellation, nested scrolling, focus, keyboard
   alternatives, reduced motion, and supported environments.
5. **Implementation fit.** Reuse current primitives and tokens. Account for performance and implementation
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
