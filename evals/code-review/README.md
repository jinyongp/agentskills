# code-review evaluation

## Current coverage

- **Focus:** Written review criteria, evidence boundaries, and proportional review workflow.
- **Evidence:** parent instruction/source review; the detailed earlier checks
  and fixtures are linked in the history.
- **Presentation revision — 2026-10-13:** uncommitted documentation working tree.
- **Change:** Behavior/standards, design, and changed-test criteria now have separate subitems.
- **Environment:** Linux/WSL, Node.js 26.10.0.
- **Checks:** full `uv run check.py` passed: 58 skill formats, 144 tests
  (one skipped), skills CLI discovery/selective installation, and packed
  project/global lifecycle checks. Internal link/anchor checks passed.

- **Standalone installation:** updated skill files matched source bytes in
  temporary Codex and Claude projects; creator validation and saved-record checks passed.
- **Limits:** no independent agent or reader study establishes the benefit of
  this presentation revision. Historical counts and passes retain their stated scope.

## Evidence and proportional workflow — 2026-10-13

Parent instruction review in Codex; model version not exposed. No independent
diagnosis, review or live PR operation was executed for these cases.

| Scenario | Expected decision |
| --- | --- |
| Lint passes but required behavior is absent | Review contract separately from mechanical standards |
| Behavior works but violates an applicable project standard | Report supported rule violation separately; avoid repeating already actionable tooling output |
| Two-adapter heuristic rejects a cleanup-owning single adapter | Assess actual responsibility/caller cost; no count-based finding |
| New outer tests omit a distinct case in old unit tests | Preserve meaningful coverage before recommending removal |

## Earlier records

[Dated reviews, executed fixtures, environments, and verification history](history.md).

## 2026-10-15 conditional workflow additions

- Revision: uncommitted changes based on 4d972c2103595674f2d84d7552da861b9a66e4b0.
- Evidence: parent instruction review and format/distribution regression checks.

Added conditional references for recorded-decision compliance and focused
boundary/failure/state/dependency checks. Parent review confirmed applicability,
accepted exceptions, evidence, and separation of explicit rule violations from
runtime defects. No unrestricted architecture audit or source edits follow from
this mode. The existing inspector was reused unchanged; no independent decision
review or fresh-agent selection was measured.

Full verification passed: 65 skills, 160 tests with one platform skip, and both
skills CLI and packed CLI checks. The package installed this skill's new references
for Codex/Claude in isolated project/global scopes and compared all files with
their sources. Older evidence above retains its original scope and date.
