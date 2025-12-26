# Founder Guidance

## What you should do next
- Decide the **org creation bootstrap path** for v0 (email-only self-serve vs manual/admin creation).
- Choose a **single response delay policy** (minutes vs hours) so implementation is consistent.
- Confirm whether **external email** (non-org domains) is in scope for v0.

## Decisions blocked on you
- **Auth/verification model:** how to validate who can issue admin commands via email.
- **Email infrastructure choice:** provider for inbound/outbound (e.g., SMTP vs API-based). This affects pipeline design.
- **Tone/brand constraints:** how “human” and playful the AI should be (to reconcile “boring is good” with light delight).

## What you should NOT think about yet
- Integrations, dashboards, analytics, multi-org management, or performance optimization.
- Cross-thread memory or knowledge bases.
- Billing or pricing complexity.

## Risks if execution continues unchecked
- **Scope creep** into web UI or status dashboards, violating “email is the UI.”
- **Inconsistent behavior** if delay policy and admin command syntax are not decided early.
- **Security ambiguity** around who can command AI coworkers via email.
