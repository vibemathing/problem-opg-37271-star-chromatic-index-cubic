"""Bounded C25 candidate replay, never a trusted-verifier receipt.

Run --batch 0 5, --batch 5 10, --batch 10 15, --batch 15 19, then --finish.
No external mathematical input, old compiler, or network request is used.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, pathlib, resource, selectors
import shutil, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WORK = HERE / 'c25-work'
WORK.mkdir(exist_ok=True)
EXEC = HERE / 'opg37271-c25-execution.json'
LIMITS = dict(wall_seconds=35, cpu_soft_seconds=30, cpu_hard_seconds=31,
              memory_bytes=768*1024**2, file_bytes=1048576,
              stdout_bytes=1048576, stderr_bytes=16384, threads=1)

def digest(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def put(p, obj): p.write_text(json.dumps(obj, sort_keys=True, indent=2)+'\n', encoding='utf-8')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30,31))
    resource.setrlimit(resource.RLIMIT_AS, (768*1024**2,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576,)*2)
def rel(p):
    try: return pathlib.Path(p).resolve().relative_to(ROOT).as_posix()
    except (ValueError,OSError): return pathlib.Path(p).name

def call(name, argv, data=b'', destination=None):
    if len(data)>4096: raise ValueError('stdin budget')
    rec=dict(name=name, command=[rel(a) if '/' in str(a) else str(a) for a in argv],
             stdin_sha256=hashlib.sha256(data).hexdigest(), stdin_bytes=len(data), started_at=now())
    start=time.monotonic(); buffers=[bytearray(),bytearray()]; timed=False; excess=False
    p=subprocess.Popen(list(map(str,argv)), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, preexec_fn=limits, cwd=ROOT,
                       env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
    p.stdin.write(data); p.stdin.close()
    selector=selectors.DefaultSelector()
    for i,pipe in enumerate((p.stdout,p.stderr)):
        os.set_blocking(pipe.fileno(),False); selector.register(pipe,selectors.EVENT_READ,i)
    while selector.get_map():
        remaining=35-(time.monotonic()-start)
        if remaining<=0:
            timed=True; p.kill(); break
        for key,_ in selector.select(min(remaining,0.25)):
            chunk=os.read(key.fileobj.fileno(),65536)
            if not chunk: selector.unregister(key.fileobj); continue
            i=key.data; buffers[i].extend(chunk)
            if len(buffers[i])>(1048576 if i==0 else 16384):
                excess=True; p.kill(); break
        if excess: break
    selector.close()
    try: code=p.wait(timeout=max(0.1,35-(time.monotonic()-start)))
    except subprocess.TimeoutExpired: timed=True; p.kill(); code=p.wait()
    p.stdout.close(); p.stderr.close()
    stdout,stderr=map(bytes,buffers)
    rec.update(ended_at=now(),elapsed_seconds=round(time.monotonic()-start,6),exit_code=code,
               timed_out=timed,output_limit_exceeded=excess,stdout_bytes=len(stdout),stderr_bytes=len(stderr),
               stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_sha256=hashlib.sha256(stderr).hexdigest())
    if destination is not None and code==0 and not timed and not excess:
        destination.write_bytes(stdout); rec.update(output_path=rel(destination),output_sha256=digest(destination))
    log=json.loads(EXEC.read_text()) if EXEC.exists() else dict(verdict='candidate_only',best_verified_result='none',limits=LIMITS,stages=[],trusted_execution=False)
    log['stages'].append(rec); put(EXEC,log)
    if timed or excess or code!=0:
        raise RuntimeError(f'{name}: exit={code}, timeout={timed}, output_limit={excess}')
    return stdout

def setup():
    for stem in ('graphs','global','replay'):
        src=HERE/f'opg37271-c25-{stem}.cpp'; exe=WORK/stem; stamp=WORK/f'{stem}.sha256'
        expected=digest(src)
        if not exe.exists() or not stamp.exists() or stamp.read_text()!=expected:
            args=['g++','-std=c++17','-O3',str(src)]
            if stem!='graphs': args+=['-lcrypto']
            call('compile-'+stem,args+['-o',str(exe)]); stamp.write_text(expected)
    compiler=call('compiler-version',['g++','--version']).decode().splitlines()[0]
    crypto=call('crypto-version',['openssl','version']).decode().strip()
    libraries=call('linked-library-identity',['ldd',WORK/'global']).decode().splitlines()
    crypto_files=[line.split('=>',1)[1].strip().split()[0] for line in libraries if 'libcrypto.so' in line and '=>' in line]
    if len(crypto_files)!=1: raise ValueError('ambiguous crypto fingerprint')
    sources={p.name:digest(p) for p in sorted(HERE.glob('opg37271-c25-*')) if p.suffix in ('.cpp','.py')}
    meta=dict(python=sys.version.split()[0],implementation=sys.implementation.name,
              python_binary_sha256=digest(pathlib.Path(sys.executable).resolve()),compiler=compiler,
              compiler_binary_sha256=digest(pathlib.Path(shutil.which('g++')).resolve()),openssl=crypto,
              crypto_binary_sha256=digest(crypto_files[0]),source_sha256=sources,
              executable_sha256={stem:digest(WORK/stem) for stem in ('global','graphs','replay')})
    log=json.loads(EXEC.read_text()); log['toolchain']=meta; put(EXEC,log)
    if not (HERE/'opg37271-c25-graphs10.json').exists():
        call('all-connected-cubic10',[WORK/'graphs','10'],destination=HERE/'opg37271-c25-graphs10.json')

def batch(lo,hi):
    catalog=json.loads((HERE/'opg37271-c25-graphs10.json').read_text())
    if not 0<=lo<=hi<=len(catalog['graphs']): raise ValueError('batch domain')
    for g in catalog['graphs'][lo:hi]:
        i=g['index']; data=('10 15\n'+''.join(f'{a} {b}\n' for a,b in g['edges'])).encode()
        dest=HERE/f'opg37271-c25-space10-{i:02d}.json'
        a_raw=call(f'global-10-{i}',[WORK/'global'],data,dest); a=json.loads(a_raw)
        b_raw=call(f'replay-10-{i}',[WORK/'replay'],data); b=json.loads(b_raw)
        ignore=('engine','nodes')
        if {k:v for k,v in a.items() if k not in ignore}!={k:v for k,v in b.items() if k not in ignore}:
            raise RuntimeError(f'Full domain mismatch: graph {i}')
        log=json.loads(EXEC.read_text())
        log.setdefault('complete_comparisons',{})[str(i)]=dict(agreed=True,stream_sha256=a['stream_sha256'],
            frames=a['frames'],phases=a['phases'],global_stdout_sha256=hashlib.sha256(a_raw).hexdigest(),
            replay_stdout_sha256=hashlib.sha256(b_raw).hexdigest())
        put(EXEC,log)
        print(i,a['frames'],a['balanced'],a['phases'],a['balanced_perfect_U'],flush=True)

def finish():
    gs=json.loads((HERE/'opg37271-c25-graphs10.json').read_text()); rows=[]
    log=json.loads(EXEC.read_text())
    for g in gs['graphs']:
        path=HERE/f"opg37271-c25-space10-{g['index']:02d}.json"; r=json.loads(path.read_text())
        cmp=log['complete_comparisons'][str(g['index'])]
        if not cmp['agreed'] or cmp['global_stdout_sha256']!=digest(path): raise ValueError('comparison binding')
        rows.append({k:v for k,v in r.items() if k not in ('U_rows','engine','nodes')}|
                    dict(index=g['index'],generated_output_sha256=digest(path),U_topologies=len(r['U_rows'])))
    put(HERE/'opg37271-c25-summary.json',dict(verdict='candidate_only',best_verified_result='none',
        order=10,types=len(rows),graphs=rows,totals={k:sum(r[k] for r in rows) for k in
        ('frames','raw_frames','phases','raw_phases','balanced','balanced_spanning_short2','balanced_perfect_U')},
        all_have_balanced_frame=all(r['balanced']>0 for r in rows),root_closed=False))
    for name in ('coverage','audit','mutations'):
        target=HERE/f"opg37271-c25-{name+'-result' if name in ('audit','mutations') else name}.json"
        call(name,[sys.executable,HERE/f'opg37271-c25-{name}.py'],destination=target)
    log=json.loads(EXEC.read_text()); log['frozen_input_sha256']=digest(HERE/'opg37271-c25-graphs10.json')
    log['final_outputs']={p.name:digest(p) for p in sorted(HERE.glob('opg37271-c25-*.json'))
                          if p.name not in ('opg37271-c25-execution.json','opg37271-c25-admission-request.json')
                          and 'topology-example' not in p.name}
    put(EXEC,log)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--batch',type=int,nargs=2)
    parser.add_argument('--finish',action='store_true'); args=parser.parse_args()
    if args.finish: finish()
    else: setup(); batch(*(args.batch or (0,19)))
