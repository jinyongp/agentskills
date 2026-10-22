# Inventory drag performance

Changed only this disposable project's `index.html`: use direct transforms for
the panel and meter, retain `rotate(-2deg)`, and remove the unused synchronous
last-item geometry read. No items were removed or virtualized. No dependencies,
transitions, layer-promotion hints, or frameworks were added.

## Conditions and reproduction

- Served at `http://127.0.0.1:8769/index.html`; no build step.
- Project-host DevTools browser: HeadlessChrome/155.0.0.0, Linux x86_64,
  1350 by 2053 CSS pixels, DPR 1, CPU 1x, no network throttle.
- Own isolated tab: DevTools page 3, context `forward-animation`.
- An idle 30-frame sample had intervals 16.6–16.8 ms, approximately 60 Hz.
- Normal motion, normal speed. Same host, browser, viewport, inventory, and
  instrumented connection before and after. Background host activity was not controlled.
- Warm-up: `await demo.run({count:4000,frames:30})`.
- Three repetitions, each with `await demo.run({count:200,frames:90})` then
  `await demo.run({count:4000,frames:90})`.
- Large-inventory warm-up: `await demo.run({count:12000,frames:30})`, then three
  repetitions of `await demo.run({count:12000,frames:90})`.
- Each run rebuilds the inventory and waits for animation frames before collecting
  90 synchronous-work samples and 89 frame intervals. Updates cycle 0–280 px.
- Baseline captured before the edit. Reloaded without cache before changed runs.
- Performance traces were separate from the repeated untraced measurements.

## Repeated untraced results

Ranges below show the three runs, in milliseconds. A reported 0 ms work median
means below the timer's observed 0.1 ms granularity, not zero browser work.

| Items | Version | Work p50 | Work p95 | Work maximum | Interval maximum | Intervals >25 ms per run |
| --- | --- | --- | --- | --- | --- | --- |
| 200 | Baseline | 0.4–0.5 | 0.7–0.8 | 0.7–1.3 | 16.8 | 0, 0, 0 |
| 200 | Changed | <0.1 | 0.1 | 0.1–0.2 | 16.8 | 0, 0, 0 |
| 4,000 | Baseline | 5.1–5.3 | 5.6–6.1 | 5.8–7.8 | 16.8 | 0, 0, 0 |
| 4,000 | Changed | <0.1 | 0.1 | 0.2 | 16.8 | 0, 0, 0 |
| 12,000 | Baseline | 14.8–15.3 | 15.7–17.2 | 16.1–21.0 | 16.8–33.4 | 3, 0, 1 |
| 12,000 | Changed | <0.1 | 0.1 | 0.1–0.2 | 16.8 | 0, 0, 0 |

Interval p50 was approximately 16.7 ms throughout. Baseline 12,000-item p95
interval was 16.7–16.8 ms; a few longer intervals therefore remain visible in
the maxima and raw samples. A 25 ms threshold identifies approximately doubled
frames at this observed cadence, not a universal refresh-rate budget.

## Trace attribution

Trace workload: mark `inventory-{baseline|changed}-start`, run
`await demo.run({count:4000,frames:90})`, then mark the corresponding `-end`.
Select only the marker's renderer process and thread. Exclude inventory setup
through the first animation-frame callback; inspect the following 90 callbacks.
Other processes, including DevTools UI activity, are excluded from these totals.

| Selected trace metric | Baseline | Changed |
| --- | --- | --- |
| Absolute timestamp range (microseconds) | 46451337557–46452814978 | 46549193273–46550655007 |
| Full trace events | 46,813 | 42,152 |
| Selected events | 7,826 | 9,269 |
| Events outside selection | 38,987 | 32,883 |
| Style updates | 89 | 88 |
| Elements recalculated per style update | 4,005 | 2 |
| Style update median / p95 / maximum (ms) | 5.168 / 5.576 / 7.311 | 0.0395 / 0.075 / 0.140 |
| Selected style duration total (ms) | 468.886 | 3.854 |
| Frame callback median / p95 / maximum (ms) | 5.446 / 5.877 / 7.907 | 0.1705 / 0.280 / 0.464 |
| Selected layout total (ms) | 9.071 | 14.952 |
| Selected paint total (ms) | 64.020 | 69.897 |

