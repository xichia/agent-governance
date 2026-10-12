# Repository improvement implementation — solo delivery

2026-10-12 · RSI-20261012-01/T-GOV-023. **Implementation finalized after the owner-approved third repair; independent acceptance still pending.** The owner requested recursive self improvement, then solo execution. No subagent, Luna session or Astra was dispatched. Coordinator self-checks are not independent review.

## Delivered value and observable behavior

The new [CLI](improve.py) implements artifact auditing, reproducible fixture execution, same-suite candidate comparison and bounded next-cycle proposals. [Catalog](catalog.json) pins eight existing reusable artifacts and their limits. [Backlog](BACKLOG.json) ties changes to source evidence and a decision/stop rule. The first [cycle](cycle-001/cycle.json) preserves separate baseline/candidate reports, exact hashes and [assessment](cycle-001/assessment.json).

On eleven frozen synthetic artifact checks, the new byte-bound auditor matched11/11expected outcomes versus5/11for a newly written existence-only baseline: six gains, zero lost controls. This baseline is not historical repository performance. All eight real catalog entries match the selected source686ebe4 and expected bytes; that checks continuity, not factual correctness or authority.

All20predeclared controls matched:11artifact cases plus9comparison/recovery gates. Sixteen additional probes matched, including FIFO rejection, self-review rejection, preserved child budgets/regressions, decreasing repair counters, no-gain parents and structured missing-cycle failures. [Results](control_results.json) preserve the actual observations and source digest. A gain is always `review_pending`, `accepted:false`; proposals never dispatch or modify code. Conditional review-record matching is cooperative syntax/byte checking, not proof of a genuinely distinct reviewer.

The planning comparator was the five adversarial grading controls of06, with a nominal fourfold20control target. It is not fourfold coverage of06's256 native rows, independent learning, throughput, cost or agent performance. No new model trials, public source claims or efficiency comparisons were made. Event records contain observed local subprocess start/end/exit/output identity only; active model time, queue, tokens and costs remain unknown.

## Corrections, negative results and unresolved gates

The original two solo artifact repair rounds were used, both preserved in [findings](findings.json), exact archived source in `history/`, and [reproduction script](reproduce_findings.py):

- Round1: reject boolean schema versions and whitespace self-review aliases; reject child assessment through a no-gain parent despite a supplied review label. Source before correction SHA3fbcca65bd9dba3b7e5e7e3eb79653153a7911bccf8bc282fbbceccd7de83ef1. That exact earlier version was recovered from the scoped diff and hash-verified, then its failure paths were actually rerun. No historical artifact was reconstructed or rewritten.
- Round2: existence-only audit previously labeled byte matching true; it now leaves that field null/unknown. Source before correction SHA695eb82eb405fc687a6f455c9f89bf922162116eaa662bd9a9d0b52b0dbde6c7. Reproduction confirms the before/after result. Actual final source SHA204369ea9b1b595069f35fa0fb5e1759109996a987a329e9ea090a5f09c1b828.

The original [NEG-01 probe](robustness_negative.json) supplied a hash-matching JSON array instead of a report object and exited1with AttributeError. That failing output and the proposed two-line patch are preserved. The owner then said “yes finalise implementation commit and push,” approving one additional repair and publication of the work branch. [Authorization](repair-003/authorization.json) is a dated owner-directed extension for this artifact, not an old-budget reset or review claim.

Round3applies the diagnostic boundary correction and represents the necessary one-off extension explicitly. The original FREEZE and cases remain byte-identical. Current [cycle](repair-003/cycle.json) has3repairs used; its bound extension permits precisely2→3, with inherited cycle/deadline bounds and no fourth repair. The helper validates serialized records; actual owner identity and authority still require the real chat/operator context. This does not authenticate arbitrary JSON labels.

The fresh solo checks matched all20original controls,16original additional checks, and11repair-specific controls. NEG-01 now returns structured invalid_evidence/acceptedfalse with no traceback; malformed top-level suite data also returns a structured error. New tests reject missing/oversized/wrong-lineage allowances and preserve extension inheritance. [Results](repair-003/repair_results.json), [fresh assessment](repair-003/assessment.json), raw reports and observed local subprocess events are saved separately from the original evidence. Source before third repair204369ea is retained exactly in history/before-round-3.py. Latest source and fixed candidate are pinned in the repair-003manifest and checkpoint.

Independent fixed-candidate review remains unavailable under solo execution. The implementation and commit/push request can be finalized, while artifact acceptance stays review pending. No required review is fabricated or silently waived; future promotion remains gated and no next implementation cycle is dispatched.

## Practical use and limits

Use the catalog audit for explicit byte-bound pointers and the evaluation commands for complete, typed local example records. Do not treat a JSON verdict, score, digest, self-report, unsigned reviewer label or Git authorship as evidence of authority or real independent review. The fixture oracle is root-authored, not independently frozen. Parent cases are retained, but new oracle validity needs actual scrutiny. Trusted root/process, hardlinks and concurrent tampering remain limitations; arbitrary prose/source truth or model reading is not checked.

No existing governance, source pack, uploaded workflow, old task, accepted01–06, X01 or old07 artifacts were modified. The first prototype is intentionally new and offline. The original07remains held; this owner-selected RSI direction does not implement its checker. Previous exhausted repairs, generation limits, hourly/end settings and October15 boundary remain unchanged.

Exactly one live handoff continues SAME RSI package for the remaining independent review: recover the finalized candidate; preserve all results/counters and the owner-approved extension; perform actual independent review only when available and authorized; verify source/record scope before truthful package acceptance. Do not run another cycle while the gates are unresolved. Full instructions and reproduction commands are in [README](README.md).
