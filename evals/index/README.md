# Index evaluation

## Task decision routes — 2026-10-16

Revision: uncommitted changes based on `bf9da24e30f73f0f23e3ce93ffe13216c478f3c2`.
Existing UI skill changes were preserved. The source-tree and installed indexes now
start with task/permission decisions from `lib/skill-routes.json`. Nine routes cover
all 65 distributed task skills. Categories remain the complete fallback; a task
without an authored route remains visible there. Partial installations omit empty
routes and unavailable choices. This is instruction selection, not a host-enforced
classifier or a mandatory execution pipeline.

Two fresh subagents received the same twelve requests and their respective index,
without expected answers or conversation history. Both selected all expected skills,
including specification versus implementation planning, read-only versus fixing
reviews, dependency assessment versus upgrade, compound guidance, and no-task input.
The candidate reported using decision routes without the category catalogs.
[Requests, expectations, artifact hashes, selections, and reported reads](task-routing.json)
record the selection rehearsal. Reads were agent-reported, not exported tool traces.

No accuracy improvement was observed: both variants matched 12/12. The mixed batch
reported eight candidate discovery files versus five baseline files; no token or
reading-cost saving is claimed. One agent per variant and shared context across
requests do not establish causal benefit, automatic activation, or underlying task
quality. Actual task execution and native Windows runtime remain untested here.

Executed checks in Linux/WSL, Node.js 26.10.0:

- Full `uv run --locked check.py`: 66 formats, 182 existing/new tests (one skipped),
  skills@1.7.0 discovery/installation, and packed CLI project/global lifecycles passed.
- Source and installed renderer tests cover all task names, partial route filtering,
  unknown-task fallback, exact paths, 100-choice route pagination, oversized navigation,
  malformed definitions, empty-route removal, and source output ownership/rollback.
- Skill-body reads remain prohibited during generation. Catalog and route pages stay
  within 2,500 characters/code units; root bodies stay within 4,000.
- Packed installation checks resolve route targets against the canonical index base
  and reject references to uninstalled skills, including through agent connections.
- An actual skills@1.7.0 installation of static index/spec-generator/plan copied every
  source byte, retained bundled route links, resolved installed sibling entrypoints,
  and excluded evaluation records. Creator checks passed for both index forms and
  the revised product-specification description.

Initial targeted checks exposed missing LF attributes for new route output and
bytecode writes from the new CLI helper import; both were fixed without weakening
read-only tests. The first full run also found an isolated scaffold fixture missing
the new helper; its copied module set was corrected before the passing full run.
These setup/output failures were retained as evidence, not counted as selection misses.
No live installation was updated and no package was published.

## CLI-generated installed index — 2026-10-16

The npm CLI now generates `index` from the installed shared sources in the selected
scope instead of shipping `skills/tooling/index/`. The source-tree index remains
available for repository navigation and skills CLI compatibility. Earlier agent
selection results below concern that static index and do not establish automatic
activation or routing accuracy for the generated template.

Runtime integration checks cover partial installation, two agents sharing a scope,
exact paths to existing skill instructions, removal and final cleanup in project
and global fixtures. Additional checks exercise replacing a previously owned
static index, rejecting user edits, rebuilding missing owned output, and preserving
the previous catalog after an injected replacement failure before retrying.
Unchanged updates perform no content or record writes. An uninstalled agent's
update must not succeed by refreshing another agent's index.

A 180-entry renderer fixture preserves every intention and exact path through
continuation pages, with no page exceeding 2,500 UTF-16 code units. Skill-body reads
are rejected by the fixture; long paths fail explicitly with bounded diagnostics.
The packed CLI verifies that the static index directory is absent, validates the
generated Agent Skill format, and checks that the catalog contains exactly its
selected installed task skills in both scopes.

