---
name: animation-audit
description: "Inventory web or React Native motion across a project and produce prioritized, evidence-backed improvement plans. Use for a broad motion audit or roadmap; source changes require a separate implementation request."
license: MIT
metadata:
  author: jinyongp
  category: frontend
---

# Animation Audit

## Scope

Audit motion across the selected web or React Native project and return prioritized
improvement plans. Source edits and dependency changes need an implementation request.
Plans stay inline unless saving is requested or needed. Respect current user/project
tools, motion tokens, platform requirements, and documented design decisions.
Recover agreed limits and omissions before planning corrections; a useful new
interaction is an extension only when requested, not an automatic audit finding.

## Inventory

Execute the Python 3.11+ and Git helper without reading its source:

```bash
python3 scripts/inventory.py --root <selected-worktree-directory>
```

Default output is counts only. It examines a sorted window of up to 1,000 eligible
Git-tracked or unignored untracked JS/CSS-family files, reading at most 1 MB each.
Use `--mode candidates` for exact paths and first matching lines, or `--mode skipped`
for oversized, binary, external, or unreadable files. Neither mode returns source text.
Use `--offset` and `--limit` (1-100) for output pages; each JSON response is at most
4,000 characters including escapes and newline. Oversized exact entries fail explicitly.

Use `next_offset` within the same scan window, then `next_scan_offset` with
`--scan-offset` for further file windows. `--scan-limit` accepts 1-10,000.
Reports distinguish omitted pages, unscanned files, and skipped files. Aggregate only
visited windows; refresh after repository changes. Inspect required source selectively.
Ignored files, other languages, dependencies, and dynamic/wrapper patterns need targeted
project inspection. Hints are candidates, not defects or an exhaustive motion map.
Outside a Git worktree or without prerequisites, report the gap and use suitable
bounded project tooling; do not silently claim the same coverage.

## Assess and plan

1. Map relevant journeys, components, tokens, motion libraries, and input environments.
   Prioritize frequent or critical interactions while stating the selected coverage.
2. Trace candidate behavior: purpose, perceived delay, spatial continuity, interruption,
   exit ownership, gesture/scroll arbitration, and reachable states. Include keyboard,
   focus, reduced motion, and device-specific interaction where applicable.
3. Confirm findings with code and available runtime evidence. Profile suspected frame
   drops before claiming performance results. Respect accepted tradeoffs; separate
   defects and evidenced costs from optional visual suggestions.
4. Merge shared causes and prioritize by impact, frequency, evidence, and correction
   cost. No supported findings is valid. Avoid speculative redesign or fixed quotas.
5. For each warranted improvement, give the affected outcome, precise repository
   locations, evidence, scoped change, prerequisites, dependencies, and useful acceptance
   checks. Link recoverable repository facts; preserve decisions unavailable from code.
   A later implementation request uses these plans without granting publication rights.

## Result

Return priorities, actionable plans, reviewed scope, actual checks, and material gaps.
Distinguish static hints, traced behavior, and observed motion. Inspection completion
does not establish correctness or smoothness across every device.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
