Employee UI — Demo Interface Builder

Objective
- Wrap the locked demo engine with a minimal, local-only single-page UI that can trigger the demo flow and render visible outputs.

Constraints
- Single page, no routing, no auth, no persistence.
- No styling beyond readability.
- UI must expose: org creation, coworker hire, user message send, AI reply display, thread continuity fields.
- Use the existing demo engine as source of truth; do not redesign logic.

Deliverables
- A runnable UI entrypoint under work/prototype/.
- Clear run instructions in README or top-level comments.
- Visible output rendering (logs + thread transcript + AI reply content).

Notes
- Hardcode glue if needed; duplicate engine code if faster.
- Keep all changes contained to work/prototype/.
