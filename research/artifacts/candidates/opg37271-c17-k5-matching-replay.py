"""No solver imports: replay all 243 constructive C17 colorings by path tests."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import signal


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def reconstruct(index):
    digits=[0]*5
    for i in range(4,-1,-1):
        index,digits[i]=divmod(index,3)
    ports={}
    for v in range(5):
        others=sorted(set(range(5))-{v})
        port_zero=(others[0],others[digits[v]+1])
        for w in others:
            ports[v,w]=2*v+(0 if w in port_zero else 1)
    pairs=[(2*v,2*v+1) for v in range(5)]
    pairs.extend((ports[v,w],ports[w,v]) for v in range(5) for w in range(v+1,5))
    return pairs


def verify_one(index, row):
    demand(type(row) is str and len(row)==10 and set(row)<=set('123456'), 'row format')
    edges=reconstruct(index)
    demand(len(edges)==15 and len(set(map(frozenset,edges)))==15, 'edge size')
    colors=[1,2,3,4,5]+list(map(int,row))
    mat=[[0]*10 for _ in range(10)]
    for (u,v),c in zip(edges,colors):
        demand(u!=v and not mat[u][v], 'simplicity')
        mat[u][v]=mat[v][u]=c
    demand(all(sum(c>0 for c in r)==3 and len(set(r)-{0})==3 for r in mat), 'cubic proper')
    reached={0}
    for _ in range(10):
        reached|={v for u in reached for v,c in enumerate(mat[u]) if c}
    demand(len(reached)==10,'connected')
    conflicts={tuple(sorted((u//2,v//2))) for u,v in edges[5:]}
    demand(conflicts==set(itertools.combinations(range(5),2)), 'K5 matching conflict')
    path_count=0
    for a,b,c,d,e in itertools.permutations(range(10),5):
        t0,t1,t2,t3=mat[a][b],mat[b][c],mat[c][d],mat[d][e]
        if t0 and t1 and t2 and t3:
            path_count+=1
            demand(t0!=t2 or t1!=t3, 'alternating four-edge simple path')
    cycle_count=0
    for a,b,c,d in itertools.permutations(range(10),4):
        t0,t1,t2,t3=mat[a][b],mat[b][c],mat[c][d],mat[d][a]
        if t0 and t1 and t2 and t3:
            cycle_count+=1
            demand(t0!=t2 or t1!=t3, 'alternating four-cycle')
    return path_count,cycle_count


def validate_header(data):
    demand(data.get('cases')==243, 'case count')
    demand(data.get('matching_colors')==[1,2,3,4,5], 'matching colors')
    rows=data.get('complement_colors_by_index')
    demand(type(rows) is list and len(rows)==243, 'complete case table')
    return rows


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall limit')))
    signal.alarm(30)
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    here=Path(__file__).parent
    source=here/'opg37271-c17-k5-matching-certificate.json'
    raw=source.read_bytes(); demand(len(raw)<=262144,'input size')
    data=json.loads(raw); rows=validate_header(data)
    total_paths=total_cycles=0
    for index,row in enumerate(rows):
        p,c=verify_one(index,row); total_paths+=p; total_cycles+=c
    mutations=[]
    tests=[('missing_case',lambda: validate_header({**data,'complement_colors_by_index':rows[:-1]})),
           ('outside_palette',lambda: verify_one(0,'7'+rows[0][1:])),
           ('improper_color',lambda: verify_one(0,'1'+rows[0][1:])),
           ('short_row',lambda: verify_one(0,rows[0][:-1]))]
    for label,test in tests:
        try: test()
        except ValueError as exc: mutations.append({'mutation':label,'rejected_by':str(exc)})
        else: raise ValueError('mutation was accepted: '+label)
    out={'verdict':'candidate_only','scope':'solver-free generator-side replay, not a trusted verifier receipt',
         'runtime':platform.python_version(),'cases_replayed':243,
         'input_sha256':hashlib.sha256(raw).hexdigest(),
         'replay_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'oriented_simple_four_edge_paths_tested':total_paths,
         'oriented_four_cycles_tested':total_cycles,
         'all_connected_simple_cubic':True,'all_matching_conflict_K5':True,
         'all_supplied_colorings_star_six':True,'mutation_tests':mutations,
         'budgets':{'wall_seconds':30,'cpu_seconds':30,'memory_mib':512,'threads':1}}
    text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n'
    demand(len(text.encode())<=65536,'output size')
    (here/'opg37271-c17-k5-matching-replay-result.json').write_text(text)
    print(text,end='')


if __name__=='__main__': main()
