"""Solver-free reconstruction, coverage and simple-path replay of C18 rows."""
import base64
import hashlib
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal
import zlib


def demand(ok,msg):
    if not ok: raise ValueError(msg)


def eligible(perm,mu):
    lab=list(mu)+[0]*5
    for i,p in enumerate(perm): lab[5+p]=mu[i]
    return all(lab[k+i]!=lab[k+(i+1)%5] for k in (0,5) for i in range(5))


def edges(perm):
    return [(i,5+perm[i]) for i in range(5)]+[(i,(i+1)%5) for i in range(5)]+[(5+i,5+(i+1)%5) for i in range(5)]


def check(perm,mu,word):
    demand(type(word) is str and len(word)==15 and set(word)<=set('123456'),'color word')
    c=list(map(int,word)); demand(c[:5]==list(mu),'matching retention')
    E=edges(perm); demand(len(set(map(frozenset,E)))==15,'simplicity')
    adj=[[] for _ in range(10)]
    for (u,v),a in zip(E,c): adj[u].append((v,a)); adj[v].append((u,a))
    demand(all(len(x)==3 and len({a for _,a in x})==3 for x in adj),'cubic proper')
    counts=[0,0]
    def walk(vs,cs):
        u=vs[-1]
        if len(cs)==4:
            counts[0]+=1
            demand(cs[0]!=cs[2] or cs[1]!=cs[3],'bad four-edge path')
            return
        for v,a in adj[u]:
            if v not in vs: walk(vs+[v],cs+[a])
            elif len(cs)==3 and v==vs[0]:
                counts[1]+=1
                demand(cs[0]!=cs[2] or cs[1]!=a,'bad four-cycle')
    for v in range(10): walk([v],[])
    return counts


def validate(rows):
    perms=list(it.permutations(range(5))); expect=set()
    for i,p in enumerate(perms):
        for mu in it.product((1,2,3),repeat=5):
            if eligible(p,mu): expect.add((i,''.join(map(str,mu))))
    actual=set(); paths=cycles=0
    for i,m,w in rows:
        demand(type(i) is int and 0<=i<120 and type(m) is str and len(m)==5 and set(m)<=set('123'),'row key')
        key=(i,m); demand(key not in actual and key in expect,'coverage key')
        actual.add(key); p,q=check(perms[i],tuple(map(int,m)),w); paths+=p; cycles+=q
    demand(actual==expect,'complete coverage')
    return len(actual),paths,cycles


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35); resource.setrlimit(resource.RLIMIT_CPU,(35,36))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    here=Path(__file__).parent; p=here/'opg37271-c18-matching3-certificate.json'
    raw=p.read_bytes(); demand(len(raw)<262144,'input size')
    obj=json.loads(raw); dec=zlib.decompressobj()
    unpacked=dec.decompress(base64.b64decode(obj['rows_zlib_base64'],validate=True),262145)
    demand(len(unpacked)<=262144 and dec.eof and not dec.unconsumed_tail and not dec.unused_data,'decompression size')
    rows=json.loads(unpacked); n,p4,c4=validate(rows)
    mutations=[]
    tests=[('missing_row',lambda: validate(rows[:-1])),
           ('duplicate_row',lambda: validate(rows+[rows[0]])),
           ('outside_palette',lambda: check(list(it.permutations(range(5)))[rows[0][0]],tuple(map(int,rows[0][1])),'7'+rows[0][2][1:]))]
    for name,test in tests:
        try: test()
        except ValueError as ex: mutations.append([name,str(ex)])
        else: raise ValueError('accepted mutation')
    out={'verdict':'candidate_only','scope':'generator-domain replay, no trusted receipt',
         'runtime':platform.python_version(),'cases':n,'oriented_four_edge_paths':p4,'oriented_four_cycles':c4,
         'input_sha256':hashlib.sha256(raw).hexdigest(),
         'replay_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'mutation_rejections':mutations,
         'budgets':{'wall_seconds':35,'cpu_seconds':35,'memory_mib':512,'threads':1}}
    text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n'
    (here/'opg37271-c18-matching3-replay-result.json').write_text(text)
    print(text,end='')
if __name__=='__main__': main()
