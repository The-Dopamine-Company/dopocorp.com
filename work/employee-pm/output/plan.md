# Execution Plan (Employee PM)

## Plan principles
- Keep v0 strictly email-only.
- Each task outputs a concrete, written artifact in the assignee’s `output/` folder.
- Prefer parallel work; avoid overlap and premature optimization.

## Tasks

### Task 1 — Email pipeline spec (Employee 04 — Email System Engineer)
- **Objective:** Turn threading/data model into an executable inbound/outbound pipeline spec (transport choices, parsing steps, delivery flow, bounce handling).
- **Expected output:** `work/employee-04/output/email-pipeline-spec.md`
- **Notes:** Must align with threading rules already documented and MVP constraints (no dashboards).

### Task 2 — AI coworker response template + delay policy (Employee 03 — AI Behavior Lead)
- **Objective:** Define a concrete v0 response format (subject prefixes, Work Notes section, signatures) and a reconciled delay policy (single delay window).
- **Expected output:** `work/employee-03/output/response-format-and-delay.md`
- **Notes:** Use the existing behavior policy and examples; keep delays human-like but deterministic enough for MVP.

### Task 3 — Email command grammar (Employee 01 — Founding Engineer)
- **Objective:** Specify the exact email command syntax for org creation, hire coworker, pause/resume, and role update. Include validation/auth assumptions.
- **Expected output:** `work/employee-01/output/email-command-spec.md`
- **Notes:** Must be email-only; clarify any bootstrap path.

### Task 4 — Email-native UX templates (Employee 02 — Product Designer)
- **Objective:** Convert core UX concepts into email templates (compose/assign, hire confirmation, digest, clarification request).
- **Expected output:** `work/employee-02/output/email-templates-v0.md`
- **Notes:** No web UI; templates must live fully inside email bodies/subjects.

### Task 5 — MVP acceptance checklist (Employee 05 — MVP Scope Police)
- **Objective:** Create a concise v0 acceptance checklist + red-line scope warnings to validate against build work.
- **Expected output:** `work/employee-05/output/v0-acceptance-checklist.md`
- **Notes:** Should explicitly call out anything that would violate “email is the UI.”
