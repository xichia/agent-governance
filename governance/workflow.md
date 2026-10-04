# Luna workflow and lifecycle

## 1. Plan

The coordinator creates a [task](../templates/task.md), assigns an implementer and separate reviewer, and pins a governance commit. Criteria must be observable and relevant. Define output paths, interfaces, read/write/tool access, dependencies, candidate branch, budget, retry limit, and escalation contact. Confirm dependencies before marking the task ready. An owner-approved criteria change creates a dated decision and requires review against the new criteria.

Parallelize work only when dependencies and edit ownership allow it. Overlapping paths require serialized work or an explicit ownership transfer. Peer consultation is allowed; peers cannot grant authority.

## 2. Implement

Move ready to active when the assigned writer begins. Work in the assigned branch/workspace; record milestones and evidence in per-agent [progress](../templates/progress.md) files. Commit a stable candidate before review. Report unresolved issues and actual checks, not an unsupported claim of completion. Shared-state updates and external actions still require the task's authorization.

## 3. Review

Move active to review when a candidate and evidence are ready. A separate Luna session receives criteria, base/candidate commits, relevant artifacts, and verification tools. Where the access profile supports it, record initial observations before receiving the executor's summary; acknowledge exposure if staging was not possible. Relevant evidence must not be withheld to manufacture agreement.

The reviewer checks correctness, completeness, scope, and edge cases. Record a [review](../templates/review.md) with pass, changes-required, or inconclusive. Approval applies only to the recorded candidate and criteria. Changed candidate content requires a new review or an explicitly scoped recheck that documents preserved evidence. Source-affecting merges or conflict resolution require review of the new content.

## 4. Iterate and integrate

Changes-required returns the task to active. Inconclusive work is blocked until evidence, access, or a method is supplied. Stop at resource limits; the owner decides whether to rescope, extend, or cancel.

After a pass, the coordinator integrates the approved output and runs the task's final checks on the resulting integrated commit. Link the candidate review and integration evidence in the task; then mark done. Final-record-only commits may follow without invalidating artifact review, provided they change no reviewed artifacts or criteria. Report outcome, validation, and limitations. Do not equate branch success with integrated success.

## States

| State | Meaning and permitted transition |
| --- | --- |
| proposed | Draft scope; coordinator can make ready after prerequisites |
| ready | Complete assignment and satisfied dependencies; writer makes active |
| active | Work underway; writer submits review or reports blocked |
| review | Fixed candidate awaiting independent verdict; coordinator closes after integration or returns active/blocked |
| blocked | Record cause, responsible resolver, and next action; coordinator resumes the appropriate prior state when resolved |
| done | Accepted and verified integrated result; new defects create a linked task |
| cancelled | Owner/coordinator ends work within charter; preserve partial evidence |

Only the coordinator updates canonical task state. Agents submit changes through their assigned branch or record channel. Keep state history as dated entries, not a shared editable dashboard with multiple writers.

## Recovery, incidents, adaptation

After interruption, read the pinned policy, canonical task, latest progress, review, and actual Git state. Confirm evidence and ownership before resuming; never infer completion from a summary alone. Reassign through a dated handoff, revoke obsolete runtime access, and preserve prior records.

For maintenance, open an [incident](../templates/incident.md). The assigned lead performs only preauthorized containment/rollback, escalates at the charter's thresholds, and records recovery checks. Close after verified recovery and a follow-up decision. Emergency authority expires with the incident; it cannot amend the charter.

At the configured cadence, assess defects, cost, blocked work, recovery, and changing conditions. Propose rule changes through [decision records](../templates/decision.md). Validate adaptation against a baseline rather than expanding the organisation by default.
