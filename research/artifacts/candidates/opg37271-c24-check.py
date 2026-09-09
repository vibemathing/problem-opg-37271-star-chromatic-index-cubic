"""C24 alternate complete-space check. Standard library; no candidate imports.
Generates U subsets and D set-partitions; graph paths by vertex sequences.
"""
from itertools import combinations,permutations
from collections import deque,Counter
from pathlib import Path
import sys,json,hashlib

def need(t,s):
    if not t: raise ValueError(s)

def norm(w):
    lookup={0:0};out=[]
    for a in w:
        if a not in lookup:lookup[a]=len(lookup)
        out.append(lookup[a])
    return tuple(out)

def code(w):
    z=0
    for a in w:z=5*z+a
    return z

def word(z,m):
    a=[]
    for _ in range(m):a.append(z%5);z//=5
    need(z==0,'code overflow');return tuple(reversed(a))

class Model:
    def __init__(self,n,E):
        need(n<=10 and len(E)<=15,'caps')
        self.n=n;self.E=[tuple(e) for e in E];self.m=len(E);self.by=[[] for _ in range(n)];lookup={}
        for i,(a,b) in enumerate(E):
            need(0<=a<b<n and (a,b) not in lookup,'simple graph')
            lookup[a,b]=i;self.by[a].append(i);self.by[b].append(i)
        need(all(len(v)<=3 for v in self.by),'subcubic')
        self.adj=[{f for v in e for f in self.by[v]}-{i} for i,e in enumerate(self.E)]
        self.shapes=[]
        for k in (4,5):
            for vs in permutations(range(n),k):
                if k==5 and vs[0]>vs[-1]:continue
                if k==4 and (vs[0]!=min(vs) or vs[1]>vs[-1]):continue
                pairs=list(zip(vs,vs[1:]))+([(vs[-1],vs[0])] if k==4 else [])
                pairs=[tuple(sorted(e)) for e in pairs]
                if all(e in lookup for e in pairs):self.shapes.append(dict(kind='cycle' if k==4 else 'path',vertices=list(vs),edges=[lookup[e] for e in pairs]))
        self.cache={}

    def topology(self,mask):
        if mask in self.cache:return self.cache[mask]
        left={v for e,(a,b) in enumerate(self.E) if mask>>e&1 for v in (a,b)};parts=[]
        while left:
            root=min(left);vs={root};q=[root]
            while q:
                v=q.pop()
                for e in self.by[v]:
                    if mask>>e&1:
                        u=self.E[e][0]^self.E[e][1]^v
                        if u not in vs:vs.add(u);q.append(u)
            es={e for v in vs for e in self.by[v] if mask>>e&1};ends=sorted(v for v in vs if sum(mask>>e&1 for e in self.by[v])==1)
            if len(es)>3 or len(vs)!=len(es)+1 or len(ends)!=2 or any(sum(mask>>e&1 for e in self.by[v])>2 for v in vs):self.cache[mask]=None;return None
            at=ends[0];seq=[]
            while len(seq)<len(es):
                e=next(e for e in self.by[at] if e in es and e not in seq);seq.append(e);at=self.E[e][0]^self.E[e][1]^at
            parts.append(seq);left-=vs
        parts.sort(key=min);owner={e:(i,p%2) for i,P in enumerate(parts) for p,e in enumerate(P)};K=1<<len(parts)
        pattern={}
        for e,f in combinations(owner,2):
            i,p=owner[e];j,q=owner[f]
            pattern[min(e,f),max(e,f)]=sum(1<<s for s in range(K) if ((s>>i&1)^p)==((s>>j&1)^q))
        fixed=[];mixed=[]
        for shape in self.shapes:
            es=shape['edges'];pos=[j for j,e in enumerate(es) if mask>>e&1]
            if not pos:fixed.append(es)
            elif pos in ([0,2],[1,3]):
                a,b=[e for j,e in enumerate(es) if j not in pos];e,f=sorted(es[j] for j in pos);mixed.append((a,b,pattern[e,f],shape))
        out=(parts,owner,K,fixed,mixed);self.cache[mask]=out;return out

    def proper(self,w):return all(len([w[e] for e in ns if w[e]])==len({w[e] for e in ns if w[e]}) for ns in self.by)
    def valid(self,w):
        if len(w)!=self.m or any(type(a)is not int or not 0<=a<=4 for a in w):return False
        t=self.topology(sum(1<<e for e,a in enumerate(w) if a==0))
        return t is not None and self.proper(w) and all(w[e[0]]!=w[e[2]] or w[e[1]]!=w[e[3]] for e in t[3])
    def costs(self,w):
        need(self.valid(w),'preframe premise');t=self.topology(sum(1<<e for e,a in enumerate(w) if not a));masks=[p for a,b,p,_ in t[4] if w[a]==w[b]]
        return [sum(p>>s&1 for p in masks) for s in range(t[2])]
    def decode(self,w,s):
        t=self.topology(sum(1<<e for e,a in enumerate(w) if not a));need(t is not None and 0<=s<t[2],'phase');out=list(w)
        for e,(i,p) in t[1].items():out[e]=5+((s>>i&1)^p)
        return out
    def direct_cost(self,full):
        need(len(full)==self.m and all(type(a)is int and 1<=a<=6 for a in full) and self.proper(full),'full proper palette')
        return sum(len({full[e] for e in sh['edges']})==2 for sh in self.shapes)
    def all_states(self):
        st={};phase_trials=0
        for mask in range(1<<self.m):
            t=self.topology(mask)
            if t is None:continue
            # Descending D-edge order and set partitions, unlike prefix-zero search.
            D=[e for e in reversed(range(self.m)) if not(mask>>e&1)];w=[0]*self.m;complete={e:[] for e in D}
            for shape in t[3]:complete[min(shape)].append(shape)
            def partition(j,used):
                nonlocal phase_trials
                if j==len(D):
                    masks=[p for a,b,p,_ in t[4] if w[a]==w[b]]
                    costs=[sum(p>>s&1 for p in masks) for s in range(t[2])];c=code(norm(w));need(c not in st,'duplicate orbit');st[c]=min(costs);phase_trials+=len(costs);return
                e=D[j];blocked={w[f] for f in self.adj[e] if w[f]}
                for a in range(1,min(4,used+1)+1):
                    if a in blocked:continue
                    w[e]=a
                    if all(w[s[0]]!=w[s[2]] or w[s[1]]!=w[s[3]] for s in complete[e]):partition(j+1,max(a,used))
                w[e]=0
            partition(0,0)
        return st,phase_trials
    def neighbors(self,w,st):
        out={}
        for e,old in enumerate(w):
            for a in range(5):
                if a==old:continue
                v=list(w);v[e]=a;q=code(norm(v))
                if q!=code(w) and q in st:out.setdefault(q,(e,a))
        return out


