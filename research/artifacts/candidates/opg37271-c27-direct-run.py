"""Generate a bounded candidate-domain execution observation for the direct audit."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib,json,os,platform,resource,subprocess,sys,tempfile,time
H=Path(__file__).resolve().parent
L=dict(wall_seconds=35,cpu_soft_seconds=30,cpu_hard_seconds=31,memory_bytes=768*1024**2,file_bytes=1048576,stdout_bytes=16384,stderr_bytes=16384,threads=1)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def restrict():
    resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(L['memory_bytes'],)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(L['file_bytes'],)*2)
def main():
    files=['opg37271-c27-direct-audit.py','opg37271-c27-direct-run.py'];before={p:sha(H/p) for p in files};stamp=datetime.now(timezone.utc).isoformat();started=time.monotonic();timed=False
    with tempfile.TemporaryFile() as out,tempfile.TemporaryFile() as err:
        p=subprocess.Popen([sys.executable,str(H/files[0])],cwd=H,stdout=out,stderr=err,preexec_fn=restrict,env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
        try:code=p.wait(timeout=L['wall_seconds'])
        except subprocess.TimeoutExpired:timed=True;p.kill();code=p.wait()
        out.seek(0);a=out.read(L['stdout_bytes']+1);err.seek(0);b=err.read(L['stderr_bytes']+1)
    limit=len(a)>L['stdout_bytes'] or len(b)>L['stderr_bytes'];unchanged=before=={p:sha(H/p) for p in files}
    r=dict(schema_version='c27-direct-execution-1',verdict='candidate_only',best_verified_result='none',trusted_execution=False,input_revision='ae10c3584208290e30e2e6cdafa584f3b89c17e5',started_at=stamp,ended_at=datetime.now(timezone.utc).isoformat(),elapsed_seconds=round(time.monotonic()-started,6),command=['python3','research/artifacts/candidates/'+files[0]],exit_code=code,timed_out=timed,output_limit_exceeded=limit,stdout_bytes=len(a),stderr_bytes=len(b),stdout_sha256=hashlib.sha256(a).hexdigest(),stderr_sha256=hashlib.sha256(b).hexdigest(),interpreter=dict(implementation=platform.python_implementation(),version=platform.python_version(),binary_sha256=sha(sys.executable)),limits=L,source_sha256=before,sources_unchanged=unchanged,preliminary_diagnostics=['A proposed nonzero-h control endpoint failed the D-star premise before acceptance; replaced with a literally enumerated valid endpoint. No failed control is used as a mathematical counterexample.'],scope='Self-contained C27 10/16 endpoint replay and five one-edge supersets, C26 literal profile interface, actual nonzero-h control, abstract cut-only countermodel. No C26 core imported, no new all-cubic census or trusted gate.')
    result=H/'opg37271-c27-direct-audit.json'
    if code==0 and not timed and not limit and not b and unchanged:
        r['summary']=json.loads(a);r['result_sha256']=sha(result);r['completed']=True
    else:r['completed']=False
    (H/'opg37271-c27-direct-execution.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(verdict='candidate_only',completed=r['completed'],exit_code=code,elapsed_seconds=r['elapsed_seconds'],result_sha256=r.get('result_sha256')),sort_keys=True))
    return 0 if r['completed'] else 1
if __name__=='__main__':raise SystemExit(main())
