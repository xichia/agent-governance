# T-GOV-009 — Build the fictional events-agency rehearsal pack

- **Status:** review
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
- Separate reviewer reserved as `/root/pack_review`, configured `gpt-6-luna`; writes only `records/reviews/R-GOV-009-01.md`, `-02.md` and `-03.md` for the initial review and two bounded rechecks.
- Runtime: cooperative shared filesystem and local tools; intended ownership is not enforced isolation. Local checks only; no supplier lookup or external messages.

Dependencies: reviewed T-GOV-007 plan; existing templates and T-GOV-008 review preference. Cooperative shared repository; Markdown scope does not enforce ACLs. No other writer active. User is the escalation contact; no substitute assigned for this local task.

## Handoff

Start at [rehearsal README](../../planning/events-agency/rehearsal/README.md). Run `python3 planning/events-agency/rehearsal/tools/check.py --self-test` from repository root. Future run must assign actual sessions/models and pin the pack; proposed run limits are not platform grants.

## State history

- 2026-10-05: proposed → ready → active. `/root` acknowledged continuation, inspected actual clean Git state and recorded the drafting scope. No live rehearsal started.
- 2026-10-05: user explicitly requested Luna workflow now and upon future request. Direct-check review method superseded before completion; two independent implementation paths dispatched with shared brief/interface and a separate review gate. No agency worker sessions dispatched; these are pack-building sessions.
- 2026-10-05: active → review. Both Luna implementers delivered scoped paths. Coordinator reconciled source resource semantics with the interface, reran 16 checker cases and both CLI fixtures, and checked local links/diff whitespace. Freeze a committed candidate for the separate reviewer; no live-run outcome or independent pass claimed yet.
- 2026-10-05: review → active. Independent Luna [R-GOV-009-01](../reviews/R-GOV-009-01.md) returned changes-required against `64c5879792bfe6eae186afbd54942adad903e18c`: v2 courtyard spend remained acceptable; change-card metadata and programme source categories were underchecked. Assigned the original checker author correction round 1; coordinator clarified the interface and made README review status refer to this task. Criteria unchanged.
- 2026-10-05: active → review. Original Luna checker author implemented F1/F2 fixes and added targeted negative cases. Coordinator aligned interface details with required programme/venue/resource evidence, verified 25 checker cases plus both direct CLI fixtures, local links and diff whitespace. A new fixed candidate receives scoped independent recheck, including expanded source-reference requirements; no pass claimed yet.
- 2026-10-05: review → active. Separate Luna [R-GOV-009-02](../reviews/R-GOV-009-02.md) rechecked `127032835946a821c6d09f2b6b798426c10b4cad`: F1/F2 fixed; F3 remains because valid programme citations could be combined with forbidden risk/support cards. Original checker author receives correction round 2, the final permitted round. Interface and acceptance unchanged.
- 2026-10-05: active → review. Original Luna author fixed F3 in the checker only, preserving interface and fixtures; coordinator reran 27 cases and both direct fixtures with passing results. Freeze the final corrected candidate for the second scoped recheck. Limits are unchanged; a failed final gate would require a new owner decision.
