"""Runnable mocked email demo loop for cycle 2."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple


@dataclass
class Thread:
    thread_id: str
    counter: int = 0
    messages: List[Dict[str, str]] = field(default_factory=list)

    def next_message_id(self) -> str:
        self.counter += 1
        return f"{self.thread_id}-msg-{self.counter:03d}"


@dataclass
class InMemoryStore:
    orgs: Dict[str, Dict[str, str]] = field(default_factory=dict)
    coworkers: Dict[str, Dict[str, str]] = field(default_factory=dict)
    threads: Dict[str, Thread] = field(default_factory=dict)

    def create_org(self, org_id: str, name: str, admin_email: str) -> None:
        self.orgs[org_id] = {
            "org_id": org_id,
            "name": name,
            "admin_email": admin_email,
        }

    def hire_coworker(self, coworker_id: str, name: str, role: str, email: str) -> None:
        self.coworkers[coworker_id] = {
            "coworker_id": coworker_id,
            "name": name,
            "role": role,
            "email": email,
        }

    def create_thread(self, thread_id: str) -> Thread:
        thread = Thread(thread_id=thread_id)
        self.threads[thread_id] = thread
        return thread


@dataclass
class MockEmailTransport:
    store: InMemoryStore

    def send_email(
        self,
        *,
        from_addr: str,
        to_addr: str,
        subject: str,
        body: str,
        thread_id: str,
    ) -> None:
        if thread_id not in self.store.threads:
            self.store.create_thread(thread_id)
        thread = self.store.threads[thread_id]
        message_id = thread.next_message_id()
        in_reply_to = thread.messages[-1]["message_id"] if thread.messages else ""
        references = " ".join(msg["message_id"] for msg in thread.messages)
        message = {
            "from": from_addr,
            "to": to_addr,
            "subject": subject,
            "body": body,
            "thread_id": thread_id,
            "message_id": message_id,
            "in_reply_to": in_reply_to,
            "references": references,
        }
        thread.messages.append(message)
        print(
            "[transport] "
            f"thread={thread_id} "
            f"msg={message_id} "
            f"in-reply-to={in_reply_to or '-'} "
            f"refs={references or '-'} "
            f'subject="{subject}"'
        )
        print(f"[send] {from_addr} -> {to_addr} | {subject} | thread={thread_id}")


@dataclass
class Scheduler:
    queue: List[Dict[str, object]] = field(default_factory=list)

    def schedule(self, delay_seconds: float, task: Callable[[], None]) -> None:
        self.queue.append({"delay": delay_seconds, "task": task})

    def run(self) -> None:
        for job in self.queue:
            delay = float(job["delay"])
            task = job["task"]
            print(f"[scheduler] waiting {delay:.1f}s")
            time.sleep(delay)
            task()
        self.queue.clear()


def demo() -> None:
    store = InMemoryStore()
    transport = MockEmailTransport(store=store)
    scheduler = Scheduler()

    admin_email = "admin@acme.test"
    control_email = "control@dopocorp.test"
    coworker_id = "cw-01"
    coworker_email = "sam@acme.test"
    requester_name = "Admin"
    timestamp = "2025-12-26 09:00 UTC"
    current_org_id = ""
    org_thread_id = "thread-org-1001"
    hire_thread_id = "thread-hire-1002"
    task_thread_id = "thread-task-1003"

    def log_checklist(step: int, message: str) -> None:
        print(f"[checklist {step}] {message}")

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

    def handle_command_email(
        *,
        from_addr: str,
        body: str,
        thread_id: str,
    ) -> None:
        nonlocal current_org_id
        command, fields = parse_command(body)
        if command == "CREATE ORG":
            org_name = fields.get("name", "Acme")
            org_id = f"org-{org_name.lower().replace(' ', '-')}"
            admin = fields.get("admin_email", from_addr)
            store.create_org(org_id, org_name, admin)
            current_org_id = org_id
            log_checklist(1, f"Org created via email command ({org_name}).")
            org_confirmation_subject = f"[Dopo] Organization created: {org_name}"
            org_confirmation_body = (
                f"Hello {requester_name},\n\n"
                "Your organization has been created.\n\n"
                "**Organization**\n"
                f"- Name: {org_name}\n"
                f"- Org ID: {org_id}\n\n"
                "**Owner**\n"
                f"- Name: {requester_name}\n"
                f"- Email: {admin}\n\n"
                "**Status**\n"
                "- Result: Created\n"
                f"- Timestamp: {timestamp}\n\n"
                'If you want to hire coworkers, reply with: “Hire Engineer named Sam.”\n\n'
                "—Dopo System"
            )
            transport.send_email(
                from_addr=control_email,
                to_addr=admin,
                subject=org_confirmation_subject,
                body=org_confirmation_body,
                thread_id=thread_id,
            )
        elif command == "HIRE COWORKER":
            name = fields.get("name", "Sam")
            role = fields.get("role", "Engineer")
            email_alias = fields.get("email_alias", coworker_email)
            coworker_key = fields.get("coworker_id", coworker_id)
            store.hire_coworker(coworker_key, name, role, email_alias)
            log_checklist(
                2,
                f"Coworker hired via email command ({name}, {role}).",
            )
            org_id = current_org_id or "org-unknown"
            org_name = store.orgs.get(org_id, {}).get("name", "Acme")
            hire_confirmation_subject = f"[Dopo] Coworker hired: {name} ({role})"
            hire_confirmation_body = (
                f"Hello {requester_name},\n\n"
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
                f"- Timestamp: {timestamp}\n\n"
                f"To assign work, reply with: “Task for {name}: Draft onboarding email flow.”\n\n"
                "—Dopo System"
            )
            transport.send_email(
                from_addr=control_email,
                to_addr=from_addr,
                subject=hire_confirmation_subject,
                body=hire_confirmation_body,
                thread_id=thread_id,
            )
        else:
            transport.send_email(
                from_addr=control_email,
                to_addr=from_addr,
                subject=f"Re: {command or 'UNKNOWN COMMAND'}",
                body="ERROR\nreason: unknown_command",
                thread_id=thread_id,
            )

    log_checklist(7, "Using in-memory storage for orgs, coworkers, and threads.")
    log_checklist(8, "Using mocked email transport for send/receive.")
    log_checklist(9, "Demo script runs deterministically from a single entrypoint.")

    print("[demo] ingest org creation command email")
    org_command_body = (
        "CREATE ORG\n"
        "name: Acme\n"
        f"admin_email: {admin_email}\n"
    )
    transport.send_email(
        from_addr=admin_email,
        to_addr=control_email,
        subject="CREATE ORG",
        body=org_command_body,
        thread_id=org_thread_id,
    )
    handle_command_email(
        from_addr=admin_email,
        body=org_command_body,
        thread_id=org_thread_id,
    )

    print("[demo] ingest coworker hire command email")
    hire_command_body = (
        "HIRE COWORKER\n"
        f"coworker_id: {coworker_id}\n"
        "name: Sam\n"
        "role: Engineer\n"
        f"email_alias: {coworker_email}\n"
    )
    transport.send_email(
        from_addr=admin_email,
        to_addr=control_email,
        subject="HIRE COWORKER",
        body=hire_command_body,
        thread_id=hire_thread_id,
    )
    handle_command_email(
        from_addr=admin_email,
        body=hire_command_body,
        thread_id=hire_thread_id,
    )

    print("[demo] send task email")
    transport.send_email(
        from_addr=admin_email,
        to_addr=coworker_email,
        subject="Task: Draft onboarding email flow",
        body=(
            "Please draft the onboarding email flow for new orgs. "
            "Include subject + body for the first message."
        ),
        thread_id=task_thread_id,
    )
    log_checklist(3, "Task assignment email stored with thread identifier.")

    def send_delayed_reply() -> None:
        transport.send_email(
            from_addr=coworker_email,
            to_addr=admin_email,
            subject="Re: Task: Draft onboarding email flow",
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
                "— Sam\n"
                "AI Coworker (Engineer)"
            ),
            thread_id=task_thread_id,
        )
        log_checklist(5, "Reply sent in the same thread with Re: subject.")
        log_checklist(6, "Reply includes Work Notes section and signature.")

    print("[demo] schedule delayed reply")
    delay_seconds = 1.5
    scheduler.schedule(delay_seconds, send_delayed_reply)
    log_checklist(4, f"Reply scheduled with {delay_seconds:.1f}s delay.")
    scheduler.run()

    log_checklist(10, "Console output includes key state transitions.")
    print("[demo] thread transcript")
    for message in store.threads[task_thread_id].messages:
        print(f"  - {message['from']} -> {message['to']} | {message['subject']}")


if __name__ == "__main__":
    demo()
