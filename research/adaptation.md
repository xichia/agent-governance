# Adapting the template to a project or maintained system

**Status: design proposal, not an activated profile.** This guide refines the earlier five-file project-folder idea. It adds no operational authority and leaves the current [charter](../governance/charter.md) unchanged. Recommendations below are a synthesis of Luna research and design critique, not performance results.

## Keep one source of authority

| Layer | Owns | Does not own |
| --- | --- | --- |
| Reusable governance | Shared workflow, decision procedures, independence, evidence and record conventions | A specific system's mission or live permissions |
| Adopted charter and owner-approved decisions | Mission, boundaries, reserved decisions, active functions, budgets and activation | Runtime enforcement by itself |
| Project context | Facts, component map, interfaces, dependencies and source provenance | New authority or automatic activation |
| Standing roles and tasks | Delegated duties; narrower scope, criteria, outputs and handoffs | Expansion beyond approved project authority |
| Runtime/operator | Actual identities, tool grants, data boundaries, expiry and revocation | Permission to ignore the charter because a tool is accessible |

Do not repeat the same decision rights in charter, organisation, permissions and task files. Roles may narrow approved authority; tasks may narrow it further. Where no standing role is needed, the task can carry a direct charter-bounded assignment. If the requested scope exceeds approval or available runtime grants, stop and escalate. Record grant references and verification evidence, never credentials.

## Minimum adaptation record

Start with a short project brief: desired outcome, boundaries, stakeholders, constraints, existing systems and relevant evidence. Record template source/version/commit, adoption date, local deviations and the reviewed configuration commit. Add a component map only when work spans multiple owned components. Select coordinator, implementer and independent reviewer first; activate other departments only where their outputs are needed.

A future configuration folder can stay small:

- `project/README.md`: context, provenance, links to the charter, verification plan and relevant records.
- `project/components.md`: optional ownership, dependencies and interfaces.
- `project/verification.md`: project-level acceptance strategy; in maintenance, health measures, monitoring evidence, thresholds and recovery checks. Task-specific criteria remain in tasks; authority to act remains in the charter.

These are proposed future paths, not files already created. Persistent role assignments use the existing [role template](../templates/role.md). Later, the [task template](../templates/task.md) should explicitly pin project configuration as well as governance, and link actual grant identity, grantor/enforcer, expiry and revocation evidence. Configuration commits alone cannot attest that external grants remain current.

## Adoption and readiness

1. **Inventory:** determine finite-project or maintenance mode, existing rules, components, data sensitivity and external actions. In an existing repository, preserve local instructions and resolve conflicts explicitly before introducing governance files.
2. **Tailor:** owner approves the adopted charter; coordinator drafts scoped tasks and context. Resolve missing owners, contradictory criteria and overlapping edit ownership.
3. **Trial:** owner explicitly authorizes a bounded test environment, operations, data, limits, expiry and rollback. A proposed brief is not trial authorization. Check ordinary completion, failed checks, handoff and forbidden-action denial where enforcement is claimed.
4. **Activate:** owner records the effective policy/configuration and scope after independent review of trial evidence. Draft, trial and active are proposed adoption states, distinct from the existing task lifecycle. A limited trial is its own authorization, not permission to operate in production.
5. **Maintain:** review actual outcomes and permission drift. Suspend dependent work when authorization or enforcement no longer matches the assignment.

## Finite work versus maintenance

| Requirement | Project | Maintenance |
| --- | --- | --- |
| Success | Accepted deliverables, integration and closure | User-relevant health targets and continuing obligations |
| Ownership | Deliverables/workstreams | Components, substitutes and incident lead |
| Work trigger | Milestones and dependencies | Monitoring signals, incidents and scheduled checks |
| Verification | Output checks and final handover | Monitoring evidence, recovery checks and tested rollback |

Google SRE's [SLO guidance](https://sre.google/workbook/implementing-slos/) informs health targets and review; its [incident response guidance](https://sre.google/workbook/incident-response/) informs operational recovery. Neither prescribes a particular LLM-agent organisation. Avoid inventing universal health thresholds before understanding the actual system.

## Provenance, upgrades and records

A fresh project instance starts with its own operational records. Keep template-development reviews and tasks upstream or clearly marked as template history; they are not evidence that the new project passed a trial. Existing-project adoption likewise preserves actual local records rather than replacing them with examples.

GitHub's [template generation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) creates a new repository with a single initial commit rather than fork ancestry. Do not assume automatic upstream merging. Record the source revision and apply reviewed diffs with local deviations visible. Migrate or explicitly retain active tasks' pinned rules before changed policy takes effect; never silently switch them.

NIST's [profile model](https://pages.nist.gov/OSCAL/learn/concepts/layer/control/profile/) motivates explicit selection/tailoring, and [configuration-management guidance](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) motivates baseline/change control. These security frameworks are design analogies, not required schemas or validation of this repository.

## Proposed validation exercises

- **Project:** assign an analysis task and then request an out-of-scope write. Verify denial/escalation, independent artifact review and a resumable handoff.
- **Maintenance:** simulate a service fault while policy changes with tasks in flight. Verify named response authority, explicit task migration/retention, bounded rollback and recovery evidence.

These exercises have not been run. Documentation/link checks validate the proposal's consistency, not operational readiness. Sources reviewed 2026-10-04.
