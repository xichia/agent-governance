# X04 offline resolver protocol

## Purpose and limits

This is a deterministic, scripted mechanics probe for source identity, scope,
expiry, and retrieval availability. It is not an LLM run and does not measure
model reliability, throughput, or comparative quality. The fixture's
`authoritative` identity is trusted input for the exercise; SHA-256 binds a
record's serialized bytes to that identity but does not authenticate who
authored the record.

The runner is Python standard-library only. It reads the one fixture path
passed on the command line. It never follows a source pointer, opens paths
named in fixture data, imports fixture code, or uses the network. Records must
be embedded in `memory`, `local_sources`, or an available retrieval result.
`expected` is kept out of the resolver's allowlisted input view and is read
only afterward for a separate oracle comparison.

## Fixture contract

The top-level JSON object has `schema_version: 1` and a `cases` array. Each
case uses the fields below; the plan's shared interface is authoritative.

| Field | Meaning |
| --- | --- |
| `id` | Stable case identifier. |
| `mechanism` | `current`, `stale`, `missing_fact`, or `absent_retrieval`; descriptive metadata. |
| `condition` | `A` full local sources, `B` selective/index with retrieval, or `C` no-index ablation. |
| `request` | `{key, scope, as_of}`; `as_of` is an exact `YYYY-MM-DD` date. |
| `authoritative` | Trusted `{source_id, version, digest}` identity. All fields must be nonempty strings and digest must be lowercase 64-character SHA-256 hex. |
| `memory`, `local_sources` | Ordered arrays of candidate records. Missing arrays behave as empty; malformed non-arrays are logged and treated as empty. |
| `index` | Array of identity descriptors. A malformed descriptor is rejected and logged. |
| `retrieval` | `{state, records}` with state `available`, `missing`, or `failing`. Records are usable only for `available`. |
| `expected` | Independent oracle object with `status`, `value`, `source_id`, `version`, `complete`. Never passed to the resolver. |

A source record contains `source_id`, `version`, `key`, `scope`, `value`,
`valid_until` (inclusive `YYYY-MM-DD`, or JSON `null` for no expiry), and
`digest`. The digest is SHA-256 over UTF-8 canonical JSON of the whole record
except `digest`, with sorted keys, compact separators `(',', ':')`,
`ensure_ascii=False`, and no non-finite JSON numbers. A record qualifies only
when its digest verifies and its source id, version, and digest exactly equal
the trusted identity; its key and scope exactly equal the request; and its
expiry is absent or is on/after `as_of`. Value comparison is JSON structural
equality. Invalid records are rejected with an event reason, not promoted.

## Resolution and routing

The resolver checks in-fixture memory, then local records, in listed order.
It accepts the first valid qualifying record. It does not infer or complete a
fact from a stale version, different scope, invalid date, digest mismatch, or
untrusted identity. If neither local group qualifies, it routes by condition:

* **A:** no retrieval call; the fixture's local source bundle is the available
  full-source channel.
* **B:** retrieval is considered only if at least one index descriptor exactly
  matches all three trusted identity fields. With that match, the runner logs
  retrieval as attempted and distinguishes `missing`, `failing`, and
  `available`. Only records in an `available` result are examined.
* **C:** retrieval is always skipped as the no-index ablation.

Unknown conditions skip retrieval. A malformed trusted identity/request makes
resolution safely unresolved. Retrieval data supplied with a missing/failing
state is never inspected. If no qualifying record is found, the output is
`status: unresolved`, null value/source/version, and `complete: false`.

Each per-case observation contains the status/value/source/version/completeness
fields, selected evidence identity and channel (when current), plus ordered
events. Events record lookup routing and candidate acceptance/rejection so an
unresolved answer can be distinguished from missing retrieval, failed
retrieval, no matching index, invalid input, or invalid/stale evidence.

## Evaluation and metrics

The runner emits JSON on stdout. `observations` contains a per-case observation
and a separate `comparison` against that case's authored expectation. The
comparison checks `status`, `value`, `source_id`, `version`, and `complete`;
differences are reported by field. Exit status is zero only when every case
matches; fixture read/envelope errors return status 2, and oracle mismatches
return status 1. Malformed individual inputs are represented as safe
unresolved observations and can still be compared without terminating the
batch.

`completeness` reports case count, expected and observed complete counts, and
the count of cases whose complete flag agrees with an otherwise fully matching
oracle result. `oracle_comparison` reports expected-output match counts and
invalid expected objects. These are correctness/completeness measures, not
calibration.

`calibration` is deliberately a narrow **evidence support rate**, not
probabilistic calibration: the runner independently rechecks every emitted
current/complete claim against the accessible fixture inventory, revalidating
the trusted identity, digest, requested key/scope, date window, and emitted
value without consulting `expected` or the resolver's events. It reports the
number of current claims, independently supported claims, unsupported current
claims, and supported/current rate (null when there are no current claims).
An unsupported current claim is a false verified/current claim relative to
the valid accessible evidence in this fixture. This metric cannot establish
truth beyond the fixture, assess confidence calibration, or detect a
consistently wrong trusted identity supplied by the fixture author.

## Validation scope

The runner is intended to be invoked as `python3 fixture_runner.py cases.json`
from this directory. It performs no writes. The independent fixture writer
owns `cases.json`; this implementation does not manufacture or edit expected
outputs. Resolution is scripted and deterministic; successful fixture
comparison demonstrates conformance to this mechanical protocol only.
