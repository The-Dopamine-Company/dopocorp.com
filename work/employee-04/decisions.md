# Decisions

- Modeled emails as immutable messages with threading derived from headers, aligning with email-first principles.
- Treated forwards as new threads by default to avoid accidental context leakage.
- Specified a single managed SMTP provider for inbound webhook + outbound relay in v0 to simplify deliverability and ops.