The actual published 0.3.1 tarball was downloaded and integrity-verified. Two
temporary projects installed it with `survey` alone or `survey` plus the static
index. The new unrestricted update generated a complete index for the 65 installed
task skills in both projects, initialized missing discovery history, and preserved
user instructions. A repeated update preserved all file hashes and timestamps;
final removal restored the original project instructions.

A native Windows project fixture with Node 22.22.2 additionally passed partial
selection, automatic discovery of a newly added task, exact generated paths,
directory junctions, removal refresh, an unchanged update and final cleanup.
This was an isolated temporary project, not an update of the user's installations.
The full WSL verification passed 66 source skill formats, 172 tests (one
Windows-specific skip), skills CLI discovery/installation and packed CLI project
and global lifecycles. Native Windows global execution and new behavioral agent
selection trials were not run for this change. File generation does not enforce
that the host loads the index automatically. Publication remains separate.

## Current coverage

### Review-loop follow-up — 2026-10-16

Sequential review covered CLI selection/history, projected ownership and installed
paths, staging/rollback and confirmation checks, renderer/template output, npm
contents, migration fixtures, test expectations and consumer/maintainer docs.
The agreed scope remains a locally generated index of managed installations,
partial task selection, automatic discovery of new names and preserved exclusions.
Host-enforced loading, publication and modification of live installations remain
outside this change.

Six defects were reproduced and corrected:

- A rules-only record's generated index prevented initialization of the first
  actual partial task selection; unrestricted update then installed excluded tasks.
- Explicitly removing a newly added task before discovery did not acknowledge its
  name. Replacing history with the current bundle also forgot exclusions when
  names disappeared and returned. Removal now acknowledges the name, and discovery
  retains previously known names.
- Inherited `constructor` properties were mistaken for exact skill ownership in
  projected legacy state, producing a path to a removed agent copy. Ownership
  checks now use own properties throughout the new projection.
- An unselected indexed task could disappear while confirmation was open without
  aborting the batch. Referenced files are checked again before applying changes.
- A valid category such as `workflow-2` collided with another category's second
  page. Continuation names now use `.page-N`, distinct from valid category names.
- Resolving relative paths through a Windows junction could find only one of
  three shared installed tasks. The generated frontmatter now supplies a canonical
  `catalog-base`, and instructions explicitly resolve catalog paths against it.

Four new integration tests and the extended renderer fixture failed before their
fixes and pass afterward. The confirmation fixture first needed an explicit
project argument to avoid an earlier scope prompt; that setup failure is not
counted as a product reproduction. The native Windows alias probe independently
observed three canonical paths but only one path through the alias; the corrected
check reads the canonical base from the index through its junction and finds all
three installed tasks.

Final verification passed `uv run --locked check.py`: 66 source skill formats,
176 tests with one Windows-only skip, skills CLI discovery/installation and npm
package lifecycles in project/global scopes. Native Windows project checks passed
on Node 22.22.2. Both actual published-0.3.1 upgrade fixtures passed again, including
idempotence and user-prose preservation. No eligible finding remains in the
reviewed scope. Windows global/native-host behavioral selection trials and
publication were not performed.

- Revision/date: uncommitted working tree based on
  `4d972c2103595674f2d84d7552da861b9a66e4b0`; 2026-10-15.
- Fresh native Codex CLI executions now cover four implicit task selections in a
  temporary project with all 66 skills. No task prompt names its expected skill.
  Actual successful reads establish index-before-workflow in all four runs.
- Expected workflows were read in 4/4 runs: code-review, qa-checklist,
  spec-generator, and trace. Catalog-before-workflow order passed in 3/4; the
  first QA run opened its skill before the category page.
- Clarified the existing index order rule. A fresh replay of the unchanged QA
  prompt then read index, catalog, and qa-checklist in order. This is one observed
  recovery, not evidence that the wording causally guarantees compliance.
- [Native selection evidence](native-selection.json) preserves prompts, expected
  workflows, successful command events, instruction fingerprints, usage and limits.
  Raw JSONL traces are temporary command logs; their exact paths are in the record.
