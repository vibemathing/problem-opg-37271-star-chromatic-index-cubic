"""Resource-bounded POSIX runner. Records actual local generation, never trusted admission."""
from pathlib import Path
import sys, subprocess, resource, selectors, time, os, signal, json, hashlib, platform
from datetime import datetime, timezone
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
LIMITS={'wall_seconds':35,'cpu_soft_seconds':30,'cpu_hard_seconds':31,'memory_bytes':768*1024**2,
        'file_bytes':1024**2,'stdout_bytes':65536,'stderr_bytes':16384,'threads':1}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(LIMITS['memory_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(LIMITS['file_bytes'],)*2)
def run(name):
    path=HERE/('opg37271-c30-'+name+'.py');start=now();tic=time.monotonic()
    p=subprocess.Popen([sys.executable,str(path.relative_to(REPO))],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                       start_new_session=True,preexec_fn=limits)
    sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,0);sel.register(p.stderr,selectors.EVENT_READ,1)
    bufs=[bytearray(),bytearray()];timed=False;over=False
    while sel.get_map():
        if time.monotonic()-tic>35:timed=True;os.killpg(p.pid,signal.SIGKILL)
        for key,_ in sel.select(0.05):
            chunk=os.read(key.fd,65536)
            if not chunk:sel.unregister(key.fileobj);continue
            i=key.data;bufs[i].extend(chunk)
            if len(bufs[i])>[65536,16384][i]:over=True;os.killpg(p.pid,signal.SIGKILL)
        if timed or over:
            p.wait(timeout=3);break
    rc=p.wait(timeout=3);sel.close()
    r={'name':name,'command':['python3',path.relative_to(REPO).as_posix()],'started_at':start,'ended_at':now(),
       'elapsed_seconds':round(time.monotonic()-tic,6),'exit_code':rc,'timed_out':timed,'output_limit_exceeded':over}
    for key,b in zip(['stdout','stderr'],bufs):r[key+'_bytes']=len(b);r[key+'_sha256']=hashlib.sha256(b).hexdigest()
    return r
if __name__=='__main__':
    inputs=[HERE/('opg37271-c30-'+s) for s in ['input.json','produce.py','check.py','run.py']]
    before={p.name:sha(p) for p in inputs};start=now();stages=[]
    for name in ['produce','check']:
        z=run(name);stages.append(z)
        if z['exit_code']!=0 or z['timed_out'] or z['output_limit_exceeded']:break
    report={'verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,
            'input_revision':json.loads(inputs[0].read_text())['input_revision'],'started_at':start,'ended_at':now(),
            'interpreter':{'implementation':platform.python_implementation(),'version':platform.python_version(),
                           'binary_sha256':sha(Path(sys.executable).resolve())},'limits':LIMITS,'source_sha256':before,
            'sources_unchanged':before=={p.name:sha(p) for p in inputs},'stages':stages,
            'completed':len(stages)==2 and all(s['exit_code']==0 and not s['timed_out'] and not s['output_limit_exceeded'] for s in stages),
            'preliminary_diagnostics':['A syntax typo in a preliminary checker version was corrected before the final source-frozen replay. No failed run is counted as a successful check.'],
            'scope':'Fixed C30 embedding; all closed supports size1..3, two core families,125 passive inputs,pointwise completion controls. No all-ten-vertex census or trusted gate.'}
    report['files_sha256']={p.name:sha(p) for p in HERE.glob('opg37271-c30-*') if p.name.endswith(('certificate.json','minimum-tables.txt','summary.json','check-result.json'))}
    (HERE/'opg37271-c30-execution.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'verdict':'candidate_only','completed':report['completed'],'stages':[(s['name'],s['exit_code']) for s in stages]}))
    if not report['completed']:sys.exit(1)
