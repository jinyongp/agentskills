# Agent Skills

jinyongp's Agent Skills collection, organized by task and technology.
Skills follow the [Agent Skills specification](https://agentskills.io/specification)
and install through the [skills CLI](https://github.com/vercel-labs/skills).

Once skills are published to GitHub, use these commands to browse and install them:

```bash
# List available skills
npx skills add jinyongp/agentskills --list

# Select skills interactively
npx skills add jinyongp/agentskills

# Install a specific skill: replace <skill-name> with a listed name.
npx skills add jinyongp/agentskills --skill <skill-name>

# Install globally for Codex
npx skills add jinyongp/agentskills --skill <skill-name> --agent codex --global
```

## Categories

| Category | Scope | Skills |
| --- | --- | --- |
| [workflow](skills/workflow/README.md) | Inspection, planning, test design, verification, review, debugging, benchmarking, handoff, closeout | [handoff](skills/workflow/handoff/SKILL.md), [verify](skills/workflow/verify/SKILL.md), [survey](skills/workflow/survey/SKILL.md), [plan](skills/workflow/plan/SKILL.md), [code-review](skills/workflow/code-review/SKILL.md), [debug](skills/workflow/debug/SKILL.md), [benchmark](skills/workflow/benchmark/SKILL.md), [test](skills/workflow/test/SKILL.md), [test-integration](skills/workflow/test-integration/SKILL.md), [test-maintenance](skills/workflow/test-maintenance/SKILL.md), [test-unit](skills/workflow/test-unit/SKILL.md), [test-contract](skills/workflow/test-contract/SKILL.md), [test-e2e](skills/workflow/test-e2e/SKILL.md), [test-property](skills/workflow/test-property/SKILL.md) |
| [frontend](skills/frontend/README.md) | Frameworks, UI, accessibility | None yet |
| [git](skills/git/README.md) | Commits, branches, remote synchronization, conflicts, PRs, worktrees | [git-commit](skills/git/git-commit/SKILL.md), [git-branch](skills/git/git-branch/SKILL.md), [git-sync](skills/git/git-sync/SKILL.md), [git-conflict](skills/git/git-conflict/SKILL.md), [git-pr](skills/git/git-pr/SKILL.md), [git-worktree](skills/git/git-worktree/SKILL.md) |
| [writing](skills/writing/README.md) | Conversation styles, summaries, documentation, editing | [clear](skills/writing/clear/SKILL.md), [terse](skills/writing/terse/SKILL.md) |
| [tooling](skills/tooling/README.md) | Development tool setup and operation | None yet |

Skills live at `skills/<category>/<skill-name>/SKILL.md`.
Categories organize the repository catalog; select a skill by its unique name when installing.

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
The writing skills [clear](skills/writing/clear/SKILL.md) and
[terse](skills/writing/terse/SKILL.md) are adapted from
[attention-span](https://github.com/alexgreensh/attention-span) under AGPL-3.0;
their bundled LICENSE and NOTICE.md apply to each skill.
Third-party material retains its original license and copyright notices.
