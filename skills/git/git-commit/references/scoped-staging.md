# Preserving excluded staging

Read only when a scoped commit would otherwise include unrelated staged changes.
An ordinary commit consumes the whole index. Inspect both index and worktree first.

For clearly separate paths:

1. Save `git diff --cached --binary -- <excluded-paths>` outside the worktree;
   preserve exact paths, staged diff, and affected working-file contents.
2. Temporarily unstage only those paths with `git restore --staged -- <paths>`.
3. Stage and verify the requested group; commit only when authorized and checks pass.
4. On success or failure, use `git apply --cached <saved-patch>` to restore exclusion
   staging. Verify its cached diff and working-file contents against the saved state.
5. Keep the saved patch until restoration is confirmed. If restoration fails,
   preserve the artifact, stop further index mutation, and report its location.

If paths/hunks overlap or exact restoration is unclear, pause that commit.
Do not discard changes, overwrite working files, or broaden the commit's scope.
