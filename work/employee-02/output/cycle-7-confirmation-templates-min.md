# Cycle 7 — Minimal Demo Confirmation Templates

These variants keep labeled sections but remove optional guidance to minimize script changes.

## 1) Organization Creation — Confirmation (Minimal)

**Subject:** [Dopo] Organization created: {{org_name}}

**Body:**
Hello {{requester_name}},

Organization created.

**Organization**
- Name: {{org_name}}
- Org ID: {{org_id}}

**Owner**
- Name: {{requester_name}}
- Email: {{requester_email}}

**Status**
- Result: Created
- Timestamp: {{timestamp}}

—Dopo System

---

## 2) Coworker Hire — Confirmation (Minimal)

**Subject:** [Dopo] Coworker hired: {{coworker_name}} ({{coworker_role}})

**Body:**
Hello {{requester_name}},

Coworker hired.

**Coworker**
- Name: {{coworker_name}}
- Role: {{coworker_role}}
- Coworker ID: {{coworker_id}}

**Organization**
- Name: {{org_name}}
- Org ID: {{org_id}}

**Status**
- Result: Hired
- Timestamp: {{timestamp}}

—Dopo System
