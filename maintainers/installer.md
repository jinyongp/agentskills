# Maintain the installer

Run commands from the repository root with Python 3.11+, uv, Node.js 22.20+, and npm.
Consumer setup lives in the
[installation guide](../docs/installation.md).

## Run installation checks

The CLI installation check requires Node.js 22.20+ and npm.
It creates two categorized fixture skills in a temporary folder, then uses pinned
`skills@1.7.0` to check discovery and selective installation:

```bash
uv run check.py smoke
```

The check compares the selected skill's `SKILL.md`, references, scripts, and assets
byte for byte, and confirms that the other skill was not installed.
The temporary project is deleted afterward. The first run needs a network connection
to download the CLI from npm. To change the CLI version, update `CLI_PACKAGE`
in `scripts/smoke_install.py` and rerun the check.

GitHub Actions runs `uv run --locked check.py --check-index` on main branch pushes,
PRs, and manual runs. Local full/format checks refresh the skill index first;
CI verifies committed generated files without rewriting them.
The reusable validation workflow also runs format checks, installer integration
tests, packed CLI lifecycle tests and skills CLI smoke checks on Ubuntu and
Windows Server 2022 with Node 22.20.0, 22.x and 24.x. The Release workflow depends
on that entire reusable workflow, so a failed Windows matrix job prevents npm
publication. Keep all matrix jobs required by that dependency.
`--locked` checks that `pyproject.toml` matches the committed dependency lockfile.
After adding a real skill, verify its local installation and behavior separately.

## CLI definitions

`agentskills.js` is the dependency-free Node CLI. `package.json` declares its npm
entrypoint and bundles the catalog, complete skill directories, shared rules,
and applicable licenses. The existing skills CLI remains supported.

Maintain CLI behavior through the definitions in `agentskills.js`: `COMMANDS`
owns supported options and command behavior. `OPTION_GROUPS` defines options in
target, selection, execution order; the flattened `OPTIONS` registry supplies
aliases, defaults, values, and conflicts. `AGENTS`/`SCOPES` own installation destinations.
Help and generated commands share this display order; input order remains free.
Parsing, help, prompts, and suggested commands use these definitions. Generate
examples with `commandLine()` using the current catalog; package identity comes
from `package.json`. Verify printed commands through actual CLI execution when
changing the interface, including selected scopes and paths requiring quoting.

`lib/skill-routes.json` owns the authored task selection conditions. The source-tree
Python generator and installed-index JavaScript renderer use the same definitions,
filtering choices to available/installed skill paths. No model classifies tasks or
rewrites routes during installation. Full catalogs retain skills outside the authored
routes; the bundle's coverage test catches missing or obsolete task names.
Keep route alternatives tied to outcomes and permission, not required workflow chains.
Routes share the 2,500-character page limit, exact continuation paths, source-index
ownership/rollback checks, and installed-index lifecycle handling.

## Package and lifecycle checks

Run the ownership/update/removal integration checks with the normal test command.
Before release, run `npm pack --dry-run` and exercise the produced tarball through
`npx` in a temporary project. Check that bundled resources and licenses are present,
and that maintainer files and Python caches are excluded. An npm release requires
an explicit publication request; local commits do not make `npx` examples available.

`uv run check.py package` packs into a temporary directory, installs that tarball
without lifecycle hooks, and invokes the installed npm shim. It checks both scopes,
both agents, bundled file bytes, shared updates, partial/final removal, and BOM/CRLF
prose preservation. Native Windows runs both PowerShell and cmd.exe and verifies
that agent connections are junctions. All homes and npm caches are isolated.
`scripts/npm_cli.py` invokes npm/npx JavaScript entrypoints directly so Python
does not need to execute `.cmd` files through an implicit shell.

## Windows verification

The Windows 11 support contract targets writable local NTFS without elevation or
Developer Mode. CI may run elevated; supplement it with a standard-user desktop
run and record the token, OS, filesystem, shells and Node versions. Windows build
26300 has been checked with a SAFER normal-user token and Developer Mode off.

### Terminal prompts

Confirmation/cancellation and prompt-time conflict tests use POSIX PTYs or the
Windows ConPTY adapter in `tests/windows_terminal.py`, with the development-only
`pyte` dependency interpreting terminal redraws. The adapter bounds buffered terminal
output and reports omitted bytes on failure.

### Agent discovery

Native Codex 0.162.1 and Claude Code
2.1.296 passed project/global skill discovery before installation, after installation
and after removal. Codex discovers the shared source; Claude reads the junction.
Repeat this check with the intended executable paths:

```bash
uv run --locked python scripts/smoke_agents.py --codex <exe> --claude <exe>
```

On Windows x64, use `--download-windows-agents` to fetch the pinned official builds
with verified integrity hashes. CI runs this check on its minimum-Node
Windows job. It isolates agent profiles, disables ancillary traffic, sends only
local discovery requests and points providers at a closed localhost port. Agent
binaries remain temporary development tools and are never bundled in the npm package.
Windows 10 has not been verified; it is outside this completed support scope.
Optional POSIX process-group helpers retain their documented platform scope.

## Shared content and rules

Keep `rules/base.md` limited to concise principles that apply to every task.
Task-specific procedures belong in independently installable skills. Installer
state belongs to the selected target, and project instructions outside managed
markers must survive installation, updates, and removal.

Store skill content once per scope in `.agents/skills/`; agent destinations use
relative symlinks on Linux/WSL or absolute-target directory junctions on Windows,
unless they read that directory directly. Version 2 records
track shared content separately from agent connections. Validate ownership of
every connected destination before modifying shared content. Migrate version 1
copies per selected skill, preserving unmigrated records and completed progress.
Check shared updates, last-connection removal, migration, and rollback with real
filesystem operations in temporary projects and homes.

Each agent record can also contain a `catalog` array of previously seen task names.
Initial task installation records the available names, including intentionally
unselected skills; an index-only/rules-only record does not count as a previous
task selection. Explicit task removal also records the removed name, even before
the next unrestricted update. Unrestricted `update` adds names absent from that history,
refreshes installed skills, then advances the catalog only after selected changes
succeed. Named updates and rules-only updates do not acknowledge new catalog
entries. Keep historical names when a later package omits them so reintroduction
does not restore excluded skills. Records without this optional field receive all missing bundled skills on
their first unrestricted update. Preserve this compatibility path for version 1
and version 2 records; never infer selection history from the current skill count.

`lib/installed-index.js` renders the installed index using the runtime template
`templates/installed-index.md.tmpl`. npm excludes `skills/tooling/index/`; that
source-tree catalog is only for repository navigation and skills CLI compatibility.
The runtime renderer filters category intentions by the projected installed state,
uses exact local paths with a canonical `metadata.catalog-base` independent of
agent aliases, and returns bounded files without reading skill bodies or
writing during preflight. `skillOperation` applies the rendered files and agent
connections with normal ownership checks, staging, record persistence and rollback.
It runs after selected task/rules changes so retries can reconcile partial batches.
Keep generated `index` out of task discovery history and automatic task additions.
Category continuation filenames use a dot separator, which is forbidden in
category names, to prevent collisions with valid names such as `workflow-2`.
Recheck referenced installed files after confirmation as well as the generated
index itself; unselected task files can change while the prompt is open.

[Back to contributing](../CONTRIBUTING.md)
