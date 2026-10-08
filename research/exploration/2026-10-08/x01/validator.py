"""Small offline validator for the T-GOV-013 X01 handoff envelope.

This module validates JSON-like Python values. It is not a security boundary.
"""

import hashlib
import re
from urllib.parse import urlsplit


_HASH = re.compile(r"[0-9a-f]{64}\Z")
_URI_SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")
_CLAIM_STATUSES = {"supplied", "verified", "assumption", "unresolved"}


def render_copy(title, attendance):
    """Render the only supported marketing sentence deterministically."""
    return f"{title} welcomes {attendance} adults."


def _mapping(value):
    return isinstance(value, dict)


def _string(value):
    return isinstance(value, str)


def _integer(value):
    # bool subclasses int; accepting True as one seat is a schema error.
    return isinstance(value, int) and not isinstance(value, bool)


def _positive(value):
    return _integer(value) and value > 0


def _nonnegative(value):
    return _integer(value) and value >= 0


def _logical_path(path):
    if not _string(path) or not path:
        return False
    if "\\" in path or path.startswith("/"):
        return False
    parts = path.split("/")
    return all(part not in ("", ".", "..") and _URI_SCHEME.match(part) is None
               for part in parts)


def _http_url_shape(value):
    """Check basic HTTP(S) URL syntax without resolving or fetching it."""
    if not _string(value) or not value:
        return False
    if any(ord(char) <= 32 or ord(char) == 127 for char in value):
        return False
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        # Accessing .port makes urllib validate malformed and out-of-range ports.
        parsed.port
    except ValueError:
        return False
    return parsed.scheme.lower() in ("http", "https") and bool(parsed.netloc) and bool(hostname)


def _add(errors, condition, message):
    if not condition:
        errors.append(message)


