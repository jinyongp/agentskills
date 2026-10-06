# Dependency update evaluation

## Decision cases

Parent instruction review on 2026-10-06 in the current Codex session; model version
not recorded. This matrix reviews decision rules; no live dependency upgrade or
independent agent execution is claimed.

| Request or condition | Expected decision | Review result |
| --- | --- | --- |
| Refresh one package within its permitted range | Respect the named target and inspect actual resolution | No automatic latest-major update |
| Explicit major upgrade needs companion adapters | Use a justified compatible group and scoped consumer migration | No unrelated dependency campaign |
| Target is unavailable or violates a runtime requirement | Verify the blocker and propose an evidenced alternative | No fabricated version or silent substitution |
| Project uses an alternate registry or prereleases | Follow project policy and verify source availability | No default registry or stable-tag assumption |
| Transitive vulnerability is constrained by a parent | Trace the affected path and actual fix | No unsupported override just to quiet a scan |
| Existing goal is already satisfied | Report verified no-change result | No forced edit |
| Workspace contains several lockfiles | Find actual ownership before updating | No automatic lock removal or manager migration |
| Resolver causes broad unexpected churn | Trace tool/configuration and dependency causes | Diff review precedes acceptance |
| Peer resolution or native build fails | Diagnose; preserve partial work and state checks not run | No blind force, reset, or repeated attempt |
| Installation hooks mutate state | Follow execution scope; isolate relevant checks | Install is not misclassified as read-only |
| Resolution succeeds but application import fails | Correct the scoped migration and rerun affected checks | Resolver success is not runtime verification |
| Offline, unauthenticated, or unsupported platform | Keep proposal and verification gaps explicit | No implied complete compatibility |
| Large dependency graph and long lock diff | Selected package summary, scoped detail, counts and recovery query | No full graph dump or hidden truncation |
| Recommendation only or global update outside scope | Return the proposal or scoped local result | No unauthorized installation or deployment |

## Input budget and limits

No universal dependency parser is bundled. Use the selected manager's scoped queries
and relevant manifests; full graphs, locks, and release histories stay outside default
input. Native output varies, so no measured universal ceiling is claimed. If reduction
requires a new helper in the target project, define recovery semantics and verify
large inputs and failures. Reference loading is conditional.

Compatibility judgment, advisory interpretation, actual installation/migration,
multi-platform execution, automatic routing, and large-graph recovery remain
unmeasured by independent execution. Guidance is original with primary-source links.

Packaging verification passed: 46 skills, 76 existing tests, and CLI fixtures.
Creator validation and actual selective installation with skills@1.7.0 passed;
all four bundled files matched byte-for-byte. MIT notice and local links passed.
Entrypoint body: 3,818 characters, excluding frontmatter.

Subsequent [parent task execution](../task-execution/README.md) exercises actual
local npm updates, incompatible peers, consumer migration and clean installation.
A zero-exit peer warning prompted explicit warning/peer inspection guidance.
The historical matrix above remains instruction review, not independent execution.
