# Writing

Skills for conversational delivery, source summaries, documentation, and editing.
`write` drafts new prose; `rewrite` edits or reviews existing prose. Language guidance
can refine either task without requiring another installed skill.
Conversation styles preserve the full scope of implementation and verification.
Each skill works independently and declares its own license.
<!-- skills:start -->
| Skill | Description | Install |
| --- | --- | --- |
| [clear](clear/SKILL.md) | Answer clearly for readers with ADHD or limited attention. Use when the user requests readable, answer-first conversation with concise explanations and essential detail preserved. | `npx skills add jinyongp/agentskills --skill clear` |
| [terse](terse/SKILL.md) | Use blunt, terse conversation when the user requests maximum signal with minimal wording. Preserve every essential condition, risk, and requested deliverable. | `npx skills add jinyongp/agentskills --skill terse` |
| [brief](brief/SKILL.md) | Present status, progress, and handover updates as a scannable briefing when requested. Distinguish completed, active, pending, and unknown states; retain blockers and real next decisions. | `npx skills add jinyongp/agentskills --skill brief` |
| [summarize](summarize/SKILL.md) | Summarize a specified document, thread, transcript, file, or pasted text faithfully. Preserve essential facts, attribution, conditions, and actual action items; use when source-content compression is requested. | `npx skills add jinyongp/agentskills --skill summarize` |
| [rewrite](rewrite/SKILL.md) | Edit prose for clarity and natural voice while preserving facts, intent, and essential qualifications | `npx skills add jinyongp/agentskills --skill rewrite` |
| [write](write/SKILL.md) | Draft reader-facing prose from a brief or evidence, with a clear purpose, appropriate voice, and supported claims. Use for new documents, articles, messages, or product copy; use rewrite for editing existing prose. | `npx skills add jinyongp/agentskills --skill write` |
| [korean-writing](korean-writing/SKILL.md) | Create, edit, or review Korean reader-facing prose for natural syntax, register, and information flow. Use for Korean writing or translationese concerns; ordinary Korean conversation alone does not require this skill. | `npx skills add jinyongp/agentskills --skill korean-writing` |
<!-- skills:end -->

Add skills at `skills/writing/<skill-name>/SKILL.md`.
[Authoring guide](../../CONTRIBUTING.md) · [All skills](../../README.md)
