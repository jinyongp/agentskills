# Installation and management guide

Use this guide for installer options, shared storage, conflicts, and platform
details. For a first installation, follow the [quick start](../README.md#quick-start).
The CLI requires Node.js 22.20+ and npm, with no runtime dependencies or uv requirement.

## Select skills, agents, and scope

The default scope is the current project. `--project PATH` selects an existing
directory; `--global` selects the user's global installation. Include `--global`
again on later global commands. `update` and `remove` target all recorded agents
in the selected scope unless narrowed with `--agent`.

### Install selected skills and shared rules

```bash
npx @jinyongp/agentskills@latest add --agent codex --skill review-loop verify --yes
```

`--skill` narrows skills; shared rules are still included. `--yes` applies without
prompts. Omit it to review and confirm; interactive `add` asks for unspecified
choices even when `--agent` is provided. Shared rules can be declined at the prompt.
Invalid scope input is rejected instead of silently selecting the project.

### Install all skills globally without shared rules

```bash
npx @jinyongp/agentskills@latest add --agent claude --global --no-rules --yes
```

### Connect another agent to the same project skills

```bash
npx @jinyongp/agentskills@latest add --agent claude --skill review-loop verify --no-rules --yes
```

This reuses the shared skill content already installed for Codex.

### Install only shared rules

```bash
npx @jinyongp/agentskills@latest add --agent codex --rules-only --yes
```

### Update global installations

```bash
npx @jinyongp/agentskills@latest update --global --yes
```

`update` refreshes installed skills and automatically includes skills added to the
bundle since the last recorded catalog. There is no need to identify new names or
run `add` after each release. Additions appear in the normal preview; omit `--yes`
to review and confirm them. Use `@latest` to run the newest published installer
and bundled content.

The installer remembers task-skill names it has seen separately for each agent and
scope, including names temporarily absent from a later bundle.
Skills excluded during initial selection, or explicitly removed later, are not
reinstalled just because they remain available. `--skill NAME ...` updates only
the named installed skills and leaves discovery pending for the next unrestricted
update. `--rules-only` updates rules without discovering or installing skills.
Agents with only shared rules receive the generated index but no task skills.

Records made by 0.3.1 and earlier contain no catalog history, so the installer
cannot distinguish new skills from previously excluded ones. The first unrestricted
update includes all missing bundled skills and records the catalog. Later updates
can distinguish newly added skills. Existing ownership and local-edit checks still
apply to every addition; unrelated content is never adopted or overwritten.

### Automatically generated index

`index` is generated locally by the CLI, not shipped as a fixed npm skill bundle.
Every active managed installation receives it, including rules-only installations.
It contains only task skills actually installed in this scope. Start with a task
decision route: define product behavior, plan work, implement, review, verify, write,
operate Git, or handle interfaces/motion. Routes distinguish nearby tasks and
permissions, with additional expertise selected only when needed. They are selection
guidance, not an automatic execution pipeline.

Both routes and full category catalogs give exact paths relative to the canonical
`metadata.catalog-base` directory in the frontmatter. Use that base even when reading
the index through an agent's symlink or junction. Pages are split at 2,500 characters
and include counts and continuation paths. Empty routes are omitted; installed
skills without an authored route remain discoverable in the full catalog. Skill
bodies are not loaded to build the index. Other tools' skills and plugins remain
discoverable through the agent's own available metadata.

The scope's index covers its shared installed sources, including skills connected
to another agent. Its paths lead directly to those files; an agent connection is
not a filesystem access boundary. Installing only selected skills never produces
entries for other uninstalled bundled skills.

`add`, `update`, and `remove` refresh the index automatically. A named or rules-only
update also refreshes it without adding other task skills. Removing the last
managed skill/rules installation removes its index connection and deletes the
shared index when no connections remain. `index` cannot be removed independently.
Owned static indexes from older releases are replaced automatically; edited or
unowned indexes stop the operation for explicit conflict resolution. A missing
owned generated index can be rebuilt by `update`.

The index is saved after the selected task changes. If a batch fails, completed
items remain; retry the command to reconcile the index with those completed items.
Shared instructions ask agents to consult it, but generating the file does not
force a host to load it automatically.

### Remove one skill and retain shared rules

```bash
npx @jinyongp/agentskills@latest remove --skill verify --no-rules --yes
```

Without selection flags, `remove` targets all recorded skills and rules in scope.

## Preview, completion, and cancellation

### Review the proposed changes

- The preview shows scope and exact destination paths, each shared skill change
  once, agent connections, and separate rule changes.
- Identical skills and managed rules are not rewritten. An unchanged selection
  succeeds without a confirmation prompt.
- Final confirmation for `add` and `update` is `Apply? [Y/n]`: Enter applies.
  For `remove` it is `Apply? [y/N]`: Enter cancels. Explicit `y` or `yes`
  applies for every command; `n` or an unrecognized answer cancels.
- Files and records are checked again after confirmation; edits during the prompt
  require a fresh inspection. Waiting for confirmation does not hold the installation lock.

### Cancel

- Answer `n` at confirmation to cancel. `Ctrl+C` cancels with exit code 130;
  native Windows shells can report their control-C exit status instead.

### Check completion

- Completion reports applied item count and record location. If a batch fails
  after some items complete, the error reports progress; completed items remain.
- `list` identifies an empty installation explicitly. Use `help <command>` or
  `<command> --help` for defaults, scope behavior, and examples.

## Storage and agent connections

| Agent | Project skills / rules | Global skills / rules |
| --- | --- | --- |
| Codex | `.agents/skills/` / `AGENTS.md` | `~/.codex/skills/` / `~/.codex/AGENTS.md` |
| Claude | `.claude/skills/` / `CLAUDE.md` | `~/.claude/skills/` / `~/.claude/CLAUDE.md` |

Skill content lives once in `.agents/skills/` for projects or `~/.agents/skills/`
globally. Codex reads the project source directly. Other paths in the table
connect to the shared source through relative symlinks on Linux/WSL or directory
junctions on native Windows.

- Adding another agent reuses the source.
- Updating a skill through either agent updates it for every connected agent.
- Removing a connection retains the source while another connection remains;
  removing the last connection deletes the source.
- Agents that read the shared directory directly can discover its skills
  regardless of their recorded selection.

### Older installations

On `add` or `update`, selected older CLI-owned copies are checked against their
recorded content, then consolidated for all recorded agents. Unselected skills
retain their previous installation until updated. Migration needs connection
support on the destination filesystem; a failed item restores its previous files
and record. Existing CLI-owned symlinks remain supported.

## Shared rules and conflicts

Shared rules come from [`rules/base.md`](../rules/base.md). Only the block between
`<!-- agentskills:rules:start -->` and `<!-- agentskills:rules:end -->` is managed;
project prose outside it remains intact.

The installer stops before applying selected changes when it finds:

- Modified installed skills, extra files, or redirected connections.
- Modified managed rules blocks or damaged markers.
- Symlinks inside skill content or installation parent paths; recorded agent
  connections to the shared source are accepted.
- Rules documents that are not UTF-8; no encoding conversion is attempted.

Skills installed by another tool are not adopted. Resolve conflicts explicitly,
for example by backing up edits and restoring the last installed content, then
retry. There is no force-overwrite option.

### Records and recovery

| Scope | Installation record |
| --- | --- |
| Project | `.agents/agentskills.json` |
| Global | `~/.local/share/agentskills/install.json` |

Retain these records to identify owned files. They are installation metadata,
separate from [saved task records](../README.md#saved-task-records).

Cooperating CLI operations use a lock next to the record. Individual writes are
staged and completed items recorded incrementally. A caught record-write failure
rolls back the current item while retaining earlier completed items. Backups are
removed only after the record is saved. Rollback failures report available backup
paths; retain those paths for recovery.

## Native Windows

### Shell commands

Use `npx.cmd` in PowerShell to avoid npm's `.ps1` shim execution-policy dependency:

```powershell
npx.cmd @jinyongp/agentskills@latest add --agent codex --project 'C:\Projects\My App' --skill survey --yes
npx.cmd @jinyongp/agentskills@latest add --agent claude --global --skill survey --yes
```

Command Prompt accepts the usual `npx` name:

```bat
npx @jinyongp/agentskills@latest add --agent codex --project "C:\Projects\My App" --skill survey --yes
npx @jinyongp/agentskills@latest update --global --yes
```

### Filesystem and relocation limits

- Supported native installations use writable local NTFS on Windows 11.
  Administrator access and Developer Mode are not required.
- Project paths may contain spaces and Unicode. Global `~` paths use the Windows
  user's home directory.
- The CLI checks connection support on the destination volume before creating
  connections. Failure is reported without switching to independent copies.
- Junctions contain absolute targets. Remove managed installations before moving
  a project, then install again at its new location.
- Network shares, cloud-synced directories, other filesystems, and relocation of
  existing junctions are outside the initial support scope.
- If a file is in use, close the process holding it and retry. Retain any backup
  paths reported by a failed rollback.
- Windows help and retry messages use PowerShell quoting and the `.cmd` entrypoint.

### Skill helper prerequisites

Installation and helper execution have separate requirements. Python helpers need
Python 3.11+; use the available interpreter (`python`, `py -3`, or `python3`) when
following a skill's command. The optional `verify`, `debug`, and `ci-fix` runners
require POSIX process groups. Run the project's check/reproduction command directly
on native Windows, or use WSL for those runners.

### Verification scope

These are recorded compatibility results, not checks run on every installation:

| Environment | Recorded coverage |
| --- | --- |
| Windows 11 build 26300 | Native regression and packed-package tests with a non-administrator token and Developer Mode disabled |
| Windows Server 2022 and Linux CI | Node 22.20.0, 22.x, and 24.x |
| Windows ConPTY | Confirmation, cancellation, and edits while a prompt is pending |
| Native Codex 0.162.1 and Claude Code 2.1.296 | Project/global discovery after installation and removal; Codex reads shared source and Claude follows junctions |

CI repeats agent discovery checks without account credentials or model requests.
Windows 10 is unverified and outside the verified support claim. See the
[maintainer verification instructions](../CONTRIBUTING.md#unified-installer) for reproduction.

## Install with the skills CLI

The [skills CLI](https://github.com/vercel-labs/skills) installs skills from GitHub
without this installer's shared rules or ownership records.

### Select interactively

```bash
npx skills add jinyongp/agentskills
```

### Select several skills

```bash
npx skills add jinyongp/agentskills --skill dev-docs dependency-update optimize db-migrate api-design --agent codex
```

### Install the complete collection

```bash
npx skills add jinyongp/agentskills --skill '*' --agent codex
```

### Install one skill globally

Replace `<skill-name>` with a name from a category catalog:

```bash
npx skills add jinyongp/agentskills --skill <skill-name> --agent codex --global
```

## Run from a checkout

Use the same CLI locally; replace `/path/to/agentskills` with your checkout path:

```bash
node /path/to/agentskills/agentskills.js add
node /path/to/agentskills/agentskills.js --help
node /path/to/agentskills/agentskills.js help remove
```

Authoring, testing, and publishing are covered in [CONTRIBUTING.md](../CONTRIBUTING.md).
