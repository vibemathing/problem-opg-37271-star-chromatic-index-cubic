"""Bounded positive-palette and explicit-template checks; candidate_only."""
from __future__ import annotations
import itertools as it, json, resource, signal, sys
from pathlib import Path

def require(ok,msg):
    if not ok: raise ValueError(msg)

def subsets(xs,max_size):
    return [set(s) for j in range(max_size+1) for s in it.combinations(xs,j)]

def is_star(n,es,cs):
    require(len(es)==len(cs),'colors length')
    require(len({tuple(sorted(e)) for e in es})==len(es),'parallel edge')
    adj=[[] for _ in range(n)]
    for i,(x,y) in enumerate(es):
        require(0<=x<n and 0<=y<n and x!=y,'endpoints')
        adj[x].append((y,i));adj[y].append((x,i))
    for xs in adj:
        if len({cs[e] for _,e in xs})!=len(xs):return False
    # Explicit simple paths of four edges and four-cycles, not just a tree test.
    def walk(v,vs,cols):
        if len(cols)==4:return len(set(cols))>2
        for w,e in adj[v]:
            if w==vs[0] and len(cols)==3:
                if len(set(cols+[cs[e]]))<=2:return False
            elif w not in vs and not walk(w,vs+[w],cols+[cs[e]]):return False
        return True
    return all(walk(v,[v],[]) for v in range(n))

def bridge_palettes(k):
    colors=range(1,k);sets=subsets(colors,2);cases=0
    for U,V in it.product(sets,repeat=2):
        found=False
        for p in it.permutations(colors):
            image={p[v-1] for v in V}
            if not U & image:found=True;break
        require(found,'bridge palette obstruction');cases+=1
    return cases

def triangle_palettes():
    C=set(range(1,7));a=1
    options=[(0,set())]
    for b in C-{a}:
        options += [(b,{b}|R) for R in subsets(sorted(C-{b}),2)]
    count=0
    for (b,P),(c,Q) in it.product(options,repeat=2):
        if a not in P:
            alpha=min(C-(P|{a,c}))
            beta=min(C-(Q|{a,c,alpha}))
        else:
            beta=min(C-(Q|{a,b}))
            alpha=min(C-(P|{c,beta}))
        require(alpha not in P|{a,c},'alpha guard')
        require(beta not in Q|{a,alpha},'beta guard')
        require(beta!=b or a not in P,'cross guard')
        count+=1
    return count

def cube():
    mult2=[0,2,3,1]
    es=[(i,4+j) for i in range(4) for j in range(4) if i!=j]
    cs=[1+(i^mult2[j-4]) for i,j in es]
    require(is_star(8,es,cs),'cube template')
    return es,cs

def pullback_tree(n,edges):
    template,tcolors=cube();tadj=[[] for _ in range(8)];tc={}
    for e,c in zip(template,tcolors):
        x,y=e;tadj[x].append(y);tadj[y].append(x);tc[tuple(sorted(e))]=c
    adj=[[] for _ in range(n)]
    for e,(x,y) in enumerate(edges):adj[x].append((y,e));adj[y].append((x,e))
    require(len(edges)==n-1 and max(map(len,adj))<=3,'tree shape')
    image={0:0};q=[0];parent={0:-1};colors=[None]*len(edges)
    for x in q:
        choices=[z for z in sorted(tadj[image[x]]) if z!=image.get(parent[x])]
        children=[(y,e) for y,e in adj[x] if y!=parent[x]]
        require(len(choices)>=len(children),'template degree')
        for (y,e),z in zip(children,choices):
            require(y not in image,'cycle');image[y]=z;parent[y]=x;q.append(y)
            colors[e]=tc[tuple(sorted((image[x],z)))]
    require(len(image)==n and is_star(n,edges,colors),'pullback coloring')
    return colors,[image[i] for i in range(n)]

def completion(n,edges):
    deg=[0]*n
    for x,y in edges:deg[x]+=1;deg[y]+=1
    require(max(deg,default=0)<=3,'subcubic input')
    J=[[],[(0,1),(2,3)],[(0,1),(1,2),(2,3),(3,0)],list(it.combinations(range(4),2))]
    out=[(4*x+i,4*y+i) for x,y in edges for i in range(4)]
    for x in range(n):out += [(4*x+i,4*x+j) for i,j in J[3-deg[x]]]
    require(len(set(tuple(sorted(e)) for e in out))==len(out),'completion simple')
    dd=[0]*(4*n)
    for x,y in out:require(x!=y,'loop');dd[x]+=1;dd[y]+=1
    require(all(d==3 for d in dd),'completion regular')
    for i in range(4):
        restriction={tuple(sorted((x//4,y//4))) for x,y in out if x%4==i and y%4==i}
        require(restriction==set(tuple(sorted(e)) for e in edges),'induced copy')
    return len(out)

def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall limit')));signal.alarm(20)
    resource.setrlimit(resource.RLIMIT_CPU,(20,21));resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
    es,cs=cube();cert=json.loads(Path(sys.argv[1]).read_text())
    tree=[e[:2] for e in cert['edges']];fresh,images=pullback_tree(len(cert['vertices']),tree)
    cycles=0
    for n in range(3,61):
        q,r=divmod(n,3);word=[1,2,3]*q+([] if r==0 else [4] if r==1 else [4,2])
        ee=[(i,(i+1)%n) for i in range(n)]+[(i,n+i) for i in range(n)]
        require(is_star(2*n,ee,word+[5]*n),'cycle with leaves');cycles+=1
    completions=[]
    for n,e in [(1,[]),(2,[(0,1)]),(4,[(0,1),(0,2),(0,3)]),(4,list(it.combinations(range(4),2))),(66,tree)]:
        completions.append({'input_vertices':n,'output_vertices':4*n,'output_edges':completion(n,e)})
    print(json.dumps({'verdict':'candidate_only','python':sys.version.split()[0],
        'bridge_palette_cases':{str(k):bridge_palettes(k) for k in (5,6)},
        'triangle_palette_cases':triangle_palettes(),'cube_edges':es,'cube_colors':cs,
        'tree_vertices':len(cert['vertices']),'fresh_tree_colors':fresh,'template_vertex_images':images,
        'old_colors_changed_by_fresh_coloring':sum(fresh[i]!=cert['edges'][i][2] for i in range(1,len(tree))),
        'cycle_leaf_cases_checked':cycles,'completion_cases':completions},sort_keys=True))

if __name__=='__main__':main()
