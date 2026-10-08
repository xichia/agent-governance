# X01 results — candidate awaiting independent review

Date 2026-10-08. Task [T-GOV-013](../../../../records/tasks/T-GOV-013.md); base `ca62b54`; coordinator `/root`, GPT-6. Builder and fixture author are distinct sessions configured gpt-6-luna, backend identity unavailable. Generation of the prior ideation pool is complete; this defined implementation preserves that pool and its provenance.

## Observations before review

The independent fixture author produced 40 cases: seven expected acceptances and 33 expected rejections. The coordinator reproduced all **40/40** expected outcomes using `PYTHONDONTWRITEBYTECODE=1 python research/exploration/2026-10-08/x01/run_cases.py`. The runner checks result type, exceptions and input immutability as well as acceptance. This is fixture coverage, not an exhaustive reliability rate. Cases were generated from the agreed task contract; after generation the author read the builder's contract and reconciled assumption/unresolved source-label fields. Review is not blind.

| Question | Observed candidate result | Practical limit |
|---|---|---|
| Do receipt labels bind actual dependency bytes? | Valid receipt accepted; changed bytes, recomputed substituted receipt and path/version/session/assignment mismatches rejected. | Manifest must be independently trusted. Matching a session string or hash does not establish authorship or reading. |
| Is modeled capacity dimensioned explicitly? | 40 chairs for 80 seated attendees rejected; missing/unknown chair reference rejected; overlap cases reject and adjacency/standing cases accept. | Only declared states and trusted units; no comprehensive attendee, duty, accessibility or service-plan validation. |
| Does copy conflict with attendance? | Deterministically rendered valid copy accepted; 180-versus-80 copy rejected. | Arbitrary paraphrases unsupported; no semantic prose comprehension claim. |
| Do evidence labels survive the envelope? | Declared supplied/verified/assumption/unresolved examples accepted; unknown source/status and missing verified-source metadata rejected. | Metadata presence is not factual verification, reachability or cross-revision epistemic tracking. |
| Are malformed values handled? | Fixture malformed nesting, unhashable field values and boolean-as-integer cases return errors rather than crashes. | No exhaustive hostile-input/security proof; custom Python objects and denial-of-service are outside the offline JSON-like scope. |

The coordinator also reran the prior four synthetic probes, in memory, against unchanged historical v2 and source files: arbitrary finance receipt labels, omitted chair references, reduced chair inventory and contradictory 180-adult copy still returned zero errors. Equivalent failure intents are rejected by the new fixtures. These use **different schemas and declared rules**, so the result supports the particular mechanism choices rather than a drop-in migration, matched whole-system benchmark, performance gain or general superiority claim. The original delivered run and historical verdict remain unchanged.

## Review, dispositions and verification

Pending separate fixed-candidate review. No final acceptance claimed yet. The reviewer must introduce additional boundary/negative observations and check the trust/semantic limitations. Any correction changes the candidate and requires bounded recheck. Post-review closure facts belong in the task or a new dated verification record; reviewed candidate results are preserved.

## Interpretation and next experiment

This study makes explicit acceptance rules inspectable and falsifiable while preserving valid exceptions. It cannot show that agents will honor the contract more reliably, that the real workflow gets cheaper, or that more/fewer roles are optimal. Those need matched runs with measurement. Next study: X02 state-by-state rejoin/refreshment accounting, keeping venue/service assumptions and owner choices unresolved unless real evidence supports them. A later historical-interface migration needs its own versioned assignment and review.

## Work-package timing

Estimated stage allocations total one hour; actual elapsed time and observed actions will be recorded at closure, with parallel activity and missing usage telemetry disclosed. No claim that this work occupied a guaranteed hour or that unused time was padded.
