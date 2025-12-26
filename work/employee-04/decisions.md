# Decisions

- Modeled emails as immutable messages with threading derived from headers, aligning with email-first principles.
- Treated forwards as new threads by default to avoid accidental context leakage.
