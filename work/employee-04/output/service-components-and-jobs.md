# Service Components and Jobs (v0)

## Runtime Components (minimal)

### 1) Ingest Service
**Purpose:** Receive inbound email events from the SMTP provider webhook.
**Responsibilities:**
- Verify provider signature + basic spam checks.
- Store raw MIME and attachments.
- Emit `ingest.received` job with minimal metadata.

### 2) Parser Service
**Purpose:** Convert raw MIME into structured fields.
**Responsibilities:**
- Parse headers (From, To, CC, Message-ID, In-Reply-To, References, Subject).
- Extract text/plain + text/html bodies.
- Identify organization and sender.
- Emit `parse.completed` job.

### 3) Router Service
**Purpose:** Determine what the message means in system terms.
**Responsibilities:**
- Threading: attach to existing thread or create new thread.
- Classify command vs normal message.
- Determine recipient coworker(s) and internal/external scope.
- Emit `route.completed` job (or `route.rejected`).

### 4) Scheduler Service
**Purpose:** Apply delay policy and enqueue response generation.
**Responsibilities:**
- Choose response delay (v0: 5–30 minutes).
- Persist scheduled time.
- Emit `response.generate` job at scheduled time.

### 5) Sender Service
**Purpose:** Send outbound emails via provider.
**Responsibilities:**
- Compose reply + headers (Message-ID, In-Reply-To, References).
- Apply from/reply-to rules.
- Track delivery + bounce webhook updates.

---

## Queue Jobs (with minimal payloads)

### `ingest.received`
**When:** Provider webhook fires.
**Payload:**
- `provider_event_id`
- `received_at`
- `raw_mime_location`
- `envelope_from`
- `envelope_to[]`
- `provider_headers` (for signature verification)

### `parse.completed`
**When:** Parser completes.
**Payload:**
- `message_id`
- `from`
- `to[]`, `cc[]`
- `subject`
- `in_reply_to`
- `references[]`
- `text_body` (plain)
- `html_body`
- `attachments[]` (metadata + storage refs)
- `organization_id` (if detected)
- `sender_user_id` (if matched)

### `route.completed`
**When:** Router finishes.
**Payload:**
- `thread_id`
- `message_id`
- `organization_id`
- `intent` (command | conversation | unknown)
- `targets[]` (coworker ids or admin)
- `visibility` (internal | external)
- `rejection_reason` (optional)

### `response.generate`
**When:** Delay window elapses.
**Payload:**
- `thread_id`
- `message_id` (triggering message)
- `organization_id`
- `target_coworker_id`
- `response_due_at`
- `context_snapshot_id` (conversation state)

### `send.outbound`
**When:** Response text is ready.
**Payload:**
- `thread_id`
- `message_id` (response)
- `from`
- `to[]`, `cc[]`
- `subject`
- `in_reply_to`
- `references[]`
- `body_text`
- `body_html` (optional)

### `delivery.update`
**When:** Provider signals delivered/bounced.
**Payload:**
- `provider_event_id`
- `message_id`
- `delivery_status` (delivered | bounced | deferred)
- `timestamp`
- `failure_reason` (if any)

---

## Data Needed to Support Delayed Responses

### Scheduling Data
- `response_due_at` (timestamp)
- `delay_window_minutes` (for audit)
- `scheduled_by` (system)

### Context Snapshot
- `context_snapshot_id` referencing a stored view of:
  - last N messages in thread
  - coworker role + persona
  - org policies (allowlists, domain rules)

### Thread and Message State
- `thread_id` (stable)
- `message_id` (immutable)
- `latest_message_at`
- `pending_response` (boolean)

### Idempotency Keys
- `provider_event_id`
- `message_id`
- `send_attempt_id`

---

## Minimal Failure Handling
- If `route.rejected`, emit a system email with a clear error reason.
- If `send.outbound` fails, retry with backoff and log to delivery status.
