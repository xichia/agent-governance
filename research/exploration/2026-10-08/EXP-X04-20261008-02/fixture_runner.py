#!/usr/bin/env python3
"""Offline, standard-library fixture resolver and independent fixture evaluator.

The resolver receives a deliberately restricted view of each case.  In
particular, expected outputs are only read after resolution, by the evaluator.
No source pointer is opened, imported, or fetched: all evidence must be present
as JSON records in the fixture.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


IDENTITY_FIELDS = ("source_id", "version", "digest")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
HEX_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_digest(record: dict[str, Any]) -> str:
    """Hash canonical UTF-8 JSON after removing the record's digest member."""
    payload = {key: value for key, value in record.items() if key != "digest"}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _iso_date(value: Any) -> dt.date | None:
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        return None
    try:
        parsed = dt.date.fromisoformat(value)
    except ValueError:
        return None
    # fromisoformat is intentionally paired with the exact YYYY-MM-DD shape.
    return parsed if parsed.isoformat() == value else None


def _trusted_identity(authoritative: Any) -> tuple[dict[str, str] | None, str | None]:
    if not isinstance(authoritative, dict):
        return None, "authoritative_not_object"
    identity: dict[str, str] = {}
    for field in IDENTITY_FIELDS:
        value = authoritative.get(field)
        if not _nonempty_string(value):
            return None, f"authoritative_invalid_{field}"
        identity[field] = value
    if not HEX_SHA256_RE.fullmatch(identity["digest"]):
        return None, "authoritative_invalid_digest"
    return identity, None


def _identity_from_descriptor(value: Any) -> tuple[dict[str, str] | None, str | None]:
    if not isinstance(value, dict):
        return None, "index_descriptor_not_object"
    identity: dict[str, str] = {}
    for field in IDENTITY_FIELDS:
        item = value.get(field)
        if not _nonempty_string(item):
            return None, f"index_invalid_{field}"
        identity[field] = item
    if not HEX_SHA256_RE.fullmatch(identity["digest"]):
        return None, "index_invalid_digest"
    return identity, None


def _record_problem(
    record: Any,
    trusted: dict[str, str] | None,
    request: dict[str, Any] | None,
    as_of: dt.date | None,
) -> tuple[str | None, dict[str, Any] | None]:
    """Return (reason, parsed evidence) without trusting malformed records."""
    if not isinstance(record, dict):
        return "record_not_object", None
    required = ("source_id", "version", "key", "scope", "value", "valid_until", "digest")
    for field in required:
        if field not in record:
            return f"record_missing_{field}", None
    for field in ("source_id", "version", "key", "scope"):
        if not _nonempty_string(record[field]):
            return f"record_invalid_{field}", None
    if not isinstance(record["digest"], str) or not HEX_SHA256_RE.fullmatch(record["digest"]):
        return "record_invalid_digest_shape", None
    try:
        actual_digest = canonical_digest(record)
    except (TypeError, ValueError, UnicodeError):
        return "record_not_canonical_json", None
    if actual_digest != record["digest"]:
        return "record_digest_mismatch", None
    until = record["valid_until"]
    if until is not None and _iso_date(until) is None:
        return "record_invalid_valid_until", None
    # Compute/validate content integrity before comparing trusted identity.
    identity = {key: record[key] for key in IDENTITY_FIELDS}
    if trusted is None or identity != trusted:
        return "identity_not_trusted_current", None
    if request is None:
        return "request_invalid", None
    if record["key"] != request["key"]:
        return "key_mismatch", None
    if record["scope"] != request["scope"]:
        return "scope_mismatch", None
    if until is not None and as_of is not None and _iso_date(until) < as_of:
        return "expired", None
    parsed = {
        "source_id": record["source_id"],
        "version": record["version"],
        "digest": record["digest"],
        "value": record["value"],
        "valid_until": until,
    }
    return None, parsed


def _request_view(value: Any) -> tuple[dict[str, Any] | None, dt.date | None, str | None]:
    if not isinstance(value, dict):
        return None, None, "request_not_object"
    key, scope = value.get("key"), value.get("scope")
    if not _nonempty_string(key):
        return None, None, "request_invalid_key"
    if not _nonempty_string(scope):
        return None, None, "request_invalid_scope"
    as_of = _iso_date(value.get("as_of"))
    if as_of is None:
        return None, None, "request_invalid_as_of"
    return {"key": key, "scope": scope}, as_of, None


def _records(value: Any, label: str, events: list[dict[str, Any]]) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        events.append({"type": "invalid_input", "field": label, "reason": "records_not_array"})
        return []
    return value


