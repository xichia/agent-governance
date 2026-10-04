# Governance foundations

## What the model governs

An **organizational chart** assigns work and relationships: roles, owners, coordination paths, and interfaces. An **institution** sets the rules of the game: who may decide, what evidence is required, how shared resources and disputes are handled, and how rules change. A repository needs both. `AGENT.md` can state policy; Git records changes. Neither enforces access control.

## Structural options

| Form | Strength | Cost or failure mode | Fit |
|---|---|---|---|
| **Hierarchy** | Clear command, escalation, and single integration point. | Coordinator bottleneck; local knowledge and initiative may be filtered upward. | Useful for tightly coupled work, emergencies, or a clear single accountable owner. |
| **Federation / polycentric governance** | Multiple bounded decision centers retain local discretion while coordinating under shared rules; permits local adaptation and explicit conflict resolution. | More negotiation, duplicated work, and interface risk; autonomy without common rules fragments. | Good default for independent components or research streams with shared objectives. |
| **Matrix** | Combines domain ownership with project priorities; supports shared specialists across work. | Competing authorities can create ambiguous priorities and accountability. | Useful when agents have durable specialties and work spans several projects; name who resolves priority conflicts. |
| **Market / contract-net** | Tasks can be offered and accepted against explicit capability, cost, and deliverables. | Bidding, monitoring, and integration overhead; agents may optimize stated deliverables while missing system-wide needs. | Useful for optional, separable tasks with measurable acceptance tests; retain an integrator. |

These forms can be mixed. A practical starting point is a **polycentric federation with a thin hierarchy for integration and reserved decisions**: domain agents own routine in-scope decisions; a coordinator manages dependencies; a separate reviewer checks consequential work; a human owner sets mission, risk tolerance, and policy. The reviewer can block a specified transition with evidence and a dispute route, but should not become the task owner.

## Functions, rules, and independence

Beer’s Viable System Model is best used as a functional checklist, not as a mandate for five agents: operations do the work; coordination prevents destructive clashes; internal management allocates resources and audits; intelligence scans for change; policy maintains identity and balances present operations with future needs. Small teams may combine functions, but should avoid self-certification on high-impact work.

For each role, state its jurisdiction, decision rights, tools, evidence of completion, escalation route, and handoff record. Local agents may act within scope. Cross-boundary changes consult affected owners. Shared or high-impact changes require independent review. Evidence disputes trigger reproducible checks; priority disputes go to the named owner; governance changes require owner approval and a recorded revision. Prefer correction and recovery over punitive responses.

Independence is a process property, not merely separate chats or model names. Reviewers should not edit work they certify; where practical, give them artifacts before the executor’s conclusion. Different tools or models may diversify failure modes but do not prove independence. All-agent **read** access to charter, interfaces, and decision records supports shared context; unrestricted **write** access creates collisions and accidental policy edits. Scope writes by paths, branches, or task artifacts. Use runtime permissions or separate repositories for security boundaries; path ownership and branches are conventions. Keep decisions and progress versioned, dated, attributable, and correctable without erasing consequential history.

## Work type and evaluation

Projects need a time-bounded objective, dependencies, acceptance criteria, integration owner, and closure record. System maintenance needs persistent component ownership, monitoring, incident and rollback authority, succession, and scheduled review of changed conditions.

Treat this architecture as an **unvalidated design hypothesis**. Compare representative tasks with a single-agent baseline and, if feasible, a simple coordinator-worker baseline. Predefine acceptance rate, escaped defects, recovery after an injected handoff or agent failure, human intervention, elapsed time, and token/tool cost. Keep tasks and tools comparable; record failures and repeat enough cases to assess whether effects recur. Add roles or gates only when measured benefits justify coordination cost. Existing studies motivate these tests; they do not establish that this design improves performance.
