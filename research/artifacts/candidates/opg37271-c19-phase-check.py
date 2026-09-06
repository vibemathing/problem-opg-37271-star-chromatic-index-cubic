"""Exact two-color completion via signed phase constraints; bounded diagnostics."""
import hashlib
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def need(ok,msg):
    if not ok: raise ValueError(msg)


def paths(n,E):
    adj=[[] for _ in range(n)]
    for e,(u,v) in enumerate(E): adj[u].append((v,e));adj[v].append((u,e))
    out=[]
    def walk(vs,es):
        if len(es)==4:
            if vs[0]<vs[-1]: out.append(['path',vs,es])
            return
        for v,e in adj[vs[-1]]:
            if v not in vs: walk(vs+[v],es+[e])
            elif len(es)==3 and v==vs[0] and vs[0]==min(vs) and vs[1]<vs[-1]:
                out.append(['cycle',vs,es+[e]])
    for v in range(n): walk([v],[])
    return adj,out


def star(adj,obstructions,c):
    if any(len([c[e] for _,e in ns if c[e]])!=len({c[e] for _,e in ns if c[e]}) for ns in adj): return False
    return all(not all(c[e] for e in es) or c[es[0]]!=c[es[2]] or c[es[1]]!=c[es[3]] for _,_,es in obstructions)


def compile_system(n,E,c):
    need(len(c)==len(E) and all(type(a) is int and 0<=a<=4 for a in c),'partial palette')
    need(all(0<=u<n and 0<=v<n and u!=v for u,v in E) and len(set(map(frozenset,E)))==len(E),'simple graph')
    adj,obs=paths(n,E); need(all(len(x)<=3 for x in adj),'subcubic')
    need(star(adj,obs,c),'fixed subgraph not star')
    U={e for e,a in enumerate(c) if not a};info={};components=[]
    while U:
        seed=min(U); stack=list(E[seed]); vs=set(stack); es=set()
        while stack:
            u=stack.pop()
            for v,e in adj[u]:
                if c[e]: continue
                es.add(e)
                if v not in vs: vs.add(v);stack.append(v)
        ends=[v for v in vs if sum(not c[e] for _,e in adj[v])==1]
        need(len(ends)==2 and len(es)==len(vs)-1 and len(es)<=3 and all(sum(not c[e] for _,e in adj[v])<=2 for v in vs),'uncolored path premise')
        u=min(ends);previous=None;seq=[]
        while True:
            nxt=[(v,e) for v,e in adj[u] if not c[e] and e!=previous]
            if not nxt: break
            v,e=nxt[0];info[e]=[len(components),len(seq)%2];seq.append(e);previous=e;u=v
        components.append(seq);U-=es
    equations=[];seen=set()
    for kind,vs,es in obs:
        for fixed,free in [((0,2),(1,3)),((1,3),(0,2))]:
            a,b=(c[es[t]] for t in fixed)
            if not a or a!=b or any(c[es[t]] for t in free): continue
            e,f=(es[t] for t in free);i,p=info[e];j,q=info[f]
            rhs=1^p^q;key=(min(i,j),max(i,j),rhs)
            if key in seen: continue
            seen.add(key);equations.append({'i':i,'j':j,'rhs':rhs,'kind':kind,'vertices':vs,'edges':es,'free_edges':[e,f]})
    return components,info,equations,adj,obs


def solve(k,eq):
    adj=[[] for _ in range(k)]
    for e,q in enumerate(eq):
        adj[q['i']].append((q['j'],q['rhs'],e));adj[q['j']].append((q['i'],q['rhs'],e))
    val=[None]*k;parent=[None]*k
    for r in range(k):
        if val[r] is not None: continue
        val[r]=0;todo=[r]
        while todo:
            u=todo.pop()
            for v,b,e in adj[u]:
                if val[v] is None: val[v]=val[u]^b;parent[v]=(u,e);todo.append(v)
                elif val[v]!=(val[u]^b):
                    ids={e}
                    for x in (u,v):
                        while parent[x] is not None:
                            x,j=parent[x];ids.symmetric_difference_update({j})
                    return None,sorted(ids)
    return val,[]


def component_count(k,eq):
    neighbors=[set() for _ in range(k)]
    for q in eq: neighbors[q['i']].add(q['j']);neighbors[q['j']].add(q['i'])
    seen=set(); count=0
    for r in range(k):
        if r in seen: continue
        count+=1;seen.add(r);todo=[r]
        while todo:
            u=todo.pop()
            for v in neighbors[u]:
                if v not in seen:seen.add(v);todo.append(v)
    return count


def coloring(c,info,phase):
    return [a if a else 5+(phase[info[e][0]]^info[e][1]) for e,a in enumerate(c)]


