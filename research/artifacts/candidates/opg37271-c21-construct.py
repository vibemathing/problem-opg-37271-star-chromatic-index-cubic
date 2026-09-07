"""Constructive outer frames; no imports from C19/C20."""
from itertools import product

def require(ok,msg):
    if not ok: raise ValueError(msg)

def edge(a,b): return tuple(sorted((a,b)))

def graph(cycles, matching):
    n=sum(map(len,cycles)); E=[]
    require(sorted(v for C in cycles for v in C)==list(range(n)), 'cycle partition')
    for C in cycles:
        require(len(C)>=3,'cycle length')
        E += [edge(C[i],C[(i+1)%len(C)]) for i in range(len(C))]
    M=[edge(*e) for e in matching]
    require(len(M)*2==n and sorted(v for e in M for v in e)==list(range(n)), 'perfect matching')
    require(len(set(E+M))==len(E)+len(M), 'simple cubic graph')
    return n,E+M

def square_frame(cycles,matching):
    require(all(len(C)==4 for C in cycles),'square factor')
    n,E=graph(cycles,matching)
    O=[edge(C[i],C[i+2]) for C in cycles for i in (0,1)]
    adj=[[] for _ in range(n)]
    # Typed parallel edges must be retained.
    for a,b in list(matching)+O:adj[a].append(b);adj[b].append(a)
    bit=[None]*n
    for s in range(n):
        if bit[s] is not None:continue
        bit[s]=0;todo=[s]
        while todo:
            a=todo.pop()
            for b in adj[a]:
                if bit[b] is None:bit[b]=1-bit[a];todo.append(b)
                else:require(bit[b]!=bit[a],'auxiliary even-cycle parity')
    U=[i for i,(a,b) in enumerate(E) if bit[a]==bit[b]]
    require(all(i<n for i in U),'matching is crossing')
    require(sorted(v for i in U for v in E[i])==list(range(n)),'U perfect matching')
    D=set(range(len(E)))-set(U); d_adj=[[] for _ in range(n)]
    for i in D:
        a,b=E[i];d_adj[a].append((b,i));d_adj[b].append((a,i))
    colors=[0]*len(E);seen=set();d_cycles=[]
    for s in range(n):
        if s in seen:continue
        v=s;last=-1;ids=[]
        while True:
            seen.add(v)
            w,i=min((w,i) for w,i in d_adj[v] if i!=last)
            ids.append(i);last=i;v=w
            if v==s:break
            require(v not in seen,'D cycle traversal')
        m=len(ids);require(m>=4 and m%2==0,'even D cycle')
        s4={0:0,1:1,2:2}[m%3];r=(m-4*s4)//3
        require(r>=0 and 3*r+4*s4==m,'block decomposition')
        word=[1,2,3]*r+[1,2,1,3]*s4
        for i,c in zip(ids,word):colors[i]=c
        d_cycles.append(ids)
    for i in U:colors[i]=5+bit[E[i][0]]
    return {'n':n,'edges':E,'cycles':cycles,'matching':matching,'bits':bit,'U':U,'D_cycles':d_cycles,'colors':colors}

def conflict_coloring(cycles,matching):
    n,E=graph(cycles,matching);k=len(matching)
    owner={v:i for i,e in enumerate(matching) for v in e}
    neighbors=[set() for _ in range(k)]
    for a,b in E[:n]:
        i,j=owner[a],owner[b];require(i!=j,'F edge in matching')
        neighbors[i].add(j);neighbors[j].add(i)
    val=[0]*k
    def assign(i):
        if i==k:return val.copy()
        for c in range(1,min(4,max(val[:i],default=0)+1)+1):
            if any(val[j]==c for j in neighbors[i]):continue
            val[i]=c;x=assign(i+1)
            if x is not None:return x
        val[i]=0
        return None
    return assign(0),neighbors

def local_specials(word):
    m=len(word);require(m in (3,5),'C3 or C5')
    require(all(word[i]!=word[(i+1)%m] for i in range(m)) and set(word)<=set(range(1,5)),'proper labels')
    if m==3:return [(0,next(c for c in range(1,5) if c not in word))]
    # Deterministic small palette construction via the proof's two normal forms.
    if len(set(word))==3:
        a=next(c for c in word if word.count(c)==1);z=word.index(a)
        d=next(c for c in range(1,5) if c not in word)
        return [((z+2)%5,a),((z+4)%5,d)]
    require(len(set(word))==4,'pentagon multiplicities')
    for z in range(5):
        for direction in (1,-1):
            inds=[(z+direction*j)%5 for j in range(5)];w=[word[i] for i in inds]
            if w[0]==w[2]:
                # Edges 0-1 and 3-4 in this orientation; convert to old cyclic edge indices.
                return [(inds[0] if direction==1 else inds[1],w[3]),
                        (inds[3] if direction==1 else inds[4],w[1])]
    raise ValueError('normal form')

