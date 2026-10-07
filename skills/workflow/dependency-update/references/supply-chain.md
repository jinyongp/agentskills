# Verify affected dependency paths

Use when an advisory, install hook, integrity failure, or suspicious upstream
change motivates the selected update. Ordinary updates do not require a broad audit.

- Resolve the installed/locked version and its direct or transitive parent path.
  A manifest range or registry's latest release is not the version under review.
  Use the owning manager's tree/advisory queries; capture selected paths, total
  coverage and omitted/unsupported lock formats before interpreting results.
- Match advisories to exact versions, affected functionality and the documented fix.
  Check relevant runtime/platform prerequisites and consumers. Unknown reachability
  remains unknown; it neither proves exposure nor makes an affected version safe.
- For lifecycle hooks, inspect which selected packages execute scripts, what those
  scripts access/change, and whether setup is required. Suppressing scripts may
  support isolated inspection but does not prove the resulting application works.
  Follow execution policy; do not execute suspicious hooks to discover their intent.
- Registry publish rights, repository contributors, downloads and recent commits
  measure different things. Do not infer maintainer authority or compromise from
  popularity, a quiet release schedule, or missing data. Verify material upstream
  changes against primary registry/release/advisory evidence when needed.
- Choose a supported parent upgrade or scoped fixed version. An override must meet
  consumer constraints; do not hide a finding through exclusions, unsupported
  forced resolution or edited integrity data. Report unresolved paths and coverage
  gaps instead of declaring the whole tree secure after a partial scan.


Primary sources: [OSV query API](https://google.github.io/osv.dev/api/),
[npm audit](https://docs.npmjs.com/cli/commands/npm-audit/),
[npm scripts](https://docs.npmjs.com/cli/using-npm/scripts/).
