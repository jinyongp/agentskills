# Workflow sequence replay

Executed on 2026-10-07 by the parent Codex session; model version not recorded.
This is a reproducible parent-authored trajectory, not an independent agent test.
The runner invokes Python processes, not an LLM or skill selector. It replays seeded
mistakes and corrections; success does not establish autonomous planning or discovery.

## Contract and observed trajectory

One owned project contains a CLI, arithmetic producer, configurable shipping rule,
plan, and handoff. Receipt export is deliberately manual. Expectations come from
the written fixture contract and concrete arithmetic/boundary examples.

| Stage | Observed result | Decision illustrated |
| --- | --- | --- |
| Plan and accepted scope | Required CLI/arithmetic/shipping behavior recorded; manual receipts retained | Completion follows the accepted contract |
| First A check, then B | A's selected input exits 0; B's distinct arithmetic case exits 1 | A narrow pass leaves B and C pending |
| Faulty B correction | Producer check exits 0 after export rename; unchanged CLI exits 1 | Reopen affected callers even when their files did not change |
| Compatible B correction | Required export restored with correct arithmetic; A and B exit 0 | Correct the existing contract without introducing a compatibility layer |
| Configuration change | Fee changes 5 to 8; old expected-fee check exits 1, current-fee check exits 0 | An earlier pass does not establish current configuration behavior |
| Handoff and fresh-process resume | Packet preserves manual receipts and links prior logs; pending inclusive-boundary check exits 1 | Resume recovers intent while continuing pending review |
| C correction and final checks | Boundary, current fee, CLI, and arithmetic checks exit 0 | Complete requested areas while preserving unaffected choices |

The run executed 14 subprocess checks, including four expected failing negative
controls. It preserved the CLI source, accepted contract, unrelated draft, manual
receipt scope, and current fee configuration. No payment integration, auto-export,
new dependency, or production operation was added.

## Reproduce

Python 3.11+ is sufficient. The recorded run used Python 3.11.17 through uv.
From the repository root, choose a new output directory:

```bash
uv run --locked python evals/workflow-sequence/replay.py --output /tmp/workflow-replay-01
```

The runner refuses existing output directories, saves the owned project, individual
command logs, and `results.json`, and exits nonzero when a replay expectation fails.
Each check has a 30-second timeout. It is optional evidence replay, not a CI suite or
a required test for every edit. Runtime logs stay outside default agent input.

Recorded evidence: `/tmp/agentskills-workflow-sequence-20261007-c/`. This temporary
path is not a durable installed dependency; the replay recreates the evidence.
Source/configuration fingerprints accompany command results. They cover the selected
fixture inputs, not every environment variable or external dependency.

An attempted rerun into existing evidence exited nonzero and preserved the report
byte-for-byte. The final replay passed after fixture refinements; earlier runs are
kept separately. Full repository checks passed for 50 skills, 76 existing tests,
and CLI fixtures; both revised skills installed individually with exact bundled
files, including the new evidence reference. Creator validation passed as well.

## Supported changes and limits

The trajectory motivates explicit review invalidation for unchanged callers and
a conditional verification reference describing tested code, configuration, and
execution conditions. Matching unaffected evidence can still be reused.

The handoff check uses a fresh Python process reading authored files; it does not
measure a fresh agent's memory, interpretation, or behavior. Automatic skill selection,
review-only versus fix activation, adversarial prompts, independent defect discovery,
parallel reviewers, actual agent sessions, and causal with/without-skill benefit remain
unmeasured. Other branches of the instructions retain their prior evidence limits.
