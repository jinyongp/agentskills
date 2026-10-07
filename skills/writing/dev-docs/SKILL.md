---
name: dev-docs
description: "Create, revise, or review developer documentation using actual product behavior and reader tasks. Use for README files, guides, API references, examples, and documentation structure; preserve requested language, publication scope, and version boundaries."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# Dev Docs

## Scope

Create, edit, or review the requested developer documentation. Follow the audience,
output language, product version, house style, and delivery format. Review-only stays
read-only; publishing or changing product behavior needs its own task scope.
This skill works alone. Accompanying language guidance refines the same deliverable.
Review agreed capabilities; documenting a limit does not authorize adding its feature.

Read [references/structure.md](references/structure.md) when drafting or reviewing
explanatory prose, examples, or navigation; read [references/verification.md](references/verification.md)
when validating commands, generated references, version claims, or examples.

## Procedure

1. Identify what the reader is trying to do, their prerequisites, and the selected
   product/version. Inspect relevant public interfaces, examples, release notes,
   existing docs, and project commands. Distinguish intended behavior from observed
   implementation; resolve material conflicts before documenting a claim as supported.
2. Start with selected paths and headings. Retrieve relevant sections rather than
   whole sites, source trees, or generated API dumps. Track omissions and recover
   necessary context before claiming complete coverage. Existing generators or native
   filters can bound mechanical output; report their limits and retrieval method.
3. State the page's reader task and answer or outcome in its opening. Use headings
   that locate actions, decisions, or lookup subjects. Keep details on the main path
   when they change the reader's next action, prevent a relevant failure, or explain
   the result; link separate design or internals material at the point of need.
   Preserve useful URLs and real inbound links when reorganizing.
4. Give required setup, steps, and a recognizable result. Introduce each example
   with what it demonstrates; keep its inputs consistent with the preceding setup.
   Separate optional variants from the first successful path. Keep API names, defaults,
   units, permissions, and versions exact; label illustrative data and placeholders.
5. Use supplied or verified evidence for behavior and claims. Preserve uncertainty,
   limitations, and author voice. Explain material gaps rather than inventing APIs,
   output, platform support, benchmarks, or guarantees. Keep secrets out of examples.
6. Verify representative commands and examples with project tools in an isolated,
   suitable environment. Distinguish tested output from illustrative output. Avoid
   live writes or paid calls merely to validate an example; report unavailable setup
   or unsupported versions. Reuse link, build, snippet, type, and schema checks.
7. Review whether the opening and headings expose the task and takeaway, and whether
   a reader can follow the example without unrelated internals. Report obstructing
   passages and their effect before minor completeness issues. Check missing setup,
   broken links, contradictions, and stale generated sources.
   Add permanent example coverage only for a meaningful uncovered contract. Preserve
   user edits and report unresolved product/documentation disagreements.

## Result

Return the document ready for its destination, or scoped review findings. Explain
material assumptions and verification gaps separately. Report inspected scope,
tested versions/examples, actual checks, and unverified paths; a docs build does
not establish that every command or supported version works.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
