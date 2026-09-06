"""Bounded generator-side checks for the C15 two-port candidate; stdlib only."""
from __future__ import annotations
import base64
import zlib
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def require(test: bool, message: str) -> None:
    if not test:
        raise ValueError(message)


def star(edges: list[list]) -> bool:
    adj: dict[str, list[tuple[str, int]]] = {}
    seen = set()
    for x,y,c in edges:
        if x == y or frozenset((x,y)) in seen:
            return False
        seen.add(frozenset((x,y)))
        adj.setdefault(x, []).append((y,c)); adj.setdefault(y, []).append((x,c))
    if any(len(ns)>3 or len({c for _,c in ns})!=len(ns) for ns in adj.values()):
        return False
    for a,b in it.combinations(sorted({e[2] for e in edges}),2):
        visited=set()
        for x in adj:
            if x in visited: continue
            todo=[x]; visited.add(x); ne=0; nv=0
            while todo:
                z=todo.pop(); nv+=1
                for w,c in adj[z]:
                    if c not in (a,b): continue
                    ne+=1
                    if w not in visited: visited.add(w); todo.append(w)
            ne//=2
            if ne>3 or (ne and ne>=nv): return False
    return True


def shore(tag: str, palettes: list[list[int]], connector: int) -> list[list]:
    edges=[]
    for i in range(2):
        for j,c in enumerate(palettes[i]):
            edges += [[f'{tag}x{i}',f'{tag}r{i}{j}',c],
                      [f'{tag}r{i}{j}',f'{tag}t{i}{j}',1]]
    edges.append([f'{tag}t00',f'{tag}t10',connector])
    return edges


def supports(n: int):
    for p,q in it.product(range(3),repeat=2):
        for t in range(min(p,q)+1):
            if p+q-t<=n:
                yield set(range(p)), set(range(t))|set(range(p,p+q-t))


def profiles(n: int):
    for p,q in supports(n):
        inc=[(i,c) for i,s in enumerate((p,q)) for c in sorted(s)]
        for vals in it.product((2,3),repeat=len(inc)):
            out=[[1]*n,[1]*n]
            for (i,c),v in zip(inc,vals): out[i][c]=v
            yield out


def neighbors(A,B,n):
    return [sum(1<<p for p in range(n)
                if all(A[i][p]+B[i][q]<=4 for i in range(2))) for q in range(n)]


def hall(neigh,n):
    for mask in range(1,1<<n):
        union=0
        for q in range(n):
            if mask>>q&1: union |= neigh[q]
        if union.bit_count()<mask.bit_count(): return False
    return True


def bad_form(A,B):
    P=[{p for p,x in enumerate(row) if x>1} for row in A]
    Q=[{q for q,x in enumerate(row) if x>1} for row in B]
    rectangles=all(all(A[i][p]+B[i][q]>4 for p in P[i] for q in Q[i])
                   for i in range(2))
    one=(len(P[0])==len(P[1])==2 and not P[0]&P[1]
         and Q[0]==Q[1] and len(Q[0])==2)
    two=(len(Q[0])==len(Q[1])==2 and not Q[0]&Q[1]
         and P[0]==P[1] and len(P[0])==2)
    return rectangles and (one or two)


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('budget')))
    signal.alarm(30)
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    A=shore('A',[[2,3],[4,5]],6)
    B=shore('B',[[2,3],[2,3]],4)
    stubs=lambda t: [[f'{t}p{i}',f'{t}x{i}',1] for i in range(2)]
    require(star(A+stubs('A')) and star(B+stubs('B')), 'shore coloring')
    cuts=[['Ax0','Bx0',1],['Ax1','Bx1',1]]
    failures=[]
    for perm in it.permutations(range(2,7)):
        pi={1:1,**dict(zip(range(2,7),perm))}
        glued=A+[[x,y,pi[c]] for x,y,c in B]+cuts
        require(not star(glued),'unexpected aligned six-color success')
        i,q=next((i,q) for i,P in enumerate(({2,3},{4,5})) for q in (2,3) if pi[q] in P)
        p=pi[q]; ja=([2,3] if i==0 else [4,5]).index(p); jb=[2,3].index(q)
        path=[f'Ar{i}{ja}',f'Ax{i}',f'Bx{i}',f'Br{i}{jb}',f'Bt{i}{jb}']
        em={frozenset((x,y)):c for x,y,c in glued}
        colors=[em[frozenset(e)] for e in zip(path,path[1:])]
        require(len(set(path))==5 and colors==[p,1,p,1], 'bad witness path')
        failures.append({'pi_2_to_6':list(perm),'path':path,'colors':colors})
    pi={1:1,2:4,3:5,4:2,5:3,6:6}
    repaired=A+[[x,y,pi[c]] for x,y,c in B]+[cuts[0],['Ax1','Bx1',6]]
    require(star(repaired),'explicit free-boundary coloring')
    reports={}
    for n in (5,6):
        pp=list(profiles(n)); bad=0; cases=0
        for aa,bb in it.product(pp,repeat=2):
            compatible=hall(neighbors(aa,bb,n),n)
            if n==5: require(compatible != bad_form(aa,bb), 'six-color Hall classification')
            else: require(compatible, 'seven-color universal alignment')
            bad+=not compatible; cases+=1
        reports[str(n+1)]={'canonical_profiles':len(pp),'ordered_cases':cases,'incompatible':bad}
    # Both shores linked in colors 1,2: actual gluing is a bad four-cycle.
    sq=[['Ax0','Ax1',2],['Bx0','Bx1',2]]+cuts
    require(not star(sq),'four-cycle mutation')
    result={'verdict':'candidate_only','runtime':platform.python_version(),
            'scope':'generator-side exact finite diagnostics, not a verifier receipt',
            'budgets':{'wall_seconds':30,'cpu_seconds':30,'memory_mib':512,'threads':1},
            'vertices_G':len({v for e in repaired for v in e[:2]}),'edges_G':len(repaired),
            'shore_A':A,'shore_B':B,'stub_color':1,'cuts':cuts,
            'six_color_permutations_rejected':len(failures),
            'rejection_paths_zlib_base64':base64.b64encode(zlib.compress(json.dumps(failures,separators=(',',':')).encode())).decode(),
            'free_boundary_star_coloring':repaired,'Hall_diagnostics':reports,
            'four_cycle_fixture_rejected':True}
    text=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    require(len(text.encode())<262144,'output budget')
    Path(__file__).with_name('opg37271-c15-twoport-result.json').write_text(text)
    print(json.dumps({k:result[k] for k in ['runtime','vertices_G','edges_G','six_color_permutations_rejected','Hall_diagnostics','four_cycle_fixture_rejected']},sort_keys=True))


if __name__=='__main__': main()
