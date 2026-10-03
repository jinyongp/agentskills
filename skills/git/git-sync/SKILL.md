---
name: git-sync
description: Fetch, pull, push, or check synchronization for an identified Git branch. Distinguish ahead, behind, and diverged histories while preserving local work.
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Sync

## Scope

- Use Git in the target worktree and follow repository/network instructions.
- Establish direction, branch, fetch remote, and actual push destination. Do not
  assume origin/main or that pull and push use the same target. Ambiguous "sync"
  needs a direction before upload; status-only reports whether refs are cached.
- Creating commits, deleting remote branches, tags, and force-push require their
  own authorization. Preserve local work; do not auto-stash, commit, or discard it.
- Pause integration during an unrelated operation. Resolve detached HEAD, missing
  upstream, or multiple candidate destinations before mutating references.

## Procedure

1. Inspect HEAD and local-change summaries first; read only affected detail.
   Select verified targets without changing configuration, except requested tracking.
   Avoid exposing credential-bearing remote URLs.
2. Fetch the selected remote when fresh state is needed. On failure, report the
   error and stop integration; do not use stale refs as current or repeatedly retry.
   Add neither pruning nor unrelated remotes to the request.
3. Use `git rev-list --left-right --count HEAD...<remote-ref>`: local-only/remote-only
   counts classify equal (0/0), ahead (>0/0), behind (0/>0), or diverged (>0/>0).
   Inspect only relevant differing commits. Report shallow-history comparison limits.
4. For an unspecified pull strategy, use `git merge --ff-only <remote-ref>` when
   behind and local work is safe. Equal/ahead needs no download integration.
   Divergence needs established repository policy or an explicit merge/rebase choice.
   Rewriting published commits requires authorization; stop requested integration
   at conflicts unless resolving them is also in scope.
5. For push, inspect outgoing commits and the exact destination, resolving multiple
   push URLs first. Use `git push --no-follow-tags <remote> HEAD:refs/heads/<branch>`.
   Set tracking only within the requested new-branch scope. On rejection, fetch and
   reassess; normal push does not authorize force. An authorized force-push needs
   a lease tied to the reviewed remote commit; a changed tip invalidates the plan.
6. Check resulting refs, ahead/behind counts, and preserved local changes. Verify
   the actual push target, and run checks appropriate to integrated changes.

## Result

Report branch/target, commit IDs, fetched/integrated/uploaded actions, actual checks,
preserved local work, and remaining divergence or blockers.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