def resolve(case: dict[str, Any]) -> dict[str, Any]:
    """Resolve only from admissible in-fixture evidence; never reads expected."""
    events: list[dict[str, Any]] = []
    case_id = case.get("id") if _nonempty_string(case.get("id")) else None
    request, as_of, request_error = _request_view(case.get("request"))
    trusted, trusted_error = _trusted_identity(case.get("authoritative"))
    if request_error:
        events.append({"type": "invalid_input", "field": "request", "reason": request_error})
    if trusted_error:
        events.append({"type": "invalid_input", "field": "authoritative", "reason": trusted_error})

    # Search in the declared evidence order.  The resolver's input is stripped
    # of `expected` by run_case before reaching this function.
    groups = (("memory", case.get("memory")), ("local", case.get("local_sources")))
    for channel, raw_records in groups:
        records = _records(raw_records, channel, events)
        events.append({"type": "lookup", "channel": channel, "action": "searched", "count": len(records)})
        for position, record in enumerate(records):
            reason, evidence = _record_problem(record, trusted, request, as_of)
            if reason:
                events.append({
                    "type": "record_rejected", "channel": channel,
                    "position": position, "reason": reason,
                })
            else:
                assert evidence is not None
                events.append({
                    "type": "record_accepted", "channel": channel,
                    "position": position, "source_id": evidence["source_id"],
                    "version": evidence["version"], "digest": evidence["digest"],
                })
                events.append({
                    "type": "lookup", "channel": "retrieval", "action": "skipped",
                    "reason": "already_resolved_from_" + channel,
                })
                return {
                    "id": case_id, "status": "current", "value": evidence["value"],
                    "source_id": evidence["source_id"], "version": evidence["version"],
                    "complete": True, "evidence": {
                        "channel": channel, "position": position,
                        "source_id": evidence["source_id"], "version": evidence["version"],
                        "digest": evidence["digest"],
                    }, "events": events,
                }

    condition = case.get("condition")
    if condition == "C":
        events.append({"type": "lookup", "channel": "retrieval", "action": "skipped", "reason": "condition_C_no_index_ablation"})
    elif condition != "B":
        events.append({"type": "lookup", "channel": "retrieval", "action": "skipped", "reason": "condition_not_B"})
    else:
        raw_index = case.get("index")
        if raw_index is None:
            raw_index = []
        if not isinstance(raw_index, list):
            events.append({"type": "invalid_input", "field": "index", "reason": "index_not_array"})
            raw_index = []
        matched = False
        for i, descriptor in enumerate(raw_index):
            indexed, problem = _identity_from_descriptor(descriptor)
            if problem:
                events.append({"type": "index_rejected", "position": i, "reason": problem})
            elif trusted is not None and indexed == trusted:
                matched = True
                events.append({"type": "index_match", "position": i, "identity": indexed})
        if not matched:
            events.append({"type": "lookup", "channel": "retrieval", "action": "skipped", "reason": "no_exact_trusted_index_match"})
        else:
            retrieval = case.get("retrieval")
            if not isinstance(retrieval, dict):
                events.append({"type": "lookup", "channel": "retrieval", "action": "skipped", "reason": "retrieval_descriptor_invalid"})
            else:
                state = retrieval.get("state")
                if state == "missing":
                    events.append({"type": "lookup", "channel": "retrieval", "action": "attempted", "result": "missing"})
                elif state == "failing":
                    events.append({"type": "lookup", "channel": "retrieval", "action": "attempted", "result": "failing"})
                elif state == "available":
                    raw_records = retrieval.get("records", [])
                    records = _records(raw_records, "retrieval.records", events)
                    events.append({"type": "lookup", "channel": "retrieval", "action": "attempted", "result": "available", "count": len(records)})
                    for position, record in enumerate(records):
                        reason, evidence = _record_problem(record, trusted, request, as_of)
                        if reason:
                            events.append({"type": "record_rejected", "channel": "retrieval", "position": position, "reason": reason})
                            continue
                        assert evidence is not None
                        events.append({
                            "type": "record_accepted", "channel": "retrieval", "position": position,
                            "source_id": evidence["source_id"], "version": evidence["version"],
                            "digest": evidence["digest"],
                        })
                        return {
                            "id": case_id, "status": "current", "value": evidence["value"],
                            "source_id": evidence["source_id"], "version": evidence["version"],
                            "complete": True, "evidence": {
                                "channel": "retrieval", "position": position,
                                "source_id": evidence["source_id"], "version": evidence["version"],
                                "digest": evidence["digest"],
                            }, "events": events,
                        }
                else:
                    events.append({"type": "invalid_input", "field": "retrieval.state", "reason": "unknown_retrieval_state"})

    return {
        "id": case_id, "status": "unresolved", "value": None,
        "source_id": None, "version": None, "complete": False,
        "evidence": None, "events": events,
    }


def _case_resolver_view(case: dict[str, Any]) -> dict[str, Any]:
    """Allowlist resolver fields so expected data cannot influence resolution."""
    return {key: case.get(key) for key in (
        "id", "mechanism", "condition", "request", "authoritative",
        "memory", "local_sources", "index", "retrieval",
    )}


