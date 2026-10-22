---
name: review-map
description: "Prepare a feature-grouped map of a change for human review, with risk reasons and code reading order. Use for review preparation; report observations without defect verdicts."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Review Map

Prepare a map of a patch, branch, commit range, or local changes for a human reviewer.
Group by changed behavior, explain review priority, and point to a useful reading
order. Findings, fixes, and merge decisions are outside this descriptive task.

## Core rules

- **Priority needs evidence.** Use consequence and reach: permissions, durable
  writes, compatibility, external effects, and recovery. A sensitive filename,
  line count, or guessed author is insufficient. Assess lockfiles/generated
  contracts by their runtime role instead of excluding them automatically.
- **Describe without a verdict.** Risks are not confirmed defects. Do not declare
  the change correct, safe, or ready to merge.

## Inspect

Use Git and Python 3.11+. Execute the bundled helper without reading its source:
`python3 scripts/inspect_changes.py --repo <root>`. It starts with counts.
Read [references/change-inspection.md](references/change-inspection.md) for
comparison arguments, layer selection, and file/diff pages.

1. **Comparison.** Establish target/base; distinguish branch additions,
   endpoint comparisons, and staged/working changes. Reuse returned commit IDs
   for detail queries. Do not silently choose main or fetch a remote.
2. **Coverage.** Inspect file pages, hunks, and caller context. Follow needed offsets;
   incomplete inspection stays visible. Untracked content needs separate reads.
   Preserve exact paths and report generated/binary or unsupported surfaces.
3. **Groups.** Follow coherent behavior across files. A file can serve several features;
   shared dependencies can get one cross-cutting entry with links to affected groups.
   Separate user-facing changes from internal restructuring when useful.
4. **Order.** Prioritize groups with evidence for their consequence and reach.
5. **Reading path.** Point to changed contract or shape, incoming values,
   transformations, decisions, effects, and relevant boundaries/tests. Choose a
   reading order that explains this change; omit empty structural categories.

## Result

Return a compact overview or a detailed reading map according to the request.
Name each behavior group, its priority reason, and exact code locations. Describe
observed surfaces without presenting risks as confirmed defects. Explain selected
target, inspected coverage, omitted/generated content, and material unknowns.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
