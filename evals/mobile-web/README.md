# Mobile web evaluation

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Bottom action hidden by browser chrome | Reproduce owner and select viewport strategy | No universal height recipe |
| Keyboard covers an input/action | Verify visual viewport and existing avoidance | Dynamic units not assumed to solve keyboards |
| Edge-to-edge sheet under notch | Check relevant viewport configuration and insets | No duplicated compensation |
| Tap leaves hover effect stuck | Preserve hybrid input and required non-hover access | Capability-based behavior |
| Button fires on touch-down by accident | Separate acknowledgement from activation | Cancellation semantics retained |
| Nested sheet blocks page scroll | Inspect boundary and gesture ownership | No global scroll/zoom disabling |
| Request removes tap highlight | Keep replacement feedback and visible focus | Feedback remains usable |
| Only desktop emulation available | Report precise platform gaps | No physical-device claim |
| Existing keyboard handler works | Reuse instead of layering offsets | Scope stays narrow |
| Many routes | Inspect selected surface and disclose omissions | No comprehensive claim from sample |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Parent review assesses written decisions, not independent execution. No mobile
browser, keyboard, safe-area, gesture, or display-mode behavior was exercised here.
Automatic invocation and real-project fixes remain unmeasured. No generic helper
is bundled because platform reproduction depends on project browser/device tools.
Tool output budgets and large-project recovery were not measured. No tests assert
incidental CSS, metadata, or instruction wording.

Body: 3,704 characters. Full locked checks passed: 41 skills, 76 tests, CLI fixtures.
Creator validation, exact four-file selective installation, local links, saved-record
fragment, and upstream MIT comparison passed.
