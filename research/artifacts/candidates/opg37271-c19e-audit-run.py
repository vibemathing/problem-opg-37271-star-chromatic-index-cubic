"""Run only the fixed C19-E audit, with an outer timeout and bounded receipts."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / 'opg37271-c19e-audit-check.py'
    input_file = here / 'opg37271-c19-phase-certificate.json'
    expected = '9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3'
    if input_file.stat().st_size > 262144 or digest(input_file.read_bytes()) != expected:
        raise ValueError('input digest or size')
    env = os.environ.copy()
    caps = dict(PYTHONHASHSEED='0', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    env.update(caps)
    started = datetime.now(timezone.utc).isoformat()
    t0 = time.monotonic()
    timed_out = False
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen([sys.executable, source.name, input_file.name], cwd=here, env=env, stdout=stdout, stderr=stderr)
        try:
            code = proc.wait(timeout=40)
        except subprocess.TimeoutExpired:
            timed_out = True
            proc.kill()
            code = proc.wait()
        elapsed = time.monotonic() - t0
        stdout.seek(0); out = stdout.read(262145)
        stderr.seek(0); err = stderr.read(262145)
    if len(out) > 262144 or len(err) > 262144:
        raise ValueError('captured output limit')
    result_file = here / 'opg37271-c19e-audit-result.json'
    # Successful output is small JSON. Raw error text is not published.
    if code == 0:
        result = json.loads(out)
        if result['input_sha256'] != expected or result['source_sha256'] != digest(source.read_bytes()):
            raise ValueError('result binding')
        cert = here / 'opg37271-c19e-audit-certificate.json'
        if cert.stat().st_size > 262144 or digest(cert.read_bytes()) != result['certificate_sha256']:
            raise ValueError('certificate binding')
        result_file.write_bytes(out)
    record = dict(verdict='candidate_only', trust_domain='generator', started_at=started,
                  ended_at=datetime.now(timezone.utc).isoformat(), elapsed_seconds=round(elapsed,6),
                  interpreter=dict(implementation=platform.python_implementation(), version=platform.python_version()),
                  command='python3 research/artifacts/candidates/opg37271-c19e-audit-run.py',
                  child_command='python3 opg37271-c19e-audit-check.py opg37271-c19-phase-certificate.json',
                  child_working_directory='research/artifacts/candidates', input_sha256=expected,
                  source_sha256=digest(source.read_bytes()), runner_sha256=digest(Path(__file__).read_bytes()),
                  input_repository_revision='cedbfc277c39317e0d2998733b2d7b45670bac63',
                  exit_code=code, outer_timeout_seconds=40, timed_out=timed_out,
                  child_limits=dict(wall_seconds=35,cpu_soft_seconds=30,cpu_hard_seconds=31,memory_mib=256,file_output_bytes=262144,stdout_bytes=16384,threads=1),
                  environment=caps, stdout_bytes=len(out), stdout_sha256=digest(out), stderr_bytes=len(err), stderr_sha256=digest(err),
                  note='Actual local candidate execution; no trusted verifier, EvidenceLink, kernel or root admission. No historical counts are assumed.')
    encoded = (json.dumps(record,sort_keys=True,indent=2)+'\n').encode()
    if len(encoded) > 16384:
        raise ValueError('execution record limit')
    (here / 'opg37271-c19e-audit-execution.json').write_bytes(encoded)
    print(json.dumps(record,sort_keys=True))
    if code != 0:
        print('audit failed; error byte digest recorded; raw diagnostics retained only locally',file=sys.stderr)
        raise SystemExit(1)
    print(out.decode(),end='')


if __name__ == '__main__':
    main()
