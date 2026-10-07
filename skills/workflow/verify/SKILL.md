---
name: verify
description: Choose and run checks for a requested change or validation task. Report evidence, failures, and unchecked scope without treating planned checks as passed.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Verify

## Scope

- The optional runner needs Python 3.11+ on POSIX; checks need their own environment.
- Validate the requested change or target. Editing fixes, publishing, and changing
  unrelated configuration require task authorization.
- Select checks for plausible failures, not a fixed checklist. Report not-needed
  when a check adds no useful signal. An unavailable required check is blocked,
  not not-needed; report its exact prerequisite and affected completion criterion.

Read [references/evidence.md](references/evidence.md) when reusing results across
edits, configuration changes, or a handoff.
Read [references/cadence.md](references/cadence.md) when scheduling checks across
several work units or preparing an expensive final check.

## Procedure

1. Identify changed behavior, public contracts, and preservation requirements.
   Map criteria to observable evidence; preserve agreed limits from decisions/plans/
   handoffs. Inspect relevant paths and commands. Earlier results apply only to their
   tested state and environment; checks do not introduce new product requirements.
2. Choose the smallest useful checks:
   - Bug: reproduce the symptom and check the correction. Reuse adequate coverage;
     add an edge case only for a distinct, meaningful uncovered failure.
   - Feature/refactor: trace changed inputs/outputs into callers. Select checks that
     exercise the changed path and an existing contract it could break; reuse prior
     evidence only when the relevant code, configuration, and environment still match.
   - UI: inspect relevant viewports and interactions using available browser tools.
   - Docs/config: check commands, links, paths, or the affected tool directly.
   - Database: use an isolated fixture for migration/data effects; live writes need
     authorization. Dependencies: check manifest/lock pairing and affected imports.
3. Check meaningful work units, not every save. Run targeted checks first and honor
   repository requirements. Integrate when shared behavior or unresolved risks need
   it; use a real boundary check if isolated checks replace the changed serializer,
   registration or persistence path. Required final checks stay pending until run.
4. For finite commands with noisy output, execute the bundled helper without reading
   its source. Supply the command explicitly; it performs no shell expansion:

   ```bash
   python3 scripts/run_check.py run --cwd <root> --log <new-log-path> -- <command> <args>
   ```

   Each JSON report is at most 4,000 characters. Full combined output stays in the
   new log; existing logs are preserved. The default timeout is 300 seconds;
   `--timeout <seconds>` kills the command's POSIX process group on expiry.
5. Read details only when needed. Search the log for relevant errors or request a
   bounded page with `python3 scripts/run_check.py log --log <path> --offset <byte-offset>`.
   Follow `next_offset` for required context; omissions are explicit. Logs may
   contain sensitive data, so share only necessary excerpts.
6. Distinguish product/test failures from missing tools, setup, and infrastructure.
   Fix only within scope; rerun affected checks after changes.

## Result

Report pass, fail, not-needed, or skipped/blocked, tested scope/state, and gaps.
Keep executed checks and observed behavior separate from model judgments. A favorable
review cannot replace missing required evidence; partial coverage stays incomplete.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
