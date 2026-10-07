---
name: prototype
description: "Build distinct interactive UI alternatives for a requested comparison, using isolated previews and realistic context. Explain tradeoffs, let the user choose, and integrate a selected direction when authorized."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Prototype

## Scope

Build UI alternatives when the user requests exploration or comparison. Ordinary
implementation and a narrow repair do not require multiple versions. Preserve the
requested surface and product constraints; a larger brief may need staged exploration,
not an automatic reduction to one component.

Inspect the selected component, real surrounding context, tokens, stack, and user
requirements. Reuse project preview tooling. Read
[references/comparison.md](references/comparison.md) when designing the comparison
surface or promoting a choice.

## Build and compare

- Name the decision each direction explores and what the comparison will reveal:
  density may trade scanning space for visible rows; navigation may trade direct
  access for fewer simultaneous choices. Recolors suffice when palette is the decision.
  Choose the number from the brief and useful decision space;
  present each direction's benefit and cost without padding the set.
- Use an isolated preview route, component story, or standalone artifact as appropriate.
  Keep production behavior intact during exploration. Reuse shared components/tokens
  without introducing production imports from disposable previews.
- Hold the task, content, and relevant states comparable. Demonstration data is
  identified; simulated integrations are explicit. Each variant's claimed controls
  must work within that simulation, and required access must survive narrow layouts,
  keyboard input, and reduced motion.
- Show alternatives at realistic size and in context. A simple accessible selector
  can switch versions; match project conventions rather than imposing fixed chrome.
  Compare more than the attractive resting state when the decision concerns a flow.
- Exercise each variant with available project tools. Report source-only or static
  verification if previews cannot run. Return the exact preview location, brief
  direction/tradeoff comparison, checks, and gaps. Keep source dumps and unrelated
  screens outside default input; inspect relevant detail before claiming coverage.

## Selection and integration

Let the user select when selection is part of the request. If a choice was already
made or delegated, use that authorization and explain the decision. Exploration alone
does not authorize replacing the production design.

Integrate the selected direction when requested. Follow local structure, remove
disposable preview wiring created for this run unless retention is requested, and
preserve pre-existing stories or fixtures. Verify production behavior and relevant
states after promotion. Reuse sufficient checks; add tests only for meaningful
uncovered behavior. Summarize the selected result and remaining evidence gaps.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
