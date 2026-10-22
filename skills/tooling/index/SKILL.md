---
name: index
description: "Select skills by task, scope, and needed expertise through decision routes, then load the applicable instructions."
license: MIT
metadata:
  author: jinyongp
  category: tooling
---

# Index

Choose instructions for the requested outcome and permission, not a category or
keyword alone. Acknowledgments need no selection. This index covers this collection;
a listing does not prove installation. Consider other available skill metadata.

## Core rules

- **Choose narrowly.** Prefer the workflow that covers the task. Add domain,
  platform, language, or delivery guidance only when needed; do not load a generic
  workflow alongside a specialist that already covers the work. Conversation
  language alone does not trigger a writing skill. Honor explicitly requested skills.
- **Read before acting.** Summaries are not instructions. Read selected SKILL.md
  files; report missing required skills without installing them unasked.
- **Keep permission boundaries.** Review, planning, and measurement do not authorize
  edits, publication, or deployment. Reuse guidance; reconsider when scope changes.

## Select and load

1. **Find the route.** Read the matching decision route below. Choices are alternatives, not a required
   workflow sequence. Follow continuation pages if needed; use the full catalog
   when no choice fits. A partial page cannot prove no applicable skill exists.
2. **Resolve installed paths.** Match names to available installed metadata or sibling
   `../<name>/SKILL.md`, then read selected instructions before acting. `Source`
   fields locate repository files relative to this skill's root only in a source
   checkout; they are not installed paths.

## Choose by task

<!-- index:catalog:start -->

- [Understand or investigate](references/routes/understand.md) — Map a project, follow behavior, or investigate an external question.
- [Define behavior or plan work](references/routes/define.md) — Decide what to build, settle rules, plan implementation, or preserve settled work.
- [Implement or fix](references/routes/change.md) — Change code, diagnose bugs or CI, upgrade dependencies, migrate data, or optimize.
- [Review or assess readiness](references/routes/review.md) — Find defects, review and fix, assess a dependency or skill, or prepare human review.
- [Verify, test, or prepare release](references/routes/verify.md) — Run checks, choose or write tests, measure performance, or prepare QA and rollout.
- [Operate Git](references/routes/git.md) — Manage ignore rules, branches, commits, conflicts, synchronization, worktrees, or pull requests.
- [Write, edit, or shape an answer](references/routes/writing.md) — Draft or revise prose, summarize sources, or apply requested language and delivery guidance.
- [Design or inspect an interface](references/routes/interface.md) — Handle visual hierarchy, responsive behavior, accessibility, mobile browsers, or UI content extremes.
- [Build or investigate motion](references/routes/motion.md) — Name, implement, debug, review, or measure web and native animation.

## Full catalog

- [Frontend](references/catalog/frontend.md) — 15 skills; 1 page.
- [Git](references/catalog/git.md) — 7 skills; 1 page.
- [Tooling](references/catalog/tooling.md) — 2 skills; 1 page.
- [Workflow](references/catalog/workflow.md) — 35 skills; 2 pages.
- [Writing](references/catalog/writing.md) — 10 skills; 1 page.

<!-- index:catalog:end -->

## Result

Routes and catalog pages stay within 2,500 characters, with counts and continuation
paths. Mention selection only when useful, without a separate routine report.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