def negative_audit(eq,ids):
    vars=set();b=0
    for e in ids:
        q=eq[e];vars.symmetric_difference_update({q['i']});vars.symmetric_difference_update({q['j']});b^=q['rhs']
    need(not vars and b==1,'invalid parity contradiction')


def certificate(n,E,c):
    comps,info,eq,adj,obs=compile_system(n,E,c);val,ids=solve(len(comps),eq)
    if val is not None: need(star(adj,obs,coloring(c,info,val)),'bad produced coloring')
    else: negative_audit(eq,ids)
    return {'n':n,'edges':E,'partial_colors':c,'uncolored_paths':comps,'equations':eq,
            'phase':val,'contradiction_rows':ids,'full_colors':None if val is None else coloring(c,info,val)}


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(35,36));resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    choices=[(i,) for i in range(4)]+[(0,2),(1,3)]
    summary=[];example=None;total=0;phase_trials=0;special_counts={};k4_single=[0,0]
    for pi,perm in enumerate(it.permutations(range(4))):
        E=[(i,4+perm[i]) for i in range(4)]+[(i,(i+1)%4) for i in range(4)]+[(4+i,4+(i+1)%4) for i in range(4)]
        lam=[1,2,3,4]+[0]*4
        for i,p in enumerate(perm):lam[4+p]=i+1
        sat=unsat=extensions=0;first=None
        for left,right in it.product(choices,repeat=2):
            S=[4+i for i in left]+[8+i for i in right]
            options=[[a for a in range(1,5) if a not in (lam[E[e][0]],lam[E[e][1]])] for e in S]
            for sc in it.product(*options):
                c=[1,2,3,4]+[0]*8
                for e,a in zip(S,sc):c[e]=a
                comps,info,eq,adj,obs=compile_system(8,E,c);val,ids=solve(len(comps),eq)
                brute_count=0
                for phase in it.product((0,1),repeat=len(comps)):
                    phase_trials+=1
                    if star(adj,obs,coloring(c,info,phase)): brute_count+=1
                need((val is not None)==bool(brute_count),'XOR/brute mismatch')
                if val is not None: need(brute_count==2**component_count(len(comps),eq),'solution count mismatch')
                extensions+=brute_count
                group=special_counts.setdefault(str(len(S)),[0,0]);group[0]+=1;group[1]+=int(val is not None)
                conflict={tuple(sorted((lam[u],lam[v]))) for u,v in E[4:]}
                if len(conflict)==6 and len(S)==2: k4_single[0]+=1;k4_single[1]+=int(val is not None)
                total+=1
                if val is None: unsat+=1;negative_audit(eq,ids)
                else:
                    sat+=1;full=coloring(c,info,val)
                    need(star(adj,obs,full),'positive audit')
                    if first is None:first=full
                    conflict={tuple(sorted((lam[u],lam[v]))) for u,v in E[4:]}
                    if example is None and len(conflict)==6:example=certificate(8,E,c)
        summary.append([pi,sat,unsat,extensions,first])
    cycle=[(i,(i+1)%6) for i in range(6)];negative=certificate(6,cycle,[1,0,1,0,1,0])
    need(negative['phase'] is None,'six-cycle must obstruct binary completion')
    # The same partial input extends with three residual colors instead.
    adj,obs=paths(6,cycle);need(star(adj,obs,[1,4,1,5,1,6]),'six-cycle wider-palette witness')
    # Check certificate equations directly, without the solver.
    positive_equations=all((example['phase'][q['i']]^example['phase'][q['j']])==q['rhs'] for q in example['equations'])
    need(positive_equations,'phase witness equations')
    out={'verdict':'candidate_only','runtime':platform.python_version(),'scope':'generator-side equivalence audit, not trusted verification','partial_frames':total,'binary_phase_assignments':phase_trials,'permutation_rows':summary,'permutation_row_format':'[lexicographic matching permutation index, feasible frames, infeasible frames, total two-color extensions, first full coloring]','by_special_count':special_counts,'k4_one_special_per_cycle':[k4_single[0],k4_single[1]],'positive_k4_frame':example,'negative_six_cycle_frame':negative,'six_cycle_wider_palette':[1,4,1,5,1,6],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'budgets':{'wall_seconds':35,'cpu_seconds':35,'memory_mib':512,'threads':1}}
    raw=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n';need(len(raw)<262144,'output budget')
    Path(__file__).with_name('opg37271-c19-phase-certificate.json').write_text(raw)
    print(json.dumps({'frames':total,'phase_assignments':phase_trials,'sat':sum(x[1] for x in summary),'unsat':sum(x[2] for x in summary),'example':example,'negative':negative},sort_keys=True))
if __name__=='__main__':main()
