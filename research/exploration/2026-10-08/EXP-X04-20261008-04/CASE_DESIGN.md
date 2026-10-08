# EXP-X04-20261008-04 case oracle

This file documents the independent fixture oracle for the 16 scenarios frozen in PLAN.md. The expected outcomes were transcribed from that predeclared matrix and reasoned from the trusted `grants.json` entries and fixture inventory. They were set without reading broker implementation or broker output.

`cases.json` uses schema version 1 and contains exactly B01–B16. Every case has a stable ID, the complete retrieval request, an expected status/reason pair, and a rationale. The expected oracle is deliberately limited to status and reason; timestamps are runtime evidence and vary between executions.

B01 and B03 deliberately have identical request fields, including `request_id: req-B01`. They represent separate calls and must remain separate cases/events. B16 uses the valid G-good authorization fields but claims `caller_label: external-claim-16`; that label is untrusted and does not authenticate the caller or invalidate the grant.

| Case | Reachable predicate | Expected status/reason |
| --- | --- | --- |
| B01 | Valid read grant, matching digest | served / verified_bytes |
| B02 | Valid zero-byte read grant | served / verified_bytes |
| B03 | Repeat B01 request ID in a distinct invocation | served / verified_bytes |
| B04 | Authorized path absent from fixture root | missing / not_found |
| B05 | Matching grant in injected failing mode | failing / injected_failure |
| B06 | Readable granted file whose bytes differ from pinned digest | changed / content_mismatch |
| B07 | Unknown grant ID | denied / grant_not_found |
| B08 | Empty path string | denied / invalid_path |
| B09 | Absolute path | denied / invalid_path |
| B10 | Parent-directory component | denied / invalid_path |
| B11 | Backslash in path spelling | denied / invalid_path |
| B12 | Dot component | denied / invalid_path |
| B13 | Safe relative path not equal to the grant path | denied / path_not_granted |
| B14 | Assignment differs from grant | denied / assignment_mismatch |
| B15 | Scope differs from grant | denied / scope_mismatch |
| B16 | Valid authorization with a different claimed caller label | served / verified_bytes |

This is a fixture oracle, not a general security proof. It does not establish global mediation, durable or tamper-resistant event storage, authenticated caller identity, or protection from trusted-root/process tampering beyond the frozen contract.
