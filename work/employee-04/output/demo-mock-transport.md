# Demo Mocked Email Transport + Scheduler Design

## Purpose
Provide a minimal, in-memory email transport and scheduler to power the demo flow:
create org → hire coworker → send task email → schedule delayed reply → send reply in same thread.

This design is intentionally simple (no external SMTP, no persistence) but keeps the same payload fields
and thread linkage behavior we expect in the real system.

---

## Components (In-Memory)

1. **MockTransport**
   - Accepts outbound email payloads and stores them in a `sent[]` array.
   - Emits `email.sent` events for inspection/testing.

2. **MockInbox**
   - Accepts inbound email payloads and stores them in a `received[]` array.
   - Emits `email.received` events for routing into the system.

3. **MockScheduler**
   - Uses a `scheduled[]` array of jobs with `runAt` timestamps.
   - Ticks via `setInterval` or manual `tick(now)` to execute due jobs.

4. **ThreadStore**
   - In-memory map keyed by `threadId` with `messageIds[]` and subject.
   - Used to ensure replies include the correct `In-Reply-To` and `References`.

---

## Required Payload Fields

### Email Message (Inbound/Outbound)
```
{
  id: "msg_123",               // unique message id
  orgId: "org_123",
  from: "pm@demo.com",
  to: ["coworker@demo.com"],
  cc: [],
  bcc: [],
  subject: "Task: Draft launch email",
  text: "...",
  html: "..." | null,
  threadId: "thr_123",         // derived or assigned
  inReplyTo: "msg_001" | null,
  references: ["msg_001", ...],
  headers: {
    "Message-ID": "msg_123",
    "In-Reply-To": "msg_001"
  },
  createdAt: "2025-02-12T12:00:00Z"
}
```

### Scheduled Job
```
{
  id: "job_123",
  type: "send_email",
  runAt: "2025-02-12T12:05:00Z",
  payload: {
    orgId,
    threadId,
    message: { ...Email Message... }
  }
}
```

---

## Thread Linkage Rules (Minimal)

- If `inReplyTo` is set, reuse the original thread:
  - `threadId` is the original thread’s id
  - `references` append the new `inReplyTo` id
- If `inReplyTo` is null, create a new `threadId`.
- `ThreadStore` keeps:
  - `threadId → { subject, messageIds[] }`.

---

## Scheduling Flow (Demo)

1. Inbound task email enters `MockInbox`.
2. Router decides coworker should respond after a delay (e.g., 3 minutes).
3. Scheduler enqueues `send_email` job with `runAt = now + delay`.
4. On tick, Scheduler dispatches job to `MockTransport`.
5. `MockTransport` stores the sent reply in the `sent[]` array.
6. Reply payload includes `inReplyTo` and `references` so it stays in the same thread.

---

## Suggested Local Dev Wiring

- **Single process** Node script or dev server.
- Use module-level in-memory arrays:
  - `const sent = []`
  - `const received = []`
  - `const scheduled = []`
  - `const threads = new Map()`

### Example wiring (pseudo)
```
const transport = new MockTransport(sent);
const scheduler = new MockScheduler(scheduled, (job) => {
  if (job.type === "send_email") transport.send(job.payload.message);
});

mockInbox.on("email.received", (message) => {
  const { threadId, inReplyTo, references } = threader.link(message, threads);
  const reply = coworker.composeReply({ threadId, inReplyTo, references });
  scheduler.schedule({ type: "send_email", runAt: Date.now() + 180000, payload: { message: reply } });
});

setInterval(() => scheduler.tick(Date.now()), 1000);
```

---

## Notes for Demo Reliability

- Make `MockScheduler` deterministic by allowing manual `tick(now)` calls for tests.
- Expose the `sent[]` array to verify the reply body and thread headers.
- Keep IDs explicit so the demo can assert that `reply.inReplyTo` matches the original task email.
