# Shared interface v1

Read root [AGENTS.md](../../../AGENTS.md), pinned governance and the run task. The coordinator alone writes shared facts and the integrated proposal. Each specialist writes one separate JSON output; do not silently change another team's work.

## Integrated proposal JSON

The [initial fixture](fixtures/initial.json) illustrates structure, not a required creative answer. `check.py` enforces this contract and rejects missing fields or malformed types.

| Field | Meaning |
| --- | --- |
| `event_id`, `brief_version`, `fictional` | `EV-SCI-001`, integer 1 or 2, literal true |
| `title`, `attendance`, `currency`, `ceiling_cents` | Title, fixed 80, AUD, fixed 600000 |
| `budget` | Rows: unique `id`, source-card `source_id`, positive integer `quantity`, source-exact `unit_cents` |
| `subtotal_cents`, `contingency_cents`, `total_cents` | Recomputed integers; contingency is subtotal × 10%, rounded up to nearest cent |
| `programme` | Rows: unique `id`, `title`, venue `room_id`, integer `start_minute`, `end_minute`, `attendees`, list `resources` and nonempty `source_ids` |
| `risks` | Unique `id`, `issue`, `owner`, `mitigation`, status `open` or `mitigated`, nonempty `source_ids` |
| `marketing` | `brief_version`, `title`, `attendance`, ordered `programme_ids` matching programme, `room_ids` matching used rooms, `draft_copy`, `publication_status` = `draft_only` |
| `handoffs` | Exactly four role keys: `finance`, `risk`, `creative`, `marketing`; each has `writer_session`, `model`, `brief_version`, `artifact`, `status`, `dependencies_acknowledged`, `source_ids`, `assumptions`, `open_questions`, `change_ack_ids` |
| `pending_human_decisions` | Nonempty list; no automatic owner approval |

Use half-open intervals `[start,end)`: adjacent activities are allowed; overlapping uses of a single room or exclusive resource are rejected. Room capacity and total simultaneous attendance are checked; a multiroom activity should use separate rows. Resource IDs must come from the pack and purchased resources need a budget line. Every used room must be covered by a selected venue card. All programme and risk cards must exist. Fixture `writer_session` values start `fixture:` and do not represent agents.

The source pack distinguishes venue/resource price cards, programme cards, risk cards and in-kind support cards. Prices include modeled taxes and fees. Resource `usage_mode` defines capacity accounting: `attendees` pools seats/materials across simultaneous participants; `event_unit` counts simultaneous activity uses; `exclusive` prohibits overlapping uses even when extra units are budgeted. Purchased quantity scales pooled capacity; included inventory depends on selecting its venue card. Budget each price card at most once, combining quantities on one line. Setup and pack-down need explicit in-window programme rows. Practical transition times and staffing coverage still require reviewer assessment.

Programme `source_ids` must refer to programme, venue or resource cards, including at least one programme card plus the used room's venue card and each listed resource's source card; risk rows use risk cards. Handoff provenance may also cite in-kind support cards. These categories validate reference compatibility, not the truth of prose. CH-001 must reference the courtyard venue source, identify the event, transition from integer version 1 to 2, change courtyard availability from available to unavailable and name all four affected roles. Its metadata is validated before acknowledgements are accepted. Version 2 rejects the courtyard budget line as well as courtyard room use and marketing references; unchanged cards are preserved for historical provenance.

## Specialist output and handoff

Each owned JSON output has `event_id`, `brief_version`, `role`, `deliverable` (role-specific rows/prose), and `handoff` using the fields above. Include alternatives, assumptions, cost/access tradeoffs, source IDs, unresolved questions and dependency requests in `deliverable`. Status is `ready_for_review` or `blocked`. A blocked output stops dependent integration. The current checker validates the integrated representation; coordinator/reviewer inspect individual deliverables separately.

Dependency acknowledgements contain role IDs: finance, risk and creative initially read the shared brief; risk must acknowledge finance and creative before final handoff; marketing acknowledges finance, risk and creative. These entries record receipt of a matching-version artifact, not agreement or authority.

## Changes and conflict record

Coordinator applies only the predeclared [change](case/changes.json), preserves v1, publishes v2 and logs `id`, old/new values, source, authority, affected roles and outcome. Each affected handoff includes `CH-001` in `change_ack_ids`; reject stale versions. New ceiling, mission, source mode, criteria or real external action requires a human decision. Record competing options and evidence; unresolved priority questions go to the user. No majority vote substitutes for checks.

Keep unknowns explicit in prose/assumptions, never encode unknown cost as zero. Budget rows require a known fictional card price; an unknown required cost blocks a complete budget. A card reference demonstrates pack provenance, not that the prose follows from that card; separate review checks that relationship.
