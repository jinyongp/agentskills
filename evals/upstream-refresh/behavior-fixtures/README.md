# Disposable evaluation projects

These synthetic inputs were prepared before independent agent dispatch. They are
not application examples or a passing production test suite. The pricing and
cleanup fixtures deliberately retain defects that an assessment must report.
Run them only in a fresh temporary copy, never by changing these recorded inputs.

- `animation/`: serve the static browser demo, then ask the agent to investigate
  and improve expensive dragging while preserving its README requirements.
- `verify/`: ask for release readiness using the existing local background facade.
  Source/tests/configuration/adapter edits are excluded; generated artifacts are
  allowed. The initial `old-unit` result is intentionally from another target.
- `handoff/`: recorded post-change inputs. For a fresh replay, first set retention
  to 30, initialize a disposable Git repository, commit the source and decisions,
  and capture the three-test pass with its actual revision/configuration hash.
  Then change retention to 14 without committing, add the unrelated operator note,
  and provide that new run's evidence to the writer. The bundled dated evidence
  records the original execution, not a new replay's identity.

Handoff session facts supplied only to the writer: retention 14 is intentional;
offline/single-device scope and rejection of cloud sync are accepted; real deletion
is temporarily forbidden pending retention-policy review, with no exit confirmed;
the next task is verification only. The receiver gets the writer's packet, named
skill, and project access, without the parent history or grading expectations.

Use fresh evaluator histories and the selected repository skill. Do not pass
`behavior-expectations.md`, previous outcomes, or intended diagnoses to evaluators.
Original temporary paths in evidence are exact historical inputs. Durable copies
of outputs are under `../behavior-artifacts/`; see the execution report for grading
and environment limits.
