# T-GOV-010 — Run the fictional science-and-culture agency rehearsal

- **Status:** active
- **Owner / escalation:** requesting user, this chat; no substitute
- **Authorization:** “Let's proceed”, followed by “Try again”, after delivery of the accepted pack and identification of a live rehearsal as next step. Proceed with the pack's fictional defaults and bounded local run; no further permission question needed. User's requested Luna workflow applies.
- **Coordinator:** `/root`, GPT-6; runtime deployment identifier unavailable
- **Governance / pack / base:** charter 0.1.1; `e577179` (full pin recorded in metrics before dispatch); accepted pack review R-GOV-009-03
- **Branch:** `work`
- **Run:** `SCI-20261005-01`; setup began 2026-10-05T08:40:14Z
- **Limits:** 60 minutes total including setup/report; one coordinator, four specialist Luna sessions, one distinct Luna reviewer; no replacement/restart retries; at most two correction batches. Per specialist/reviewer: 8 minutes active work, at most six/four task-response activations respectively; coordinator integration: 10 minutes active work. Dependency-wait time is recorded separately and remains inside total wall-clock. Tokens/tool usage unavailable unless exposed; session/activation/wall-clock limits apply, no token cap enforcement claimed.
- **Access:** local non-sensitive governance, brief/interface/source/change pack, owned/dependent run artifacts and checker; no network research, contact, spend, commitments, personal data, publication or actual event operation. Cooperative shared filesystem; grants are not path ACLs.

## Objective and fixed acceptance

Have real, separately dispatched Luna workstreams produce a v1 proposal, respond to disclosed CH-001, and deliver a reviewed v2 proposal for fictional EV-SCI-001: 80 adults, AUD 6000 inclusive of 10% contingency, 18:00–21:00 Perth on fictional 2026-11-14.

1. Four actual JSON specialist envelopes/handoffs, with actual session/model IDs and matching version/dependency receipts; preserve v1 before v2. Workers do not read pack fixtures or example answers.
2. Finance supplies source-exact integer-cent arithmetic; creative supplies source-traced timed programme, setup/pack-down, transitions, seating and quiet option; risk supplies practical issues/owners/mitigations and unresolved human decisions; marketing matches the programme and remains draft-only.
3. V1 includes a courtyard activity to exercise the known change. V2 removes courtyard cost/use/marketing references while attendance, ceiling/access and end time remain fixed. All four acknowledge CH-001.
4. Integrated v1/v2 pass the pack checker; separately crosscheck arithmetic and physical resource constraints (especially the actual 80-chair inventory), practical transitions, volunteer coverage and source-to-claim support.
5. Freeze exact candidate; distinct Luna reviewer checks all run artifacts/criteria and records pass/changes-required/inconclusive; corrections within bounds; coordinator verifies accepted integrated candidate before closure.
6. Record elapsed phases, assignments/activations, corrections, conflicts, interventions, change coverage, missing telemetry and observed limitations. Publish a local readable results document, clearly labeling all supplier facts fictional and actual run evidence as such.

## One-writer assignments

- `/root/rehearsal_finance`, configured `gpt-6-luna`: only `runs/SCI-20261005-01/outputs/finance.json`.
- `/root/rehearsal_creative`, configured `gpt-6-luna`: only `runs/SCI-20261005-01/outputs/creative.json`.
- `/root/rehearsal_risk`, configured `gpt-6-luna`: only `runs/SCI-20261005-01/outputs/risk.json`; depends on finance + creative same-version artifacts.
- `/root/rehearsal_marketing`, configured `gpt-6-luna`: only `runs/SCI-20261005-01/outputs/marketing.json`; depends on finance + creative + risk.
- `/root/rehearsal_review`, configured `gpt-6-luna`: new files only under `runs/SCI-20261005-01/reviews/`; no implementation authorship.
- Coordinator: task/progress, run assignment/metrics/change/conflict logs, immutable v1 archive, integrated JSON candidates, readable result and continuation links. Coordinator alone performs Git operations. No pack/governance edits.

All task contracts expire on completion/stop. Specialists are prompted with role and shared inputs; v1 output snapshots are archived before authors update owned files for v2. Evidence-first review with shared history visible; no blind-review claim. A coherent hypothetical risk plan is required; actual legal/access/venue/volunteer approvals remain human decisions, not run failures simply because they are fictional.

## History

- 2026-10-05T08:40:14Z: proposed → ready → active. Coordinator confirmed clean tree at the delivered pack, available local tools and explicit continuation authorization. No prior T-GOV-010 run exists. Set up bounded run and reserved disjoint writer paths and distinct reviewer.
- 2026-10-05: finance startup failed with “Selected model is at capacity” before any artifact existed; creative session started. User's explicit “Try again” authorizes one same-session delivery retry for this transient startup failure. Record one failed dispatch/retry separately; no replacement session/model, output regeneration or expansion of fictional scope. If that delivery also fails, stop dependent work as blocked. This owner-directed exception supersedes the zero-retry proposal only for this startup event.
