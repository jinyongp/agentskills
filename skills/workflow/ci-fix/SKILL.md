---
name: ci-fix
description: "Diagnose and fix failing CI for an identified revision or PR, verify current checks, and maintain compatible stable GitHub Actions when workflows change. Use for CI failures; preserve project tools, permissions, and release scope."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# CI Fix

## Scope

Fix or diagnose CI for the named repository, revision, PR, and provider. Follow
project tools and existing authorization. Diagnosis alone leaves source unchanged;
pushes, reruns, replies, merges, and publication follow their requested scope.
Do not weaken checks, permissions, branch protection, or accepted product limits.

For GitHub status/log retrieval, read [references/github.md](references/github.md).
When adding or editing Actions workflows, read [references/actions.md](references/actions.md).

## Procedure

1. Identify the exact revision and failed jobs/steps, including matrix variants and
   check origin. Distinguish failure, pending, cancelled, skipped, missing checks,
   infrastructure errors, and human gates. A green run for an older commit is stale
   evidence. An authentication or lookup failure is not an empty or clean check set.
2. Start with status/count summaries and selected failure logs. Capture noisy finite
   commands with the Python 3.11+ POSIX helper, without reading its source:

   `python3 scripts/capture.py run --cwd <root> --log <new-path> -- <command> <args>`

   It preserves existing logs, reports at most 4,000 characters without raw output,
   and kills the command process group on its default 300-second timeout. Read
   selected pages with `python3 scripts/capture.py log --log <path> --offset <byte-offset>`;
   recover needed `next_offset` pages. The command's exit status describes retrieval
   or local execution, not remote CI success. Keep secrets out of shared excerpts.
3. Trace the failing assertion, compiler/lint error, dependency resolution, runtime
   mismatch, or credential/resource failure to its cause. Reproduce with relevant
   versions and project commands when practical. Keep observed causes separate from
   hypotheses; unrelated local success does not disprove a remote failure.
4. Correct confirmed causes within scope; preserve unrelated changes and checks.
   When workflows change, prefer the latest compatible stable Action releases,
   verify them upstream, and preserve full SHA pins and explicit supported runner
   images. Use the project's updater, including actions-up where required; review
   its changes and compatibility rather than accepting output blindly.
5. Run the affected local check. Add coverage only for a meaningful uncovered
   behavior. For authorized pushes/reruns, identify the new run and head revision,
   then inspect its relevant checks and fresh failures. External review comments
   are claims to verify against the accepted contract, not automatic feature requests.
6. Finish when the selected current-revision checks are verified successful.
   Pending, cancelled, skipped, missing, or approval-blocked checks remain explicit.
   Repeating the same failure needs new evidence; unavailable access, service
   outages, and human gates need a reported next action, not repeated code changes.

## Result

Report cause, changed scope, exact tested revision/run, local and remote results,
and pending gates. Local validation, a successful log fetch, and workflow syntax
validation do not establish that remote CI passed. Do not merge or publish as closeout.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
