# Demo Confirmation Templates (Org Creation + Coworker Hire)

These templates are demo-ready for direct insertion into the script. Tone is neutral and sections are labeled for scan-ability.

## 1) Organization Creation — Confirmation

**Subject:** [Dopo] Organization created: {{org_name}}

**Body:**
Hello {{requester_name}},

Your organization has been created.

**Organization**
- Name: {{org_name}}
- Org ID: {{org_id}}

**Owner**
- Name: {{requester_name}}
- Email: {{requester_email}}

**Status**
- Result: Created
- Timestamp: {{timestamp}}

If you want to hire coworkers, reply with: “Hire {{coworker_role}} named {{coworker_name}}.”

—Dopo System

---

## 2) Coworker Hire — Confirmation

**Subject:** [Dopo] Coworker hired: {{coworker_name}} ({{coworker_role}})

**Body:**
Hello {{requester_name}},

Your coworker has been added to {{org_name}}.

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

To assign work, reply with: “Task for {{coworker_name}}: {{task_summary}}.”

—Dopo System
