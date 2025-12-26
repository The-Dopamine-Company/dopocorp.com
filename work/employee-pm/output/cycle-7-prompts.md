Employee 01 — Founding Engineer
Update `work/employee-01/output/demo_loop.py` so demo outputs match the demo templates and logging requirements. Specifically:
- Replace org creation and coworker hire confirmations with the templates in `work/employee-02/output/demo-confirmation-templates.md` (subject + labeled sections).
- Replace coworker reply body with the template in `work/employee-03/output/demo-reply-body-template.md` (acknowledgment, Work Notes fields, Questions, signature format).
- Add transport logging for `thread_id`, `message_id`, `in_reply_to`, and `references` per `work/employee-04/output/thread-continuity-log-fields.md`.
- Keep the script deterministic and runnable from a single entrypoint.
- Run `python work/employee-01/output/demo_loop.py` and note output highlights in a short review file under `work/employee-01/output/`.

Employee 02 — Product Designer
Provide a minimal “demo-safe” variant of the org creation and coworker hire confirmation templates that preserves labeled sections but trims optional copy (to reduce script changes). Save as `work/employee-02/output/cycle-7-confirmation-templates-min.md`.

Employee 03 — AI Coworker Behavior Lead
Provide a minimal coworker reply body variant that still meets v0 format requirements (acknowledgment, Work Notes with required fields, Questions, signature). Save as `work/employee-03/output/cycle-7-demo-reply-body-min.md`.

Employee 04 — Email System Engineer
Provide a concrete one-line logging format example that includes required thread continuity fields and a short checklist to verify it in the demo output. Save as `work/employee-04/output/cycle-7-logging-format.md`.

Employee 05 — MVP Scope Police
After demo updates land, re-run the demo acceptance checklist against `python work/employee-01/output/demo_loop.py` and record PASS/FAIL with evidence in `work/employee-05/output/cycle-7-demo-acceptance-rerun.md`.

