---
name: debug
description: Investigate a reported bug or failing command through reproduction, evidence, root-cause analysis, a scoped fix, and regression checks. Separate confirmed causes from hypotheses.
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Debug

Diagnose the reported symptom and apply a scoped fix when authorized.

## Core rules

- **Fix authority.** Investigate the named target. Apply fixes only when
  requested or already authorized; otherwise return diagnosis and a proposed fix.
- **Preservation.** Preserve unrelated work. Reproduction does not authorize live data changes,
  publishing, broad cleanup, or disabling controls to make a failure disappear.

- **Discriminating evidence.** Form a testable cause and choose a check that
  distinguishes alternatives. State each probe's prediction before running it;
  inspect only needed state. Separate observations from hypotheses.

## Reproduce, diagnose, correct

1. **Baseline.** Establish expected/observed behavior, trigger/input, environment,
   and relevant revision. Reuse current evidence and repository commands.
   Ask for missing inputs only when they block meaningful investigation.
2. **Reproduce.** Use the smallest useful failure in an isolated fixture where practical.
   Define a verdict for the exact symptom, not just successful exit. Reduce inputs
   or steps one at a time while checking that the same failure remains; stop when
   further reduction adds little diagnostic value. Preserve the original case.
   For noisy finite commands, run the bundled helper without reading its source:

   ```bash
   python3 scripts/reproduce.py run --cwd <root> --log <new-log-path> -- <command> <args>
   ```

   This optional helper needs Python 3.11+ and POSIX. It performs no shell expansion,
   preserves existing logs, and reports at most 4,000 characters without raw output.
   On native Windows, run reproductions directly and capture logs with project tools.
   Commands run with existing permissions; choose their side effects deliberately.
   The default 300-second timeout kills the command's process group.
3. **Evidence.** Read relevant detail. Search the log or use
   `python3 scripts/reproduce.py log --log <path> --offset <byte-offset>`.
   Required pages follow `next_offset`; omission counts are explicit.
   Keep credentials and unrelated output out of shared excerpts.
4. **Classification.** Distinguish product failure from test/setup/infrastructure problems. If the
   symptom does not reproduce, record what was tried and the remaining gap.
   A successful unrelated command does not disprove the reported bug.
5. **Cause.** Trace relevant inputs, state, and callers; change one variable at a
   time. Avoid broad speculative edits.
6. **Correction.** When authorized, correct the demonstrated cause with the smallest
   scoped change. Add regression coverage when it proves the failure and matters;
   do not write tests that only repeat the implementation.
7. **Regression.** Rerun the original, unreduced scenario and affected checks. Remove temporary
   instrumentation owned by this investigation; retain useful evidence separately.
   Broaden validation only for shared effects, failures, or unresolved risks.
   Preserve pre-existing user changes.

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
