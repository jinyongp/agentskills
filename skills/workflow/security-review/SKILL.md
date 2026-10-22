---
name: security-review
description: "Review specified code, configuration, or changes for exploitable security defects. Trace attacker control, trust boundaries, permissions, and existing defenses; report supported findings with confidence and scoped evidence."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Security Review

Review the named files, revision, configuration, or system boundary. Establish
assets, attacker capabilities, and expected access rules from project policy and
actual behavior. Review alone does not authorize fixes, live exploits, credential
access, publication, or broad hardening. Use existing project tools and protections.

## Core rules

- **Reachable attack path.** Trace attacker control, violated boundary, reachable
  effect, and existing defenses. A dangerous API or string match is a lead, not a
  finding. Missing control or unresolved defenses leave a verification gap.
- **Safe evidence.** Read the complete relevant path. Use a minimal isolated
  reproducer only when needed and authorized; do not send live attack payloads,
  inspect secret values, or disable defenses to demonstrate risk.
- **Severity and confidence differ.** Prioritize supported impact and realistic
  prerequisites. Zero findings is valid; inaccessible areas remain unreviewed.

Read [references/attack-path.md](references/attack-path.md) when tracing authorization,
injection, files, outbound requests, secrets, or workflow credentials.

## Trace and confirm

1. **Coverage.** Pin the target and map every requested area. For a patch, distinguish introduced
   defects from existing issues; for a broader audit, retain the requested coverage.
   Inspect relevant callers/configuration to confirm a finding without expanding
   the reported scope. Recover accepted design limits before proposing changes.
2. **Attacker control.** Identify control over each input, stored value, file, dependency,
   or event. Follow it through validation, parsing, permissions, and sensitive use.
   An authenticated user can still attack another tenant or exceed their own role.
   Assess configuration under the actual deployment and trust model.
3. **Defenses.** Confirm escaping, parameter binding, canonicalization, authorization,
   sandboxing, or workflow event restrictions on the reachable path. Separate a
   concrete bypass from optional improvements or hypothetical future exposure.
4. **Confirmation.** Explain trigger, boundary, effect, location, mitigations, and
   confidence using the attack-path and safe-evidence rules.
5. **Disposition.** Report uncertain candidates separately with the exact
   fact needed to resolve them. Duplicate symptoms of one cause share one finding.
6. **Authorized fixes.** Correct the demonstrated boundary and exercise the
   attack condition plus a legitimate operation. Preserve public contracts and
   accepted limits; do not add unrelated infrastructure, controls, or test matrices.

## Result

Return findings with precise locations, attacker prerequisites, evidence, impact,
confidence, and a scoped remedy. State reviewed areas, actual checks, and unresolved
coverage. Neither a clean scanner nor a clean reviewed subset establishes system safety.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
