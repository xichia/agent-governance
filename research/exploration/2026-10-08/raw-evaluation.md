# Raw evaluation, recovery and overlooked-needs ideas

## E01 — Test service-state accounting for the unresolved rejoin case

- **Lens:** Evaluation and overlooked needs
- **Origin:** Configured model: `gpt-6-luna`; session: `/root/ideation_evaluation`; actual backend deployment identity unavailable
- **Idea:** Evaluate whether a proposal accounts for each attendee, seat and staff duty through every service and transition state, including a quiet-room attendee rejoining during refreshments. Keep unknown venue or service conditions distinct from internal design gaps.
- **Proposed observable test:** Give the evaluator matched scenarios that differ only in whether the rejoin transition is specified. Check whether it identifies any state with unaccounted attendance, seats or staff duties, and whether it labels unresolved external conditions as unknown instead of resolved. Compare its findings with a prewritten state-by-state checklist.
- **Assumption needing verification:** The current report's open refreshment rejoin case can be represented in a compact scenario without requiring unstated venue facts, and the checklist can distinguish an internal omission from a genuinely unknown condition.

## E02 — Probe checker coverage against cross-field contradictions

- **Lens:** Evaluation and recovery
- **Origin:** Configured model: `gpt-6-luna`; session: `/root/ideation_evaluation`; actual backend deployment identity unavailable
- **Idea:** Measure whether validation catches contradictions that appear only when structured values, prose and source inventories are compared, building on the report's synthetic probes for chair inventory/demand and audience counts.
- **Proposed observable test:** Run a fixed set of valid and deliberately inconsistent fixtures through the current checker and a candidate cross-field validator. Include a reduced chair inventory, omitted required chair accounting, and free text with a larger audience than the structured count; record acceptance, rejection or explicit review flag for each case and whether valid fixtures remain accepted.
- **Assumption needing verification:** The relevant structured fields and prose are available to a local, isolated validator, and expected outcomes can be specified without imposing a literal-copy rule that is absent from the written contract.

## E03 — Exercise bounded recovery from a failed handoff

- **Lens:** Recovery
- **Origin:** Configured model: `gpt-6-luna`; session: `/root/ideation_evaluation`; actual backend deployment identity unavailable
- **Idea:** Test a delivery-recovery policy for startup or response failures so an incomplete handoff cannot be treated as accepted work and retries do not silently change the assignment or exceed a declared limit.
- **Proposed observable test:** In an isolated mock, inject a startup failure, a missing artifact, and a late response. Check that each event is recorded, no absent or partial artifact is accepted, retry/stop behavior follows a predeclared bound, and any reassignment carries the exact task inputs and current state.
- **Assumption needing verification:** A local mock can exercise the acceptance and reassignment logic without representing unavailable platform runtime behavior as observed fact.

## E04 — Check whether handoff receipts identify the actual dependency

- **Lens:** Evaluation and overlooked needs
- **Origin:** Configured model: `gpt-6-luna`; session: `/root/ideation_evaluation`; actual backend deployment identity unavailable
- **Idea:** Evaluate dependency receipts against the exact upstream artifact identity, since the report says current receipts do not bind the exact upstream content.
- **Proposed observable test:** Supply receipts for the correct path/version/content, then substitute bytes, path or version while keeping a plausible receipt string. Verify that the coordinator's local check accepts only a receipt matching the assigned dependency, and that reissued content requires a new receipt.
- **Assumption needing verification:** The proposed task envelope can expose stable path, version and content identifiers, and the validation can check them without treating a hash as proof of authorship or authorization.

## E05 — Measure recovery and coordination events without inferring overhead

- **Lens:** Evaluation
- **Origin:** Configured model: `gpt-6-luna`; session: `/root/ideation_evaluation`; actual backend deployment identity unavailable
- **Idea:** Assess whether event-level records support useful elapsed-time and recovery comparisons while preserving missing telemetry as missing, rather than estimating coordination cost by subtracting worker windows from wall time.
- **Proposed observable test:** Record setup, dispatch, queue, response, integration, correction, review and verification events in two matched local rehearsals, including overlapping intervals and an injected wait/failure. Check whether the report can reconstruct elapsed intervals and interventions, labels unavailable measurements, and avoids reporting residual time as coordination overhead.
- **Assumption needing verification:** Event timestamps and a matched rehearsal can be captured within the bounded sessions; any unavailable platform queue or usage data can be explicitly omitted without undermining the local comparison.
