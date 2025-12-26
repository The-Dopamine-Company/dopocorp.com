from __future__ import annotations

import html
import sys
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List, Tuple
from urllib.parse import parse_qs

sys.path.append("/workspace/dopocorp.com/work/employee-01/output")

from demo_loop import InMemoryStore, MockEmailTransport, Scheduler  # noqa: E402


@dataclass
class DemoInputs:
    org_name: str
    admin_email: str
    org_thread_id: str
    coworker_id: str
    coworker_name: str
    coworker_role: str
    coworker_email: str
    hire_thread_id: str
    task_subject: str
    task_body: str
    task_thread_id: str
    requester_name: str
    timestamp: str


@dataclass
class DemoResult:
    logs: List[str]
    messages: List[Dict[str, str]]
    ai_reply: Dict[str, str] | None


DEFAULT_INPUTS = DemoInputs(
    org_name="Acme",
    admin_email="admin@acme.test",
    org_thread_id="thread-org-1001",
    coworker_id="cw-01",
    coworker_name="Sam",
    coworker_role="Engineer",
    coworker_email="sam@acme.test",
    hire_thread_id="thread-hire-1002",
    task_subject="Task: Draft onboarding email flow",
    task_body=(
        "Please draft the onboarding email flow for new orgs. "
        "Include subject + body for the first message."
    ),
    task_thread_id="thread-task-1003",
    requester_name="Admin",
    timestamp="2025-12-26 09:00 UTC",
)


