"""Grade preserved agent observations against predeclared fictional truth.

Lookup/read assertions are self-reported, not independent tool traces.
Wrong answers are study outcomes and never rewritten by this grader.
"""
import hashlib
import json
from pathlib import Path


def exact(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False)


def grade(truth, outputs):
    rows, errors, seen = [], [], set()
    for owner, bundle in outputs.items():
        if not isinstance(bundle, dict) or not isinstance(bundle.get('trials'), list):
            errors.append({'owner': owner, 'error': 'invalid_bundle'})
            continue
        for raw in bundle['trials']:
            if not isinstance(raw, dict):
                errors.append({'owner': owner, 'error': 'invalid_trial'})
                continue
            tid = raw.get('trial_id')
            targets = [x for x in truth['trials'] if x['trial_id'] == tid]
            if len(targets) != 1 or tid in seen:
                errors.append({'owner': owner, 'trial_id': tid, 'error': 'unknown_or_duplicate_trial'})
                continue
            target = targets[0]
            seen.add(tid)
            if target['executor'] != owner:
                errors.append({'owner': owner, 'trial_id': tid, 'error': 'wrong_writer'})
            expected = target['expected']
            fields = ('status', 'value', 'source_id', 'version', 'complete')
            differences = {k: {'expected': expected[k], 'observed': raw.get(k)} for k in fields if not exact(raw.get(k), expected[k])}
            packet = json.loads(Path(target['packet_path']).read_text())
            expected_digest = packet['authoritative']['digest'] if expected['status'] == 'current' else None
            if not exact(raw.get('evidence_digest'), expected_digest):
                differences['evidence_digest'] = {'expected': expected_digest, 'observed': raw.get('evidence_digest')}
            schema_ok = all(k in raw for k in (*fields, 'evidence_digest', 'reason', 'lookups', 'limitation')) and raw.get('status') in ('current', 'unresolved') and type(raw.get('complete')) is bool and isinstance(raw.get('reason'), str) and isinstance(raw.get('limitation'), str) and isinstance(raw.get('lookups'), list)
            if not schema_ok:
                errors.append({'owner': owner, 'trial_id': tid, 'error': 'invalid_observation_schema'})
            current = raw.get('status') == 'current'
            false_current = current and bool(differences)
            safe_unresolved = raw.get('status') == 'unresolved' and raw.get('complete') is False and all(raw.get(k) is None for k in ('value', 'source_id', 'version', 'evidence_digest'))
            recovered = expected['status'] == 'current' and not differences
            pointer = target['granted_pointer']
            lookup_claim = False
            if isinstance(raw.get('lookups'), list):
                lookup_claim = any(isinstance(x, dict) and x.get('path') == pointer and x.get('attempted') is True and x.get('result') == 'available' for x in raw['lookups']) if pointer else False
            rows.append({'trial_id': tid, 'owner': owner, 'condition': target['condition'], 'mechanism': target['mechanism'], 'matched': not differences, 'differences': differences, 'false_current': false_current, 'factual_recovery': recovered, 'safe_unresolved': safe_unresolved, 'expected_current': expected['status'] == 'current', 'supported_retrieval_self_report': bool(recovered and lookup_claim), 'schema_ok': schema_ok})
    missing = [x['trial_id'] for x in truth['trials'] if x['trial_id'] not in seen]
    if missing:
        errors.append({'error': 'missing_trials', 'ids': missing})
    return {'rows': rows, 'artifact_errors': errors, 'summary': {'expected_trials': len(truth['trials']), 'delivered_unique': len(seen), 'matched': sum(x['matched'] for x in rows), 'false_current': sum(x['false_current'] for x in rows), 'expected_current': sum(x['expected_current'] for x in rows), 'factual_recovery': sum(x['factual_recovery'] for x in rows), 'safe_unresolved': sum(x['safe_unresolved'] for x in rows), 'supported_retrieval_self_report': sum(x['supported_retrieval_self_report'] for x in rows), 'read_compliance': 'not independently audited', 'usage_cost_queue': 'unavailable'}}


def main():
    root = Path(__file__).resolve().parent
    truth = json.loads((root / 'groundtruth.json').read_text())
    for t in truth['trials']:
        assert hashlib.sha256(Path(t['packet_path']).read_bytes()).hexdigest() == t['packet_sha256'], 'packet changed'
        if t['granted_pointer']:
            assert hashlib.sha256(Path(t['granted_pointer']).read_bytes()).hexdigest() == t['source_sha256'], 'source changed'
    outputs = {f'trial_{n}': json.loads((root / 'trials' / f'trial_{n}.json').read_text()) for n in range(1, 5)}
    result = grade(truth, outputs)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2))
    return bool(result['artifact_errors'])


if __name__ == '__main__':
    raise SystemExit(main())
