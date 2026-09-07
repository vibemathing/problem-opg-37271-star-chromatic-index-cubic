"""Bounded candidate replay or read-only admission preflight. Never signs evidence."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LIMIT = 262144

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bounded_write(path, obj):
    data = (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()
    if len(data) > LIMIT:
        raise ValueError('bounded JSON output exceeded')
    path.write_bytes(data)

def preflight():
    request_path = HERE / 'opg37271-c20-admission-request.json'
    request = json.loads(request_path.read_text())
    defects = []
    for entry in request['frozen_files']:
        path = ROOT / entry['path']
        if not path.is_file() or digest(path) != entry['sha256']:
            defects.append('request file mismatch: ' + entry['path'])
    statement = json.loads((HERE / 'opg37271-c20-statement.json').read_text())
    ids = []
    graphfile = ROOT / 'research/records/obligation-graphs.jsonl'
    if graphfile.exists():
        for line in graphfile.read_text().splitlines():
            if line.strip():
                for ob in json.loads(line).get('obligations', []):
                    if ob.get('statement_sha256') == statement['primary_statement_sha256']:
                        ids.append(ob['obligation_id'])
    if not graphfile.exists():
        defects.append('obligation ledger unavailable in this checkout')
    elif not ids:
        defects.append('no admitted obligation matching the exact C20 local statement')
    candidatefile = ROOT / 'research/records/candidate-artifacts.jsonl'
    registered = []
    if candidatefile.exists():
        registered = [json.loads(line).get('candidate_id') for line in candidatefile.read_text().splitlines() if line.strip()]
    if not candidatefile.exists():
        defects.append('candidate ledger unavailable in this checkout')
    elif request['candidate_id'] not in registered:
        defects.append('candidate absent from trusted candidate records')
    registry = ROOT / 'research/verifiers.json'
    principals = {}
    if registry.exists():
        principals = {p['id']:p for p in json.loads(registry.read_text()).get('principals',[])}
    if not registry.exists():
        defects.append('verifier registry unavailable in this checkout')
    for name in request['proposed_verifier_ids']:
        if not principals.get(name,{}).get('toolchain_allowlist'):
            defects.append('no toolchain allowlist for ' + name)
    # No arbitrary shell command or workflow dispatch is executed here.
    if request['formal_source'] is None:
        defects.append('faithful Lean translation and exact declaration remain pending')
    if request['permitted_verifier_workflow'] is None:
        defects.append('no permitted mathematical-verifier workflow in frozen repository')
    out = dict(verdict='candidate_only',status='admission_request_pending',
               request_sha256=digest(request_path),matching_obligation_ids=ids,missing_gates=defects,
               executed_verifier=False,workflow_run=None,toolchain_fingerprint=None,
               axiom_escape_audit='pending_no_formal_source',truth_files_written=False)
    bounded_write(HERE/'opg37271-c20-admission-preflight.json',out)
    print(json.dumps(out,sort_keys=True))
    return 2 if defects else 0

def child_limits():
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(LIMIT,)*2)

def replay():
    env = os.environ.copy()
    env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONHASHSEED='0')
    start, clock = datetime.now(timezone.utc).isoformat(), time.monotonic()
    timed_out = False
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        proc = subprocess.Popen([sys.executable,'opg37271-c20-test.py'],cwd=HERE,env=env,
                                stdout=out,stderr=err,preexec_fn=child_limits)
        try:
            code=proc.wait(timeout=40)
        except subprocess.TimeoutExpired:
            timed_out=True;proc.kill();code=proc.wait(timeout=5)
        out.seek(0);stdout=out.read(LIMIT+1)
        err.seek(0);stderr=err.read(LIMIT+1)
    if len(stdout)>16384 or len(stderr)>16384:
        raise ValueError('stdout/stderr budget exceeded')
    (HERE/'opg37271-c20-result.json').write_bytes(stdout if code==0 else b'{}\n')
    inputs=['opg37271-c19-phase-certificate.json','opg37271-c20-core.py','opg37271-c20-test.py','opg37271-c20-run.py']
    record=dict(verdict='candidate_only',command='python3 research/artifacts/candidates/opg37271-c20-run.py',
                input_revision='ddc49c1978a196490702150bb75264793a658457',
                started_at=start,ended_at=datetime.now(timezone.utc).isoformat(),
                elapsed_seconds=round(time.monotonic()-clock,6),exit_code=code,timed_out=timed_out,
                interpreter=dict(implementation=platform.python_implementation(),version=platform.python_version()),
                interpreter_binary_sha256=digest(Path(sys.executable).resolve()),
                source_hashes={p:digest(HERE/p) for p in inputs},
                stdout_sha256=hashlib.sha256(stdout).hexdigest(),stdout_bytes=len(stdout),
                stderr_sha256=hashlib.sha256(stderr).hexdigest(),stderr_bytes=len(stderr),
                limits=dict(outer_seconds=40,wall_seconds=35,cpu_soft_seconds=30,cpu_hard_seconds=31,
                            memory_mib=256,threads=1,file_output_bytes=LIMIT,stdout_bytes=16384,stderr_bytes=16384),
                local_tools=dict(lean_found=shutil.which('lean') is not None or (Path.home()/'.elan/bin/lean').is_file(),
                                 lake_found=shutil.which('lake') is not None or (Path.home()/'.elan/bin/lake').is_file()),
                trusted_execution=False,axiom_escape_audit='pending_no_formal_source',
                note='Actual generator-domain run. No registered adapter, mathematical workflow, Evidence or Result operation.')
    if code==0:
        record['certificate_sha256']=digest(HERE/'opg37271-c20-certificate.json')
    bounded_write(HERE/'opg37271-c20-execution.json',record)
    print(stdout.decode('utf-8'),end='')
    if stderr:
        # Do not mirror potentially unsanitized process diagnostics.
        print(json.dumps({'stderr_bytes':len(stderr),'stderr_sha256':record['stderr_sha256']}))
    return code

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--admission-preflight',action='store_true')
    args=parser.parse_args()
    sys.exit(preflight() if args.admission_preflight else replay())
