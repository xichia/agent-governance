#!/usr/bin/env python3
"""Reproduce frozen controls and probe actual evidence/lineage failure paths."""
import copy
from datetime import timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
import improve as engine

HERE = Path(__file__).resolve().parent


def write(root, name, value):
    data = (json.dumps(value, indent=2, allow_nan=False) + "\n").encode()
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {"path": name, "sha256": engine.sha(data)}


def fixture(root, suite, freeze, before, after):
    source = engine.read_file(HERE / "improve.py")
    (root / "implementation.py").write_bytes(source)
    suite_ref = write(root, "suite.json", suite)
    local_freeze = dict(freeze, suite_sha256=suite_ref["sha256"])
    cycle = {"schema_version": 1, "id": "TEST-01", "lineage": "TEST",
             "iteration": 1, "repairs_used": 0, "implementer": "/root",
             "objective": "bounded control", "hypothesis": "bound references expose drift",
             "stop_rule": "no gain, regression, unavailable review or exhausted bound",
             "budget": freeze["budget"], "freeze": write(root, "freeze.json", local_freeze),
             "suite": suite_ref,
             "implementation": {"path": "implementation.py", "sha256": engine.sha(source)},
             "baseline": write(root, "before.json", before),
             "candidate": write(root, "after.json", after)}
    return cycle


