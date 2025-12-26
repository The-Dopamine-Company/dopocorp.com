# Cycle 7 Demo Loop Review

Command:
- `python work/employee-01/output/demo_loop.py`

Output highlights:
- Confirmation templates emitted with labeled sections and [Dopo] subjects for org creation and coworker hire.
- Transport logs include `thread`, `msg`, `in-reply-to`, and `refs` fields for each message.
- Coworker reply body uses the v0 template with acknowledgment, Work Notes fields, Questions, and signature.
- Checklist steps 1–10 appear in order through the run.

Sample log lines:
- `[transport] thread=thread-org-1001 msg=thread-org-1001-msg-002 in-reply-to=thread-org-1001-msg-001 refs=thread-org-1001-msg-001 subject="[Dopo] Organization created: Acme"`
- `[transport] thread=thread-task-1003 msg=thread-task-1003-msg-002 in-reply-to=thread-task-1003-msg-001 refs=thread-task-1003-msg-001 subject="Re: Task: Draft onboarding email flow"`
