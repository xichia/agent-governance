# Plan: a live agent-staffed events agency demo

**Status:** planning proposal; implementation and rehearsal require a new scoped assignment after owner choices. Independent review and integration evidence are recorded in [T-GOV-007](../../records/tasks/T-GOV-007.md).

**Purpose:** let a well-educated general audience watch real Luna sessions turn a client brief into a coherent event proposal, handle a change, and demonstrate independent review and final verification.

**Authority:** planning only. The [charter](../../governance/charter.md) remains unconfigured. This document neither activates an events business nor authorizes bookings, spending, supplier contact, contracts or public marketing. Governance pin: 0.1.1 at `5c35200db736c86b6a6e31cd30de8d3af48211de`.

This is the integrated recommendation. [Agency design](agency-design.md) and [delivery design](demo-delivery.md) are separate Luna contributions, not additional sources of authority. Differences in staffing or sequencing are resolved here. No agency runtime, role pack, fact pack, checker or demo UI has been implemented.

## Recommended starting point

Build a proposal-producing agency first, using prepared fictional supplier facts and real Luna sessions. Start with a local rehearsal coordinated through available session tools and versioned files. Build a custom interface only after the rehearsal shows what the audience needs to see.

Candidate commission, **not yet chosen:** a small community science-and-culture evening, combining short talks, art, accessible activities and food. This gives budgets, sourcing, risk, marketing, art direction, themes and curation real dependencies without requiring the audience to understand code. Do not fix a venue, currency, attendance, date or cost ceiling until the owner chooses the brief; illustrative numbers are not approvals.

Prepared facts let the audience judge agent work against known prices, capacities and availability. Live public-source research is an alternative after location/date, allowed sources and freshness requirements are agreed. Research can identify options; it does not confirm availability, obtain a quote or authorize a transaction. Prepared input mode remains a recommendation, not an approved choice.

## Staffing and parallel work

| Function | Exclusive output ownership | Required handoffs |
| --- | --- | --- |
| Coordinator / producer | Event brief, shared event record, assignments, conflict log, integrated proposal and final verification | Versioned brief and changes to all affected teams; collects dependency acknowledgements |
| Finance and sourcing | Supplier option ledger and budget | Priced options, tax/fee basis, capacities and constraints to creative/risk; final cost consequences to coordinator |
| Legal and risk | Advisory risk/issues register | Venue/activity/accessibility/contract questions to affected teams; unresolved matters to owner or qualified specialist |
| Marketing and audience | Positioning, campaign proposal and draft attendee copy | Audience needs to creative; factual copy from reconciled programme, venue and budget |
| Art direction, themes and curation | Creative concept, visual direction, programme and run-of-show | Programme/resource needs to finance/sourcing and risk; confirmed content to marketing |
| Independent reviewer | New review record only | Findings against the exact candidate; no edits to the reviewed artifacts |

Four workstreams cover the requested functions without requiring seven permanent departments. Split finance from sourcing or art direction from curation only if rehearsal evidence shows a bottleneck. Every function is covered even when two functions share a session; the reviewer never reviews its own authored content.

**Available concurrency:** this environment supports the coordinator plus up to three active workers. First wave: finance/sourcing, creative/curation, and legal/risk. Risk can produce a preliminary checklist from the common brief, then assess the returned venue/activity options. Second wave: marketing uses those options while affected teams resolve changes. Use separate sessions but stagger execution; do not promise four simultaneous workers with the current capacity. Dispatch the independent reviewer after implementers stop editing and the integrated candidate is frozen. A later runtime may support more concurrent workers without changing ownership or review rules.

All teams receive the same brief and evidence pack. Outputs may remain preliminary until dependencies are satisfied. For example, marketing can develop positioning early but must refresh event details before final review. A shared assumption never becomes confirmed through repetition.

## What we need to build

