"""Runnable mocked email demo loop for cycle 2."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple


@dataclass
class Thread:
    thread_id: str
    messages: List[Dict[str, str]] = field(default_factory=list)


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
        message = {
            "from": from_addr,
            "to": to_addr,
            "subject": subject,
            "body": body,
            "thread_id": thread_id,
        }
        self.store.threads[thread_id].messages.append(message)
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
        command, fields = parse_command(body)
        if command == "CREATE ORG":
            org_name = fields.get("name", "Acme")
            org_id = f"org-{org_name.lower().replace(' ', '-')}"
            admin = fields.get("admin_email", from_addr)
            store.create_org(org_id, org_name, admin)
            log_checklist(1, f"Org created via email command ({org_name}).")
            transport.send_email(
                from_addr=control_email,
                to_addr=admin,
                subject="Re: CREATE ORG",
                body=f"OK\norg_id: {org_id}\nname: {org_name}",
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
            transport.send_email(
                from_addr=control_email,
                to_addr=from_addr,
                subject="Re: HIRE COWORKER",
                body=(
                    "OK\n"
                    f"coworker_id: {coworker_key}\n"
                    f"name: {name}\n"
                    f"role: {role}"
                ),
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
                "Work Notes:\n"
                "- Proposed subject: Welcome to Acme (Getting Started)\n"
                "- Body: Thanks for joining... (steps 1-3)\n\n"
                "-- Sam"
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
