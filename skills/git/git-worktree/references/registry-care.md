# Registry maintenance

Read only for requested locking, relocation, repair, or stale-registry cleanup.

- Lock/unlock: use the exact registered path and preserve the lock's purpose.
- Move: use `git worktree move <old-path> <new-path>`; verify both registrations.
  Main checkouts and worktrees containing submodules need another approach.
- Repair: identify the actual relocated checkout before `git worktree repair <path>`.
- Prune: inspect `git worktree prune --dry-run --verbose` first. Prune has no
  per-path filter; every affected registration must fit the requested cleanup.
  Missing storage may be temporary. Preserve locks and data still needed elsewhere.
- Treat Git refusals as evidence, not permission to force or edit administrative files.

Command behavior: [Git worktree documentation](https://git-scm.com/docs/git-worktree).