| Work package | Owner and dependencies | Concrete outputs | Gate before proceeding |
| --- | --- | --- | --- |
| 1. Adopt the bounded demo brief | Human owner + coordinator; depends on owner choices below | Context, named actors, input mode, environment, allowed data/tools, event constraints, task and resource ceilings | Explicit bounded rehearsal authority; operational business stays inactive |
| 2. Write the role and interface pack | Scoped Luna writers; depends on 1 | One agency context document, four role contracts, coordinator/reviewer instructions, common data schema, handoff/change formats | Separate review confirms complete responsibilities, nonoverlapping paths and compatible interfaces |
| 3. Prepare the case and checks | Data/check writer on a separate path; depends on approved brief and schema; can parallelize with role drafting once interfaces are pinned | Versioned evidence cards, reference arithmetic, check sheet or small validator, controlled-change card | Fact provenance and expected checks verified separately; no hidden contradictions or unstated acceptance criteria |
| 4. Run one complete live rehearsal | Coordinator + four staggered workstreams + separate reviewer; depends on reviewed 2 and 3 | Actual outputs, conflict/decision records, change acknowledgements, fixed-candidate review, integrated verification and usage record | Acceptance passes, or documented failed/inconclusive outcome; stop rules honored |
| 5. Build the presentation | Marketing/art direction or UI writer; depends on rehearsal evidence | Audience view, presenter sequence and clear fact/evidence labels | Separate review of accuracy and usability; all displayed claims trace to actual run evidence |
| 6. Deliver and assess | Human presenter + coordinator; depends on rehearsal and presentation gates | Fresh bounded live run or explicitly labeled rehearsal replay; audience feedback and follow-up decision | Preserve evidence; owner decides whether to iterate or authorize a separate business/runtime project |

Each work package gets its own task, policy/configuration pin, named writer, reviewer, paths and bounds. These are future assignments, not permissions created by this plan. The first build milestone is the reviewed role/interface pack and prepared case; the first performance milestone is one end-to-end rehearsal. A successful demo is not operational activation.

## Role instructions and interaction contracts

Keep common operating rules in one `AGENTS.md` linked to governance. Use separate role documents loaded with each task; duplicating a long policy in every prompt creates competing instruction sources. Use the existing [role](../../templates/role.md) and [task](../../templates/task.md) templates. A role contract must specify:

- Identity/function, accountable person and substitute; actual configured model and session.
- Mandate, observable outputs and acceptance checks.
- Required inputs, dependencies, owned files and output format.
- Routine decision rights; human-reserved decisions and escalation triggers.
- Read/write/tool scope, actual runtime grantor/operator, limits, expiry and handoff.
- Independent review requirements, evidence/provenance conventions and prohibited conflicting duties.

**Common data:** event ID, brief version, audience, attendance, venue/options, currency, cost ceiling, programme times, accessibility needs, source cards, budget lines, risks, assumptions, decisions and pending approvals. Money needs units, tax/fee treatment and contingency assumptions; times need date/time-zone or explicitly fictional local-time convention. Stable IDs connect programme activities, venue/supplier options and costs. Unknown is distinct from zero, verified or approved.

**Handoff:** event/brief version; artifact and writer; source references; assumptions; dependency requests; proposed changes; unresolved questions; ready/blocked status. Receiving teams acknowledge the version and any unmet prerequisite.

**Change:** coordinator records old/new values, decision authority, affected teams and criteria that remain fixed. Shared operational assumptions can be reconciled within the assignment; mission, acceptance, additional risk, budget ceiling, permissions and external commitments remain owner decisions. Stale outputs are flagged; no unacknowledged version is silently integrated.

**Conflict:** surface options, evidence and cost/programme implications. Coordinator resolves routine integration within approved constraints; unresolved priorities and risk acceptance go to the human owner. Preserve disagreement. Majority preference is not a correctness check.

## Runtime and demo surface

For the first rehearsal, use coordinator-dispatched separate Luna sessions with scoped context, disjoint files, saved outputs and fixed Git candidates. This avoids building an autonomous scheduler before proving the contracts. The coordinator remains responsible for dependency dispatch, retry accounting, recovery and integration.

Session tools and scoped prompts coordinate behavior; they do not establish file ACLs, authenticated business identities or isolation. Record what the actual platform grants and what cannot be enforced. In cooperative mode, demonstrate detection/escalation of an out-of-scope request. Claim technical denial only with an operator-enforced boundary and direct denial evidence from harmless authorized test resources.

The audience view should show the client brief, workstream state, visible proposal changes, budget, source/assumption labels, review findings and pending human decisions. Display actual session progress and evidence rather than fabricated chat between agents. A shared document or simple board is sufficient initially; a custom dashboard and automatic scheduler are later scoped options. A recorded fallback must be labeled as replay and cannot be presented as a live completion.

