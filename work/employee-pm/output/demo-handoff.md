DEMO READY

Run Instructions
1) Start the UI:
   python work/prototype/server.py
2) Open http://localhost:8000
3) Fill in the org creation, coworker hire, and task message fields (defaults provided).
4) Click “Run Demo” to execute the locked demo flow and render outputs.

What you will see
- AI reply content rendered in-page.
- Demo logs with checklist confirmations.
- Thread transcript table showing thread IDs, message IDs, reply headers, and full bodies.

Known Limitations
- In-memory only (no persistence across server restarts).
- Single-session UI; no routing or auth.
- The demo flow is deterministic and runs the fixed sequence defined by the locked engine.

Handing control back to the founder.
