# Employee 05 — MVP Scope Police

## MVP Feature List (Must Exist in v0)

1. **Email-only org setup**
   - User emails a system address to create an org (or replies to an invite email).
   - Confirmation email returns a unique org address.

2. **Hire AI coworker via email**
   - User emails "hire" request (role + name) to org address.
   - System replies with coworker email identity and role summary.

3. **Assign tasks by email thread**
   - User emails coworker with a task; system replies acknowledging receipt.
   - Coworker responds asynchronously with progress + questions.

4. **Thread memory (minimal)**
   - Coworker can reference earlier messages in the same thread.
   - No cross-thread knowledge in v0.

5. **Simple scheduling delay**
   - Responses are intentionally delayed (e.g., 5–30 minutes randomized) to reinforce async.

6. **Audit trail in email**
   - All outputs are delivered as email replies or attachments.
   - No dashboard, no inbox cloning, no web UI beyond signup.

7. **Basic admin controls (email commands)**
   - Email commands to pause/stop a coworker or change role.

8. **Single model / single provider**
   - One LLM backing all coworkers. Keep infrastructure minimal.

---

## Anti-Feature List (Explicitly Banned from v0)

- **No web app UI** beyond a bare signup/landing page.
- **No chat, Slack, Discord, or in-app messaging.**
- **No real-time presence indicators, typing indicators, or status dashboards.**
- **No multi-agent orchestration UI** (coworkers may loop in others only via email).
- **No project management views** (Kanban, timelines, dashboards).
- **No file editing suites** (Google Docs-style collaboration, shared workspaces).
- **No integrations** (Zapier, GitHub, Notion, Calendar) in v0.
- **No analytics beyond basic email logs** (no charts, no KPIs).
- **No multi-org management** (one org per account).
- **No billing complexity** (no plans, trials, metered billing) — just manual access.

---

## Good-Sounding Features That Violate the North Star

1. **Slack-style chat with AI coworkers**
   - Violates: "Email is the UI" and async-first.

2. **Realtime "AI coworker status" page**
   - Violates: "Visibility through work, not status." Adds presence mechanics.

3. **Collaborative web workspace**
   - Violates: email-only premise; becomes a productivity tool.

4. **Cross-thread memory / knowledge base**
   - Sounds smart, but shifts product toward a tool, not a coworker. Adds scope.

5. **Automatic task tracking / Kanban**
   - Violates "boring is good" and adds management UI complexity.

6. **Live co-editing docs**
   - Shifts to real-time collaboration; breaks async-by-default.

7. **Automatic integrations (GitHub, Notion, Calendar)**
   - Implies real-time workflows and removes email as the sole interface.

---

## 2-Week Execution Plan (Solo Founder + Codex)

### Week 1 — Prove the Email Loop
- **Day 1–2:** Set up inbound email processing.
  - Parse threads and route messages to org inbox.
- **Day 3–4:** Implement "hire coworker" flow via email.
  - Create coworker identities + basic role instructions.
- **Day 5–6:** Implement task assignment + delayed responses.
  - Coworker replies with acknowledgement + first questions.
- **Day 7:** Manual QA with real email accounts.
  - Validate thread continuity + delay behavior.

### Week 2 — Shipable MVP
- **Day 8–9:** Add minimal admin commands via email.
  - pause/resume coworker; update role instructions.
- **Day 10–11:** Harden deliverables.
  - Ensure outputs are only via email.
- **Day 12:** Polish onboarding emails.
  - Make them clear, human, and minimal.
- **Day 13–14:** Launch private alpha.
  - 3–5 users max, collect email-thread feedback.

---

### Ruthless Scope Guardrails
- If it can’t be done entirely through email, it doesn’t ship.
- If it reduces the "human coworker" illusion, it is removed.
- If it requires a dashboard, it is not in v0.
- If it creates real-time expectations, it is banned.
