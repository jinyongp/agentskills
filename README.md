# Agent Skills

jinyongp's Agent Skills collection, organized by task and technology.
Skills follow the [Agent Skills specification](https://agentskills.io/specification).
The bundled CLI manages skills and shared rules together; the
[skills CLI](https://github.com/vercel-labs/skills) remains compatible for skill-only installs.

## Unified installer

The CLI is ready locally. The commands below require publication of
`@jinyongp/agentskills` to npm; the package is not published yet.

```bash
npx @jinyongp/agentskills@latest add
npx @jinyongp/agentskills@latest update
npx @jinyongp/agentskills@latest list
npx @jinyongp/agentskills@latest remove
```

`add` asks for Codex or Claude, project or global scope, and skill names, then
shows the proposed changes before applying them. Shared rules are included.
Use `@latest` to run the newest published installer and bundled content.
`update` reuses recorded selections; newly available skills require `add`.

Run the same CLI now from a checkout:

```bash
node /path/to/agentskills/agentskills.js add
node /path/to/agentskills/agentskills.js --help
node /path/to/agentskills/agentskills.js help remove
```

For explicit selections or unattended use:

```bash
# Install two skills and shared rules into the current project
npx @jinyongp/agentskills@latest add --agent codex --skill review-loop verify --yes

# Install all skills globally without shared rules
npx @jinyongp/agentskills@latest add --agent claude --global --no-rules --yes

# Install only shared rules
npx @jinyongp/agentskills@latest add --agent codex --rules-only --yes

# Update only the recorded global installations
npx @jinyongp/agentskills@latest update --global --yes

# Remove one skill while retaining shared rules
npx @jinyongp/agentskills@latest remove --skill verify --no-rules --yes
```

Omit `--yes` to review and confirm changes. `--project PATH` targets an existing
project directory. The default scope is the current directory; global scope must
be selected with `--global` on subsequent commands. `update` and `remove` target
all recorded agents in that scope, or just the selected `--agent`.
Skill selection and rule selection are separate: `--skill` narrows skills;
use `--no-rules` to exclude shared rules from that operation.
Interactive `add` asks for unspecified choices even when `--agent` is provided.
Shared rules can be declined at the prompt. An invalid scope is rejected instead
of silently installing into the project. Answer `n` at confirmation to cancel;
`Ctrl+C` cancels with exit code 130. Waiting for confirmation does not hold the
installation lock.

The preview shows the selected scope and exact destination paths. Completion
reports the applied item count and record location. If a batch fails after some
items completed, the error reports that progress; those completed items remain.
`list` identifies an empty installation explicitly. Use `help <command>` or
`<command> --help` for defaults, scope behavior, and examples.

| Agent | Project skills / rules | Global skills / rules |
| --- | --- | --- |
| Codex | `.agents/skills/` / `AGENTS.md` | `~/.codex/skills/` / `~/.codex/AGENTS.md` |
| Claude | `.claude/skills/` / `CLAUDE.md` | `~/.claude/skills/` / `~/.claude/CLAUDE.md` |

Shared rules come from `rules/base.md`. Only the block between
`<!-- agentskills:rules:start -->` and `<!-- agentskills:rules:end -->` is managed;
project prose outside it remains intact. Existing skills installed by another
tool are not adopted. Modified skills, extra files, modified rules blocks,
damaged markers, and symlinks stop the operation before applying selected changes.
Rules documents must be UTF-8; other encodings are rejected without conversion.
Files and the installation record are checked again after confirmation, so edits
made while the prompt is pending require a fresh inspection.
Resolve a conflict explicitly, such as backing up edits and restoring the last
installed content, then retry. There is no force-overwrite option.

Installation records live at `.agents/agentskills.json` in projects and
`~/.local/share/agentskills/install.json` globally. Retain them to identify owned
files; they are installation metadata, not saved task records. Cooperating CLI
operations use a lock next to the record. Individual writes are staged; completed
items are recorded incrementally. A caught record-write failure rolls back the
current item while retaining earlier completed items. Backups are removed only
after the installation record is saved. Record-write rollback failures report
available backup paths.

The CLI requires Node.js 22.20+ and npm, with no runtime dependencies or uv requirement.

## Install with the skills CLI

Once skills are published to GitHub, use these commands to browse and install them:

```bash
# List available skills
npx skills add jinyongp/agentskills --list

# Select skills interactively
npx skills add jinyongp/agentskills

# Install several skills together
npx skills add jinyongp/agentskills --skill dev-docs dependency-update optimize db-migrate api-design --agent codex

# Install the complete collection for Codex
npx skills add jinyongp/agentskills --skill '*' --agent codex

# Install a specific skill: replace <skill-name> with a listed name.
npx skills add jinyongp/agentskills --skill <skill-name>

# Install globally for Codex
npx skills add jinyongp/agentskills --skill <skill-name> --agent codex --global
```

## Categories

| Category | Scope | Skills |
| --- | --- | --- |
| [workflow](skills/workflow/README.md) | Implementation, inspection, planning, test design, verification, review, debugging, benchmarking, handoff, closeout | [handoff](skills/workflow/handoff/SKILL.md), [verify](skills/workflow/verify/SKILL.md), [survey](skills/workflow/survey/SKILL.md), [plan](skills/workflow/plan/SKILL.md), [code-review](skills/workflow/code-review/SKILL.md), [debug](skills/workflow/debug/SKILL.md), [benchmark](skills/workflow/benchmark/SKILL.md), [test](skills/workflow/test/SKILL.md), [test-integration](skills/workflow/test-integration/SKILL.md), [test-maintenance](skills/workflow/test-maintenance/SKILL.md), [test-unit](skills/workflow/test-unit/SKILL.md), [test-contract](skills/workflow/test-contract/SKILL.md), [test-e2e](skills/workflow/test-e2e/SKILL.md), [test-property](skills/workflow/test-property/SKILL.md), [implement](skills/workflow/implement/SKILL.md), [dependency-update](skills/workflow/dependency-update/SKILL.md), [optimize](skills/workflow/optimize/SKILL.md), [db-migrate](skills/workflow/db-migrate/SKILL.md), [api-design](skills/workflow/api-design/SKILL.md), [review-loop](skills/workflow/review-loop/SKILL.md) |
| [frontend](skills/frontend/README.md) | Web and native UI, accessibility, motion | [ui-design](skills/frontend/ui-design/SKILL.md), [responsive](skills/frontend/responsive/SKILL.md), [accessibility](skills/frontend/accessibility/SKILL.md), [animate](skills/frontend/animate/SKILL.md), [animation-review](skills/frontend/animation-review/SKILL.md), [animation-audit](skills/frontend/animation-audit/SKILL.md), [animation-opportunities](skills/frontend/animation-opportunities/SKILL.md), [animation-vocabulary](skills/frontend/animation-vocabulary/SKILL.md), [animate-native](skills/frontend/animate-native/SKILL.md), [animation-debug](skills/frontend/animation-debug/SKILL.md), [animation-performance](skills/frontend/animation-performance/SKILL.md), [prototype](skills/frontend/prototype/SKILL.md), [ui-stress](skills/frontend/ui-stress/SKILL.md), [ui-library](skills/frontend/ui-library/SKILL.md), [mobile-web](skills/frontend/mobile-web/SKILL.md) |
| [git](skills/git/README.md) | Commits, branches, remote synchronization, conflicts, PRs, worktrees | [git-commit](skills/git/git-commit/SKILL.md), [git-branch](skills/git/git-branch/SKILL.md), [git-sync](skills/git/git-sync/SKILL.md), [git-conflict](skills/git/git-conflict/SKILL.md), [git-pr](skills/git/git-pr/SKILL.md), [git-worktree](skills/git/git-worktree/SKILL.md) |
| [writing](skills/writing/README.md) | Conversation styles, summaries, documentation, editing | [clear](skills/writing/clear/SKILL.md), [terse](skills/writing/terse/SKILL.md), [brief](skills/writing/brief/SKILL.md), [summarize](skills/writing/summarize/SKILL.md), [rewrite](skills/writing/rewrite/SKILL.md), [write](skills/writing/write/SKILL.md), [korean-writing](skills/writing/korean-writing/SKILL.md), [english-writing](skills/writing/english-writing/SKILL.md), [dev-docs](skills/writing/dev-docs/SKILL.md) |
| [tooling](skills/tooling/README.md) | Development tool setup and operation | None yet |

Skills live at `skills/<category>/<skill-name>/SKILL.md`.
Categories organize the catalog. Select several unique skill names in one command,
choose them interactively, or use the quoted `'*'` selector for the collection.

## Testing workflows

| Skill | Use when | Required justification |
| --- | --- | --- |
| [test](skills/workflow/test/SKILL.md) | Decide whether and where to add coverage | A named failure, an observable contract, and a meaningful coverage gap |
| [test-integration](skills/workflow/test-integration/SKILL.md) | Exercise a real dependency or module boundary | Evidence that isolated/static checks cannot supply |
| [test-maintenance](skills/workflow/test-maintenance/SKILL.md) | Audit or improve existing tests | A concrete maintenance cost and preserved failure detection |
| [test-unit](skills/workflow/test-unit/SKILL.md) | Check isolated calculations, decisions, or state transitions | An uncovered logic failure at a stable interface |
| [test-contract](skills/workflow/test-contract/SKILL.md) | Verify consumer/provider compatibility | Independently justified expectations and provider conformance |
| [test-e2e](skills/workflow/test-e2e/SKILL.md) | Exercise a critical journey from the actual entrypoint | A user outcome whose failure cheaper checks cannot expose |
| [test-property](skills/workflow/test-property/SKILL.md) | Explore generated inputs or state transitions | An independently justified invariant and meaningful domain |

Each works independently. Choose by the requested work rather than loading all of them.
Reuse existing checks when sufficient; adding no new test is a valid outcome.
Property testing is a technique that can use unit or integration boundaries;
contract testing focuses on compatibility rather than a required execution layer.

## Add a skill

From the repository root, specify a category and name to prepare the skill,
evaluation notes, and catalog entries:

```bash
uv run new_skill.py workflow my-skill
```

Write the triggers, procedure, and result checks in the generated `SKILL.md`.
See the [authoring guide](CONTRIBUTING.md) for options and rules.
Bundle required files in the skill's `scripts/`, `references/`, or `assets/`
directories so they remain available after individual installation.

Run all checks from the repository root with one command.
This requires Python 3.11+, uv, Node.js 22.20+, and npm.

```bash
uv run check.py
```

The command prepares development dependencies and runs format validation, tests,
and installation checks in a temporary project.
For a quick format and layout check, use `uv run check.py validate`.
GitHub Actions runs the same script with `--locked` to enforce committed dependency versions.
See the [verification instructions](CONTRIBUTING.md#verify-before-committing) for details.
Skill users do not need these maintenance tools.

## Saved task records

When a workflow needs saved records, skills default to
`.agents/artifacts/<run-id>/<skill-name>/` in the target project.
User destinations and project conventions take precedence. Inline results stay
inline unless saving is requested or needed by the workflow. Records remain local.
See the [record convention](CONTRIBUTING.md#saved-task-records) for run IDs and contents.

## License

Original repository content uses the [MIT License](LICENSE). Individual skills
declare their license in SKILL.md and bundle applicable notices.
The writing skills [clear](skills/writing/clear/SKILL.md),
[terse](skills/writing/terse/SKILL.md), [brief](skills/writing/brief/SKILL.md), and
[summarize](skills/writing/summarize/SKILL.md) are adapted from
[attention-span](https://github.com/alexgreensh/attention-span) under AGPL-3.0;
their bundled LICENSE and NOTICE.md apply to each skill.
Third-party material retains its original license and copyright notices.
