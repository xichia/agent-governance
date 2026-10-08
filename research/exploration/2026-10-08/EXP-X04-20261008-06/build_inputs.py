"""Coordinator-only construction: freeze archived evidence/presentation/truth, not agent answers."""
import base64,hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;OLD=P.parent/'EXP-X04-20261008-05';C='a3daa24410eb10fa126d1f07b08509bdad835bb8';ROOT=P.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(path,obj):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n')
def oldread(name):
 f=OLD/name;b=f.read_bytes();assert b==subprocess.check_output(['git','show',C+':'+str(f.relative_to(ROOT))],cwd=ROOT),name;return json.loads(b)
truth05=oldread('groundtruth.json')['trials'];receipts={};updates={};prior={}
for n in range(1,5):
 w=f'mediated_{n}'
 receipts.update({r['trial_id']:r for r in oldread('receipts/'+w+'.json')['results']})
 updates.update({r['trial_id']:r for r in oldread('updates/'+w+'.json')['trials']})
 prior.update({r['trial_id']:r for r in oldread('packets/'+w+'.json')['trials']})
variants={v:[] for v in 'ABCD'};pre={v:[] for v in 'CD'};truth=[]
hyp={'A':'Historic full-context distraction: distinguish prior authoritative/local/memory claims from finalv3query and observedreceipt.','B':'Selective context retrieval: recover needed bytes through exact index export, never infer value from descriptor/path or source ID.','C':'Staged evidence-first handoff: a receipt observed before final authority/query is insufficient to determine currentness; retainpending until exact finalscope/date arrives.','D':'Claim-first anchoring: do not carry a historically supplied count into final task after dated supersession, even withdenied/changedreceipt.'}
for t in truth05:
 baseid=t['trial_id'];r=receipts[baseid];a=r['actual'];u=updates[baseid];context=prior[baseid]['context'];payload=base64.b64decode(a['payload_b64'],validate=True) if a['payload_b64'] is not None else None
 if payload is not None:assert sha(payload)==a['event']['observed_sha256']==t['trusted_source_sha256']
 envelope={'base_trial_id':baseid,'archive_candidate':C,'observed_broker_candidate':'ffb52d9f93f94569b2cabc47a305586536b53c22','provenance':'Actual05root-service archive; NO new06broker service or authenticatedcaller proof.','service_status':a['status'],'service_reason':a['reason'],'event':a['event'],'payload_utf8':payload.decode() if payload is not None else None,'payload_raw_sha256':sha(payload) if payload is not None else None}
 export=P/'receipt_exports'/f'{baseid}.json';write(export,envelope);pointer=str(export);pointersha=sha(export.read_bytes())
 for v in 'ABCD':
  tid='M06-'+v+'-'+sha((baseid+':semantic').encode())[:10]
  authority={'source_id':u['authoritative']['source_id'],'version':u['authoritative']['version'],'raw_sha256':u['authoritative']['raw_sha256']}
  row={'trial_id':tid,'prior_case_id':t['prior_case_id'],'query':u['request'],'authority':authority,'notice':u['notice'],'receipt_export_sha256':pointersha}
  if v=='A':row.update(historical_context=context,irrelevant_historic_note={'scope':'unrelated_demo','valid_until':'2025-12-31','value':6000,'status':'historical background, irrelevant to this query'},receipt=envelope)
  elif v=='B':row['index']={'exact_export_pointer':pointer,'sha256':pointersha,'base_trial_id':baseid,'capability':'read exactly this coordinator-owned archived receipt envelope; no new broker call; no other sources granted'}
  elif v=='C':
   pre[v].append({'trial_id':tid,'receipt':envelope,'stage_notice':'Final query/authority intentionally withheld until coordinator second nativehandoff. Record pending, notcurrent; retainobservedservice forlater.'})
   row['receipt_reference']={'previous_stage_trial_id':tid,'same_receipt_export_sha256':pointersha}
  else:
   older=context['memory']+context['local_sources'];note=older[0] if older else {'source_id':'fictional.catalog','version':'v1','scope':'north_depot','key':context['request']['key'],'value':80,'valid_until':'2026-10-01','status':'historical fictional summary; unsupported for unconfigured finalquery'}
   pre[v].append({'trial_id':tid,'historical_claim':note,'stage_notice':'This is a historical planningnote, not current finaltask evidence. Finalauthority/query follows insecondnativehandoff; recordpending, preservehistorydo not certify.'})
   row['receipt']=envelope
  variants[v].append(row)
  truth.append({'trial_id':tid,'base_trial_id':baseid,'variant':v,'worker':'semantic_'+v,'prior_case_id':t['prior_case_id'],'transition_kind':t['transition_kind'],'expected':t['final_expected'],'expected_service':{'service_status':a['status'],'service_reason':a['reason'],'service_seq':a['event']['seq']},'hypothesis':t['rationale']+' '+hyp[v],'receipt_export':pointer,'receipt_export_sha256':pointersha,'query':u['request'],'authority':authority})
for v,rows in variants.items():
 rows.sort(key=lambda r:r['trial_id'])
 if v in pre:pre[v].sort(key=lambda r:r['trial_id'])
 write(P/'packets'/f'semantic_{v}.json',{'worker':'semantic_'+v,'phase':'final','variant':v,'naming':'Opaque trial IDs do not encode expected status. Originalfamily/update mapping preserved only in coordinator truth. Evaluate provided evidence/query, not IDs or another row.','code_use':'Individually modelcompose statuses/values/reasons using literalJSON. No code/loop/branch deriving classification/reason/value. Readingtext, computinghashonly and validatingalreadywrittenJSONsyntax/count permissible; not classification. Serializationmustnotderiveanswers.','current_rule':'Exact finalauthority(source/version/rawhash), querykey/scope, inclusive valid_until>=as_of (null=noexpiry), supplied observedservedpayload. Supersessionnotice overrides historiccontext. Unresolvedfieldsnull/completefalse. Rootverifiedpayload_raw_sha256 is admissible integrity observation; recomputationoptionalhashonly. Hash does not authenticatesourceauthority.','presentation_hypothesis':hyp[v],'trials':rows})
 if v in pre:write(P/'packets'/f'semantic_{v}.preliminary.json',{'worker':'semantic_'+v,'phase':'preliminary','trials':pre[v]})
write(P/'groundtruth.json',{'schema_version':1,'source_candidate':C,'trials':truth})
(P/'trials').mkdir(exist_ok=True);(P/'snapshots').mkdir(exist_ok=True);(P/'handoffs').mkdir(exist_ok=True)
manifest={str(f.relative_to(P)):sha(f.read_bytes()) for sub in ('packets','receipt_exports') for f in (P/sub).glob('*')};manifest['groundtruth.json']=sha((P/'groundtruth.json').read_bytes());write(P/'frozen_manifest.json',manifest)
assert len(truth)==256 and len({x['trial_id'] for x in truth})==256
print('Frozen256distinctcrossedIDs;64pervariant, current',sum(t['expected']['status']=='current' for t in truth),'unresolved',sum(t['expected']['status']=='unresolved' for t in truth));print({v:(P/'packets'/f'semantic_{v}.json').stat().st_size for v in 'ABCD'})