- Actual collaboration subagents additionally passed five blinded routing tasks
  and one same-task status follow-up. Independent filesystem observations confirm
  index/catalog/workflow access order. Missing-workflow fallback, second-page
  selection, and task/platform composition are now covered on these fixtures.
- Full Git-fix verification passed 66 skill formats, 164 tests (one Windows-only
  skip), and both installer checks. Final index wording passed format/catalog and
  packed installation checks; the package fixture includes 14 selected skills.
- Not established: all-task routing, changed-scope multi-turn reselection,
  repeated-trial accuracy, comparative benefit, or token/latency savings. Native
  executions used a read-only sandbox; preservation does not prove authorization
  judgment without enforcement. Global context was not completely isolated.

## Actual subagent selection — 2026-10-15

Five collaboration subagents started with `fork_turns=none`, the task request,
and an owned temporary project. Prompts named no expected task skill and supplied
no previous findings or desired answer. Project AGENTS.md required index-first
selection and limited applicable skills to project copies. Four projects contained
all 66 bundles; the missing-workflow project contained only index. This tests the
mandatory project flow, not activation without an index-reading rule.

| Request | Expected selection / condition | Observed result |
| --- | --- | --- |
| Review a change without editing | code-review rather than review-loop | Read index, workflow catalog, and code-review; found the contract defect; implementation and Git bytes preserved. |
| Prepare human QA without execution | qa-checklist rather than executing tests | Catalog preceded the full workflow; returned planned CLI setup/action/expected result and no execution claim. |
| Transfer current work inline | handoff on workflow page 2 | Read both workflow pages before handoff; preserved integer-only scope, deferred validation, and pending checks; no file or agent created. |
| Explain a source journey with no workflow installed | Verify local availability and proceed within scope | Acknowledged unavailable trace; used source citations and derived output without running, diagnosing, fixing, or installing. |
| Plan a mobile keyboard fix without implementation | plan plus mobile-web | Both relevant catalogs preceded the workflows; accessibility also applied to the explicit input/zoom requirements; device verification stayed pending. |

All five expected results passed parent semantic grading. The chosen scope did not
expand into implementation, installation, publication, or nested delegation.
SHA-256 manifests covering every project file, including Git internals where
present, matched before and after every run. A status follow-up to the original
review agent reported no new commands; continuous observation recorded only one
index-file open across the initial review and follow-up, consistent with reuse.
No changed-scope follow-up was tested.

Evidence is retained in [subagent-selection.json](subagent-selection.json), with
reproducible fixture files and expectations in
[subagent-cases.json](subagent-cases.json). Only the case's input files were supplied;
expectations remained outside each evaluated project. Outputs and command summaries
are normalized excerpts/reported records, not complete captured tool transcripts.

### Independent access observations

A temporary Linux inotify monitor watched 490 project directories for file-open,
access, and read-close events. Parent-controlled read probes verified all five
watches before task execution. It captured all 240 events with no omissions or
kernel overflow; it stopped before parent post-run fingerprint reads. The full
trace is [subagent-file-access.jsonl](subagent-file-access.jsonl).

Filesystem observations independently match the reported selection order. They
verify accesses, not full-text consumption or model attention. Events carry no
process identifier; each project had one evaluating agent, and the parent did not
read its skill/source files during observation except marked probe files. Parallel
catalog reads can occur in either order, and both preceded the selected workflows.

Unique accessed task-skill entrypoints were code-review, qa-checklist, handoff,
none for the missing-workflow case, and plan/mobile-web/accessibility for the
combined case. The agents did not read every installed skill body. Some inventories
still enumerated installed resource paths, and QA/fallback also consulted writing
catalogs; actual returned tokens and efficiency impact were not measured.

### Limits and checks

These are disposable copies with read-only task instructions, not separate enforced
subagent sandboxes. All agents share host permissions. Outside-project skill use
was prohibited by the task contract; global context was not proven absent.
Inherited model identity, usage counters, timing, billing, and comparative benefit
were unavailable. Review severity, exhaustive QA quality, and real mobile runtime
behavior were not graded. Passing five requests does not certify all-task routing.

