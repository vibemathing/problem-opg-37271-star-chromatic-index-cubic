"""Bounded, stdlib-only generator-side audit of the height-four witness."""
import itertools, json, resource, signal

def require(ok, msg):
    if not ok: raise ValueError(msg)

def witness():
    es=[['v','u',0],['u','x',1],['u','y',2],['x','a',3],['x','b',4],['y','c',5],['y','d',6]]
    for i,A,B,L,R in [('a',1,2,5,6),('b',1,3,3,5),('c',2,1,3,4),('d',2,5,5,3)]:
        es += [[i,'z'+i,A],['z'+i,'l'+i,L],['z'+i,'r'+i,R],[i,'w'+i,B]]
    es += [['wb','tb',2],['wb','sb',6],['wd','td',1],['wd','sd',4]]
    return es

def star(es, colors, omit_leaf=False):
    maxima={}
    for a,b in itertools.combinations(range(1,7),2):
        adj={}
        for i,(x,y,_) in enumerate(es):
            if omit_leaf and i==0: continue
            c=colors[i]
            if c not in (a,b): continue
            adj.setdefault(x,[]).append((y,c));adj.setdefault(y,[]).append((x,c))
        if any(len(ns)>2 or len(set(c for y,c in ns))!=len(ns) for ns in adj.values()):return None
        seen=set(); longest=0
        for x in adj:
            if x in seen:continue
            todo=[x]; degree_sum=0
            while todo:
                y=todo.pop()
                if y in seen:continue
                seen.add(y);degree_sum+=len(adj[y]);todo.extend(z for z,c in adj[y] if z not in seen)
            longest=max(longest,degree_sum//2)
        if longest>3:return None
        maxima[f'{a},{b}']=longest
    return maxima

def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall limit')));signal.alarm(20)
    resource.setrlimit(resource.RLIMIT_CPU,(20,21));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
    es=witness();old=[c for x,y,c in es];adj={}
    for x,y,c in es:adj.setdefault(x,[]).append(y);adj.setdefault(y,[]).append(x)
    require(len(es)==27 and len(adj)==28,'size')
    require(all(len(ns)<=3 for ns in adj.values()),'maximum degree')
    require(len({tuple(sorted((x,y))) for x,y,c in es})==len(es),'simplicity')
    dist={'u':0};queue=['u']
    for x in queue:
        for y in adj[x]:
            if y not in dist:dist[y]=dist[x]+1;queue.append(y)
    require(len(dist)==len(adj) and len(es)==len(adj)-1,'tree')
    require(max(dist.values())==4 and len(adj['v'])==1,'height and leaf')
    before=star(es,old,True);require(before is not None,'old coloring')
    critical=[1,2,3,4,5,6,7,11,15,19]
    frozen=0
    for e in critical:
        for c in range(1,7):
            if c==old[e]:continue
            colors=old.copy();colors[e]=c
            require(star(es,colors,True) is None,'critical edge not frozen')
        frozen+=1
    trials=0;valid=0
    for t in range(1,7):
        colors=old.copy();colors[0]=t;trials+=1;valid+=star(es,colors) is not None
        for e in range(1,len(es)):
            for c in range(1,7):
                if c==old[e]:continue
                colors=old.copy();colors[0]=t;colors[e]=c;trials+=1
                valid+=star(es,colors) is not None
    require(valid==0 and trials==786,'one-edit exhaustive test')
    colors=old.copy();colors[0]=1;colors[1]=3;colors[3]=5
    after=star(es,colors);require(after is not None,'two-edit extension')
    require(sum(a!=b for a,b in zip(old[1:],colors[1:]))==2,'edit count')
    report={'verdict':'candidate_only','vertices':len(adj),'edges':len(es),'height_from_u':4,
        'critical_edges_frozen':frozen,'old_edge_alternatives_checked':50,
        'zero_or_one_edit_trials':trials,'successful_trials':valid,
        'old_pair_max_lengths':before,'final_pair_max_lengths':after,
        'changes':[['u','x',1,3],['x','a',3,5]],'leaf_color':1}
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
