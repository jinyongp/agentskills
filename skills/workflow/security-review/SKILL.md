---
name: security-review
description: "Review specified code, configuration, or changes for exploitable security defects. Trace attacker control, trust boundaries, permissions, and existing defenses; report supported findings with confidence and scoped evidence."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Security Review

## Scope

Review the named files, revision, configuration, or system boundary. Establish
assets, attacker capabilities, and expected access rules from project policy and
actual behavior. Review alone does not authorize fixes, live exploits, credential
access, publication, or broad hardening. Use existing project tools and protections.

Read [references/attack-path.md](references/attack-path.md) when tracing authorization,
injection, files, outbound requests, secrets, or workflow credentials.

## Procedure

1. Pin the target and map every requested area. For a patch, distinguish introduced
   defects from existing issues; for a broader audit, retain the requested coverage.
   Inspect relevant callers/configuration to confirm a finding without expanding
   the reported scope. Recover accepted design limits before proposing changes.
2. Identify who can control each relevant input, stored value, file, dependency,
   or event. Follow it through validation, parsing, permissions, and sensitive use.
   An authenticated user can still attack another tenant or exceed their own role.
   Assess configuration under the actual deployment and trust model.
3. Confirm defenses on the reachable path: framework escaping, parameter binding,
   canonicalization, authorization, sandboxing, or workflow event restrictions.
   A dangerous-looking API is a lead; a string match is not a finding. Separate
   a concrete bypass from an optional improvement or hypothetical future exposure.
4. Explain the trigger, violated boundary, reachable effect, affected location,
   existing mitigations, and confidence. Read the complete relevant code path;
   missing attacker control or an unresolved defense leaves a verification gap.
   Use a minimal isolated reproducer when needed and authorized. Do not send live
   attack payloads, inspect secret values, or disable defenses to demonstrate risk.
5. Prioritize supported defects by impact and realistic prerequisites; distinguish
   severity from confidence. Report uncertain candidates separately with the exact
   fact needed to resolve them. Duplicate symptoms of one cause share one finding.
   Evidence can support zero findings; inaccessible areas remain unreviewed.
6. If fixes are authorized, correct the demonstrated boundary and exercise the
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
