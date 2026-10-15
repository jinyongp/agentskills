# Suggest useful cases

Use for test-idea requests or when identifying meaningful uncovered behavior.
Ideas-only scope writes no test code and runs no application/test commands solely
because they are available. Keep candidate expectations independent of generated
implementation; read code to locate surfaces, not to define the intended policy.

1. Establish the accepted behavior and inspect relevant existing coverage across
   files and layers. Note whether coverage is complete, partial, or unknown;
   uncertainty does not establish an uncovered defect.
2. Consider only dimensions with distinct failure mechanisms: absent or empty
   input/state; one/common operation; multiple items, ordering, or concurrent
   operations; justified limits and transitions; public interface compatibility;
   invalid input, external failure, expiration, access, and recovery.
3. Select specific cases supported by requirements, independently checked examples,
   or public contracts. A column size or current timeout is useful investigation
   evidence but not automatically the correct product limit. Resolve materially
   uncertain expectations before treating them as assertions.
4. Skip adequately covered behavior. For partial coverage name the missing contract
   observation, and for unknown coverage name the needed inspection. Do not demand
   tests in every dimension or repeat a case across layers without another failure
   it can detect.
5. Give each idea a trigger, expected observable result, the distinct failure it
   protects, and a suitable stable boundary. Match the requested detail; no
   incidental helper names, mock-call order, or factory recipe is required.

Return prioritized candidates and material expectation/coverage gaps. A legitimate
outcome is no useful additions. Suggestions are not implemented tests or evidence
that the current implementation passes them.
