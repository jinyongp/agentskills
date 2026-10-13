# Documentation structure and presentation

Read when drafting or reviewing organization, prose, lists, tables, examples, or navigation.

## Identify the reader's task

Choose the form from what the reader needs:

- **Learn a workflow:** a coherent path with prerequisites and recognizable success.
- **Complete a task:** direct steps, relevant decisions, and recovery.
- **Look up an interface:** exact names, parameters, defaults, errors, and versions.
- **Understand a design:** reasons, boundaries, and tradeoffs.

The [Diataxis framework](https://diataxis.fr/) distinguishes these needs. Use it as
a lens; a small product does not need a mandatory four-part documentation tree.

## Group information before formatting

Open with the task and its answer or outcome. A lookup page can start with the
interface and applicability. Preserve deliberate narrative sequencing where relevant.

Give distinct reader questions useful headings. Separate setup, defaults,
exceptions, recovery, and internals when mixing them forces readers to classify
facts themselves. Replacing every sentence with a bullet does not repair mixed scope.

Keep a detail beside the step when it changes the next action, prevents a relevant
failure, or explains the result. Link independent variants, design rationale, or
internals where needed. Keep limits and cautions before the affected operation.
Preserve useful source notes while shaping the requested document; drafting does
not require rewriting those sources or consuming every fragment.

## Choose a form that supports use

- **Prose:** explain context, reasons, or cause and effect in connected sentences.
- **Bullets:** expose independent requirements, conditions, or alternatives.
- **Numbered steps:** show actions whose order matters for completion.
- **Task headings and fenced code:** let readers find and execute an operation.
- **Comparison tables:** compare attributes that change a choice, such as platform
  support, requirements, or behavior. Shared column labels alone do not justify a table.
- **Lookup tables:** retain compact mappings that help readers find an exact value
  or meaning, such as option/default or term/definition pairs.
- **Specific links:** route separate tasks and optional workflows to their own detail.

A task/command/description table often adds no useful comparison. Long link lists,
commands, or paragraphs inside cells can hide structure again; use grouped lists,
task examples, or short summaries with detail links. Do not add formats solely for
variety or impose paragraph, table, or section quotas.

## Build a complete example

Introduce what the example demonstrates, then keep its required setup, inputs,
public invocation, and recognizable result together. Keep inputs consistent with
preceding setup. Separate independent variants; retain composition when the example
is intended to demonstrate APIs working together.

An API call need not teach object prototypes first. Keep a field-access caveat beside
the call if it changes how the response is used; link unrelated mechanics separately.
Introduce concepts before later reasoning relies on them, using the audience's stated
prerequisites. Expert references need not become beginner tutorials.

Missing output or examples need evidence, a labeled hypothetical illustration, or
a narrower claim. Never invent observed results or author experiences. Retain names,
qualifications, and conditions that affect the task.

## Preserve navigation

Keep supported-version access and useful anchors and URLs. Inspect known inbound
links and redirect support before moving published paths; report gaps rather than
promising unverified redirects. Update relevant generated indexes through their source.

## Review discovery and completion separately

1. Scan headings, opening lines, lists, table labels, and example introductions.
   Can readers locate prerequisites, actions, choices, and results without reading
   every paragraph? Identify buried conditions, mixed tasks, and excessive detail.
2. Follow the selected task fully. Check that each step has its setup and that the
   result is recognizable. Compiling commands, screenshots, and a docs build do not
   establish usability or reader comprehension.

For each obstruction, name the passage, affected task, reader impact, and a concrete
regrouping, format change, or relocation. Prioritize missing/misleading instructions
and structural obstacles before wording polish. Keep effective prose and necessary
qualifications. Draft continuously unless collaboration was requested; paragraph-by-
paragraph approval is not a default writing workflow.
