# Component craft and spatial clarity

Read only the section relevant to the requested design decision. These principles
support the product's chosen identity; they do not prescribe an Apple-like appearance.

## Coherent defaults

Design the resting state and common interaction as one experience. Defaults should
carry readable hierarchy, predictable feedback, and useful state behavior before
offering customization. Reuse established tokens and primitives. Component APIs
should make the intended use easy without accumulating options for hypothetical needs.

Distinguish acknowledgement from commitment: a press can show immediate feedback
while activation still respects cancellation and control semantics. Deliberate
confirmation must match the action and accessible alternatives, not a universal
hold gesture. Explain consequential outcomes before committing them.

## Information relationships and hierarchy

Before choosing containers or type styles, identify what the user must decide or do,
which facts belong together, and which information changes that decision. A shared
row, border, badge treatment, or emphasis implies a relationship; check that it is
the intended one. Increasing a heading's size cannot repair a wrong grouping.

Use these examples to choose a representation, not as fields to add to every screen.
Keep actual product content and deliberate density; unrelated chat context and an
illustrative example are not requirements for the interface.

| Relationship and typical task | Inspect and decide |
| --- | --- |
| Label/value in account settings | Can the reader tell which value each label describes? Keep the association through alignment, proximity, wording, and suitable semantics; obvious values need not gain redundant labels. |
| Price/condition in plan selection | Can the buyer find the billing period and eligibility condition for the displayed price? Keep them associated; visual subordination must not hide a material condition. |
| Item/state/action in order management | Can the user identify an order's payment and delivery states and which order an action affects? Keep status distinct from an available action and bind both to their item. |
| Comparable properties in search results | Can the user compare the same property across results? Use consistent labels, order, or aligned columns; a separate card for every fact can obstruct comparison. |
| Peer choices or supporting article metadata | Equal weight or a compact author/date row can be appropriate when roles are clear. Do not invent a priority or expand every value into a labeled block. |

Choose grouping, labels, reading order, and emphasis together. A separator is useful
inside a clear metadata group; punctuation changes, more badges, or extra cards do
not establish missing relationships. Preserve those relationships in source order
and accessible semantics as well as visually. See [GOV.UK summary lists](https://design-system.service.gov.uk/components/summary-list/)
for label/value versus list/table decisions and [WCAG information and relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)
for preserving meaning when presentation changes.

Inspect the rendered surface by following a task: find the relevant item and decisive
facts, identify current state, and locate the action and its target. Recheck after
regrouping. Equal weight and small type are not defects by themselves; source review
or screenshots alone cannot establish user comprehension.

## Spatial continuity and direct manipulation

Keep the relationship between a trigger, expanded content, and destination clear.
Origin, grouping, or restrained motion can explain that relationship; instant changes
are also valid when movement adds delay or discomfort. Keep perceived and semantic
state coherent, especially after rapid reversal or interrupted dismissal.

For dragging, preserve where the user grabbed the surface and distinguish tracking
from settling. Input changes should not cause avoidable jumps. Appropriate velocity
handoff can support continuity, but a particular spring engine or momentum formula
is not a requirement. Preserve explicit controls and reduced-motion alternatives.

## Layers and materials

Use depth, borders, scrims, or translucent surfaces to clarify hierarchy and modality.
Choose the technique from the product's identity and actual background. Translucency
needs legibility over changing content and a suitable fallback when unavailable or
inappropriate; increasing blur alone does not establish contrast or accessibility.

Visual dimming is separate from modal behavior: a modal still needs focus and
background interaction handling. A nonmodal panel should not acquire an unnecessary
blocking scrim. Check expensive effects when performance evidence warrants it.

## Typography in context

Judge size, weight, spacing, and line height together using actual content and fonts.
Optical sizing helps only when the font and rendering path support it. Tracking that
works for a large display heading may not fit body text or another writing system.
Keep diacritics, CJK, emoji, and supported scripts legible without clipping.

Honor chosen typefaces and product tokens. A system font can be a useful default,
not a compulsory replacement. Exercise text enlargement and reflow before declaring
hierarchy usable. A fixed numeric typography recipe is not a review criterion.
