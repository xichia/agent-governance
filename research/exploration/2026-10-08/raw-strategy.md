# Raw ideas — coordination strategy

Originating lens: coordination strategy  
Contributor: session `/root/ideation_strategy`; configured model `gpt-6-luna`; actual backend deployment identity unavailable. Generic system GPT-6 wording and the configured model do not independently verify the backend.  
Source brief: `BRIEF.md`, dated 2026-10-08. Generation only; these ideas have not been evaluated or shortlisted.

## S01 — Version-bound handoff receipts

**Idea:** Make each dependent handoff identify the assignment, upstream artifact path and version/content digest, and the receiving role's accepted input. The coordinator checks the receipt against the artifact actually supplied before treating downstream work as ready. A receipt mismatch routes to a bounded re-acknowledgement step.

**Proposed observable test:** In a local synthetic workflow, supply a correct upstream artifact, then separately substitute stale bytes, change the path, and provide a receipt with a mismatched assignment. Record whether each mismatch is caught before downstream acceptance and whether a valid receipt still passes.

**Assumption needing verification:** The available runtime can expose stable artifact identity and the coordinator can compare it with what the downstream session actually received; a digest alone would establish byte identity, not who authored or read the bytes.

## S02 — Readiness gates tied to decision criteria

**Idea:** Use explicit task gates between draft, reviewable candidate, and operationally ready states. Each gate names its evidence and unresolved owner decision; a review pass advances only the state whose criteria were checked. Unknown real-world conditions remain visible blockers rather than being absorbed into a general “approved” label.

**Proposed observable test:** Build a small synthetic task with a passing document review but an unresolved seating/service decision. Check that the workflow records the review result while preventing the operational-readiness state, then allow transition only after the named evidence/decision is supplied.

**Assumption needing verification:** The chosen state labels and evidence rules can be applied consistently across task types without obscuring legitimate cases where operational readiness is out of scope.

## S03 — Event-based coordination ledger

**Idea:** Record coordination as timestamped events for setup, dispatch, queue/wait, response, correction, integration, review, and verification, with an explicit source and precision for each time. Derive elapsed and active intervals from events while preserving overlap and missing telemetry as unknown; do not infer overhead by subtraction.

**Proposed observable test:** Replay a scripted workflow containing parallel work, a queue delay, one correction, and an untimed setup interval. Compare the ledger's reported wall time and per-role active intervals with the script's known intervals; verify that overlap is not double-counted as wall time and unavailable intervals remain marked missing.

**Assumption needing verification:** The platform or task wrapper can provide event times with enough precision and provenance to distinguish observed runtime events from agent-reported estimates.

## S04 — Resource reconciliation at coordination boundaries

**Idea:** Add a coordinator-owned reconciliation step whenever a task changes phase or service state: compare declared demand with the latest source inventory and named staff/resource assignments, then route any mismatch to the responsible owner before integrating the plan. Keep explicit exception paths for tasks that do not consume the resource in question.

**Proposed observable test:** Use a synthetic plan with 80 seated attendees and an inventory changed from 80 to 40 chairs between draft and integration. Check whether the coordinator blocks or flags integration, identifies the changed source and demand, and accepts a matched inventory case plus a declared standing exception.

**Assumption needing verification:** Relevant resource demand can be represented in structured fields and the coordinator can identify which source inventory version is authoritative for each phase.

## S05 — Matched coordination-topology rehearsal

**Idea:** Compare a four-specialist coordination layout with a predeclared smaller layout on matched synthetic tasks, holding the brief, change event, acceptance criteria, review requirement, and available resource envelope constant. Record output acceptance, escaped issues, corrections, human interventions, elapsed time, and whatever usage telemetry is available before deciding whether to combine roles.

**Proposed observable test:** Design and, if the bounded week permits, run paired repetitions for both layouts using the same task variants and blind-to-condition scoring rubric where feasible. Publish per-run outcomes and missing measures; do not infer comparative efficiency from one rehearsal or unmatched durations.

**Assumption needing verification:** Enough equivalent task variants and runtime availability exist to make the comparison informative within the seven-session limit; if not, this period can produce only the protocol, not a reliable staffing conclusion.
