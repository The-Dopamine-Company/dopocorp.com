"""Runnable mocked email demo loop for cycle 2."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List


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

    org_id = "org-acme"
    admin_email = "admin@acme.test"
    coworker_id = "cw-01"
    coworker_email = "sam@acme.test"
    thread_id = "thread-1001"

    print("[demo] create org")
    store.create_org(org_id, "Acme", admin_email)

    print("[demo] hire coworker")
    store.hire_coworker(coworker_id, "Sam", "Engineer", coworker_email)

    print("[demo] send task email")
    transport.send_email(
        from_addr=admin_email,
        to_addr=coworker_email,
        subject="Task: Draft onboarding email flow",
        body=(
            "Please draft the onboarding email flow for new orgs. "
            "Include subject + body for the first message."
        ),
        thread_id=thread_id,
    )

    def send_delayed_reply() -> None:
        transport.send_email(
            from_addr=coworker_email,
            to_addr=admin_email,
            subject="Re: Task: Draft onboarding email flow",
            body=(
                "Work Notes:\n"
                "- Proposed subject: Welcome to Acme (Getting Started)\n"
                "- Body: Thanks for joining... (steps 1-3)\n\n"
                "- Sam"
            ),
            thread_id=thread_id,
        )

    print("[demo] schedule delayed reply")
    scheduler.schedule(1.5, send_delayed_reply)
    scheduler.run()

    print("[demo] thread transcript")
    for message in store.threads[thread_id].messages:
        print(
            f"  - {message['from']} -> {message['to']} | {message['subject']}"
        )


if __name__ == "__main__":
    demo()
