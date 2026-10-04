# Agent access and independence

Independence has several dimensions. **Context independence** concerns which information an agent sees and when; **write authority** concerns which changes it may propose or make; **read access** concerns what information it can inspect. Limiting one dimension does not limit the others. Separate prompts or branches do not create security boundaries.

## Default access

For cooperative work, give agents broad read access to non-sensitive governance records, including the [charter](charter.md), [workflow](workflow.md), decisions, and progress records. Give each task access to the relevant source artifacts and acceptance criteria. Full-repository reading is optional when it adds useful context; avoid disclosing unrelated or sensitive material. Never commit production secrets or credentials to Git: deleting a secret from the current tree does not remove it from repository history.

Assign one primary writer per scoped artifact or work area. Other agents may suggest changes as patches or review comments; the coordinator integrates them and checks conflicts. This is a coordination protocol, not an access-control list: if every agent has filesystem write permission, path ownership in this document cannot technically prevent other edits.

| Role | Read | Write or propose | Review and merge |
|---|---|---|---|
| Coordinator | Governance records and task-relevant artifacts | Plans, assignments, integration, progress and decisions | Integrates accepted work; does not self-certify consequential changes |
| Implementer | Assignment, criteria, relevant artifacts and necessary context | Scoped implementation and its evidence | Does not approve its own work |
| Reviewer | Criteria, changed artifacts, diff, and verification evidence | A new review record with findings and verdict | Does not edit the implementation under review; recommends acceptance or rework |
| Owner | All records and artifacts needed for oversight | Charter, policy, and reserved decisions | Approves governance changes and any reserved release or merge decision |

## Review independence

Stage review context deliberately: first provide the reviewer the task, criteria, changed artifacts or diff, and testable evidence. Ask for a review record before sharing the implementer’s conclusion or rationale. This can reduce anchoring, but it is not a blind review if the reviewer can inspect unrestricted repository history, existing notes, or agent conversation logs. Where those are visible, call the review **evidence-first**, not blind. Distinct models, fresh sessions, and deterministic checks can add useful diversity; none guarantees independence.

Keep reviewer output in a new review record (for example, under `records/reviews/`) or have the coordinator broker it. Do not give a reviewer write access to the implementation being evaluated. If a review requires broader access, record the reason, scope, grantor, and duration; revoke temporary access after the review and note the revocation.

## Enforcement profiles

**Cooperative shared repository:** agents may read the shared repository and make scoped changes in separate branches or worktrees; the coordinator integrates, and review is recorded separately. Git worktrees share repository data, while sparse checkout only changes the visible working tree. Neither is a security boundary. Git hosting `CODEOWNERS` routes or gates reviews when protected-branch rules require it; it does not grant path-level read/write ACLs, and any one listed owner may satisfy an owner-review requirement. Protect governance and review rules themselves.

**Enforced isolation:** when confidentiality or stronger separation matters, run agents under separate OS/container identities or expose files through an API that enforces path-level permissions. Grant only required paths and least-privilege tool credentials; isolate secrets outside the repository. Have an external, operator-controlled check or trusted coordinator enforce merge and review gates, so an agent cannot edit its own enforcement. Branches and repository Markdown alone cannot provide this guarantee.

See [sources](../research/sources.md) for the Git, GitHub, and multi-agent research references. The process and reserved decisions are defined in the [workflow](workflow.md) and [charter](charter.md).
