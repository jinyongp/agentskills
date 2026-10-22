# Validation results and reuse

Read for background/delegated checks or when deciding whether an earlier result
still applies.

**Confirm the result.** A successful launch, queue receipt, or delegation prompt
does not establish that a check ran. Retain the job identity and obtain its actual
result through the host's supported mechanism. Match the result to the requested
command, target state, and outcome; a terminal worker status alone does not prove
the required check passed. Report an observed check failure as failed. A missing or
pending result, or a worker failure without check results, leaves that criterion
unverified. Continue independent checks without launching duplicate work merely
because the result is delayed.

- Record the command, outcome, checked behavior, relevant code/configuration state,
  and environment with the evidence. A commit ID alone omits dirty and untracked
  inputs. Use scoped Git detail or fingerprints when needed; capture no credentials.
- Trace actual inputs and consumers. A serializer or exported function change can
  invalidate a caller's check although the caller's file is unchanged. A focused
  producer pass does not establish consumer compatibility.
- Compare relevant configuration, lock/runtime versions, fixture data, and execution
  conditions as well as source. Passing before a configuration change is historical
  evidence; rerun the affected check and preserve its earlier log separately.
- Reuse results for unaffected contracts when the tested inputs and conditions still
  apply. A documentation edit alone need not invalidate runtime evidence. Missing
  state identity limits reuse; it is not evidence that the whole suite must rerun.
- On handoff, link durable evidence and identify its tested state. Record unlogged
  results only when they change the next action. The receiver checks current inputs
  before treating a previous pass as valid; a resume does not reset required checks.
