# Skill authoring guide

Each skill is an independent folder for one task. Its description must let an agent
recognize when to use it, and installing that skill alone must provide all required files.
Write documentation, skill instructions, references, catalogs, and evaluation notes in English.

## Create a skill

Choose the closest existing category and a name that is unique across the repository.
Names must contain 1–64 lowercase ASCII letters, digits, or single hyphens.
Hyphens cannot appear at either end or consecutively.

This example creates `my-skill` in `workflow`; replace both values as needed:

```bash
uv run new_skill.py workflow my-skill
```

The command sets `name`, `metadata.category`, and the title in `SKILL.md`,
creates `evals/my-skill/README.md`, and adds root and category catalog entries.
It requires an existing category and rejects duplicate names or existing evaluation folders.
Preparation requires Python 3.11+ and uv.

You can also supply a description:

```bash
uv run new_skill.py workflow my-skill --description "Describe the task and when to use it."
```

Replace the generated guidance with actual instructions and fill in the evaluation cases.
Add resource directories only when needed. This command prepares the files;
writing instructions, evaluating behavior, committing, and publishing are subsequent steps.

## File layout

```text
skills/<category>/<skill-name>/
├── SKILL.md
├── scripts/       # Executable helpers, when needed
├── references/    # Detailed material loaded when needed
└── assets/        # Templates, sample data, images
```

Place `SKILL.md` only in actual skill directories.
Putting it at the repository or category root affects CLI discovery of nested skills.
Keep templates under a separate extension, such as `skill.md.tmpl`.

Reference bundled files relative to the skill root, and include them inside the skill
so they are copied during individual installation. Runtime dependencies must not rely
on author-specific absolute paths, the repository's `AGENTS.md`, or other skill folders.

## Metadata and instructions

`SKILL.md` contains YAML frontmatter and a Markdown body.

- `name`: matches the skill directory name.
- `description`: explains the task and when to use the skill in 1–300 characters.
- `metadata.author`: author name as a string.
- `metadata.category`: category directory name as a string.
- `compatibility`: required environment, if applicable; at most 500 characters.
- `license`: the skill's license; MIT is the repository default.

