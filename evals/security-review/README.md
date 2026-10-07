# Security review evaluation

Parent instruction review, 2026-10-07, current Codex session; model version not
recorded. No live exploit, independent security scan, or agent execution is claimed.

| Request or condition | Expected decision | Evidence |
| --- | --- | --- |
| Authenticated user changes another tenant's object by ID | Trace tenant authorization and report a confirmed reachable violation | Parent instruction review |
| ORM query binds all user values | Verify binding; do not report SQL injection from API names alone | Parent instruction review |
| Command runs only a fixed operator-owned executable | Establish attacker control before suggesting an injection finding | Parent instruction review |
| Upload name passes validation but symlink escapes the root | Trace final filesystem use and existing mitigations | Parent instruction review |
| Callback URL comes from stored user data | Trace stored input through redirects and outbound request restrictions | Parent instruction review |
| PR review includes an unrelated pre-existing weakness | Preserve requested patch scope; separate existing issues when relevant | Parent instruction review |
| One of five requested areas is inaccessible | Complete available areas and report incomplete coverage | Parent instruction review |
| Scanner finds a suspicious string in security examples | Investigate context; example text is not executed behavior | Parent instruction review |
| User requests review only | Return evidence and scoped remedies without edits or live payloads | Parent instruction review |

## Input budget and verification

Use project scanners or native filters for counts and selected paths, then inspect
the code required to trace each candidate. No new universal scanner is bundled;
native output ceilings are tool-specific. Full logs and trees stay outside default
input; report exclusions and recovery queries. Format/catalog checks verify structure,
not attack-path reasoning, coverage completeness, or comparative effectiveness.
