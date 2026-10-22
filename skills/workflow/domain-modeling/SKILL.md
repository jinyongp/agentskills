---
name: domain-modeling
description: "Clarify ambiguous business terms and rules using concrete scenarios. Reconcile domain language across code and docs; record settled meanings and consequential decisions only when useful."
license: MIT
metadata:
  author: jinyongp
  category: workflow
---

# Domain Modeling

Clarify business concepts when overloaded terms, conflicting rules, or uncertain
relationships affect a requested decision. Reading established terminology alone
needs no modeling session. Preserve accepted product limits and context boundaries.
Analysis stays inline unless documentation edits are requested or already in scope;
modeling does not authorize code changes, renames, migrations, or external writes.

## Core rules

- **Intent is not implementation.** Compare stated intent, definitions, and
  observed code behavior. Report contradictions with sources; current code does
  not settle intended policy. Keep unresolved rules explicit instead of choosing
  the easiest implementation.
- **Context matters.** Keep distinct names across contexts when meanings differ.
  Invented scenarios are probes, not established requirements.

## Clarify and record

1. **Sources.** Locate definitions and decisions for the selected area. Start
   with relevant headings and symbol searches, then inspect necessary definitions
   and callers. Report missing contexts rather than treating a partial search as
   proof that a concept or rule is absent.
2. **Ambiguity.** Identify one word for different concepts, different words for one
   concept, or a disputed relationship or lifecycle rule.
3. **Scenarios.** Test the distinction concretely. For example, can one
   customer own two accounts, and can an account exist without an active user?
   Ask only questions whose answers change the model or dependent work.
4. **Reconcile.** Apply the intent/evidence distinction to the disputed scenarios.
5. **Meaning.** Settle the term, relevant relationships/invariants, and distinguishing
   example. Keep implementation names as source pointers rather than mixing file
   mechanics into the business definition. Recheck the disputed scenarios against
   the agreed meaning, including a legitimate case it must still allow.
6. **Record when authorized.** Update the existing glossary or equivalent in
   place; create a small glossary only when settled terms need a durable home.
   Follow project destinations. Propose a decision record only when the choice is
   costly to reverse, surprising without context, and reflects a real tradeoff.
   Record the current choice and necessary rationale; preserve earlier history
   according to project policy. Keep open questions separate from settled terms.

## Result

Return clarified terms/rules, source-backed conflicts, decisions still needed, and
affected work. Link existing definitions instead of copying the repository model.
Report documentation edits separately from proposed code changes. A resolved name
does not prove implementation matches the rule.

## Saved records

Save only when requested or needed by this workflow. User/project paths take
precedence; default: `<project-root>/.agents/artifacts/<run-id>/<skill-name>/`.
Use a UTC timestamp plus unique suffix for a new run; reuse an explicitly shared ID.
Add a short `summary.md` linking raw evidence when useful. Preserve existing files
unless updating them was requested. Return exact paths; commit or publish records
only when requested. Disposable command files use OS temp.
