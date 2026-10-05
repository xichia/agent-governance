# Demo delivery plan — agent-staffed events agency

- **Task:** [T-GOV-007](../../records/tasks/T-GOV-007.md)
- **Writer / session / model:** `/root/demo_delivery` · configured model `gpt-6-luna` (internal deployment identifier unavailable)
- **Governance:** charter 0.1.1 at `5c35200db736c86b6a6e31cd30de8d3af48211de`
- **Status:** planning proposal only; no agency charter, operational agents, or live event is authorized

## Objective and proposed audience challenge

Demonstrate how a small, role-based AI events agency can turn an ambiguous client request into a coherent, costed event proposal, expose disagreements and risks, and hand a reviewed recommendation to a human decision-maker. The audience is educated non-specialists; the presentation should make responsibilities, sources, uncertainty, and approval boundaries visible without requiring knowledge of agent frameworks.

Use this as a candidate brief, subject to owner choice: **“Plan a welcoming community science evening for about 80 adults and families, on a Saturday next month, with a modest budget, accessible activities, and a weather-safe fallback.”** This is a fictional planning prompt, not a real booking request or confirmed event. It is relatable and gives the teams meaningful tradeoffs across venue, food, accessibility, safety, budget, programming, and promotion. Do not invent local venue availability, supplier quotes, permits, or legal conclusions.

## Evidence boundary and input modes

The repository currently contains Markdown governance and planning records, not an orchestrator, interface, event database, or running agency. The first proof should use the available coordinator plus separate Luna sessions for bounded roles and an independent reviewer, within the task limit of three concurrent worker sessions alongside the coordinator. A human can pass a shared event brief and collect their written outputs. This is evidence that sessions followed a process in one exercise; it is not evidence of autonomous software, durable agent memory, secured permissions, supplier availability, or successful real-world delivery.

Two input modes remain for the owner to choose:

| Mode | What the exercise uses | Benefits | Limits and controls |
| --- | --- | --- | --- |
| Prepared case (recommended first rehearsal) | A clearly labeled fictional brief, venue/supplier fact cards, fixed budget ceiling, and seeded constraint change | Repeatable, low effort, safe to compare; no external sourcing | Facts are synthetic. Watermark every quote and venue as simulated; assess reasoning and handoffs only. |
| Live-source case | Human-approved public-source research for an agreed location/date, with links, retrieval times, and fact/estimate labels | Demonstrates sourcing workflow and source traceability | Availability and prices change; web research does not confirm inventory or legal permission. No calls, contact forms, accounts, reservations, purchases, or publication. Human reviews sources and obtains quotes separately. |

Prepared inputs are appropriate to prove the workflow before deciding whether live sourcing adds useful audience value. A later live-source demonstration needs explicit location/date, allowed domains/tools, source freshness expectations, and an owner-approved research scope. In either mode, distinguish deterministic checks (schema, arithmetic, presence of citations, budget cap, role and approval gates) from qualitative judgments (theme fit, accessibility quality, clarity, originality, audience appeal). A fluent answer alone proves neither correctness nor model capability.

## Work packages, ownership, dependencies, and gates

Owners below are proposed functional assignments, not standing authority grants. The coordinator assigns named sessions and records each configured model and available runtime session identifier before execution. Every package is planning or rehearsal work; any external commitment remains outside scope.

