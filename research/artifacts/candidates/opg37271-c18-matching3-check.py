"""Bounded constructive audit: specified strong 3-colored perfect matching."""
from __future__ import annotations
import hashlib
import base64
import zlib
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def need(b, msg):
    if not b:
        raise ValueError(msg)


def cycle_word(n):
    need(n >= 3 and n != 5, 'cycle length')
    s = (0, 1, 2)[n % 3]
    r = (n - 4*s)//3
    need(r >= 0 and 3*r+4*s == n, 'block decomposition')
    return [4,5,6]*r + [4,5,4,6]*s


def construct(n, edges, matching_colors):
    m=len(matching_colors)
    need(len(set(map(frozenset,edges)))==len(edges), 'simple edges')
    at=[[] for _ in range(n)]; lam=[0]*n; out=[0]*len(edges)
    for e,(u,v) in enumerate(edges):
        need(0<=u<n and 0<=v<n and u!=v, 'endpoints')
        at[u].append((v,e)); at[v].append((u,e))
        if e<m:
            a=matching_colors[e]
            need(a in (1,2,3) and not lam[u] and not lam[v], 'matching')
            lam[u]=lam[v]=a; out[e]=a
    need(all(lam) and all(len(ns)<=3 for ns in at), 'perfect subcubic')
    F=[[(v,e) for v,e in ns if e>=m] for ns in at]
    need(all(lam[u]!=lam[v] for u,v in edges[m:]), 'conflict three-coloring')
    seen=set(); specials=[]
    for start in range(n):
        if start in seen: continue
        comp={start}; todo=[start]
        while todo:
            u=todo.pop()
            for v,_ in F[u]:
                if v not in comp: comp.add(v); todo.append(v)
        seen|=comp
        ends=[v for v in comp if len(F[v])<2]
        root=min(ends or comp); vs=[root]; es=[]; previous=None; u=root
        while True:
            nxt=[(v,e) for v,e in F[u] if e!=previous]
            if not nxt: break
            v,e=min(nxt)
            es.append(e)
            if v==root: break
            need(v not in vs, 'component traversal')
            vs.append(v); previous=e; u=v
        if ends:
            for j,e in enumerate(es): out[e]=4+j%3
        elif len(es)!=5:
            for e,c in zip(es,cycle_word(len(es))): out[e]=c
        else:
            rare=[a for a in (1,2,3) if sum(lam[v]==a for v in vs)==1]
            need(len(rare)==1, 'five-cycle rare color')
            a=rare[0]; p=next(j for j,v in enumerate(vs) if lam[v]==a)
            j=(p+2)%5; out[es[j]]=a; specials.append(es[j])
            need(all(lam[vs[(p+t)%5]]!=a for t in (1,2,3,4)), 'safe four vertices')
            for t,c in enumerate((4,5,6,4),1): out[es[(j+t)%5]]=c
    need(all(out), 'uncolored edge')
    return out,specials


def direct_check(n,edges,colors):
    # Deliberately does not invoke the construction or its special-edge rules.
    at=[[] for _ in range(n)]
    need(len(colors)==len(edges), 'color length')
    for (u,v),c in zip(edges,colors):
        need(1<=c<=6, 'palette')
        at[u].append((v,c)); at[v].append((u,c))
    need(all(len(ns)==len({c for _,c in ns}) for ns in at), 'properness')
    for a,b in it.combinations(range(1,7),2):
        seen=set()
        for v in range(n):
            if v in seen: continue
            todo=[v]; seen.add(v); deg=nv=0
            while todo:
                x=todo.pop(); nv+=1
                for y,c in at[x]:
                    if c in (a,b):
                        deg+=1
                        if y not in seen: seen.add(y); todo.append(y)
            ne=deg//2
            need(ne<=3 and (not ne or ne<nv), 'bichromatic component')


def input_graph(perm):
    return [(i,5+perm[i]) for i in range(5)] + [(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+1)%5) for i in range(5)]


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35); resource.setrlimit(resource.RLIMIT_CPU,(35,36))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    words=[w for w in it.product((1,2,3),repeat=5) if all(w[i]!=w[(i+1)%5] for i in range(5))]
    need(len(words)==30, 'proper C5 label count')
    rows=[]; covered=set()
    for pi,perm in enumerate(it.permutations(range(5))):
        E=input_graph(perm)
        for mu in words:
            inverse=[0]*5
            for i,j in enumerate(perm): inverse[j]=mu[i]
            if not all(inverse[i]!=inverse[(i+1)%5] for i in range(5)): continue
            c,S=construct(10,E,list(mu)); need(len(S)==2,'two repairs')
            direct_check(10,E,c)
            rows.append([pi,''.join(map(str,mu)),''.join(map(str,c))]); covered.add(pi)
    # Positive fixtures with all non-five cycle lengths, plus subcubic paths.
    fixture_count=0
    for n in range(3,101):
        E=[(i,n+i) for i in range(n)]+[(i,(i+1)%n) for i in range(n)]+[(n+i,n+(i+1)%n) for i in range(n)]
        mu=[1+i%2 for i in range(n)]
        if n%2: mu[-1]=3
        c,_=construct(2*n,E,mu); direct_check(2*n,E,c); fixture_count+=1
    for n in range(1,31):
        E=[(2*i,2*i+1) for i in range(n)]+[(2*i+1,2*i+2) for i in range(n-1)]
        c,_=construct(2*n,E,[1+i%2 for i in range(n)])
        direct_check(2*n,E,c); fixture_count+=1
    mutations=[]
    for name,fn in [('bad_matching_precolor',lambda: construct(10,input_graph(tuple(range(5))),[1]*5)),
                    ('color_seven',lambda: direct_check(2,[(0,1)],[7]))]:
        try: fn()
        except ValueError as exc: mutations.append([name,str(exc)])
        else: raise ValueError('accepted mutation')
    out={'verdict':'candidate_only','scope':'generator-side finite audit, not trusted verification',
         'runtime':platform.python_version(),'proper_five_cycle_words':len(words),
         'permutations_checked':120,'precolors_per_permutation':243,
         'eligible_graph_precolors':len(rows),'distinct_labeled_eligible_graphs':len(covered),
         'rows_zlib_base64':base64.b64encode(zlib.compress(json.dumps(rows,separators=(',',':')).encode(),9)).decode(),
         'rows_format':'zlib-compressed UTF-8 JSON list of [permutation_index, matching_color_word, full_color_word]',
         'encoding':'permutations(range(5)) lexicographic; M edges (i,5+pi(i)); F first C5 then second C5, cyclic index order',
         'additional_fixtures':fixture_count,'mutations':mutations,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'budgets':{'wall_seconds':35,'cpu_seconds':35,'memory_mib':512,'threads':1}}
    raw=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n'
    need(len(raw.encode())<262144,'output budget')
    Path(__file__).with_name('opg37271-c18-matching3-certificate.json').write_text(raw)
    print(json.dumps({k:out[k] for k in out if k!='rows_zlib_base64'},sort_keys=True))
if __name__=='__main__': main()
