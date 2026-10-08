#!/usr/bin/env python3
"""Small local, grant-checked source retrieval broker for EXP-X04-20261008-04."""

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path


_HEX = re.compile(r"[0-9a-f]{64}\Z")
_REQUIRED_REQUEST = ("request_id", "grant_id", "assignment", "scope", "path", "caller_label")


class InvalidConfiguration(ValueError):
    """Trusted grant configuration is malformed; no source may be read."""


def _valid_path(value):
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        return False
    if value.startswith("/"):
        return False
    return all(part not in ("", ".", "..") for part in value.split("/"))


def _nonempty_string(value):
    return isinstance(value, str) and bool(value)


def _load_grants(document):
    if (not isinstance(document, dict) or set(document) != {"schema_version", "grants"}
            or type(document.get("schema_version")) is not int or document.get("schema_version") != 1):
        raise InvalidConfiguration("invalid_config")
    entries = document.get("grants")
    if not isinstance(entries, list):
        raise InvalidConfiguration("invalid_config")
    result = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise InvalidConfiguration("invalid_config")
        if set(entry) != {"grant_id", "path", "assignment", "scope", "sha256", "mode"}:
            raise InvalidConfiguration("invalid_config")
        gid, path = entry.get("grant_id"), entry.get("path")
        assignment, scope = entry.get("assignment"), entry.get("scope")
        digest, mode = entry.get("sha256"), entry.get("mode")
        if (not _nonempty_string(gid) or gid in result or not _valid_path(path)
                or not _nonempty_string(assignment) or not _nonempty_string(scope)
                or not isinstance(digest, str) or not _HEX.fullmatch(digest)
                or mode not in ("read", "failing")):
            raise InvalidConfiguration("invalid_config")
        result[gid] = dict(entry)
    return result


class Broker:
    """Serve bytes only after exact grant checks and raw-byte hash verification."""

    def __init__(self, root, grants):
        self.root = os.fspath(root)
        self._grants = _load_grants(grants)
        self.events = []

    @staticmethod
    def _open_regular(root, relpath):
        """Open beneath root by walking no-follow directory descriptors."""
        nofollow = getattr(os, "O_NOFOLLOW", None)
        directory = getattr(os, "O_DIRECTORY", None)
        nonblock = getattr(os, "O_NONBLOCK", None)
        if (nofollow is None or directory is None or nonblock is None
                or os.open not in getattr(os, "supports_dir_fd", set())):
            raise OSError("safe descriptor opens unavailable")
        flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
        rootfd = os.open(root, flags | directory | nofollow)
        current = rootfd
        try:
            parts = relpath.split("/")
            for component in parts[:-1]:
                nxt = os.open(component, flags | directory | nofollow, dir_fd=current)
                if current != rootfd:
                    os.close(current)
                current = nxt
            fd = os.open(parts[-1], flags | nofollow | nonblock, dir_fd=current)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    raise OSError("source is not a regular file")
                return fd
            except BaseException:
                os.close(fd)
                raise
        finally:
            if current != rootfd:
                os.close(current)
            os.close(rootfd)

    def retrieve(self, request):
        seq = len(self.events) + 1
        vals = {key: None for key in _REQUIRED_REQUEST}
        if isinstance(request, dict):
            vals.update({key: request.get(key) for key in _REQUIRED_REQUEST})
        status, reason, payload = "invalid", "invalid_request", None
        observed_hash, observed_count, served_count = None, 0, 0

        required_nonempty = ("request_id", "grant_id", "assignment", "scope", "caller_label")
        if (not isinstance(request, dict)
                or any(not isinstance(vals[k], str) for k in _REQUIRED_REQUEST)
                or any(not vals[k] for k in required_nonempty)):
            pass
        else:
            status = "denied"
            if not _valid_path(vals["path"]):
                reason = "invalid_path"
            else:
                grant = self._grants.get(vals["grant_id"])
                if grant is None:
                    reason = "grant_not_found"
                elif vals["path"] != grant["path"]:
                    reason = "path_not_granted"
                elif vals["assignment"] != grant["assignment"]:
                    reason = "assignment_mismatch"
                elif vals["scope"] != grant["scope"]:
                    reason = "scope_mismatch"
                elif grant["mode"] == "failing":
                    status, reason = "failing", "injected_failure"
                else:
                    try:
                        fd = self._open_regular(self.root, vals["path"])
                    except FileNotFoundError:
                        status, reason = "missing", "not_found"
                    except OSError:
                        status, reason = "denied", "unsafe_file"
                    else:
                        try:
                            chunks = []
                            while True:
                                chunk = os.read(fd, 1024 * 1024)
                                if not chunk:
                                    break
                                chunks.append(chunk)
                            data = b"".join(chunks)
                        except OSError:
                            status, reason = "failing", "io_failure"
                        else:
                            observed_count = len(data)
                            observed_hash = hashlib.sha256(data).hexdigest()
                            if observed_hash != grant["sha256"]:
                                status, reason = "changed", "content_mismatch"
                            else:
                                status, reason = "served", "verified_bytes"
                                payload = base64.b64encode(data).decode("ascii")
                                served_count = len(data)
                        finally:
                            os.close(fd)

        event = {
            "seq": seq,
            "request_id": vals["request_id"] if isinstance(vals["request_id"], str) else None,
            "caller_label": vals["caller_label"] if isinstance(vals["caller_label"], str) else None,
            "caller_authenticated": False,
            "requested_path": vals["path"] if isinstance(vals["path"], str) else None,
            "grant_id": vals["grant_id"] if isinstance(vals["grant_id"], str) else None,
            "assignment": vals["assignment"] if isinstance(vals["assignment"], str) else None,
            "scope": vals["scope"] if isinstance(vals["scope"], str) else None,
            "status": status,
            "reason": reason,
            "observed_sha256": observed_hash,
            "observed_byte_count": observed_count,
            "served_byte_count": served_count,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "time_source": "process_wall_clock",
        }
        self.events.append(event)
        return {"status": status, "reason": reason, "payload_b64": payload, "event": event}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--grants", required=True)
    parser.add_argument("--cases", required=True)
    args = parser.parse_args(argv)
    try:
        with open(args.grants, "r", encoding="utf-8") as stream:
            grant_doc = json.load(stream)
        with open(args.cases, "r", encoding="utf-8") as stream:
            case_doc = json.load(stream)
        broker = Broker(args.root, grant_doc)
        if (not isinstance(case_doc, dict) or set(case_doc) != {"schema_version", "cases"}
                or type(case_doc.get("schema_version")) is not int or case_doc.get("schema_version") != 1
                or not isinstance(case_doc.get("cases"), list)):
            raise ValueError("invalid_cases")
        results = []
        mismatches = 0
        for case in case_doc["cases"]:
            if not isinstance(case, dict) or not isinstance(case.get("expected"), dict):
                raise ValueError("invalid_cases")
            actual = broker.retrieve(case.get("request"))
            expected = case["expected"]
            matched = actual["status"] == expected.get("status") and actual["reason"] == expected.get("reason")
            mismatches += not matched
            results.append({"id": case.get("id"), "actual": actual, "expected": {"status": expected.get("status"), "reason": expected.get("reason")}, "matched": matched})
        print(json.dumps({"results": results, "events": broker.events, "comparison": {"case_count": len(results), "mismatch_count": mismatches}}, ensure_ascii=False))
        return 1 if mismatches else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "invalid_config" if isinstance(exc, InvalidConfiguration) else str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
