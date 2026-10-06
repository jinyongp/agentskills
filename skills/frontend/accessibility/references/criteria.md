# Accessibility criteria

Read only the applicable section when measuring or resolving a standards question.
The selected standard governs; these notes summarize WCAG 2.2 AA checks and link
to their explanations. Consult the criterion's applicability and exceptions.

## Contrast

For SC 1.4.3, applicable normal text needs at least 4.5:1; large text needs 3:1.
Large means at least 18pt (24 CSS px), or 14pt bold (about 18.67 CSS px), including
equivalent sizes for applicable scripts. An 18px regular label is not large text.
Classify the unrounded ratio: 4.499:1 fails 4.5:1 even if the display rounds to 4.50.
Account for rendered compositing and relevant background variations. Inactive,
incidental, decorative, and logo text have specified exceptions.
See [Text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

SC 1.4.11 generally requires 3:1 for visual information needed to identify active
controls/states and understand graphics against adjacent colors, with exceptions.
It does not require every decorative border to contrast.
See [Non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

## Enlargement and reflow

SC 1.4.4 requires applicable text to enlarge to 200% without losing content or
functionality. Check labels and controls too; CSS units alone do not determine success.
See [Resize text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html).

SC 1.4.10 checks reflow without two-dimensional scrolling at 320 CSS px width for
vertically scrolling content, or 256 CSS px height for horizontally scrolling content.
Content requiring two dimensions, such as some tables and diagrams, has an exception;
keep the surrounding content usable.
See [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

## Targets and focus

SC 2.5.8 uses 24 by 24 CSS px or its spacing condition, with exceptions for inline,
equivalent, user-agent-controlled, and essential targets. A 44px target may be a
useful recommendation; it is not the universal AA minimum.
See [Target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

SC 2.4.11 requires a focused component not be entirely hidden by author-created
content. Keeping it fully visible is preferable; distinguish that recommendation
from the AA minimum.
See [Focus not obscured](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

For custom widget semantics and keyboard patterns, consult only the relevant
[ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)
guidance. Prefer native semantics and verify actual interaction; example code is
not a conformance guarantee.
