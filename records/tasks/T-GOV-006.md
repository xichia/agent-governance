# Task: T-GOV-006 — Interactive governance demo

- **Status:** cancelled
- **Human owner / escalation:** requesting user, this conversation
- **Coordinator / executor:** `/root`, Codex GPT-6 (exact deployment identifier unavailable)
- **Reviewer:** separate Luna session, to be assigned against a fixed candidate
- **Authority:** user's request to create an engaging demo of this governance system; repository drafting only
- **Governance version / commit:** 0.1.1 at `5c35200db736c86b6a6e31cd30de8d3af48211de`
- **Branch:** `codex/governance-demo` · **Base:** `5c35200db736c86b6a6e31cd30de8d3af48211de`
- **Bounds:** this session; no paid services or deployment; two review/fix rounds; stop and report at limits

## Scope

Create a self-contained interactive browser demo for first-time readers. The viewer coordinates a fictional reversible release-note task and explores normal completion, failed review, interruption/handoff, and an out-of-scope publication request. Every simulated actor, verdict, identifier and record must be distinguished from actual operating evidence.

- **Acceptance:** useful initial view; working scenario choices and task transitions; separate review and integration gates; fixed candidate/recheck semantics; bounded recovery and owner-reserved actions; explicit cooperative-access limits; no network calls, credentials, real agents or external mutations; keyboard access, responsive layout, reduced-motion support; a repeatable check and usage guide; independent fixed-candidate review followed by coordinator verification.
- **Dependencies:** existing charter, workflow, access profile and handoff; no configured operational system required.
- **Access:** read repository governance and records; executor writes `demo/`, this task, its own progress, and a README demo entry. Reviewer writes only `records/reviews/R-GOV-006-01.md`. Local file, Git and browser verification tools permitted. No governance amendment, historical-record rewriting, publishing, runtime grants or operational activation.
- **Contract:** portable browser entry point; no build/install step; fictional demonstration records kept in the browser, separate from actual governance records. Actual creation checks recorded in Git.
- **Write ownership:** `/root` owns demo and integration paths; separate reviewer owns its review record. Reviewer does not edit the implementation.

## History

- 2026-10-05: proposed → ready → active. User requested demo; coordinator scoped a local explanatory simulation, pinned current governance, and reserved reviewer record. This does not authorize an operational trial. Independent review assignment and final verification pending.
- 2026-10-05: active → cancelled. User paused implementation to choose the demo approach, then selected a live events-agency challenge. No demo implementation was created. Retain this initial assignment as history; [T-GOV-007](T-GOV-007.md) covers the newly requested Luna planning work.