The baseline largest style event begins at 46452045947 microseconds. Its stack
points to `setTravel` at original index.html line 49, the descendant
`getBoundingClientRect()` read, called from `run` line 83. It recalculates 4,005
elements after `--travel` changes on the panel. The panel variable was inherited
through the inventory although only the panel and meter consumed it. Direct
transforms remove that descendant invalidation; eliminating the unused geometry
read also avoids forcing synchronous style/layout in the input callback.

The changed trace still contains layout and paint for status text and the visible
surface. Their totals did not improve in this sample. Direct transforms do not
establish a compositor-only path. Inventory creation also remains proportional
to item count. The robust gain is removal of inventory-sized style work; the
untraced synchronous measurement alone would omit deferred rendering work.

Summarize the retained traces with:

```sh
python3 diagnostics/summarize_trace.py /home/jinyongp/.config/loki/data/browser/results/42cea9d903dc42f43ac1b3dac2f1c48f/devtools/session-991cded237f2edb5f004799c4ab95e0c/baseline-trace.json.gz baseline
python3 diagnostics/summarize_trace.py /home/jinyongp/.config/loki/data/browser/results/42cea9d903dc42f43ac1b3dac2f1c48f/devtools/session-991cded237f2edb5f004799c4ab95e0c/changed-trace.json.gz changed
```

The helper emits aggregate counts plus one largest event per selected category;
it reports excluded event counts instead of dumping or silently truncating traces.

## Interaction validation

Own Playwright tab 1, 1280 by 720 viewport: 16 assertions passed using real mouse
and keyboard actions. Verified clamping at 0/280, 140 px midpoint, -2 degree
rotation, meter scale/status/ARIA synchronization, both arrow keys, dragging,
direction reversal, release, focus retention, loss of pointer capture, recovery
after interruption, and reduced-motion keyboard and drag behavior. Pointercancel
was synthetically dispatched during a real held drag; capture loss used the real
`releasePointerCapture(1)` API. All 12,000 buttons remained present, and Item 12000
was scrolled into view and focused.

An initial diagnostic script ended with `ReferenceError: window is not defined`
while trying to save results from the automation context. The corrected script
used `page.evaluate` and completed all 16 assertions. The sole page console error
was the existing `/favicon.ico` HTTP 404. No browser capability was unavailable.

## Raw artifacts

DevTools output directory:
`/home/jinyongp/.config/loki/data/browser/results/42cea9d903dc42f43ac1b3dac2f1c48f/devtools/session-991cded237f2edb5f004799c4ab95e0c/`

- `baseline-runs.json`, `baseline-large-runs.json`
- `changed-runs.json`, `changed-large-runs.json`
- `baseline-trace.json.gz`, `changed-trace.json.gz`

Interaction results:
`/home/jinyongp/.config/loki/data/browser/results/42cea9d903dc42f43ac1b3dac2f1c48f/playwright/session-a3208113ee7a737a3ce9195920cb65ce/interaction-checks.json`

## Limits and file accounting

This is a headless desktop diagnostic workload with three repetitions per size,
not physical touch-device responsiveness or cross-browser evidence. Frame
presentation and input-to-display latency were not separately measured. The
short baseline includes occasional 33 ms frames at 12,000 items; the changed runs
observed none, which does not guarantee their absence on all hardware.

Modified existing file: `index.html`. Added diagnostic files:
`diagnostics/summary.md` and `diagnostics/summarize_trace.py`. `README.md` is unchanged.
The directory is not a Git worktree: `git status --short` returned
`fatal: not a git repository (or any of the parent directories): .git`.
Consequently repository status/diff checks are unavailable. No repository, package
installation, commit, publication, or live-service changes were performed.
