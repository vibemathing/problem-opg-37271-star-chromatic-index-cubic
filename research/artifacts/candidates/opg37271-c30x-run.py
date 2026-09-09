"""Bounded, synchronous replay; candidate-only observations, not trusted receipts."""
from pathlib import Path
import datetime,hashlib,json,os,platform,resource,selectors,subprocess,sys,time
HERE=Path(__file__).resolve().parent
LIMITS=dict(wall_seconds=35,cpu_soft_seconds=30,cpu_hard_seconds=31,memory_bytes=768*1024**2,file_bytes=1048576,stdout_bytes=65536,stderr_bytes=16384,threads=1)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def caps():
 resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(LIMITS['memory_bytes'],)*2);resource.setrlimit(resource.RLIMIT_FSIZE,(LIMITS['file_bytes'],)*2)
def stage(name):
 begin=utc();t=time.monotonic();env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 p=subprocess.Popen([sys.executable,str(HERE/name)],cwd=HERE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,preexec_fn=caps)
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'stdout');sel.register(p.stderr,selectors.EVENT_READ,'stderr');buffers={'stdout':bytearray(),'stderr':bytearray()};timeout=False;over=False
 while sel.get_map():
  if time.monotonic()-t>35:timeout=True;p.kill()
  for key,_ in sel.select(.02):
   b=os.read(key.fileobj.fileno(),4096)
   if not b:sel.unregister(key.fileobj);continue
   buffers[key.data].extend(b)
   if len(buffers[key.data])>LIMITS[key.data+'_bytes']:over=True;p.kill()
  if timeout or over:break
 p.wait(timeout=2);sel.close()
 return {'name':name,'command':['python3','research/artifacts/candidates/'+name],'started_at':begin,'ended_at':utc(),'elapsed_seconds':round(time.monotonic()-t,6),'exit_code':p.returncode,'timed_out':timeout,'output_limit_exceeded':over,**{k+'_bytes':len(v) for k,v in buffers.items()},**{k+'_sha256':hashlib.sha256(v).hexdigest() for k,v in buffers.items()}}
def main():
 files=['opg37271-c30x-produce.py','opg37271-c30x-check.py','opg37271-c30x-mutations.py','opg37271-c30x-run.py','opg37271-c30x-input.json'];before={n:digest(HERE/n) for n in files}
 rec={'verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,'state':'NONTERMINAL_CHECKPOINT','source_sha256':before,'input_revision':'3ee4c60c3feb274e60b9a54e430c2d135f77fed8','started_at':utc(),'limits':LIMITS,'interpreter':{'implementation':platform.python_implementation(),'version':platform.python_version(),'binary_sha256':digest(Path(sys.executable))},'stages':[],'preliminary_diagnostics':['Two preliminary complete-checker runs reached CPU limit (exit -24). Residual-degree-feasible passive graph enumeration replaced flat 5^pairs enumeration; final replay is separate.','An initial mutation fixture had h=0 for every boundary and thus could not test omission of nonzero h. A distinct actual nonzero-h fixture was selected; that preliminary test was not counted as a passed mutation.'],'scope':'All exact seven-row, three-U-component realizations of orders8,9,10, including all passive D completions on the fixed vertices; not a general ten-vertex frame census or arbitrary-order embedding theorem.'}
 for name in files[:3]:
  r=stage(name);rec['stages'].append(r)
  if r['exit_code'] or r['timed_out'] or r['output_limit_exceeded']:break
 rec['sources_unchanged']=before=={n:digest(HERE/n) for n in files};rec['ended_at']=utc();rec['completed']=len(rec['stages'])==3 and rec['sources_unchanged'] and all(r['exit_code']==0 and not r['timed_out'] and not r['output_limit_exceeded'] for r in rec['stages'])
 rec['output_sha256']={n:digest(HERE/n) for n in ['opg37271-c30x-certificate.json','opg37271-c30x-check-result.json','opg37271-c30x-mutations.json'] if (HERE/n).exists()}
 (HERE/'opg37271-c30x-execution.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'completed':rec['completed'],'verdict':'candidate_only','stages':rec['stages'],'output_sha256':rec['output_sha256']}))
 sys.exit(0 if rec['completed'] else 1)
if __name__=='__main__':main()