Category metadata and ASCII naming constraints are repository rules.
Other format requirements follow the [Agent Skills specification](https://agentskills.io/specification).
Store additional maintenance metadata as string values under `metadata`.

Keep the body to scope, prerequisites, essential steps, and result or failure checks.
Omit general knowledge and repetition while preserving context that affects decisions
and conditions for protecting existing work. Use short lists and steps, within 4,000 characters.
The description and body limits are repository policy, enforced by validation and CI.

## Decision quality and composition

Separate task workflows from language, presentation, and platform guidance when their
triggers differ. Each installed skill must remain usable alone. When several skills
are loaded, apply specialized criteria within the requested task and produce one
result. Descriptions guide discovery; client activation is not an automatic dependency
or composition guarantee. Bundle essential boundaries rather than requiring another skill.

Preserve user scope, output language, genre, voice, factual qualifications, and current
project choices. A style request changes communication, not implementation depth or
authorization. Ask about material unresolved decisions; settle routine details from
available evidence. Review-only and measurement-only requests retain those boundaries.

Tie each rule to a concrete decision or failure. Distinguish required contracts and
standards from starting values, examples, and optional recommendations. Choose form,
timing, tools, and checks from the task; word bans, sentence counts, fixed checklists,
preferred libraries, and test quotas cannot substitute for contextual judgment.
Mechanical inspection budgets protect agent input and require recoverable omissions;
they are not writing-quality scores or caps on a requested complete deliverable.

Use existing coverage before adding lasting tests. Report observed, inferred, and
unverified behavior separately. Format validation, installation, scripted replay,
parent instruction review, and independent agent execution establish different things;
record the evidence actually obtained without promoting one into another.

When a rule leaves the next action unclear, specify its trigger, the observable
evidence to inspect, and the decision that evidence changes. For example, replace
"keep documentation clear" with "when internals interrupt an API-call example,
keep details that change the call or explain its result beside that step; link
independent implementation rationale separately." Evaluate a case needing the
detail as well as one where it distracts. Keep this authoring check out of generated
deliverables; it is a way to improve instructions, not a mandatory output template.

Recover agreed scope, deliberate omissions, and accepted tradeoffs before judging
completion or proposing fixes. Preserve their rationale through plans and handoffs.
Absence alone establishes no missing requirement. Anchor findings to the active
contract, an in-scope regression, or a concrete reachable safety/data violation.
Unknown intent needs evidence or clarification; it does not authorize expanded
features, recovery flows, hardening, or tests. Review every requested area while
limiting repeated review to changed effects and invalidated evidence.

## Tool selection

Task skills choose tools from the user's current instructions and applicable repository
requirements. Reuse a suitable existing tool before adding one; explain capability or
availability gaps before substituting a tool that changes the requested workflow.

Tool-specific skills are valid. Make their scope clear in the name and description,
and state actual prerequisites in the body or `compatibility`. Keep portable task
skills focused on required capabilities rather than a mandatory product.
The specification's experimental `allowed-tools` field depends on client support;
it is not a portable enforcement mechanism.

## Saved task records

Generated records belong to the target project, separate from installed skill files.
Follow an explicit user destination or project convention first. Otherwise use:

```text
<project-root>/.agents/artifacts/<run-id>/<skill-name>/
```

For a new run, create a fresh ID from a UTC timestamp plus a unique suffix, for example
`20261003T090000Z-a7f2c9`. Reserve its directory without replacing an existing one;
retry a collision with a different suffix. An explicitly supplied run ID can group
multiple skills working on the same task. Use the current checkout root, or the selected
working directory outside a repository. Resolve actual paths before returning them.

Persist only requested records or evidence needed by the workflow. Inline inspection,
planning, and handoff results remain inline by default. Disposable command files belong
in the OS temporary directory. Source changes and requested deliverables keep their
normal project destinations; this convention covers task records, not all created files.

A saved `summary.md`, when useful, contains only the goal, result/status, essential
decisions or reproduction details, remaining gaps/next action, and links to raw evidence.
Omit empty fields and link recoverable repository facts. Keep tool exports in their native
format and logs separate. A handoff packet may be `handoff.md` without a duplicate summary.
Read selected summaries first and only relevant raw evidence afterward. Folder existence
does not prove completion; record failed or partial runs accurately.

Preserve existing records unless an update was requested. Report exact output paths.
Records stay local; committing or publishing them requires an explicit request.
Respect existing ignore rules. This repository ignores `/.agents/artifacts/`; installing
a skill does not modify another project's ignore configuration.

Every installed skill carries the short convention itself, so individual installation
needs no shared skill or root document. `templates/saved-records.md.tmpl` is the canonical
maintenance fragment; `new_skill.py` appends it during preparation. Keep existing copies
aligned when revising the convention and within the skill body budget.

## Agent input budget

Start with the smallest summary needed to decide the next action, then request relevant detail.
Do not aim to fill specification limits or move an unchanged full dump into a script.

- Move conditional detail into `references/` and state when to read it.
  Do not load every reference at startup.
- Use self-contained `scripts/` for repeated mechanical inspection or large-output reduction.
  Execute them by default; read their source when editing or investigating failures.
- Default inspection output should contain state, counts, and facts needed for decisions.
  Return full diffs, long logs, or file contents only for selected detail requests.
- Define output limits and report omissions, total counts, and the next page position.
  Never silently shorten paths, changes, or errors and present them as complete.
  Bound follow-up requests too, and inspect required pages before making changes.
- Test normal inputs, large inputs, and failures for output size, information recovery,
  and preservation of existing work. Record the results in evaluation notes.
  Retain essential context when reducing length.

Token counts vary by the agent's tokenizer and the detail required.
Enforce character limits and selective queries to avoid unnecessary default input.
The `git-commit` inspection helper limits each JSON response to 4,000 characters,
including escaped characters and the trailing newline.

## Verify before committing

Test additions must protect a named failure or contract absent from existing checks.
Prefer extending useful coverage, or reusing lint, type, and schema validation, over
adding a separate test for each change. Inspecting or validating a task does not
automatically require permanent test code.

Assert stable behavior and required contracts, with independently justified expectations.
Exact literals, document structures, HTML attributes, snapshots, and architecture
constraints need a concrete reason; preserve legitimate implementation freedom.
Evaluate additional confidence against setup, runtime, failure-analysis, and maintenance
cost. Removing a redundant or incidental assertion must preserve meaningful coverage.
See the [test skill](skills/workflow/test/SKILL.md) for the full decision procedure.

Full verification requires Python 3.11+, [uv](https://docs.astral.sh/uv/),
Node.js 22.20+, and npm. Run from the repository root:

```bash
uv run check.py
```

The command prepares development dependencies, validates formats, runs tests,
and checks CLI installation. Any failed step makes the command fail.
You can run each check separately:

| Command | Checks |
| --- | --- |
| `uv run check.py validate` | Skill formats and category layout |
| `uv run check.py test` | Normal and failure cases for validators and runtime scripts |
| `uv run check.py smoke` | CLI discovery, selective installation, resource copying |

`validate` and `test` do not require Node.js or npm.
Repository validation uses the official `skills-ref` validator and checks category layout,
ASCII names, repository-wide name uniqueness, and matching `metadata.category`.
An empty initial catalog is valid; an existing skill directory must contain `SKILL.md`.
To validate one skill:

```bash
uv run --locked skills-ref validate skills/<category>/<skill-name>
```

`skills-ref` is a development reference tool pinned to a commit in the official repository.
It is not a runtime dependency of installed skills.
Authors must check that referenced files exist and evaluate actual behavior using
the [evaluation guide](evals/README.md).
Format validation does not establish instruction quality or compatibility with every agent.

Refine the catalog descriptions added by the preparation command.
When renaming, moving, or removing skills, update root and category catalog links
and installation commands. Preserve third-party licenses and copyright notices.

## Verify installation

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

GitHub Actions runs `uv run --locked check.py` on main branch pushes, PRs, and manual runs.
`--locked` checks that `pyproject.toml` matches the committed dependency lockfile.
After adding a real skill, verify its local installation and behavior separately.

### Unified installer

`agentskills.js` is the dependency-free Node CLI. `package.json` declares its npm
entrypoint and bundles the catalog, complete skill directories, shared rules,
and applicable licenses. The existing skills CLI remains supported.

Maintain CLI behavior through the definitions in `agentskills.js`: `COMMANDS`
owns supported options and command behavior, `OPTIONS` owns aliases, defaults,
values, and conflicts, and `AGENTS`/`SCOPES` own installation destinations.
Parsing, help, prompts, and suggested commands use these definitions. Generate
examples with `commandLine()` using the current catalog; package identity comes
from `package.json`. Verify printed commands through actual CLI execution when
changing the interface, including selected scopes and paths requiring quoting.

Run the ownership/update/removal integration checks with the normal test command.
Before release, run `npm pack --dry-run` and exercise the produced tarball through
`npx` in a temporary project. Check that bundled resources and licenses are present,
and that maintainer files and Python caches are excluded. An npm release requires
an explicit publication request; local commits do not make `npx` examples available.

Keep `rules/base.md` limited to concise principles that apply to every task.
Task-specific procedures belong in independently installable skills. Installer
state belongs to the selected target, and project instructions outside managed
markers must survive installation, updates, and removal.

## Changes and commits

Include a skill's instructions, resources, checks, and catalog updates in the same commit.
Keep independent skill or tooling changes in separate commits.
Use Conventional Commit titles, such as `feat(workflow): add my-skill`.
