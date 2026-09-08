"""Direct endpoint audit; no imports from any previous candidate implementation.
Run under the supplied process limits. Output is candidate_only.
"""
from itertools import permutations, product, combinations
from pathlib import Path
from collections import defaultdict
import hashlib, json, signal, resource

def require(q, msg):
    if not q: raise ValueError(msg)

class Graph:
    def __init__(self, n, edges):
        require(type(n) is int and 0 <= n <= 12, 'vertex bound')
        self.n=n; self.E=[tuple(sorted(e)) for e in edges]; self.m=len(edges)
        require(self.m <= 18 and len(set(self.E))==self.m, 'simple edge list')
        self.inc=[[] for _ in range(n)]; self.edge={}
        for i,(u,v) in enumerate(self.E):
            require(type(u) is int and type(v) is int and 0<=u<v<n,'endpoints')
            self.inc[u].append(i); self.inc[v].append(i); self.edge[u,v]=i
        require(max(map(len,self.inc),default=0)<=3,'subcubic')
        self.sh=[]
        for length in (4,5):
            for vs in permutations(range(n),length):
                if length==5 and vs[0]>vs[-1]: continue
                if length==4 and (vs[0]!=min(vs) or vs[1]>vs[-1]): continue
                pairs=list(zip(vs,vs[1:]))+([(vs[-1],vs[0])] if length==4 else [])
                if all(tuple(sorted(p)) in self.edge for p in pairs):
                    self.sh.append((('cycle' if length==4 else 'path'),vs,tuple(self.edge[tuple(sorted(p))] for p in pairs)))
    def proper(self,c):
        return all(len([c[e] for e in ns if c[e]>0])==len({c[e] for e in ns if c[e]>0}) for ns in self.inc)
    def paths(self,w):
        todo={e for e,c in enumerate(w) if c==0}; out=[]
        while todo:
            a=min(todo); part={a}; todo.remove(a); stack=[a]
            while stack:
                e=stack.pop()
                for v in self.E[e]:
                    for f in self.inc[v]:
                        if f in todo: todo.remove(f); part.add(f); stack.append(f)
            vs={v for e in part for v in self.E[e]}
            deg={v:sum(e in part for e in self.inc[v]) for v in vs}; ends=sorted(v for v,d in deg.items() if d==1)
            require(1<=len(part)<=3 and len(vs)==len(part)+1 and len(ends)==2 and max(deg.values())<=2,'U path premise')
            v=ends[0]; seq=[]
            while len(seq)<len(part):
                e=next(e for e in self.inc[v] if e in part and e not in seq); seq.append(e); v=next(x for x in self.E[e] if x!=v)
            out.append(seq)
        out.sort(key=min); return out
    def astar(self,w):
        if not self.proper(w): return False
        for a,b in combinations(range(1,5),2):
            todo={e for e,c in enumerate(w) if c in (a,b)}
            while todo:
                stack=[todo.pop()]; size=0
                while stack:
                    e=stack.pop(); size+=1
                    for v in self.E[e]:
                        for f in self.inc[v]:
                            if f in todo: todo.remove(f); stack.append(f)
                if size>=4: return False
        return True
    def premise(self,w):
        require(len(w)==self.m and all(type(c) is int and c in range(5) for c in w),'A palette')
        require(self.astar(w),'D star'); return self.paths(w)
    def violations(self,c,filter_edges=None):
        require(len(c)==self.m and all(type(a) is int and a in range(1,7) for a in c),'full palette')
        require(self.proper(c),'proper full coloring')
        return [dict(kind=k,vertices=list(v),edges=list(es)) for k,v,es in self.sh
                if (filter_edges is None or set(es)&filter_edges) and len({c[e] for e in es})==2]
    def full(self,w,bits):
        ps=self.premise(w); require(len(bits)==len(ps),'phase arity'); c=list(w)
        for i,p in enumerate(ps):
            for j,e in enumerate(p): c[e]=5+(bits[i]^(j%2))
        return c
    def profile(self,w,S):
        ps=self.premise(w); require(all(not(set(p)&S) or set(p)<=S for p in ps),'joint U closure')
        ext=[i for i,p in enumerate(ps) if not set(p)&S]; profile={}; attain={}
        for bits in product(range(2),repeat=len(ps)):
            c=self.full(w,bits); key=tuple(bits[i] for i in ext); cost=len(self.violations(c,S))
            if key not in profile or cost<profile[key]: profile[key]=cost; attain[key]=c
        return ext,profile,attain
    def endpoints(self,w,S,ext_bits):
        """All literal six-color support assignments; only proper prefixes prune.
        Outside B colors fixed literally. Projecting B back to zero groups phases.
        """
        ps=self.premise(w); ext=[i for i,p in enumerate(ps) if not set(p)&S]
        require(all(not(set(p)&S) or set(p)<=S for p in ps),'old closure')
        require(len(ext_bits)==len(ext),'outside phase arity')
        c=list(w)
        for i,b in zip(ext,ext_bits):
            for j,e in enumerate(ps[i]): c[e]=5+(b^(j%2))
        order=sorted(S)
        for e in S:c[e]=-1
        table={}
        def rec(t):
            if t==len(order):
                q=tuple(a if a<=4 else 0 for a in c)
                if not self.astar(q): return
                try: qp=self.paths(q)
                except ValueError: return
                if not all(not(set(p)&S) or set(p)<=S for p in qp): return
                key=tuple(c[p[0]]-5 for p in qp)
                table.setdefault(q,{})[key]=dict(colors=list(c),bad=self.violations(c))
                return
            e=order[t]
            for a in range(1,7):
                if any(c[f]==a for v in self.E[e] for f in self.inc[v] if f!=e): continue
                c[e]=a; rec(t+1)
            c[e]=-1
        rec(0); return table