def validate(payload, assignment, inputs):
    """Return deterministic validation errors without mutating arguments.

    The assignment is the coordinator-supplied manifest. ``payload`` and
    ``inputs`` are candidate-controlled. Unexpected shapes are reported as
    errors; this function is designed to tolerate malformed JSON-like values.
    """
    errors = []
    if not _mapping(assignment):
        return ["assignment: expected object"]
    if not _mapping(payload):
        return ["payload: expected object"]
    if not _mapping(inputs):
        return ["inputs: expected object mapping paths to bytes"]

    # Validate the trusted manifest sufficiently before using it.
    aid = assignment.get("assignment_id")
    session = assignment.get("writer_session")
    title = assignment.get("title")
    attendance = assignment.get("attendance")
    _add(errors, _string(aid) and bool(aid), "assignment.assignment_id: expected nonempty string")
    _add(errors, _string(session) and bool(session), "assignment.writer_session: expected nonempty string")
    _add(errors, _string(title) and bool(title), "assignment.title: expected nonempty string")
    _add(errors, _positive(attendance), "assignment.attendance: expected positive integer")

    raw_deps = assignment.get("dependencies")
    manifest = {}
    if not isinstance(raw_deps, list):
        errors.append("assignment.dependencies: expected list")
    else:
        for i, dep in enumerate(raw_deps):
            if not _mapping(dep):
                errors.append(f"assignment.dependencies[{i}]: expected object")
                continue
            path, version, digest = dep.get("path"), dep.get("version"), dep.get("sha256")
            valid = (_logical_path(path) and _positive(version) and _string(digest)
                     and _HASH.fullmatch(digest) is not None)
            if not valid:
                errors.append(f"assignment.dependencies[{i}]: invalid path, version, or lowercase SHA256")
                continue
            if path in manifest:
                errors.append(f"assignment.dependencies[{i}]: duplicate path {path}")
                continue
            manifest[path] = (version, digest)

    resources = assignment.get("resources")
    resource_caps = {}
    if not _mapping(resources):
        errors.append("assignment.resources: expected object")
    else:
        for rid, resource in resources.items():
            if not _string(rid) or not rid or not _mapping(resource):
                errors.append("assignment.resources: each entry needs a nonempty string id and object")
                continue
            units = resource.get("inventory_units")
            seats = resource.get("seats_per_unit")
            if not _nonnegative(units) or not _nonnegative(seats):
                errors.append(f"assignment.resources.{rid}: inventory_units and seats_per_unit must be nonnegative integers")
                continue
            resource_caps[rid] = units * seats

    handoff = payload.get("handoff")
    if not _mapping(handoff):
        errors.append("handoff: expected object")
        handoff = {}
    _add(errors, _string(aid) and handoff.get("assignment_id") == aid,
         "handoff.assignment_id: does not match assignment")
    _add(errors, _string(session) and handoff.get("writer_session") == session,
         "handoff.writer_session: does not match assignment")
    _add(errors, handoff.get("status") == "ready_for_review",
         "handoff.status: expected ready_for_review")

    receipts = handoff.get("dependencies")
    received = {}
    if not isinstance(receipts, list):
        errors.append("handoff.dependencies: expected list")
    else:
        for i, receipt in enumerate(receipts):
            if not _mapping(receipt):
                errors.append(f"handoff.dependencies[{i}]: expected object")
                continue
            path = receipt.get("path")
            version = receipt.get("version")
            digest = receipt.get("sha256")
            if not _logical_path(path):
                errors.append(f"handoff.dependencies[{i}].path: invalid logical path")
                continue
            if path in received:
                errors.append(f"handoff.dependencies[{i}]: duplicate path {path}")
                continue
            received[path] = (version, digest)
    if set(received) != set(manifest):
        errors.append("handoff.dependencies: paths do not exactly match assignment")
    for path, (expected_version, expected_hash) in manifest.items():
        if path not in received:
            continue
        version, digest = received[path]
        if not _positive(version) or version != expected_version:
            errors.append(f"handoff.dependencies[{path}].version: does not match assignment")
        if not _string(digest) or _HASH.fullmatch(digest) is None or digest != expected_hash:
            errors.append(f"handoff.dependencies[{path}].sha256: does not match assignment")
        actual = inputs.get(path)
        if not isinstance(actual, bytes):
            errors.append(f"inputs[{path}]: expected bytes")
        elif hashlib.sha256(actual).hexdigest() != expected_hash:
            errors.append(f"inputs[{path}]: content hash does not match assignment")

    # Assignment paths must be present as actual byte strings. Inputs may have
    # additional keys; those keys are intentionally ignored.
    for path in manifest:
        if path not in inputs:
            errors.append(f"inputs[{path}]: missing dependency")

    for key in ("attendance", "title"):
        value = payload.get(key)
        expected = assignment.get(key)
        if key == "attendance":
            ok = _positive(value) and _positive(expected) and value == expected
        else:
            ok = _string(value) and _string(expected) and value == expected
        _add(errors, ok, f"{key}: does not match assignment")

    marketing = payload.get("marketing")
    if not _mapping(marketing):
        errors.append("marketing: expected object")
    else:
        _add(errors, _string(title) and _string(marketing.get("title")) and marketing.get("title") == title,
             "marketing.title: does not match assignment")
        _add(errors, _positive(attendance) and _positive(marketing.get("attendance"))
             and marketing.get("attendance") == attendance,
             "marketing.attendance: does not match assignment")
        copy = marketing.get("copy")
        expected_copy = render_copy(title, attendance) if _string(title) and _positive(attendance) else None
        _add(errors, _string(copy) and expected_copy is not None and copy == expected_copy,
             "marketing.copy: does not match deterministic renderer")

    states = payload.get("states")
    if not isinstance(states, list):
        errors.append("states: expected nonempty list")
        states = []
    elif not states:
        errors.append("states: expected nonempty list")

    parsed_states = []
    ids = set()
    for i, state in enumerate(states):
        prefix = f"states[{i}]"
        if not _mapping(state):
            errors.append(f"{prefix}: expected object")
            continue
        sid = state.get("id")
        if not _string(sid) or not sid:
            errors.append(f"{prefix}.id: expected nonempty string")
        elif sid in ids:
            errors.append(f"{prefix}.id: duplicate id")
        else:
            ids.add(sid)
        start, end = state.get("start"), state.get("end")
        valid_interval = _nonnegative(start) and _positive(end) and start < end
        if not valid_interval:
            errors.append(f"{prefix}: start/end must define a nonempty half-open interval")
        attendees = state.get("attendees")
        if not _nonnegative(attendees):
            errors.append(f"{prefix}.attendees: expected nonnegative integer")
        elif _positive(attendance) and attendees > attendance:
            errors.append(f"{prefix}.attendees: exceeds expected audience")
        seating = state.get("seating")
        resource_id = state.get("chair_resource")
        capacity = None
        if seating == "standing":
            if resource_id is not None:
                errors.append(f"{prefix}.chair_resource: must be null for standing")
        elif seating == "seated":
            if not _string(resource_id) or not resource_id:
                errors.append(f"{prefix}.chair_resource: required for seated state")
            elif resource_id not in resource_caps:
                errors.append(f"{prefix}.chair_resource: unknown resource")
            else:
                capacity = resource_caps[resource_id]
        else:
            errors.append(f"{prefix}.seating: expected seated or standing")
        if valid_interval and _nonnegative(attendees):
            parsed_states.append((start, end, attendees, capacity, prefix, resource_id if seating == "seated" else None))

    # Sweep all distinct boundaries and evaluate half-open occupancy per span.
    boundaries = sorted({point for row in parsed_states for point in row[:2]})
    for left, right in zip(boundaries, boundaries[1:]):
        active = [row for row in parsed_states if row[0] < right and row[1] > left]
        if not active:
            continue
        total = sum(row[2] for row in active)
        if _positive(attendance) and total > attendance:
            errors.append(f"states: simultaneous attendance exceeds expected audience during [{left},{right})")
        by_resource = {}
        for row in active:
            rid = row[5]
            if rid is not None and row[3] is not None:
                by_resource[rid] = by_resource.get(rid, 0) + row[2]
        for rid, used in by_resource.items():
            if used > resource_caps[rid]:
                errors.append(f"states: resource {rid} capacity exceeded during [{left},{right})")

    claims = payload.get("claims")
    if not isinstance(claims, list):
        errors.append("claims: expected list")
    else:
        claim_ids = set()
        for i, claim in enumerate(claims):
            prefix = f"claims[{i}]"
            if not _mapping(claim):
                errors.append(f"{prefix}: expected object")
                continue
            cid = claim.get("id")
            if not _string(cid) or not cid:
                errors.append(f"{prefix}.id: expected nonempty string")
            elif cid in claim_ids:
                errors.append(f"{prefix}.id: duplicate id")
            else:
                claim_ids.add(cid)
            status = claim.get("status")
            if not _string(status) or status not in _CLAIM_STATUSES:
                errors.append(f"{prefix}.status: expected supplied, verified, assumption, or unresolved")
                continue
            if not _string(claim.get("text")) or not claim.get("text"):
                errors.append(f"{prefix}.text: expected nonempty string")
            source = claim.get("source")
            if status == "supplied":
                if not _string(source) or source not in manifest:
                    errors.append(f"{prefix}.source: supplied claim requires a known dependency path")
            elif status == "verified":
                if not _http_url_shape(source):
                    errors.append(f"{prefix}.source: verified claim requires a shaped HTTP(S) URL with a hostname")
            elif status in ("assumption", "unresolved"):
                if not _string(source) or not source.strip():
                    errors.append(f"{prefix}.source: assumption or unresolved claim must remain labeled")

    return errors
