# Raw generation — practical reuse lens

Session: `/root/next_reuse` · configured model: `gpt-6-luna` · actual deployment/backend identity: unknown. Generated only N01–N04 for the authorized new pool. Shared repository/history is cooperative, not blind or isolated. These are proposals; no tests below have been run.

## N01 — A decision-oriented reuse index

- **Lens:** Practical reuse and useful deliverables.
- **Idea:** Prepare a compact owner-facing index that links the strongest reusable artifacts to their demonstrated use, limitations, and the question each could inform. Keep raw evidence intact and make the index easy to update as a navigation layer.
- **Evidence hook:** Existing value review identifies the rehearsal kit, governance/interface contracts, X04-02 fixtures, X04-04 byte-service receipts, and the X04-05/06 counterexamples as distinct reusable items, with explicit limits in `REV-VALUE-20261012-01/REPORT.md`. The index's usefulness is an assumption.
- **Proposed observable test:** In a bounded desk review, give an owner three concrete questions drawn from the appraisal; pass if the index leads to the supporting artifact and its stated limit for all three without an unsupported claim. Otherwise, decide whether the index needs a different organization or has insufficient value. Not run.
- **Assumption/prerequisite:** The owner expects to revisit or compare these findings; source links and stable paths remain available.
- **Burden/tradeoff:** Small initial writing task, with maintenance cost and risk of duplicating the report. May add little if the owner already navigates the source records easily.
- **Related prior work:** X04-01 source-card register and X04-02–06 evidence; this is a navigation reuse proposal, not a claim of a new finding.

## N02 — Adapt the rehearsal kit by replacing the fictional case only

- **Lens:** Practical reuse and useful deliverables.
- **Idea:** Treat the rehearsal pack as a reusable interface-and-checker template: map one owner-selected, still-fictional or safely bounded case into its existing schema, and list every field that cannot be grounded or does not fit before considering any code change.
- **Evidence hook:** `planning/events-agency/rehearsal/README.md` describes an invented local demonstration kit and explicitly separates mechanical consistency from reviewer judgments about audience value, accessibility, provenance, risk, availability, legal compliance, isolation, and approval. Whether another case fits the schema is unknown.
- **Proposed observable test:** A design-only schema mapping for one chosen case. Pass if each required field is mapped to supplied evidence or marked unknown, and a reviewer can identify schema gaps without silently filling them; fail/decision to stop if adapting requires unsupported facts or broad schema changes. No rehearsal or checker run proposed in this card; not run.
- **Assumption/prerequisite:** The owner can name a decision-relevant case and supply permitted source material; no real supplier or venue facts are inferred from the fictional fixture.
- **Burden/tradeoff:** Reuses a tangible interface, but could import assumptions from the fictional event domain and invite scope expansion. A failed fit is still useful evidence to leave the pack domain-specific.
- **Related prior work:** X02 (service-state/rehearsal case) and X01 (checker limits); no X01 repair is proposed.

## N03 — Reuse byte-service receipts as a narrow handoff audit pattern

- **Lens:** Practical reuse and useful deliverables.
- **Idea:** Extract the X04-04 receipt fields and event sequence as a small, implementation-independent acceptance example for future local handoffs that need to distinguish served, missing, changed, failed, and denied inputs. First check whether a proposed use actually needs byte-level provenance; do not infer that a receipt proves reading or understanding.
- **Evidence hook:** X04-04 `CHECKPOINT.md` records 16 declared cases and reconstructed payload/hash/count plus no-payload failure events, while stating that this does not prove model reading, caller authentication, authority authentication, or global mediation. Relevance to a future handoff is an assumption.
- **Proposed observable test:** Produce a one-page mapping from one owner-selected handoff to the receipt states; pass if an independent reader can distinguish the observed byte event from the separate claim that an agent used or understood the input, and all unobservable claims are marked as such. If the use case needs behavioral proof, decide not to reuse this receipt pattern alone. Not run.
- **Assumption/prerequisite:** A concrete local handoff has a decision-relevant dependency-integrity question and its input boundaries can be stated.
- **Burden/tradeoff:** Could avoid redesigning a useful narrow contract, but maintaining receipts adds coordination and record burden and can create false confidence if consumers overread them.
- **Related prior work:** X04-04 broker receipts and X04-03 reported lookup/read distinction.

## N04 — Preserve the counterexamples as a reviewable challenge catalog

- **Lens:** Practical reuse and useful deliverables.
- **Idea:** Make an implementation-neutral catalog of known failure examples with the triggering input, observed error, expected cautious interpretation, and provenance link. Use it to challenge future claims or proposed interfaces; do not convert it into an automatic pass gate or use it to reopen exhausted repairs.
- **Evidence hook:** The value review records X01's unresolved Unicode URL false accepts after exhausted repairs, plus X04-06 wrong-scope explanation, wrong event sequence, pointer/report mismatches, and empty-list deviations. These are specific observations, not proof the catalog covers the failure space.
- **Proposed observable test:** Have a separate reader trace each selected catalog entry to its source record and state what it does and does not establish; pass if every entry is traceable and none is described as a general validator or reliability result. A missing link or inflated inference fails the catalog review. Not run.
- **Assumption/prerequisite:** The owner values preserving these negatives for future design decisions; cited raw records remain available and may be read without modifying historical artifacts.
- **Burden/tradeoff:** Makes important failures easier to carry forward, but another index can become stale or mistaken for exhaustive regression coverage. X01 remains blocked unless the owner separately authorizes an extension.
- **Related prior work:** X01, X04-05, and X04-06; preserves their boundaries and does not claim novelty or repair.