## Rehearsal and validation

1. Freeze the authorized brief, criteria, input pack, role/schema versions and resource envelope.
2. Dispatch the first wave, receive explicit handoffs, then run marketing and needed revisions. Integrate a coherent initial proposal without changing acceptance criteria.
3. Introduce one **disclosed, preauthorized document change**: for example, an outdoor area becomes unavailable while attendance, accessibility and the cost ceiling stay fixed. Propagate the version to all affected teams. This is fictional scenario information, not an actual cancellation or emergency.
4. Freeze the revised integrated candidate. A fresh Luna reviewer checks artifacts and evidence before receiving the executor's verdict where practical. Disclose shared-history or prior exposure; call this evidence-first, not blind review.
5. Fix findings within the agreed cap. New content receives new review or an explicitly scoped recheck. Coordinator verifies the resulting integrated artifact and records closure only after required checks pass.

Keep natural review findings as observed; do not guarantee or fabricate a defect to make the story exciting. A failed-check demonstration can be a separately labeled authorized fixture, with its expected failure established before the run. An interruption/handoff exercise is a later optional trial, rather than adding every governance stress case to the first demo.

| Check | Evidence required |
| --- | --- |
| Budget | Recomputed line-item totals, fees/tax assumptions and contingency; total within the fictional approved ceiling |
| Programme and resources | No impossible room/staff/equipment overlaps; activities fit the supplied capacity/time constraints |
| Provenance | Every material price, availability and factual claim traced to a case card/public source or labeled estimate/unknown |
| Cross-team coherence | Same brief version; matching venue, attendance, programme and marketing facts; all changed dependencies acknowledged |
| Risk and boundaries | Each material issue has an owner and mitigation/open status; no draft claims legal clearance or unauthorized commitment |
| Review and integration | Separate reviewer, exact candidate, verdict, scoped rechecks and final integrated checks recorded |
| Audience clarity | Audience can identify who owns decisions, what is fictional, what was actually checked and what still needs a human |

Use deterministic tools for arithmetic, required fields, versions and schedule/resource conflicts where inputs permit. Separate review assesses theme fit, usefulness, clarity, unsupported assumptions and edge cases. Legal/risk identifies questions; the demo does not provide legal sign-off. An inconclusive check is not a pass.

Measure elapsed time including setup, role/review retries, actual model/tool usage where exposed, coordinator interventions, unsupported claims, cross-team conflicts, change propagation and findings resolved. Report missing cost telemetry as unavailable. A single run is a feasibility demonstration; no claim of superiority over a baseline without a separately authorized matched comparison.

## Proposed resource and recovery envelope

Before dispatch, agree total wall-clock and resource ceilings covering setup, all workers, review and integration. Starting rehearsal proposal: one event, four workstreams, three concurrent workers maximum, one disclosed change, no more than one retry per failed worker and two review/fix rounds. If usage cannot be measured, bound sessions, turns and wall-clock instead and disclose that this is not a measured spending cap. No paid-service authorization is included.

Stop dependent work on unauthorized action/data exposure, unresolved critical safety/legal issue, missing independent reviewer, exhausted limits or failed recovery. Preserve last known state and evidence; report partial results. For an interrupted worker, transfer exclusive ownership, acknowledge the pinned task and actual artifacts, and have the authorized operator revoke obsolete runtime grants if any. Resume only after the blocker is resolved; never reconstruct completion from a favorable summary.

## Owner choices needed for the first build assignment

1. **Commission:** science-and-culture evening, another festival, corporate launch or private celebration; desired audience and final deliverable.
2. **Inputs:** prepared fictional fact pack (recommended first) or bounded public-source research. If live, location/date and allowed sources.
3. **Event constraints:** attendance, fictional budget/currency, venue/time constraints, accessibility and priorities.
4. **Demonstration:** local/private rehearsal first; eventual audience surface and live-versus-replay fallback preference.
5. **Execution limits:** allowed models/tools/data, wall-clock, session/retry ceilings, resource telemetry and escalation contact.

Once these choices are supplied, create the bounded build/rehearsal assignment and draft the role/interface pack plus case data on separate paths. Do not start an operational event agency from acceptance of this planning document alone.
