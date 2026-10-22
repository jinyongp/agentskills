# Independent task execution — 2026-10-22

## Scope and controls

The user requested parallel independent execution of the three revised skills,
supported corrections, and a commit. Three evaluators started in parallel with
`fork_turns: none`; a fourth fresh agent then resumed the writer's handoff.
No evaluator received the parent conversation, upstream conclusions, proposed
diagnoses, or [predeclared expectations](behavior-expectations.md).

Each agent received its named skill path, realistic request, disposable project,
and permitted effects. Evaluators could read only the named skill/resources and
their project outside the supplied packet. The animation task authorized a scoped
fix; verification and handoff tasks did not authorize source changes. Agents used
the parent model configuration without an override; exact model version and usage
counters were not exposed. This tests explicit invocation, not automatic discovery.
Reference-read coverage is agent-reported; task outputs were checked against raw
artifacts. Full per-call tool transcripts were not exported into this record.

The evaluated skill snapshot is
`674f2d70e11a5ac0ac43f0b6988678d8958f074703fc00bd6c51e3c8f2b9ff70`
on repository base `24ad0fd35c07049b8639c4c1547ed0b223a087e3`, using the manifest
method recorded in the [source review](README.md). Fixtures and outputs below are
independent synthetic data, not examples taken from the maintainer's repositories.

## Execution ledger

| Skill/task | Independent agent | Work performed | Grading status |
| --- | --- | --- | --- |
| Animation performance | `/root/forward_animation` | Browser investigation, authorized fixture fix, matched measurements, preservation checks | Pass |
| Verify | `/root/forward_verify` | Current release-readiness assessment through local background-check adapter | Pass |
| Handoff preparation | `/root/forward_handoff_writer` | Inline packet from project and session facts | Pass |
| Handoff resume | `/root/forward_handoff_receiver` | Fresh-session verification using only packet, project, and skill | Pass |

All original fixture inputs are preserved in [behavior-fixtures](behavior-fixtures/README.md).
Recorded temporary paths identify the original execution; durable artifacts are
linked below so understanding the results does not depend on those paths surviving.

## Verify: executed checks and lifecycle recovery

The agent read the selected skill and relevant evidence/cadence references, assessed
the current price calculator, and obtained results for fingerprint
`91faafbc9126577d6e677537c0d6c9db2c7fe94a435033ce142247bac9bd6b09`.

- **Unit failure:** a real Python unittest process ran three tests; the half-cent
  case returned 10 rather than required 11, exit 1. The remaining two tests passed.
- **Configuration pass:** the executed configuration check returned exit 0.
- **Contract blocked:** the adapter failed before executing the required external
  check because its prerequisite was unavailable. The agent kept this separate
  from the observed unit failure and returned not release-ready.
- **Stale evidence rejected:** the seeded earlier PASS targeted `prior-checkout-0`.
- **Transport recovery:** detached fixture workers did not survive the execution
  host's command cleanup. The agent inspected worker liveness, resumed the existing
  job IDs through the adapter's worker entrypoint, and retrieved actual outputs.
  The [dispatch audit](behavior-artifacts/verify/requests.log) records exactly one
  dispatch per required check; there were no replacement jobs merely for delay.

The parent parsed the raw results and checked their requested/executed fingerprints,
exit codes, and outputs. SHA-256 comparison confirmed all five project input files
remained unchanged. This is successful execution under a controlled local transport,
not testing of an actual partner service or a production CI provider.

Evidence: [agent response](behavior-artifacts/verify/agent-response.md),
[unit result](behavior-artifacts/verify/job-a4f4e7e23c.result.json),
[configuration result](behavior-artifacts/verify/job-657500f8e9.result.json),
[contract worker status](behavior-artifacts/verify/job-e57de6a02d.json).

## Handoff: preparation and fresh-session resume

The writer received session-only facts about intentional retention 14, accepted
offline scope, the unresolved temporary restriction on deletion, and verification
as the next authorized action. It inspected the project and returned an inline
packet with exact lookups, the historical evidence source, and current constraints.
It did not run tests or edit files during preparation. Its source-based observation
about the fixed retention constant was transferred as an observation, not a test pass.

The fresh receiver read that packet and project state, ran the focused tests, and
reported not ready: three tests executed, one failed because the implementation
ignored the intentional 14-day setting. It identified the tested revision and dirty
configuration fingerprint, preserved the deletion restriction and operator note,
and made no unauthorized fix or rollback. An interactive-shell initialization warning
did not prevent execution of the test command.

The parent independently reran the focused check and confirmed the reported failure.
All seven project input/evidence/note file hashes remained unchanged. Git inspection
still showed the intentional config edit and original untracked evidence/operator
note, plus permitted Python caches. No staged changes or authored project edits.

Evidence: [writer packet](behavior-artifacts/handoff/handoff-packet.md),
[receiver response](behavior-artifacts/handoff/receiver-response.md),
[original three-test pass](behavior-artifacts/handoff/handoff-baseline.log),
[parent failure confirmation](behavior-artifacts/handoff/parent-handoff-confirmation.log).