def absorption(G,F,Q,S,T):
    require(S<=T and all(F[e]==Q[e] for e in range(G.m) if e not in S),'fixed endpoint support')
    p=G.premise(F); pq=G.premise(Q)
    for w in (F,Q): G.profile(w,S); G.profile(w,T)
    outsideS=[i for i,P in enumerate(p) if not set(P)&S]
    outsideT=[i for i,P in enumerate(p) if not set(P)&T]
    absorbed=[i for i in outsideS if i not in outsideT]
    _,old,unused=G.profile(F,S); _,new,unused=G.profile(Q,S)
    _,oldt,_=G.profile(F,T); _,newt,_=G.profile(Q,T)
    require([p[i] for i in outsideS]==[P for P in pq if not set(P)&S],'common exterior paths')
    cases=[]
    for b in product(range(2),repeat=len(outsideT)):
        assigned=dict(zip(outsideT,b)); rows=[]
        for z in product(range(2),repeat=len(absorbed)):
            bits=assigned|dict(zip(absorbed,z)); key=tuple(bits[i] for i in outsideS); hs=set(); wh=[]
            for iv in product(range(2),repeat=len(p)-len(outsideS)):
                bs=dict(bits); bs.update(zip([i for i in range(len(p)) if i not in outsideS],iv))
                full=G.full(F,[bs[i] for i in range(len(p))])
                bad=[q for q in G.violations(full,T) if not set(q['edges'])&S]; hs.add(len(bad)); wh=bad
            require(len(hs)==1,'h independent of old internal phases'); h=hs.pop()
            rows.append(dict(z=list(z),old=old[key],new=new[key],h=h,r=old[key]+h-oldt[b],g=old[key]-new[key],newly_bad=wh))
        gain=max(a['g']-a['r'] for a in rows)
        require(gain==oldt[b]-newt[b],'exact max(g-r) identity')
        cases.append(dict(b=list(b),old_T=oldt[b],new_T=newt[b],gain=gain,terms=rows))
    return cases