| Phase / package | Proposed owner | Inputs and dependency | Deliverable and completion gate |
| --- | --- | --- | --- |
| 0. Owner choices and scope | Human owner with coordinator | This plan and agency-design interface draft | Record event choice, audience, prepared/live input choice, location/date if needed, presentation format, and resource ceiling. Gate: coordinator confirms bounded task briefs; unresolved choices stay visibly pending. |
| 1. Demo specification and setup | Coordinator / product hat | Phase 0 choices; this plan plus `agency-design.md` | Freeze the brief, shared event record/schema, role contracts, acceptance criteria, source labels, check sheet, allowed tools, stop/recovery conditions, and output shape. Gate: all four workstream contracts and deterministic checks are ready before any rehearsal session starts; no ambiguous real-world action. |
| 2. One bounded rehearsal: initial proposals | Four workstreams: finance/sourcing; legal/risk; marketing/audience; art direction/curation (including program, accessibility, and cultural fit) | Frozen brief, contracts, prepared fact pack, and check sheet from Phase 1 | All four proposal sections. Dispatch three workers concurrently in the first wave and the fourth as soon as a slot opens; all four are part of this same rehearsal. Gate: each output names its brief version, evidence/provenance, dependencies, alternatives, and decisions for a human. |
| 3. Convergence and controlled change | Coordinator facilitates; affected package owners respond | Initial proposals from Phase 2 | One integrated proposal and decision log for conflicts; then propagate one seeded constraint change through affected sections. Gate: stale sections are identified, dependent outputs revised, and no reserved decision is silently resolved. |
| 4. Fixed-candidate review and coordinator verification | Separate QA/reviewer session, then coordinator | Integrated post-change candidate, criteria, and check evidence | Reviewer findings for traceability, arithmetic, completeness, contradictions, risk language, accessibility, and clarity; coordinator verifies links, same-version handoffs, scope, and acceptance coverage after review. Gate: pass, changes-required, or inconclusive recorded; changed content receives a scoped recheck. |
| 5. Audience demo package | Coordinator with marketing/audience and art-direction/curation owners; human presenter | Reviewed, verified candidate and rehearsal findings | A short visible walkthrough, source/assumption labels, event board, budget/risk summary, and audience questions. Gate: owner approves what is shown and confirms no simulated fact could be mistaken for a real offer. Presentation is not publication or event approval. |
| 6. Post-demo decision | Human owner; coordinator records | Audience feedback and measures | Decide whether to stop, revise, or request a separately scoped plan. Gate: no operational activation by implication. |

The runtime has at most three worker slots alongside the coordinator, so all four functions are covered through staggered dispatch in the single rehearsal: send finance/sourcing, legal/risk, and art direction/curation in the first parallel wave, then dispatch marketing/audience when a slot opens. This preserves parallel initial work while retaining every function. Marketing can draft audience framing and goals immediately, but final channel, schedule, venue-specific copy, and calls to action depend on the event format, program, location/date, and source status; unresolved details remain placeholders. Following convergence and the controlled change, close the workstream sessions, freeze one candidate, and dispatch the separate reviewer. The coordinator verifies after the reviewer returns. Every stream returns the same event ID and brief revision, its owned section, assumptions, provenance, costs/confidence where relevant, dependencies, alternatives, requested changes, open human decisions, and status (`draft`, `ready_for_review`, or `blocked`). The coordinator can integrate proposals, but cannot turn an estimate into an approved commitment. Finance owns arithmetic and scenario comparison; sourcing/research records evidence; legal/compliance identifies questions and routes them to a qualified human; marketing and art direction propose drafts, with human approval required before public use.

## Visible presentation

Show one event brief feeding several clearly named workstreams, then a shared board with the current proposal, budget, sourcing evidence, risk/accessibility flags, theme and run-of-show, and decisions waiting for a human. Label cards as **simulated**, **estimate**, or **source checked at [time]**. Keep a visible change log and show which session supplied each section. Present one concrete disagreement and its resolution path instead of implying unanimous agent consensus. End with “what the agents propose / what still needs a human” and a clear statement that the exercise is a demonstration, not a booking, quotation, compliance sign-off, or execution authorization. A static slide or shared Markdown document is sufficient for the first rehearsal; custom UI is a later decision only if the owner authorizes a separate implementation task.

## Bounded live rehearsal and recovery

