---
name: verify
description: Choose and run checks for a requested change or validation task. Report evidence, failures, and unchecked scope without treating planned checks as passed.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Verify

Run checks for requested behavior and preservation criteria.

## Core rules

- **Useful evidence.** Select checks for plausible failures, not a fixed list.
  Not-needed means no useful signal. An unavailable required check is blocked;
  give its exact prerequisite and affected completion criterion.
- **Task boundary.** Editing fixes, publishing, and changing
  unrelated configuration require task authorization.

The optional runner needs Python 3.11+ on POSIX; checks need their own environment.
On Windows, run checks directly with project log capture.

Read [references/evidence.md](references/evidence.md) when reusing results across
edits, configuration changes, or a handoff.
Read [references/cadence.md](references/cadence.md) when scheduling checks across
several work units or preparing an expensive final check.

## Run and interpret

1. **Criteria.** Identify changed behavior, public contracts, and preservation needs.
   Map criteria to observable evidence; preserve agreed limits from decisions/plans/
   handoffs. Inspect relevant paths/commands. Earlier results apply only to their
   tested state and environment; checks do not introduce new product requirements.
2. **Checks.** Choose the smallest useful checks:
   - Bug: reproduce the symptom and check the correction. Reuse adequate coverage;
     add an edge case only for a distinct, meaningful uncovered failure.
   - Feature/refactor: trace changed inputs/outputs into callers. Select checks that
     exercise the changed path and a contract it could break; reuse evidence only
     while its relevant code, configuration, and environment match.
   - UI: inspect relevant viewports and interactions using available browser tools.
   - Docs/config: check commands, links, paths, or the affected tool directly.
   - Database: use an isolated fixture for migration/data effects; live writes need
     authorization. Dependencies: check manifest/lock pairing and affected imports.
3. **Cadence.** Check meaningful work units, not every save. Run targeted checks first; honor
   repository requirements. Integrate when shared behavior or unresolved risks need
   it; use a real boundary check if isolated checks replace the changed serializer,
   registration or persistence path. Required final checks stay pending until run.
4. **Capture.** For noisy finite commands, execute the bundled helper without reading
   its source. Supply the command explicitly; it performs no shell expansion:

   ```bash
   python3 scripts/run_check.py run --cwd <root> --log <new-log-path> -- <command> <args>
   ```

   Each JSON report is at most 4,000 characters. Full combined output stays in the
   new log; existing logs are preserved. The default timeout is 300 seconds;
   `--timeout <seconds>` kills the command's POSIX process group on expiry.
5. **Detail.** Read only needed detail. Search relevant errors or request a
   bounded page with `python3 scripts/run_check.py log --log <path> --offset <byte-offset>`.
   Follow `next_offset` for required context; omissions are explicit. Logs may
   contain sensitive data, so share only necessary excerpts.
6. **Interpret.** Distinguish product/test failures from missing tools, setup, and infrastructure.
   Fix only within scope; rerun affected checks after changes.

## Result

Report pass, fail, not-needed, or skipped/blocked, tested scope/state, and gaps.
Separate run results from model judgments. A favorable review cannot
replace required evidence; partial coverage stays incomplete.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
