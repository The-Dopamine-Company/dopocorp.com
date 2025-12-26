# Employee 04 — Email System Engineer

## Data model sketches (text)

### Core entities
```
Organization
- id (uuid)
- name
- domains[] (for internal vs external classification)
- created_at

Mailbox
- id (uuid)
- organization_id
- address (local@domain)
- type (human | ai)
- display_name
- status (active | disabled)

Message (Email)
- id (uuid)
- organization_id
- thread_id
- mailbox_id (sender)
- from_address (string)
- reply_to (string | null)
- to[] (address list)
- cc[] (address list)
- bcc[] (address list)
- subject
- body_text
- body_html
- attachments[] (AttachmentRef)
- sent_at (timestamp)
- received_at (timestamp)
- direction (inbound | outbound)
- is_internal (bool)
- headers_raw (blob)
- message_id_header (string)
- in_reply_to_header (string | null)
- references_header[] (string[])
- status (queued | sent | failed | delivered)

Thread
- id (uuid)
- organization_id
- canonical_subject
- participants[] (address list)
- last_message_at
- created_at
- status (open | closed | archived)

AttachmentRef
- id (uuid)
- message_id
- filename
- content_type
- size_bytes
- storage_uri
- checksum

DeliveryLog
- id (uuid)
- message_id
- recipient_address
- transport (smtp | api)
- status (accepted | bounced | deferred)
- timestamp
- error_code
- error_detail
```

### Derived/auxiliary entities
```
Recipient
- message_id
- address
- type (to | cc | bcc)
- is_internal (bool)
- delivery_status (accepted | bounced | deferred)

ThreadMembership
- thread_id
- mailbox_id
- role (participant | owner | observer)
- last_read_at

MailboxAlias
- mailbox_id
- alias_address
- is_primary
```

## Definitions

### What an Email is
An Email is a persisted message object representing a single sent or received communication. It includes envelope data (sender, recipients), content (subject, body, attachments), and transport headers (Message-ID, In-Reply-To, References). Emails are immutable once stored; edits are represented as a new Email linked by threading.

### What a Thread is
A Thread is a logical grouping of Emails that form a conversation. It is defined by header-based relationships (Message-ID ↔ In-Reply-To/References) and secondarily by subject normalization. A Thread aggregates participants, maintains ordering by timestamp, and acts as the unit of context for AI coworkers.

## Reply, forward, and CC behavior

### Replies
- A reply creates a new Email where:
  - `in_reply_to_header` references the original Email’s `message_id_header`.
  - `references_header` appends the original Message-ID chain.
  - `thread_id` is inherited from the original, unless threading logic reassigns.
- Default recipient handling:
  - Reply → original sender in `to`, prior `to/cc` (excluding the current sender) copied to `cc`.
  - Reply-all → original sender + all prior `to/cc` (excluding the current sender).
- When replying to an external Email, internal aliases are de-duplicated to avoid loops.

### Forwards
- A forward creates a new Email with new recipients and a fresh `message_id_header`.
- Thread behavior:
  - “Forward as attachment” → typically new thread (no In-Reply-To).
  - “Inline forward” → optional linkage to original thread via `references_header` but marked `thread_id` = new thread unless an explicit “forward within thread” flag is set.
- Original content is preserved inside the body/attachment but does not mutate the original Email.

### CC-like behavior
- `cc` recipients are visible to all non-bcc recipients.
- `bcc` recipients are stored and delivered but never surfaced to recipients or to other participants in the Thread UI.
- Thread participant list includes `to` + `cc` + sender; `bcc` is excluded from visible participants but may exist in internal thread metadata for delivery tracking.

## Internal vs external emails

### Internal
- `is_internal = true` when all sender and recipient domains match Organization domains.
- Internal Emails may skip some compliance checks, but still enforce spam/bounce handling.
- Internal Threads are visible only inside the Organization and used to coordinate AI coworkers.

### External
- `is_internal = false` when any participant is outside Organization domains.
- External Emails must enforce outbound safeguards (e.g., bounce handling, SPF/DKIM alignment if required by transport).
- External Emails may carry a compliance audit trail and stricter rate limiting.

## Metadata that exists but is not shown to users

- Raw headers (`headers_raw`), including transport routing details.
- Message-ID / References used for threading.
- Delivery logs, SMTP status, and bounce codes.
- Spam score / security classification tags.
- Original recipient envelope (especially for BCC).
- Internal routing metadata (queue IDs, processing timestamps).
- Read tracking markers (if enabled) for internal system analytics.
- Content hashes / checksums for deduplication.

## Threading logic (explanation)

1. **Header-first linking**
   - If `In-Reply-To` matches a known Message-ID, attach to that Email’s Thread.
   - Else if any `References` header matches known Message-IDs, attach to the newest matching Thread.
2. **Subject normalization fallback**
   - Normalize subject by stripping “Re:”, “Fwd:”, whitespace, and list prefixes.
   - If a recent Thread with same normalized subject exists and participant overlap >= 1, attach.
3. **New Thread creation**
   - If no header or subject-based match, create a new Thread.
4. **Cross-org guardrail**
   - Do not merge Threads across organizations, even if headers match (prevents data leakage).
5. **Override hooks**
   - Allow system operators or explicit reply metadata to override threading when a known mismatch occurs.

## Edge cases & failure scenarios

### Edge cases
- **Missing Message-ID**: Treat as new Email; thread via subject fallback.
- **Duplicate Message-ID**: Store both but flag conflict; use received order for threading.
- **Multiple In-Reply-To values**: Choose the most recent known Message-ID; append all to references.
- **Subject drift**: Replies that change subject must still thread via headers.
- **Alias-based loops**: Internal aliases can cause reply-all loops; de-duplicate recipients by mailbox.
- **BCC replies**: BCC recipient replies will not expose original BCC list; threading relies on headers.

### Failure scenarios
- **SMTP hard bounce**: Mark delivery failed; log bounce; notify sender via system event email.
- **Partial delivery**: Some recipients accepted, others deferred—store per-recipient delivery status.
- **Attachment storage failure**: Store Email without attachment; mark as degraded and retry attachment ingestion.
- **Thread mismatch**: Incorrect subject-based threading; allow manual or automated re-threading.
- **External spoofing**: Inbound email claims internal domain; rely on SMTP validation and DKIM to set `is_internal`.
- **Clock skew**: Received timestamps out of order; order by received_at then sent_at.
