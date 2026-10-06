# Animate evaluation

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Add drag-to-dismiss to a web sheet | Handle cancellation, nested scroll, settling, and explicit dismissal | Web gestures are included |
| Animate a route while another navigation interrupts it | Protect new state from stale exit completion and preserve focus | State ownership retained |
| A mobile keyboard covers an animated form footer | Verify actual viewport access and preserve the action | Web keyboard behavior included |
| Keep an existing CSS transition that works | Reuse it rather than install a motion library | Tool choice follows project |
| Add a playful transition with a justified long duration | Tune contextually instead of failing a universal threshold | Taste separated from defects |
| Reduced-motion preference changes during use | Preserve outcome through a suitable alternative | Preference and functional outcome retained |
| No browser access is available | Report source-only verification | No observed-motion claim |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decisions through parent review, not independent agent execution.
Automatic selection and real-project motion quality remain unmeasured. No browser,
device, or frame-rate behavior was exercised here. No tests pin instruction wording.

No inspection script is needed for selected implementation. Project tooling supplies
bounded detail; large-project inspection and runtime judgments were not measured.

Body: 3,359 characters. Full verification passed: 30 skills, 67 existing tests,
and CLI fixtures. Creator validation, actual selective installation of all five
files byte-for-byte, upstream MIT comparison, and local links passed.