def main():
    raw = engine.read_file(HERE / "suite.json")
    suite = engine.decode(raw)
    freeze = engine.decode(engine.read_file(HERE / "FREEZE.json"))
    assert engine.sha(raw) == freeze["suite_sha256"], "frozen suite bytes changed"
    assert [c["id"] for c in suite["audit_cases"] + suite["gate_cases"]] == freeze["case_ids"]
    before = engine.run_suite(suite, engine.sha(raw), "existence_v0")
    after = engine.run_suite(suite, engine.sha(raw), "bound_v1")
    output = {"suite_sha256": engine.sha(raw), "producer_sha256": after["producer_sha256"],
              "primary_controls": [], "additional_checks": [],
              "independent_review": "unavailable; coordinator self-check only"}
    for case, row in zip(suite["audit_cases"], after["observations"]):
        assert row["outcome"] == case["expected"], (case["id"], row)
        output["primary_controls"].append({"id": case["id"], "observed": row["outcome"], "matched": True})
    now = engine.time_value("2026-10-12T08:32:59Z")
    for case in suite["gate_cases"]:
        with tempfile.TemporaryDirectory(prefix="rsi-gate-") as tmp:
            root = Path(tmp)
            b, a = copy.deepcopy(before), copy.deepcopy(after)
            scenario = case["scenario"]
            if scenario == "no_gain":
                b = copy.deepcopy(a)
            elif scenario == "regression":
                a["observations"][0]["outcome"] = "changed"
            elif scenario == "suite_changed":
                a["suite_sha256"] = "0" * 64
            elif scenario == "missing_row":
                a["observations"].pop()
            cycle = fixture(root, suite, freeze, b, a)
            if scenario == "tampered_report":
                with (root / "after.json").open("ab") as stream:
                    stream.write(b"\n")
            elif scenario == "repair_overrun":
                cycle["repairs_used"] = 3
            elif scenario == "cycle_overrun":
                cycle["iteration"] = 4
            when = engine.time_value(freeze["budget"]["deadline"]) + timedelta(seconds=1) if scenario == "deadline" else now
            result = engine.assess(root, cycle, when)
            assert result["status"] == case["expected"], (case["id"], result)
            assert not result.get("accepted", False)
            output["primary_controls"].append({"id": case["id"], "observed": result["status"], "matched": True})
    with tempfile.TemporaryDirectory(prefix="rsi-extra-") as tmp:
        root = Path(tmp)
        cycle = fixture(root, suite, freeze, before, after)
        cycle_ref = write(root, "cycle.json", cycle)
        proposal = engine.next_plan(root, cycle, cycle_ref, now=now)
        assert proposal["status"] == "review_pending" and proposal["automatic_dispatch"] is False
        output["additional_checks"].append("no review cannot advance or dispatch")
        # Fabricated review DATA tests syntax/binding; no actual review is claimed.
        review = {"kind": "independent_review", "verdict": "pass", "reviewer": "/root",
                  "implementer": "/root", "candidate": cycle["candidate"],
                  "suite": cycle["suite"], "implementation": cycle["implementation"]}
        ref = write(root, "review.json", review)
        assert engine.next_plan(root, cycle, cycle_ref, ref, now)["status"] == "review_blocked"
        output["additional_checks"].append("self-review label rejected")
        review["reviewer"] = "fictional-separate-reviewer"
        review["candidate"] = {"path": "after.json", "sha256": "0" * 64}
        ref = write(root, "review.json", review)
        assert engine.next_plan(root, cycle, cycle_ref, ref, now)["status"] == "review_blocked"
        output["additional_checks"].append("wrong candidate review rejected")
        review["candidate"] = cycle["candidate"]
        ref = write(root, "review.json", review)
        proposal = engine.next_plan(root, cycle, cycle_ref, ref, now)
        assert proposal["status"] == "proposal_only" and proposal["budget"] == cycle["budget"]
        assert proposal["repairs_used"] == cycle["repairs_used"] and proposal["automatic_dispatch"] is False
        assert "unverified" in proposal["reviewer_identity"]
        output["additional_checks"].append("synthetic distinct-label proposal retains bounds; identity remains unverified")
        child = copy.deepcopy(cycle)
        child.update(id="TEST-02", iteration=2, parent=cycle_ref, parent_review=ref,
                     baseline=cycle["candidate"])
        child["repairs_used"] = 0
        child["budget"] = dict(cycle["budget"], max_cycles=4)
        assert engine.assess(root, child, now)["status"] == "invalid_evidence"
        output["additional_checks"].append("child budget reset rejected")
        child["budget"] = cycle["budget"]
        altered_suite = copy.deepcopy(suite)
        altered_suite["audit_cases"][0]["expected"] = "changed"
        child["suite"] = write(root, "child-suite.json", altered_suite)
        assert engine.assess(root, child, now)["status"] == "invalid_evidence"
        output["additional_checks"].append("child rewritten regression oracle rejected")
        child["suite"] = cycle["suite"]
        assert engine.assess(root, child, now)["status"] == "no_gain"
        output["additional_checks"].append("valid child with no new improvement stops at no_gain")
        cycle["repairs_used"] = 1
        child["parent"] = write(root, "cycle.json", cycle)
        assert engine.assess(root, child, now)["status"] == "invalid_evidence"
        output["additional_checks"].append("child decreasing inherited used repairs rejected")
        child["repairs_used"] = 1
        cycle["baseline"] = cycle["candidate"]
        child["parent"] = write(root, "cycle.json", cycle)
        assert engine.assess(root, child, now)["status"] == "invalid_evidence"
        output["additional_checks"].append("matching review labels cannot advance a no-gain parent")
        review["reviewer"] = " /root "
        try:
            engine.check_review(review, cycle)
            raise AssertionError("whitespace self-review alias accepted")
        except engine.EvidenceError:
            output["additional_checks"].append("whitespace self-review alias rejected")
        write(root, "registry.json", {"schema_version": 1, "artifacts": [{"id": "fifo", "path": "pipe", "sha256": "0" * 64}]})
        os.mkfifo(root / "pipe")
        completed = subprocess.run([sys.executable, "-B", str(HERE / "improve.py"), "audit",
                                    "--root", str(root), "--registry", str(root / "registry.json")],
                                   capture_output=True, text=True, timeout=3)
        assert completed.returncode == 1 and json.loads(completed.stdout)["rows"][0]["outcome"] == "nonregular"
        output["additional_checks"].append("FIFO rejected by CLI within three-second bound")
        missing = subprocess.run([sys.executable, "-B", str(HERE / "improve.py"), "assess",
                                  "--root", str(root), "--cycle", "absent.json"],
                                 capture_output=True, text=True, timeout=3)
        assert missing.returncode == 2 and json.loads(missing.stdout)["accepted"] is False
        output["additional_checks"].append("missing whole cycle has structured CLI failure")
        try:
            engine.decode(b'{"id": 1, "id": 2}')
            raise AssertionError("duplicate JSON keys accepted")
        except engine.EvidenceError:
            output["additional_checks"].append("duplicate JSON keys rejected")
        (root / "parent").symlink_to(root, target_is_directory=True)
        registry = {"schema_version": 1, "artifacts": [{"id": "nested", "path": "parent/before.json", "sha256": cycle["baseline"]["sha256"]}]}
        assert engine.audit(root, registry)["rows"][0]["outcome"] == "symlink"
        output["additional_checks"].append("symlink in ancestor rejected")
        try:
            engine.audit(root, {"schema_version": True, "artifacts": [{"id": "one", "path": "before.json", "sha256": "0" * 64}]})
            raise AssertionError("boolean schema version accepted")
        except engine.EvidenceError:
            output["additional_checks"].append("boolean schema version rejected")
        unbound_baseline = engine.audit(root, {"schema_version": 1, "artifacts": [{"id": "one", "path": "before.json", "sha256": "0" * 64}]}, "existence_v0")
        assert unbound_baseline["all_bound_bytes_match"] is None
        output["additional_checks"].append("existence-only baseline leaves byte matching unknown")
    output["primary_matched"] = len(output["primary_controls"])
    output["baseline_audit_matches"] = sum(engine.scores(before, suite).values())
    output["candidate_audit_matches"] = sum(engine.scores(after, suite).values())
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
