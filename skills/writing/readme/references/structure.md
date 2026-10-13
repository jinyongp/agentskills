# README structure and presentation

Read when drafting or reviewing README organization, prose, examples, lists,
tables, or navigation. Judge whether consumers can find and complete their task.

## Group before formatting

Identify the questions a consumer needs answered: what this does, requirements,
installation, first use, success, relevant choices, and where to go next. Give
distinct tasks meaningful headings. Keep one initial path together; separate
independent examples and maintainer work. Existing house style and useful anchors
still apply; these questions do not require a fixed set of sections.

Do not turn accumulated facts into successive paragraphs or bullet every sentence.
First decide which facts belong together and which belong in deeper documentation.

## Choose a form that exposes the relationship

| Information | Useful form | Decision check |
| --- | --- | --- |
| Reasons, context, or cause and effect | Prose | Does the connection need explanation? |
| Independent requirements, conditions, or choices | Bullets | Can readers locate each item without parsing a paragraph? |
| Actions whose order matters | Numbered steps | Is sequence required for completion? |
| Alternatives sharing comparison attributes | Table | Do rows and columns answer a real selection or lookup question? |
| Executable input and recognizable output | Code blocks beside the relevant step | Does each block have a clear purpose and required setup? |
| Separate reader tasks or optional workflows | Headings and links | Can readers find one task without traversing another? |

A table cell containing many links, commands, or paragraphs may hide the structure
again. Use a short summary with a specific detail link, or a grouped list when
there are no useful comparison columns. Keep a compact, useful existing table.
Do not add tables, diagrams, badges, or contents merely for visual variety.

A task/command/description table often repeats each task's name without helping
readers compare choices. When readers need to find and execute a known task, use
a task heading, a short explanation, and a fenced command block. Use a comparison
table when attributes affect a choice, such as installation methods differing in
agent support, scope, or included rules. Shared column labels alone do not justify
a table; compact option/default lookup tables can still serve a real lookup task.

## Review discovery as well as completion

Scan headings, opening lines, lists, table labels, and example introductions.
Can a new consumer locate prerequisites, one install command, first use, and the
success signal without reading every paragraph? Then follow that path fully.
Successful commands do not establish that the document is easy to navigate.

Retain details that change the next action, prevent failure, or explain the result.
Link independent variants, internal mechanics, migration histories, and maintainer
operations where needed. Keep applicable limits before incompatible setup.

Rank failures by reader impact: missing or misleading instructions, buried tasks,
mixed information, and excessive detail can obstruct use. Report the specific
passage, affected task, and repair before wording polish. No paragraph-length,
table-count, or section-count quota establishes readability.
