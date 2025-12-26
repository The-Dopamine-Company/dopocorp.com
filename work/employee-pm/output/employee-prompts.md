# Employee Prompts

Employee 04 — Email System Engineer
You already documented the threading rules and data model in `work/employee-04/output/email-system-design.md`. Build on that by writing an executable inbound/outbound email pipeline spec for v0. Include: transport choices, parsing steps, threading flow, storage writes, delivery flow, bounce handling, and failure paths. Keep it email-only and aligned to MVP scope. Output to `work/employee-04/output/email-pipeline-spec.md`.

Employee 03 — AI Coworker Behavior Lead
You defined behavior policy and examples in `work/employee-03/output/behavior-spec.md` and `work/employee-03/output/email-examples.md`. Now produce a concrete v0 response format and a single delay policy. Specify: subject prefixes, required “Work Notes” section fields, tone constraints, signatures, and a deterministic delay window (reconcile the 5–30 min vs 1–24h conflict). Output to `work/employee-03/output/response-format-and-delay.md`.

Employee 01 — Founding Engineer
You set the system boundary and core entities in `work/employee-01/output/system-boundary.md`. Draft the email command grammar for v0: org creation, hire coworker, pause/resume coworker, update role. Include sender validation/auth assumptions and any bootstrap path. Keep everything email-only and aligned to the MVP anti-features. Output to `work/employee-01/output/email-command-spec.md`.

Employee 02 — Product Designer
You outlined email-native UX in `work/employee-02/output/employee-02-ux.md`. Convert those concepts into concrete email templates (subject + body) for: task assignment, hire confirmation, clarification request, progress update, and digest. Keep all interaction inside email, no web UI. Output to `work/employee-02/output/email-templates-v0.md`.

Employee 05 — MVP Scope Police
You delivered scope guardrails in `work/employee-05/output/mvp-scope-police.md`. Create a v0 acceptance checklist and red-line scope warnings that can be used to gate build decisions. Keep it short and strict. Output to `work/employee-05/output/v0-acceptance-checklist.md`.
