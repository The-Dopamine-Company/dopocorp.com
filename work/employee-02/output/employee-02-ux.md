# Employee 02 — Product Designer Deliverables

## North Star Alignment
**North star (from context):** Email-first, async-by-default, clarity mandatory, AI coworkers feel like real remote employees. No chat, no presence, no dashboards. Work should be fun.

This proposal keeps the experience anchored in email metaphors, makes async activity visible through artifacts (messages, summaries, timelines), and adds playful, opt-in game-like elements that never block core work.

---

## Core Screens

### 1) Inbox (Primary Workspace)
**Purpose:** One place to see what’s waiting, what’s completed, and what’s pending clarification.

**Key elements (all email-native):**
- **Folders/labels** for AI coworkers (e.g., “Leah (Designer)”, “Sam (Engineer)”).
- **Thread subject prefixes** (e.g., `[Draft]`, `[Question]`, `[Delivered]`) rather than real-time state.
- **Digest emails** (daily/weekly) for visibility into AI coworker activity.
- **Task Cards** are emails with structured sections (Status, Assumptions, Next Steps), not a separate UI.

ASCII wireframe:
```
+----------------------------------------------------------+
| Inbox                                                    |
| Search [_________________________________________]       |
| Folders: All | Unread | Questions | Delivered            |
|----------------------------------------------------------|
| [Question] Brand refresh: need logo size?    (Leah)  2m  |
| [Draft] Hiring email copy v1                 (Ari)  1h  |
| [Delivered] Site footer spec                 (Sam)  4h  |
| [Draft] Podcast outreach list                (Nia)  1d  |
| [Digest] Weekly summary from AI coworkers           1d  |
+----------------------------------------------------------+
```

### 2) Thread (Email Thread View)
**Purpose:** The full async conversation and artifacts live in the thread.

**Key elements:**
- **Thread timeline** with message timestamps.
- **AI coworker “Work Notes” block** in each reply (assumptions, risks, next steps).
- **“Request Clarification”** button = templated email reply (no chat).
- **“Archive with reason”** to keep async work legible.

ASCII wireframe:
```
+----------------------------------------------------------+
| Thread: Brand refresh                                    |
|----------------------------------------------------------|
| You: Please explore new logo variants.                  |
|----------------------------------------------------------|
| Leah (Designer):                                         |
| - Draft attached: 3 concepts.pdf                         |
| - Assumptions: modern tech, minimal palette              |
| - Questions: preferred typography?                       |
| - Next step: iterate after type choice                   |
| [Reply] [Request Clarification] [Archive]                |
+----------------------------------------------------------+
```

### 3) Compose (Task Assignment)
**Purpose:** Assign work via email with guardrails for clarity.

**Key elements:**
- **Role-based templates** (Designer, Engineer, PM) with clear sections.
- **Scope & constraints checklist** (deadline, quality bar, inputs).
- **Async expectations** (explicit due time, follow-up cadence).

ASCII wireframe:
```
+----------------------------------------------------------+
| Compose                                                   |
| To: Leah (Designer)                                      |
| Subject: [Draft] Brand refresh options                   |
|----------------------------------------------------------|
| Goal: Provide 3 logo directions for review               |
| Constraints: modern, minimal, 2 color palette            |
| Inputs: current logo + competitor links                  |
| Due: Friday 3pm                                          |
|----------------------------------------------------------|
| [Send] [Save Draft] [Use Template]                       |
+----------------------------------------------------------+
```

### 4) Hire AI (Onboarding Flow)
**Purpose:** Create an AI coworker with role, context, and expectations.

**Key elements:**
- **Role card selection** (Designer, Engineer, PM, etc.).
- **“How we work” section** (response cadence, ask questions, async expectations).
- **First assignment prompt** at the end (encourages immediate use).

ASCII wireframe:
```
+----------------------------------------------------------+
| Hire AI Coworker                                         |
|----------------------------------------------------------|
| Role: [Designer ▼]                                       |
| Name: [Leah]                                             |
| Context:                                                 |
|  - Company summary                                       |
|  - Brand guidelines (optional)                           |
|----------------------------------------------------------|
| Expectations:                                            |
|  - Async responses OK                                    |
|  - Ask clarifying questions                              |
|----------------------------------------------------------|
| [Hire + Assign First Task]                               |
+----------------------------------------------------------+
```

---

## How Users Understand AI Coworker Activity (Without Real-Time Signals)
**Principle:** Visibility through work, not status.

Mechanisms:
1. **Threaded Work Notes**: every AI reply includes structured “Work Notes” (assumptions, progress, next step). This creates clarity without needing live status.
2. **Progress Bundles**: AI sends scheduled summary emails (e.g., “End of day: what I did / what I need”).
3. **Explicit “Waiting On” Tags**: if AI is blocked, it replies with a question and marks subject `[Question]`.
4. **Artifact-first replies**: deliverables arrive as attachments or structured text, so users infer progress from tangible outputs.
5. **Follow-up nudges**: if the AI is idle due to missing info, it sends a reminder email after a set delay.

---

## UX Flow Descriptions (Async-first)

### Flow A: Assign work → Receive deliverable
1. User composes email using a role template (Compose screen).
2. AI coworker acknowledges with clarifying questions (Thread screen) if needed.
3. AI returns deliverable in-thread with Work Notes.
4. User replies with feedback or archive.

### Flow B: Clarification needed
1. User sees `[Question]` in Inbox.
2. Opens thread; AI has bullet list of clarifications.
3. User replies to unblock; AI continues asynchronously.

### Flow C: Hiring a new AI coworker
1. User opens Hire AI screen; selects role and sets context.
2. System sends a confirmation email with coworker intro.
3. User immediately assigns first task (Compose).

---

## Making the UI Feel Fun (Game UI Principles, No Gamification)
**Guiding idea:** add delightful micro-moments while keeping email-native seriousness.

Game UI principles applied:
- **Progression bars → “Work Milestones”** inside threads (text-only, like “Milestone 2/3: Drafts complete”).
- **Loot-style rewards → “Artifact Drops”**: deliverables feel like “items” (files, checklists, drafts) with a playful label (e.g., “🎁 Artifact: Brand Concepts v1”).
- **Quests → “Assignments”**: a structured task email feels like a quest briefing.
- **NPC flavor → coworker personalities**: each AI coworker has a distinct voice and sign-off.
- **Soundless celebration**: small emoji in subject lines or message headers, never intrusive.

This keeps the work fun without violating the no-dashboard, no-real-time constraints.

---

## UX Rationale (Explicitly tied to North Star)
- **Email is the UI**: all interactions are modeled as email threads, folders, and messages.
- **Async is intentional**: no real-time indicators; work progress appears through artifacts and periodic summaries.
- **Clarity is mandatory**: structured templates + Work Notes reduce ambiguity.
- **Work is fun**: playful framing of deliverables and progress without gamifying or adding dashboards.

