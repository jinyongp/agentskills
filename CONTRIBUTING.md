# Skill authoring guide

Each skill is an independent folder for one task. Its description must let an agent
recognize when to use it, and installing that skill alone must provide all required files.
Write documentation, skill instructions, references, catalogs, and evaluation notes in English.

## Create a skill

Run from the repository root with Python 3.11+ and uv.
Choose the closest existing category and a name that is unique across the repository.
Names must contain 1–64 lowercase ASCII letters, digits, or single hyphens.
Hyphens cannot appear at either end or consecutively.

This example creates `my-skill` in `workflow`; replace both values as needed:

```bash
uv run new_skill.py workflow my-skill
```

The command prepares:

- `SKILL.md` with its name, category, title, and saved-record convention.
- `evals/my-skill/README.md` for evaluation cases and results.
- The root category count and a new category catalog entry.

New entries appear under `New skills`; move them to the appropriate task group
and refine their short descriptions before committing.

When the `index` skill exists, preparation also refreshes its bundled catalog.
The category README entries are the single source for its short skill descriptions.
Normal verification refreshes the index automatically, so catalog edits do not
require a separate generation command:

```bash
uv run check.py validate
```

Generated catalog pages stay within 2,500 characters and split automatically.
Missing/duplicate catalog entries and references to removed skills still fail.
CI uses `uv run --locked check.py --check-index` to reject stale committed pages
without regenerating them. Use `uv run check.py validate --check-index` for the
same freshness check locally, or `uv run scripts/generate_index.py` to regenerate
without running validation. Edit category catalogs rather than generated pages
under `skills/tooling/index/references/catalog/`. Include refreshed output in the
same commit as the catalog change.

The preparation command requires an existing category and rejects duplicate names
or existing evaluation folders.

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

### Compose standalone skills

Separate task workflows from language, presentation, and platform guidance when their
triggers differ. Each installed skill must remain usable alone. When several skills
are loaded, apply specialized criteria within the requested task and produce one
result. Descriptions guide discovery; client activation is not an automatic dependency
or composition guarantee. Bundle essential boundaries rather than requiring another skill.

### Preserve task scope

Preserve user scope, output language, genre, voice, factual qualifications, and current
project choices. A style request changes communication, not implementation depth or
authorization. Ask about material unresolved decisions; settle routine details from
available evidence. Review-only and measurement-only requests retain those boundaries.

### Make criteria actionable

Tie each rule to a concrete decision or failure. Distinguish required contracts and
standards from starting values, examples, and optional recommendations. Choose form,
timing, tools, and checks from the task; word bans, sentence counts, fixed checklists,
preferred libraries, and test quotas cannot substitute for contextual judgment.
Mechanical inspection budgets protect agent input and require recoverable omissions;
they are not writing-quality scores or caps on a requested complete deliverable.

When generalizing a reported failure into reusable guidance, identify the failure
mechanism and its applicable conditions. Use independent, ordinary scenarios
for teaching examples and transfer checks; changing nouns in the reported example
does not establish generality. Preserve exact inputs when reproducing that failure,
and use supplied content when the actual deliverable requires it.

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

## Writing instructions for agents

For each description or reference link, name the task or decision that should
trigger it. List genuinely different branches, not multiple synonyms for one task.
Keep guidance needed on every branch in SKILL.md; load substantial branch-specific
detail through a local reference with its reading condition beside the link.

Group a rule with its definition, applicable exception, and resulting action so a
reader need not assemble the decision from scattered sections. State completion
as observable evidence within the requested scope. Sharpen an unclear criterion
before adding another phase, skill, agent, or approval gate.

Prefer a source pointer for cheap repository lookups such as commands, versions,
or current paths. Retain local copies of essential boundaries when standalone
installation needs them; single-source maintenance must not create a runtime
dependency on another skill or this repository's instructions.

When pruning guidance, identify the behavior it should change and review a case
needing it alongside a legitimate alternative. Non-use in one session does not
prove a rule is redundant. Measure behavioral claims with realistic runs before
claiming a benefit from terminology, wording, or deletion; format checks alone
cannot establish effectiveness. Express current choices directly while preserving
necessary safety, data and compatibility constraints.

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

### Validate formats

Check skill formats and category layout:

```bash
uv run check.py validate
```

### Run tests

Exercise normal and failure cases for validators and runtime scripts:

```bash
uv run check.py test
```

### Check skill-only installation

Verify discovery, selective installation, and copied resources:

```bash
uv run check.py smoke
```

### Check the packed installer

Exercise npm entrypoints, shared updates, and removal:

```bash
uv run check.py package
```

### Validation scope

`validate` does not require Node.js or npm. Installer integration tests require
Node.js; the installation and package smoke checks also require npm.
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

For a focused quality review, use [skill-review](skills/tooling/skill-review/SKILL.md).
It checks discovery, decision rules, standalone resources, and evaluation evidence;
its findings complement format and installation checks.

Refine the catalog descriptions added by the preparation command.
When renaming, moving, or removing skills, update root and category catalog links
and installation commands. Preserve third-party licenses and copyright notices.

Keep source attribution, upstream license declarations, and adaptation history in
each skill's `LICENSE` and `NOTICE.md`, so standalone installation retains them.
These notices are distribution metadata, not default runtime reading; omit notice
links and provenance paragraphs from `SKILL.md` and task references. Keep technical
source links that help verify task decisions, and licensing checks when the task
itself requires choosing or redistributing third-party material.

## Verify installation

Run the skill-only discovery and selective-installation fixture:

```bash
uv run check.py smoke
```

After adding a real skill, check its own local installation and behavior too.
See [installer verification](maintainers/installer.md#run-installation-checks) for
fixture details, CI coverage, and native agent discovery.

## Unified installer

The bundled CLI shares one copy of skill content per scope. Changes to its parsing,
connections, ownership, migration, or rollback need the corresponding lifecycle checks.
See [CLI maintenance and verification](maintainers/installer.md).

## Releases

Publication has no additional confirmation prompt. Follow the
[release guide](maintainers/releasing.md) for prerequisites, stable/prerelease
commands, first-time setup, and failure recovery.

## Changes and commits

Include a skill's instructions, resources, checks, and catalog updates in the same commit.
Keep independent skill or tooling changes in separate commits.
Use Conventional Commit titles, such as `feat(workflow): add my-skill`.
