# Prototyping logic and state

Read when a concrete question about business rules, state transitions, or data
relationships needs a runnable answer rather than visual design alternatives.

1. State the question and accepted limits in the demo. Define the states/actions
   needed to test it, using the project's domain terms. A demo is a model of the
   selected rules, not proof that a remote system behaves identically.
2. Choose the smallest runnable shape the intended reviewer can use. An existing
   sandbox, CLI or notebook may suffice; a self-contained HTML file is useful for
   non-developers clicking through states. No framework or file format is mandatory.
3. Isolate the modeled rules from presentation. Use explicit transitions, a reducer,
   or focused functions as appropriate. Show the relevant current state and expose
   actions with meaningful labels; avoid making raw JSON the only explanation for
   a nontechnical reviewer. Label simulated data and integrations.
4. Offer a reset and repeatable scenarios for the normal path, the disputed edge,
   and an action the agreed model rejects. Permit free exploration where useful;
   illegal actions can be disabled with a reason or rejected without corrupting
   state. Capture unexpected transitions instead of silently changing the policy.
5. Run the scenarios using available project tools. Record initial state, actions,
   observed result, and what that does or does not settle. For persistence or
   concurrency questions, an in-memory single-client demo cannot verify actual
   database or racing-request behavior; use a suitable isolated experiment or
   leave that evidence gap explicit. Avoid live writes for a disposable demo.
6. Return the demo location and the answer or remaining question. Exploration
   authorizes the prototype and its evidence; promoting logic to production,
   retaining a branch, committing, and publishing follow the requested scope.

Keep scaffolding proportional to the question. Reuse sufficient checks; permanent
tests or a reusable prototype platform are not automatic deliverables. Treat
prototype logic as a candidate requiring production integration checks, even if
its local scenarios passed. Preserve unrelated previews and user work.
