"""Coordinator ONLY: persist initial snapshots, actual broker results and final file responses."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
P=Path(__file__).resolve().parent
C='ffb52d9f93f94569b2cabc47a305586536b53c22'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(path,obj):
 with path.open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def run(worker):
 for name,digest in json.loads((P/'frozen_manifest.json').read_text()).items():assert sha((P/name).read_bytes())==digest,'changed frozen input '+name
 bpath=P.parent/'EXP-X04-20261008-04'/'broker.py';rel=bpath.relative_to(P.parents[3]);assert bpath.read_bytes()==subprocess.check_output(['git','show',C+':'+str(rel)],cwd=P.parents[3])
 spec=importlib.util.spec_from_file_location('accepted04broker',bpath);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 initialpath=P/'trials'/f'{worker}.initial.json';initial=initialpath.read_bytes();snapshot=P/'snapshots'/f'{worker}.initial.json'
 with snapshot.open('xb') as f:f.write(initial)
 bundle=json.loads(initial);assert bundle['worker']==worker and bundle['phase']=='initial';rows=bundle['trials'];assert len(rows)==16 and len({x['trial_id'] for x in rows})==16
 target={x['trial_id']:x for x in json.loads((P/'groundtruth.json').read_text())['trials'] if x['worker']==worker}
 broker=m.Broker(P/'sources',json.loads((P/'grants.json').read_text()));results=[]
 for row in rows:
  assert row['trial_id'] in target,'unexpected trial'
  req=row.get('lookup_request');result=broker.retrieve(req)
  results.append({'trial_id':row['trial_id'],'submitted_request':req,'exact_declared_request':req==target[row['trial_id']]['expected_request'],'actual':result})
 response={'worker':worker,'phase':'final','initial_sha256':sha(initial),'broker_candidate':C,'recipient':'/root/'+worker,'delivery_kind':'coordinator-owned file response with exact native pointer/hash message; not inline native payload delivery','created_at':datetime.now(timezone.utc).isoformat(),'updates':json.loads((P/'updates'/f'{worker}.json').read_text())['trials'],'service_results':results,'limitations':'Root observed broker bytes; agent reading and all other reads not audited; caller_label untrusted; shared filesystem; no usage/queue/cost telemetry.'}
 put(P/'receipts'/f'{worker}.json',{'worker':worker,'initial_sha256':sha(initial),'broker_candidate':C,'results':results,'events':broker.events})
 put(P/'handoffs'/f'{worker}.json',response)
 print(json.dumps({'worker':worker,'response_sha256':sha((P/'handoffs'/f'{worker}.json').read_bytes()),'events':len(broker.events),'status_counts':{s:sum(x['status']==s for x in broker.events) for s in ('served','denied','changed','missing','failing')}}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('worker',choices=[f'mediated_{i}' for i in range(1,5)]);run(parser.parse_args().worker)