def _evidence_supported(case: dict[str, Any], observation: dict[str, Any]) -> bool:
    """Independently recheck a current claim against accessible case evidence."""
    if observation.get("status") != "current" or observation.get("complete") is not True:
        return False
    # Reconstruct the accessible input inventory without using expected or the
    # resolver's event trail.  This is the explicit calibration denominator.
    view = _case_resolver_view(case)
    request, as_of, request_error = _request_view(view.get("request"))
    trusted, trusted_error = _trusted_identity(view.get("authoritative"))
    if request_error or trusted_error:
        return False
    inventories: list[Any] = []
    for name in ("memory", "local_sources"):
        value = view.get(name)
        if isinstance(value, list):
            inventories.extend(value)
    if view.get("condition") == "B":
        index = view.get("index")
        has_match = False
        if isinstance(index, list):
            for descriptor in index:
                ident, error = _identity_from_descriptor(descriptor)
                if not error and ident == trusted:
                    has_match = True
                    break
        retrieval = view.get("retrieval")
        if has_match and isinstance(retrieval, dict) and retrieval.get("state") == "available":
            records = retrieval.get("records", [])
            if isinstance(records, list):
                inventories.extend(records)
    for record in inventories:
        reason, evidence = _record_problem(record, trusted, request, as_of)
        if reason or evidence is None:
            continue
        if (observation.get("source_id") == evidence["source_id"]
                and observation.get("version") == evidence["version"]
                and observation.get("value") == evidence["value"]):
            return True
    return False


def evaluate(cases: list[Any]) -> tuple[list[dict[str, Any]], dict[str, Any], int]:
    outputs: list[dict[str, Any]] = []
    mismatches: list[dict[str, Any]] = []
    invalid_expected = 0
    expected_complete_count = 0
    observed_complete_count = 0
    false_current_claims = 0
    current_claims = 0
    supported_current_claims = 0
    for i, raw_case in enumerate(cases):
        if not isinstance(raw_case, dict):
            case = {}
            observed = resolve({})
            expected: Any = None
            invalid_expected += 1
            mismatch = {"case_index": i, "id": None, "reason": "case_not_object"}
            mismatches.append(mismatch)
            outputs.append({"observation": observed, "comparison": mismatch})
            continue
        observed = resolve(_case_resolver_view(raw_case))
        expected = raw_case.get("expected")
        comparison: dict[str, Any]
        if not isinstance(expected, dict):
            invalid_expected += 1
            comparison = {"case_index": i, "id": observed["id"], "reason": "expected_not_object"}
            mismatches.append(comparison)
        else:
            fields = ("status", "value", "source_id", "version", "complete")
            differences = {
                field: {"observed": observed.get(field), "expected": expected.get(field)}
                for field in fields if observed.get(field) != expected.get(field)
            }
            comparison = {"case_index": i, "id": observed["id"], "matched": not differences, "differences": differences}
            if differences:
                mismatches.append(comparison)
            if expected.get("complete") is True:
                expected_complete_count += 1
        if observed.get("complete") is True:
            observed_complete_count += 1
        if observed.get("status") == "current":
            current_claims += 1
            if _evidence_supported(raw_case, observed):
                supported_current_claims += 1
            else:
                false_current_claims += 1
        outputs.append({"observation": observed, "comparison": comparison})

    total = len(cases)
    matched = total - len(mismatches)
    summary = {
        "completeness": {
            "case_count": total,
            "expected_complete_count": expected_complete_count,
            "observed_complete_count": observed_complete_count,
            "observed_unresolved_count": total - observed_complete_count,
            "expected_observed_complete_agreement_count": sum(
                1 for item in outputs
                if isinstance(item.get("comparison"), dict)
                and item["comparison"].get("matched") is True
                and item["observation"].get("complete") is True
            ),
        },
        "calibration": {
            "definition": "A current/complete claim is supported only when an independently rechecked, accessible, integrity-valid record matches the trusted identity, request key/scope, date window, and emitted value. This is a safety support rate, not probabilistic calibration or expected-output accuracy.",
            "current_claim_count": current_claims,
            "evidence_supported_current_claim_count": supported_current_claims,
            "unsupported_current_claim_count": false_current_claims,
            "supported_current_claim_rate": (supported_current_claims / current_claims if current_claims else None),
        },
        "oracle_comparison": {
            "matched_case_count": matched,
            "mismatch_count": len(mismatches),
            "invalid_expected_count": invalid_expected,
        },
    }
    return outputs, {"summary": summary, "mismatches": mismatches}, int(bool(mismatches))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", help="path to a schema_version=1 fixture JSON file")
    args = parser.parse_args(argv)
    def reject_nonfinite(token: str) -> None:
        raise ValueError(f"non-finite JSON number is forbidden: {token}")
    try:
        with Path(args.cases).open("r", encoding="utf-8") as handle:
            fixture = json.load(handle, parse_constant=reject_nonfinite)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, RecursionError) as exc:
        print(json.dumps({"error": "fixture_read_failed", "detail": str(exc)}, ensure_ascii=False))
        return 2
    if not isinstance(fixture, dict) or fixture.get("schema_version") != 1 or not isinstance(fixture.get("cases"), list):
        print(json.dumps({"error": "invalid_fixture_envelope", "required": {"schema_version": 1, "cases": "array"}}))
        return 2
    observations, evaluation, status = evaluate(fixture["cases"])
    result = {
        "schema_version": 1,
        "observations": observations,
        **evaluation,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, allow_nan=False))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
