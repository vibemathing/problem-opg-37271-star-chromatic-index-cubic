"""Bounded C26 replay in a disposable checkout. Never a trusted receipt.
No network calls. Every program and input is supplied in this repository.
"""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, resource, selectors
import shutil, subprocess, sys, time
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
WORK=HERE/'c26-work'
LIMITS={'wall_seconds':35,'cpu_soft_seconds':30,'cpu_hard_seconds':31,
        'memory_bytes':768*1024**2,'file_bytes':4*1024**2,
        'stdout_bytes':1024**2,'stderr_bytes':16384,'threads':1}
EXEC=HERE/'opg37271-c26-execution.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def filehash(p):return sha(pathlib.Path(p).read_bytes())
def put(p,obj):p.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rel(p):
    try:return pathlib.Path(p).resolve().relative_to(ROOT).as_posix()
    except (ValueError,OSError):return pathlib.Path(p).name

def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(4*1024**2,)*2)

def call(name,args,data=b''):
    if len(data)>16384:raise ValueError('stdin cap')
    entry={'name':name,'command':[rel(x) if '/' in str(x) else str(x) for x in args],
           'started_at':now(),'stdin_bytes':len(data),'stdin_sha256':sha(data)}
    started=time.monotonic();buffers=[bytearray(),bytearray()];timeout=False;excess=False
    process=subprocess.Popen(list(map(str,args)),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        cwd=ROOT,preexec_fn=limits,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
    process.stdin.write(data);process.stdin.close();sel=selectors.DefaultSelector()
    for i,f in enumerate((process.stdout,process.stderr)):
        os.set_blocking(f.fileno(),False);sel.register(f,selectors.EVENT_READ,i)
    while sel.get_map():
        remaining=35-(time.monotonic()-started)
        if remaining<=0:timeout=True;process.kill();break
        for key,_ in sel.select(min(remaining,.2)):
            chunk=os.read(key.fileobj.fileno(),65536)
            if not chunk:sel.unregister(key.fileobj);continue
            k=key.data;buffers[k].extend(chunk)
            if len(buffers[k])>(1024**2 if k==0 else 16384):excess=True;process.kill();break
        if excess:break
    sel.close()
    try:code=process.wait(timeout=max(.1,35-(time.monotonic()-started)))
    except subprocess.TimeoutExpired:timeout=True;process.kill();code=process.wait()
    process.stdout.close();process.stderr.close();out,err=map(bytes,buffers)
    entry.update(ended_at=now(),elapsed_seconds=round(time.monotonic()-started,6),exit_code=code,
        timed_out=timeout,output_limit_exceeded=excess,stdout_bytes=len(out),stderr_bytes=len(err),
        stdout_sha256=sha(out),stderr_sha256=sha(err))
    report['stages'].append(entry);put(EXEC,report)
    if code or timeout or excess:raise RuntimeError(name+' failed; see execution record')
    return out

def request(obj,mode,bound):
    s=f"{mode} {obj['n']} {len(obj['edges'])} {bound}\n"+''.join(f'{a} {b}\n' for a,b in obj['edges'])
    if mode=='patches':s+=' '.join(map(str,obj['word']))+'\n'
    return s.encode()

report={}
def main():
    global report
    WORK.mkdir(exist_ok=True)
    report={'verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,
      'input_revision':'bf3b3306434831fd5300670fb6a2de92914787f2','started_at':now(),'limits':LIMITS,'stages':[],
      'scope':'Three complete smaller-graph state catalogues; all supports through four edges on one fixed eight-vertex frame. No new all-order-eight or all-order-ten census.'}
    put(EXEC,report)
    sources={p.name:filehash(p) for p in sorted(HERE.glob('opg37271-c26-*')) if p.suffix in ('.py','.cpp')}
    compiler=call('compiler-version',['g++','--version']).decode().splitlines()[0]
    report['toolchain']={'python':sys.version.split()[0],'implementation':sys.implementation.name,
      'python_binary_sha256':filehash(pathlib.Path(sys.executable).resolve()),'compiler':compiler,
      'compiler_binary_sha256':filehash(pathlib.Path(shutil.which('g++')).resolve()),
      'source_sha256':sources,'lean_found':shutil.which('lean') is not None,'lake_found':shutil.which('lake') is not None}
    raw=(HERE/'opg37271-c26-input.json').read_bytes();inp=json.loads(raw);report['input_sha256']=sha(raw)
    exe=WORK/'c26-search';call('compile-search',['g++','-std=c++17','-O3',HERE/'opg37271-c26-search.cpp','-o',exe])
    report['toolchain']['search_binary_sha256']=filehash(exe)
    table={}
    for obj in inp['graphs']+[inp['case']]:
        mode='patches' if obj is inp['case'] else 'catalog';K=4 if mode=='patches' else 3
        out=call('search-'+obj['name'],[exe],request(obj,mode,K));table[obj['name']]=json.loads(out)
        (WORK/(obj['name']+'.json')).write_bytes(out)
    put(HERE/'opg37271-c26-search-result.json',table)
    put(HERE/'opg37271-c26-supports.json',table[inp['case']['name']])
    checks={}
    for label in ('K4','K33','prism','case'):
        out=call('check-'+label,[sys.executable,HERE/'opg37271-c26-check.py',label]);checks[label]=json.loads(out)
    mutation=json.loads(call('mutations',[sys.executable,HERE/'opg37271-c26-mutations.py']))
    cert=json.loads((HERE/'opg37271-c26-certificate.json').read_text())
    catalogs={}
    for name in ('K4','K33','prism'):
        full=(json.dumps(table[name],sort_keys=True,separators=(',',':'))+'\n').encode()
        catalogs[name]=checks[name]|{'complete_table_bytes':len(full),'complete_table_sha256':sha(full)}
    summary={'verdict':'candidate_only','state':'NONTERMINAL_CHECKPOINT','best_verified_result':'none',
      'small_graph_catalogues':catalogs,'case':cert['summary'],'mutations':mutation,
      'weighted_cycle_cases':cert['weighted_cycle_checks'],
      'all_catalogues_path':'research/artifacts/candidates/opg37271-c26-search-result.json',
      'all_catalogues_sha256':filehash(HERE/'opg37271-c26-search-result.json'),
      'all_catalogues_note':'Regenerated by this runner and retained in the recovery archive; not a hidden input.',
      'new_census_order_bound':6,'larger_fixed_case_order':8,
      'not_replayed':'The C25 full nineteen-graph computation is prior main data, not a new execution in this turn.'}
    put(HERE/'opg37271-c26-summary.json',summary)
    report['ended_at']=now();report['all_exit_zero']=all(s['exit_code']==0 for s in report['stages'])
    report['all_stderr_empty']=all(s['stderr_bytes']==0 for s in report['stages'])
    report['outputs']={p.name:filehash(p) for p in sorted(HERE.glob('opg37271-c26-*.json')) if p.name not in ('opg37271-c26-execution.json','opg37271-c26-admission-request.json','opg37271-c26-statement.json')}
    put(EXEC,report)
    print(json.dumps({'verdict':'candidate_only','stages':len(report['stages']),'all_exit_zero':report['all_exit_zero'],
        'all_stderr_empty':report['all_stderr_empty'],'summary_sha256':filehash(HERE/'opg37271-c26-summary.json'),'case':cert['summary'],'mutations':mutation},sort_keys=True))
if __name__=='__main__':main()
