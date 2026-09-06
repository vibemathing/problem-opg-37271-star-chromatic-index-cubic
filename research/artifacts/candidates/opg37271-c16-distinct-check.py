"""Exact, bounded, generator-side tests for distinct two-port star-color gluing."""
from __future__ import annotations
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def star(edges):
    adj={}; seen=set()
    for x,y,c in edges:
        if x==y or frozenset((x,y)) in seen: return False
        seen.add(frozenset((x,y)))
        adj.setdefault(x,[]).append((y,c)); adj.setdefault(y,[]).append((x,c))
    if any(len(n)>3 or len(n)!=len({c for _,c in n}) for n in adj.values()): return False
    for a,b in it.combinations(sorted({c for _,_,c in edges}),2):
        seen=set()
        for x in adj:
            if x in seen: continue
            todo=[x]; seen.add(x); ne=0; nv=0
            while todo:
                z=todo.pop(); nv+=1
                for w,c in adj[z]:
                    if c not in (a,b): continue
                    ne+=1
                    if w not in seen: todo.append(w); seen.add(w)
            ne//=2
            if ne>3 or (ne and ne>=nv): return False
    return True


def lengths(edges, leaf, k):
    adj={}
    for x,y,c in edges:
        adj.setdefault(x,[]).append((y,c)); adj.setdefault(y,[]).append((x,c))
    require(len(adj[leaf])==1, 'not private leaf')
    nxt,a=adj[leaf][0]; row=[0]*(k+1)
    for b in range(1,k+1):
        if b==a: continue
        prev,z=leaf,nxt; n=1; color=b; visited={leaf,nxt}
        for _ in range(4):
            possibilities=[w for w,c in adj[z] if c==color and w!=prev]
            if not possibilities: break
            require(len(possibilities)==1,'improper continuation')
            w=possibilities[0]; require(w not in visited,'cyclic stem')
            visited.add(w); prev,z=z,w; n+=1; color=a if color==b else b
        require(n<=3,'nonstar stem')
        row[b]=n
    return a,row


def augmented(tag,edges,stems):
    return edges+[[f'{tag}p{i}',f'{tag}x{i}',c] for i,c in enumerate(stems)]


def permuted(edges,pi): return [[x,y,pi[c]] for x,y,c in edges]


def test(A,B,stems,k):
    AA=augmented('A',A,stems); BB=augmented('B',B,stems)
    require(star(AA) and star(BB),'initial shore coloring')
    LA=[lengths(AA,f'Ap{i}',k)[1] for i in range(2)]
    LB=[lengths(BB,f'Bp{i}',k)[1] for i in range(2)]
    remaining=[c for c in range(1,k+1) if c not in stems]
    good=[]; checked=0
    for vals in it.permutations(remaining):
        pi={**dict(zip(remaining,vals)),**{a:a for a in stems}}
        inv={p:q for q,p in pi.items()}
        predicted=all(LA[i][p]+LB[i][inv[p]]<=4
                      for i,a in enumerate(stems) for p in range(1,k+1) if p!=a)
        G=A+permuted(B,pi)+[[f'Ax{i}',f'Bx{i}',a] for i,a in enumerate(stems)]
        require(star(G)==predicted,'transfer predicate disagreement')
        if predicted: good.append(pi)
        checked+=1
    return {'palette':k,'tested_permutations':checked,'valid_permutations':len(good),
            'LA':LA,'LB':LB,'first_valid_permutation':good[0] if good else None}


def branching(tag,palettes,connector):
    edges=[]
    for i in range(2):
        for j,c in enumerate(palettes[i]):
            edges += [[f'{tag}x{i}',f'{tag}r{i}{j}',c],
                      [f'{tag}r{i}{j}',f'{tag}t{i}{j}',1 if i==0 else 7]]
    return edges+[[f'{tag}t00',f'{tag}t10',connector]]


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(20)
    resource.setrlimit(resource.RLIMIT_CPU,(20,21))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    path=lambda T:[[T+'x0',T+'z',2],[T+'z',T+'w',1],[T+'w',T+'x1',3]]
    A,B=path('A'),path('B')
    cross=[test(A,B,[1,2],k) for k in (6,7,8)]
    require(all(r['valid_permutations']==0 for r in cross),'fixed cross obstruction lost')
    cyc=['Ax0','Az','Aw','Ax1','Bx1','Bw','Bz','Bx0']
    recolored=[[cyc[i],cyc[(i+1)%8],i%4+1] for i in range(8)]
    require(star(recolored),'free eight-cycle coloring')
    C=branching('A',[[2,3],[4,5]],6); D=branching('B',[[2,3],[2,3]],4)
    threshold=[test(C,D,[1,7],k) for k in (7,8)]
    require(threshold[0]['valid_permutations']==0,'seven-color threshold witness')
    require(threshold[1]['valid_permutations']>0,'eight-color compatible example')
    # Enumerate actual colored five-edge paths, not abstract state vectors.
    reference=[]; sigs=set(); count=0; same=0
    for cs in it.product(range(1,7),repeat=5):
        if any(cs[i]==cs[i+1] for i in range(4)): continue
        if any(cs[i]==cs[i+2] and cs[i+1]==cs[i+3] for i in range(2)): continue
        es=[[f'q{i}',f'q{i+1}',cs[i]] for i in range(5)]
        s=tuple((a,tuple(row[1:])) for a,row in [lengths(es,'q0',6),lengths(es,'q5',6)])
        sigs.add(s); count+=1; same+=cs[0]==cs[4]
        if len(reference)<2: reference.append({'edges':es,'signature':s})
    result={'verdict':'candidate_only','runtime':platform.python_version(),
      'scope':'local generator-side finite diagnostics; not a mathematical verifier receipt',
      'budgets':{'wall_seconds':20,'cpu_seconds':20,'memory_mib':512,'threads':1},
      'fixed_cross_example':{'shore_A':A,'shore_B':B,'stems':[1,2],
        'invariant_bad_path':['Aw','Az','Ax0','Bx0','Bz'],'bad_colors':[1,2,1,2],
        'runs':cross,'free_four_color_extension':recolored},
      'conditional_threshold_example':{'shore_A':C,'shore_B':D,'stems':[1,7],'runs':threshold},
      'actual_path_realizability':{'all_assignments':6**5,'star_colorings':count,
        'same_end_color_count':same,'distinct_end_color_count':count-same,
        'realized_signature_pairs':len(sigs),'example_backpointers':reference}}
    text=json.dumps(result,sort_keys=True,separators=(',',':'))+'\n'
    require(len(text.encode())<262144,'output budget')
    Path(__file__).with_name('opg37271-c16-distinct-result.json').write_text(text)
    print(json.dumps({'runtime':result['runtime'],'cross':cross,'threshold':threshold,
                     'actual_path_realizability':result['actual_path_realizability']},sort_keys=True))


if __name__=='__main__': main()
