# Selection questions

Read the section matching the capability gap, not an entire library catalog.

## Interactive primitives

For dialogs, menus, selects, or command surfaces, check keyboard behavior, focus,
dismissal, semantic state, portals, and supported input methods. Confirm the wrapper
or customization preserves these capabilities. A library's accessibility claim is
evidence to investigate, not proof that every integration is accessible.

## Motion, large data, and visuals

Simple transitions can use platform primitives. Gestures, interruption, presence,
or shared geometry may justify an existing controller. Verify supported targets
and reduced-motion paths rather than picking an engine from a fixed preference list.

For tables or lists, use actual data scale and measured rendering needs. Pagination
and virtualization solve different tasks; check semantics, focus, variable sizes,
and SSR where required. A chart choice follows the user's analytical task, data
update rate, and accessible alternatives, not merely an attractive example.

## Framework and rendering boundaries

Confirm framework/runtime support, peer dependencies, module formats, styling,
SSR/hydration, islands, and native builds as applicable. A React package cannot be
assumed to work in a non-React component. A React island can be deliberate when
authorized; its serialization and ownership costs remain part of the decision.

## Adoption cost

Inspect the public API, release notes, license, dependency footprint, and unresolved
issues relevant to the required behavior. Prefer primary evidence and scope claims
to inspected versions. A popularity score or last-commit date alone is insufficient.
Check the migration effort, theming surface, and ability to replace the dependency.

A compact comparison can list candidate, constraint fit, integration cost, risk, and
reason to choose it. Use only columns that change the decision. If evidence is absent,
state the gap and propose the smallest proof rather than inventing compatibility.
