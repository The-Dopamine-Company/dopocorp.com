# Decisions

- Modeled emails as immutable messages with threading derived from headers, aligning with email-first principles.
- Treated forwards as new threads by default to avoid accidental context leakage.
- Specified a single managed SMTP provider for inbound webhook + outbound relay in v0 to simplify deliverability and ops.
- Chose a minimal five-service pipeline (ingest, parser, router, scheduler, sender) with explicit queue jobs and idempotency keys to support delayed responses.
- For the demo, standardized on an in-memory transport + scheduler with explicit thread linkage fields (`threadId`, `inReplyTo`, `references`) to keep the reply in the same thread.
