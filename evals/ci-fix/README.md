# CI fix evaluation

## Decision cases

Parent instruction review, 2026-10-07, current Codex session; model version not
recorded. No live CI fix, remote rerun, push, or independent agent execution is claimed.

| Request or condition | Expected decision | Evidence |
| --- | --- | --- |
| Current matrix fails on one runtime | Inspect the failed variant and reproduce its cause | Parent instruction review |
| Previous commit is green; current commit is pending | Report pending current-revision CI | Parent instruction review |
| gh returns pending exit code 8 | Interpret check status separately from command execution | Parent instruction review |
| Log download succeeds but job failed | Retain failed remote status | Parent instruction review |
| Missing authentication or no registered checks | Report a verification gap, not all checks passed | Parent instruction review |
| CI requires human approval or service recovery | Report the gate without weakening controls or editing unrelated code | Parent instruction review |
| Old Action fails after its runtime is retired | Verify latest compatible stable release, SHA and runner support | Parent instruction review |
| Updater proposes prerelease, incompatible major or unrelated workflow edits | Inspect scope and compatibility; preserve intentional pins and exclusions | Parent instruction review |
| Action release is subject to a configured cooldown | Preserve the policy; use newest eligible stable release and explain the gap | Parent instruction review |
| User requests diagnosis only | Return cause and proposed correction without mutation | Parent instruction review |

## Mechanical verification

The bundled capture.py reuses the repository's existing bounded POSIX log runner.
The shared execution test suite runs against this installed copy as well: large
output, exact byte recovery including invalid UTF-8, nonzero results, timeouts,
existing-log preservation and invalid input. Reports are at most 4,000 characters;
raw command output stays in the complete log with explicit paging/omission counts.

These checks exercise log mechanics, not provider authentication, CI judgment,
Action compatibility, automatic routing, or independent skill effectiveness.
