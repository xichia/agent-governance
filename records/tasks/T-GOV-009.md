# T-GOV-009 — Build the fictional events-agency rehearsal pack

- **Status:** active
- **Owner / escalation:** requesting user in this chat
- **Coordinator / executor:** `/root`, GPT-6; deployment identifier unavailable
- **Review method:** owner explicitly invoked Luna workflow during implementation. Separate Luna workers and a separate fixed-candidate Luna reviewer; coordinator integrates and verifies. Future Luna use remains upon request.
- **Governance:** charter 0.1.1; current instructions at `10546edf45c962a92016389eeeafc5985b5fb9f3`
- **Branch / base:** `work` / `10546edf45c962a92016389eeeafc5985b5fb9f3`
- **Authority:** user said “Let's do it” after the suggested next step: choose demo brief/inputs/limits and build role/interface pack plus case data. Adopt the suggested fictional science-and-culture evening for drafting. Numeric constraints are explicit editable rehearsal defaults, not real event approvals.
- **Bounds:** one local drafting assignment; two Luna implementers, one separate Luna reviewer, at most two correction rounds. No live agency rehearsal, network research, paid services, contact, publication, bookings or operational activation.

## Scope and acceptance

Write `planning/events-agency/rehearsal/`, this task and own progress; update README and HANDOFF continuation pointers. Preserve historical planning and governance.

1. Provide one fictional brief, four specialist contracts, coordinator/reviewer contracts, owned output paths, handoff/change interfaces and dispatch instructions.
2. Provide provenance-labeled source cards and a disclosed outdoor-closure change with stable IDs and two brief versions.
3. Provide a deterministic, standard-library validator and hand-authored initial/revised examples; label examples as fixtures, not agent work.
4. Verify source/card references, arithmetic, capacities, resources, same-version handoffs, dependencies, risk fields and change acknowledgements. Include meaningful negative checks.
5. Report exactly what validation establishes; live-run outcome remains unverified and independent pack review must be evidenced.

Independent review must pass a fixed candidate; coordinator must verify integrated artifacts before closure. Separate review evaluates pack readiness only, not a live rehearsal.

## Assignments

- `/root/roles_pack`: configured `gpt-6-luna`; owns only `rehearsal/roles/*.md` and `rehearsal/runbook.md`.
- `/root/case_checker`: configured `gpt-6-luna`; owns only `rehearsal/case/*.json`, `rehearsal/fixtures/*.json` and `rehearsal/tools/check.py`.
- `/root`: coordinator GPT-6 owns remaining scoped documentation, task/progress, integration and Git operations.
- Separate reviewer reserved as `/root/pack_review`, configured `gpt-6-luna`; writes only `records/reviews/R-GOV-009-01.md` (or `-02.md` for recheck).
- Runtime: cooperative shared filesystem and local tools; intended ownership is not enforced isolation. Local checks only; no supplier lookup or external messages.

Dependencies: reviewed T-GOV-007 plan; existing templates and T-GOV-008 review preference. Cooperative shared repository; Markdown scope does not enforce ACLs. No other writer active. User is the escalation contact; no substitute assigned for this local task.

## Handoff

Start at [rehearsal README](../../planning/events-agency/rehearsal/README.md). Run `python3 planning/events-agency/rehearsal/tools/check.py --self-test` from repository root. Future run must assign actual sessions/models and pin the pack; proposed run limits are not platform grants.

## State history

- 2026-10-05: proposed → ready → active. `/root` acknowledged continuation, inspected actual clean Git state and recorded the drafting scope. No live rehearsal started.
- 2026-10-05: user explicitly requested Luna workflow now and upon future request. Direct-check review method superseded before completion; two independent implementation paths dispatched with shared brief/interface and a separate review gate. No agency worker sessions dispatched; these are pack-building sessions.
- 2026-10-05: active → review. Both Luna implementers delivered scoped paths. Coordinator reconciled source resource semantics with the interface, reran 16 checker cases and both CLI fixtures, and checked local links/diff whitespace. Freeze a committed candidate for the separate reviewer; no live-run outcome or independent pass claimed yet.
