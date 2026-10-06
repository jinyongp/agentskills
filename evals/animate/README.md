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
| CSS exit is cancelled or reduced to zero duration | Reach the correct semantic state without depending on an event | Lifecycle fallback is explicit |
| Project uses an older Framer Motion version | Follow installed APIs and reuse its presence owner | Conditional reference preserves tool choice |
| Scroll reveal is unavailable or repeatedly retriggered | Keep content reachable and choose replay deliberately | Visibility and progress-linked effects are distinguished |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decisions through parent review, not independent agent execution.
Automatic selection and real-project motion quality remain unmeasured. No browser,
device, or frame-rate behavior was exercised here. No tests pin instruction wording.

No inspection script is needed for selected implementation. Project tooling supplies
bounded detail; large-project inspection and runtime judgments were not measured.

The 2026-10-06 extension adds conditional CSS and Motion for React references,
scroll coordination, and preference-change handling. Runtime behavior remains
unmeasured; parent review checks instruction decisions, not rendered results.

Validation: full locked checks passed (35 skills, 76 tests, CLI fixtures). Creator
validation, selective installation of all seven files byte-for-byte, MIT preservation,
and local links passed. Body: 3,531 characters.
