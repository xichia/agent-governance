# EXP-X04-20261008-04 — retrieval events

Task T-GOV-017, coordinator /root, charter 0.1.1. Activation start 2026-10-08T04:03:19Z (12:03:19 Perth); claim 2026-10-08T04:05:11.506575+00:00, base 24fdefcd6178edc56ea8a7139222bf2d122c48ce. Checkpoint by05:03:19Z if interrupted/incomplete. Current thread matches this automation; only root active before claim, previous03 accepted966e62ce8e90bfd376333e5b3bf80a677845a256/R01601 and released ownership. Atomic new directory/OWNER claimed before dispatch. Repository/Python/native collaboration available, no network required.

## Frame and target

Objective: a local broker that records what it serves or declines, with16 predeclared access-event scenarios.03 produced matching model outputs but source-read reports remained unaudited. This tests T03/X04 and S03/E05/X05; it does not repair or import blocked X01. Prior comparable T03 proposal had four route states; approximately4x coverage target16 distinct access scenarios, not measured throughput relative to03's16 outputs. No equivalent actual broker benchmark.

Facts: fictional trusted manifest and source bytes below are coordinator supplied; caller labels are untrusted. Assumptions: fixture root/config trusted and local standard library available. Questions: does each reachable grant/path/assignment/scope/content predicate produce the declared event? Hard constraints: new isolated paths; no operations/network/spending/secrets/governance/history/X01 edits; no new ideas; distinct review; at mosttwo artifact repairs. Comparative criteria separate: byte/status accuracy, reconstructable events, explicit error/unknown provenance and feasibility. No role or efficiency ranking.

## Frozen contract BEFORE implementation

Coordinator sole writer grants.json and fixtures. Manifest schema_version1, grants array with grant_id/path/assignment/scope/sha256/mode(read or failing). Root fixture paths relative POSIX strings, no absolute, backslash, empty component, dot/dotdot, NUL; do not normalize forbidden spelling into permission. IDs and scopes exact nonempty strings. SHA256 lowercase64hex, raw bytes. No duplicate grant IDs; malformed trusted manifest must fail closed (explicit invalid config, no source reads).

Request fields: request_id, grant_id, assignment, scope, path, caller_label (untrusted label). Request IDs need not be unique: repeating them produces separate event sequences, never overwrites. Broker checks object/field shape, safe path spelling, grant ID, exact grant path, exact assignment, exact scope, then injected manifest mode. Only authorized read-mode files may be opened. Root is trusted fixture directory; no symlink components or nonregular files may be read. Use safe descriptor opens/no-follow where supported, reject unsupported safety rather than claim it. No arbitrary source/network paths; no actual security sandbox claim. Trusted-root/hardlink/process tampering outside threat model explicitly disclosed.

Statuses/reasons: invalid/invalid_request; denied/invalid_path, grant_not_found, path_not_granted, assignment_mismatch, scope_mismatch or unsafe_file; failing/injected_failure or io_failure; missing/not_found; changed/content_mismatch; served/verified_bytes. Never return source payload except served. Changed may disclose observed digest/count, not bytes. Missing/denied/failing should have no digest and zero served count. Served payload base64 encodes exact bytes; raw SHA256 equals trusted grant. Empty bytes are valid served evidence. File metadata/log receipt doesn't prove model understanding or globally mediated access.

Each request emits one event in a retained sequence, including malformed or failed requests: seq (1-based monotonic in this batch), request_id or null, claimed caller_label, caller_authenticated=false, requested_path, grant_id, assignment/scope, status/reason, observed_sha256 or null, observed_byte_count (0 when no bytes read), served_byte_count, observed_at UTC ISO timestamp, time_source=process_wall_clock. No inferred queue/agent active time/cost. Broker.events retained in memory; CLI prints all records and coordinator persists stdout. No crash-durable append or anti-tamper/authenticated ledger guarantee. Repeated requests remain separate events.

Public API `Broker(root, grants).retrieve(request)` returns status, reason, payload_b64 (null unless served), event. CLI `python broker.py --root fixtures --grants grants.json --cases cases.json` prints JSON with results, events, comparison/mismatch counts; validates fixtures but resolver never consults expected fields. Expected oracle: cases envelope schema_version1/cases array; each case {id,request,expected:{status,reason},rationale}. CLI can compare expected status/reason after retrieving. Exit nonzero on mismatch/envelope/config errors. Runtime timestamps vary; compare deterministic status/content/sequence fields across repeats after retaining original observed timestamps.

## Frozen16-case oracle matrix

All ordinary requests use A1/S1 and caller_label local-unverified. Matrix materialized independently by case writer without consulting broker code; cases are implementation tests, not new ideas.

| ID | Variation | Expected status/reason |
|---|---|---|
| B01 | G-good/good.txt valid | served/verified_bytes |
| B02 | G-empty/empty.txt | served/verified_bytes |
| B03 | G-good repeat B01 exact request_id | served/verified_bytes, distinct event seq |
| B04 | G-missing/missing.txt | missing/not_found |
| B05 | G-failing/good.txt | failing/injected_failure before open |
| B06 | G-changed/changed.txt expected old hash | changed/content_mismatch |
| B07 | nonexistent grant, safe good.txt | denied/grant_not_found |
| B08 | G-good path empty | denied/invalid_path |
| B09 | G-good absolute /outside/not-real.txt | denied/invalid_path |
| B10 | G-good ../good.txt | denied/invalid_path |
| B11 | G-good backslash path | denied/invalid_path |
| B12 | G-good ./good.txt | denied/invalid_path |
| B13 | G-good safe ungranted.txt | denied/path_not_granted |
| B14 | G-good good.txt wrong assignment A2 | denied/assignment_mismatch |
| B15 | G-good good.txt wrong scope S2 | denied/scope_mismatch |
| B16 | G-good good.txt valid, different claimed caller | served/verified_bytes; caller_authenticated=false |

## Ownership and acceptance

Coordinator owns PLAN/grants/fixtures/report/observations/checkpoint/NEXT/OWNER and new T017 records. /root/broker_builder sole writer broker.py/protocol.md; /root/broker_cases sole writer cases.json/CASE_DESIGN.md. Both configuredgpt-6-luna, deployment identity unavailable; distinct /root/broker_review only new R017 reviews, after fixed candidate. Shared repository/history not blind or enforced agent isolation.

Acceptance:16 independent predeclared IDs/materialized oracle, all matrix outcomes, one event per request, exact served bytes/hash and unsuccessful-event null provenance; repeated ID does not erase events. Coordinator persists observations, independent reconstruction of summary/status/sequence/content and reproducibility with timestamp variation disclosed. Reviewer independently executes matrix plus new adversarial path/access probe, checks reachable predicates and report limits against fixed candidate. At mosttwo artifact repair rounds, all findings/dispositions recorded; source authority and global access limitations never waived. No token/cost/reliability/superiority claims. Exactly one grounded successor or SAME04 continuation.

Estimated elapsed stages8 recovery/framing,24 independent implementation/cases,10 event observations/integration,10 review,5 bounded fixes/verification,3 checkpoint/successor=60min. Stop/checkpoint at limit, no idle filler. Missing Python/repo yields reproducible unrun conversation protocol; contributors absent coordinator sequential with actual provenance; reviewer absent draft/self-check; uncertain ownership defer conflicts. Current X01 blocked/two repairs/no extension unchanged. October15/hourly boundaries retained.
