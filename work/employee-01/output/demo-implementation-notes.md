# Demo Implementation Notes (Employee 01)

## What this covers
- Create org → hire coworker → send task email → schedule delayed reply → send reply in same thread.
- Uses a mocked email transport and in-memory storage only.
- Scheduler is a simple in-process delay queue to simulate async reply.

## Files
- `work/employee-01/output/demo_loop.py`

## How to run
```bash
python work/employee-01/output/demo_loop.py
```

Expected output includes:
- Logs for org creation and coworker hire
- A task email sent on `thread-1001`
- A delayed reply in the same thread
- A printed transcript of the thread
