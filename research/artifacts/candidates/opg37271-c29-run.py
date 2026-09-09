"""Reproduce C29 under bounded processes; emits observations, not trusted receipts."""
from pathlib import Path
import subprocess,sys,platform,resource,hashlib,json,time,datetime,os

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
LIMITS={'wall_seconds':35,'cpu_soft_seconds':30,'cpu_hard_seconds':31,'memory_bytes':805306368,'file_bytes':1048576,'stdout_bytes':65536,'stderr_bytes':16384,'threads':1}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def encode(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(805306368,805306368));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def main():
    source_names=['opg37271-c29-produce.py','opg37271-c29-check.py','opg37271-c29-run.py','opg37271-c29-input.json']
    frozen={n:digest(HERE/n) for n in source_names}
    receipt={'schema_version':'c29-execution-1','verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,'input_revision':'d85f00bf7793de78a7d85e7d32b692925e8c2236','interpreter':{'version':platform.python_version(),'implementation':platform.python_implementation(),'binary_sha256':digest(Path(sys.executable).resolve())},'limits':LIMITS,'source_sha256':frozen,'started_at':now(),'stages':[],'route':'single-thread exact finite CPU work; no GPU or remote repository execution'}
    env=os.environ.copy();env.update({'PYTHONDONTWRITEBYTECODE':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
    for name in ('produce','check'):
        script='research/artifacts/candidates/opg37271-c29-'+name+'.py';start=now();tick=time.monotonic();timed=False
        try:
            p=subprocess.run([sys.executable,script],cwd=REPO,env=env,capture_output=True,timeout=35,preexec_fn=limits)
            stdout,stderr,exit_code=p.stdout,p.stderr,p.returncode
        except subprocess.TimeoutExpired as e:
            timed=True;stdout=e.stdout or b'';stderr=e.stderr or b'';exit_code=None
        overflow=len(stdout)>65536 or len(stderr)>16384
        stage={'name':name,'command':['python3',script],'started_at':start,'ended_at':now(),'elapsed_seconds':round(time.monotonic()-tick,6),'exit_code':exit_code,'timed_out':timed,'output_limit_exceeded':overflow,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()};receipt['stages'].append(stage)
        if timed or overflow or exit_code!=0:
            receipt.update(completed=False,ended_at=now());(HERE/'opg37271-c29-execution.json').write_bytes(encode(receipt));raise SystemExit('C29 stage did not complete: '+name)
    assert frozen=={n:digest(HERE/n) for n in source_names}
    cert=json.loads((HERE/'opg37271-c29-certificate.json').read_bytes());inp=json.loads((HERE/'opg37271-c29-input.json').read_bytes());aud=json.loads((HERE/'opg37271-c29-check-result.json').read_bytes())
    tables=[]
    for f in cert['main']['families']:
        S=f['support'];tables.append({'support':S,'endpoints':[{'entries':[r['word'][e] for e in S],'phase_costs':[p['cost'] for p in r['phases']],'anchored':r['anchored_minima']} for r in f['endpoints']]})
    summary={'schema_version':'c29-summary-1','verdict':'candidate_only','best_verified_result':'none','input_sha256':frozen['opg37271-c29-input.json'],'certificate_sha256':digest(HERE/'opg37271-c29-certificate.json'),'certificate_bytes':(HERE/'opg37271-c29-certificate.json').stat().st_size,'edges':inp['edges'],'old':inp['old'],'new':inp['new'],'paths':cert['main']['paths'],'old_phase_costs':[r['cost'] for r in cert['main']['old_phases']],'new_phase_costs':[r['cost'] for r in cert['new_phases']],'old_attainers':cert['main']['attainers'],'rows':[{'vertices':cert['main']['shapes'][r['shape']]['vertices'],'kind':cert['main']['shapes'][r['shape']]['kind'],'variables':r['variables'],'rhs':r['rhs']} for r in cert['main']['rows']],'minimum_connected_support':2,'complete_minimum_support_tables':tables,'core_families':[{'support':f['support'],'endpoints':len(f['endpoints']),'full_table_sha256':hashlib.sha256(encode(f)).hexdigest()} for f in cert['core_families']],'passive_completion_summary':[{'passive_colors':c['passive_colors'],'edge_count':len(c['edges']),'minimum_connected_support':c['audit']['minimum_support'],'repairs':c['audit']['repairs'],'full_table_sha256':hashlib.sha256(encode(c)).hexdigest()} for c in cert['passive_completions']],'transfer':cert['transfer'],'absorbed_profiles':cert['absorbed_profiles'],'literal_phase_records_compared':aud['literal_phase_records_compared'],'mutations':len(aud['mutations']),'A_relabelings':24,'all_embeddings_classified':False,'trusted_execution':False}
    (HERE/'opg37271-c29-summary.json').write_bytes(encode(summary))
    receipt.update(completed=True,sources_unchanged=True,ended_at=now(),files_sha256={n:digest(HERE/n) for n in ('opg37271-c29-certificate.json','opg37271-c29-check-result.json','opg37271-c29-summary.json')},preliminary_diagnostics=['A discovery-only broader embedding scan hit its35-second limit; no incomplete broad census is a final claim. Final replay uses only the fixed input and the complete125-choice passive family.'])
    (HERE/'opg37271-c29-execution.json').write_bytes(encode(receipt))
    print(json.dumps({'verdict':'candidate_only','completed':True,'phase_records':aud['literal_phase_records_compared'],'execution_sha256':digest(HERE/'opg37271-c29-execution.json')}))

if __name__=='__main__':main()