def odd35_frame(cycles,matching,labels=None):
    require(all(len(C) in (3,5) for C in cycles),'C3/C5 factor')
    n,E=graph(cycles,matching)
    if labels is None:labels,_=conflict_coloring(cycles,matching)
    require(labels is not None,'K5 exception needs separate coloring')
    require(len(labels)==len(matching) and all(c in range(1,5) for c in labels),'matching palette')
    lam={v:c for e,c in zip(matching,labels) for v in e}
    require(all(lam[a]!=lam[b] for a,b in E[:n]),'strong matching coloring')
    colors=[0]*n+list(labels);S=[];off=0
    for C in cycles:
        for j,c in local_specials([lam[v] for v in C]):
            colors[off+j]=c;S.append(off+j)
        off+=len(C)
    U=[i for i,c in enumerate(colors) if c==0]
    # Alternation on the remaining path components, each length at most two.
    a=[[] for _ in range(n)]
    for i in U:
        u,v=E[i];a[u].append((v,i));a[v].append((u,i))
    for s in range(n):
        if len(a[s])!=1 or colors[a[s][0][1]]:continue
        v=s;last=-1;t=0
        while True:
            nxt=[(w,i) for w,i in a[v] if i!=last]
            if not nxt:break
            w,i=nxt[0];require(colors[i]==0,'U component repeated');colors[i]=5+t
            t^=1;last=i;v=w
    require(all(colors),'uncolored edge')
    return {'n':n,'edges':E,'cycles':cycles,'matching':matching,'matching_colors':labels,'S':S,'U':U,'colors':colors}

def full_coloring_search(n,E,fixed):
    """Small finite exception only; standard-library constrained search, no XOR code."""
    adj=[[] for _ in range(n)]
    for i,(a,b) in enumerate(E):adj[a].append(i);adj[b].append(i)
    colors=list(fixed);nodes=0
    def safe(e,c):
        if any(colors[f]==c for v in E[e] for f in adj[v] if f!=e):return False
        colors[e]=c
        for d in range(1,7):
            if d==c:continue
            reached={e};todo=[e]
            while todo:
                f=todo.pop()
                for v in E[f]:
                    for g in adj[v]:
                        if colors[g] in (c,d) and g not in reached:reached.add(g);todo.append(g)
            if len(reached)>=4:colors[e]=0;return False
        colors[e]=0;return True
    def rec():
        nonlocal nodes
        nodes+=1;require(nodes<=100000,'search node bound')
        un=[e for e,c in enumerate(colors) if c==0]
        if not un:return colors.copy()
        options=[]
        for e in un:
            cs=[c for c in range(1,7) if safe(e,c)]
            if not cs:return None
            options.append((len(cs),e,cs))
        _,e,cs=min(options)
        for c in cs:
            colors[e]=c;ans=rec()
            if ans is not None:return ans
        colors[e]=0;return None
    return rec(),nodes



