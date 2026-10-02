---
name: git-sync
description: "Fetch, pull, or push an identified Git branch when the user asks to synchronize with a remote. Classify ahead, behind, and divergent histories; preserve local work and avoid unrequested history rewriting."
license: MIT
metadata:
  author: jinyongp
  category: git
---

# Git Sync

Synchronize the requested branch with the identified remote while preserving work.

## When to use

Use for fetching, pulling, pushing, or checking branch synchronization. Establish
the direction: downloading updates does not authorize uploading commits. If
"sync" leaves that direction ambiguous, inspect first and ask before uploading.
For status-only requests, report whether remote information is cached or freshly
fetched. Creating commits, deleting remote branches, and publishing tags are
separate actions.

## Prerequisites

Use Git in the target worktree, following repository instructions and network
permissions. Inspect `git status --short --branch`, `git branch -vv`, remote names,
and the requested branch's configured upstream. A remote URL can contain credentials;
do not expose them in logs or reports. Do not assume the remote is `origin` or
the base is `main`.

Do not integrate changes during an unrelated merge, rebase, or cherry-pick.
Detached HEAD, missing upstream, multiple candidate remotes, or a mismatch between
pull and push targets require identifying the exact branch before mutation.

## Procedure

1. Record HEAD, staged and unstaged changes, and untracked paths. Select the remote
   and branch from the user's request or verified tracking configuration. Inspect
   the fetch and push destinations separately; resolve multiple push destinations
   before uploading. Keep Git configuration unchanged
   unless establishing tracking is part of the request.
2. Fetch the selected remote with `git fetch <remote>` when current remote state
   is needed. Fetch failure leaves integration pending: explain authentication,
   network, or missing-reference errors without repeatedly retrying the same action.
   Do not add pruning or fetch every remote to a single-branch request.
3. Compare with the verified remote-tracking reference:

   ```bash
   git rev-list --left-right --count HEAD...<remote-ref>
   git log --oneline --left-right HEAD...<remote-ref>
   ```

   The left count is local-only commits; the right count is remote-only commits.
   Zero on both sides means equal; only the right is nonzero means behind; only
   the left is nonzero means ahead; both nonzero means diverged. If a shallow
   boundary prevents comparison, report that limit before choosing integration.
4. For a pull or update request without a specified integration strategy, use
   `git merge --ff-only <remote-ref>` when behind and the worktree is ready. Equal
   or ahead needs no download integration. Before integrating, resolve any local
   staged, unstaged, or untracked work that could be affected; do not automatically
   stash, create a commit, or discard it. Fetch alone can leave that work in place.
5. A diverged branch needs the repository's established policy or an explicit
   choice of merge or rebase. Explain which commits differ if neither settles it.
   Rebase of published history requires explicit authorization. During a requested
   merge or rebase, stop at conflicts, preserve the operation state, and report
   the paths. Resolving them requires the corresponding task scope.
6. For a push request, inspect the outgoing commits and the actual push destination.
   Use an explicit refspec such as
   `git push --no-follow-tags <remote> HEAD:refs/heads/<branch>` for
   the selected branch. Set tracking only when requested or needed to establish
   the requested new branch. Leave other branches and tags unchanged. On rejection,
   fetch and reassess; a normal push request does not authorize force-push.

Force-push is a separate, explicitly authorized action. If requested, identify
the target and expected remote commit, account for collaborators' work, and use
a lease tied to that expected commit. A changed remote tip invalidates the plan;
do not weaken the lease or substitute unconditional force.

## Output

Report the local branch, remote target, before/after commit IDs, direction, and
ahead/behind result. Distinguish fetched references, integrated changes, and
uploaded commits. If blocked, identify the unresolved strategy or failure and
the local work that remains preserved.

## Verification

After integration, check status and the resulting commits, then run checks
appropriate to incoming changes. After a push, verify the selected destination's
branch tip; do not assume the pull upstream is also the push destination. Compare
local changes with the inspected state and report any remaining divergence.

Command reference: [git fetch](https://git-scm.com/docs/git-fetch),
[git merge](https://git-scm.com/docs/git-merge),
[git push](https://git-scm.com/docs/git-push).
