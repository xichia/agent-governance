"""Coordinator synthetic negative controls; never produce or rewrite model answers."""
import copy,hashlib,json
from pathlib import Path
from grade_trials import grade
P=Path(__file__).resolve().parent

def main():
 truth=json.loads((P/'groundtruth.json').read_text())
 files=sorted(f for f in (P/'trials').glob('*.json') if not f.name.endswith('.preliminary.json'))
 before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
 bundles={f.name:json.loads(f.read_text()) for f in files}
 denied=next(t for t in truth['trials'] if t['variant']=='A' and t['expected_service']['service_status']=='denied')
 wrong=copy.deepcopy(bundles);row=next(r for r in wrong['semantic_A.json']['trials'] if r['trial_id']==denied['trial_id'])
 row.update(status='current',value=999,source_id='fabricated',version='v999',evidence_digest='0'*64,complete=True)
 fake=grade(truth,wrong);target=next(r for r in fake['rows'] if r['trial_id']==denied['trial_id']);assert target['false_current'] and not target['matched']
 code=copy.deepcopy(bundles);code['semantic_A.json']['method']['classification_code_used']=True
 code_result=grade(truth,code);assert code_result['summary']['reported_classification_code_rows']==64 and code_result['summary']['verified_unassisted_rows']=='unknown_without_audit'
 missing=copy.deepcopy(bundles);removed=missing['semantic_C.json']['trials'].pop();missing_result=grade(truth,missing)
 assert any(e.get('error')=='missing_trials' and e['ids']==[removed['trial_id']] for e in missing_result['artifact_errors'])
 malformed=copy.deepcopy(bundles);malformed['semantic_A.json']['trials'][0]['lookups']=None
 malformed_result=grade(truth,malformed);assert any(e.get('error')=='bad_row_schema' for e in malformed_result['artifact_errors'])
 provenance=copy.deepcopy(bundles);provenance['semantic_A.json'].pop('method')
 provenance_result=grade(truth,provenance);assert any(e.get('error')=='missing_method_evidence' for e in provenance_result['artifact_errors'])
 after={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};assert before==after
 print(json.dumps({'type':'synthetic coordinator controls, in-memory copies only; not new model trials','unsupported_current':{'trial_id':denied['trial_id'],'false_current':target['false_current'],'matched':target['matched']},'declared_classification_code':{'reported_rows':64,'actual_unassisted':'unknown_without_audit'},'missing_row':{'removed':removed['trial_id'],'delivered':missing_result['summary']['delivered_unique'],'caught':True},'invalid_lookup_schema':'caught_without_crash','missing_method':'artifact_error','disk_raw_unchanged':before==after},indent=2))
if __name__=='__main__':main()
