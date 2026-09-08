"""Bounded local reproduction; no repository governance or trusted gate actions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
LIMITS = {'wall_seconds':35,'cpu_soft_seconds':30,'cpu_hard_seconds':31,
          'memory_bytes':805306368,'file_bytes':1048576,
          'stdout_bytes':65536,'stderr_bytes':16384,'threads':1}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30,31))
    resource.setrlimit(resource.RLIMIT_AS, (805306368,805306368))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1048576,1048576))
    os.environ['OMP_NUM_THREADS'] = '1'


def run():
    sources = sorted(HERE.glob('opg37271-c28-*.py'))
    before = {p.name:sha(p) for p in sources}
    began = datetime.now(timezone.utc).isoformat(); stages = []
    for stem in ('produce','check'):
        script = 'opg37271-c28-'+stem+'.py'
        out = HERE/('opg37271-c28-'+stem+'.stdout.txt')
        err = HERE/('opg37271-c28-'+stem+'.stderr.txt')
        start = datetime.now(timezone.utc).isoformat(); t = time.monotonic(); timed_out = False
        with out.open('wb') as o, err.open('wb') as e:
            try:
                process = subprocess.run([sys.executable,script],cwd=HERE,stdout=o,stderr=e,
                                         timeout=35,preexec_fn=limits,check=False)
                code = process.returncode
            except subprocess.TimeoutExpired:
                code = None; timed_out = True
        record = {'stage':stem,'command':['python3','research/artifacts/candidates/'+script],
                  'started_at':start,'ended_at':datetime.now(timezone.utc).isoformat(),
                  'elapsed_seconds':round(time.monotonic()-t,6),'exit_code':code,'timed_out':timed_out,
                  'stdout_bytes':out.stat().st_size,'stderr_bytes':err.stat().st_size,
                  'stdout_sha256':sha(out),'stderr_sha256':sha(err)}
        record['output_limit_exceeded'] = record['stdout_bytes']>65536 or record['stderr_bytes']>16384
        stages.append(record)
        if code!=0 or timed_out or record['output_limit_exceeded']:
            break
    after = {p.name:sha(p) for p in sources}
    products = ['opg37271-c28-input.json','opg37271-c28-certificate-binding.json',
                'opg37271-c28-certificate.json','opg37271-c28-check-result.json']
    receipt = {'schema_version':'c28-execution-1','verdict':'candidate_only','best_verified_result':'none',
               'input_revision':'69b475b0ce24540775d0f0149d446212415146b0',
               'started_at':began,'ended_at':datetime.now(timezone.utc).isoformat(),
               'interpreter':{'implementation':platform.python_implementation(),'version':platform.python_version(),
                              'binary_sha256':sha(Path(sys.executable))},
               'limits':LIMITS,'stages':stages,'source_sha256':before,'sources_unchanged':before==after,
               'files_sha256':{name:sha(HERE/name) for name in products if (HERE/name).exists()},
               'completed':len(stages)==2 and before==after and all(z['exit_code']==0 and not z['timed_out'] and not z['output_limit_exceeded'] for z in stages),
               'trusted_execution':False,
               'scope':'Exact ten-vertex interface; complete stated endpoint families and all phases; exhaustive exact-pattern realizability below ten. No repeated ten-vertex full-frame census or trusted mathematical workflow.'}
    (HERE/'opg37271-c28-execution.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'verdict':'candidate_only','completed':receipt['completed'],'stages':stages},sort_keys=True))
    if not receipt['completed']:
        raise SystemExit(1)


if __name__ == '__main__':
    run()
