# Email Command Spec v0 (MVP)

## Purpose
Define the minimal email-only command grammar to manage organizations and coworkers (create org, hire coworker, pause/resume, update role). This spec assumes no UI and no real-time systems.

## Scope / Anti-Features Alignment
- **Email is the UI**: all commands are sent via email to a control address.
- **Async only**: no chat, live status, or dashboards.
- **Minimal HR**: no payroll, scheduling, performance tracking, or complex permissions.
- **Single-thread command execution**: each command is handled within its own email thread.

## Command Transport
- **Control address**: `control@dopocorp.com` (or tenant-specific alias `control@<org-domain>` once org exists).
- **Command format**: plain text in email body (subject ignored except for routing).
- **One command per email**.

## Sender Validation & Auth Assumptions (v0)
1. **Allowlist-based admin**: only emails in an allowlist are allowed to issue commands.
2. **Domain verification**: for org creation, the sender’s email domain is treated as the org domain unless explicitly specified.
3. **Bootstrap secret (optional)**: an optional one-time token may be required in the body for org creation if no allowlist exists.
4. **No delegated admin**: only the initial admin email(s) may issue commands (until role management exists).

If a command fails auth, the system replies with an error and takes no action.

## Bootstrap Path (Email-Only)
- **Path A (allowlist)**: Operator pre-loads a single admin email; that admin can email `CREATE ORG`.
- **Path B (token)**: Operator sends a one-time bootstrap token to the intended admin. The admin includes it in the `CREATE ORG` command body.

No UI, no API keys, no dashboards.

---

## Command Grammar

### Conventions
- Keywords are uppercase.
- Required fields are plain `key: value` lines.
- Optional fields are marked `(optional)`.
- Identifiers should be stable and human-readable (e.g., `coworker_id: eng-1`).

### 1) Create Organization
```
CREATE ORG
name: <Organization Name>
admin_email: <Admin Email>
(org_domain: <domain>) (optional)
bootstrap_token: <token> (optional; required if no allowlist)
```
**Notes**
- `org_domain` defaults to the sender’s domain.
- `admin_email` must match the sender.

### 2) Hire Coworker
```
HIRE COWORKER
coworker_id: <id>
name: <Full Name>
role: <Role Title>
email_alias: <local-part>@<org-domain>
model: <model_name> (optional)
```
**Notes**
- `email_alias` must be within the org domain.
- `coworker_id` is unique within the org.

### 3) Pause Coworker
```
PAUSE COWORKER
coworker_id: <id>
reason: <short reason> (optional)
```
**Effect**
- Coworker stops responding to new threads until resumed.

### 4) Resume Coworker
```
RESUME COWORKER
coworker_id: <id>
```
**Effect**
- Coworker resumes responding to new threads.

### 5) Update Role
```
UPDATE ROLE
coworker_id: <id>
role: <New Role Title>
```
**Notes**
- Role updates do not change email aliases.

---

## Response Semantics (v0)
- System replies in the same thread with one of:
  - `OK` + a short summary of the action taken.
  - `ERROR` + a short reason (e.g., `auth_failed`, `missing_field`, `unknown_coworker`).

## Examples

**Create org**
```
CREATE ORG
name: Dopocorp
admin_email: founder@dopocorp.com
bootstrap_token: 9f2c-…
```

**Hire coworker**
```
HIRE COWORKER
coworker_id: eng-1
name: Alex Rivera
role: Founding Engineer
email_alias: alex@dopocorp.com
model: gpt-5
```

**Pause coworker**
```
PAUSE COWORKER
coworker_id: eng-1
reason: on leave
```

**Resume coworker**
```
RESUME COWORKER
coworker_id: eng-1
```

**Update role**
```
UPDATE ROLE
coworker_id: eng-1
role: Staff Engineer
```
