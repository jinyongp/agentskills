# GitHub checks and logs

Use the project's GitHub integration, or authenticated gh. Confirm repository,
PR/head SHA and run attempt before collecting evidence; local branch names alone
can identify the wrong remote target.

- gh pr view: select number, URL and headRefOid. Do not request full discussions.
- gh pr checks: request structured fields and summarize counts by bucket with
  native filters first. Select required checks when that is the requested scope;
  disclose excluded checks. Exit code 8 means checks pending, not a failed fetch.
- gh run view: select the matching run's headSha, status, conclusion and jobs.
  Select failed job IDs before retrieving logs. Reusable jobs and unavailable
  log mappings may require provider/API detail; do not invent a clean result.
- Capture a selected failure log with the bundled helper, for example:

  `python3 scripts/capture.py run --cwd <root> --log <new-path> -- gh run view <run-id> --repo <owner/repo> --job <job-id> --log-failed`

  A successful capture proves only that this command completed. Inspect remote
  status separately; search the saved log for the first relevant error and callers.
  For large JSON/job lists, use scoped filters/pages and disclose total/omitted
  counts; the helper also pages the saved complete output without truncating names.

After an authorized push or rerun, inspect its current head and attempt. A missing
check, approval gate or stale run is unresolved. Respect repository check policy;
do not skip a named check because it appears informational.

Sources: [gh pr checks](https://cli.github.com/manual/gh_pr_checks),
[gh run view](https://cli.github.com/manual/gh_run_view).
Workflow inspiration: [Sentry iterate-pr](https://github.com/getsentry/skills/tree/main/skills/iterate-pr)
(Apache-2.0). Guidance is independently written; automatic pushes and bot-name lists
are not required.
