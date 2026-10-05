# Local-model handoff

Updated 2026-10-05. This file supplies continuation context; [AGENTS.md](AGENTS.md) remains the instruction entry point and [the charter](governance/charter.md) defines authority.

## Read first

1. [AGENTS.md](AGENTS.md): execution guardrails and the Luna workflow.
2. This handoff, then [README.md](README.md) and [TREE.md](TREE.md): orientation.
3. [D-GOV-003](records/decisions/D-GOV-003.md): latest reviewed recommendation, still proposed.
4. [Charter](governance/charter.md), [workflow](governance/workflow.md), [access](governance/access.md), and your assigned task. Load other research/records only when relevant.

## Established state

- This is a Markdown governance prototype, not an agent runtime. The charter remains unconfigured.
- Institutional research covers bounded autonomy, polycentric principles, coordination, audit and adaptation. Company examples cover Amazon, GitLab, Toyota and the historical Valve handbook.
- Company titles are optional function labels. Default active functions are coordinator, implementer and separate reviewer. Titles grant no permissions.
- Rules distinguish read access, write authority and review-context exposure. Shared Git history and separate sessions do not provide blind review or access enforcement.
- Task completion requires review of a fixed candidate and coordinator verification of the integrated result. Existing records describe development of this template.
- The adaptation proposal describes possible project context and trial/activation; no project profile, operational trial, maintenance drill or performance comparison has been implemented.
- Latest direction: choose one representative reversible task, define bounded trial authority, then evaluate the workflow. Compare against a single executor plus separate reviewer with matched criteria and resource ceilings.
- Earlier tags v0.1.0 and v0.1.1 exclude later research and handoff changes. Use the delivered working HEAD for continuation.

## Pending decisions

The user still needs to identify a concrete project or maintained system, boundaries, actors, environment and budget. The reviewed pilot recommendation is not approval to operate a system. Until an assignment and authority are supplied, continue with read-only assessment or expressly requested repository drafting.

Possible drafting work: consolidate duplicated onboarding without changing semantics, clarify source-index coverage, and design a first trial contract using existing templates. Preserve historical records. New project instances should start their own operational records, retaining template provenance.

## Continue locally

Extract the ZIP into a directory of your choice; the `agent-governance/` folder includes its Git repository. In that folder, check:

```sh
git status --short
git log --oneline -5
git fsck --full
```

The working tree should be clean. If it is not, inspect and preserve local edits before proceeding. No remote, hosted repository, runtime isolation or production credential is configured by this package.

Use Luna for scoped workers and reviewers when available. With a different local model, record its actual identity and maintain separate implementer/reviewer sessions; never pretend a session is Luna. If a separate reviewer cannot be provided, report the blocker rather than certify your own work. Platform/user instructions take precedence over repository guidance.

## Suggested continuation prompt

> Read AGENTS.md and HANDOFF.md, then inspect the current Git state and D-GOV-003. Summarize established decisions, pending decisions and validation limits. Propose the smallest next task using existing templates. Keep governance authority in the charter, distinguish requested access from actual runtime grants, preserve historical records, and obtain separate review before completion. Ask for the concrete project details needed for an operational trial; do not activate or operate a system from this handoff alone.

## Validation limits

Prior checks covered document consistency, local links, tables, Git integrity, archive extraction and cloning. Separate Luna sessions reviewed fixed commits and disclosed prior exposure. These checks do not demonstrate operational effectiveness, authenticated agent identity or enforced runtime permissions. The handoff/package is also verified before delivery.
