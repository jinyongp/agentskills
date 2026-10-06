---
name: animation-performance
description: "Measure and improve web or React Native animation frame pacing and input responsiveness. Use for motion profiling or demonstrated stalls; compare matched runs and distinguish rendering costs from timing choices."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Performance

## Scope

Profile a selected web or React Native animation and improve demonstrated performance
costs when authorized. Frame pacing and input responsiveness are the target; a timing
preference or general API/CPU benchmark alone does not activate this skill.
Honor measurement-only requests and keep the intended interaction intact.

Use current user/project tools and available target environments. Inspect selected
components, engine versions, and existing profiling commands first. Read only the
matching platform section of [references/profiling.md](references/profiling.md) when
choosing evidence or interpreting a trace. A new profiler or engine needs a concrete
capability gap and compatible setup.

## Measure and attribute

- Define the interaction, relevant load, device/browser, build mode, refresh rate,
  and goal. Choose metrics the tools actually expose: frame intervals/missed deadlines,
  input acknowledgement, or selected scripting/layout/paint/runtime costs. Distinguish
  animation duration from processing delay. At 60Hz a frame interval is about 16.7ms;
  use the actual refresh rate rather than a universal 60fps threshold.
- Capture a short reproducible baseline at normal speed. Match warm/cold state,
  viewport/data, device conditions, and concurrent work across comparisons. Repeat
  enough to expose variability; preserve slow intervals rather than just averages.
  Debug builds, throttled runs, and remote instrumentation have explicit limits.
- Read an interval summary first, then selected trace events or stacks for the
  suspected bottleneck. Keep raw exports outside default agent input. Report inspected
  ranges, totals/omissions, and retrieval positions; recover required detail before
  assigning cause. Avoid claiming a whole-trace analysis from a sample.
- Attribute cost to observed work: JS scheduling/renders, measurement/layout, paint,
  composition, UI-runtime work, or crossings. Transform/opacity, a worklet, or a
  compositor path can help but does not prove the full pipeline meets its budget.
  A stale callback or snapping value may require correctness diagnosis instead.

## Improve and verify

Change the demonstrated bottleneck within scope: reduce redundant renders or reads,
batch appropriate work, simplify an expensive surface, or use a supported execution
path. Preserve visual requirements, input/focus, interruption, and reduced motion.
Use layer promotion, virtualization, or dependency changes only where relevant evidence
justifies their cost. Remove temporary instrumentation and reuse sufficient checks.

Repeat the original workload under matched conditions; report baseline and changed
values, variability, and residual stalls. A gain smaller than observed noise is
inconclusive. If profiling is unavailable, return hypotheses and the smallest capture
needed; source review does not establish measured improvement.

Deliver the bottleneck evidence, scoped change or recommendation, comparison conditions,
and unverified environments. Save native trace exports when requested or needed to
support the result, with a concise summary linking selected intervals and reproduction.
Do not replace raw evidence with a large pasted trace or invented measurements.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
