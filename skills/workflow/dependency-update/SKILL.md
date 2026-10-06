---
name: dependency-update
description: "Update selected dependencies or runtimes with verified target versions, compatibility review, scoped manifest and lockfile changes, and relevant checks. Use for requested upgrades or remediation; recommendations alone do not authorize installation."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Dependency Update

## Scope

Update only the requested packages, runtimes, or dependency group. Follow the user's
target policy, project package manager, registry, lockfiles, and supported platforms.
Inspect-only returns a proposal. Global installs, deployment, broad rewrites, and
unrelated updates need their own scope. Preserve user changes and credentials.

Read [references/compatibility.md](references/compatibility.md) for target selection,
peer/runtime conflicts, or security remediation. Read
[references/resolution.md](references/resolution.md) for workspaces, lockfile churn,
lifecycle execution, failed resolution, or reproducibility checks.

## Procedure

1. Identify the goal and selected scope: compatible refresh, explicit version,
   major upgrade, or remediation. Inspect relevant manifests, lock entries, runtime
   pins, consumers, and CI. Separate declared ranges, resolved versions, and installed
   state; an outdated listing alone does not establish the intended target.
2. Verify target availability and applicable release/migration notes from primary
   sources. Respect pins, prerelease policy, engine/peer requirements, framework
   integrations, native builds, and license constraints. Missing required facts leave
   a tentative plan, not assumed compatibility. Ask only about consequential choices.
3. Choose the smallest coherent update meeting the goal. Group packages that must
   move together; explain unavoidable transitive changes. For remediation, trace the
   affected path and verified fixed version rather than blindly upgrading everything.
   An already satisfied goal can require no change.
4. Use the project's supported resolver and configuration. Preserve unrelated pins
   and regenerate locks through their owner tool. Apply necessary consumer/config
   migrations within scope; a larger redesign needs a separate decision. Inspect the
   resulting diff, resolved versions, and unexpected removals or broad churn.
5. Inspect warnings and peer validity even when the resolver exits successfully.
   Investigate resolution, peer, integrity, native-build, or install-script failures.
   A forced override or suppressed check needs an understood compatibility tradeoff
   and applicable authorization. Preserve evidence and partial changes; do not reset
   unrelated work, delete locks, switch registries, or repeat failing updates blindly.
6. Validate manifest/lock consistency, reproducible resolution where useful, affected
   imports/build/runtime behavior, and required project checks. Use owned fixtures for
   destructive or environment-changing verification. Reuse sufficient coverage; add
   tests only for a meaningful migration gap. Keep unavailable platform checks explicit.
7. Start with selected package/version summaries and relevant changed paths. Use native
   scoped queries; retrieve necessary release sections and lock details progressively.
   Report total/selected/omitted items and a recovery query for large outputs. If a
   reducer is needed, define limits and test large inputs and failures.

## Result

Report requested and actual version changes, relevant compatibility decisions,
consumer migrations, transitive scope, checks and tested environments, and blockers.
Keep credentials and full lockfile/log dumps out of the response. Distinguish proposed,
resolved, installed, and verified states; a successful resolver is not runtime proof.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