def parse_command(body: str) -> Tuple[str, Dict[str, str]]:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    command = lines[0].upper() if lines else ""
    fields: Dict[str, str] = {}
    for line in lines[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = value.strip()
    return command, fields


def run_demo(inputs: DemoInputs) -> DemoResult:
    store = InMemoryStore()
    transport = MockEmailTransport(store=store)
    scheduler = Scheduler()

    logs: List[str] = []
    current_org_id = ""

    def log(message: str) -> None:
        logs.append(message)

    def log_checklist(step: int, message: str) -> None:
        log(f"[checklist {step}] {message}")

    def handle_command_email(*, from_addr: str, body: str, thread_id: str) -> None:
        nonlocal current_org_id
        command, fields = parse_command(body)
        if command == "CREATE ORG":
            org_name = fields.get("name", inputs.org_name)
            org_id = f"org-{org_name.lower().replace(' ', '-')}"
            admin = fields.get("admin_email", from_addr)
            store.create_org(org_id, org_name, admin)
            current_org_id = org_id
            log_checklist(1, f"Org created via email command ({org_name}).")
            org_confirmation_subject = f"[Dopo] Organization created: {org_name}"
            org_confirmation_body = (
                f"Hello {inputs.requester_name},\n\n"
                "Your organization has been created.\n\n"
                "**Organization**\n"
                f"- Name: {org_name}\n"
                f"- Org ID: {org_id}\n\n"
                "**Owner**\n"
                f"- Name: {inputs.requester_name}\n"
                f"- Email: {admin}\n\n"
                "**Status**\n"
                "- Result: Created\n"
                f"- Timestamp: {inputs.timestamp}\n\n"
                'If you want to hire coworkers, reply with: “Hire Engineer named Sam.”\n\n'
                "—Dopo System"
            )
            transport.send_email(
                from_addr="control@dopocorp.test",
                to_addr=admin,
                subject=org_confirmation_subject,
                body=org_confirmation_body,
                thread_id=thread_id,
            )
        elif command == "HIRE COWORKER":
            name = fields.get("name", inputs.coworker_name)
            role = fields.get("role", inputs.coworker_role)
            email_alias = fields.get("email_alias", inputs.coworker_email)
            coworker_key = fields.get("coworker_id", inputs.coworker_id)
            store.hire_coworker(coworker_key, name, role, email_alias)
            log_checklist(2, f"Coworker hired via email command ({name}, {role}).")
            org_id = current_org_id or "org-unknown"
            org_name = store.orgs.get(org_id, {}).get("name", inputs.org_name)
            hire_confirmation_subject = f"[Dopo] Coworker hired: {name} ({role})"
            hire_confirmation_body = (
                f"Hello {inputs.requester_name},\n\n"
                f"Your coworker has been added to {org_name}.\n\n"
                "**Coworker**\n"
                f"- Name: {name}\n"
                f"- Role: {role}\n"
                f"- Coworker ID: {coworker_key}\n\n"
                "**Organization**\n"
                f"- Name: {org_name}\n"
                f"- Org ID: {org_id}\n\n"
                "**Status**\n"
                "- Result: Hired\n"
                f"- Timestamp: {inputs.timestamp}\n\n"
                f"To assign work, reply with: “Task for {name}: Draft onboarding email flow.”\n\n"
                "—Dopo System"
            )
            transport.send_email(
                from_addr="control@dopocorp.test",
                to_addr=from_addr,
                subject=hire_confirmation_subject,
                body=hire_confirmation_body,
                thread_id=thread_id,
            )
        else:
            transport.send_email(
                from_addr="control@dopocorp.test",
                to_addr=from_addr,
                subject=f"Re: {command or 'UNKNOWN COMMAND'}",
                body="ERROR\nreason: unknown_command",
                thread_id=thread_id,
            )

    log_checklist(7, "Using in-memory storage for orgs, coworkers, and threads.")
    log_checklist(8, "Using mocked email transport for send/receive.")
    log_checklist(9, "Demo script runs deterministically from a single entrypoint.")

    org_command_body = (
        "CREATE ORG\n"
        f"name: {inputs.org_name}\n"
        f"admin_email: {inputs.admin_email}\n"
    )
    transport.send_email(
        from_addr=inputs.admin_email,
        to_addr="control@dopocorp.test",
        subject="CREATE ORG",
        body=org_command_body,
        thread_id=inputs.org_thread_id,
    )
    handle_command_email(
        from_addr=inputs.admin_email,
        body=org_command_body,
        thread_id=inputs.org_thread_id,
    )

    hire_command_body = (
        "HIRE COWORKER\n"
        f"coworker_id: {inputs.coworker_id}\n"
        f"name: {inputs.coworker_name}\n"
        f"role: {inputs.coworker_role}\n"
        f"email_alias: {inputs.coworker_email}\n"
    )
    transport.send_email(
        from_addr=inputs.admin_email,
        to_addr="control@dopocorp.test",
        subject="HIRE COWORKER",
        body=hire_command_body,
        thread_id=inputs.hire_thread_id,
    )
    handle_command_email(
        from_addr=inputs.admin_email,
        body=hire_command_body,
        thread_id=inputs.hire_thread_id,
    )

    transport.send_email(
        from_addr=inputs.admin_email,
        to_addr=inputs.coworker_email,
        subject=inputs.task_subject,
        body=inputs.task_body,
        thread_id=inputs.task_thread_id,
    )
    log_checklist(3, "Task assignment email stored with thread identifier.")

    def send_delayed_reply() -> None:
        transport.send_email(
            from_addr=inputs.coworker_email,
            to_addr=inputs.admin_email,
            subject=f"Re: {inputs.task_subject}",
            body=(
                "Quick note — I can take the first pass on this and will follow up if I hit any gaps.\n\n"
                "**Work Notes**\n"
                "- **Status:** In progress\n"
                "- **Assumptions:** None\n"
                "- **Blockers:** None\n"
                "- **Next Step:** Draft the initial outline and share a short update\n"
                "- **ETA:** Later today\n\n"
                "**Questions**\n"
                "1) Is there a preferred deadline I should aim for?\n"
                "2) Any examples or references I should mirror?\n\n"
                f"— {inputs.coworker_name}\n"
                f"AI Coworker ({inputs.coworker_role})"
            ),
            thread_id=inputs.task_thread_id,
        )
        log_checklist(5, "Reply sent in the same thread with Re: subject.")
        log_checklist(6, "Reply includes Work Notes section and signature.")

    delay_seconds = 1.5
    scheduler.schedule(delay_seconds, send_delayed_reply)
    log_checklist(4, f"Reply scheduled with {delay_seconds:.1f}s delay.")
    scheduler.run()

    log_checklist(10, "Console output includes key state transitions.")

    messages: List[Dict[str, str]] = []
    for thread in store.threads.values():
        messages.extend(thread.messages)

    ai_reply = next(
        (
            message
            for message in reversed(messages)
            if message["from"] == inputs.coworker_email
        ),
        None,
    )

    return DemoResult(logs=logs, messages=messages, ai_reply=ai_reply)


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def render_page(inputs: DemoInputs, result: DemoResult | None) -> str:
    ai_reply_html = ""
    if result and result.ai_reply:
        reply = result.ai_reply
        ai_reply_html = (
            "<section>"
            "<h2>AI Reply</h2>"
            f"<p><strong>From:</strong> {escape(reply['from'])}</p>"
            f"<p><strong>Subject:</strong> {escape(reply['subject'])}</p>"
            f"<pre>{escape(reply['body'])}</pre>"
            "</section>"
        )

    logs_html = ""
    transcript_html = ""
    if result:
        logs_html = "<pre>" + "\n".join(escape(line) for line in result.logs) + "</pre>"
        rows = []
        for message in result.messages:
            rows.append(
                "<tr>"
                f"<td>{escape(message['thread_id'])}</td>"
                f"<td>{escape(message['message_id'])}</td>"
                f"<td>{escape(message['from'])}</td>"
                f"<td>{escape(message['to'])}</td>"
                f"<td>{escape(message['subject'])}</td>"
                f"<td>{escape(message['in_reply_to'] or '-')}</td>"
                f"<td>{escape(message['references'] or '-')}</td>"
                f"<td><pre>{escape(message['body'])}</pre></td>"
                "</tr>"
            )
        transcript_html = (
            "<table>"
            "<thead><tr>"
            "<th>Thread ID</th><th>Message ID</th><th>From</th><th>To</th>"
            "<th>Subject</th><th>In-Reply-To</th><th>References</th><th>Body</th>"
            "</tr></thead>"
            "<tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )

    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Dopamine Demo UI</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.4; }}
    fieldset {{ margin-bottom: 16px; }}
    label {{ display: block; margin: 6px 0 2px; }}
    input, textarea {{ width: 100%; max-width: 640px; padding: 6px; }}
    textarea {{ height: 100px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
    th, td {{ border: 1px solid #ccc; padding: 6px; text-align: left; vertical-align: top; }}
    pre {{ white-space: pre-wrap; }}
    button {{ padding: 8px 16px; }}
  </style>
</head>
<body>
  <h1>Dopamine Demo Interface</h1>
  <p>Use this single-page UI to trigger the locked demo flow and inspect outputs.</p>
  <form method="POST" action="/run">
    <fieldset>
      <legend>Org Creation</legend>
      <label for="org_name">Org Name</label>
      <input id="org_name" name="org_name" value="{escape(inputs.org_name)}" />
      <label for="admin_email">Admin Email</label>
      <input id="admin_email" name="admin_email" value="{escape(inputs.admin_email)}" />
      <label for="org_thread_id">Org Thread ID</label>
      <input id="org_thread_id" name="org_thread_id" value="{escape(inputs.org_thread_id)}" />
    </fieldset>
    <fieldset>
      <legend>Coworker Hire</legend>
      <label for="coworker_id">Coworker ID</label>
      <input id="coworker_id" name="coworker_id" value="{escape(inputs.coworker_id)}" />
      <label for="coworker_name">Coworker Name</label>
      <input id="coworker_name" name="coworker_name" value="{escape(inputs.coworker_name)}" />
      <label for="coworker_role">Coworker Role</label>
      <input id="coworker_role" name="coworker_role" value="{escape(inputs.coworker_role)}" />
      <label for="coworker_email">Coworker Email</label>
      <input id="coworker_email" name="coworker_email" value="{escape(inputs.coworker_email)}" />
      <label for="hire_thread_id">Hire Thread ID</label>
      <input id="hire_thread_id" name="hire_thread_id" value="{escape(inputs.hire_thread_id)}" />
    </fieldset>
    <fieldset>
      <legend>User Message</legend>
      <label for="task_subject">Task Subject</label>
      <input id="task_subject" name="task_subject" value="{escape(inputs.task_subject)}" />
      <label for="task_body">Task Body</label>
      <textarea id="task_body" name="task_body">{escape(inputs.task_body)}</textarea>
      <label for="task_thread_id">Task Thread ID</label>
      <input id="task_thread_id" name="task_thread_id" value="{escape(inputs.task_thread_id)}" />
    </fieldset>
    <button type="submit">Run Demo</button>
  </form>
  {ai_reply_html}
  <section>
    <h2>Demo Logs</h2>
    {logs_html or '<p>No run yet.</p>'}
  </section>
  <section>
    <h2>Thread Transcript</h2>
    {transcript_html or '<p>No messages yet.</p>'}
  </section>
</body>
</html>
"""


class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.respond(render_page(DEFAULT_INPUTS, None))

    def do_POST(self) -> None:
        if self.path != "/run":
            self.send_error(404, "Not Found")
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        data = parse_qs(body)

        def field(name: str, fallback: str) -> str:
            value = data.get(name, [fallback])[0].strip()
            return value or fallback

        inputs = DemoInputs(
            org_name=field("org_name", DEFAULT_INPUTS.org_name),
            admin_email=field("admin_email", DEFAULT_INPUTS.admin_email),
            org_thread_id=field("org_thread_id", DEFAULT_INPUTS.org_thread_id),
            coworker_id=field("coworker_id", DEFAULT_INPUTS.coworker_id),
            coworker_name=field("coworker_name", DEFAULT_INPUTS.coworker_name),
            coworker_role=field("coworker_role", DEFAULT_INPUTS.coworker_role),
            coworker_email=field("coworker_email", DEFAULT_INPUTS.coworker_email),
            hire_thread_id=field("hire_thread_id", DEFAULT_INPUTS.hire_thread_id),
            task_subject=field("task_subject", DEFAULT_INPUTS.task_subject),
            task_body=field("task_body", DEFAULT_INPUTS.task_body),
            task_thread_id=field("task_thread_id", DEFAULT_INPUTS.task_thread_id),
            requester_name=DEFAULT_INPUTS.requester_name,
            timestamp=DEFAULT_INPUTS.timestamp,
        )

        start = time.time()
        result = run_demo(inputs)
        elapsed = time.time() - start
        result.logs.append(f"[ui] Demo completed in {elapsed:.2f}s")
        self.respond(render_page(inputs, result))

    def respond(self, html_body: str) -> None:
        encoded = html_body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main() -> None:
    server_address = ("0.0.0.0", 8000)
    httpd = HTTPServer(server_address, DemoHandler)
    print("Demo UI running on http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
