---
name: dev-docs
description: "Create, revise, or review developer documentation using actual product behavior and reader tasks. Use for README files, guides, API references, examples, and documentation structure; preserve requested language, publication scope, and version boundaries."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Dev Docs

Create, edit, or review developer docs. Follow the audience,
output language, product version, house style, and delivery format.

## Core rules

- **Supported claims.** Use supplied or verified evidence. Preserve uncertainty,
  limitations, and author voice. Expose material gaps; do not invent APIs, output,
  platform support, benchmarks, or guarantees. Keep secrets out of examples.
- **Reader task first.** Open with the task and answer/outcome. Keep details that
  change actions, prevent failure, or explain results beside the step.
- **Documentation scope.** Review-only stays read-only; publishing or changing
  product behavior needs its own scope. Documenting a limit does not authorize
  adding its feature.

This skill works alone; language guidance refines the same deliverable. Review
agreed capabilities.

Read [references/structure.md](references/structure.md) when drafting or reviewing
organization, prose, lists, tables, examples, or navigation; read [references/verification.md](references/verification.md)
when validating commands, generated references, version claims, or examples.

## Draft and verify

1. **Baseline.** Identify the reader task, prerequisites, and selected
   product/version. Inspect relevant public interfaces, examples, release notes,
   existing docs, and project commands. Distinguish intended behavior from observed
   implementation; resolve material conflicts before documenting a claim as supported.
2. **Inspection.** Start with selected paths and headings. Retrieve relevant sections rather than
   whole sites, source trees, or generated API dumps. Track omissions and recover
   necessary context before claiming complete coverage. Bound output with existing
   tools; report limits and retrieval method.
3. **Organization.** Group actions, decisions, and
   lookup subjects under useful headings; choose prose, lists, tables, and code by
   their relationships. Link separate design/internals material.
   Preserve useful URLs and inbound links.
4. **Examples.** Give required setup, steps, and a recognizable result. Introduce each example
   with what it demonstrates; keep its inputs consistent with the preceding setup.
   Separate optional variants from the first successful path. Keep API names, defaults,
   units, permissions, and versions exact; label illustrative data and placeholders.
5. **Execution.** Verify representative commands and examples with project tools in an isolated,
   suitable environment. Distinguish tested output from illustrative output. Avoid
   live writes or paid calls merely to validate an example; report unavailable setup
   or unsupported versions. Reuse link, build, snippet, type, and schema checks.
6. **Reader check.** Can readers locate prerequisites, steps, choices, and results
   without reading every paragraph. Review grouping, format choice, and detail load
   separately from command correctness. Prioritize obstructing structure and passages
   over polish; name their effect and repair. Check missing setup, broken links,
   contradictions, and stale generated sources.
   Add permanent example coverage only for a meaningful uncovered contract. Preserve
   user edits and report unresolved product/documentation disagreements.

## Result

Return the finished document or scoped findings. Explain assumptions and gaps
separately. Report scope, tested versions/examples, actual checks, and unverified
paths; a docs build does not establish that every command or supported version works.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
