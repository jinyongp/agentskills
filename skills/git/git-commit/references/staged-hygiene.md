# Inspect staged commit hygiene

Use for inspection-only requests or a requested final hygiene gate. Inspect the
index version of each selected path; the working copy can differ after staging.
This mode never stages, unstages, rewrites, or commits files.

1. Use the bundled worktree inspector for bounded counts and file/diff pages.
   Follow needed offsets from references/inspection.md. Review the requested
   staged scope, including newly added, modified, binary, and relevant renamed
   paths. A comparison with HEAD does not include unstaged or untracked content.
2. Inspect introduced credential values with suitable existing redacting tools
   or scoped index reads. Distinguish configuration references, authorized test
   fixtures, and examples from suspected live credentials. Report suspicion with
   evidence; never expose a full secret in the report.
3. Assess unintended debug scaffolding, disabled behavior, obsolete code blocks,
   generated output, local data, and oversized/binary additions against project
   rules and the path's intended role. Valid logging, fixtures, and intentional
   assets are not automatically mistakes; numeric cutoffs are project decisions.
4. For size/content checks use the staged blob, such as `git cat-file -s :<path>`
   with the exact path passed as a literal argument. Do not use on-disk file size
   or current working content as a substitute. Refresh after the index changes.
5. Report exact paths/lines, redacted evidence, and why the item would be unintended
   or violate the commit contract. Separate hygiene concerns from a full behavior,
   security, or architecture review; the gate establishes only its inspected scope.

For a requested verdict: PASS means complete relevant inspection with no blocking
concerns; BLOCK names supported blocking concerns or incomplete required inspection.
Do not claim PASS after failed/truncated inspection. A report alone performs no
cleanup or Git mutation. If committing is also requested, keep the normal commit
workflow and required checks; do not bypass hooks based on this inspection.
