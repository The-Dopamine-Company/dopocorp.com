# System Boundary Spec (Minimum Viable)

## Purpose
Enable a user to create an organization, hire an AI coworker, and assign a task via email. The coworker replies in the same email thread with a basic deliverable.

## In-Scope (Minimum System)
- Inbound email ingestion for a single organization domain (or a shared inbound address)
- Thread identification and message storage
- Organization + coworker creation (admin-only, manual or simple CLI ok)
- Task assignment via email to a coworker address
- AI coworker generates a response and replies into the same thread
- Basic audit trail (who sent what, when)

## Out of Scope (For Now)
- UI/dashboard or real-time interfaces
- Multi-tenant scaling, quotas, rate limits
- Complex permissions, roles, or HR workflows
- Real-time presence, chat, or Slack-like constructs
- Scheduling, reminders, or project management features

## System Boundary
The system is an email-driven task loop: ingest → interpret → respond. Anything not required to receive an email, map it to a coworker, and send a reply is out of scope.

---

# Minimal Entity List

1. **Organization**
   - id, name
   - inbound_email (or org email alias)

2. **Coworker**
   - id, organization_id
   - role_title, email_alias
   - model_config (simple: model_name)

3. **Thread**
   - id, organization_id
   - external_thread_id (email thread/Message-Id linkage)

4. **Message**
   - id, thread_id
   - sender (user or coworker)
   - body, timestamp
   - direction (inbound/outbound)

---

# “Hello World” End-to-End Flow

1. Admin creates an **Organization** and a single **Coworker** (role: “Engineer”, email alias: engineer@org.example).
2. User sends an email to engineer@org.example with a simple task (e.g., “Write a 3-bullet summary of today’s goals”).
3. System ingests the email, creates/updates the **Thread**, stores the inbound **Message**, and routes to the coworker.
4. Coworker generates a short reply and the system sends it back into the same email thread.
5. The thread now contains both the user’s request and the coworker’s response, proving the loop works.
