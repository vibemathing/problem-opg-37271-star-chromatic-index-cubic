"""Bounded constructive certificates for all 243 split-K5 cubic matching inputs."""
from __future__ import annotations
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def require(b,msg):
    if not b: raise ValueError(msg)


def graph(digits):
    # Each K5 vertex i is split into 2i,2i+1 joined by matching edge i.
    side={}
    for i,d in enumerate(digits):
        ns=[j for j in range(5) if j!=i]
        pair={ns[0],ns[d+1]}
        for j in ns: side[i,j]=int(j not in pair)
    return [(2*i,2*i+1) for i in range(5)]+[(2*i+side[i,j],2*j+side[j,i]) for i,j in it.combinations(range(5),2)]


def constraints(E):
    at=[[] for _ in range(10)]
    for e,(x,y) in enumerate(E):
        at[x].append((y,e)); at[y].append((x,e))
    adjacent=[set() for _ in E]
    for ns in at:
        for (_,e),(_,f) in it.combinations(ns,2): adjacent[e].add(f); adjacent[f].add(e)
    paths=set()
    def visit(start,vs,es):
        if len(es)==4:
            paths.add(min(tuple(es),tuple(reversed(es)))); return
        for w,e in at[vs[-1]]:
            if w not in vs or (len(es)==3 and w==start):
                visit(start,vs+[w],es+[e])
    for v in range(10): visit(v,[v],[])
    containing=[[] for _ in E]
    for p in paths:
        for e in p: containing[e].append(p)
    return adjacent,containing


def solve(E):
    adjacent,containing=constraints(E); c=list(range(1,6))+[0]*10; nodes=0
    def domain(e):
        out=[]
        forbidden={c[f] for f in adjacent[e]}
        for z in range(1,7):
            if z in forbidden: continue
            c[e]=z
            if not any(c[p[0]] and c[p[1]] and c[p[2]] and c[p[3]]
                       and c[p[0]]==c[p[2]] and c[p[1]]==c[p[3]] for p in containing[e]):
                out.append(z)
        c[e]=0
        return out
    def dfs():
        nonlocal nodes
        nodes+=1
        require(nodes<=2000000,'per-case node budget')
        best=None; colors=None
        for e in range(5,15):
            if c[e]: continue
            ds=domain(e)
            if not ds: return False
            if colors is None or len(ds)<len(colors): best,colors=e,ds
        if best is None: return True
        for z in colors:
            c[best]=z
            if dfs(): return True
            c[best]=0
        return False
    ok=dfs()
    return c.copy() if ok else None,nodes


def check(E,c):
    # Different check: monochromatic degree followed by ALL two-color components.
    adj=[[] for _ in range(10)]
    require(len(E)==15 and len(set(map(frozenset,E)))==15,'simple size')
    for (x,y),z in zip(E,c):
        require(x!=y and 1<=z<=6,'edge or color')
        adj[x].append((y,z)); adj[y].append((x,z))
    require(all(len(n)==3 and len({c for _,c in n})==3 for n in adj),'cubic proper')
    for a,b in it.combinations(range(1,7),2):
        seen=set()
        for v in range(10):
            if v in seen: continue
            todo=[v]; seen.add(v); ne=0; nv=0
            while todo:
                x=todo.pop(); nv+=1
                for y,z in adj[x]:
                    if z not in (a,b): continue
                    ne+=1
                    if y not in seen: seen.add(y); todo.append(y)
            ne//=2
            require(ne<=3 and (not ne or ne<nv),'bad two-color component')


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(30); resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    rows=[]; counts=[]
    for ds in it.product(range(3),repeat=5):
        E=graph(ds); c,n=solve(E); require(c is not None,'fixed distinct matching did not extend')
        check(E,c); rows.append(''.join(map(str,c[5:]))); counts.append(n)
    require(len(rows)==243,'coverage')
    result={'verdict':'candidate_only','runtime':platform.python_version(),
      'scope':'generator-side complete finite constructive certificate, not a trusted receipt',
      'budgets':{'wall_seconds':30,'cpu_seconds':30,'memory_mib':512,'threads':1,'per_case_nodes':2000000},
      'case_order':'lexicographic ternary digits d0,...,d4; index=sum(di*3**(4-i))',
      'vertices':'0,...,9; matching edge i joins 2i and 2i+1',
      'partition':'At i sort the four other labels ns; side 0 gets ns[0] and ns[di+1], side 1 the other two.',
      'edge_order':'first five matching edges, then ten K5 pairs (i,j) lexicographically; endpoint at i is 2i+side_i(j)',
      'matching_colors':[1,2,3,4,5],
      'complement_colors_by_index':rows,'cases':len(rows),'total_search_nodes':sum(counts),'max_search_nodes':max(counts)}
    text=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    require(len(text.encode())<262144,'output budget')
    Path(__file__).with_name('opg37271-c17-k5-matching-certificate.json').write_text(text)
    print(json.dumps({k:result[k] for k in ('runtime','cases','total_search_nodes','max_search_nodes')}))

if __name__=='__main__': main()
