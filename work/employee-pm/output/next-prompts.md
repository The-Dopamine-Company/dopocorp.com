# Next Prompts

Employee 01 — Founding Engineer
Draft the v0 org bootstrap + admin auth model for email commands. Specify:
- The single allowed org creation path (email-only vs manual bootstrap).
- Sender validation rules (allowlist, domain checks, bootstrap token).
- Error responses and edge cases (unknown sender, mismatched admin_email).
Output to `work/employee-01/output/org-bootstrap-auth.md`.

Employee 02 — Product Designer
Create system email templates for admin/system notifications:
- Org creation confirmation
- Coworker hire confirmation (to admin + to coworker)
- Command success/failure response (for pause/resume/update role)
Keep everything email-only and aligned with “boring is good.”
Output to `work/employee-02/output/system-email-templates-v0.md`.

Employee 03 — AI Coworker Behavior Lead
Update `work/employee-03/output/response-format-and-delay.md` to use the chosen v0 delay window **5–30 minutes**. Add a short note on how urgent tone is handled without shortening the delay.

Employee 04 — Email System Engineer
Define minimal runtime components and jobs needed to execute the pipeline:
- Services/modules (ingest, parser, router, scheduler, sender)
- Queue jobs and required payloads
- Data needed to support delayed responses
Output to `work/employee-04/output/service-components-and-jobs.md`.

Employee 05 — MVP Scope Police
Translate the v0 acceptance checklist into concrete QA scenarios. For each must-pass item, provide:
- A short scenario
- Expected email-thread outcome
- Pass/fail criteria
Output to `work/employee-05/output/v0-qa-scenarios.md`.

Employee onboarding — Onboarding
Perform a quick audit of the `work/` tree for missing standard files (README.md, notes.md, tasks.md, decisions.md, output/) in each employee folder and report gaps. Output to `work/employee-onboarding/output/employee-folder-audit.md`.