def general_preframe(n,E):
    """Every simple cubic graph: bipartite double cover -> short path factor."""
    require(type(n)is int and n>=0 and len({edge(a,b) for a,b in E})==len(E),'simple input')
    adj=[[] for _ in range(n)]
    for i,(a,b) in enumerate(E):
        require(0<=a<n and 0<=b<n and a!=b,'endpoints')
        adj[a].append(b);adj[b].append(a)
    require(all(len(ns)==3 for ns in adj),'cubic input')
    right=[None]*n
    def augment(v,seen):
        for w in sorted(adj[v]):
            if w in seen:continue
            seen.add(w)
            if right[w] is None or augment(right[w],seen):right[w]=v;return True
        return False
    for v in range(n):require(augment(v,set()),'regular bipartite matching')
    succ=[None]*n
    for w,v in enumerate(right):succ[v]=w
    require(sorted(succ)==list(range(n)),'permutation')
    lookup={edge(a,b):i for i,(a,b) in enumerate(E)};seen=set();U=[];cycle_records=[]
    for v in range(n):
        if v in seen:continue
        C=[];w=v
        while w not in seen:seen.add(w);C.append(w);w=succ[w]
        require(w==v and len(C)>=2,'permutation cycle')
        cycle_records.append(C)
        start=0
        if len(C)%2:
            U += [lookup[edge(C[0],C[1])],lookup[edge(C[1],C[2])]];start=3
        for j in range(start,len(C),2):U.append(lookup[edge(C[j],C[j+1])])
    U=set(U);da=[[] for _ in range(n)]
    for i,(a,b) in enumerate(E):
        if i not in U:da[a].append((b,i));da[b].append((a,i))
    require(all(1<=len(ns)<=2 for ns in da),'D degree one or two')
    colors=[0]*len(E);remaining={i for i in range(len(E)) if i not in U}
    while remaining:
        seed=min(remaining);V=set(E[seed]);todo=list(V)
        while todo:
            for w,i in da[todo.pop()]:
                if w not in V:V.add(w);todo.append(w)
        ends=sorted(v for v in V if len(da[v])==1);v=ends[0] if ends else min(V);start=v;ids=[];last=-1
        while True:
            nxt=[(w,i) for w,i in da[v] if i!=last]
            if not nxt:break
            w,i=min(nxt);ids.append(i);last=i;v=w
            if v==start:break
        if ends:word=([1,2,3]*((len(ids)+2)//3))[:len(ids)]
        elif len(ids)==5:word=[1,2,1,3,4]
        else:
            t={0:0,1:1,2:2}[len(ids)%3];r=(len(ids)-4*t)//3
            require(r>=0,'cycle block range');word=[1,2,3]*r+[1,2,1,3]*t
        for i,c in zip(ids,word):colors[i]=c
        remaining-=set(ids)
    return {'n':n,'edges':E,'successor':succ,'permutation_cycles':cycle_records,'U':sorted(U),'partial_colors':colors}



def odd35_coloring(cycles,matching,exception_rows):
    """Componentwise unconditional constructor; finite K5 table is explicit input."""
    require(all(len(C) in (3,5) for C in cycles),'odd factor lengths')
    n,E=graph(cycles,matching);adj=[[] for _ in range(n)]
    for a,b in E:adj[a].append(b);adj[b].append(a)
    lookup={e:i for i,e in enumerate(E)};full=[0]*len(E);unseen=set(range(n))
    while unseen:
        start=min(unseen);V={start};todo=[start]
        while todo:
            for w in adj[todo.pop()]:
                if w not in V:V.add(w);todo.append(w)
        unseen-=V;Cs=[C for C in cycles if C[0] in V]
        old=[v for C in Cs for v in C];new={v:i for i,v in enumerate(old)}
        lc=[[new[v] for v in C] for C in Cs];lm=[edge(new[a],new[b]) for a,b in matching if a in V]
        labels,conf=conflict_coloring(lc,lm);ln,le=graph(lc,lm)
        if labels is not None:cols=odd35_frame(lc,lm,labels)['colors']
        else:
            require(list(map(len,lc))==[5,5] and len(lm)==5 and all(len(ns)==4 for ns in conf),'exact K5 exception shape')
            mate={a:b for e in lm for a,b in (e,e[::-1])}
            require(all(5<=mate[i]<10 for i in range(5)),'exception matching crosses cycles')
            perm=[mate[i]-5 for i in range(5)]
            entry=next((r for r in exception_rows if r['permutation']==perm),None)
            require(entry is not None,'missing exception table row')
            _,ce=graph(lc,[(i,mate[i]) for i in range(5)])
            table=dict(zip(ce,entry['colors']));cols=[table[e] for e in le]
        for e,c in zip(le,cols):full[lookup[edge(old[e[0]],old[e[1]])]]=c
    require(all(full),'full component coverage')
    return {'n':n,'edges':E,'cycles':cycles,'matching':matching,'colors':full}


def stress_stream(spec,exception_rows):
    """Finite interface stress only. Domain is supplied by the frozen input JSON."""
    def all_mates(left,forbidden):
        if not left:yield [];return
        a=left[0]
        for b in left[1:]:
            if edge(a,b) not in forbidden:
                for M in all_mates([v for v in left[1:] if v!=b],forbidden):yield [(a,b)]+M
    groups=[]
    for kind,lengths in [('square',[4]*k) for k in spec['square_cycle_counts']]+[('odd35',x) for x in spec['odd_factor_lengths']]:
        cycles=[];n=0
        for m in lengths:cycles.append(list(range(n,n+m)));n+=m
        F={edge(C[i],C[(i+1)%len(C)]) for C in cycles for i in range(len(C))}
        rows=[]
        for M in all_mates(list(range(n)),F):
            out=(square_frame if kind=='square' else odd35_frame)(cycles,M)
            rows.append({'matching':M,'colors':out['colors']})
        groups.append({'kind':kind,'cycles':cycles,'rows':rows})
    cycles=[list(range(5)),list(range(5,10))];F={edge(C[i],C[(i+1)%5]) for C in cycles for i in range(5)};rows=[]
    for M in all_mates(list(range(10)),F):
        out=odd35_coloring(cycles,M,exception_rows);rows.append({'matching':M,'colors':out['colors']})
    groups.append({'kind':'odd35_full','cycles':cycles,'rows':rows})
    words=[{'word':list(w),'specials':local_specials(w)} for m in spec['word_lengths'] for w in product(spec['word_palettes'],repeat=m) if all(w[i]!=w[(i+1)%m] for i in range(m))]
    preframes=[general_preframe(r['n'],r['edges']) for r in spec['general_cubic_inputs']]
    return {'verdict':'candidate_only','groups':groups,'local_words':words,'general_preframes':preframes}

if __name__=='__main__':
    import json,sys,resource,signal
    from pathlib import Path
    signal.alarm(35)
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,768*1024**2))
    raw=Path(sys.argv[1]).read_bytes();require(len(raw)<=65536,'input cap')
    spec=json.loads(raw)
    require(spec['square_cycle_counts']==[1,2,3] and spec['odd_factor_lengths']==[[3,3],[3,5],[3,3,3,3]],'frozen finite domain')
    exception_rows=json.loads(Path(__file__).with_name('opg37271-c21-certificate.json').read_text())['k5_exceptions']
    text=json.dumps(stress_stream(spec,exception_rows),sort_keys=True,separators=(',',':'))+'\n'
    require(len(text.encode())<=1048576,'stream cap')
    print(text,end='')
