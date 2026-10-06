# Documentation form and navigation

Read when choosing a form or restructuring a documentation area.

## Choose the reader's next action

A beginner learning a workflow needs a coherent guided path and visible success.
An experienced reader completing a task needs prerequisites, decisions, commands,
and relevant recovery. Someone looking up an interface needs precise parameters,
defaults, errors, units, and version applicability. Understanding a design needs
reasons, boundaries, and tradeoffs. Use the form that answers the request; a small
product need not create four separate document trees.

The [Diataxis framework](https://diataxis.fr/) distinguishes tutorial, how-to,
reference, and explanation needs. Treat this as a useful design lens rather than
an enforced repository layout. Keep conceptual discussion out of a command sequence
when it blocks progress, linking an explanation when the reader needs one.

## Scope and navigation

A README should give enough orientation and first-use information for its audience.
Link deeper material when it has a separate reader task. Organize around actual
tasks and public concepts rather than copying internal folders into a table of contents.
Keep required information available without relying on an undocumented chat history.

Preserve stable anchors, cross-links, and supported-version access when reorganizing.
Inspect known inbound links and redirect support before moving published paths.
If redirects cannot be verified, report the gap rather than silently promising them.
Update only relevant catalogs or generated indexes through the project's tooling.

## Make the main path visible

Use these decisions when drafting or reviewing; they are not a word-count target
or a requirement to split every subject into its own page.

| Inspect | Decision |
| --- | --- |
| Opening and headings | Name the task and its answer or outcome before supporting detail. A lookup page names the interface and applicability instead of inventing a tutorial. |
| Paragraph on the main path | Retain it here if it changes an action or choice, prevents a relevant failure, or explains the shown result. Put independent rationale or implementation mechanics in a linked section. |
| Code example | Introduce the behavior it demonstrates, keep only setup needed for that behavior, and explain how to recognize the result. Use separate labeled examples for independent variants; retain integrated examples when composition is the task. |
| Instructions between setup and success | Keep prerequisites and applicable safety or correctness warnings before the affected step. Place optional alternatives and deeper mechanics after success or behind a specific link. |
| Repeated explanation | Keep a canonical definition and a link; repeat only the local condition needed to act. |
| Review finding | Cite the passage, the reader task it obstructs, and the concrete move, cut, or rewrite. Distinguish a blocked or misleading path from distracting detail; describe the effect rather than calling the page merely verbose. |

For an API-call guide, a normal request and response belong on the main path.
Prototype construction or clone semantics belong there only when they affect that
call or the reader's next operation. A mutation caveat can stay beside the affected
step while its implementation explanation moves to a linked section.

Review readability separately from command correctness: a compiling example can
still bury its purpose. Inspect the opening and heading sequence for the promised
task, then follow a representative example from setup to result. Check whether its
meaning depends on unrelated internal explanations. Preserve qualifications needed
for correct use; shorten by relocating competing topics and removing repetition.
