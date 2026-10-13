# Independently verifiable work units

Read when breaking a larger plan into work items or drafting a task list.

- Start each item with an action and observable result. "Improve reliability" needs
  the selected failure and required behavior; "preserve the saved draft after a
  failed submission" identifies a result that can be checked.
- Keep tightly coupled changes together when splitting would leave no usable or
  verifiable result. Separate independently reviewable outcomes; one file, function,
  or checklist line is not automatically one task.
- A strict dependency means the later item consumes an earlier artifact, contract,
  or environment state. Shared files require coordination, not necessarily a serial
  dependency. Preserve dependencies and priorities established by the user.
- Separate executable work, in-scope decisions awaiting evidence, areas that still
  need exploration, and accepted exclusions. For each material unknown, name the
  question, the evidence that would settle it, and the work it blocks. An accepted
  exclusion stays outside the plan until the user changes the goal.
- Reuse source references and existing task IDs when supplied. Consolidate duplicated
  outcomes without dropping acceptance conditions. Add validation work when it is
  required completion evidence; avoid automatically appending extra quality tasks.
- Return a draft within planning scope. Creating records in an external task system
  needs a registration request and a known destination; drafting grants neither.
  Follow the requested format rather than imposing a tracker or task template.

## Larger or uncertain efforts

Prefer a narrow usable slice across the necessary layers over separate database,
backend, and UI tickets that cannot demonstrate a result alone. Keep enabling work
separate when another slice genuinely consumes it; do not invent demo scaffolding
or extra features to make every task independently shippable.

For sweeping migrations, consider expand → migrate → contract: first preserve old
consumers while adding the new path, move callers in verifiable batches, then remove
the old path after required consumers and compatibility checks permit it. If only
the combined change can pass, record that integration constraint and the final
checks rather than claim each intermediate unit is releasable.

For work too uncertain to plan end to end, keep a small map: destination, settled
decisions with source links, blocking questions, and next evidence-gathering steps.
Expand executable detail as decisions settle. Carry the map across sessions without
copying recoverable repository facts. Research and prototypes answer named questions;
their completion does not itself authorize implementation or tracker changes.

A task intended for another session needs enough accepted behavior, relevant paths,
decision references, dependencies, and completion evidence to resume without this
chat. Size it around a coherent result, not a fixed token budget or session count.

For motion or other experiential decisions, inspect available code and tokens first.
Ask about the unresolved user outcome or a perceptible reference; propose technical
values from evidence. Known facts and routine settings need no interview. Record a
material assumption, or resolve it before dependent work when it changes the result.
