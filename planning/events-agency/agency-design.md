# Events agency: team and interface design

**Status:** planning proposal only; no agency is activated.  
**Task / policy:** T-GOV-007; charter 0.1.1, commit `5c35200db736c86b6a6e31cd30de8d3af48211de`.  
**Author:** `/root/agency_design` (session/agent identifier), configured model `gpt-6-luna`; internal deployment identifier unavailable in this environment.  
**Scope:** assigned contribution to `planning/events-agency/agency-design.md`; no external research or operational actions.

## Smallest useful team

Use one coordinator/integrator, four parallel workstream agents, one integrator-selected independent reviewer, and the human owner. Coordinator and reviewer are separate sessions; reviewer cannot author reviewed content. The four workstreams are:

| Workstream | Owns | Produces |
|---|---|---|
| Finance and sourcing | Cost model, quote/option comparison, supplier-input ledger | Budget with ranges, assumptions, source status, and decision points |
| Legal and risk | Issue spotting, compliance questions, risk register and mitigations | Advisory checklist with escalation triggers; no legal clearance |
| Marketing and audience | Audience framing, positioning, channel/content proposals | Draft campaign concept and measurable audience goals |
| Art direction and curation | Themes, program/experience, accessibility and cultural fit | Curated concept options linked to brief and constraints |

Do not create separate departments for each title. The coordinator owns the event brief, common schema, assignment/dependency tracking, conflict log, and final package. Every workstream has one named writer and one output path. Reviewer reviews the fixed integrated candidate against task criteria; it does not rewrite it. Human owner resolves priorities and reserved decisions.

### Parallel dependency graph

```text
Human chooses event type / input mode / limits (pending)
                     |
Coordinator publishes versioned event brief + shared schema
       |             |              |                 |
    Budget &       Legal &       Marketing &      Art direction &
    sourcing        risk          audience          curation
       \             |              |                 /
        +------ shared proposal handoffs / conflict log -----+
                               |
Coordinator resolves dependencies, flags unresolved choices
                               |
Independent reviewer checks fixed candidate and evidence
                               |
Human reserved decisions; coordinator integrates/reports
```

Workstreams can run in parallel after the brief is frozen. Midstream changes to audience, capacity, venue constraints, date, spend ceiling, or input mode are versioned by the coordinator; affected workstreams acknowledge and revise their outputs. Do not merge incompatible assumptions into a single “agreed” value. Record competing options and the decision owner.

## Role instructions and authority

Use one common instruction source (AGENTS.md plus pinned governance) for workflow, boundaries, evidence, escalation, and record rules. Each task assignment adds a short role contract using the fields in `templates/role.md`: identity/model; accountable person/substitute; policy pin; mandate/outcomes; inputs/outputs/interfaces; local decision rights; reserved decisions/escalation; read/write/tools; runtime grantor/enforcer; budget/expiry; review/conflicting hats; activation decision. A task contract narrows this further with the single owned output path, acceptance checks, and handoff deadline. Avoid copying policy paragraphs into every role: duplication drifts. Roles and prompts express intended behavior; they do not technically enforce permissions.

Runtime enforcement is a separate control plane. In any future rehearsal, the operator must verify which identity actually runs each session, exposed files and tools, credentials, limits, expiry and revocation, and any external-action gate. Separate prompts, worktrees, Markdown ownership, or agent titles are not access controls. Claim only observed UI/runtime controls; otherwise report enforcement as unverified. No runtime tool grants or operational agents are authorized by this plan.

## Shared event record

Coordinator maintains one versioned event record; agents propose changes through their owned outputs or a structured handoff, not by silently overwriting shared facts.

| Field group | Minimum fields |
|---|---|
| Identity and scope | `event_id`, `brief_version`, purpose, status (`proposal` / `assumption` / `owner_decided` / `verified`), last_updated_by, timestamp |
| Audience and experience | audience, capacity range, accessibility needs, program/theme options, success measures |
| Constraints | candidate date/time, location/format, spend ceiling and currency, safety constraints, excluded activities |
| Budget and sourcing | line item, low/high estimate, tax/fee basis, supplier/option, availability/quote status, quote date/expiry, source reference, contact/action status |
| Risk and legal questions | hazard/obligation question, affected activity, severity/likelihood rationale, proposed mitigation, owner/counsel escalation state |
| Marketing and curation | audience claim, channel, draft content/link, evidence needed, responsible owner, publication status |
| Decision and change log | decision/change ID, old/new value, rationale, affected workstreams, approver or pending owner, effective brief version |

Every material figure, supplier claim, legal premise, availability claim, and audience assertion carries provenance: source identifier or “agent estimate”; observation date; author; confidence/unknowns; and whether independently verified. Label illustrative values and prepared/mock inputs visibly. Never present an estimate as a quote or a legal question as a determination. Empty or unknown fields remain explicitly unknown, not zero or implicitly approved.

## Handoffs and change control

Each workstream handoff includes: brief version used; owned artifact/link; recommendations and alternatives; evidence/provenance; assumptions and unresolved questions; dependencies or conflicts; changes needed from another stream; and a concise ready/blocked status. Receiver acknowledges the version and either accepts the dependency, requests a correction with the disputed field/evidence, or records a conflict for coordinator resolution.

An update to a shared assumption is a proposal until the coordinator records its source and impact. Changes affecting purpose, event type, input mode, audience, risk tolerance, budget ceiling, external actions, or evaluation criteria require human owner decision where reserved or presently pending. Coordinator propagates approved brief versions and marks stale outputs for refresh; no downstream output may imply approval by silence.

## Human decisions and specialist limits

Pending owner choices include event type and audience, prepared versus live supplier inputs, environment, actual budget and currency, whether a bounded rehearsal may use real-world data, acceptable risks, and any later operational activation. Owner approval is required before supplier contact, booking, spending, contracts, collecting attendee data, publishing/sending campaign materials, or opening an audience event. Suggestions or sample figures do not approve these actions.

The legal/risk workstream may identify questions and propose mitigations. It cannot provide binding legal advice, determine compliance, approve permits/insurance/contracts, accept liability, or replace qualified local counsel and accountable human review. Escalate jurisdiction-dependent questions and unresolved safety/privacy concerns to the owner and qualified specialists before any real event. Finance estimates do not authorize expenditure; sourcing does not authorize supplier outreach or commitments; marketing does not authorize publication; curation does not authorize activities that create safety or access obligations.

## Review and integration gates

Coordinator checks that every workstream uses the same brief version, unknowns and estimates are labeled, handoffs are complete, cross-stream conflicts are visible, dependencies have owners, and no reserved action is represented as authorized. The independent reviewer receives fixed candidate artifacts, criteria, and evidence and records pass/changes-required/inconclusive. A reviewer pass is limited to that candidate; changed content requires scoped recheck or new review. Coordinator performs integration checks after review, including local links, schema consistency, scope/authority language, and task acceptance coverage. Only then can the coordinator report readiness for owner decisions; this design alone is not evidence that an actual runtime enforces boundaries or that the event is ready to operate.

**Handoff to coordinator:** align `demo-delivery.md` with the proposed four workstreams, shared event record and change/handoff rules. Coordinate on the illustrative brief and pending human choices. Treat runtime enforcement claims as unverified unless the rehearsal records direct evidence.