def rejected(name,fn,tests):
    try:fn()
    except (ValueError,KeyError,IndexError):tests.append(dict(name=name,decision='rejected'));return
    raise ValueError('mutation survived '+name)

def run():
    E=[(0,5),(0,6),(0,7),(1,4),(1,6),(1,7),(2,3),(2,5),(2,7),(3,4),(3,6),(4,5)]
    G=Graph(8,E); F=[1,2,3,4,3,0,4,0,1,0,1,0]; S={3,6,7,9,11};T=S|{5}
    ps=G.premise(F); costs=[len(G.violations(G.full(F,b))) for b in ((0,0),(1,0),(0,1),(1,1))]
    require(costs==[3,1,1,3],'frozen C27 phase costs')
    ts=G.endpoints(F,T,()); require(len(ts)==16,'complete T endpoints')
    compact=[]
    for q,rs in sorted(ts.items()):
        require(len(rs)==2**len(G.paths(q)),'all endpoint phases')
        require(min(len(r['bad']) for r in rs.values())>=1,'all T endpoints fail')
        compact.append(dict(word=list(q),phases=[dict(bits=list(b),**r) for b,r in sorted(rs.items())]))
    bare=[G.endpoints(F,S,(b,)) for b in (0,1)]
    require(all(len(q)==10 for q in bare),'ten S endpoints at each boundary')
    require(set(bare[0])==set(bare[1]),'endpoint premise independent of phase')
    require(all(min(len(r['bad']) for rs in tab.values() for r in rs.values())==1 for tab in bare),'bare envelope')
    Q=F.copy();Q[0]=0;Q[7]=2;R=T|{0}
    ex,pr,_=G.profile(Q,R); require(pr[()]==0,'joint repair')
    extensions=[]
    for e,expected in ((0,169),(2,119),(4,95),(8,60),(10,116)):
        family=G.endpoints(F,T|{e},());require(len(family)==expected,'one-edge family completeness')
        optimum=min(len(r['bad']) for rs in family.values() for r in rs.values())
        require(optimum==(1 if e==8 else 0),'one-edge family optimum')
        extensions.append(dict(added_edge=e,endpoints=len(family),minimum=optimum))
    original=[1,2,0,0,0,3,3,0,4,2,0,3]; repaired=[1,2,0,2,0,3,3,0,4,0,1,3]; A={1,3,4,9,10};B=A|{2}
    literal_control=absorption(G,original,repaired,A,B)
    original[8]=1
    modified_candidates=G.endpoints(original,A,(0,0))
    repaired2=list(next(q for q in sorted(modified_candidates) if list(q)!=original))
    nonzero_h=absorption(G,original,repaired2,A,B|{7})
    require(any(r['h']>0 for case in nonzero_h for r in case['terms']),'nonzero actual h exercised')
    tests=[]
    rejected('duplicate_graph_edge',lambda:Graph(8,E+[E[0]]),tests)
    rejected('D_palette_crossing',lambda:G.premise([5]+F[1:]),tests)
    rejected('U_length_four',lambda:Graph(5,[(0,1),(1,2),(2,3),(3,4)]).premise([0]*4),tests)
    rejected('nonclosed_core_support',lambda:G.profile(F,S-{11}),tests)
    rejected('outside_endpoint_change',lambda:absorption(G,F,Q,S,T),tests)
    rejected('missing_endpoint',lambda:require(len(compact[:-1])==16,'endpoint coverage'),tests)
    rejected('missing_phase',lambda:require(len(list(next(iter(ts.values())))[:-1])==len(next(iter(ts.values()))),'phase coverage'),tests)
    C=Graph(4,[(0,1),(1,2),(2,3),(3,0)]);require(len(C.violations([5,1,5,1]))==1,'C4 control')
    tests.append(dict(name='omit_four_cycle',decision='distinguished',actual=1,mutant=0))
    H=Graph(5,[(0,1),(1,2),(2,3),(3,4),(1,3)])
    require(any(r['vertices']==[0,1,2,3,4] for r in H.violations([5,1,5,1,2])),'noninduced path')
    tests.append(dict(name='induced_only',decision='distinguished'))
    tests.append(dict(name='ignore_self_row',decision='distinguished',actual_min=min(costs),mutant_min=0))
    require(len({tuple(r['vertices']) for r in G.violations(G.full(F,(0,0)))})==3,'support multiplicity')
    tests.append(dict(name='merge_equal_rows',decision='distinguished',actual_cost=3,mutant_cost=2))
    require(min(costs[::3])>min(costs),'deleted minimizing phases')
    tests.append(dict(name='discard_minimizing_phases',decision='distinguished'))
    # An abstract signed interface, NOT asserted to be realized by a subcubic graph.
    interface=[]
    for p,q in product(range(2),repeat=2):
        old=1+min(2*(t!=p)+3*(t!=q) for t in (0,1));new=int(p==q);h=int(p!=q)
        interface.append(dict(ports=[p,q],old=old,new=new,h=h,r=old+h-1,g=old-new))
    require(max(a['g']-a['r'] for a in interface)==0,'cut-only countermodel')
    require(max(a['g']-(a['old']-1) for a in interface)==1,'dropping h is unsound')
    tests.append(dict(name='drop_new_h',decision='distinguished',actual_gain=0,mutant_gain=1))
    signed=[]
    for k in (1,2,3):
        rows=[(0,1,0)]*k
        margins=[]
        for mask in range(4):margins.append(sum(((mask>>i&1)^(mask>>j&1)) for i,j,_ in rows))
        require(min(margins[1:3])==k,'parallel separator price')
        signed.append(dict(multiplicity=k,shortest_length=1,separator_price=k))
    tests.append(dict(name='price_equals_shortest_length',decision='distinguished'))
    require(min(len(r['bad']) for rs in ts.values() for r in rs.values())==1,'all old U absorbed is not sufficient')
    tests.append(dict(name='zero_exterior_ports_implies_zero_cost',decision='distinguished'))
    local_gain=max(t['g']-t['r'] for t in literal_control[0]['terms'])
    optimal_only=max(t['g']-t['r'] for t in literal_control[0]['terms'] if t['r']==0)
    require((local_gain,optimal_only)==(1,0),'nonattaining absorbed phase matters')
    tests.append(dict(name='keep_only_old_optimal_absorbed_phase',decision='distinguished',actual_gain=1,mutant_gain=0))
    for i in (0,7):
        mid=F.copy();mid[i]=Q[i]
        rejected('require_legal_single_edit_'+str(i),lambda mid=mid:G.premise(mid),tests)
    return dict(verdict='candidate_only',best_verified_result='none',root_closed=False,graph=dict(n=8,edges=E),
      C27=dict(word=F,S=sorted(S),T=sorted(T),old_costs=costs,S_endpoints=10,T_endpoints=16,full_T_table=compact,
               repair=Q,repair_support=sorted(R),repair_profile=[pr[()]],one_edge_extensions=extensions),
      C26_literal_absorption=literal_control,nonzero_h_control=dict(old=original,new=repaired2,S=sorted(A),T=sorted(B|{7}),cases=nonzero_h),
      signed_interface_countermodel=dict(scope='abstract signed interface only; no graph realization or global frame optimum asserted',terms=interface),
      parallel_separator_controls=signed,mutations=tests,
      limits='Exact named endpoints and literal support colorings only; no new all-cubic census and no genuine two-port GLOBAL-EXCHANGE closure.')

if __name__=='__main__':
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
    out=run();data=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
    require(len(data)<1048576,'output size');path=Path(__file__).with_name('opg37271-c27-direct-audit.json');path.write_bytes(data)
    print(json.dumps(dict(verdict='candidate_only',T_endpoints=out['C27']['T_endpoints'],mutations=len(out['mutations']),sha256=hashlib.sha256(data).hexdigest()),sort_keys=True))
