# Raw idea pool — context, memory and external developments

Generation only; entries are unranked, unevaluated proposals. Lens: context/memory/tool-routing alternatives and assessment of new external developments. Contributor/session: `/root/ideation_context`; configured model `gpt-6-luna`; backend deployment identity unavailable. No external development claims were researched or verified for this batch.

## T01 — Decision-linked context packets

- **Lens:** Context selection
- **Contributor/model/session:** `/root/ideation_context`; configured model `gpt-6-luna`; backend identity unavailable.
- **Idea:** For each task phase, assemble a small context packet from the current decision, its acceptance criteria, directly relevant artifacts, and unresolved dependencies. Keep an index of omitted sources with retrieval pointers so an agent can request additional context when it identifies a concrete need. This tests selective, task-linked context against indiscriminate broad context while preserving a path back to source material.
- **Proposed observable test:** Replay matched synthetic tasks with (a) the full relevant repository context and (b) a decision-linked packet plus the source index. Seed each task with one necessary fact outside the initial packet. Record correct task outcomes, unsupported claims, requests that retrieve the seeded fact, and context volume; check that packet users can recover the fact before making the affected decision.
- **Assumption to verify:** The task can be decomposed into decisions and dependencies well enough to build a compact packet, and agents will request missing source material instead of silently filling gaps.

## T02 — Memory with expiry and revalidation triggers

- **Lens:** Memory lifecycle
- **Contributor/model/session:** `/root/ideation_context`; configured model `gpt-6-luna`; backend identity unavailable.
- **Idea:** Store reusable memory as dated claims with scope, source, and a revalidation trigger (such as a changed policy version, task boundary, or elapsed review interval). At use time, classify each item as current, stale, or unverified; stale or unverified items can guide a lookup but cannot serve as established evidence. This gives memory a lifecycle instead of treating prior context as timeless.
- **Proposed observable test:** Create a fixture containing current, expired, superseded, and scope-mismatched memory entries. Change the relevant source for one entry, then ask an agent to prepare a new task. Observe whether it uses current entries, flags or rechecks the others, and avoids presenting stale content as current; repeat with the trigger removed to check the declared rule.
- **Assumption to verify:** Memory entries can carry reliable dates, scope, and source pointers, and useful revalidation triggers can be specified without making routine retrieval too burdensome.

## T03 — Capability-first tool routing with a fallback path

- **Lens:** Tool routing
- **Contributor/model/session:** `/root/ideation_context`; configured model `gpt-6-luna`; backend identity unavailable.
- **Idea:** Route each subtask by its required capability (for example, local text search, structured calculation, or primary-source retrieval) using a small, explicit tool capability map. Before dispatch, check that the tool is actually available; when it is absent or fails, switch to a declared lower-capability path that narrows the claim or marks it unverified. This makes routing depend on task needs and observed availability rather than tool names or assumed access.
- **Proposed observable test:** In a local mock router, present tasks requiring each listed capability while varying tool availability and injecting one tool failure. Compare chosen route and final claim status against a predeclared routing table; verify that unavailable retrieval does not yield a fabricated verification and that fallback outputs preserve the limitation.
- **Assumption to verify:** Tool capabilities and availability can be described in a compact map that stays accurate for the session, and safe fallback behavior can be defined for each consequential capability gap.

## T04 — External-development evidence cards with a novelty check

- **Lens:** Assessing new external developments
- **Contributor/model/session:** `/root/ideation_context`; configured model `gpt-6-luna`; backend identity unavailable.
- **Idea:** Assess a claimed new development through a dated evidence card: the specific claim and why it could matter to this prototype, primary-source publication/update date, source type, what changed relative to the existing baseline, and a replication or counterevidence check. Separate “newly found” from “newly published” and defer recommendations until the development survives that check. The card is a repeatable assessment method, not a standing feed of unverified novelty claims.
- **Proposed observable test:** Give reviewers a small synthetic packet mixing a genuinely later primary-source change, an older source discovered recently, a secondary-source summary, and a conflicting update. Have them complete cards independently against the packet; check whether they distinguish discovery date from publication date, support each stated change with a source, and leave unresolved conflicts marked uncertain.
- **Assumption to verify:** Relevant developments can be tied to accessible dated primary sources and a usable baseline; if dates, provenance, or comparison evidence are absent, the method must permit an “unverified” result.
