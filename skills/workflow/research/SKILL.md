---
name: research
description: "Investigate a specified question using primary sources, reconcile conflicting evidence, and distinguish facts, inference, and unknowns. Use for external technical research or comparisons; repository mapping alone uses survey."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Research

## Scope

Research the specified question or comparison using available browsing, source,
and project tools. Preserve the requested breadth, language, and decision criteria.
Research alone does not authorize installation, implementation, or external writes.
Use current project facts to narrow the question; repository mapping alone is survey.

## Procedure

1. Define what the answer must establish: supported version, observed result,
   comparison criteria, or evidence for a claim. Reuse settled constraints; ask
   only when ambiguity would change the investigation or recommendation.
2. Use search to locate evidence, then open the source that owns each claim:
   official documentation, releases, specifications, source code, or original
   research. A search snippet or another summary is a lead, not verification.
3. Match evidence to the relevant version, platform, population, and date. Verify
   changeable facts at the time of the task. A draft, prerelease, benchmark on a
   different workload, or lab result does not establish the requested production
   behavior. Trace useful secondary claims back to their primary evidence.
4. Collect only decision-relevant sections. For a requested complete review, track
   every requested area and recover needed pages; disclose inaccessible or omitted
   material. Use targeted queries and bounded exports instead of dumping sites,
   repository trees, or papers into context. Read [references/evidence.md](references/evidence.md)
   when sources disagree, results are empirical, or a comparison needs synthesis.
5. Separate directly supported facts, reasoned inference, and unresolved questions.
   Seek evidence that could change the conclusion; repeated summaries of one study
   are one evidence source. Explain a material disagreement rather than averaging
   incompatible results or choosing the newest page automatically.
6. Tie conclusions to direct source links and meaningful limitations. Recommend an
   option only against the actual criteria; an existing adequate approach is valid.
   Stop when the question is answered with adequate evidence, or report the precise
   access/input gap. Delegation and saved reports follow the task, not a fixed ritual.

## Result

Lead with the answer, then its strongest evidence, important alternatives, and
remaining uncertainty. Keep citations beside the claims they support; never imply
that reading a source executed or independently reproduced its results.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
