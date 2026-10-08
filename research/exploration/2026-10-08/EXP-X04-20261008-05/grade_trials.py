"""Grade unchanged scripted-assistance agent outputs; never rewrite raw observations.

Oracle comparison is not proof of model reading. Root service correspondence is
separate from factual currentness. Exports remain clustered and nonblind.
"""
import base64,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
FIELDS=('status','value','source_id','version','evidence_digest','complete')
def same(a,b):return json.dumps(a,sort_keys=True,ensure_ascii=False)==json.dumps(b,sort_keys=True,ensure_ascii=False)
def sha(b):return hashlib.sha256(b).hexdigest()
def grade(truth,outputs,receipts):
 rows=[];errors=[]
 for worker,both in outputs.items():
  targets={t['trial_id']:t for t in truth['trials'] if t['worker']==worker}
  recs=receipts[worker]['results'];service={r['trial_id']:r for r in recs}
  for phase,bundle in both.items():
   if not isinstance(bundle,dict) or bundle.get('worker')!=worker or bundle.get('phase')!=phase or not isinstance(bundle.get('trials'),list):errors.append({'worker':worker,'phase':phase,'error':'bad_bundle'});continue
   seen=set()
   for raw in bundle['trials']:
    if not isinstance(raw,dict):errors.append({'worker':worker,'phase':phase,'error':'bad_row'});continue
    tid=raw.get('trial_id')
    if tid not in targets or tid in seen:errors.append({'worker':worker,'phase':phase,'trial_id':tid,'error':'unknown_duplicate_wrong_owner'});continue
    seen.add(tid);t=targets[tid];exp=t[phase+'_expected']
    schema=(all(k in raw for k in (*FIELDS,'trial_id','reason','limitation')) and raw['status'] in ('current','unresolved') and type(raw['complete']) is bool and isinstance(raw['reason'],str) and isinstance(raw['limitation'],str))
    dif={k:{'expected':exp[k],'observed':raw.get(k)} for k in FIELDS if not same(raw.get(k),exp[k])}
    receipt=service[tid];actual=receipt['actual'];event=actual['event']
    request_matches=same(receipt['submitted_request'],t['expected_request'])
    event_match=True
    if phase=='initial':
     request_matches=request_matches and same(raw.get('lookup_request'),t['expected_request']);schema=schema and isinstance(raw.get('lookup_request'),dict)
    else:
     schema=schema and all(k in raw for k in ('service_status','service_reason','service_seq')) and type(raw.get('service_seq')) is int
     event_match=all(same(raw.get(k),v) for k,v in {'service_status':actual['status'],'service_reason':actual['reason'],'service_seq':event['seq']}.items())
    if not schema:errors.append({'worker':worker,'phase':phase,'trial_id':tid,'error':'bad_schema'})
    safe=raw.get('status')=='unresolved' and raw.get('complete') is False and all(raw.get(k) is None for k in ('value','source_id','version','evidence_digest'))
    rows.append({'trial_id':tid,'phase':phase,'worker':worker,'prior_case_id':t['prior_case_id'],'transition_kind':t['transition_kind'],'matched':not dif,'differences':dif,'false_current':raw.get('status')=='current' and bool(dif),'safe_unresolved':safe,'expected_current':exp['status']=='current','factual_recovery':exp['status']=='current' and not dif,'request_matches':request_matches,'service_correspondence':event_match,'schema_ok':schema})
   if seen!=set(targets):errors.append({'worker':worker,'phase':phase,'error':'missing_trials','ids':sorted(set(targets)-seen)})
 summary={phase:{'delivered':sum(r['phase']==phase for r in rows),'matched':sum(r['phase']==phase and r['matched'] for r in rows),'false_current':sum(r['phase']==phase and r['false_current'] for r in rows),'factual_recovery':sum(r['phase']==phase and r['factual_recovery'] for r in rows),'safe_unresolved':sum(r['phase']==phase and r['safe_unresolved'] for r in rows),'request_matches':sum(r['phase']==phase and r['request_matches'] for r in rows),'service_correspondence':sum(r['phase']==phase and r['service_correspondence'] for r in rows)} for phase in ('initial','final')}
 return {'rows':rows,'artifact_errors':errors,'summary':summary,'limits':'Four configured-Luna sessions used locally written deterministic scripts;64clustered transitions, not64independent model judgments. Shared file responses; no independent read audit or unassisted model memory test.'}
def verify_receipts(truth,receipts):
 byid={t['trial_id']:t for t in truth['trials']};counts={};issues=[]
 for worker,bundle in receipts.items():
  if len(bundle['events'])!=16:issues.append(worker+':event_count')
  for seq,r in enumerate(bundle['results'],1):
   t=byid[r['trial_id']];a=r['actual'];e=a['event'];counts[a['status']]=counts.get(a['status'],0)+1
   assert e==bundle['events'][seq-1] and e['seq']==seq
   assert a['status']==t['expected_broker']['status'] and a['reason']==t['expected_broker']['reason']
   assert e['caller_authenticated'] is False and e['time_source']=='process_wall_clock'
   assert e['requested_path']==r['submitted_request']['path'] and e['request_id']==r['submitted_request']['request_id']
   source=(P/'sources'/t['source_path']).read_bytes()
   assert sha(source)==t['actual_source_sha256']
   if a['status']=='served':
    b=base64.b64decode(a['payload_b64'],validate=True);assert b==source and sha(b)==e['observed_sha256']==t['trusted_source_sha256'] and len(b)==e['observed_byte_count']==e['served_byte_count']
   elif a['status']=='changed':assert a['payload_b64'] is None and e['observed_sha256']==sha(source) and e['observed_byte_count']==len(source) and e['served_byte_count']==0
   else:assert a['payload_b64'] is None and e['observed_sha256'] is None and e['observed_byte_count']==e['served_byte_count']==0
 return {'event_count':sum(counts.values()),'status_counts':counts,'issues':issues}
def main():
 for name,digest in json.loads((P/'frozen_manifest.json').read_text()).items():assert sha((P/name).read_bytes())==digest,'frozen input changed '+name
 truth=json.loads((P/'groundtruth.json').read_text());outputs={};receipts={};continuity=[]
 dispatch={x['recipient'].split('/')[-1]:x for x in json.loads((P/'native_dispatches.json').read_text())}
 for n in range(1,5):
  w=f'mediated_{n}';initial=(P/'trials'/f'{w}.initial.json').read_bytes();snapshot=(P/'snapshots'/f'{w}.initial.json').read_bytes();assert initial==snapshot,'initial output changed'
  receipt=json.loads((P/'receipts'/f'{w}.json').read_text());assert sha(initial)==receipt['initial_sha256'];receipts[w]=receipt
  response=(P/'handoffs'/f'{w}.json').read_bytes();assert sha(response)==dispatch[w]['response_sha256'];handoff=json.loads(response);assert handoff['service_results']==receipt['results'] and handoff['updates']==json.loads((P/'updates'/f'{w}.json').read_text())['trials']
  outputs[w]={ph:json.loads((P/'trials'/f'{w}.{ph}.json').read_text()) for ph in ('initial','final')};continuity.append({'worker':w,'initial_sha256':sha(initial),'final_sha256':sha((P/'trials'/f'{w}.final.json').read_bytes()),'response_sha256':sha(response)})
 result=grade(truth,outputs,receipts);result['service_verification']=verify_receipts(truth,receipts);result['raw_continuity']=continuity
 print(json.dumps(result,indent=2));return bool(result['artifact_errors'])
if __name__=='__main__':raise SystemExit(main())
