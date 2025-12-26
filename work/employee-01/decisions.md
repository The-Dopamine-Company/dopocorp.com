# Decisions

- Kept the system boundary limited to the email task loop (ingest → interpret → respond) to align with “email is the UI” and avoid feature creep.
- For v0 email command auth, assumed allowlist-first with optional bootstrap token to avoid any UI-based setup.
- Org creation is email-only, gated by sender allowlist or one-time bootstrap tokens tied to the admin email.
