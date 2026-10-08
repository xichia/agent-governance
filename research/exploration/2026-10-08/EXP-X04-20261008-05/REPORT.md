# Observed service and tool-assisted status transitions — EXP-X04-20261008-05

The64frozen crossed transitions produced64initial and64final records from four separate configured-Luna sessions. Final answers matched20current and44safe-unresolved expectations, with zero false-current claims in this fixture set. All workers used locally written classification scripts; this supports the bounded tool-assisted workflow, and leaves unassisted model status preservation untested. No general reliability or model superiority result follows.

## Actual evidence

[PLAN](PLAN.md), [frozen oracle](groundtruth.json), [input manifest](frozen_manifest.json), [actual root invocation](invoke_broker.py), [grader](grade_trials.py), [full observations](observations.json), [execution method/exposure](METHOD.md), [native messages](native_dispatches.json). Inputs frozen2861fa78f0dc58197130e033c084afa3a15bdf92 BEFORE first executor dispatch. Initial snapshots and root response service were committed5f6619232e5c9e7018f81a2149367fcbb0a5b37d before grading; raw trial files unchanged, no answer corrections.

| Measure | Initial | Final |
|---|---:|---:|
| Delivered records / expected matches |64/64|64/64|
| Factual recovery |16|20|
| Safe unresolved |48|44|
| False current claims |0|0|

Root broker64requests:32served,16denied withdrawn grants,16changed-content mismatches. No fabricated unavailable/missing/failing events; those04cases were not rerun here. All submitted requests match declared identity/path/scope/assignment and final service status/reason/sequence correspond to root receipts.32served includes12scope/expiry-invalid final tasks and20admissiblecurrent tasks. Initial→final transitions:5current→current,11current→unresolved,15unresolved→current,33unresolved→unresolved. Superseded local/memory values never silently retained as current in these emitted records. Safe unresolved is not factual recovery or probabilistic calibration. Initial 'service correspondence' in grader is a vacuous/not-applicable true field; actual service-field correspondence checked only in final records.

Root independently decoded exact served bytes and reconstructed rawSHA/counts/event sequences/manifest continuity. Denied no bytes/hash; changed only observedhash/count without payload.64events are local process observations; time_source process_wall_clock, caller_authenticated=false. Raw served byte SHA differs from initial canonical record digest rule and final answers used the declared correct raw hash. Native final message delivers pointer/hash to coordinator-owned shared file, not inline byte payloads or authenticatedcaller identity. See METHOD for actual tool-assisted computation and access deviations/self-report limits.

## Coverage, negative results and review status

Target64cells is4x nominal comparable03's16actual output count, not measured throughput. The16prior families retain different memory/currentness/missing-fact predicates, crossed with four update mechanisms. Original routing deferred, repeated facts/source-family clustering and scripts reduce independent behavioral coverage. This is64distinct provenance/update cells, not64independent reasoning attempts. Scombined4cases exercise two simultaneous invalidities without isolating detectioncause. No filler/new ideation IDs introduced; hypotheses T01/T02/T03/X04 and S03/E05/X05 preserved.

First freeze generator failed on null valid_until atfd84ec3; no packets/oracle/model dispatch existed then despite premature commit title. Null=noexpiry preserved from02, explicit packet rule fixed before successful inputfreeze2861fa7. Counted conservatively as repairround1overall for this artifact; maximum2, one remains. No current oracle or raw answer changed after dispatch. Later review finding/disposition must be recorded in new R018 records; **separate review pending**, no pass claimed here. Shared-context review is evidence-first, not blind. No X01 repair/import/reset; it remains blocked1191ac83 with two repairs exhausted.

## Recommendations (judgement, not operational authority)

1. Preserve exact served-byte receipt and final query admissibility separately;12served receipts did not warrant a current answer.
2. Keep root-owned service records separate from raw agent-owned answers, with initial-before-response hashes.
3. Record classification method: scripted assistance is useful reproducible evidence but does not test unaided model memory reasoning.
4. Use the successor to probe semantic preservation under varied context presentation without row-classification scripts, retaining raw mistakes and exposure limits.

These recommendations refine existing IDs only, require their own scoped review, and do not alter governance. Their benefits beyond these fixtures remain unmeasured. [One proposed successor](NEXT_PACKAGE.md) specifically addresses the scripted-classification limitation; no successor executor dispatched.

## Provenance and unchanged unknowns

Accepted04brokerffb52d9f93f94569b2cabc47a305586536b53c22/R01701; prior03packetced1ebb54fd9ff4c09c5d34d9af93da66d62053b/raw966e62ce8e90bfd376333e5b3bf80a677845a256;02candidate5c5a08a4b619899199e5bb5d5155e99af38b35bf;01primaryregisterd46484fd36f013810decc5c79f8f3aa5e15489cc. No new primary-source scan/publication claim here; source descriptions are not measuredbenefits, docsdates stillunknown. No real operations, network/API/spend, usage/cost/queue metrics or authenticated backend/source identities. Source authority/root/process/file access remain trusted fictional/cooperative assumptions, not a securityboundary. Future runtime/storage/scheduler execution not guaranteed.
