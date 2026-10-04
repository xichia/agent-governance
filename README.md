# Agent governance

A small, versioned operating agreement for independent agents managing a project or maintaining a system.

**Default: autonomous work within explicit boundaries, shared non-sensitive records, scoped writes, independent review, and one accountable integrator.** This is a governance specification, not an agent runtime or an access-control implementation.

## Start here

1. The adopting human owner fills in [the charter](governance/charter.md), names the coordinator, and selects an [access profile](governance/access.md). Until configured, use this repository for drafting only.
2. Choose only the needed [company roles](governance/roles.md), informed by [real-company patterns](research/company-patterns.md). A title does not grant permissions. The coordinator creates a task from [the task template](templates/task.md): criteria, dependencies, ownership, write paths, access, budget, and review assignment. Pin the governance commit in the task.
3. Give each agent [AGENT.md](AGENT.md), the task, relevant artifacts, and permitted tools. Use a separate branch or worktree per writer when available; assign disjoint paths.
4. Follow [the Luna workflow](governance/workflow.md). Record progress and evidence, obtain a separate review, integrate, and verify the resulting state.

Luna is the default worker/reviewer model when available. Record the actual model used; a separate session is required for review. Role independence comes from duties and evidence access, not the model's name.

## Repository map

| Path | Purpose |
| --- | --- |
| [AGENT.md](AGENT.md) | Common agent operating instructions |
| [AGENTS.md](AGENTS.md) | Discovery entry point for compatible agent tools |
| [governance/charter.md](governance/charter.md) | Mission, authority, and reserved decisions |
| [governance/workflow.md](governance/workflow.md) | Task lifecycle, review, integration, recovery |
| [governance/roles.md](governance/roles.md) | CEO, CTO, legal, marketing, PR, and other role contracts |
| [governance/access.md](governance/access.md) | Read/write policy and independence profiles |
| [research/foundations.md](research/foundations.md) | Institutional models and design rationale |
| [research/company-patterns.md](research/company-patterns.md) | Company structures, borrowed mechanisms, and tradeoffs |
| [research/sources.md](research/sources.md) | Primary sources and evidence limits |
| [templates/](templates/) | Task, progress, review, decision, incident forms |
| [records/README.md](records/README.md) | Versioned records, naming, discovery, and handoffs |

## What to validate

Evaluate this design against a single-agent baseline using comparable tasks and budgets. Track acceptance success, escaped defects, cost, completion time, human interventions, and recovery after interruption. Add roles only when their benefit justifies coordination cost.

The research supports the design principles; it does not establish that this exact architecture is optimal. Review identities, permissions, protected branches, durable execution, and monitoring require configuration outside these Markdown files. No remote hosting or runtime permissions are configured by this starter.
