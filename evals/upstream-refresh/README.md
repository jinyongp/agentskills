# Upstream review — 2026-10-22

**Behavioral follow-up:** [independent task execution](behavior-results.md) now
covers all three revised skills, including a fresh-session handoff receiver.
The source review and its original evidence limits below precede that follow-up.

**Result:** reviewed the 12 repositories named in distribution notices, Caveman,
and the pinned Agent Skills format/validator source. Adopted three improvements:
content-dependent style-recalculation probes, background-check result handling,
and dated handoff evidence. Source inspection and parent instruction review
establish written decisions, not agent effectiveness or measured performance gains.

**Target:** working tree based on `24ad0fd35c07049b8639c4c1547ed0b223a087e3`.
Sources were fetched on 2026-10-22 and pinned below rather than inferred from push
timestamps. Existing skill structure, scope, exceptions, and saved-record rules
remain the comparison contract. Installed skills and dependency versions are unchanged.

## Coverage and baselines

The inventory covered 69 entrypoints, the root notice, 50 skill notices, and tracked
source links. Twelve repositories provide adaptation, inspiration, or comparison
provenance. Independent original skills have no upstream to update. Caveman is an
additional structural comparison. Agent Skills is a separate format/validation
dependency. The skills CLI is an installation tool, outside this instruction refresh.

**P** means an exact revision recorded in a notice or dependency declaration.
**H** means the latest default-branch commit at or before the local attribution
commit. Five notices used moving links; their original observed revision cannot be
recovered exactly. H is a historical comparison, not the revision originally read.
**Fresh** means no prior immutable comparison was recorded. Unchanged below refers
to selected source paths, not the whole repository.

