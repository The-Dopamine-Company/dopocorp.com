# v0 Org Bootstrap + Admin Auth Model (Email Commands)

## Scope
Email-only org creation and admin validation for v0. No UI or manual console paths.

## Single Allowed Org Creation Path
**Email-only bootstrap** via a system address (e.g., `create@dopocorp.com`).

**Required email command (new thread):**
```
create org
name: <org_name>
admin_email: <admin_email>
bootstrap_token: <token> (optional if sender is pre-allowed)
```

**Rules:**
- Org creation **only** occurs from an inbound email command.
- No manual back-office or UI bootstrap is permitted in v0.
- `admin_email` becomes the initial admin and primary allowlisted sender.
- Sender must pass validation (see below). Otherwise, the command is rejected.

## Sender Validation Rules
Validation occurs before any org record is created.

1. **Normalize sender + fields**
   - Lowercase `From` and `admin_email`.
   - Strip display names; compare pure addresses only.

2. **Hard allowlist check (highest trust)**
   - If sender email is in the system allowlist, org creation is allowed **without** a bootstrap token.
   - Use this for internal test accounts or pre-approved customers.

3. **Domain check (moderate trust)**
   - If sender is not explicitly allowlisted, the sender’s domain must match `admin_email` domain.
   - If domains mismatch → reject.

4. **Bootstrap token check (required if not allowlisted)**
   - If sender is not on the allowlist, `bootstrap_token` is required.
   - Token must be valid, unused, and tied to the `admin_email` (or domain).
   - Tokens are one-time use and expire after a short window (e.g., 7 days).

5. **Final admin_email match**
   - Sender must equal `admin_email` after normalization.
   - If not equal → reject (even if token is valid).

## Error Responses & Edge Cases
All failures respond in the same thread with a concise, email-only message.

**Unknown sender (not allowlisted + no/invalid token):**
- Response: “We couldn’t verify your sender address. Please request a bootstrap token or contact support.”

**Domain mismatch:**
- If sender domain differs from `admin_email` domain:
  - Response: “Sender domain must match admin_email domain.”

**Mismatched admin_email:**
- If `From` ≠ `admin_email` after normalization:
  - Response: “admin_email must match the sender address.”

**Invalid or reused token:**
- Response: “Bootstrap token is invalid or expired. Please request a new token.”

**Org already exists:**
- If org name already exists (case-insensitive):
  - Response: “Organization name is already in use. Choose another name.”

**Duplicate request in same thread:**
- If a valid org was created already and a new create command appears:
  - Response: “Organization already created for this thread.”

**Missing required fields:**
- If `name` or `admin_email` missing:
  - Response: “Missing required fields: name, admin_email.”

**Ambiguous sender (forwarded messages / multiple From headers):**
- If multiple From headers or Resent-From present:
  - Use the top-level `From`. If ambiguous, reject with:
  - Response: “Unable to verify sender from forwarded email. Please resend from the intended admin address.”

**Plus addressing:**
- Treat `admin+tag@domain.com` as a distinct address (no stripping). Keep simple for v0.

## Notes
- All decisions are consistent with “email is the UI” and no real-time setup.
- The allowlist + bootstrap token provides a minimal, auditable gate for org creation.
