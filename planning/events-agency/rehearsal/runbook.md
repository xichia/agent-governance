# Runbook — fictional events-agency rehearsal

This pack was assembled as a governance drafting task. Its coordinator for pack drafting was `/root`, model GPT-6. That fact does not assign a future rehearsal session. The source cards and examples are fictional. **No live agency rehearsal is running or authorized by this runbook.** Future work here means a local, fictional exercise only; no contact, booking, payment, personal data collection, commitment, publication or event operation is permitted.

## 1. Freeze scope before dispatch

A future coordinator first confirms the owner has explicitly authorized a rehearsal run and accepted its constraints, success criteria, proposed time/token ceilings, correction limit and any change to the fictional brief. Silence or acceptance of this pack is not run authorization. The starter charter remains unconfigured; authority over real systems cannot be inferred from it.

Record a unique `run-id`, the pinned governance commit, pack commit, brief/source/change versions, acceptance decision, criteria, allowed paths/tools, escalation contact and stop conditions. Give each assigned role an actual agent/session ID and model in its task assignment. The coordinator and reviewer also need recorded identities. Do not use `/root` / GPT-6 from the pack-building task as an implicit future assignment. If a distinct reviewer session cannot be assigned, stop before claiming an independent review.

Apply the following proposed ceilings only if the owner expressly accepts them: one 60-minute total wall-clock run including setup, work, change propagation, review, corrections and final reporting; one session per role (coordinator, four specialists, reviewer), six sessions total and no restart/replacement retries; each specialist up to 8 minutes, 6,000 generated tokens and six model-response turns; coordinator up to 10 minutes, 8,000 tokens and ten turns; reviewer up to 8 minutes, 6,000 tokens and four turns; at most two correction rounds total. One correction round is a single bounded batch of findings routed to affected authors and their returned revisions. These are planning limits, not platform-enforced controls or spending authority. If the owner does not accept them, do not dispatch until revised limits are recorded. Stop when any bound is reached. Record actual tokens and tool usage only when platform telemetry exposes them; when token telemetry is unavailable, record `unavailable`, apply the session/turn/wall-clock bounds, and make no claim that the token cap was enforced.

Create the run directory and assign one writer per artifact:

- `runs/<run-id>/outputs/finance.json`
- `runs/<run-id>/outputs/creative.json`
- `runs/<run-id>/outputs/risk.json`
- `runs/<run-id>/outputs/marketing.json`
- Coordinator only: `runs/<run-id>/candidate/integrated.json` and a change log.
- Reviewer only: `runs/<run-id>/reviews/<candidate-id>.md`.
- Coordinator only: `runs/<run-id>/metrics.md`, created before dispatch and updated through final reporting.

These path conventions organize collaboration; they do not enforce filesystem permissions. Keep the brief, source cards, interface, task criteria and assigned role contract available to each worker. Withhold fixtures and example answers from workers until their outputs are frozen; the reviewer can inspect them if relevant after candidate freeze.

## 2. Dispatch and hand off

Use the assigned contracts: [coordinator](roles/coordinator.md), [finance](roles/finance.md), [creative](roles/creative.md), [risk](roles/risk.md), [marketing](roles/marketing.md), and [reviewer](roles/reviewer.md). Every specialist returns a versioned JSON envelope from the interface, with exact artifact path, session/model, source IDs, dependencies, assumptions, open questions, change acknowledgements, and `ready_for_review` or `blocked` status.

Finance and creative work independently from the same frozen v1 brief/source pack. Neither claims a missing cost is zero or makes external enquiries. Once both matching-version outputs exist, risk reads finance and creative and records both dependency acknowledgements. Once finance, risk and creative are complete and unblocked, marketing reads all three and records acknowledgements. The coordinator checks the handoff metadata and reconciles proposals. A blocked or stale artifact halts its dependent work; return a concrete correction request or escalate rather than integrating around the gap.

For the disclosed closure exercise only, preserve the v1 candidate, apply `CH-001` as the sole predeclared change, publish v2 inputs to affected roles, and log the old/new value, source, authority, affected roles and outcome. Risk and creative reassess their affected plans; marketing removes courtyard references; finance revisits resource costs. All four final handoffs acknowledge `CH-001` and use v2. Any new constraint, mission, source mode, criterion, external action or increased ceiling goes back to the owner as a separate decision.

## 3. Record run metrics

Before dispatch, create `runs/<run-id>/metrics.md` from the record outline below. Keep it current as the run proceeds; before freezing a review candidate, fill in every field observable so far and link the workstream artifacts and validation evidence. Append review and final-verification results after those phases. Record missing telemetry literally as `unavailable`; do not estimate hidden token use or call an unenforced token ceiling a measured or enforced cap.

