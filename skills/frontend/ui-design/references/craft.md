# Component craft and spatial clarity

Read only the section relevant to the requested design decision. These principles
support the product's chosen identity; they do not prescribe an Apple-like appearance.

## Coherent defaults

Design the resting state and common interaction as one experience. Defaults should
carry readable hierarchy, predictable feedback, and useful state behavior before
offering customization. Reuse established tokens and primitives. Component APIs
should make the intended use easy without accumulating options for hypothetical needs.

For hierarchy, follow the selected task: locate its next action, distinguish current
state from available actions, and read the required information in the intended order.
If equal emphasis makes these compete, regroup related content or strengthen the
task's priority. Equal weight can be correct for peer choices; size alone is not a
hierarchy defect. Source tokens and screenshots cannot establish user comprehension.

Distinguish acknowledgement from commitment: a press can show immediate feedback
while activation still respects cancellation and control semantics. Deliberate
confirmation must match the action and accessible alternatives, not a universal
hold gesture. Explain consequential outcomes before committing them.

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
