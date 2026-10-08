# EXP-X04-20261008-01 — Primary-source evidence register

Writer: `/root`, GPT-6 coordinator; backend deployment identity unavailable. Retrieved **2026-10-08**, public-source content inspected in this activation. Package/task: [T-GOV-014](../../../../records/tasks/T-GOV-014.md). Seven sources below include all three handoff leads. Date statements are page publication/update labels; undocumented later revision dates remain unknown. None is established as newly published during this October research week. No paid/API trial or local model-performance experiment occurred.

## X04-S01 — Scoped delegation and artifact references

- **Primary source:** [Anthropic, How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).
- **Date / novelty:** published June 13, 2025; established background, lead re-inspected now. Later update date unverified.
- **Supported description:** delegated research tasks specify objectives, output formats, tools/sources and boundaries; independently stored subagent artifacts can be returned through lightweight references. Its long-horizon discussion also describes stored plans and memory.
- **Evidence type / locator:** vendor engineering account; “Teach the orchestrator how to delegate,” “Long-horizon conversation management,” “Subagent output to a filesystem.”
- **Baseline relevance:** T01 context/source pointers, T03 capability selection and X04; consistent with recorded disjoint artifact ownership, not proof of optimal staffing.
- **Limitation:** proprietary research experience/internal evaluations do not establish benefit for our event-planning case or authenticated receipt/ownership enforcement.
- **Discriminating test (proposal):** seed one necessary fact outside an initial packet; require retrieval from its supplied artifact pointer before the affected decision. Missing pointer must yield a visible unresolved item.

## X04-S02 — Inspect workflow traces before formal comparisons

- **Primary source:** [OpenAI, Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals).
- **Date / novelty:** publication/update date **unverified**; current documentation inspected October 8, not a dated new development.
- **Supported description:** trace records include model/tool calls and handoffs; structured grading can investigate tool choice, routing and instruction-following; repeatable datasets/eval runs support later comparisons.
- **Evidence type / locator:** official documentation; “Start with traces when you are still debugging behavior,” “Move to datasets and eval runs when you need repeatability.”
- **Baseline relevance:** T03 routing, T04 evidence cards and X04 measurement; the existing rehearsal lacks complete queue/usage/coordinator telemetry.
- **Limitation:** documentation is not evidence that all advertised hosted surfaces are available to this runtime; read lifecycle card S07 before tooling recommendations. Grader agreement is not factual correctness.
- **Discriminating test (proposal):** a scripted missing-tool case must record attempted capability, observed unavailability and narrowed claim status, rather than a fabricated successful verification.

## X04-S03 — Manager delegation versus control transfer

- **Primary source:** [OpenAI Agents SDK, Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/).
- **Date / novelty:** publication/update date **unverified**; undated documentation re-inspected, not an October release claim.
- **Supported description:** orchestration can be decided by a model, by code or a combination. Agents-as-tools retain a manager's control; SDK handoffs transfer the active turn to a specialist.
- **Evidence type / locator:** official SDK documentation; “Core SDK patterns” and “Orchestrating via code.”
- **Baseline relevance:** T03 capability-first routing and X04; control transfer and artifact ownership should be explicit instead of being inferred from role titles.
- **Limitation:** these SDK patterns are not proof our collaboration tools implement identical semantics or that deterministic routing is more efficient on our tasks. No SDK deployed.
- **Discriminating test (proposal):** a declared capability map routes a bounded lookup with and without retrieval availability; only the authorized active owner edits the final artifact, and absence produces an unverified result.

## X04-S04 — Retrieve on demand, retain structured notes

