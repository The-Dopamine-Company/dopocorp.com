# Decisions

- Prioritized an email-only MVP with minimal organization setup and tasking to uphold the "email is the UI" north star.
- Explicitly banned any real-time UI, dashboards, and non-email integrations to prevent scope creep.
- Interpreted the single model/provider check as verifying consistent model/provider identifiers across coworker responses when metadata is available.
- Defined demo acceptance criteria that require mocked transport, in-memory storage, explicit delay scheduling, and thread-linked replies to protect the email-only loop.
- Flagged missing email-initiated org creation/hire, scheduled-time logging, and reply format requirements as PASS-blocking gaps in the updated demo design.
- Confirmed the runnable demo script output satisfies all demo acceptance checklist items (PASS across all 10 criteria).
