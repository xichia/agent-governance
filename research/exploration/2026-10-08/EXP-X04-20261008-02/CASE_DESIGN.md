# X04 predeclared fixture design

`cases.json` is the fixture oracle for this package. It was authored from the shared interface in `PLAN.md` before consulting any resolver implementation. The fixture data is fictional and synthetic. The oracle is independent of resolver output: a case is `current` only when a matching record is actually observable and passes identity, digest, request-key, scope, and date checks. A trusted authority descriptor identifies the expected source bytes; it does not itself reveal the value or establish authenticity. An inaccessible record, an index descriptor, or a supplied payload accompanying failed retrieval is not observed evidence.

All record digests are SHA-256 over the UTF-8 bytes of canonical JSON for the six fields `source_id`, `version`, `key`, `scope`, `value`, and `valid_until`, excluding `digest`; canonicalization uses sorted keys, compact separators, and `ensure_ascii=False`. Dates are ISO dates. Expiration is inclusive (`valid_until >= as_of`); `null` means no expiration. Source identity is the tuple `(source_id, version, digest)`. The source digest binds content and does not authenticate its publisher.

For every unresolved outcome, the value, source ID, and version are null and `complete` is false. For every current outcome, the value and source identity match a record visible through the allowed source path and `complete` is true. The separate `complete` bit lets downstream checks distinguish safe uncertainty from a fully recovered requested fact.

The shared A/B/C conditions are represented through actual case contents and retrieval metadata:

- **A** supplies a full local source bundle. Lookup can resolve from local records without a retrieval call.
- **B** supplies selective/index descriptors and tests available, missing, or failing retrieval. A matching pointer is necessary but not sufficient; the record bytes must also be observed and validate.
- **C** is the no-index ablation. Even when a fixture includes index or retrieval payload fields to probe misuse, they must not be used as retrieved evidence. A local record can still resolve in C.

There are four distinct cases per mechanism. Across all sixteen cases, A appears four times, B eight times, and C four times; the extra B cases cover retrieval-specific controls. Inventory version `v1` records 80 units and is superseded by `v2` at 40 units. The required storage limit is a separate necessary fact; the inventory discrepancy cannot be used to infer it.

| ID | Mechanism / condition | Predeclared result and purpose |
|---|---|---|
| `X04-CUR-01` | current / A | Current inventory 40 is present locally; resolve. |
| `X04-CUR-02` | current / B | Exact current inventory record is returned through its matching pointer; resolve. |
| `X04-CUR-03` | current / C | No-index mode still has the current record locally; resolve. |
| `X04-CUR-04` | current / B | Returned record's digest is altered and no local copy exists; unresolved despite trusted descriptor. |
| `X04-STA-01` | stale / A | Memory says 80 at v1; local superseding v2 says 40; resolve to 40. |
| `X04-STA-02` | stale / B | Memory says 22 at expired v2; matching retrieval returns v3 limit 18; resolve to 18. |
| `X04-STA-03` | stale / C | Only superseded v1 inventory 80 is visible; unresolved. |
| `X04-STA-04` | stale / A | Available lookalikes are wrong scope or expired before `as_of`; unresolved. |
| `X04-MIS-01` | missing_fact / A | Necessary storage limit 18 is present in full local bundle; resolve. |
| `X04-MIS-02` | missing_fact / B | Omitted storage limit is recovered through a matching pointer; resolve. |
| `X04-MIS-03` | missing_fact / C | Required limit is omitted and there is no index retrieval; unresolved. |
| `X04-MIS-04` | missing_fact / B | Inventory 40 (versus stale 80) is retrieved, but the separate required limit is absent; unresolved. |
| `X04-ABS-01` | absent_retrieval / B | No index pointer and only stale memory exist; unresolved. |
| `X04-ABS-02` | absent_retrieval / B | Exact pointer exists but retrieval is missing; descriptor alone is insufficient; unresolved. |
| `X04-ABS-03` | absent_retrieval / B | Retrieval fails and carries a payload; payload is not observed evidence; unresolved. |
| `X04-ABS-04` | absent_retrieval / C | No-index mode includes tempting index/payload plus stale memory; lookup is forbidden and result unresolved. |

The fixture also tests behavior beyond the four named mechanisms: a valid current record in a no-index condition; digest tampering; superseded records; request scope mismatch; inclusive expiry; a necessary fact omitted from inventory; and distinct pointer-absent, retrieval-missing, and retrieval-failing states. Case IDs and source identities are stable fixture identifiers. No case makes a claim about measured model reliability, speed, or comparative performance.