- **Primary source:** [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
- **Date / novelty:** published September 29, 2025; older methodology newly inspected for this package, not newly published this week. Later update date unverified.
- **Supported description:** lightweight source identifiers enable runtime context retrieval; compaction, structured notes outside the context window and subagents are different long-horizon techniques. It warns that compaction may discard important details and retrieval has tradeoffs.
- **Evidence type / locator:** vendor engineering guidance; “Context retrieval and agentic search,” “Compaction,” “Structured note-taking.”
- **Baseline relevance:** T01 selective packets and T02 memory lifecycle. **Claim expiry/version revalidation is our proposed extension**, not a verified requirement or measured result of this article.
- **Limitation:** retained notes can be incomplete/stale; documented approaches do not guarantee completeness, recoverability or local performance.
- **Discriminating test (proposal):** compare a full source bundle with a smaller packet plus retrievable pointers, using the same omitted dependency and a superseded memory claim; report wrong/unresolved/recovered states separately.

## X04-S05 — Recoverable history separate from active context

- **Primary source:** [Anthropic, Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents).
- **Date / novelty:** published April 8, 2026; established 2026 architecture background, reverified from prior unreviewed source checkpoint. Later update date unverified.
- **Supported description:** session event storage, harness and sandbox are separate interfaces; past events can be retrieved independently of the model's currently retained context.
- **Evidence type / locator:** vendor engineering account; component abstraction, “Recovering from harness failure,” “The session is not Claude's context window.”
- **Baseline relevance:** T01/T02 and X04/X05: retain source/event pointers for recovery instead of treating a summary as the complete record.
- **Limitation:** the provider's durable-session guarantees and latency claims do not transfer to Markdown files or this automation. No hosted system tested.
- **Discriminating test (proposal):** discard a summary detail but retain its source/event record; verify reconstruction recovers the authoritative version. Missing record must remain unavailable.

## X04-S06 — Managed harness options, not installed continuity guarantees

- **Primary source:** [OpenAI, Introducing the Agents API](https://openai.com/index/introducing-the-agents-api/).
- **Date / novelty:** published September 10, 2026; recent pre-week announcement, **not** newly published October 8. Reverified from prior unreviewed seed notes.
- **Supported description:** announces a public-beta managed Codex harness with context compaction, tool search/programmatic calls, subagent support and execution-environment choices.
- **Evidence type / locator:** official product announcement; introduction, “Keep agents working across long sessions,” tool-use/subagent sections.
- **Baseline relevance:** T01/T03 and X04: capability availability, saved state and execution environment are separate concerns.
- **Limitation:** product/customer performance statements are not a matched local evaluation or proof the scheduled runtime can work continuously for an hour; no API purchase, credentials or deployment authorized.
- **Discriminating test (proposal):** a local capability declaration and saved checkpoint must state unavailable execution/retrieval honestly; test a recovery protocol without assuming a managed product is installed.

## X04-S07 — Dated product lifecycle can qualify undated guides

- **Primary source:** [OpenAI, Introducing AgentKit](https://openai.com/index/introducing-agentkit/).
- **Date / novelty:** original page October 6, 2025; explicit update **June 3, 2026**. Existing lifecycle notice discovered/reverified now; not a new weekly announcement.
- **Supported description:** updated notice says Agent Builder and Evals products are winding down and unavailable from November 30, 2026; it recommends Agents SDK for workflows continuing as code.
- **Evidence type / locator:** official dated update near page top, before original launch text.
- **Baseline relevance:** T02 revalidation and T04 novelty/source dates; prevents recommending a hosted surface from older/undated launch guidance alone.
- **Limitation:** this notice is product-specific; it does not establish that every evaluation method/API or SDK is discontinued. Actual migration/API coverage needs separate checks.
- **Discriminating test (proposal):** an evidence packet containing old launch text plus a dated lifecycle update must identify the superseding notice and mark unsupported current-availability claims unverified.

## Observations, negatives and limits

All three specified leads and four contextual primary sources were reachable and inspected; no source-access failure observed here. Two documentation publication/update dates remain unverified. We found no source establishing new publication during this research week, no local comparative performance measurements and no proof of enforceable global ownership. Prior seed's repository-absent observation is superseded for this activation by actual local inspection, not by these sources. Source-card tests above are proposals, not completed experiments or additional bulk ideas. Pending independent fixed-candidate review.
