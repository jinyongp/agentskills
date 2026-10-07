# README evaluation

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
