# Demo Email Scripts (Cycle 2)

Below are ready-to-use demo emails (subject + body) for the mocked flow:
Create org → Hire coworker → Assign task → Coworker reply.

---

## 1) Org Creation
**Subject:** [System] Organization created: Dopoco Labs

**Body:**
Hello,

Your organization has been created.

**Organization**
- Name: Dopoco Labs
- Owner: alex@dopoco.com

**Next Steps**
- Hire a coworker by replying with a role and name.

— Dopoco System

---

## 2) Coworker Hire Confirmation
**Subject:** [System] Coworker hired: “Jamie Park” (Product Designer)

**Body:**
Hello,

Your coworker has been added.

**Coworker**
- Name: Jamie Park
- Role: Product Designer
- Email: jamie@dopoco.com

**Next Steps**
- Assign a task by replying in this thread.

— Dopoco System

---

## 3) Task Assignment Email
**Subject:** [Task] Draft onboarding email series for new orgs

**Body:**
Hi Jamie,

Please draft a short onboarding email series for new organizations.

**Goal**
- Provide a 3-email sequence for newly created orgs.

**Scope**
- 3 emails total
- Plain text only
- Each email ≤ 120 words

**Constraints**
- No marketing hype
- Keep tone neutral and practical

**Work Notes**
- The product is email-first and async by default.
- Avoid chat metaphors.

Thanks,
Alex

---

## 4) Coworker Reply (Formatted per v0 Templates)
**Subject:** Re: [Task] Draft onboarding email series for new orgs

**Body:**
Hi Alex,

Here’s a draft of the 3-email onboarding sequence.

**Work Notes**
- Kept each message short and practical.
- Avoided marketing language and chat metaphors.
- Included one clear action per email.

**Artifacts**
**Email 1 — Welcome & setup**
Subject: Welcome to Dopoco Labs
Body:
Welcome to Dopoco Labs.

Your org is ready. To start, reply with the role and name of the first coworker you want to hire.

If you already know the first task, you can include it in the same reply.

— Dopoco System

**Email 2 — First task prompt**
Subject: Your first task
Body:
You can assign work by replying in any thread.

Send a short goal, scope, and constraints. The coworker will reply asynchronously in the same thread.

— Dopoco System

**Email 3 — Async expectations**
Subject: How replies work
Body:
Coworkers respond in the same email thread. There are no real-time updates.

If something is unclear, they will ask follow-up questions before proceeding.

— Dopoco System

**Questions**
- Do you want these emails signed as “Dopoco System” or “Dopoco Team”? If not specified, I’ll keep “Dopoco System.”

— Jamie
