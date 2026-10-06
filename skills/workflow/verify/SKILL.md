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
  when no available check adds useful confidence; explain why.

## Procedure

1. Identify changed behavior, public contracts, and preservation requirements.
   Inspect only relevant paths and repository commands. Existing test results
   apply only to their tested state and environment.
2. Choose the smallest useful checks:
   - Bug: reproduce the symptom and check the correction. Reuse adequate coverage;
     add an edge case only for a distinct, meaningful uncovered failure.
   - Feature/refactor: cover affected behavior, contracts, and preserved behavior.
   - UI: inspect relevant viewports and interactions using available browser tools.
   - Docs/config: check commands, links, paths, or the affected tool directly.
   - Database: use an isolated fixture for migration/data effects; live writes need
     authorization. Dependencies: check manifest/lock pairing and affected imports.
3. Run targeted checks first. Add integration checks when shared behavior, failures,
   or unresolved risks justify them. Respect required repository checks.
   For several work units, keep required final checks pending until they run.
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

Report pass, fail, not-needed, or skipped/blocked; checks and tested scope/state;
meaningful failures and remaining gaps. Partial coverage is not full validation.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
