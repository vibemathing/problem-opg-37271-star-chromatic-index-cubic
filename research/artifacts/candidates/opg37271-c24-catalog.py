"""Exhaust all rooted labelled connected simple cubic graphs of orders 4,6,8.
No external graph catalogue. Candidate calculation, not a trusted receipt.
"""
from itertools import combinations,permutations
from pathlib import Path
import json,hashlib

def catalog(n):
    adj=[set() for _ in range(n)]
    for v in (1,2,3):adj[0].add(v);adj[v].add(0)
    representatives=[];counts=[];labelled=disconnected=0
    def equivalent(A,B):
        # Isomorphism maps A's root to any vertex, then its three neighbors
        # to that vertex's neighbors and all other vertices bijectively.
        for r in range(n):
            for ns in permutations(sorted(B[r])):
                rest=sorted(set(range(n))-{r}-set(ns))
                for tail in permutations(rest):
                    p=(r,)+ns+tail
                    if all(p[v] in B[p[u]] for u in range(n) for v in A[u] if v>u):return True
        return False
    def finish():
        nonlocal labelled,disconnected
        labelled+=1;seen={0};todo=[0]
        while todo:
            for w in adj[todo.pop()]:
                if w not in seen:seen.add(w);todo.append(w)
        if len(seen)<n:disconnected+=1;return
        for i,A in enumerate(representatives):
            if equivalent(adj,A):counts[i]+=1;return
        representatives.append([set(x) for x in adj]);counts.append(1)
    def build(v):
        if v==n:
            if all(len(x)==3 for x in adj):finish()
            return
        need=3-len(adj[v]);avail=[w for w in range(v+1,n) if len(adj[w])<3]
        if need<0 or need>len(avail):return
        for choice in combinations(avail,need):
            for w in choice:adj[v].add(w);adj[w].add(v)
            # Remaining deficiency cannot exceed later eligible vertices.
            if all(3-len(adj[u]) <= sum(w!=u and w not in adj[u] and len(adj[w])<3 for w in range(v+1,n)) for u in range(v+1,n)):
                build(v+1)
            for w in choice:adj[v].remove(w);adj[w].remove(v)
    build(1)
    rows=[dict(n=n,edges=[[u,v] for u in range(n) for v in sorted(A[u]) if u<v],rooted_labelled_count=c) for A,c in zip(representatives,counts)]
    return dict(n=n,root_neighbors=[1,2,3],rooted_labelled_graphs=labelled,disconnected=disconnected,representatives=rows)

if __name__=='__main__':
    out=dict(verdict='candidate_only',orders=[catalog(n) for n in (4,6,8)],normalization='vertex 0 neighbors exactly 1,2,3; exact isomorphism check tests root image, neighbor permutations, all remaining permutations')
    p=Path(__file__).with_name('opg37271-c24-catalog.json');p.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    for row in out['orders']: print(row['n'],row['rooted_labelled_graphs'],row['disconnected'],len(row['representatives']))
