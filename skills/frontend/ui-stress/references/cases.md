# UI stress cases

Read only the section relevant to the selected fields and supported states.
Expected behavior comes from product/consumer contracts, not this example catalog.

## Text and locale

Use realistic long names, short names, unbroken identifiers, translated labels,
multiline content where accepted, diacritics, CJK, and emoji grapheme clusters.
Use reserved example domains for synthetic links or emails.
Check legibility, wrapping, action access, and meaningful identity information.
Initials and truncation rules are product choices, not universal naming formulas.

Exercise RTL or mixed-direction text when relevant; unsupported locales may inform
a proposal but do not automatically establish a current-contract failure.
Display markup-like text through the intended escaping or rich-text boundary,
without executing arbitrary fixture code.

## Relationships under content changes

Vary supported optional fields, translated labels, item states, and container widths.
Check whether settings values stay associated with their labels, plan conditions
with their prices, and order actions with their targets. A missing search-result
field must not make the next value appear to describe a different property.
Wrapping must preserve these associations and the task's information priority.

Compare against a healthy case: a compact author/date row or equally weighted peer
options can remain unchanged when meaning and access survive. Flag a specific lost
relationship, misleading state, or inaccessible action; separator counts, uniform
styling, and density alone do not establish a failure.

## Numbers, collections, and time

Check zero/one and boundaries such as page size and page size plus one.
Use realistic large totals and supported negative, fractional, or precision-sensitive
values. Check localization and units; preserve exact information where the task needs it.
Empty and singleton collections can expose state logic independently of long text.
Use a representative upper bound without turning UI inspection into a load campaign.

For dates, check supported time zones, missing values, past/future boundaries, and
long durations. Freeze or control time through existing fixtures when needed so
the reproduction stays interpretable.

## Media and task states

Exercise missing, failing, slow, and unusual-aspect media where supported. Inspect
fallbacks, reserved space, and required content visibility, not a required CSS literal.
For task flows, check relevant loading, failure/retry, partial data, unavailable
permissions, and completion. A failure must enter through a real supported boundary.

## Investigate a visible break

Trace the affected container and consumer state before prescribing CSS.
Intrinsic sizing, unbreakable text, shrinking siblings, fixed tracks, stale data,
or formatting may explain the symptom. Wrapping, local scrolling, a disclosed
truncation control, or a product fallback can all be valid solutions.
Test the chosen user outcome; do not pin the exact implementation.
