# Run metrics — SCI-20261005-01

- Authorization: user “Let’s proceed” and “Try again”; [T-GOV-010](../../records/tasks/T-GOV-010.md).
- Governance/pack pin: `e577179d78bb7b18e70746326d4e3c883d85f44d`; brief v1→v2; interface v1; CH-001.
- First timed setup observation: 08:40:14 UTC; final elapsed/outcome pending. Initial orientation before the first clock sample is unmeasured.
- Sixty-minute total ceiling; six distinct role sessions; no replacement sessions; at most two correction batches.
- Token/cost and detailed tool telemetry: unavailable. Task-response activations are coordinator dispatch/follow-up deliveries; internal sampling-turn count is unavailable.

## Specialist phase observations

| Role | V1 active window UTC | V2 active window UTC | Reported active seconds (excluding small schema correction) | Successful activations |
| --- | --- | --- | ---: | ---: |
| finance | 2026-10-05T08:43:48Z – 2026-10-05T08:44:45Z | 2026-10-05T08:52:13Z – 2026-10-05T08:52:54Z | 98 | 2 |
| creative | 2026-10-05T08:43:11Z – 2026-10-05T08:45:52Z | 2026-10-05T08:52:17Z – 2026-10-05T08:54:39Z | 303 | 2 |
| risk | 2026-10-05T08:47:20Z – 2026-10-05T08:48:40Z | 2026-10-05T08:55:59Z – 2026-10-05T08:57:16Z | 157 | 3 |
| marketing | 2026-10-05T08:49:15Z – 2026-10-05T08:50:06Z | 2026-10-05T08:58:02Z – 2026-10-05T08:58:43Z | 92 | 3 |

Times are author tool-clock reports. Risk and marketing each performed one additional schema edit under a minute; exact correction duration unavailable. All observed specialist active totals remain below eight minutes. Waiting for dependencies is inside total wall-clock, separately from active edit time. Finance had one additional failed startup delivery, not included in successful activations.

## Phase chronology

- v1_integrated_utc: 2026-10-05T08:51:19.593783+00:00.
- change_issued_utc: 2026-10-05T08:51:46.857551+00:00.
- v2_integrated_utc: 2026-10-05T09:00:32.287837+00:00.

Initial proposal snapshot: `078762986f8da27394d933bb689fd3722ce384d3`. Dependency order: finance and creative in parallel → risk → marketing, repeated after CH-001. Coordinator integration/check work is bounded separately; exact coordinator active-time telemetry unavailable.

## Coordination evidence

- Six assigned identities in [assignment.json](assignment.json); reviewer is reserved and dispatched only after candidate freeze.
- Failed startup/retry: finance model-capacity failure before artifact; same-session retry once under explicit user instruction.
- Correction batch 1: initial schema alignment (risk-only row citations, supporting references retained; marketing exact title and audience literals). One batch remains for review findings.
- Two substantive design issues surfaced by risk: quiet-host timing gap and chair-handling/wayfinding contention. Revised public timing and fixed seating address them at the proposed schedule level. Real layout/volunteer availability remains open.
- CH-001 propagation: four of four specialist handoffs use v2 and acknowledge CH-001; no stale final handoff.
- Routine coordinator interventions: shared brief dispatch, dependency sequencing, schema requests and disclosed-change routing. No criteria or budget changes, supplier facts invented beyond the pack, external actions or replacement agents observed.
- Independent review: pending; no pass claimed. Qualitative source-to-claim inspection and exact final resource/staff feasibility await reviewer.
