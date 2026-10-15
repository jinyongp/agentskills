# Agent Skills

Task-focused skills for Codex and Claude: inspect repositories, implement and review
code, work with Git, build interfaces, and write documentation. Install the skills
you need, with optional shared working rules.

[Quick start](#quick-start) · [Browse skills](#categories) ·
[Manage installations](#manage-installations) · [Compatibility](#compatibility)

<a id="unified-installer"></a>

## Quick start

Requirements:

- **Installer:** Node.js 22.20+ and npm. No uv or Python required for installation.
- **Example below:** Codex and Python 3.11+ for the `survey` skill's helper.
- **PowerShell:** use `npx.cmd` in place of `npx`; see [Native Windows](#native-windows).

### 1. Install one skill

Run this from the project where you want to use it:

```bash
npx @jinyongp/agentskills@latest add --agent codex --project . --skill survey
```

The installer asks whether to include shared rules in `AGENTS.md`, then previews
the changes for confirmation. Confirm to install; answer `n` to cancel.

### 2. Check the installation

```bash
npx @jinyongp/agentskills@latest list --agent codex --project .
```

Under **Installed**, look for `survey` and the Codex project path.
The skill lives at `.agents/skills/survey/`; the installation record lives at
`.agents/agentskills.json`.

### 3. Use the skill

Open Codex in that project and make a request such as:

> Use the survey skill to map this repository. Report its main folders, project
> commands, risks, and next checks.

The intended result is a repository map and suggested checks. `survey` inspects
files without running project code or changing source files.

For Claude, select `--agent claude` when installing. For interactive selection of
agent, scope, and skills, run `npx @jinyongp/agentskills@latest add`.

## Categories

Each category links to its complete skill catalog and installation commands.

| Category | Choose for | Skills |
| --- | --- | --- |
| [workflow](skills/workflow/README.md) | Planning, implementation, review, debugging, testing, and research | 33 |
| [frontend](skills/frontend/README.md) | UI, accessibility, responsive layouts, and motion | 15 |
| [git](skills/git/README.md) | Commits, branches, synchronization, conflicts, PRs, and worktrees | 6 |
| [writing](skills/writing/README.md) | Documentation, drafting, editing, summaries, and conversation styles | 10 |
| [tooling](skills/tooling/README.md) | Skill selection, skill review, and development tool operation | 2 |

Choose by the task you need done; skills work independently. For example,
`code-review` reports defects, `review-loop` reviews and fixes, and `verify` runs
checks and reports evidence. Skills follow the
[Agent Skills specification](https://agentskills.io/specification).

The CLI automatically creates an `index` skill from the skills actually installed
in the selected scope. It includes compact category pages, short intentions, and
exact local paths. Installation, updates, and removal refresh it automatically;
there is no separate index installation or generation command. Partial skill
selections are supported, and uninstalled skills do not appear in the index.
Shared rules direct agents to read it before choosing the applicable instructions.
This is an instruction to the agent, not a host-enforced automatic-load guarantee.

## Manage installations

Use `@latest` to run the newest published installer and bundled content.

### Add skills

Select skills and optional shared rules:

```bash
npx @jinyongp/agentskills@latest add
```

### Update installed skills

Refresh installed skills and automatically add newly bundled skills. You do not
need to find their names or run a separate `add` command. Previously excluded or
removed skills stay excluded once the installer has recorded the catalog.

```bash
npx @jinyongp/agentskills@latest update
```

Older installation records have no catalog history. Their first unrestricted
update includes all missing bundled skills and records the current catalog.
Use `--skill NAME ...` to update only specific installed skills.

### Inspect installations

Show available skills and recorded installations:

```bash
npx @jinyongp/agentskills@latest list
```

### Remove installations

Preview removal of recorded skills and rules, then confirm:

```bash
npx @jinyongp/agentskills@latest remove
```

### Choose scope and content

| Option | Effect |
| --- | --- |
| `--project PATH` | Target an existing project directory; default is the current directory |
| `--global` | Target the user's global installation; include it on every global command |
| `--agent codex` / `--agent claude` | Select an agent; `update` and `remove` otherwise target all recorded agents in scope |
| `--skill NAME ...` | Select named skills; shared rules remain included unless excluded |
| `--no-rules` / `--rules-only` | Manage only skills / only shared rules |
| `--yes` | Apply without prompts; `add` also requires `--agent` |

Updates to a shared skill affect every connected agent. Modified installed content
stops the operation for explicit conflict resolution; there is no force-overwrite
option. See the [installation guide](docs/installation.md) for additional examples,
storage paths, shared rules, migration, and recovery.

## Compatibility

- **Linux / WSL:** agent connections use relative symlinks.
- **Native Windows 11:** writable local NTFS; connections use directory junctions.
- **Skill helpers:** Python helpers need Python 3.11+. The optional `verify`, `debug`,
  and `ci-fix` runners need POSIX process groups; on native Windows, use the project's
  command directly or run those helpers in WSL.

### Native Windows

In PowerShell, use the `.cmd` entrypoint:

```powershell
npx.cmd @jinyongp/agentskills@latest add --agent codex --project 'C:\Projects\My App' --skill survey
```

Administrator access and Developer Mode are not required. Remove managed
installations before moving a project, then install again at its new location.
Windows 10, network shares, and cloud-synced directories are outside the verified
support scope. See [Windows setup, limits, and verification](docs/installation.md#native-windows).

## Install with the skills CLI

The [skills CLI](https://github.com/vercel-labs/skills) also supports skill-only
installation from GitHub. It does not install this collection's shared rules.

Browse available skills:

```bash
npx skills add jinyongp/agentskills --list
```

Install a selected skill for Codex:

```bash
npx skills add jinyongp/agentskills --skill survey --agent codex
```

See [alternative installation examples](docs/installation.md#install-with-the-skills-cli).
The bundled installer does not adopt skills owned by another tool.

## Testing workflows

Start with `test` to assess whether coverage is needed. Use a specialized skill when
the task calls for a specific boundary or technique. The
[testing skill guide](docs/testing-skills.md) compares all seven choices.

## Saved task records

- Inline results stay inline unless saving is requested or needed by the workflow.
- Saved records default to `.agents/artifacts/<run-id>/<skill-name>/` in the target project.
- User destinations and project conventions take precedence; records remain local.

See the [record convention](CONTRIBUTING.md#saved-task-records) for run IDs and contents.

<a id="add-a-skill"></a>
<a id="release"></a>

## Contributing

Skills live at `skills/<category>/<skill-name>/SKILL.md`. Maintainer tasks have
separate instructions:

- [Create or update a skill](CONTRIBUTING.md#create-a-skill)
- [Run repository checks](CONTRIBUTING.md#verify-before-committing)
- [Publish a release](CONTRIBUTING.md#releases)

## License

Original repository content uses the [MIT License](LICENSE). Individual skills
declare their license in SKILL.md and bundle applicable notices.
The writing skills [clear](skills/writing/clear/SKILL.md),
[terse](skills/writing/terse/SKILL.md), [brief](skills/writing/brief/SKILL.md), and
[summarize](skills/writing/summarize/SKILL.md) are adapted from
[attention-span](https://github.com/alexgreensh/attention-span) under AGPL-3.0;
their bundled LICENSE and NOTICE.md apply to each skill.
Third-party material retains its original license and copyright notices.
