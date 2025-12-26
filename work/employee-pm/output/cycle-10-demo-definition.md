# Cycle 10 Demo Definition — UI Wrap

## How to start the demo

```bash
python work/prototype/server.py
```

Then open: http://localhost:8000

## What the user does

1. **Org creation**: Enter org name, admin email, and org thread ID.
2. **Coworker hire**: Enter coworker ID, name, role, email, and hire thread ID.
3. **User message send**: Enter task subject/body and task thread ID.
4. Click **Run Demo**.

## What the user sees

- **AI Reply**: The coworker reply content is rendered with subject and body.
- **Demo Logs**: Checklist steps confirming org creation, coworker hire, task assignment, delay scheduling, and reply.
- **Thread Transcript**: A table listing each message with thread IDs, message IDs, subject lines, reply threading fields, and full body content.

## Demo flow summary

- The UI submits inputs to the locked demo engine logic.
- The engine runs the standard sequence: org creation → coworker hire → task message → delayed reply.
- Outputs are rendered directly on the page (not just the console).
