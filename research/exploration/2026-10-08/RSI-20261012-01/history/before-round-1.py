#!/usr/bin/env python3
"""Offline, cooperative evidence checks. Never edit or promote repository code."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

VERSION = "1.0"
MAX_BYTES = 2 * 1024 * 1024
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class EvidenceError(ValueError):
    pass


class BudgetStop(EvidenceError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def integer(value):
    return type(value) is int and value >= 0


def object_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise EvidenceError(f"duplicate JSON key: {key}")
        obj[key] = value
    return obj


def decode(data):
    try:
        return json.loads(data, object_pairs_hook=object_pairs,
                          parse_constant=lambda x: (_ for _ in ()).throw(
                              EvidenceError(f"nonfinite JSON number: {x}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"invalid JSON: {exc}") from exc


def safe_path(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or "\\" in relative
            or "\0" in relative or ":" in relative
            or any(part in ("", ".", "..") for part in relative.split("/"))):
        raise EvidenceError("unsafe_path")
    root = root.resolve(strict=True)
    cursor = root
    for part in relative.split("/"):
        cursor = cursor / part
        try:
            mode = cursor.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise EvidenceError("symlink")
    return cursor


def read_file(path: Path) -> bytes:
    """Reject FIFO/device/directory before opening; cooperative, no race isolation."""
    mode = path.lstat().st_mode
    if stat.S_ISLNK(mode):
        raise EvidenceError("symlink")
    if not stat.S_ISREG(mode):
        raise EvidenceError("nonregular")
    if path.stat().st_size > MAX_BYTES:
        raise EvidenceError("oversize")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise EvidenceError("nonregular")
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise EvidenceError("oversize")
    return data


def bound(root, reference):
    if (not isinstance(reference, dict) or set(reference) != {"path", "sha256"}
            or not isinstance(reference["sha256"], str)
            or not DIGEST.fullmatch(reference["sha256"])):
        raise EvidenceError("invalid bound reference")
    try:
        data = read_file(safe_path(root, reference["path"]))
    except (OSError, ValueError) as exc:
        raise EvidenceError(f"cannot read bound reference: {exc}") from exc
    if sha(data) != reference["sha256"]:
        raise EvidenceError("bound bytes changed")
    return decode(data)


def audit(root: Path, registry: dict, method="bound_v1") -> dict:
    if (not isinstance(registry, dict) or registry.get("schema_version") != 1
            or not isinstance(registry.get("artifacts"), list)
            or not registry["artifacts"]):
        raise EvidenceError("registry must contain a nonempty artifact list")
    if method not in ("bound_v1", "existence_v0"):
        raise EvidenceError("unknown audit method")
    seen, rows = set(), []
    for entry in registry["artifacts"]:
        if (not isinstance(entry, dict) or not isinstance(entry.get("id"), str)
                or not entry["id"] or not isinstance(entry.get("path"), str)):
            raise EvidenceError("artifact id/path required")
        outcome, observed = "ok", None
        if method == "bound_v1" and entry["id"] in seen:
            outcome = "duplicate_id"
        seen.add(entry["id"])
        digest = entry.get("sha256")
        if outcome == "ok" and method == "bound_v1":
            if digest is None:
                outcome = "unbound"
            elif not isinstance(digest, str) or not DIGEST.fullmatch(digest):
                outcome = "invalid_digest"
        if outcome == "ok":
            try:
                if method == "existence_v0":
                    # Synthetic comparator: same lexical scope, only existence.
                    relative = entry["path"]
                    if (not relative or "\\" in relative or ":" in relative
                            or "\0" in relative
                            or any(x in ("", ".", "..") for x in relative.split("/"))):
                        raise EvidenceError("unsafe_path")
                    if not (root / relative).exists():
                        outcome = "missing"
                else:
                    observed = sha(read_file(safe_path(root, entry["path"])))
                    if observed != digest:
                        outcome = "changed"
            except FileNotFoundError:
                outcome = "missing"
            except EvidenceError as exc:
                outcome = str(exc)
            except OSError:
                outcome = "unreadable"
        rows.append({"id": entry["id"], "path": entry["path"], "outcome": outcome,
                     "expected_sha256": digest, "observed_sha256": observed})
    issues = [row for row in rows if row["outcome"] != "ok"]
    return {"schema_version": 1, "method": method, "rows": rows,
            "issue_count": len(issues), "all_bound_bytes_match": not issues,
            "limitations": "byte identity only; no authority, truth or reading certification"}


def suite_data(root, reference):
    suite = bound(root, reference)
    if (not isinstance(suite, dict) or suite.get("schema_version") != 1
            or not isinstance(suite.get("audit_cases"), list) or not suite["audit_cases"]):
        raise EvidenceError("invalid suite")
    ids = [c.get("id") for c in suite["audit_cases"] if isinstance(c, dict)]
    if (len(ids) != len(suite["audit_cases"]) or any(not isinstance(x, str) or not x for x in ids)
            or len(set(ids)) != len(ids)):
        raise EvidenceError("invalid/duplicate case IDs")
    return suite


def run_suite(suite: dict, suite_sha: str, method: str) -> dict:
    observations = []
    for case in suite["audit_cases"]:
        with tempfile.TemporaryDirectory(prefix="rsi-fixture-") as tmp:
            root = Path(tmp)
            for relative, spec in case["files"].items():
                path = safe_path(root, relative)
                path.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(spec, str):
                    path.write_text(spec, encoding="utf-8")
                elif spec["kind"] == "directory":
                    path.mkdir()
                elif spec["kind"] == "symlink":
                    target = safe_path(root, spec["target"])
                    path.symlink_to(target)
                else:
                    raise EvidenceError("invalid fixture kind")
            report = audit(root, case["registry"], method)
            failures = [r["outcome"] for r in report["rows"] if r["outcome"] != "ok"]
            outcome = failures[0] if failures else "ok"
            observations.append({"id": case["id"], "outcome": outcome})
    return {"schema_version": 1, "suite_sha256": suite_sha, "method": method,
            "producer_sha256": sha(read_file(Path(__file__))), "observations": observations,
            "provenance": "local synthetic execution; labels and digests are not authenticated identity"}


def scores(report, suite):
    if (not isinstance(report, dict) or report.get("schema_version") != 1
            or not isinstance(report.get("method"), str) or not report["method"]
            or not isinstance(report.get("producer_sha256"), str)
            or not DIGEST.fullmatch(report["producer_sha256"])
            or not isinstance(report.get("observations"), list)):
        raise EvidenceError("invalid report schema")
    rows = report["observations"]
    if any(not isinstance(r, dict) or set(r) != {"id", "outcome"}
           or not isinstance(r["id"], str) or not isinstance(r["outcome"], str) for r in rows):
        raise EvidenceError("invalid observation schema")
    values = {r["id"]: r["outcome"] for r in rows}
    expected = {c["id"]: c["expected"] for c in suite["audit_cases"]}
    if len(values) != len(rows) or set(values) != set(expected):
        raise EvidenceError("missing, extra or duplicated observation")
    return {key: values[key] == value for key, value in expected.items()}


def time_value(value):
    if not isinstance(value, str):
        raise EvidenceError("timestamp must be a string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError("invalid timestamp") from exc
    if parsed.tzinfo is None:
        raise EvidenceError("timezone required")
    return parsed.astimezone(timezone.utc)


def validate_cycle(root, cycle, seen=None):
    if not isinstance(cycle, dict) or cycle.get("schema_version") != 1:
        raise EvidenceError("invalid cycle")
    for field in ("id", "lineage", "objective", "hypothesis", "stop_rule", "implementer"):
        if not isinstance(cycle.get(field), str) or not cycle[field].strip():
            raise EvidenceError(f"{field} required")
    budget = cycle.get("budget")
    if (not isinstance(budget, dict) or set(budget) != {"max_cycles", "max_repairs", "deadline"}
            or not integer(budget["max_cycles"]) or not 1 <= budget["max_cycles"] <= 20
            or not integer(budget["max_repairs"]) or not 0 <= budget["max_repairs"] <= 2
            or not integer(cycle.get("iteration")) or cycle["iteration"] < 1
            or not integer(cycle.get("repairs_used"))):
        raise EvidenceError("invalid bounds")
    time_value(budget["deadline"])
    freeze = bound(root, cycle.get("freeze"))
    if budget != freeze.get("budget"):
        raise EvidenceError("root frozen budget changed")
    current_suite = suite_data(root, cycle.get("suite"))
    # Implementation is source bytes, not JSON. Bind it without interpreting it.
    implementation = cycle.get("implementation")
    if (not isinstance(implementation, dict) or set(implementation) != {"path", "sha256"}
            or not isinstance(implementation["sha256"], str)
            or not DIGEST.fullmatch(implementation["sha256"])
            or sha(read_file(safe_path(root, implementation["path"]))) != implementation["sha256"]):
        raise EvidenceError("implementation bytes changed or unbound")
    if (cycle["iteration"] > budget["max_cycles"]
            or cycle["repairs_used"] > budget["max_repairs"]):
        raise BudgetStop("cycle or repair budget exceeded")
    seen = set() if seen is None else seen
    if cycle["id"] in seen or len(seen) >= 20:
        raise EvidenceError("cyclic or excessive ancestry")
    seen.add(cycle["id"])
    if cycle["iteration"] == 1:
        if cycle.get("parent") is not None or cycle["suite"]["sha256"] != freeze["suite_sha256"]:
            raise EvidenceError("invalid root cycle/freeze")
    else:
        parent = bound(root, cycle.get("parent"))
        validate_cycle(root, parent, seen)
        if (cycle["lineage"] != parent["lineage"] or budget != parent["budget"]
                or cycle["freeze"] != parent["freeze"]
                or cycle["iteration"] != parent["iteration"] + 1
                or cycle["repairs_used"] < parent["repairs_used"]):
            raise EvidenceError("child resets lineage, suite or budget")
        review = bound(root, cycle.get("parent_review"))
        check_review(review, parent)
        old_suite = suite_data(root, parent["suite"])
        existing = {case["id"]: case for case in current_suite["audit_cases"]}
        if any(existing.get(case["id"]) != case for case in old_suite["audit_cases"]):
            raise EvidenceError("child removes or changes a frozen regression case")
        prior = bound(root, parent["candidate"])
        baseline = bound(root, cycle["baseline"])
        if (baseline.get("method"), baseline.get("producer_sha256")) != (
                prior.get("method"), prior.get("producer_sha256")):
            raise EvidenceError("child baseline is not previous candidate method")


def assess(root, cycle, now=None):
    now = datetime.now(timezone.utc) if now is None else now
    if now.tzinfo is None:
        raise EvidenceError("evaluation time must have a timezone")
    try:
        validate_cycle(root, cycle)
        budget = cycle["budget"]
        if (now >= time_value(budget["deadline"]) or cycle["iteration"] > budget["max_cycles"]
                or cycle["repairs_used"] > budget["max_repairs"]):
            return {"status": "budget_exhausted", "next_action": "checkpoint; no automatic extension"}
        suite = suite_data(root, cycle["suite"])
        baseline, candidate = bound(root, cycle["baseline"]), bound(root, cycle["candidate"])
        if any(report.get("suite_sha256") != cycle["suite"]["sha256"]
               for report in (baseline, candidate)):
            return {"status": "incomparable", "next_action": "preserve results; recover matching suite"}
        before, after = scores(baseline, suite), scores(candidate, suite)
        if candidate["producer_sha256"] != cycle["implementation"]["sha256"]:
            raise EvidenceError("candidate method source is not bound implementation")
        gains = [key for key in before if not before[key] and after[key]]
        regressions = [key for key in before if before[key] and not after[key]]
        remaining = [key for key in after if not after[key]]
        status = ("regression" if regressions else "candidate_fails" if remaining else
                  "review_pending" if gains else "no_gain")
        return {"status": status, "cycle_id": cycle["id"], "suite_sha256": cycle["suite"]["sha256"],
                "baseline_matches": sum(before.values()), "candidate_matches": sum(after.values()),
                "case_count": len(before), "gains": gains, "regressions": regressions,
                "remaining_failures": remaining, "candidate": cycle["candidate"],
                "next_action": "independent fixed-candidate review" if status == "review_pending"
                    else "checkpoint; use observed failures/stop rule, no automatic iteration",
                "accepted": False, "reviewer_identity": "unverified",
                "limitations": "finite synthetic cases; report provenance must be independently reproduced"}
    except BudgetStop as exc:
        return {"status": "budget_exhausted", "reason": str(exc), "accepted": False,
                "next_action": "checkpoint; no automatic extension"}
    except (EvidenceError, KeyError, TypeError, OSError) as exc:
        return {"status": "invalid_evidence", "reason": str(exc),
                "accepted": False, "next_action": "preserve error; recover exact evidence"}


def check_review(review, cycle):
    if (not isinstance(review, dict) or review.get("kind") != "independent_review"
            or review.get("verdict") != "pass" or not isinstance(review.get("reviewer"), str)
            or not review["reviewer"].strip() or not isinstance(review.get("implementer"), str)
            or not review["implementer"].strip() or review["reviewer"] == review["implementer"]
            or review["implementer"] != cycle["implementer"]
            or review.get("candidate") != cycle["candidate"]
            or review.get("suite") != cycle["suite"]
            or review.get("implementation") != cycle["implementation"]):
        raise EvidenceError("distinct review on exact candidate and suite required")


def next_plan(root, cycle, cycle_ref, review_ref=None, now=None):
    decision = assess(root, cycle, now)
    if decision["status"] != "review_pending":
        return {"status": "stopped", "decision": decision, "automatic_dispatch": False}
    if review_ref is None:
        return {"status": "review_pending", "decision": decision, "automatic_dispatch": False,
                "remaining_failures": decision["remaining_failures"], "budget": cycle["budget"],
                "repairs_used": cycle["repairs_used"]}
    try:
        if bound(root, cycle_ref) != cycle:
            raise EvidenceError("parent cycle reference changed")
        check_review(bound(root, review_ref), cycle)
    except (EvidenceError, OSError) as exc:
        return {"status": "review_blocked", "reason": str(exc), "automatic_dispatch": False}
    if cycle["iteration"] >= cycle["budget"]["max_cycles"]:
        return {"status": "budget_exhausted", "automatic_dispatch": False}
    return {"status": "proposal_only", "automatic_dispatch": False,
            "lineage": cycle["lineage"], "iteration": cycle["iteration"] + 1,
            "budget": cycle["budget"], "repairs_used": cycle["repairs_used"],
            "freeze": cycle["freeze"], "suite": cycle["suite"], "parent": cycle_ref,
            "parent_review": review_ref, "baseline_method_from": cycle["candidate"],
            "next_action": "name a distinct sourced defect, expected gain and permitted paths before implementation",
            "regression_rule": "expanded suites must retain every parent audit case unchanged; rerun both methods",
            "reviewer_identity": "labels unverified; record matching is a cooperative check, not authentication"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("audit")
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--registry", type=Path, required=True)
    p = sub.add_parser("run-suite")
    p.add_argument("--suite", type=Path, required=True)
    p.add_argument("--method", choices=("existence_v0", "bound_v1"), required=True)
    for name in ("assess", "next-plan"):
        p = sub.add_parser(name)
        p.add_argument("--root", type=Path, required=True)
        p.add_argument("--cycle", required=True, help="path relative to root")
        if name == "next-plan":
            p.add_argument("--review", help="typed review JSON relative to root")
    args = parser.parse_args()
    try:
        if args.command == "audit":
            result = audit(args.root, decode(read_file(args.registry)))
            code = 0 if result["issue_count"] == 0 else 1
        elif args.command == "run-suite":
            data = read_file(args.suite)
            result = run_suite(decode(data), sha(data), args.method)
            code = 0
        else:
            data = read_file(safe_path(args.root, args.cycle))
            cycle = decode(data)
            cycle_ref = {"path": args.cycle, "sha256": sha(data)}
            if args.command == "assess":
                result = assess(args.root, cycle)
                code = 0 if result["status"] in ("review_pending", "no_gain") else 1
            else:
                ref = None
                if args.review:
                    ref = {"path": args.review, "sha256": sha(read_file(safe_path(args.root, args.review)))}
                result = next_plan(args.root, cycle, cycle_ref, ref)
                code = 0 if result["status"] in ("review_pending", "proposal_only") else 1
        print(json.dumps(result, indent=2, allow_nan=False))
        return code
    except (EvidenceError, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "invalid_evidence", "reason": str(exc), "accepted": False}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
