# Science, art and shared wonder — rehearsal pack

This is a **fictional, local demonstration kit**. All suppliers, prices, availability and venues are invented. The examples are hand-authored checker fixtures, not outputs from agent sessions. No rehearsal has run and no independent review pass is claimed.

The user accepted building this pack after the reviewed [plan](../PLAN.md). The default brief below makes the kit runnable without real supplier research. Change these fictional constraints before freezing a run if desired.

## Read and run

1. Read [brief](brief.md), [interface](interface.md) and [case data](case/sources.json).
2. Read the assigned [role contract](roles/coordinator.md); specialist contracts link from it.
3. Validate the prepared case and examples from repository root:

```sh
python3 planning/events-agency/rehearsal/tools/check.py --self-test
python3 planning/events-agency/rehearsal/tools/check.py planning/events-agency/rehearsal/fixtures/revised.json
```

4. For a future live rehearsal follow [runbook](runbook.md). The examples establish feasibility of the fictional arithmetic and scheduling; give workers the brief, source pack and interface, rather than an example answer. Sources and criteria remain openly available.

## Contents and current evidence

| Artifact | Purpose |
| --- | --- |
| [Brief](brief.md) | Audience, constraints, provenance and editable defaults |
| [Interface](interface.md) | JSON contract, handoff and version/change rules |
| [Source cards](case/sources.json) | Invented supplier facts and venue/resource limits |
| [Changes](case/changes.json) | Disclosed closure exercise and version patches |
| [Initial](fixtures/initial.json) / [revised](fixtures/revised.json) | Feasible reference examples for checker verification |
| [Checker](tools/check.py) | Standard-library deterministic validation |
| [Runbook](runbook.md) | Dispatch, review, recovery and evidence capture |

The checker checks structure and mechanical consistency. A separate reviewer must assess theme, audience value, accessibility detail, provenance sufficiency and unresolved risks. The checker cannot establish legal compliance, actual availability, runtime isolation or human approval.
