# Publish a release

Run commands from the repository root. Running `release.py` authorizes publication
without another confirmation prompt. GitHub Actions publishes the package.

## Before running

- Start on the repository's default branch (currently `main`). Commit pending work;
  clean local commits ahead of the remote are included.
- Install Git, uv, Node.js 22.20+/npm/npx, and `gh`. Authenticate `gh` with repository write access.
- Choose the intended version without a `v` prefix or build metadata. Published
  versions cannot be replaced; source changes after a release tag need a new version.
- The origin fetch/push repository must match `package.json`. Behind or diverged
  branches stop before preparation.
- Complete [first-time publication setup](#first-time-publication-setup) before
  the first automated release.

## Publish a stable version

Replace the example version with the intended release:

```bash
uv run release.py 0.2.0
```

A stable version uses npm's `latest` tag and removes any prerelease dist-tag override.

## Publish a prerelease

A prerelease sets `publishConfig.tag` to `next`:

```bash
uv run release.py 0.3.0-rc.1
```

## Inspect command help

```bash
uv run release.py --help
```

## What the command does

1. Reads package identity, entrypoint, packaging allowlist, and repository from
   `package.json`. It discovers the default branch through GitHub and the publication
   workflow through its releaseway npm action.
2. Updates the package version, runs `uv run --locked check.py`, packs into a temporary
   directory, and exercises the tarball's help and full skill installation outside
   the checkout. Bundled resources are compared with their sources using the
   packaging allowlist and exclusions. The generated index is format-validated
   and checked against the installed task paths, rather than the source-tree index.
3. Commits only release metadata and atomically pushes the branch and selected tag.
   It never force-pushes or pushes unrelated tags. The workflow rejects version mismatches.
4. Waits up to two minutes for the matching tag/commit workflow and one hour for
   completion. The `Release` workflow runs on `v*` tags, reuses full validation,
   publishes with `releaseway/npm-actions`, and creates an immutable GitHub Release
   with `releaseway/actions` and commit-based release notes.
5. Checks npm version, integrity, available commit metadata, intended dist-tag, and
   GitHub release/tag. It downloads that exact registry version into a fresh temporary
   npm cache with scripts disabled and compares archive bytes with registry SHA-512 integrity.

Transient archive download failures are retried for a bounded interval. Missing or
mismatched archives and registry lookup failures prevent a completion report;
lookup failures are not treated as proof a version is unpublished. Logs remain at
the printed OS temporary path. Failed or pending runs return nonzero.

## Resume after failure or interruption

Retry the same version to resume a matching local or remote tag. The script checks
actual refs and runs rather than deleting tags or rolling back possibly completed pushes.

### Preparation failed

Only the expected version/dist-tag edit in `package.json` is accepted on retry,
including when staged. Resolve other changes explicitly. Prepared commits and tags
are reused. No extra release state file is maintained.

### A workflow is active or failed

- An active run is observed.
- An existing failed run receives at most one rerun per invocation, after its logs
  are saved. A newly failed run is reported without automatic retry.
- Cancellation reruns the workflow; ordinary failures rerun failed jobs.
- Timeouts and interrupted pushes may have completed remotely; retry resolves actual state.

### Publication and source disagree

An already-published version without a matching tag stops for inspection. Once a
release tag exists, new source commits require a new version. Installing or updating
personal skills is separate from releasing the package. There is no local `npm publish` path.

## First-time publication setup

Publish the initial package once, then configure:

- npm Trusted Publisher: user `jinyongp`, repository `agentskills`, workflow
  `release.yml`, allowing direct publication.
- GitHub Immutable Releases: enabled for the repository.
- `.github/npm/packages.yml`: direct publication rather than staged approval.

Subsequent npm releases use OIDC without a publish token.

## Maintain release workflows

When changing workflows, refresh action references:

```bash
npx actions-up --yes
```

Keep full commit SHA pins and explicit `ubuntu-24.04` runners. All validation matrix
jobs remain required by the Release dependency; a failed Windows job prevents publication.

[Installer verification](installer.md) · [Contributing](../CONTRIBUTING.md)
