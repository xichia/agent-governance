#!/usr/bin/env python3
"""Run the independently authored X01 acceptance fixtures against validator.py."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from validator import validate


def main() -> int:
    fixture_path = Path(__file__).with_name("cases.json")
    try:
        cases = json.loads(fixture_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL fixtures: could not read {fixture_path.name}: {type(exc).__name__}: {exc}")
        return 1

    if not isinstance(cases, list) or not cases:
        print("FAIL fixtures: expected a nonempty JSON array")
        return 1

    failures = 0
    for index, case in enumerate(cases, 1):
        case_id = case.get("id", f"case-{index}") if isinstance(case, dict) else f"case-{index}"
        if not isinstance(case, dict):
            print(f"FAIL {case_id}: fixture is not an object")
            failures += 1
            continue
        expected = case.get("expect_valid")
        try:
            inputs = {path: value.encode("utf-8") for path, value in case["inputs"].items()}
            before = copy.deepcopy((case["payload"], case["assignment"], inputs))
            errors = validate(case["payload"], case["assignment"], inputs)
            unchanged = before == (case["payload"], case["assignment"], inputs)
            if not isinstance(errors, list) or any(not isinstance(error, str) for error in errors):
                outcome = "invalid-return"
                detail = f"returned {type(errors).__name__}, expected list[str]"
            else:
                accepted = len(errors) == 0
                outcome = "accepted" if accepted else "rejected"
                detail = "; ".join(errors) if errors else "no errors"
            matches = isinstance(expected, bool) and accepted == expected if isinstance(errors, list) and all(isinstance(e, str) for e in errors) else False
            if not unchanged:
                matches = False
                detail += "; validator mutated an input"
            status = "PASS" if matches else "FAIL"
            if not matches:
                failures += 1
            print(f"{status} {case_id}: expected={'accept' if expected is True else 'reject' if expected is False else expected}, actual={outcome}; {detail}")
        except Exception as exc:
            failures += 1
            print(f"FAIL {case_id}: validator/fixture crashed: {type(exc).__name__}: {exc}")

    total = len(cases)
    passed = total - failures
    print(f"Summary: {passed}/{total} cases matched expectations; {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
