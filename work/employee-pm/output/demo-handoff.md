# DEMO READY

A runnable demo exists and satisfies the primary objective: a user can create an organization, hire an AI coworker, send a task email, and receive an asynchronous in-thread reply.

## How to run the demo
```bash
python work/employee-01/output/demo_loop.py
```

## What you will see
- Org creation via an email command and a confirmation reply.
- Coworker hire via an email command and a confirmation reply.
- A task email sent to the coworker.
- A scheduled delay before the coworker reply.
- A coworker reply in the same thread with the required Work Notes + signature format.

## Known hacks, limitations, and shortcuts
- Mocked email transport only (no SMTP/IMAP or provider integration).
- In-memory storage for orgs, coworkers, threads, and messages.
- Hardcoded demo email addresses, thread IDs, and content.
- Simulated delay uses a short sleep (1.5s) instead of the real 5–30 minute window.
- No persistence, no auth, no multi-org support, and no UI beyond console logs.

Control is ready to return to the founder.
