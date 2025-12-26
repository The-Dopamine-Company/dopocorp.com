# Decisions

- Kept the system boundary limited to the email task loop (ingest → interpret → respond) to align with “email is the UI” and avoid feature creep.
- For v0 email command auth, assumed allowlist-first with optional bootstrap token to avoid any UI-based setup.
- Org creation is email-only, gated by sender allowlist or one-time bootstrap tokens tied to the admin email.
- Implemented the demo loop as a self-contained Python script inside the employee output folder to avoid writing outside `work/` while still being runnable.
- Used a simple sleep-based scheduler to model delayed replies without external dependencies.
- 2025-12-26: Added explicit email command ingestion and checklist-step logging in the demo loop to mirror acceptance criteria while keeping mocked transport and in-memory storage.
- 2025-12-26: Verified demo script output includes checklist steps 1–10; no changes required.
