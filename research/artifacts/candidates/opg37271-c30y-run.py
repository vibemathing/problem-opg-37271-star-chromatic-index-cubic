"""Reproduce only the order-eleven extension with per-process hard bounds.
No workflow dispatch or mathematical admission. Use a disposable POSIX checkout.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,resource,selectors,subprocess,sys,time
BASE=Path(__file__).resolve().parent
LIMITS={'wall_seconds':35,'cpu_seconds':[30,31],'memory_bytes':805306368,'file_bytes':1048576,'stdout_bytes':65536,'stderr_bytes':16384,'threads':1,'total_wall_seconds':1800}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def caps():
 resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(805306368,805306368));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
def execute(script,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic();out=bytearray();err=bytearray();reason=None
 p=subprocess.Popen([sys.executable,'-B',str(BASE/script),*args],cwd=BASE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=caps,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,('stdout',out,65536));sel.register(p.stderr,selectors.EVENT_READ,('stderr',err,16384))
 while sel.get_map():
  if time.monotonic()-clock>35 and reason is None:reason='wall_timeout';p.kill()
  for key,_ in sel.select(0.1):
   name,buf,cap=key.data;data=os.read(key.fd,4096)
   if not data:sel.unregister(key.fileobj);continue
   if len(buf)+len(data)>cap:
    if reason is None:reason=name+'_limit';p.kill()
    data=data[:max(0,cap-len(buf))]
   buf.extend(data)
 p.wait();sel.close()
 rec={'script':script,'arguments':args,'source_sha256':digest(BASE/script),'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-clock,'exit_code':p.returncode,'limit_event':reason,'stdout_bytes':len(out),'stderr_bytes':len(err),'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()}
 return rec,bytes(out),bytes(err)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--mutations-only',action='store_true');args=parser.parse_args()
 sources={p.name:digest(p) for p in BASE.glob('opg37271-c30[xy]-*.py')}
 record={'verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,'limits':LIMITS,'python':platform.python_version(),'implementation':platform.python_implementation(),'interpreter_sha256':digest(Path(sys.executable)),'source_sha256':sources,'stages':[]}
 driver='opg37271-c30y-enumerate.py'
 jobs=[]
 if not args.mutations_only:
  jobs.extend((driver,['case',str(k)]) for k in range(32));jobs.append((driver,['catalog']))
  jobs.extend((driver,['batch',str(k),str(k+8)]) for k in range(0,315,8))
  jobs.extend((driver,['check_case',str(k)]) for k in range(32))
  jobs.extend((driver,['check_batch',str(k)]) for k in range(0,315,8))
 jobs.append(('opg37271-c30y-mutations.py',[]));beg=time.monotonic()
 log=BASE/('opg37271-c30y-mutation-execution.json' if args.mutations_only else 'opg37271-c30y-reproduction.json')
 for script,argv in jobs:
  if time.monotonic()-beg>=1800:record['total_limit_hit']=True;break
  rec,out,err=execute(script,argv);record['stages'].append(rec)
  record['sources_unchanged']=all(digest(BASE/name)==h for name,h in sources.items())
  log.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
  if rec['exit_code'] or rec['limit_event'] or not record['sources_unchanged']:
   print(json.dumps({'state':'NONTERMINAL_CHECKPOINT','failed_stage':rec}));return 1
 record['completed']=len(record['stages'])==len(jobs);log.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
 print(json.dumps({'verdict':'candidate_only','stages':len(record['stages']),'completed':record['completed']}));return 0 if record['completed'] else 1
if __name__=='__main__':raise SystemExit(main())
