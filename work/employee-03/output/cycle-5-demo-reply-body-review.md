# Cycle 5 — Demo Reply Body Review (Employee 03)

## Reference Template
Source: `work/employee-03/output/demo-reply-body-template.md`

Template requirements:
- Opens with a quick acknowledgment line.
- **Work Notes** section with fields:
  - Status
  - Assumptions
  - Blockers
  - Next Step
  - ETA
- **Questions** section with at least two numbered questions.
- Signature in the format:
  - Em dash + name
  - Role line (e.g., `AI Coworker (Role)`)

## Demo Script Reply Body
Source: `work/employee-01/output/demo_loop.py` (function `send_delayed_reply`)

Body used:
```
Work Notes:
- Proposed subject: Welcome to Acme (Getting Started)
- Body: Thanks for joining... (steps 1-3)

-- Sam
```

## Deviations
1. Missing opening acknowledgment line (e.g., “Quick note — …”).
2. **Work Notes** section does not include required fields (Status, Assumptions, Blockers, Next Step, ETA).
3. Missing **Questions** section entirely.
4. Signature format does not include role line (`AI Coworker (Role)`), and uses `-- Sam` instead of the em dash line.

## Conclusion
The demo script reply body does **not** match the v0 demo reply template. It is missing required sections and formatting.
