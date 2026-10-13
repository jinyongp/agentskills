# README evaluation history

Historical records retain their original wording, dates, environments, and
limitations. Their checks do not automatically apply to later revisions.

## Command presentation correction — 2026-10-13

User rejected the management task/command/behavior table in the authored README:
rows described independent operations rather than supporting a comparison. Replaced
it with task headings, brief explanations, and fenced commands. This observed
feedback qualifies the earlier application; reduced length and passing checks did
not establish a useful format choice. Parent instruction review covers the pair:

| Condition | Expected decision |
| --- | --- |
| Readers know they want to add, update, list, or remove | Use task headings with executable examples |
| Readers choose installation methods by agent support, scope, or included rules | Use a comparison table when those attributes change the choice |

No new executable behavior or permanent presentation assertions were added.

## Repository README application — 2026-10-13

Parent applied the revised skill to this repository's README: first installation,
installation check, and an example skill request now precede management detail.
Category rows compare purpose and counts; full lists remain in category catalogs.
Installer internals and Windows verification moved to `docs/installation.md`;
the testing comparison moved to `docs/testing-skills.md`. Existing root section
anchors were retained. README length fell from 17,593 to 7,183 characters (59%).

On Linux/WSL with Node 26.10.0, 36 local links/anchors and all five category counts
passed. The quick-start candidate installed and listed `survey`; its installed
summary/entries helper ran without changing project files. The example agent prompt
was not submitted to a model. npm's dry-run manifest included both new guides.
Repository validation passed for 58 skills; the 143-test suite passed with one skip. Skills CLI
discovery/selective installation and packed project/global lifecycle checks passed.
An initial smoke run could not write the default npm cache; retrying that stage
with a temporary cache succeeded. The scaffold tests now protect count refresh and
preserved catalog content. Registry `@latest` and native Windows were not exercised.
This is an authored application with scoped checks, not independent reader evaluation.

## Information grouping and presentation — 2026-10-13

Parent instruction review against the current repository README and paired cases;
model version not exposed. The earlier review emphasized missing first use and
command flow while underweighting scanability. These cases check the revised rules,
not independent drafting, reader comprehension, or comparative quality gains.

| Condition | Expected decision |
| --- | --- |
| README mixes defaults, cancellation, locks, migration, and rollback in consecutive paragraphs | Group consumer tasks; retain invocation-changing facts and link independent operational detail |
| Install, update, remove, and alternative setups share one long code block | Separate independent tasks with labels and focused examples; preserve one initial path |
| Category table contains dozens of links in one cell | Use summary rows with specific catalog links or grouped lists; do not assume table syntax makes navigation useful |
| Agent/path table compares the same attributes across agents | Retain the useful comparison |
| A paragraph explains why an installation constraint exists | Keep coherent prose when the reason helps the task; do not bullet each sentence |
| A short README already exposes setup and first use | Preserve its simple form; no mandatory table, diagram, or extra sections |
| A platform restriction changes the next install command | Keep it before that command even when moving other detail |
| Commands pass but prerequisites and results require reading every paragraph | Report discovery failure separately from command correctness and before wording polish |

The README structure reference is bundled inside this skill; no `dev-docs`
installation is required. Scope remains review-only when requested, and no prose,
heading, or table-count assertions were added.

Revision verification: `uv run check.py validate` passed for 58 skills, and creator
validation passed. Body: 3,947 characters. Reference paths and the canonical saved-record
fragment passed. On Linux/WSL with Node 26.10.0, standalone local CLI installation
into temporary Codex and Claude projects matched all four bundled files byte-for-byte;
the Claude connection resolved correctly. Temporary projects were removed. Registry,
native Windows, and independent writing quality were not tested for this revision.

## Decision cases — 2026-10-07

Parent instruction review in Codex; exact model version not recorded. These cases
assess written boundaries, not independently generated READMEs or comparative gains.

| Request or condition | Expected decision | Review result |
| --- | --- | --- |
| Published library README | Registry installation, imports, public call, recognizable result | Steps 1, 4, 5, 7 |
| CLI or plugin README | Command or registration plus use, with actual prerequisites | Steps 4 and 5 |
| SDK requires an account and paid call | Document setup; report blocked live verification instead of inventing output | Steps 5 and 7 |
| Registry package with clone/dev-server instructions first | Put consumer installation first; separate maintainer setup | Step 4 |
| Package actually ships only from source | Retain required checkout/build in that distribution path | Step 4 permits genuinely required setup |
| Checkout API absent from the release | Target documented version; mark unreleased behavior distinctly | Steps 1 and 7 |
| Example imports an unexported checkout module | Check entry points in a fresh consumer environment | Steps 1, 5, 7 |
| Mutation caveat changes the call | Keep caveat beside the affected step | Step 6 |
| Internal design interrupts setup | Link independent rationale after first-use path | Steps 3 and 6 |
| Required platform limit or cleanup | Keep before incompatible setup or within correct usage | Steps 4, 5, 6 |
| Missing configuration prevents success | Identify missing step, reader impact, scoped repair | Steps 5 and 8 |
| Unsupported superiority or speed claim | Require evidence or omit claim | Step 3 |
| Review-only request | Return findings; preserve files and product scope | Scope and result |
| Full API reference, runbook, or profile README | Use the relevant documentation task | Outside package-consumer scope |
| Long generated API dump | Query relevant interfaces; recover needed omitted detail | Step 2; no mandatory whole-tree read |
| Useful badges or license/contribution links | Include when verified and useful; no section quota | Step 6 |

## Input budget and evidence scope

No inspection script is bundled: this skill chooses document content and checks,
using project tools and bounded queries. It defines no universal command-output or
README length cap. Default inspection selects headings, manifests, public entry
points, and first use; recover missing detail before conclusions. Independent-agent
large-input retrieval is not measured. SKILL.md body: 3,950 characters.

Format/catalog checks, installation checks, and package behavior establish different
claims. Neither a docs build nor a local tarball establishes registry availability.
Permanent tests for headings or prose matching were not added.

## Revision verification

Linux/WSL; Node.js 22.22.2; repository checks used Python 3.11 through uv.
Full `uv run --locked check.py` passed: 56 skill formats/catalogs, 131 existing
tests, and skills@1.7.0 discovery/selective-installation fixtures.

The actual new skill was installed alone into separate temporary Codex and Claude
projects through the bundled CLI. All three files matched source bytes; the MIT
license matched the repository license, NOTICE.md remained bundled, and the Claude
connection resolved to the shared directory. Actual selective installation through
skills@1.7.0 for Codex also passed with all three files matching. Temporary projects
were removed; personal installations were unchanged.

No new runtime helper or permanent tests were needed. Parent rule review covers the
decision cases above; independent README writing, consumer example selection,
large-input recovery, and measurable readability improvements remain unevaluated.
