# Responsive evaluation

## Cases

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Repair a long translated label overflowing a flex row | Find intrinsic sizing and preserve required text | Actual source of overflow drives the fix |
| Keep an existing two-state layout that works | Retain its breakpoints and layout states | No mandatory third state |
| Make a wide data table usable on a phone | Preserve meaningful two-dimensional reading with localized access | Intentional scrolling distinguished from page leakage |
| A sticky footer covers the focused field under a mobile keyboard | Reproduce relevant device behavior and restore access | Desktop resizing is insufficient evidence |
| Audit one page among hundreds | Select relevant components and limit conclusions | Omitted pages remain explicit |
| A 320px screenshot looks good but the action is hover-only | Exercise the action with supported input methods | Static appearance is not completion |
| A reviewed layout uses fixed pixel values without failure | Keep working implementation | CSS literals alone do not establish defects |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decision rules through parent review, not independent agent
execution. Automatic selection, real-project effectiveness, and large-input
recovery remain unmeasured. No runtime helper or dependency is bundled; inspection
ceilings depend on project tools. No tests that pin instruction text were added.

Body: 3,499 characters excluding frontmatter. Full verification passed: 28 skills,
67 existing tests, and CLI fixture checks. Creator validation passed. Actual
selective installation with `skills@1.7.0` copied all three files byte-for-byte
without another skill. Upstream MIT license comparison and local links passed.
No browser or mobile layout behavior was independently evaluated.
