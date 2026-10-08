"""Coordinator-only grading of preserved model outputs, not production of answers.

Code-use/read statements are self-reports; no unassisted proof is inferred.
Prose review is independent/manual and separate from structured agreement.
"""
import hashlib,json,base64
from pathlib import Path
P=Path(__file__).resolve().parent
FIELDS=('status','value','source_id','version','evidence_digest','complete')
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
def method_grade(m):
 if not isinstance(m,dict) or type(m.get('classification_code_used')) is not bool or not isinstance(m.get('classification'),str) or not isinstance(m.get('serialization'),str) or not isinstance(m.get('deviations'),list):return 'unknown_or_invalid_method'
 return 'reported_classification_code_used' if m['classification_code_used'] else 'self_reported_model_composed_not_audited'
def grade(truth,bundles):
 targets={t['trial_id']:t for t in truth['trials']};seen=set();rows=[];errors=[];methods=[]
 for filename,bundle in bundles.items():
  if not isinstance(bundle,dict) or bundle.get('phase')!='final' or not isinstance(bundle.get('trials'),list):errors.append({'file':filename,'error':'bad_bundle'});continue
  worker=bundle.get('worker');method=method_grade(bundle.get('method'));methods.append({'file':filename,'worker':worker,'method_status':method,'raw_method':bundle.get('method'),'access_notes':bundle.get('access_notes')})
  if method=='unknown_or_invalid_method':errors.append({'file':filename,'error':'missing_method_evidence'})
  if not isinstance(bundle.get('access_notes'),list):errors.append({'file':filename,'error':'missing_access_notes'})
  for raw in bundle['trials']:
   if not isinstance(raw,dict):errors.append({'file':filename,'error':'bad_row'});continue
   tid=raw.get('trial_id')
   if tid not in targets or tid in seen:errors.append({'file':filename,'trial_id':tid,'error':'unknown_or_duplicate'});continue
   seen.add(tid);t=targets[tid]
   if worker!=t['worker']:errors.append({'file':filename,'trial_id':tid,'error':'wrong_worker'})
   dif={k:{'expected':t['expected'][k],'observed':raw.get(k)} for k in FIELDS if not same(raw.get(k),t['expected'][k])}
   schema=(all(k in raw for k in (*FIELDS,'reason','limitation','service_status','service_reason','service_seq','lookups')) and raw.get('status') in ('current','unresolved') and type(raw.get('complete')) is bool and isinstance(raw.get('reason'),str) and bool(raw.get('reason')) and isinstance(raw.get('limitation'),str) and bool(raw.get('limitation')) and type(raw.get('service_seq')) is int and isinstance(raw.get('lookups'),list))
   if not schema:errors.append({'file':filename,'trial_id':tid,'error':'bad_row_schema'})
   service_match=all(same(raw.get(k),v) for k,v in t['expected_service'].items())
   safe=raw.get('status')=='unresolved' and raw.get('complete') is False and all(raw.get(k) is None for k in ('value','source_id','version','evidence_digest'))
   lookup_claim=any(isinstance(x,dict) and x.get('path')==t['receipt_export'] and x.get('attempted') is True and x.get('result') in ('read','available','retrieved','success') for x in (raw.get('lookups') if isinstance(raw.get('lookups'),list) else []))
   rows.append({'trial_id':tid,'file':filename,'worker':worker,'variant':t['variant'],'prior_case_id':t['prior_case_id'],'transition_kind':t['transition_kind'],'matched':not dif,'differences':dif,'schema_ok':schema,'false_current':raw.get('status')=='current' and bool(dif),'safe_unresolved':safe,'factual_recovery':t['expected']['status']=='current' and not dif,'service_correspondence':service_match,'lookup_report_matches_exact_pointer':lookup_claim,'method_status':method,'prose_review':'not decided by structured grader; separate manual review required'})
 missing=sorted(set(targets)-seen)
 if missing:errors.append({'error':'missing_trials','ids':missing})
 summary={'expected':len(targets),'delivered_unique':len(seen),'matched':sum(r['matched'] for r in rows),'factual_recovery':sum(r['factual_recovery'] for r in rows),'safe_unresolved':sum(r['safe_unresolved'] for r in rows),'false_current':sum(r['false_current'] for r in rows),'service_correspondence':sum(r['service_correspondence'] for r in rows),'reported_classification_code_rows':sum(r['method_status']=='reported_classification_code_used' for r in rows),'self_reported_model_composed_rows':sum(r['method_status']=='self_reported_model_composed_not_audited' for r in rows),'verified_unassisted_rows':'unknown_without_audit'}
 return {'summary':summary,'rows':rows,'artifact_errors':errors,'method_records':methods,'limits':'Clustered/presentation-worker confounded; native outputs plus self-reported code-use, no independent reading or classification tool audit. Wrong model answers preserved.'}
