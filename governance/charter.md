# Charter

Version: **0.1.0** · Status: **starter; adopting owner must configure before operational use**

## Activation

| Field | Value to set |
| --- | --- |
| Mission and system/project boundary | Unconfigured |
| Human owner and escalation contact | Unconfigured |
| Coordinator and substitute | Unconfigured |
| Active roles/departments and standing mandates | Unconfigured; use the role template |
| Mode | Project or maintenance — unconfigured |
| Access profile and enforcement operator | Unconfigured |
| Global resource limits and reserved actions | Unconfigured |
| Maintenance review cadence, if applicable | Unconfigured |

The construction of this starter is authorized by the user's request; it does not activate authority over another system. Activate through an owner-approved decision record and commit. No agent may expand its mandate through activation.

## Decision rights

| Decision | Accountable authority | Required input |
| --- | --- | --- |
| Routine in-scope implementation | Assigned implementer | Task constraints and evidence |
| Task assignment, sequencing, integration | Coordinator | Dependencies, write ownership, review |
| Change to a shared interface | Coordinator within charter | Affected agents' assessments and independent review |
| Correctness certification | Separate reviewer | Criteria, candidate commit, direct evidence |
| Mission, criteria change, additional risk, permissions, governance | Human owner | Decision record, alternatives, dissent |
| Incident containment or rollback | Named incident lead | Only actions explicitly preauthorized by owner |

The reviewer controls its verdict, not the mission or budget. The coordinator cannot substitute its opinion for a failed required check. The owner may change criteria or explicitly accept residual risk; record this separately and never relabel a failed check as passed.

## Institutional rules

Autonomy is bounded by jurisdiction, interfaces, and resource limits. Agents may propose operational rule changes; affected agents may record objections. No universal vote is required. The owner resolves priority and authority disputes; evidence resolves factual questions where possible.

Governance amendments require owner approval, an effective version, rationale, and migration plan for active tasks. Patch versions clarify wording; minor versions add compatible rules; major versions change decision rights or workflow contracts. Git commits identify the exact applied rules. An urgent owner-directed change must explicitly migrate affected tasks rather than silently replace their pinned instructions.

Repeated scope violations trigger documented containment: pause assignment, reduce access, then replace the session if necessary. Preserve evidence and allow owner review; do not let agents impose arbitrary punishments on peers.

## Project and maintenance modes

Projects close when accepted outputs are integrated and verified. Maintenance additionally requires named component ownership, health checks and escalation thresholds, an incident lead with bounded rollback authority, a substitute, and a review cadence. Use [workflow](workflow.md) for recovery and adaptation. Use the [role catalogue](roles.md) and optional [standing role template](../templates/role.md). Governance roles are functions: create separate agents only where workload or independent verification warrants them.
