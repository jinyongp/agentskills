# Parent task execution and replay

On 2026-10-06 the parent Codex session loaded the five recent skills and relevant
conditional references, authored scoped task outputs, and exercised them in
disposable projects. The model version was not recorded. Commands, package
resolution, application behavior, timed code, database effects and consumer
failures actually ran.

The [replay](replay.py) checks those completed outputs against explicit fixture
contracts. It does not invoke an agent, automatically select skills or generate
new solutions. Parent authoring and checking are not independent judgment. These
results establish behavior of selected outputs; they do not establish that the
instructions caused better decisions or every procedural step was followed.

## Task briefs and outcomes

| Skill and request | Required outcome | Executed evidence |
| --- | --- | --- |
| dev-docs: Write a short English guide to the existing quantity-sum CLI; leave implementation unchanged | Accurate prerequisites, stdin/output and relevant recovery | Documented Bash pipeline and direct Python invocations; valid, empty, negative, boolean, object and malformed inputs; implementation hash unchanged |
| dependency-update: Move the owned core package to version 2; migrate necessary consumers and coupled packages; preserve unrelated work | Real resolver and runtime compatibility, reproducible installation | Local npm packaging, install, peer warning, invalid installed tree, strict resolution failure, adapter update, runtime failure before consumer migration, corrected runtime and npm ci rerun |
| optimize: Reduce repeated catalog-search CPU cost; preserve ordering, repeated IDs, first matching label and missing-value behavior; transient index memory is acceptable | Supported time improvement with behavior and memory costs reported | Independent expected-value cases, deliberately wrong last-wins negative control, profile, seven alternating unprofiled samples per variant and one traced-memory sample per variant |
| db-migrate: Add and backfill a new label while old consumers remain usable; preserve populated targets; recover an interrupted batch | Atomic data/checkpoint work, durable resume, reconciliation | SQLite file database, injected interruption, rollback, close/reopen resume, completed retry, old/new reads, below-cursor late insert, gap detection, reconciliation and disposable backup readback |
| api-design: Review an additive response-field proposal against the strict supported consumer; leave implementation unchanged | Concrete compatibility finding backed by actual consumer behavior | Current serialization decodes successfully; proposed serialization raises ValueError; source hash unchanged; scoped written finding |

Task outputs are in [fixtures](fixtures/). Inputs are synthetic and local. No
project dependency, deployed service, installed skill, user database, remote
record or global tool installation was changed.

## Findings and correction

The first replay expected an incompatible peer update to return a failing npm
exit code. npm 10.9.7 instead returned **0** with `ERESOLVE overriding peer dependency`
warnings. That replay failed at its expectation and was not reported as a five-task pass.

The completed replay checks that warning and the invalid installed tree
(`npm ls --all --json` fails), then exercises strict-peer resolution failure.
dependency-update now explicitly requires inspecting warnings and peer validity
after a successful resolver exit. Moving the compatible adapter still leaves
the old application call broken; consumer migration must precede runtime success.
These are observed npm results, not cross-manager exit-code guarantees.

The local search fixture's median elapsed time changed from **17.698173 ms** to
**0.118253 ms**, including index construction. Traced allocation peaks increased
from **17,064 bytes** to **110,784 bytes**. Seven samples alternated order; all
candidate samples were below all baseline samples in this run. The profile
attributes original cost to repeated scanning. Single traced-memory samples are
allocator/order sensitive, not RSS or confidence intervals. This workload does
not establish production benefit.

The completed [results.json](results.json) includes versions, fixture hashes,
raw timing samples, tradeoffs and task statuses. Raw logs and native profile remain
local in `/tmp/agentskills-task-execution-20261006-c/`; that location is temporary.
The replay regenerates them in an explicitly selected new directory.

## Reproduce

Requirements: Linux/POSIX, Bash, Python 3.11+, Node.js and npm. This run used Python
3.11.17; the documented pipeline used Python 3.14.8 from PATH. Node.js was 22.22.2,
npm 10.9.7 and SQLite 3.53.1. Packages use local tarballs, offline resolution and
disabled lifecycle scripts; no registry access is needed. Other npm versions can
have different peer behavior; record that difference rather than claiming a skill failure.

From the repository root, choose an unused evidence directory:

```bash
uv run --locked python evals/task-execution/replay.py --output /tmp/agentskills-task-eval-01
```

The runner refuses to overwrite evidence directories, saves command logs and a
JSON report, uses temporary task projects and fails on violated fixture expectations.
It does not gate on fixed speedups: overlapping timings are reported as inconclusive.
Run it when reproducing these findings or revising their task boundaries; it is
not another mandatory CI suite.

## Limits and repository checks

This does not cover all 49 skills, automatic activation, fresh-agent solution quality,
skill combinations, multilingual reader judgment, public package release/advisory
research, workspaces, native builds, lifecycle hooks, live concurrency, other database
engines, production restoration, HTTP transport, SDK generation, authorization or
retry guarantees. No with/without-skill comparison was performed.

Repository validation passed for 49 skills and all 76 existing tests passed.
The initial installation check failed because the default npm cache was read-only.
Retrying only `check.py smoke` with a writable temporary npm cache passed discovery,
selective installation and byte-for-byte resource checks using skills@1.7.0.
No required check was bypassed.
