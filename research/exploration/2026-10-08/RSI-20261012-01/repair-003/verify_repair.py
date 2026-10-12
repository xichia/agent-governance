#!/usr/bin/env python3
"""Third-repair regression and bounded owner-extension controls; solo only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
import improve as engine
import verify


def main():
    suite = engine.decode(engine.read_file(ROOT / "suite.json"))
    freeze = engine.decode(engine.read_file(ROOT / "FREEZE.json"))
    original_authorization = engine.decode(engine.read_file(HERE / "authorization.json"))
    before = engine.run_suite(suite, freeze["suite_sha256"], "existence_v0")
    after = engine.run_suite(suite, freeze["suite_sha256"], "bound_v1")
    checks = []
    now = engine.time_value("2026-10-12T10:01:14Z")
    with tempfile.TemporaryDirectory(prefix="rsi-repair3-") as tmp:
        root = Path(tmp)
        cycle = verify.fixture(root, suite, freeze, before, after)
        cycle["repairs_used"] = 3
        assert engine.assess(root, cycle, now)["status"] == "budget_exhausted"
        checks.append("original frozen two-repair gate remains effective without extension")
        authorization = dict(original_authorization, lineage=cycle["lineage"])
        # Synthetic metadata checks are not new real-world owner authorizations.
        ref = verify.write(root, "extension.json", authorization)
        cycle["repair_extension"] = ref
        decision = engine.assess(root, cycle, now)
        assert decision["status"] == "review_pending" and decision["repairs_used"] == 3
        assert decision["effective_repair_limit"] == 3 and decision["accepted"] is False
        checks.append("one bound 2-to-3 extension permits evaluation, never acceptance")
        cycle_ref = verify.write(root, "cycle.json", cycle)
        pending = engine.next_plan(root, cycle, cycle_ref, now=now)
        assert pending["repair_extension"] == ref and pending["repairs_used"] == 3
        assert pending["automatic_dispatch"] is False
        checks.append("review-pending handoff retains extension and used repairs")
        cycle["repairs_used"] = 4
        assert engine.assess(root, cycle, now)["status"] == "budget_exhausted"
        checks.append("fourth repair remains forbidden")
        cycle["repairs_used"] = 3
        for label, patch in [
            ("wrong lineage", {"lineage": "OTHER"}),
            ("larger extension", {"additional_repairs": 2, "total_limit": 4}),
            ("boolean allowance", {"additional_repairs": True}),
        ]:
            cycle["repair_extension"] = verify.write(root, "invalid-extension.json", dict(authorization, **patch))
            assert engine.assess(root, cycle, now)["status"] == "invalid_evidence"
            checks.append(label + " rejected")
        cycle["repair_extension"] = ref
        review = {"kind": "independent_review", "verdict": "pass",
                  "reviewer": "fictional-separate-reviewer", "implementer": "/root",
                  "candidate": cycle["candidate"], "suite": cycle["suite"],
                  "implementation": cycle["implementation"]}
        review_ref = verify.write(root, "review.json", review)
        proposed = engine.next_plan(root, cycle, cycle_ref, review_ref, now)
        assert proposed["status"] == "proposal_only" and proposed["repair_extension"] == ref
        assert proposed["repairs_used"] == 3 and proposed["automatic_dispatch"] is False
        checks.append("synthetic reviewed proposal inherits extension; labels remain unverified")
        child = copy.deepcopy(cycle)
        child.update(id="TEST-02", iteration=2, parent=cycle_ref, parent_review=review_ref,
                     baseline=cycle["candidate"])
        assert engine.assess(root, child, now)["status"] == "no_gain"
        del child["repair_extension"]
        assert engine.assess(root, child, now)["status"] == "budget_exhausted"
        checks.append("child cannot drop inherited extension to erase repair accounting")
        bad = verify.write(root, "array-report.json", [])
        malformed = dict(cycle, candidate=bad)
        malformed_ref = verify.write(root, "malformed-cycle.json", malformed)
        process = subprocess.run([sys.executable, "-B", str(ROOT / "improve.py"), "assess",
                                  "--root", str(root), "--cycle", malformed_ref["path"]],
                                 capture_output=True, text=True, timeout=3)
        response = json.loads(process.stdout)
        assert process.returncode == 1 and not process.stderr
        assert response["status"] == "invalid_evidence" and response["accepted"] is False
        checks.append("NEG-01 returns structured invalid_evidence without traceback")
        (root / "array-suite.json").write_text("[]\n")
        process = subprocess.run([sys.executable, "-B", str(ROOT / "improve.py"), "run-suite",
                                  "--suite", str(root / "array-suite.json"), "--method", "bound_v1"],
                                 capture_output=True, text=True, timeout=3)
        assert process.returncode == 2 and not process.stderr
        assert json.loads(process.stdout)["accepted"] is False
        checks.append("malformed top-level suite has structured CLI failure")
    print(json.dumps({"producer_sha256": after["producer_sha256"], "repairs_used": 3,
                      "original_limit": 2, "explicit_additional_allowance": 1,
                      "checks": checks, "matched": len(checks),
                      "review": "solo self-check; no independent review claimed"}, indent=2))


if __name__ == "__main__":
    main()
