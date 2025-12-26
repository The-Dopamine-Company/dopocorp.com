# Demo Acceptance Checklist (Mocked Transport Path)

## Scope
This checklist validates the runnable demo that uses mocked email transport, in-memory storage, and a delay scheduler. It ensures the full loop works end-to-end: create org → hire coworker → send task email → schedule delayed reply → send reply in same thread.

## Acceptance Checklist (Pass/Fail)

### 1) Organization Creation (Email-Initiated)
- **Pass**: Demo accepts a single email command that creates an org and produces a confirmation email reply.
- **Fail**: Org creation requires UI clicks, dashboards, or out-of-band APIs.

### 2) Coworker Hire (Email-Initiated)
- **Pass**: Demo accepts a hire coworker email and returns a confirmation reply that includes coworker name + role.
- **Fail**: Coworker is created via config file edits or web UI only.

### 3) Task Assignment Email (Threaded)
- **Pass**: A task email to the coworker is accepted and stored with a thread identifier.
- **Fail**: Task assignment is handled outside an email thread or without thread linkage.

### 4) Delayed Reply Scheduling
- **Pass**: The system schedules a reply with a non-zero delay (simulated timer or queued job) and logs/surfaces the scheduled time.
- **Fail**: Reply is sent immediately or delay is skipped.

### 5) Reply Sent in Same Thread
- **Pass**: The coworker reply is sent with the same thread identifier and references the original subject (e.g., “Re: …”).
- **Fail**: Reply is sent as a new thread or lacks subject continuity.

### 6) Required Reply Format (Demo Format)
- **Pass**: Reply includes subject prefix + “Work Notes” section + coworker signature (per demo prompt template).
- **Fail**: Reply omits the required format or is free-form.

### 7) In-Memory Storage Path
- **Pass**: Demo uses in-memory storage for orgs, coworkers, and emails (no DB required).
- **Fail**: Demo requires external DB setup to run.

### 8) Mocked Email Transport Path
- **Pass**: All email send/receive operations are routed through the mocked transport layer (queue + scheduler).
- **Fail**: Real SMTP/IMAP dependencies are required for the demo to run.

### 9) Deterministic Demo Script
- **Pass**: A documented local run path produces the full sequence in a predictable order.
- **Fail**: Demo depends on manual, ad-hoc steps not captured in run instructions.

### 10) Logging/Traceability
- **Pass**: Console or log output shows key events: org created, coworker hired, task received, reply scheduled, reply sent.
- **Fail**: No observable trace of state transitions.

## Red-Line Scope Violations (Do Not Include)
- Any real-time UI, web dashboard, or chat UX.
- Live email server integration (SMTP/IMAP) or third-party mail providers.
- Multi-user permissions, auth flows, or user management.
- Persistent storage setup (databases, migrations, etc.).
- Any non-email task creation surface (forms, REST endpoints used as primary UI).
- Slack/Teams/Discord metaphors, presence indicators, or real-time collaboration features.

## Notes
- The demo is **email-only**. If a UI exists, it must be strictly optional and not required for any pass criteria.
- Delays can be simulated, but the delay must be explicit and observable.
