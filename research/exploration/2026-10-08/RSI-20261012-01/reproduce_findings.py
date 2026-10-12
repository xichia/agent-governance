#!/usr/bin/env python3
"""Reproduce retained solo findings against exact archived source candidates."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
import improve
import verify

HERE = Path(__file__).resolve().parent


def module(name, file, expected):
    data = improve.read_file(file)
    assert improve.sha(data) == expected
    spec = importlib.util.spec_from_file_location(name, file)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def main():
    first = module("prior1", HERE / "history/before-round-1.py",
                   "3fbcca65bd9dba3b7e5e7e3eb79653153a7911bccf8bc282fbbceccd7de83ef1")
    second = module("prior2", HERE / "history/before-round-2.py",
                    "695eb82eb405fc687a6f455c9f89bf922162116eaa662bd9a9d0b52b0dbde6c7")
    findings = []
    with tempfile.TemporaryDirectory(prefix="rsi-findings-") as tmp:
        root = Path(tmp)
        data = b"current evidence\n"
        (root / "payload.txt").write_bytes(data)
        registry = {"schema_version": True, "artifacts": [
            {"id": "one", "path": "payload.txt", "sha256": improve.sha(data)}]}
        assert first.audit(root, registry)["rows"][0]["outcome"] == "ok"
        try:
            improve.audit(root, registry)
            raise AssertionError("boolean schema accepted")
        except improve.EvidenceError:
            findings.append({"round": 1, "finding": "boolean schema version accepted",
                             "before": "ok", "after": "EvidenceError", "disposition": "fixed"})
        suite = improve.decode(improve.read_file(HERE / "suite.json"))
        freeze = improve.decode(improve.read_file(HERE / "FREEZE.json"))
        b = first.run_suite(suite, freeze["suite_sha256"], "existence_v0")
        a = first.run_suite(suite, freeze["suite_sha256"], "bound_v1")
        cycle = verify.fixture(root, suite, freeze, b, a)
        old_source = improve.read_file(HERE / "history/before-round-1.py")
        (root / "implementation.py").write_bytes(old_source)
        cycle["implementation"]["sha256"] = improve.sha(old_source)
        review = {"kind": "independent_review", "verdict": "pass", "reviewer": " /root ",
                  "implementer": "/root", "candidate": cycle["candidate"],
                  "suite": cycle["suite"], "implementation": cycle["implementation"]}
        first.check_review(review, cycle)
        try:
            improve.check_review(review, cycle)
            raise AssertionError("whitespace self-review accepted")
        except improve.EvidenceError:
            findings.append({"round": 1, "finding": "whitespace alias passes self-review label check",
                             "before": "record accepted", "after": "EvidenceError", "disposition": "fixed",
                             "limitation": "distinct arbitrary labels still do not authenticate people or agents"})
        review["reviewer"] = "fictional-separate-reviewer"
        cycle["baseline"] = cycle["candidate"]
        parent_ref = verify.write(root, "parent.json", cycle)
        review_ref = verify.write(root, "review.json", review)
        child = copy.deepcopy(cycle)
        child.update(id="TEST-02", iteration=2, parent=parent_ref, parent_review=review_ref)
        now = improve.time_value("2026-10-12T08:32:59Z")
        old = first.assess(root, child, now)
        fixed = improve.assess(root, child, now)
        assert old["status"] == "no_gain" and fixed["status"] == "invalid_evidence"
        findings.append({"round": 1, "finding": "no-gain parent could reach child assessment with a supplied review label",
                         "before": old["status"], "after": fixed["status"], "disposition": "fixed",
                         "limitation": "synthetic review data only; no actual independent review occurred"})
        registry["schema_version"] = 1
        before = second.audit(root, registry, "existence_v0")["all_bound_bytes_match"]
        after = improve.audit(root, registry, "existence_v0")["all_bound_bytes_match"]
        assert before is True and after is None
        findings.append({"round": 2, "finding": "existence-only comparator incorrectly labels byte matching true",
                         "before": before, "after": after, "disposition": "fixed"})
    print(json.dumps({"review_kind": "solo self-check; not independent", "repairs_used": 2,
                      "repair_limit": 2, "findings": findings}, indent=2))


if __name__ == "__main__":
    main()
