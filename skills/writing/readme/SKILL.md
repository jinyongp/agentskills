---
name: readme
description: "Create, revise, or review package README files for consumers: purpose, installation, a working first-use example, compatibility, and deeper documentation. Keep contributor setup separate and verify claims against the documented release."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# README

Write, edit, or review consumer READMEs for libraries, CLIs, plugins, and SDKs.
Excludes general guides, API references, runbooks, and profile READMEs. Works alone.
Honor language, release, audience, and scope. Review-only returns findings;
docs do not authorize product changes or publication.

## Core rules

- **Release accuracy.** Separate published behavior from checkout changes;
  settle conflicts before claiming availability.
- **First use.** Put purpose, supported installation, a working example,
  and recognizable success before independent internals. Keep required setup,
  result explanations, and failure prevention beside the step.

Read [references/structure.md](references/structure.md) when drafting or reviewing
organization, prose, examples, lists, tables, or navigation.

## Build the consumer path

1. **Baseline.** Identify package, consumer, distribution channel, and documented
   version from manifests, entry points, releases, and docs.
2. **Inspection.** Read selected paths/headings, then interfaces needed by the first example.
   Use scoped queries, report omissions, and recover required detail; avoid full
   source trees, API dumps, and logs by default.
3. **Purpose.** Open with the task solved and intended user. State a capability or boundary that
   helps adoption; substantiate comparisons/performance claims. Group questions under useful
   headings; choose prose, lists, tables, and code by the information's relationship.
4. **Install.** Give one supported path with the package name and required runtime,
   platform, peers, permissions, and configuration. Separate alternatives and maintainer
   setup. Registry users need no clone, contributor tools, or dev server unless required.
5. **First use.** Build a complete example: required input/configuration,
   public invocation, and recognizable success. Show imports and a call for a
   library/SDK, a command for a CLI, or registration and use for a plugin.
   Include required cleanup/error handling. Label illustrative output and placeholders;
   supply no real credentials. Each command or snippet must
   follow from the setup without checkout-only files.
6. **Deeper detail.** Link full API tables, variants, and rationale where needed.
   Show limits before incompatible setup.
   Add badges or contents for verified status or navigation. Link license/contribution
   files; preserve useful anchors and URLs.
7. **Execution.** Walk the consumer path in a fresh temporary environment using the documented
   release when available. Check installation, entry-point resolution, required setup,
   example completion, and success signal. A checkout
   or local tarball verifies that candidate, not registry availability. Avoid live
   writes or paid calls solely for a docs check; state blocked prerequisites and
   untested behavior. Reuse existing link, type, snippet, and build checks.
8. **Reading.** Check that headings, lists, and tables make setup, choices, and results findable
   without reading every paragraph. Prioritize obstructing structure and excess detail
   over polish. Name each passage/gap, reader impact, and repair. A docs build does
   not prove usability. Preserve facts and edits; lasting tests protect meaningful
   uncovered contracts, not headings, prose literals, or section counts.

## Result

Return README or prioritized findings. Separately report version, exercised path,
evidence, and gaps. Keep review notes/unrelated internals out of the document.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