| Source | Baseline | Checked head | Selected scope and decision |
| --- | --- | --- | --- |
| [Emil Kowalski](https://github.com/emilkowalski/skills) | P `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` | [2d22863](https://github.com/emilkowalski/skills/commit/2d228630ba1446365f614a108cb8252f1feda202) | Existing referenced paths unchanged; new `skills/animation-performance/SKILL.md` supplies the content-growth probe. Adopt conditionally. |
| [Matt Pocock](https://github.com/mattpocock/skills) | P `49dd158d1076134a641b33efb035946536778336` | [5beb35b](https://github.com/mattpocock/skills/commit/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | Referenced engineering/writing paths unchanged; new wiki section in `skills/in-progress/chief-of-staff/SKILL.md` motivates dated evidence. Adopt without the wiki workflow. |
| [Ouroboros](https://github.com/Q00/ouroboros) | P `0df5b9893897dc28f1597235e586df60b15f319d` | [19e72c7](https://github.com/Q00/ouroboros/commit/19e72c7f7cfbaa7e6e7ce5d777f583b3cc9b5cd4) | Screened 21 changed entrypoints and removed `maintain`; read evidence, execution, requirements, and resume branches. Adopt dispatch/result distinction from `seed` and `qa`. Exclude runtime protocols. |
| [Anti-slop](https://github.com/miqdadbadjuber/anti-slop) | P `388cbe3b6c37d5175b9f460015bb092ef9e34894` | [439a2ef](https://github.com/miqdadbadjuber/anti-slop/commit/439a2ef5b9dd0ebe74e8113ff43f5928d0fe2a6a) | Read changed accessibility instructions and contrast helper patches. Unrounded classification already exists locally; helpers are not bundled. No additional rule. |
| [Attention-span](https://github.com/alexgreensh/attention-span) | P `2714c965e6be1fa2597510e66651e63bc67cb448` | [f4ae0de](https://github.com/alexgreensh/attention-span/commit/f4ae0de76ed3ab98fa9398a56f30bbfbaa146590) | Compared three output styles and moved `tldr`. Changes concern version comments and plugin packaging; no new instruction decision. Keep AGPL attribution. |
| [Karpathy guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | P `2c606141936f1eeef17fa3043a72095b4765b9c2` | [2c60614](https://github.com/multica-ai/andrej-karpathy-skills/commit/2c606141936f1eeef17fa3043a72095b4765b9c2) | Identical revision. No new material. |
| [Unlearn](https://github.com/unlearndev/skills) | P `4fd5a1f491e81a8800722f3f6d95cc992999e358` | [4fd5a1f](https://github.com/unlearndev/skills/commit/4fd5a1f491e81a8800722f3f6d95cc992999e358) | Identical revision; no new license declaration. Keep independently authored workflows; import no instructions/resources. |
| [Sentry](https://github.com/getsentry/skills) | H `7291c516520f8619737f9faa9eaab6cd5dfe74e5` | [f57ada2](https://github.com/getsentry/skills/commit/f57ada2d0b640406ea7e25b11d636c530e77c58b) | `skills/iterate-pr` and `skills/security-review` file/subdirectory identities match H. No new source guidance. |
| [Superpowers](https://github.com/obra/superpowers) | H `8ca22dba9a94f28898bbce59f2537ff4d87c747d` | [2ce8aa1](https://github.com/obra/superpowers/commit/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | Referenced `receiving-code-review` unchanged. Examined related fix-loop, cannot-verify, resume, and authoring guidance. Relevant decisions already covered locally; no fixed round count or mandatory delegation. |
| [pkuppens](https://github.com/pkuppens/skills) | H `fc39170d22a94696282304a4b7949495ad0c50a4` | [0e91fef](https://github.com/pkuppens/skills/commit/0e91fef55daa36097faa7c36c9072ea7ca4c331a) | `skills/readme-authoring/SKILL.md` and `reference.md` blob identities match H. No change. |
| [Awesome Copilot](https://github.com/github/awesome-copilot) | H `3a685010a7afdc0dbd4c83b7fbda6c316aa516e5` | [2d4b998](https://github.com/github/awesome-copilot/commit/2d4b998d2df28917074ee33db45c9601484c72ad) | `skills/create-readme/SKILL.md` blob identity matches H. No change. |
| [Trail of Bits](https://github.com/trailofbits/skills) | H `82fe8226252622fa807643bdca1710901198553a` | [f0dd11d](https://github.com/trailofbits/skills/commit/f0dd11d2b1da17a1ff8c403741fbe1f6bca0f871) | `plugins/supply-chain-risk-auditor` directory entries/subtree identities match H. No change; no CC BY-SA resources imported. |
| [Caveman](https://github.com/JuliusBrussee/caveman) | Fresh | [bad48a0](https://github.com/JuliusBrussee/caveman/commit/bad48a0e1df55e05e3f52249afa35ecc1909ee76) | Read `skills/caveman/SKILL.md`. Meaning/payload preservation agrees with existing authoring rules. No voice switch, sentence quota, hooks, or proxy imported. |
| [Agent Skills](https://github.com/agentskills/agentskills) | P `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | [69ef37e](https://github.com/agentskills/agentskills/commit/69ef37e9424c0a7ea9dd2293b559e43ec8176379) | Identical pinned format/validator source. No dependency update. |

Historical cutoffs in UTC: Sentry `2026-10-07T08:28:20Z`; Superpowers
`2026-10-07T08:28:28Z`; Trail of Bits `2026-10-07T08:31:31Z`; both README
sources `2026-10-07T12:30:36Z`. Reproduce H using GitHub's commits endpoint with
`sha=main`, `until=<cutoff>`, and `per_page=1`.

Ouroboros and Awesome Copilot comparisons reached GitHub's 300-file listing limit.
Missing repository detail was not treated as complete: Ouroboros skill changes were
cross-checked against both complete recursive trees (`truncated: false`); the selected
Copilot directory was compared directly by blob identity. Unrelated engine, plugin,
benchmark, and repository changes were not audited or executed. All identified source
repositories were accessible.

## Adoption decisions

- **Animation performance:** add a trace-led probe for inherited custom-property
  updates whose cost grows with descendants. Preserve legitimate inheritance and
  transform composition. [MDN inheritance](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties#inheritance_of_custom_properties)
  and [web.dev measurements](https://web.dev/blog/at-property-performance) support the
  mechanism, not a performance claim for a particular application. The original's
  blanket shorthand warning conflicts with the current
  [Motion performance guide](https://motion.dev/docs/performance), which documents
  accelerated independent transforms. Keep installed-version checks; do not import
  universal blur thresholds, equivalent-property claims, or guaranteed acceleration.
- **Verify:** require the actual check result behind a background/delegated receipt.
  Match identity and tested state; distinguish failed checks from unavailable worker
  results. Use host tools without mandatory agents, a new poller, auto-fixes, or an
  Ouroboros installation.
- **Handoff:** date changeable observations and identify their source/snapshot.
  Separate current decisions from historical observations. Reuse records and account
  for relevant uncommitted inputs without requiring a wiki, new artifact, full Git
  inventory, or permanent history of every claim.

The three affected notices pin new sources. Existing attribution remains intact;
handoff and verify MIT licenses additionally retain verified upstream copyrights.
Other provenance revisions remain their actual origins: checking a newer head is
not itself a reason to rewrite adaptation history.

## Decision cases

Parent instruction review in the current Codex session, 2026-10-22; exact model
version not reported. Expectations follow observable input facts and the existing
contract, not candidate wording. These are written-rule checks, not independent
agent executions or browser/device measurements.

| Input | Expected decision | Parent review |
| --- | --- | --- |
| A drag writes a parent custom property; cost grows with content without framework commits | Inspect style-recalculation evidence before selecting a change | Conditional web probe supports it |
| Descendants intentionally use the inherited value | Preserve consumers; no automatic non-inheritance fix | Consumer/inheritance conditions retained |
| Installed engine accelerates independent transforms; only source is available | Check engine/version; no slow-shorthand or measured-gain claim | Version and evidence limits retained |
| A queued check returns a worker prompt | Record pending evidence; retrieve matching result | Receipt is not a check result |
| A completed worker returns another revision's results | Do not reuse them for the requested target | Identity/state match required |
| Test output reports failure; another worker exits without output | Report failed test separately from unverified worker check | Failure and missing evidence distinguished |
| An old report predates a checkout/configuration change | Carry dated snapshot/lookup; compare current inputs before reuse | Handoff and reuse rules agree |
| Settled decision and evidence already exist in repository records | Link precise records; create no wiki or duplicate Git inventory | Packet and saved-record boundaries preserved |
| An unchanged caller's check still applies after unrelated prose edits | Reuse evidence without rerunning the whole suite | Existing unaffected-evidence exception retained |

## Validation

- Initial format/catalog validation: 69 skills passed; generated index unchanged.
- Final `uv run --locked check.py --check-index`: passed on Linux/WSL with Python
  3.15.0 and Node.js 26.10.0. Validated 69 skills; ran 184 tests with one Windows-only
  skip; passed skills@1.7.0 discovery/selective installation and packed CLI
  project/global lifecycle, bundled-byte, rule-preservation, and shim checks.
- Creator validation passed for all three affected skills. All 20 changed-document
  local links resolved. New upstream copyright notices and MIT permission terms
  matched the fetched sources. Metadata and saved-record paragraphs are unchanged;
  body sizes: animation-performance 3,783; handoff 3,973; verify 3,971 characters.
- Final skill snapshot: `674f2d70e11a5ac0ac43f0b6988678d8958f074703fc00bd6c51e3c8f2b9ff70`.
  This SHA-256 covers the 10 changed skill files, sorted by repository-relative path:
  hash each path's UTF-8 bytes, NUL, file bytes, and NUL in that order. Evaluation
  records are excluded so recording results does not change the tested snapshot.
- Source-review diff inspection and `git diff --check` passed. At that stage,
  fifteen task-owned files changed, including this record; no unrelated edits or
  deletions. The source-review check's
  raw log is local temporary evidence at `/tmp/agentskills-upstream-refresh-final.log`;
  the commands and results above remain available without that temporary file.
- Initial-review limits: no independent execution or performance capture had been
  performed at this stage. The linked follow-up adds that evidence for selected
  tasks. Comparative benefit remains unmeasured, and five original observed source
  revisions remain unknown beyond the historical comparisons above.
