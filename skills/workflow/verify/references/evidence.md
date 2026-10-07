# Reusing validation evidence

Read when deciding whether an earlier result still applies.

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