def check(tag):
    here=Path(__file__).parent;data=list(map(int,(here/(tag+'.txt')).read_text().split()));n,m=data[:2];E=list(zip(data[2::2],data[3::2]));g=Model(n,E)
    rows=[list(map(int,s.split())) for s in (here/(tag+'.states')).read_text().splitlines()];need(len({r[0] for r in rows})==len(rows),'unique state records')
    st,trials=g.all_states();need(st=={r[0]:r[1] for r in rows},'complete state/mu coverage')
    adj={};raw=0;phase_checks=0;hist=Counter();parent={r[0]:r for r in rows}
    for r in rows:
        z,mu,phase,to,dist,block=r;w=word(z,m);q=max(w);orbit=1
        for k in range(q):orbit*=4-k
        raw+=orbit;hist[mu]+=1;costs=g.costs(w);need(costs[phase]==mu,'optimal phase');need(g.direct_cost(g.decode(w,phase))==mu,'actual-color check')
        phase_checks+=len(costs);adj[z]=g.neighbors(w,st)
        if dist>=0:
            if mu==0:need(to==z and dist==0,'balanced parent')
            else:need(to in adj[z] and st[to]<=mu and parent[to][4]==dist-1,'descending parent chain')
    unseen={z for z in st if st[z]>0};blocks=[]
    while unseen:
        seed=min(unseen);part={seed};todo=[seed];unseen.remove(seed)
        while todo:
            for v in adj[todo.pop()]:
                if v in unseen and st[v]==st[seed]:unseen.remove(v);part.add(v);todo.append(v)
        exits=[(u,v) for u in sorted(part) for v in adj[u] if st[v]<st[u]]
        blocks.append(dict(level=st[seed],size=len(part),representative=seed,exit=None if not exits else list(exits[0]),closed_members=sorted(part) if not exits else None))
    closed=[b for b in blocks if b['exit'] is None];bad={z for b in closed for z in b['closed_members']}
    need(all(parent[z][4]==-1 for z in bad),'closed block has no parent escape')
    # Independent reverse reachability, rather than trusting parent absence.
    reached={z for z in st if st[z]==0};todo=deque(reached)
    while todo:
        u=todo.popleft()
        for v in adj[u]:
            if v not in reached and st[v]>=st[u]:reached.add(v);todo.append(v)
    need({r[0] for r in rows if r[4]>=0}==reached,'exact reachability')
    compact=''.join(f'{z} {st[z]}\n' for z in sorted(st)).encode()
    out=dict(verdict='candidate_only',tag=tag,n=n,edges=E,states=len(st),raw_frames=raw,phase_trials=trials,direct_optimal_color_checks=len(st),positive_blocks=len(blocks),closed_blocks=closed,unreachable=len(st)-len(reached),mu_histogram=dict(hist),state_mu_sha256=hashlib.sha256(compact).hexdigest(),state_stream_sha256=hashlib.sha256((here/(tag+'.states')).read_bytes()).hexdigest(),all_blocks=blocks)
    (here/(tag+'.checked.json')).write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('all_blocks','edges','closed_blocks')},sort_keys=True));return out
if __name__=='__main__':check(sys.argv[1])
