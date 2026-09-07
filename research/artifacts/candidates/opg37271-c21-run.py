"""Bounded generator-domain runner. Does not invoke repository/trusted adapters."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,platform,subprocess,sys,time,shutil

HERE=Path(__file__).resolve().parent
CAP=1048576

def digest(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def run(script,args=(),input_bytes=None):
    env=os.environ.copy()
    env.update(PYTHONHASHSEED='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    start=now();clock=time.monotonic()
    p=subprocess.Popen([sys.executable,script,*args],cwd=HERE,env=env,stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    timeout=False
    try:out,err=p.communicate(input_bytes,timeout=40)
    except subprocess.TimeoutExpired:
        p.kill();out,err=p.communicate();timeout=True
    record={'command':['python3',script,*args],'started_at':start,'ended_at':now(),'elapsed_seconds':round(time.monotonic()-clock,6),'exit_code':p.returncode,'timed_out':timeout,'stdin_sha256':None if input_bytes is None else digest(input_bytes),'stdout_bytes':len(out),'stdout_sha256':digest(out),'stderr_bytes':len(err),'stderr_sha256':digest(err)}
    if timeout or p.returncode!=0 or len(out)>CAP or len(err)>16384:
        raise RuntimeError(json.dumps({'execution':record,'stderr_excerpt':err[:512].decode('utf-8','replace')}))
    return out,record

def main():
    files=['opg37271-c21-input.json','opg37271-c21-certificate.json','opg37271-c21-construct.py','opg37271-c21-replay.py','opg37271-c21-run.py','opg37271-c19-phase-certificate.json']
    hashes={name:digest((HERE/name).read_bytes()) for name in files}
    stream,a=run('opg37271-c21-construct.py',('opg37271-c21-input.json',))
    result,b=run('opg37271-c21-replay.py',input_bytes=stream)
    report=json.loads(result)
    if report['stream_sha256']!=digest(stream):raise ValueError('stream identity')
    (HERE/'opg37271-c21-result.json').write_bytes(result)
    execution={'verdict':'candidate_only','trust_domain':'web-candidate-generation','input_revision':'d4853563085f4310d1d99cb332de62f44c36fbda','command':'python3 research/artifacts/candidates/opg37271-c21-run.py','interpreter':{'implementation':platform.python_implementation(),'version':platform.python_version(),'binary_sha256':digest(Path(sys.executable).read_bytes())},'input_and_source_sha256':hashes,'limits_per_child':{'wall_seconds':35,'cpu_soft_seconds':30,'cpu_hard_seconds':31,'address_space_bytes':768*1024**2,'outer_timeout_seconds':40,'stdout_bytes':CAP,'stderr_bytes':16384,'threads':1},'runs':[a,b],'result_sha256':digest(result),'stress_stream_disposition':'Deterministically reconstructed from the committed finite domain and constructor; passed directly to the separate replay, not a trusted receipt. Compact exceptional graph witnesses are committed.','local_tools':{'lean_found':shutil.which('lean') is not None,'lake_found':shutil.which('lake') is not None},'assurance':'No Lean, SMT, registered verifier, EvidenceLink or admission executed.'}
    text=json.dumps(execution,sort_keys=True,indent=2)+'\n'
    (HERE/'opg37271-c21-execution.json').write_text(text)
    print(json.dumps({'verdict':'candidate_only','groups':report['groups'],'exception_graphs':report['k5_exceptions']['graphs'],'mutations':len(report['tests']['mutations']),'local_words':report['tests']['local_words_checked'],'general_preframes':[(r['n'],len(r['minimum_core'] or [])) for r in report['tests']['general_preframes']],'k33':report['tests']['k33_complete_small_palette_counts'],'result_sha256':digest(result),'execution_sha256':digest(text.encode())},sort_keys=True))
if __name__=='__main__':main()
