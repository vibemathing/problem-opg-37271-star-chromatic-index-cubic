"""Bounded C27 replay in an isolated temporary working directory.
Produces generator-domain observations, not a trusted verifier receipt.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
PREFIX = 'opg37271-c27-'
LIMITS = dict(wall_seconds=35, cpu_soft_seconds=30, cpu_hard_seconds=31,
              memory_bytes=768*1024**2, file_bytes=1024**2,
              stdout_bytes=65536, stderr_bytes=16384, threads=1)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def child_limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 31))
    resource.setrlimit(resource.RLIMIT_AS, (LIMITS['memory_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMITS['file_bytes'],)*2)


def main():
    names = [PREFIX+x for x in ('input.json', 'certificate.json', 'produce.py', 'check.py')]
    for name in names:
        if not (HERE/name).is_file() or (HERE/name).stat().st_size > LIMITS['file_bytes']:
            raise ValueError('missing or oversized input: '+name)
    report = dict(schema_version='c27-execution-1', verdict='candidate_only',
                  best_verified_result='none', trusted_execution=False,
                  started_at=now(), limits=LIMITS,
                  toolchain=dict(python=platform.python_version(),
                                 implementation=platform.python_implementation(),
                                 interpreter_sha256=digest(Path(sys.executable)),
                                 dependencies='Python standard library only'),
                  frozen_sources={n:digest(HERE/n) for n in names+[PREFIX+'run.py']},
                  stages=[], outputs={}, root_closed=False)
    ok = True
    with tempfile.TemporaryDirectory(prefix='c27-replay-') as temp:
        work = Path(temp)
        for name in names:
            shutil.copyfile(HERE/name, work/name)
        for name in ('produce.py', 'check.py'):
            stage = dict(name=name, command=['python3', PREFIX+name], started_at=now())
            start = time.monotonic()
            with (work/'stdout.txt').open('wb') as out, (work/'stderr.txt').open('wb') as err:
                try:
                    completed = subprocess.run([sys.executable, str(work/(PREFIX+name))],
                        cwd=work, stdout=out, stderr=err, timeout=LIMITS['wall_seconds'],
                        preexec_fn=child_limits, check=False)
                    stage.update(exit_code=completed.returncode, timeout=False)
                except subprocess.TimeoutExpired:
                    stage.update(exit_code=None, timeout=True)
            stage.update(ended_at=now(), elapsed_seconds=round(time.monotonic()-start,6))
            for label in ('stdout','stderr'):
                p = work/(label+'.txt')
                stage[label+'_bytes'] = p.stat().st_size
                stage[label+'_sha256'] = digest(p)
            stage['output_limit_exceeded'] = any(stage[k+'_bytes']>LIMITS[k+'_bytes'] for k in ('stdout','stderr'))
            report['stages'].append(stage)
            if stage['exit_code'] != 0 or stage['timeout'] or stage['output_limit_exceeded']:
                ok = False
                break
        if ok:
            for suffix in ('expanded.json', 'certificate-replay.json', 'check-result.json'):
                p=work/(PREFIX+suffix)
                if not p.is_file() or p.stat().st_size > LIMITS['file_bytes']:
                    raise ValueError('missing or oversized output: '+suffix)
                report['outputs'][PREFIX+suffix] = dict(sha256=digest(p), bytes=p.stat().st_size)
                shutil.copyfile(p, HERE/p.name)
        report.update(ended_at=now(), all_exit_zero=ok,
                      limitation='Same generator trust domain. No C26 core import, Lean, SMT, admission, or closure execution.')
        (HERE/(PREFIX+'execution.json')).write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(verdict='candidate_only',all_exit_zero=ok,
                         execution_sha256=digest(HERE/(PREFIX+'execution.json')),
                         stage_exits=[s['exit_code'] for s in report['stages']]),sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