## Animation performance

The agent captured real browser baselines, changed the disposable drawer, and
repeated the same workloads. HeadlessChrome 155 on Linux used a 1350×2053 CSS-pixel
viewport, DPR 1, CPU 1x, no network throttle, normal speed, and an observed cadence
near 60 Hz. It warmed up and ran three 90-frame repetitions at 200, 4,000, and
12,000 items. Traces were captured separately from untraced timing runs.

| Observed metric | Baseline | Candidate |
| --- | --- | --- |
| 4,000 items: synchronous work p95 across three runs | 5.6–6.1 ms | 0.1 ms |
| 12,000 items: synchronous work p95 across three runs | 15.7–17.2 ms | 0.1 ms |
| 12,000 items: maximum frame interval | 16.8–33.4 ms | 16.8 ms |
| Selected 4,000-item trace: elements recalculated/update | 4,005 | 2 |
| Selected trace: style-update p95 | 5.576 ms | 0.075 ms |

The trace ties inherited property updates and a synchronous geometry read to the
inventory-sized style work. The agent used direct transforms for the panel/meter,
retained rotation, removed the unused read, and preserved all items. It did not
claim deferred browser work disappeared: selected layout and paint totals did not
improve, and median frame intervals remained approximately 16.7 ms. The measured
gain concerns the demonstrated style work; input-to-display latency was not measured.

Sixteen browser interaction assertions passed, including real mouse and keyboard
actions, clamps/reversal, focus, meter/status/ARIA synchronization, rotation,
interruption, reduced motion, and reaching Item 12000. Pointer cancellation was
synthetic during a real drag. The agent reported and recovered from an initial
diagnostic save attempt using `window` outside page context; that attempt is not
counted as a successful assertion run.

The parent inspected the candidate source, recomputed trace summaries, read every
timing run, and independently checked rendered matrices, clamps, rotation, meter,
status/ARIA, keyboard updates, and the 12,000-item count. The independent parent
check passed. The standalone fixture has no Git metadata; source/whitespace checks
and changed-file accounting were used rather than claiming a clean Git worktree.

Evidence: [agent summary](behavior-artifacts/animation/summary.md),
[candidate source](behavior-artifacts/animation/changed-index.html),
[baseline timing](behavior-artifacts/animation/baseline-runs.json),
[large baseline timing](behavior-artifacts/animation/baseline-large-runs.json),
[candidate timing](behavior-artifacts/animation/changed-runs.json),
[large candidate timing](behavior-artifacts/animation/changed-large-runs.json),
[interaction results](behavior-artifacts/animation/interaction-checks.json),
[baseline trace summary](behavior-artifacts/animation/baseline-trace-summary.jsonl),
[candidate trace summary](behavior-artifacts/animation/changed-trace-summary.jsonl),
and [parent preservation check](behavior-artifacts/animation/parent-preservation-check.json).

Raw compressed traces stay outside Git in the engine-owned directory recorded in
the agent summary (approximately 6 MB each). Their SHA-256 values are:

- Baseline: `577bfd28ac2901c5976242c8101c133364f531e69a5db942d7af71b7fdfd5e3f`.
- Candidate: `9e2b3d735a04cca566cc20535fd589902a3417b7b87c9848b92f1a42612ed755`.

The committed bounded summaries retain exact selected ranges, event counts,
exclusions, and relevant stacks. No physical-device, native, cross-browser, or
presentation-latency conclusion follows from this headless desktop workload.

## Conclusions and limits

All four independent task executions passed their applicable predeclared outcomes.
No supported skill defect was found, so no additional instruction correction or
fresh-agent retest was necessary. The deliberate fixture defects remain in recorded
inputs; correct assessment is a passing evaluator outcome. Only the animation
task authorized a fix, and its fixed artifact is recorded separately.

The three upstream reinforcements and their existing scope/exception boundaries
remain unchanged from the evaluated skill snapshot.

## Final repository checks

`uv run --locked check.py --check-index` passed after the behavioral records and
fixtures were added: 69 skill formats, 184 tests with one Windows-only skip,
skills@1.7.0 discovery/selective installation, and packed CLI project/global
lifecycle, bundled-byte, rule-preservation, and shim checks. The local full log is
`/tmp/agentskills-upstream-behavior-final.log`.

All 57 local Markdown links in the changed documents resolved at inspection; all
evaluation JSON/JSONL parsed. `git diff --check` passed. The 55 task-owned files
include the three skill changes, attribution/licenses, source research, declared
expectations, disposable fixture inputs, and actual result artifacts. No unrelated
work or deletions were introduced. The large raw traces remain outside Git.

This provides independent execution evidence for selected tasks. It does not prove
comparative improvement, broad reliability, automatic skill selection, token/cost
savings, or behavior on untested devices and providers. No with/without-skill control
run was performed. Source-baseline uncertainty for five upstream references remains
as described in the initial review.
