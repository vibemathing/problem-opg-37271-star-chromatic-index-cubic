"""C26 geometric checker. No imports of any candidate search or older core.
Search uses prefix colors and path traversal. Here whole supports use cartesian
six-color products, while color validity/cost uses two-color components.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import json,hashlib,resource,signal,sys
HERE=Path(__file__).resolve().parent

def need(p,msg):
    if not p:raise ValueError(msg)

def digest(b):return hashlib.sha256(b).hexdigest()

def normalize(w):
    names={};out=[]
    for x in w:
        if x:names.setdefault(x,len(names)+1);out.append(names[x])
        else:out.append(0)
    return tuple(out)

class Graph:
    def __init__(self,n,edges):
        need(type(n)is int and 0<n<=10 and 0<len(edges)<=15,'input bound')
        self.n=n;self.E=[tuple(e) for e in edges];self.m=len(edges);self.adj=[set() for _ in range(n)]
        need(len(set(self.E))==self.m,'simple edges')
        for i,(a,b) in enumerate(self.E):
            need(type(a)is int and type(b)is int and 0<=a<b<n,'endpoints')
            self.adj[a].add(i);self.adj[b].add(i)
        need(all(len(a)<=3 for a in self.adj),'subcubic')
        self.shapes=[]
        # Four-edge subset topology, not searcher's vertex DFS.
        for es in combinations(range(self.m),4):
            vs={v for e in es for v in self.E[e]};deg={v:sum(e in self.adj[v] for e in es) for v in vs}
            if sorted(deg.values())==[1,1,2,2,2]:kind='path';start=min(v for v in vs if deg[v]==1)
            elif sorted(deg.values())==[2,2,2,2]:kind='cycle';start=min(vs)
            else:continue
            seen=[];vseq=[start];v=start
            for _ in range(4):
                options=sorted((sum(self.E[e])-v,e) for e in self.adj[v] if e in es and e not in seen)
                if not options:break
                v,e=options[0];seen.append(e);vseq.append(v)
            if len(seen)!=4:continue
            if kind=='cycle':need(vseq[-1]==vseq[0],'cycle closure');vseq.pop()
            need(len(set(vseq))==len(vseq),'simple shape')
            self.shapes.append({'kind':kind,'vertices':vseq,'edges':seen})
        self.pathcache={}
    def groups(self,es):
        pending=set(es);out=[]
        while pending:
            start=min(pending);pending.remove(start);group={start};stack=[start]
            while stack:
                e=stack.pop()
                for v in self.E[e]:
                    new=self.adj[v]&pending;pending-=new;group|=new;stack.extend(new)
            out.append(group)
        return out
    def proper(self,c):
        return all(len([c[e] for e in es if c[e]])==len({c[e] for e in es if c[e]}) for es in self.adj)
    def pair_cost(self,c,allow_partial=False):
        need(len(c)==self.m and all(type(x)is int and (0 if allow_partial else 1)<=x<=6 for x in c),'palette')
        need(self.proper(c),'proper coloring')
        total=0
        for a,b in combinations(range(1,7),2):
            for component in self.groups(e for e,x in enumerate(c) if x in (a,b)):
                vs={v for e in component for v in self.E[e]};cycle=all(len(self.adj[v]&component)==2 for v in vs);L=len(component)
                total+= (1 if L==4 else L) if cycle else max(0,L-3)
        return total
    def paths(self,w):
        mask=tuple(i for i,c in enumerate(w) if c==0)
        if mask in self.pathcache:
            need(self.pathcache[mask] is not None,'U paths');return self.pathcache[mask]
        ps=[]
        for es in self.groups(mask):
            vs={v for e in es for v in self.E[e]};d={v:len(self.adj[v]&es) for v in vs};ends=sorted(v for v in vs if d[v]==1)
            if not(1<=len(es)<=3 and len(vs)==len(es)+1 and max(d.values())<=2 and len(ends)==2):
                self.pathcache[mask]=None;raise ValueError('U paths')
            v=ends[0];seq=[]
            while len(seq)<len(es):
                options=sorted((self.adj[v]&es)-set(seq));need(len(options)==1,'U sequence');e=options[0];seq.append(e);v=sum(self.E[e])-v
            ps.append(seq)
        self.pathcache[mask]=ps;return ps
    def frame(self,w):
        need(len(w)==self.m and all(type(x)is int and 0<=x<=4 for x in w),'A palette')
        need(self.pair_cost(w,True)==0,'D star');return self.paths(w)
    def decode(self,w,p):
        ps=self.frame(w);need(type(p)is int and 0<=p<1<<len(ps),'phase domain');c=list(w)
        for j,P in enumerate(ps):
            for k,e in enumerate(P):c[e]=5+((p>>j&1)^(k%2))
        return c
    def costs(self,w):return [self.pair_cost(self.decode(w,p)) for p in range(1<<len(self.frame(w)))]
    def connected(self,S):return bool(S) and len(self.groups(S))==1
    def closed(self,w,S):return all(not(set(p)&S) or set(p)<=S for p in self.frame(w))
    def endpoint(self,old,new,S):
        need(self.connected(S) and self.closed(old,S),'old connected closed support')
        need(len(new)==self.m and all(type(x)is int and 1<=x<=6 for x in new),'new palette')
        word=[x if x<=4 else 0 for x in new];self.frame(word)
        need(self.proper(new),'new proper');need(self.closed(word,S),'new closed support')
        return word
    def family(self,w,p,S):
        old=self.decode(w,p);need(self.connected(S) and self.closed(w,S),'support premise');count=0;best=1000000;solutions=[]
        for vals in product(range(1,7),repeat=len(S)):
            c=old.copy()
            for e,x in zip(sorted(S),vals):c[e]=x
            try:self.endpoint(w,c,S)
            except ValueError:continue
            v=self.pair_cost(c);count+=1
            if v<best:best=v;solutions=[c]
            elif v==best:solutions.append(c)
        need(count>0,'old endpoint retained');return count,best,solutions
    def rows(self,w):
        info={e:(j,k%2) for j,P in enumerate(self.frame(w)) for k,e in enumerate(P)};out=[]
        for W in self.shapes:
            es=W['edges'];z=[j for j,e in enumerate(es) if w[e]==0]
            if z not in ([0,2],[1,3]):continue
            fixed=[es[j] for j in range(4) if j not in z]
            if w[fixed[0]]!=w[fixed[1]]:continue
            e,f=[es[j] for j in z];i,a=info[e];j,b=info[f]
            out.append(W|{'i':i,'j':j,'rhs':1^a^b,'fixed_edges':fixed,'free_edges':[e,f]})
        return out
    def row_check(self,w,q):
        need(q in self.rows(w),'actual witness row')
    def minimal_core(self,w):
        rows=self.rows(w);ps=self.frame(w);candidates=[]
        for k in range(1,len(ps)+1):
            for ids in combinations(range(len(rows)),k):
                mask=rhs=0;S=set()
                for t in ids:
                    q=rows[t];mask^=(1<<q['i'])^(1<<q['j']);rhs^=q['rhs'];S.update(q['edges'])
                if mask==0 and rhs==1:
                    for P in ps:
                        if set(P)&S:S.update(P)
                    need(self.connected(S),'core hull connected');candidates.append((len(S),tuple(sorted(S)),ids))
            if candidates:
                size,S,ids=min(candidates);return {'row_count':k,'hull_edges':list(S),'rows':[rows[t] for t in ids]}
        return None

def full_catalog(g):
    # Literal five-symbol words; only A-name normalization is filtered.
    states={}
    for w in product(range(5),repeat=g.m):
        maximum=0;good=True
        for x in w:
            if x>maximum+1:good=False;break
            maximum=max(x,maximum)
        if not good or not g.proper(w):continue
        try:ps=g.frame(w)
        except ValueError:continue
        states[''.join(map(str,w))]=g.costs(w)
    return states

def check_catalog(g,table):
    records=table['states'];states=full_catalog(g);seen=set();raw=0;phases=0;sizes=Counter()
    for key,mu,orbit,cs,S,p,new in records:
        need(key not in seen and key in states,'state coverage or duplicate');seen.add(key)
        need(cs==states[key] and min(cs)==mu,'all phase values');w=list(map(int,key));q=max(w);factor=1
        for t in range(q):factor*=4-t
        need(orbit==factor,'A orbit');raw+=factor;phases+=len(cs)
        c=list(map(int,new));need(cs[p]==mu,'old attaining phase')
        old=g.decode(w,p)
        if mu:
            es={e for e in range(g.m) if S>>e&1};need(len(es)<=3,'three-edge support');g.endpoint(w,c,es)
            need(all(c[e]==old[e] for e in range(g.m) if e not in es),'exterior held')
            need(g.pair_cost(c)<mu,'strict endpoint gain');sizes[len(es)]+=1
        else:need(g.pair_cost(c)==0,'balanced witness')
    need(seen==set(states) and table['count']==len(states),'complete state space')
    return {'frames':len(states),'raw_frames':raw,'phases':phases,'positive':sum(min(c)>0 for c in states.values()),'certificate_support_sizes':dict(sizes)}

def profile(g,w,S):
    ps=g.frame(w);inside=[P for P in ps if set(P)<=S];outside=[P for P in ps if not(set(P)&S)]
    need(len(inside)+len(outside)==len(ps),'closed patch');touched=[W for W in g.shapes if set(W['edges'])&S]
    boundary=[P for P in outside if any(set(P)&set(W['edges']) for W in touched)]
    vals=[];attainers=[]
    for b in range(1<<len(boundary)):
        candidates=[]
        for a in range(1<<len(inside)):
            c=list(w)
            for family,t in ((inside,a),(outside,0),(boundary,b)):
                for j,P in enumerate(family):
                    for k,e in enumerate(P):c[e]=5+((t>>j&1)^(k%2))
            v=sum(len({c[e] for e in W['edges']})==2 for W in touched);candidates.append((v,c))
        v,c=min(candidates);vals.append(v);attainers.append(c)
    return {'boundary_paths':boundary,'inside_paths':inside,'values':vals,'attainers':attainers,'touched':touched}

def cycle_dp(weights,signs,fields):
    r=len(weights);need(r>=3 and len(signs)==r and len(fields)==r,'cycle dimensions')
    values=[]
    for first in (0,1):
        d=[10**9,10**9];d[first]=fields[0][first]
        for i in range(1,r):
            d=[fields[i][b]+min(d[a]+weights[i-1]*((a^b)!=signs[i-1]) for a in (0,1)) for b in (0,1)]
        values.append(min(d[a]+weights[-1]*((a^first)!=signs[-1]) for a in (0,1)))
    return min(values)

def check_patches(g,w,table,K):
    cs=g.costs(w);need(table['costs']==cs,'case phases');ps=g.frame(w);required=[]
    for k in range(1,K+1):
        for S0 in combinations(range(g.m),k):
            S=set(S0)
            if g.connected(S) and g.closed(w,S):required.extend((sum(1<<e for e in S),p) for p in range(len(cs)))
    records=table['rows'];need(len(records)==len(required) and {(r[0],r[1]) for r in records}==set(required),'all supports and phases')
    bysize=Counter();counted=0;bestK=1000
    for mask,p,count,nodes,best,new in records:
        S={e for e in range(g.m) if mask>>e&1};c,b,solutions=g.family(w,p,S)
        need(c==count and best==b and list(map(int,new)) in solutions,'exact endpoint family')
        counted+=c
        if p==0:bysize[len(S)]+=1
        if cs[p]==min(cs) and best<min(cs):bestK=min(bestK,len(S))
    return {'support_counts':dict(bysize),'support_phase_pairs':len(records),'enumerated_legal_endpoints':counted,'minimum_anchored_improving_support':bestK}

def closure_family_tests():
    def closure(parts,seed):
        reached=set(seed)
        while True:
            old=set(reached)
            for P in parts:
                if reached&set(P):reached.update(P)
            if old==reached:return reached
    out=[]
    for q in range(1,9):
        L=4*q;n=2*L
        E=[(layer*L+j,layer*L+(j+1)%L) for layer in range(2) for j in range(L)]+[(j,L+j) for j in range(L)]
        adj=[[] for _ in range(n)]
        for i,(a,b) in enumerate(E):adj[a].append((b,i));adj[b].append((a,i))
        need(len({frozenset(e) for e in E})==len(E) and all(len(ns)==3 for ns in adj),'prism cubic')
        partitions=[]
        for shift,missing in ((0,3),(2,1)):
            parts=[[layer*L+(4*j+shift+t)%L for t in range(3)] for layer in range(2) for j in range(q)]
            covered=[]
            for P in parts:
                vs={v for e in P for v in E[e]};need(len(vs)==4,'three-edge path vertices');covered.extend(vs)
                need(all(set(E[P[j]])&set(E[P[j+1]]) for j in range(2)),'path adjacency')
            need(sorted(covered)==list(range(n)),'path factor covers vertices once')
            U={e for P in parts for e in P};colors=[0]*len(E)
            for j in range(missing,L,4):
                cycle=[j,2*L+(j+1)%L,L+j,2*L+j]
                for e,c in zip(cycle,(1,2,1,3)):colors[e]=c
            for e in range(2*L,3*L):
                if not colors[e]:colors[e]=1
            need({i for i,c in enumerate(colors) if not c}==U,'D/U partition')
            need(all(len([colors[e] for _,e in ns if colors[e]])==len({colors[e] for _,e in ns if colors[e]}) for ns in adj),'D proper')
            def walk(vs,es):
                if len(es)==4:
                    need(not all(colors[e] for e in es) or len({colors[e] for e in es})>=3,'D path star');return
                for z,e in adj[vs[-1]]:
                    if z not in vs:walk(vs+[z],es+[e])
                    elif len(es)==3 and z==vs[0]:
                        seq=es+[e];need(not all(colors[e] for e in seq) or len({colors[e] for e in seq})>=3,'D cycle star')
            for v in range(n):walk([v],[])
            partitions.append(parts)
        cl=closure(partitions[0]+partitions[1],{0});need(cl==set(range(L)),'exact unbounded closure')
        # A negative control for wrongly propagating via vertex intersection.
        singleton_parts=[[i] for i in range(L)]
        need(closure(singleton_parts,{0})=={0},'single-edge partitions do not spread')
        out.append({'q':q,'vertices':n,'edges':len(E),'closure_edges':len(cl),'both_D_star':True,'U_component_length':3})
    return out

def main():
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
    inp=json.loads((HERE/'opg37271-c26-input.json').read_text());tab=json.loads((HERE/'opg37271-c26-search-result.json').read_text());scope=sys.argv[1] if len(sys.argv)>1 else 'case'
    if scope in ('K4','K33','prism'):
        d=next(x for x in inp['graphs'] if x['name']==scope);out=check_catalog(Graph(d['n'],d['edges']),tab[scope]);out['verdict']='candidate_only';print(json.dumps(out,sort_keys=True));return
    o=inp['case'];g=Graph(o['n'],o['edges']);w=o['word'];summary=check_patches(g,w,tab[o['name']],4);core=g.minimal_core(w);need(core['row_count']==2,'minimum core length')
    S=set(o['selected_support']);mask=sum(1<<e for e in S);row=next(q for q in tab[o['name']]['rows'] if q[0]==mask and q[1]==0);new=list(map(int,row[5]));nw=[x if x<=4 else 0 for x in new];a=profile(g,w,S);b=profile(g,nw,S)
    need(a['boundary_paths']==b['boundary_paths'] and a['values']==[1,1] and b['values']==[0,0],'strict profiles')
    # Real graph rows, not inferred solely from old result files.
    rows=g.rows(w);costs=g.costs(w)
    for p,v in enumerate(costs):
        need(sum(((p>>q['i']&1)^(p>>q['j']&1))!=q['rhs'] for q in rows)==v,'geometric row costs')
    cut=[]
    for p in range(len(costs)):
        if costs[p]!=min(costs):continue
        for A in range(len(costs)):
            lhs=sum((1 if ((p>>q['i']&1)^(p>>q['j']&1))==q['rhs'] else -1) for q in rows if (A>>q['i']&1)!=(A>>q['j']&1))
            need(lhs==costs[p^A]-costs[p] and lhs>=0,'cut optimality');cut.append([p,A,lhs])
    dp_cases=0
    for r in range(3,9):
        for seed in range(32):
            weights=[1+(seed+3*i)%4 for i in range(r)];signs=[(seed>>i%5)&1 for i in range(r)];signs[-1]^=1^(sum(signs)%2)
            fields=[[(seed+i)%3,(2*seed+i)%4] for i in range(r)]
            exact=min(sum(fields[i][x[i]]+weights[i]*((x[i]^x[(i+1)%r])!=signs[i]) for i in range(r)) for x in product((0,1),repeat=r))
            need(cycle_dp(weights,signs,fields)==exact,'cycle transfer');dp_cases+=1
    # Enumerate the complete single-U-component replacement, with boundary P=0.
    S0={4,6,10};base=g.decode(w,0);forced=[]
    for colors in product(range(1,7),repeat=3):
        candidate=base.copy()
        for e,color in zip(sorted(S0),colors):candidate[e]=color
        try:g.endpoint(w,candidate,S0)
        except ValueError:continue
        violations=[W for W in g.shapes if len({candidate[e] for e in W['edges']})==2]
        need(len(violations)==g.pair_cost(candidate),'forced port witness count')
        forced.append({'inside_colors':list(colors),'full_colors':candidate,'cost':len(violations),'violations':violations})
    need(len(forced)==8 and min(t['cost'] for t in forced)==1,'complete forced port table')
    one_edge_family=[]
    for phase in range(4):
        count,value,colors=g.family(w,phase,{7})
        one_edge_family.append({'old_phase':phase,'endpoint_count':count,'minimum':value,'attainer':colors[0]})
    need([r['minimum'] for r in one_edge_family]==[1,0,0,1],'full migration envelope')
    out={'verdict':'candidate_only','state':'NONTERMINAL_CHECKPOINT','best_verified_result':'none','summary':summary,'old':{'n':g.n,'edges':g.E,'word':w,'paths':g.frame(w),'costs':costs,'rows':rows,'minimum_core':core},'exchange':{'support':sorted(S),'new_word':nw,'new_colors':new,'new_paths':g.frame(nw),'old_profile':a,'new_profile':b},'cut_checks':cut,'weighted_cycle_checks':dp_cases,'forced_component_family':forced,'single_D_edge_envelope':one_edge_family,'closure_family_checks':closure_family_tests()}
    raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();(HERE/'opg37271-c26-certificate.json').write_bytes(raw);print(json.dumps({'verdict':'candidate_only','certificate_sha256':digest(raw),'summary':summary,'weighted_cycle_checks':dp_cases},sort_keys=True))
if __name__=='__main__':main()