Run one rehearsal only, after the brief, shared event record, four role contracts, check sheet, and stop/recovery rules are ready. Use one fictional event and a prepared fact pack. Start three workstreams concurrently; when one completes, dispatch the fourth. The coordinator then integrates their proposals and versioned seeded change, closes the workstream sessions, and dispatches the reviewer against the fixed candidate; coordinator verification follows. At no point should more than three worker sessions be active alongside the coordinator. Set an owner-approved wall-clock limit (suggested planning assumption: 30 minutes), one retry per failed role, and a fixed maximum number of output revisions (suggested: one integration pass plus one reviewer-requested correction). The coordinator records actual usage and stops at the agreed cap; these suggested limits are not approved spend or platform quota.

Exercise one controlled change after initial drafts, such as “the outdoor area becomes unavailable; retain accessibility and the stated cost ceiling.” The coordinator sends the same versioned change to affected roles. Check that affected workstreams revise their sections, finance recalculates if costs change, curation adapts the program, marketing updates dependent draft details, and the later reviewer can trace superseded content. Do not inject or simulate a medical emergency, real weather alert, or actual supplier cancellation; this is a document-change exercise only.

Stop if a session requests external contact or commitment, introduces personal/sensitive data, cannot distinguish simulated from sourced facts, exceeds the time/attempt cap, or produces an unresolved safety/legal concern. Recovery: preserve the last coherent version, mark failed sections `blocked`, show the gap, and have the human facilitator continue with the prepared fallback or end the rehearsal. Do not silently regenerate until a favorable answer appears. If there is no usable independent reviewer, report the rehearsal as inconclusive.

## Checks and measures

Before the rehearsal, the coordinator should create a small check sheet. Deterministic checks should confirm: required fields and event revision exist; every sourced claim has a traceable source or is labeled simulated/estimate; line items sum to totals and remain within the fictional ceiling; each risk has an owner and mitigation or explicit open status; the change propagated to affected outputs; no role claims booking, publication, legal approval, or spending authority; and the reviewer is a separate session. A human reviewer should assess usefulness, coherence, accessibility, theme fit, evidence quality, conflicts surfaced, and whether the audience can identify pending decisions. Mark each check pass/fail/not assessed and keep raw evidence.

Track elapsed time by phase, retries, missing or conflicting fields, arithmetic corrections, unsupported claims, change-propagation coverage, reviewer findings and resolution, and audience comprehension (for example, can attendees state what is simulated and what still needs a human?). Compare prepared and live-source runs only if both are separately approved and use the same criteria. A single rehearsal is a feasibility signal, not a reliable estimate of accuracy, cost, or performance across events.

## Pending owner decisions and next action

Still pending: whether to use this candidate event or another type; prepared case or live-source case; location/date and approved sources if live research is chosen; allowed demonstration surface; time/session/retry ceiling; any spend authorization (none is requested here); and whether to commission later software or an operational trial. These cannot be inferred from the planning request.

**Next action:** coordinator reconciles this plan with `planning/events-agency/agency-design.md`, resolves interface details without erasing open choices, then submits the fixed integrated planning candidate to the assigned separate reviewer. The reviewer should check whether package ownership, gates, evidence labels, rehearsal bounds, recovery, and pending decisions are explicit. Only after review and coordinator integration checks should the owner decide whether any further trial is in scope.

## Handoff evidence

- **Writer/session:** `/root/demo_delivery`; actual deployment session identifier unavailable to this writer.
- **Model:** configured model `gpt-6-luna`; internal deployment identifier unavailable.
- **Base / pinned governance commit:** `5c35200db736c86b6a6e31cd30de8d3af48211de`.
- **Changed path:** `planning/events-agency/demo-delivery.md` only.
- **Checks:** reviewed task acceptance criteria, charter/workflow/access/roles, records convention, and role/task/progress templates; confirmed working tree initially contained coordinator-authored untracked T-GOV task records and left them untouched. No operational rehearsal or automated tests performed; this is a proposal artifact.
- **Limitations:** no owner decisions supplied for event type, input mode, location, presentation environment, or resource cap; no legal, supplier, or market research performed.
- **Next:** separate reviewer assesses the fixed integrated planning candidate; coordinator resolves findings and performs final link/scope verification.