Initial temporary Git setup encountered the existing Conventional Commit hook;
setup succeeded with a conforming message and normal hooks. Two task agents saw
interactive Bash job-control/fnm permission messages, while requested inspection
commands completed. These attempts were retained, not treated as routing defects.
Index runtime instructions/catalogs did not change during this evaluation.

## Windows checkout regression — 2026-10-15

The first release attempt at `040f19d62b4cb13b9685473e59a3c55f7fe5c75f`
passed Linux checks but failed all three Windows catalog-validation jobs:
[release run 38663009573](https://github.com/jinyongp/agentskills/actions/runs/38663009573).
Git converted generated LF files to CRLF on checkout. The read-only freshness check
compares exact bytes, so the otherwise current entrypoint and all six catalog pages
were incorrectly rejected. npm publication and GitHub release jobs were skipped.

Targeted Git attributes now keep only the generated index entrypoint and catalog
pages at LF, preserving exact-byte freshness checks and ordinary checkout policy
for other files. No validator bypass, regeneration in CI, or hook suppression was
introduced. The failed v0.3.0 tag remains unchanged; new source requires a new tag.

A new regression performs a real Git clone with `core.autocrlf=true`. Its control
file is CRLF; index freshness succeeds without rewriting any generated bytes.
Changing a generated intent still produces a stale result and leaves that change
untouched. Before the attributes were added, this test failed on all three generated
fixture files. Afterward, all ten index tests passed on Linux/WSL. Native Windows
validation and the final release workflow remain required before publication.

## Initial mechanical coverage — 2026-10-15

- Revision: uncommitted implementation based on `4d972c2103595674f2d84d7552da861b9a66e4b0`, evaluated 2026-10-15.
- Evidence: parent instruction review, nine mechanical generator/scaffold tests,
  repository regression checks, and actual packed CLI installation.
- Format validation passed for all 59 skills. The final full verification
  completed 156 tests with one platform-specific skip, plus discovery and package
  checks. Nine index tests and seven check-runner tests passed.
- Skills CLI fixture discovery/installation passed. The packed CLI installed
  `survey` and `index` for Codex and Claude in isolated project/global scopes,
  comparing every bundled file with its source and exercising update/removal.
- Not measured: independent agent selection, mandatory-read adherence, selection
  accuracy, elapsed time, or token savings compared with native skill discovery.
  No Windows execution was performed for this change.

## Cases

### Typical request

- Request: "Review these changes and report defects; do not edit source."
- Expected: read the workflow catalog, select installed `code-review`, and read
  its full instructions. Do not select `review-loop` solely because it reviews.
- Parent instruction review: the catalog distinguishes reporting from fixing;
  the index explicitly preserves the requested action and requires full instructions.
- Mechanical replay: distinct review and verification intents remain intact;
  generation does not read skill bodies, including large invalid UTF-8 bodies.
- Independent execution: original native review and actual subagent case-a now
  cover this request; see dated sections above.

### Adjacent request

- Request: "What is the status of the same task?"
- Expected: reuse already loaded instructions without rereading every catalog.
- Parent instruction review: new substantive tasks and changed scope trigger
  selection; follow-up responses can reuse loaded instructions.
- Independent execution: one same-agent status follow-up now covers reuse;
  changed-scope reselection and general multi-turn behavior remain untested.

### Missing skill or failed lookup

- Request: "Use a catalog skill that is not installed in this session."
- Expected: verify current availability and exact paths. Do not infer installation
  from the collection catalog or install a package without authorization.
- Parent instruction review: these boundaries are explicit. Subagent case-d now
  covers a catalogued but unavailable task workflow in a project-only skill context.
- Mechanical failures: missing/duplicate/removed catalog entries, oversized
  headings, unmanaged files, and output symlinks fail without replacing output.
  An injected write failure restores the index, catalogs, and scaffold state.

### Large catalog and stale output

- Fixture: 180 skills with long Unicode intent summaries.
- Observed: generated pages stay within 2,500 characters, all entries are recovered
  exactly once through exact continuation paths, and omission counts remain visible.
- Summary edits make validation fail without changing files; regeneration restores
  freshness. Shrinking a category removes obsolete generated pages.
- New skill preparation automatically includes its catalog entry in the index.
- Forgetting explicit generation is covered by normal full/format checks: they
  regenerate before validation. Seven subprocess runner tests verify ordering,
  generation failure propagation, and a read-only `--check-index` mode that
  rejects stale output without repairing it. CI invokes that read-only mode.
- A 10,000-character malformed catalog line produces failure output below 4,000
  characters. Both generation failure and `--check` preserve existing files.

## Input budget

- `SKILL.md` body: 2,706 characters at the evaluated revision.
- Generated pages: frontend 1,399; git 628; tooling 259; workflow 2,121;
  writing 1,053 characters. They contain all 59 collection entries.
- Only task-relevant category pages are requested. Larger categories provide page
  counts and skill-root-relative continuation paths; partial coverage is explicit.
- Skill bodies, diffs, logs, installation commands, and runtime scripts are absent
  from catalog pages. The generator is a maintainer tool, not an installed runtime
  dependency. It has bounded summary/failure output and a read-only check mode.
- Character limits are measured output budgets, not token-count measurements.

## Environment and checks

- Linux/WSL; Python 3.14.8; uv 0.12.22; Node.js 26.10.0; npm 11.19.1.
- Agent: Codex parent session; exact application build and model version unknown.
- `uv run scripts/generate_index.py --check`: passed.
- `uv run check.py` with a temporary npm cache: the final full run passed.
  An earlier smoke step stopped because the default npm cache was read-only.
- `uv run check.py validate --check-index`: passed without regeneration.
- `uv run check.py smoke` with a temporary npm cache: passed.
- `uv run check.py package`: passed with both skills in both agent/scope combinations.
- `uv run python -m unittest discover -s tests -p test_skill_index.py -v`: nine passed.
- `uv run python -m unittest discover -s tests -p test_new_skill.py -v`: twelve passed.
- `uv run python -m unittest discover -s tests -p test_check.py -v`: seven passed.
- `git diff --check`: passed.

The first repository run exposed an outdated CLI test fixture that copied the
validator without its new generator dependency. The fixture now copies both;
its focused rerun and the subsequent repository suite passed.

## Native selection execution — 2026-10-15

The setup copied each standalone skill into an owned temporary project's
`.agents/skills/`, using rules/base.md as its AGENTS.md. An incorrect `double`
implementation, independent multiplication contract, and small caller provided
real review/QA/trace inputs. Product requirements supplied explicit accepted limits.
Each request used a fresh `codex exec --json --ephemeral --sandbox read-only`
process, with user config ignored and no desired answer supplied to the model.

Parent scoring inspected successful command output, read order, final task scope,
and expected workflow use. It did not grade comprehensive review quality, severity
calibration, every proposed product default, or every QA input assumption. Code
review found the real mismatch; QA returned planned steps without executing tests;
the product draft preserved excluded features; trace cited the static source.
Project file fingerprints were unchanged across the later runs. The initial review
also retained its source bytes and Git change state.

The first startup failed because Codex's runtime needed writes outside the
workspace. Temporary sqlite/log settings alone did not resolve startup. Successful
executions required permitted CLI runtime writes while keeping task commands
read-only. No credentials were copied or published. CLI version: 0.160.0; exact
model identity was not emitted in the ephemeral JSONL traces.

Method reference: [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills).
The experiment uses task prompts and recorded tool actions rather than treating
an agent's statement that it used a skill as sufficient evidence. Native evals
are opt-in executions, separate from ordinary repository regression checks.
