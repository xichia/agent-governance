# Task: T-GOV-007 — Plan the live events-agency demo

- **Status:** done
- **Human owner / escalation contact:** requesting user, this conversation
- **Coordinator / integrator:** `/root`, Codex GPT-6 (exact deployment identifier unavailable)
- **Implementers:** separate Luna sessions `agency_design` and `demo_delivery`; actual IDs recorded after assignment
- **Reviewer:** separate Luna session `plan_review`, assigned against a fixed candidate
- **Governance:** charter 0.1.1 at `5c35200db736c86b6a6e31cd30de8d3af48211de`
- **Branch:** `codex/governance-demo` · **Base:** `5c35200db736c86b6a6e31cd30de8d3af48211de`
- **Authority:** user explicitly requested Luna workflow to plan the live events-planning business demo
- **Bounds:** planning only, this session; two independent drafting sessions and one review session; maximum two review/fix rounds; no paid services, external commitments or operational activation

## Objective and acceptance

Produce a concrete, reviewable implementation plan for an agent-staffed events agency serving a well-educated general audience. Cover budgets, sourcing, legal/risk, marketing, art direction, themes and curation, with parallel scoped work and a separate review gate.

Acceptance:

1. Distinguish current Markdown governance from proposed runtime and demonstration evidence.
2. Define work packages, dependencies, owned outputs and gates through a first live rehearsal and audience demo.
3. Specify role-contract contents, common event data, inter-agent handoffs, cross-team conflicts, review and final verification.
4. Include a relatable proposed event brief, bounded change/failure exercise, deterministic checks, measured evidence and a feasible starting footprint.
5. Mark unchosen event type, input-source mode, environment, budgets and owner approvals as pending; do not interpret a suggestion as user approval.
6. Preserve current governance and history. Scope planning artifacts only; do not run operational agents, source suppliers, spend, book, publish, or give legal approval.
7. Separate Luna reviews a fixed candidate; coordinator verifies the integrated artifacts and local links before closure.

## Assignments and access

- `agency_design`: read governance, this task and relevant templates; write only `planning/events-agency/agency-design.md`. Design staffing, role instructions, shared data and interfaces. Do not edit governance or the other draft.
- `demo_delivery`: same read scope; write only `planning/events-agency/demo-delivery.md`. Design work packages, rehearsal, presentation and validation. Do not edit governance or the other draft.
- `/root`: write `planning/events-agency/PLAN.md`, this task, own progress, README planning link and dated cancellation entry in T-GOV-006. Integrate accepted contributions without replacing writers' records.
- `plan_review`: read pinned policy, task, candidate artifacts and verification evidence; write only `records/reviews/R-GOV-007-01.md` (or `-02.md` for recheck). No implementation edits.
- Tools: local read/write and checks; coordinator alone performs scoped Git commits. Cooperative shared repository, not enforced per-agent isolation.
- Dependencies: existing governance and templates; no active agency charter or operational trial authorization.

## History

- 2026-10-05: proposed → ready → active. User requested Luna planning. Coordinator reserved disjoint paths and separate review. Earlier scripted-demo task cancelled rather than silently migrated. New work does not amend governance or activate the agency.
- 2026-10-05: active → review. Separate `gpt-6-luna` sessions `/root/agency_design` and `/root/demo_delivery` delivered their disjoint contributions. Coordinator reconciled four workstreams, three-worker concurrency, dependency waves and one rehearsal sequence in PLAN.md. Fixed candidate commit and independent review pending. The branch name is retained from the cancelled drafting task; it is not operational authorization.
- 2026-10-05: review → active. Separate `gpt-6-luna` reviewer `/root/plan_review` returned changes-required in [R-GOV-007-01](../reviews/R-GOV-007-01.md) against `35bcaee70c6df0dbc9b9e73ba32bc7e5ba9fa616`: agency-design contribution still depicted four simultaneous workers. Coordinator requested its assigned author align the contribution with the integrated three-worker schedule. Criteria unchanged; second and final review round follows a corrected candidate.
- 2026-10-05T05:35Z: active → review. Assigned author corrected agency-design.md description, diagram and handoff sequencing to show three-worker waves and dependent marketing/risk follow-up. Coordinator inspected the diff; working diff whitespace check passed. Fixed correction candidate and scoped independent recheck pending; no acceptance criteria changed.
- 2026-10-05T05:38:43Z: review → done. Separate Luna scoped recheck [R-GOV-007-02](../reviews/R-GOV-007-02.md) passed corrected candidate `cc171f20e7acb0f3692e250059e252ce8f1682f9`, preserving prior evidence for unchanged artifacts. Integrated by fast-forward into canonical `main` at `354af03ff6b5b86b2e55ea11f9f8e6130e2fa12b`. Coordinator verified reviewed planning artifacts and README exactly match the passing candidate, governance/AGENTS.md remain unchanged from the pin, integrated diff whitespace check passed, 45 Markdown files / 106 local links had zero unresolved targets, and the tree was clean. Closure edits only task/progress records; plan acceptance does not authorize implementation, rehearsal or agency operation. Outcome and remaining owner choices are in [PLAN.md](../../planning/events-agency/PLAN.md).
