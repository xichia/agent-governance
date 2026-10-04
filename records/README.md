# Shared records

Git is the durable shared record; chat is a working channel. `main` is canonical after coordinator integration. While work is underway, discover progress through the task's branch and record paths. The coordinator shares exact branch/commit references with dependent agents and reconciles them into main at meaningful milestones.

## Names and ownership

| Record | Path | Writer |
| --- | --- | --- |
| Task and dated state history | `tasks/T-<unique-id>.md` | Coordinator |
| Progress and handoff | `tasks/T-<id>/<agent-id>/<UTC-timestamp>-<sequence>.md` | Named agent |
| Independent review | `reviews/R-<task-id>-<unique-id>.md` | Named reviewer |
| Decision | `decisions/D-<unique-id>.md` | Decision maker via coordinator |
| Incident | `incidents/I-<unique-id>.md` | Named incident lead |

Start from [templates](../templates/); standing roles use [the role template](../templates/role.md). Reserve IDs when assigning work; never reuse an existing filename. Use ISO 8601 UTC times and stable agent/session identifiers. Include exact evidence commit IDs and relative links where possible. External evidence should use durable, authorized references and a short result summary; do not commit sensitive content.

Preserve consequential history. A correction is a new dated entry or record identifying what it supersedes; no force-push of shared history. Git authorship is not authenticated agent identity on its own: use trusted runtime identity and review records for assurance. Keep tool-specific credentials outside Git.

On handoff, record completed work, current state, evidence, blockers, next action, and required access. The recipient acknowledges the takeover. This repository's bootstrap records demonstrate the construction workflow, not an operational deployment.
