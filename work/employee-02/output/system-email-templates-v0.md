# System Email Templates v0

All templates are email-only and intentionally plain. Replace placeholders in `{braces}`.

---

## 1) Org Creation Confirmation

**Subject:** Your organization is ready — {org_name}

**To:** {admin_email}
**From:** {system_email}

**Body:**
Hi {admin_name},

Your organization is now active.

**Organization**
- Name: {org_name}
- Admin: {admin_email}

**Next step**
Reply to this thread to hire a coworker, e.g.:

"Hire a {role} named {coworker_name}."

If you didn’t request this, reply with “Cancel org.”

Thanks,
{system_name}

---

## 2) Coworker Hire Confirmation — Admin Copy

**Subject:** Coworker hired — {coworker_name} ({role})

**To:** {admin_email}
**From:** {system_email}

**Body:**
Hi {admin_name},

Your coworker has been added.

**Coworker**
- Name: {coworker_name}
- Role: {role}
- Email: {coworker_email}

You can assign work by replying to this thread or emailing {coworker_email} directly.

Thanks,
{system_name}

---

## 3) Coworker Hire Confirmation — Coworker Copy

**Subject:** Welcome to {org_name}

**To:** {coworker_email}
**From:** {system_email}

**Body:**
Hi {coworker_name},

You’ve been added to {org_name} as {role}.

**How work arrives**
- You’ll receive tasks by email
- Reply in the thread when you need clarification

If this is unexpected, reply with “Decline role.”

Thanks,
{system_name}

---

## 4) Command Response — Success

(Use for pause/resume/update role)

**Subject:** Command completed — {command_summary}

**To:** {requester_email}
**From:** {system_email}

**Body:**
Hi {requester_name},

Your request was completed.

**Command**
- Action: {command_action}
- Target: {command_target}
- Result: {command_result}

If this isn’t correct, reply with the desired change.

Thanks,
{system_name}

---

## 5) Command Response — Failure

(Use for pause/resume/update role)

**Subject:** Command failed — {command_summary}

**To:** {requester_email}
**From:** {system_email}

**Body:**
Hi {requester_name},

We couldn’t complete your request.

**Command**
- Action: {command_action}
- Target: {command_target}

**Issue**
{failure_reason}

**How to fix**
{recovery_steps}

Reply in this thread to try again.

Thanks,
{system_name}
