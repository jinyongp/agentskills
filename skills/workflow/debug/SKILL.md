---
name: debug
description: Investigate a reported bug or failing command through reproduction, evidence, root-cause analysis, a scoped fix, and regression checks. Separate confirmed causes from hypotheses.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Debug

## Scope

- Investigate the reported symptom in the named target. Apply fixes only when
  requested or already authorized; otherwise return diagnosis and a proposed fix.
- Preserve unrelated work. Reproduction does not authorize live data changes,
  publishing, broad cleanup, or disabling controls to make a failure disappear.

## Procedure

1. Establish expected versus observed behavior, trigger/input, affected environment,
   and relevant revision. Reuse current evidence and repository commands.
   Ask for missing inputs only when they block meaningful investigation.
2. Reproduce the smallest useful failure in an isolated fixture where practical.
   For noisy finite commands, run the bundled helper without reading its source:

   ```bash
   python3 scripts/reproduce.py run --cwd <root> --log <new-log-path> -- <command> <args>
   ```

   This optional helper needs Python 3.11+ and POSIX. It performs no shell expansion,
   preserves existing logs, and reports at most 4,000 characters without raw output.
   Commands run with existing permissions; choose their side effects deliberately.
   The default 300-second timeout kills the command's process group.
3. Read only relevant evidence. Search the log or use
   `python3 scripts/reproduce.py log --log <path> --offset <byte-offset>`.
   Required pages follow `next_offset`; omission counts are explicit.
   Keep credentials and unrelated output out of shared excerpts.
4. Distinguish product failure from test/setup/infrastructure problems. If the
   symptom does not reproduce, record what was tried and the remaining gap.
   A successful unrelated command does not disprove the reported bug.
5. Form a testable cause and choose a check that distinguishes it from alternatives.
   Trace relevant inputs, state, and callers; change one variable at a time.
   Separate confirmed observations from hypotheses. Avoid broad speculative edits.
6. When fixes are authorized, correct the demonstrated cause with the smallest
   scoped change. Add regression coverage when it proves the failure and matters;
   do not write tests that only repeat the implementation.
7. Rerun the original reproducer and affected checks. Broaden validation only for
   shared effects, failures, or unresolved risks. Preserve pre-existing user changes.

## Result

Report symptom and trigger, confirmed cause or remaining hypotheses, relevant
evidence, scoped changes, and verification gaps. An unreproduced or unverified
symptom remains unresolved.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
