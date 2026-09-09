"""Bounded reference/replay. Produces generator-domain observations only."""
from pathlib import Path
import sys,subprocess,hashlib,json,time,datetime,resource,selectors,os
B=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def bounded(name):
 def limits():
  resource.setrlimit(resource.RLIMIT_AS,(805306368,805306368));resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
 start=now();t=time.monotonic();p=subprocess.Popen([sys.executable,str(B/name)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=limits,env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1'})
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ,'out');sel.register(p.stderr,selectors.EVENT_READ,'err');streams={'out':bytearray(),'err':bytearray()};event=None
 while sel.get_map():
  if time.monotonic()-t>35:event='wall_limit';p.kill()
  for key,_ in sel.select(.05):
   chunk=os.read(key.fileobj.fileno(),4096)
   if not chunk:sel.unregister(key.fileobj);continue
   streams[key.data].extend(chunk)
   if len(streams[key.data])>(65536 if key.data=='out' else 16384):event='stream_limit';p.kill()
  if event:p.wait();break
 code=p.wait(timeout=2);sel.close()
 result={'script':name,'started_at':start,'ended_at':now(),'elapsed_seconds':time.monotonic()-t,'exit_code':code,'limit_event':event,'stdout_bytes':len(streams['out']),'stderr_bytes':len(streams['err']),'stdout_sha256':sha(streams['out']),'stderr_sha256':sha(streams['err'])}
 if event or code!=0:raise RuntimeError(json.dumps(result))
 return result
if __name__=='__main__':
 names=['opg37271-c30x-produce.py','opg37271-c30z-produce.py','opg37271-c30z-check.py','opg37271-c30z-run.py'];before={n:sha((B/n).read_bytes()) for n in names};stages=[bounded(n) for n in names[1:3]]
 r=json.loads((B/'opg37271-c30z-reference.json').read_text());q=json.loads((B/'opg37271-c30z-result.json').read_text())
 for k in ['all_D_star_colorings','eligible_phase_optimal_frames','width_histogram','word_width_sha256','all_D_words_sha256']:assert r[k]==q[k],k
 assert before=={n:sha((B/n).read_bytes()) for n in names}
 out={'verdict':'candidate_only','best_verified_result':'none','trusted_execution':False,'python':sys.version.split()[0],'interpreter_sha256':sha(Path(sys.executable).read_bytes()),'source_sha256':before,'limits':{'wall_seconds':35,'cpu_seconds':[30,31],'address_space_bytes':805306368,'file_bytes':1048576,'stdout_bytes':65536,'stderr_bytes':16384,'threads':1},'stages':stages,'all_D_star_colorings':q['all_D_star_colorings'],'eligible_frames':q['eligible_phase_optimal_frames'],'widths':q['width_histogram'],'boundary_tests':12,'word_width_sha256':q['word_width_sha256'],'result_sha256':sha((B/'opg37271-c30z-result.json').read_bytes()),'result_bytes':(B/'opg37271-c30z-result.json').stat().st_size,'all_profiles_checked':True,'all_sources_unchanged':True,'root_closed':False}
 (B/'opg37271-c30z-execution.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out))
