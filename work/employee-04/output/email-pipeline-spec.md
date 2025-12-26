# Employee 04 — Email System Engineer

# Email Pipeline Spec v0 (Inbound/Outbound)

## Scope
- Email-only MVP pipeline for inbound and outbound messages.
- No chat, no real-time signaling, no additional channels.
- Builds on `email-system-design.md` threading/data model assumptions.

## Transport choices (v0)
- **Inbound:** Managed SMTP provider with inbound routing to an HTTPS webhook (e.g., SES inbound or comparable). The system receives the full MIME payload plus envelope metadata.
- **Outbound:** Managed SMTP relay/API provider (e.g., SES SMTP or API). Use a single provider initially to minimize operational complexity.
- **Reasoning:** Keeps deliverability, DKIM/SPF, and bounce handling in a single integration path.

## Inbound pipeline

### 1) Receive (SMTP → webhook)
1. SMTP provider accepts email for organization domains.
2. Provider posts the raw MIME payload + envelope sender/recipients + receipt timestamp to `/email/inbound`.
3. System acknowledges receipt immediately (202) and enqueues processing.

### 2) Parse & normalize
1. Parse headers: `Message-ID`, `In-Reply-To`, `References`, `Subject`, `From`, `To`, `Cc`, `Bcc`, `Reply-To`, `Date`.
2. Parse body:
   - Extract `text/plain` and `text/html` (sanitize HTML).
   - Strip tracking pixels/inline scripts.
3. Parse attachments:
   - Extract filename/content-type/size.
   - Store binary to object storage.
4. Normalize addresses:
   - Lowercase domains.
   - De-duplicate recipients by mailbox alias.

### 3) Classify organization & internal/external
1. Resolve organization by recipient domain (match to `Organization.domains`).
2. Determine `is_internal` by checking if all participants are on org domains.
3. Validate internal claims using provider validation (SPF/DKIM/DMARC status if available).

### 4) Threading flow
1. Use header-first threading per `email-system-design.md`:
   - Match `In-Reply-To` to existing `Message-ID`.
   - Else match `References` to newest known thread.
2. If no header match, apply normalized subject fallback with participant overlap ≥ 1.
3. If still unmatched, create a new thread.
4. Do not cross org boundaries.

### 5) Storage writes (inbound)
- **Message** record (immutable):
  - `direction = inbound`
  - `received_at` from SMTP receipt
  - `sent_at` from `Date` header if present
  - Store `headers_raw`, parsed fields, `message_id_header`, `in_reply_to_header`, `references_header`.
- **Thread**:
  - Create or update `last_message_at`.
- **Recipients**:
  - Write `Recipient` rows for to/cc/bcc with delivery status `accepted`.
- **Attachments**:
  - Store `AttachmentRef` records with storage URI/checksum.
- **DeliveryLog**:
  - Log provider acceptance for inbound receipt (status `accepted`).

### 6) Downstream delivery (inbound)
- Route the inbound message to any internal mailboxes (AI or human) that are recipients.
- For AI mailboxes:
  - Enqueue an async processing job with thread context.
- For human mailboxes:
  - Display the message in the email UI (or surface in outbound relay if acting as mailbox host).

## Outbound pipeline

### 1) Compose & queue
1. User/AI composes an email from a mailbox.
2. Create an outbound `Message` with `direction = outbound`, `status = queued`.
3. Generate `Message-ID` header.
4. Apply threading headers from original thread if reply:
   - Set `In-Reply-To` and append `References`.

### 2) Address validation & policy checks
1. De-duplicate recipients across `to/cc/bcc`.
2. Prevent internal alias loops (skip self-sends unless explicitly allowed).
3. Enforce org policy: external sending allowed only for approved mailboxes (v0 simple allow-all or domain whitelist).

### 3) Render & send
1. Build MIME:
   - Include text and HTML.
   - Include attachments via multipart/mixed.
2. Send via SMTP/API provider.
3. Record provider response IDs in `DeliveryLog`.

### 4) Storage writes (outbound)
- Update `Message.status`:
  - `sent` once provider accepts.
  - `failed` if provider rejects.
- Write `DeliveryLog` entries per recipient (status `accepted`, `deferred`, or `bounced`).

## Bounce & complaint handling

### Inbound bounces (for outbound messages)
1. Provider posts bounce/complaint webhook to `/email/bounce`.
2. Match by provider message ID or `Message-ID` header.
3. Update:
   - `DeliveryLog.status = bounced`
   - `Recipient.delivery_status = bounced`
   - `Message.status = failed` if all recipients bounced, else keep `sent`.
4. Emit system notification email to the sender (from a system mailbox) with bounce details.

### Outbound bounces (delivery failures)
- Immediate SMTP rejection → mark failed and notify sender.
- Deferred/temporary → mark `deferred`, schedule retry.

## Failure paths & retries

### Inbound
- **Webhook failure**: provider retries webhook; if permanent failure, store payload in dead-letter queue for manual reprocess.
- **Parsing failure**: store raw headers/body, mark message as `failed_parse`, do not drop.
- **Attachment ingestion failure**: store message without attachment and schedule retry.
- **Thread mismatch**: store in new thread; allow manual re-threading.

### Outbound
- **Provider rejection**: set `Message.status = failed`, log error, notify sender.
- **Provider timeout**: keep `queued`, retry with exponential backoff.
- **Rate limit**: throttle and retry; record in `DeliveryLog`.
- **Partial delivery**: maintain per-recipient statuses.

## MVP alignment notes
- One transport provider for inbound/outbound (reduces complexity).
- No multi-region, no advanced queue orchestration.
- Threading uses header-first rules with subject fallback only.
- Only email-based notifications; no push or UI alerts.