def support(envelope,t):
 if envelope['service_status']!='served' or envelope['payload_utf8'] is None:return None
 b=envelope['payload_utf8'].encode();r=json.loads(b);a=t['authority'];q=t['query']
 if sha(b)!=a['raw_sha256'] or any(r.get(k)!=a[k] for k in ('source_id','version')) or any(r.get(k)!=q[k] for k in ('key','scope')) or (r.get('valid_until') is not None and r['valid_until']<q['as_of']):return None
 return r

def main():
 for name,digest in json.loads((P/'frozen_manifest.json').read_text()).items():assert sha((P/name).read_bytes())==digest,'frozen input changed '+name
 truth=json.loads((P/'groundtruth.json').read_text());exports={};checks=[]
 old=P.parent/'EXP-X04-20261008-05';actual05={r['trial_id']:r['actual'] for n in range(1,5) for r in json.loads((old/'receipts'/f'mediated_{n}.json').read_text())['results']}
 for t in truth['trials']:
  path=Path(t['receipt_export']);b=path.read_bytes();assert sha(b)==t['receipt_export_sha256'];envelope=json.loads(b);a=actual05[t['base_trial_id']];assert envelope['event']==a['event'] and envelope['service_status']==a['status'] and envelope['service_reason']==a['reason']
  raw=base64.b64decode(a['payload_b64'],validate=True) if a['payload_b64'] is not None else None;assert envelope['payload_utf8']==(raw.decode() if raw is not None else None);assert envelope['payload_raw_sha256']==(sha(raw) if raw is not None else None)
  supported=support(envelope,t);exp=t['expected'];assert (supported is not None)==(exp['status']=='current')
  if supported:assert same(supported['value'],exp['value']) and supported['source_id']==exp['source_id'] and supported['version']==exp['version'] and sha(raw)==exp['evidence_digest']
  exports[t['base_trial_id']]=envelope
 bundles={};rawhashes={}
 for f in sorted((P/'trials').glob('*.json')):
  b=f.read_bytes();rawhashes[str(f.relative_to(P))]=sha(b)
  if not f.name.endswith('.preliminary.json'):bundles[f.name]=json.loads(b)
 snapshot_checks=[]
 for f in sorted((P/'snapshots').glob('*.json')):
  assert f.read_bytes()==(P/'trials'/f.name).read_bytes(),'submitted record changed '+f.name;snapshot_checks.append(f.name)
 preliminary={}
 for v in 'CD':
  path=P/'trials'/f'semantic_{v}.preliminary.json'
  if path.exists():
   doc=json.loads(path.read_text());target={t['trial_id'] for t in truth['trials'] if t['variant']==v};got=[r['trial_id'] for r in doc['trials']];assert len(got)==64 and set(got)==target and all(r['status']=='pending' and isinstance(r['provisional_note'],str) and r['provisional_note'] for r in doc['trials']);preliminary[v]={'count':len(got),'method_status':method_grade(doc.get('method'))}
 result=grade(truth,bundles);result['raw_sha256']=rawhashes;result['snapshot_continuity']=snapshot_checks;result['preliminary']=preliminary;result['archived_service']={'unique_base_receipts':len(exports),'status_counts':{s:sum(r['service_status']==s for r in exports.values()) for s in ('served','denied','changed')},'new06_broker_invocations':0,'distinction':'64actual05archives exported in256presentations; no256newserviceevents'}
 print(json.dumps(result,indent=2));return bool(result['artifact_errors'])
if __name__=='__main__':raise SystemExit(main())
