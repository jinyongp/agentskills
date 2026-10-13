# Authoring policy verification history

These records describe the stated revisions and environments, not the current
checkout. Dates, limitations, and original observations are retained below.

## Authoring policy verification

### Agent instruction writing — 2026-10-13

#### Revision verification

Added domain-modeling and retro; reinforced plan, queue, prototype, write, rewrite,
dev-docs, debug, code-review and git-pr. Authoring guidance lives in CONTRIBUTING.md.
All documentation and evaluation cases are English. Matt Pocock adaptations pin
commit `49dd158d1076134a641b33efb035946536778336`; standalone skills retain their
own upstream license and attribution outside runtime instructions. The maintainer
guide's attribution/license is in the root NOTICE.md.

Actual `uv run --locked check.py` passed: 58 skill formats/catalogs, 133 tests,
and skills@1.7.0 fixture discovery/selective installation. Local runtime-reference
links, saved-record fragments, copyright notices and body limits passed for all
11 added/changed skills. Bodies range from 3,159 to 3,982 characters.

An actual npm tarball was installed through npx into an isolated temporary project
for Codex and Claude. All files of the 11 selected skills matched source bytes;
Codex read the shared project directory and Claude linked to the same content.
Tarball checks found all selected resources and no Python caches. Actual
skills@1.7.0 installation of domain-modeling, retro and prototype also matched
every source file and installed no unselected skills. The first package replay
used an incorrect expected Codex project path; the harness was corrected to the
declared `.agents/skills` destination and rerun successfully, without source edits.

These checks establish format and distribution, not independent agent behavior
or comparative skill benefit. Decision cases are parent instruction reviews.
No package publication, personal installation, or live tracker/PR operation was run.

#### Authoring decisions

Parent instruction review in Codex; model version not exposed. The authoring
guide now defines reading conditions, co-located decisions, observable completion,
repository lookups and evidence-based pruning. No independent authoring run or
causal improvement was measured.

| Case | Expected decision |
| --- | --- |
| UI-only reference and logic-only reference | Load the branch relevant to the actual question, not both by default |
| Rule and its exception appear in distant sections | Co-locate them and state their resulting action |
| Current command/version is cheap to retrieve | Point to its source instead of maintaining a prompt copy |
| A standalone skill needs a safety boundary | Retain it locally even when maintainers share a canonical fragment |
| One session did not exercise a constraint | Non-use does not establish redundancy; evaluate relevant cases before pruning |
| A coined term supposedly improves agent behavior | Treat the benefit as unverified until realistic execution supports it |

### Research, security and CI additions — 2026-10-07

Attribution layout was corrected afterward: upstream provenance and license notices
now live in the affected skills' NOTICE.md files, including the pre-existing Git
commit reference. Task references retain their useful technical source links.
The existing implement notice was extended without replacing earlier attribution.
Format/catalog validation and actual tarball/selected-skill installation passed;
the complete resource comparisons included the new notice files.

Added research, security-review and ci-fix; reinforced review-loop feedback handling,
plan/implement structural decisions, and dependency-update supply-chain checks.
Guidance is independently written with source links; upstream scripts and
OWASP-derived reference text are not bundled. Existing original MIT log-runner code
is included inside ci-fix so individual installation retains its runtime.

Full verification passed: 55 skill formats/catalog entries and 131 tests, including
the bounded log execution suite applied to the CI helper. Actual npm tarball help
and full-catalog installation passed with all bundled resources compared byte-for-byte.
Actual skills@1.7.0 selective installation of the three new skills and standalone
execution of the installed CI helper passed. Creator validation of all three skills
and local Markdown-link checks for all seven changed skills passed.

Body lengths excluding frontmatter: research 2,964; security-review 3,229;
ci-fix 3,668; review-loop 3,977; plan 3,534; implement 3,967;
dependency-update 3,988 characters. New references load only for stated conditions.

Decision cases are parent instruction reviews. Mechanical results do not establish
independent agent selection, security coverage, live CI repair, research synthesis
quality, or comparative skill benefit. No npm publication or personal installation
was performed for these additions.

See [parent task execution and replay](../task-execution/README.md) for five executed
local tasks, fixture contracts, actual package/runtime failures, measurements,
database recovery and an API consumer break. This supplements instruction review
and packaging checks; it does not measure independent selection or causal skill benefit.

Five additions on 2026-10-06 bring the collection to 49 skills: dev-docs,
dependency-update, optimize, db-migrate, and api-design. Their evaluation records
separate parent decision-rule review from mechanical verification and the scoped
SQLite rehearsal. Full verification passed with 76 existing tests. Actual installation
of these five names in one command and wildcard installation of all 49 skills with
skills@1.7.0 passed; all bundled files matched byte-for-byte, with no extra selections.

See the [repository-wide context review](../context-review/README.md) for the 44-skill snapshot,
their decision boundaries, corrections, mechanical evidence, and unmeasured behavior.

See [saved-records verification](../saved-records/README.md) for the shared artifact
location, individual installation, generation, and file preservation checks.

On 2026-10-03, the Git skills were revised to start with summaries and use input budgets.
Repository limits are 300 characters for descriptions and 4,000 for SKILL.md bodies,
separate from the official format limits.
All 40 tests in `uv run check.py test` passed, covering accepted boundary values,
rejected overflows, preservation on generation failure, bounded inspection output,
and information recovery. These results do not measure automatic skill selection
or independent agent judgment.

The five Git skill bodies decreased from 23,042 characters at initial commit `6669a64`
to 12,429 characters, about 46%. This comparison excludes frontmatter and conditional references.
The final `uv run --locked check.py`, individual installation and execution of the inspection
helper, local documentation links, and per-skill MIT notices all passed verification.
