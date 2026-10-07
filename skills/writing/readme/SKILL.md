---
name: readme
description: "Create, revise, or review package README files for consumers: purpose, installation, a working first-use example, compatibility, and deeper documentation. Keep contributor setup separate and verify claims against the documented release."
license: MIT
metadata:
  author: jinyongp
  category: writing
---

# README

## Scope

Create, edit, or review consumer READMEs for libraries, CLIs, plugins, and SDKs.
General guides, API references, runbooks, and profile READMEs have different tasks.
Works alone. Follow requested language, release, audience, and scope. Review-only
returns findings; documentation work does not authorize product changes or publication.

## Procedure

1. Identify package, consumer, distribution channel, and documented version from
   relevant manifests, entry points, releases, and docs. Separate published behavior
   from checkout changes; settle conflicts before claiming a command or API is available.
2. Inspect selected paths/headings, then interfaces needed by the first example.
   Use scoped queries, report omissions, and recover required detail. Keep full source
   trees, API dumps, and logs out of default input; existing facts stay at their sources.
3. Open with the task solved and intended user. State a capability or boundary that
   helps adoption; substantiate comparisons and performance claims. Put installation
   and first use before independent internals.
4. Give one supported installation path using the actual package name. Include the
   runtime, platform, peer dependency, permission, or configuration needed for that
   path. Keep optional alternatives separate. A registry consumer should not need
   repository cloning, contributor dependencies, or a dev server unless actually
   required. Separate maintainer setup by link or heading.
5. Build the smallest complete first-use example: required input/configuration,
   public invocation, and how to recognize success. For a library/SDK, show imports
   and the call; for a CLI, show the command; for a plugin, show registration and use.
   Include cleanup or error handling when required for correct use. Label illustrative
   output and placeholders; supply no real credentials. Each command or snippet must
   follow from the setup shown, without relying on checkout-only files.
6. Keep a detail beside a step if it changes the invocation, explains its result,
   or prevents a relevant failure. Link full API tables, independent variants, and
   design rationale at their point of need. Show limits before incompatible setup.
   Add badges, contents, or contribution sections for verified status or navigation.
   Link relevant license/contribution files; preserve useful anchors and URLs.
7. Walk the consumer path in a fresh temporary environment using the documented
   release when available. Check installation, entry-point resolution, required setup,
   example completion, and the stated success signal with project tools. A checkout
   or local tarball verifies that candidate, not registry availability. Avoid live
   writes or paid calls solely for a docs check; state blocked prerequisites and
   untested behavior. Reuse existing link, type, snippet, and build checks.
8. Follow purpose → install → example → success → deeper detail. For each defect,
   name the passage/missing step, reader impact, and scoped repair. A docs build does
   not prove usability. Preserve valid facts and user edits. Lasting tests protect
   meaningful uncovered contracts, not headings, prose literals, or section counts.

## Result

Return the requested README or prioritized findings. Separately report the documented
version, exercised consumer path, actual evidence, and gaps. Keep review notes and
unrelated implementation details out of the finished document.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
