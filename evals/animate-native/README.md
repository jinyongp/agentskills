# Animate native evaluation

| Request | Expected decision | Parent review |
| --- | --- | --- |
| Add a simple fade using an adequate existing native driver | Reuse the project tool | No compulsory Reanimated migration |
| Gesture competes with nested scroll in a sheet | Resolve ownership, cancellation, and explicit dismissal | Motion is more than timing |
| Keyboard compensation already exists | Verify actual access before adding another offset | No duplicate keyboard handling |
| Haptic call succeeds but hardware supplies no feedback | Preserve visual/semantic outcome and report physical-device evidence | Capability limits retained |
| System reduced-motion preference changes during use | Update the alternative where supported | State remains usable |
| Performance is judged only in a debug simulator | Report evidence limits; use relevant release/device profiling for claims | No unsupported smoothness claim |
| A worklet API differs across installed versions | Consult installed-version documentation | No universal runtime API recipe |
| A native animation is also used on web | Check web-specific input and viewport behavior | Platform coverage explicit |
| A large application contains unrelated screens | Inspect selected scope with bounded project detail | No broad inspection claim |

## Validation and limits

Evaluated 2026-10-06 (Asia/Seoul), current Codex session; model version not recorded.
Cases assess written decisions through parent review, not independent agent execution.
Automatic selection and real-project motion quality remain unmeasured. No browser,
device, or frame-rate behavior was exercised here. No tests pin instruction wording.

No runtime helper is bundled for selected implementation. Inspection budgets depend
on project tools. Release builds, gesture feel, accessibility focus, keyboard behavior,
and haptics were not independently exercised during authoring.

Body: 3,773 characters. Full verification passed: 35 skills, 74 tests, and CLI
fixtures. Creator validation, actual selective installation of all four files
byte-for-byte, upstream MIT comparison, and local links passed.
