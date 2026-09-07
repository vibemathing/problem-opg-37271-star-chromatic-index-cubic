"""Reproduce C24 finite complete spaces in a fresh output directory.
No network, Git writes, Evidence creation or old compiler imports.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,platform,resource,shutil,subprocess,sys,tempfile,time
HERE=Path(__file__).parent
SOURCES=['opg37271-c24-catalog.py','opg37271-c24-space.cpp','opg37271-c24-check.py','opg37271-c24-audit.py']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--resume',action='store_true');parser.add_argument('--max-new-graphs',type=int,default=8);args=parser.parse_args();out=Path(args.output)
    source_lock={name:sha(HERE/name) for name in SOURCES+['opg37271-c24-run.py']}
    if args.resume:
        old=json.loads((out/'execution.partial.json').read_text())
        if old['source_lock']!=source_lock:raise ValueError('resume source drift')
        records=old['stages']
    else:
        if out.exists():raise ValueError('output directory must not exist; preserve old runs')
        out.mkdir(parents=True);records=[]
        for name in SOURCES:shutil.copyfile(HERE/name,out/name)
    compiler=shutil.which('g++')
    if compiler is None:raise RuntimeError('g++ missing')
    def execute(label,argv,inputs):
        def caps():
            resource.setrlimit(resource.RLIMIT_CPU,(35,36));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(5242880,)*2)
        input_sha={name:sha(out/name) for name in inputs}
        for old in records:
            if old['stage']==label:
                b=(out/(label+'.stdout')).read_bytes()
                if old['inputs']!=input_sha or hashlib.sha256(b).hexdigest()!=old['stdout_sha256']:raise ValueError('resume input/output drift')
                if old['exit_code']!=0:raise ValueError('cannot reuse failed stage')
                return b
        start=datetime.now(timezone.utc).isoformat();t=time.monotonic();timed=False
        with tempfile.TemporaryFile() as so,tempfile.TemporaryFile() as se:
            p=subprocess.Popen(argv,cwd=out,stdout=so,stderr=se,preexec_fn=caps,env=dict(os.environ,PYTHONHASHSEED='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
            try:rc=p.wait(timeout=40)
            except subprocess.TimeoutExpired:timed=True;p.kill();rc=p.wait(timeout=3)
            so.seek(0);stdout=so.read(5242881);se.seek(0);stderr=se.read(5242881)
        r=dict(stage=label,argv=[Path(argv[0]).name]+argv[1:],inputs=input_sha,started=start,ended=datetime.now(timezone.utc).isoformat(),elapsed=round(time.monotonic()-t,6),exit_code=rc,timed_out=timed,stdout_bytes=len(stdout),stdout_sha256=hashlib.sha256(stdout).hexdigest(),stderr_bytes=len(stderr),stderr_sha256=hashlib.sha256(stderr).hexdigest())
        records.append(r);(out/(label+'.stdout')).write_bytes(stdout);(out/'execution.partial.json').write_text(json.dumps(dict(source_lock=source_lock,stages=records),sort_keys=True,indent=2)+'\n')
        if rc or timed or len(stdout)>5242880 or len(stderr)>16384:raise RuntimeError('bounded stage failed: '+label)
        if label not in ('build','catalog'):(out/(label+'.json')).write_bytes(stdout)
        return stdout
    version=execute('compiler-version',[compiler,'--version'],[]).decode().splitlines()[0]
    execute('catalog',[sys.executable,'opg37271-c24-catalog.py'],[SOURCES[0]])
    cat=json.loads((out/'opg37271-c24-catalog.json').read_text())
    if [(r['n'],r['rooted_labelled_graphs'],r['disconnected'],len(r['representatives'])) for r in cat['orders']]!=[(4,1,0,1),(6,7,0,2),(8,553,1,5)]:raise ValueError('catalogue coverage sentinel')
    execute('build',[compiler,'-O2','-std=c++20','opg37271-c24-space.cpp','-o','c24-space'],[SOURCES[1]])
    reports=[];new_graphs=0
    for group in cat['orders']:
        for i,g in enumerate(group['representatives']):
            tag=f"n{g['n']}-g{i}";file=tag+'.txt';(out/file).write_text(f"{g['n']} {len(g['edges'])}\n"+''.join(f'{a} {b}\n' for a,b in g['edges']))
            was_done=any(r['stage']=='check-'+tag for r in records)
            if not was_done and new_graphs>=args.max_new_graphs:
                print(json.dumps(dict(verdict='candidate_only',state='bounded_replay_partial',completed_graphs=len(reports))));return
            execute('space-'+tag,['./c24-space',file,tag],[SOURCES[1],file])
            execute('check-'+tag,[sys.executable,SOURCES[2],tag],[SOURCES[2],file,tag+'.states'])
            report=json.loads((out/(tag+'.checked.json')).read_text());report.pop('all_blocks')
            report['blocks_stream_sha256']=sha(out/(tag+'.blocks'));report['blocks_stream_bytes']=(out/(tag+'.blocks')).stat().st_size
            report['state_stream_bytes']=(out/(tag+'.states')).stat().st_size
            reports.append(report)
            if not was_done:new_graphs+=1
    audit=json.loads(execute('audit',[sys.executable,SOURCES[3]],[SOURCES[2],SOURCES[3]]))
    summary=dict(verdict='candidate_only',state='NONTERMINAL_CHECKPOINT',scope='ALL connected simple cubic graph isomorphism types of orders 4,6,8; ALL D/U choices and A-color orbits, ALL B phases. No claim beyond this finite domain.',graphs=reports,totals={k:sum(r[k] for r in reports) for k in ('states','raw_frames','phase_trials','positive_blocks','unreachable')},mutation_count=audit['mutations'],primary_certificate_sha256=audit['certificate_sha256'],canonicalization='No graph quotient inside a fixed graph; only global A color permutations on preframes. Zero/U is fixed. Phase bits are exhaustively optimized. Parent chains lift by completing the partial A-label bijection.' ,outputs='Each graph .states contains code mu phase parent distance block; .blocks contains id level size exit-count exit-code lower-code. Every reachable state has a terminating parent chain; all closed block members are listed. Regenerate these exact streams; hashes bind the supplied program/input.',expanded_phase_semantics='Each projected preframe state expands to all its B phases with free phase resets and potential mu(w). Primary singleton therefore expands to four phase states, not one full coloring.')
    (out/'opg37271-c24-summary.json').write_text(json.dumps(summary,sort_keys=True,separators=(',',':'))+'\n')
    rec=dict(verdict='candidate_only',trust_domain='candidate-generation',input_revision='b66703bd76d56f0791ad58542ec8bc7d3b8ee35b',interpreter=platform.python_version(),interpreter_binary_sha256=sha(Path(sys.executable).resolve()),compiler_version=version,compiler_binary_sha256=sha(Path(compiler).resolve()),compiled_program_sha256=sha(out/'c24-space'),sources={s:sha(HERE/s) for s in SOURCES+['opg37271-c24-run.py']},limits=dict(cpu_soft_seconds=35,cpu_hard_seconds=36,wall_seconds_per_child=40,memory_mib=768,file_output_bytes=5242880,stderr_bytes=16384,threads_per_child=1,children_sequential=True),stages=records,outputs={p.name:sha(p) for p in out.glob('opg37271-c24-*.json')},trusted_verifier_run=None,axiom_escape_audit=None)
    (out/'opg37271-c24-execution.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(verdict='candidate_only',totals=summary['totals'],mutations=audit['mutations'],summary_sha256=sha(out/'opg37271-c24-summary.json')),sort_keys=True))
if __name__=='__main__':main()
