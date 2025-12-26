# Synthesis (Employee PM)

## What is clearly decided
- **North star:** Email-first company simulator; async by default; no chat, no real-time presence, no dashboards. AI coworkers behave like imperfect, slow human coworkers who communicate only through email threads. (Context files)
- **System boundary (v0):** Core loop is email ingest → interpret → respond within a thread. Anything beyond receiving, threading, routing, and replying is out of scope. (Employee 01)
- **MVP scope guardrails:** Email-only org setup, hire coworker via email, task assignment via email thread, minimal thread memory, intentional delay, audit trail in email, simple admin commands via email, single LLM provider. Explicit bans: web app UI beyond signup, chat, dashboards, integrations, project management views, real-time presence. (Employee 05)
- **AI behavior model:** Read threads like a human, imperfect understanding is acceptable, delays are intentional, respond only when needed, loop in other coworkers via CC/forward, and make assumptions explicit. (Employee 03)
- **Email/threading model:** Immutable email messages, thread linkage via headers first with subject fallback; forwards default to new thread; internal vs external classification by org domains; rich metadata stored but not shown. (Employee 04)
- **UX framing:** All user-facing interactions are email-native (threads, subject tags, templates). Visibility comes from “work notes” and digest emails, not presence signals. (Employee 02)

## What is still ambiguous
- **Org creation mechanism:** Employee 05 suggests email-based org setup; Employee 01 allows manual/CLI creation. Need a single, explicit v0 path (email-only vs manual bootstrap).
- **Admin controls:** MVP includes email commands (pause/resume/update role), but no spec exists for syntax, authentication, or who can issue commands.
- **Response delay policy:** Employee 03 allows hours-long delays; Employee 05 suggests 5–30 minutes. Need a single, explicit delay policy for v0.
- **UI boundaries:** Employee 02 references “core screens” (Inbox/Thread/Compose) as conceptual email client views, while Employee 05 bans dashboards/web UI. Clarify that these are email-client-native patterns (templates/subjects), not a new web app.
- **External email policy:** Employee 04 defines internal/external handling, but MVP scope doesn’t state whether external recipients are supported in v0.

## What is missing but required to build v0
- **Concrete inbound/outbound email pipeline spec:** transport choice, parsing stack, webhook/inbox provider, bounce handling behaviors aligned to MVP.
- **Prompting and role instruction templates:** defined per-role system instructions, email reply format (incl. Work Notes), and default signatures.
- **Email command grammar:** exact subject/body syntax for hire/pause/resume/role update, and validation rules.
- **Security/auth rules:** who can create an org/hire coworkers, and how sender identity is verified (domain allowlist, reply token, etc.).
- **Minimal storage schema and API surfaces:** how orgs, mailboxes, threads, messages are created and updated at runtime.
- **Test/QA scenarios:** end-to-end email loop, threading edge cases, delay scheduling, and failure handling.

## Contradictions between employees
- **Delay window:** Employee 03’s “respond later (1–24 hours)” conflicts with Employee 05’s “5–30 minutes randomized” MVP delay; needs reconciliation.
- **Org setup:** Employee 05’s email-only setup conflicts with Employee 01’s allowance for admin/CLI creation; must pick one for v0.
- **UI framing risk:** Employee 02’s “core screens” could be misread as a web app; must explicitly constrain to email client conventions to align with Employee 05’s anti-feature list.