```markdown
# Run metrics — <run-id>
- Authorization / accepted envelope: <owner decision reference>
- Governance, pack, brief and criteria pins: <exact identifiers>
- Run start UTC / end UTC / total elapsed: <...>
- Outcome: <pass / partial / blocked / inconclusive>

## Phase times (UTC start, UTC end, elapsed wall-clock)
| Phase | Start | End | Elapsed | Notes |
|---|---|---|---:|---|
| Setup and freeze inputs/metrics scaffold | | | | |
| Initial v1 workstreams and handoffs | | | | |
| v1 integration and deterministic checks | | | | |
| CH-001 propagation and v2 workstreams | | | | |
| v2 integration and candidate preparation | | | | |
| Independent review | | | | |
| Corrections / re-review | | | | |
| Final verification and report | | | | |

## Sessions, retries and corrections
| Role | Session ID / model | Start/end | Session starts | Retry/replacement count | Model-response turns | Corrections received |
|---|---|---|---:|---:|---:|---:|
| Coordinator | | | | | | |
| Finance | | | | | | |
| Creative | | | | | | |
| Risk | | | | | | |
| Marketing | | | | | | |
| Reviewer | | | | | | |
- Total distinct sessions / starts: <...> / 6 maximum
- Total retries/replacements: <...> / 0 allowed
- Correction rounds used: <...> / 2 maximum; list each batch and affected roles.

## Usage and coordination
- Token telemetry source: <platform / none exposed>
- Prompt tokens / generated tokens by role: <counts, or unavailable>
- Tool calls by role and tool name: <counts, or unavailable>
- Coordinator interventions: <count and links; distinguish routine handoff from substantive reroute/correction>
- Unsupported factual claims: <count, IDs, disposition; or none observed>
- Cross-team conflicts: <count, options/evidence, resolution or open owner decision; or none observed>
- Change propagation: <CH-001 recipients, v2 acknowledgement IDs, stale/missing responses>
- Reviewer findings: <candidate ID, total, resolved, unresolved, evidence/recheck links>
- Limits hit / stop reason / unavailable metrics: <...>
```

Measure each phase including setup, not only model execution. Distinguish elapsed wall time from summed role time when workers overlap. Report session starts and retries separately from correction rounds. “None observed” requires reviewing the relevant outputs; otherwise say `not assessed`. Unknown or unavailable usage is not zero.

## 4. Integrate and validate

The coordinator integrates only supported proposals into one candidate and resolves conflicts with evidence while preserving open questions. Retain budget arithmetic, schedule/capacity/resource feasibility, room coverage, risk owners and mitigations, source traceability, marketing consistency, exact dependency receipts, matching versions and pending human decisions. Do not mark recommendations as approvals. Run the local deterministic checker on the integrated JSON and record the exact command and result. The checker validates mechanical structure and consistency only; it does not judge creative quality, source truth, legal compliance, real availability, isolation or human approval.

Freeze the review candidate by exact commit or content hash before independent review. Before freeze, update `metrics.md` through candidate preparation and link the current artifact/check evidence. That identifier and the criteria define the review target; any content edit makes a new candidate. Snapshot the candidate and checker evidence so a reviewer can reproduce them. A fixed candidate is required so the reviewer and coordinator assess the same content.

## 5. Independent review and iteration

A distinct reviewer receives the criteria, candidate ID/content, task-relevant sources and verification evidence. Where practical, supply this evidence before the executor's explanation; record if unrestricted history or prior notes reduce independence. The reviewer writes its own verdict and evidence to its review path without editing implementation files. Review must cover scope, completeness, source-to-claim support, arithmetic, capacities, time/resource collisions, access detail, risk fields, dependencies, versions, change acknowledgements, draft-only marketing and edge cases.

A `pass` applies only to the identified candidate and criteria. `changes_required` returns scoped findings to the coordinator; make at most two correction rounds, then freeze a new candidate and obtain a new review or a documented scoped recheck of affected evidence. `inconclusive` means the review gate has not passed. Do not suppress dissent or convert an unresolved decision into approval. If criteria conflict or a residual risk is reserved, escalate to the owner.

The coordinator then reruns the relevant deterministic validation on the final integrated candidate and records its candidate ID, review link/verdict and exact evidence. Complete the reviewer findings/resolution, end time, phase metrics, usage availability and final outcome in `metrics.md`. A review pass alone does not close or activate a task; integration and final verification remain the coordinator's responsibility. No operational event can be activated from this rehearsal.

## 6. Stop, recover and report

Stop dispatch or dependent work if the owner has not accepted the run, identity/version is missing or stale, a required dependency is blocked, criteria conflict, evidence is unavailable, a ceiling is reached, a requested action leaves the fictional/local scope, or review cannot be independent. Mark the relevant artifact/run blocked or inconclusive; record what is preserved, the exact reason, next safe action and owner escalation. Do not improvise a new source, permission, budget, session or authority to get past a stop.

On interruption, resume only after the coordinator checks the pinned policy/task, latest run records, actual candidate and ownership. Reassign with a recorded handoff and new identity/session details; obsolete assignment details do not transfer automatically. Preserve prior candidate and review evidence. If outputs conflict, record both positions and evidence, then route reserved tradeoffs to the owner. Never let a majority vote replace a failed check.

Final reporting separates: (a) fixture/checker results for this pack, (b) evidence from any future agent run, (c) independent review verdict and candidate ID, and (d) limitations and unverified claims. A successful fixture self-test demonstrates only the checker on hand-authored examples. It is not a live run, agent output, independent review, event approval or proof of production readiness.
