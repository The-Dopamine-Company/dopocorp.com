# v0 Acceptance Checklist (Strict Gate)

## Must-Pass Checks
- **Email-only interface**: All user and coworker interactions happen in email threads. No UI beyond bare signup/landing.
- **Org setup by email**: Users can create/join an org via email and receive an org address.
- **Hire by email**: Users can hire a coworker via email and receive the coworker’s email identity.
- **Task assignment by thread**: Users can assign tasks to coworkers in a thread; coworker replies asynchronously.
- **Thread-local memory only**: Coworkers reference only the active thread; no cross-thread knowledge.
- **Deliberate delays**: Responses are delayed to enforce async behavior.
- **Email audit trail**: Outputs are delivered as email replies/attachments only.
- **Basic email admin commands**: Pause/resume or update role via email commands.
- **Single model/provider**: One LLM backing all coworkers in v0.

## Red-Line Scope Warnings (Auto-Reject)
- **Any non-email primary UI** (dashboard, inbox clone, chat panel).
- **Real-time presence/status** (typing indicators, online status, live updates).
- **Chat or Slack/Teams metaphors**.
- **Project management views** (Kanban, timelines, dashboards).
- **Cross-thread memory, knowledge base, or global context**.
- **Integrations** (GitHub, Notion, Calendar, Zapier) in v0.
- **File collaboration suites** (Docs-style editing or shared workspaces).
- **Multi-org management or billing complexity**.
