"""C29 finite object generator. No previous candidate module is imported.
Shapes are constructed as connected four-edge subsets. Candidate only.
"""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
import json, hashlib

ROOT=Path(__file__).resolve().parent

def pack(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()

def shape_table(edges):
    ans=[]
    for inds in combinations(range(len(edges)),4):
        adj={}
        for e in inds:
            a,b=edges[e];adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
        degrees=sorted(len(t) for t in adj.values())
        if degrees not in ([1,1,2,2,2],[2,2,2,2]):continue
        reached={next(iter(adj))};todo=list(reached)
        while todo:
            for b in adj[todo.pop()]:
                if b not in reached:reached.add(b);todo.append(b)
        if len(reached)!=len(adj):continue
        cycle=len(adj)==4;start=min(adj) if cycle else min(v for v in adj if len(adj[v])==1)
        seq=[start];prev=None
        for _ in range(3 if cycle else 4):
            options=[v for v in adj[seq[-1]] if v!=prev and (v!=start or len(seq)==4)]
            v=min(options);prev=seq[-1];seq.append(v)
        ans.append({'kind':'cycle' if cycle else 'path','vertices':seq,'edges':list(inds)})
    return sorted(ans,key=lambda s:(s['kind'],s['vertices']))

def components(edges,word):
    adj={}
    for e,(a,b) in enumerate(edges):
        if word[e]==0:
            adj.setdefault(a,[]).append((b,e));adj.setdefault(b,[]).append((a,e))
    if any(len(t)>2 for t in adj.values()):return None
    unused={i for i,c in enumerate(word) if c==0};paths=[]
    while unused:
        first=min(unused);todo=list(edges[first]);vertices=set(todo);part=set()
        while todo:
            for b,e in adj[todo.pop()]:
                part.add(e)
                if b not in vertices:vertices.add(b);todo.append(b)
        if len(part)>3 or len(vertices)!=len(part)+1:return None
        v=min(a for a in vertices if len(adj[a])==1);ordered=[]
        while len(ordered)<len(part):
            b,e=next((b,e) for b,e in adj[v] if e not in ordered);ordered.append(e);v=b
        paths.append(ordered);unused-=part
    return paths

def proper(edges,word):
    used={}
    for (a,b),c in zip(edges,word):
        if c:
            if c in used.get(a,set()) or c in used.get(b,set()):return False
            used.setdefault(a,set()).add(c);used.setdefault(b,set()).add(c)
    return True

def frame(edges,word,shapes):
    if len(edges)!=len(word) or any(c not in range(5) for c in word) or not proper(edges,word):return None
    ps=components(edges,word)
    if ps is None:return None
    for s in shapes:
        cc={word[e] for e in s['edges']}
        if 0 not in cc and len(cc)==2:return None
    return ps

def phases(edges,word,paths,shapes):
    out=[]
    for bits in product((0,1),repeat=len(paths)):
        colors=list(word)
        for p,b in zip(paths,bits):
            for j,e in enumerate(p):colors[e]=5+(b^(j&1))
        bad=[i for i,s in enumerate(shapes) if len({colors[e] for e in s['edges']})==2]
        out.append({'bits':list(bits),'cost':len(bad),'bad':bad})
    return out

def decode(word,paths,bits):
    colors=list(word)
    for p,b in zip(paths,bits):
        for j,e in enumerate(p):colors[e]=5+(b^(j&1))
    return colors

def rows(edges,word,paths,shapes):
    lookup={tuple(e):i for i,e in enumerate(edges)}
    position={e:(i,j&1) for i,p in enumerate(paths) for j,e in enumerate(p)};out=[]
    for k,s in enumerate(shapes):
        vs=s['vertices'];pairs=list(zip(vs,vs[1:]))
        if s['kind']=='cycle':pairs.append((vs[-1],vs[0]))
        es=[lookup[tuple(sorted(p))] for p in pairs];zero=[i for i,e in enumerate(es) if word[e]==0]
        if zero not in ([0,2],[1,3]):continue
        ds=[e for e in es if word[e]!=0]
        if word[ds[0]]!=word[ds[1]]:continue
        (i,a),(j,b)=[position[es[z]] for z in zero]
        out.append({'shape':k,'variables':sorted([i,j]),'rhs':1^a^b,'D_edges':sorted(ds)})
    return out

def connected(edges,S):
    reached={min(S)};stack=list(reached)
    while stack:
        e=stack.pop()
        for f in S-reached:
            if set(edges[e])&set(edges[f]):reached.add(f);stack.append(f)
    return reached==S

def closed(paths,S):return all(not(set(p)&S) or set(p)<=S for p in paths)

def family(edges,word,S,shapes,old_paths,attainers):
    positions=sorted(S);out=[]
    for values in product(range(5),repeat=len(S)):
        new=list(word)
        for e,c in zip(positions,values):new[e]=c
        ps=frame(edges,new,shapes)
        if ps is None or not closed(ps,S):continue
        pp=phases(edges,new,ps,shapes);anchors=[]
        for a in attainers:
            old_colors=decode(word,old_paths,a)
            costs=[]
            for rec in pp:
                cols=decode(new,ps,rec['bits'])
                if all(cols[e]==old_colors[e] for e in range(len(edges)) if e not in S):costs.append(rec['cost'])
            assert costs
            anchors.append(min(costs))
        out.append({'word':new,'paths':ps,'phases':pp,'anchored_minima':anchors})
    return {'support':positions,'endpoints':out}

def minimum_families(edges,word,cap=2):
    shapes=shape_table(edges);ps=frame(edges,word,shapes);assert ps is not None
    old=phases(edges,word,ps,shapes);mu=min(r['cost'] for r in old);atts=[r['bits'] for r in old if r['cost']==mu]
    families=[];repairs=[];minimum=None
    for size in range(1,cap+1):
        for inds in combinations(range(len(edges)),size):
            S=set(inds)
            if not connected(edges,S) or not closed(ps,S):continue
            f=family(edges,word,S,shapes,ps,atts);families.append(f)
            for k,q in enumerate(f['endpoints']):
                if all(v<mu for v in q['anchored_minima']):repairs.append({'support':list(inds),'endpoint':k,'word':q['word']})
        if repairs:minimum=size;break
    return {'shapes':shapes,'paths':ps,'old_phases':old,'rows':rows(edges,word,ps,shapes),'mu':mu,'attainers':atts,'families':families,'repairs':repairs,'minimum_support':minimum}

def calculate(inp):
    E=list(map(tuple,inp['edges']));w=inp['old'];new=inp['new'];main=minimum_families(E,w)
    ss=main['shapes'];ps=main['paths'];assert frame(E,new,ss)==ps
    newph=phases(E,new,ps,ss)
    S={E.index(tuple(e)) for e in inp['joint_support']}
    H={E.index(tuple(e)) for e in inp['core_hull']};T=H|S
    touch=[i for i,s in enumerate(ss) if set(s['edges'])&S]
    transfer=[]
    for r,q in zip(main['old_phases'],newph):
        h=[i for i in r['bad'] if set(ss[i]['edges'])&T and not(set(ss[i]['edges'])&S)]
        hnew=[i for i in q['bad'] if set(ss[i]['edges'])&T and not(set(ss[i]['edges'])&S)]
        assert h==hnew
        a=sum(i in touch for i in r['bad']);b=sum(i in touch for i in q['bad'])
        transfer.append({'bits':r['bits'],'old_sigma':a,'new_sigma':b,'h':len(h),'h_shapes':h,'g':a-b})
    enlarged=[]
    for p,q in product((0,1),repeat=2):
        records=[r for r in transfer if r['bits'][1:]==[p,q]]
        m=min(r['old_sigma']+r['h'] for r in records)
        for r in records:r['r']=r['old_sigma']+r['h']-m;r['net']=r['g']-r['r']
        enlarged.append({'boundary':[p,q],'old':m,'new':min(r['new_sigma']+r['h'] for r in records),'gain':max(r['net'] for r in records)})
    # Complete passive completions: do not discard an existing graph edge in a proof.
    # This is a fixed thirteen-edge embedding family, not an all-graph census.
    base=list(zip(map(tuple,inp['fixed_edges']),inp['fixed_colors']))
    choices=[];excluded=[]
    target=Counter({(a,b,s):v for a,b,s,v in inp['exact_row_counts']})
    for colors in product(range(5),repeat=3):
        full=sorted(base+[(tuple(e),c) for e,c in zip(inp['passive_candidates'],colors) if c])
        es=[e for e,c in full];ww=[c for e,c in full];deg=Counter(v for e in es for v in e)
        if max(deg.values())>3:excluded.append([list(colors),'degree']);continue
        sh=shape_table(es);pp=frame(es,ww,sh)
        if pp is None:excluded.append([list(colors),'preframe']);continue
        rr=rows(es,ww,pp,sh)
        sig=Counter((r['variables'][0],r['variables'][1],r['rhs']) for r in rr)
        if sig!=target:excluded.append([list(colors),'witness_count']);continue
        result=minimum_families(es,ww)
        assert result['minimum_support'] is not None
        choices.append({'passive_colors':list(colors),'edges':list(map(list,es)),'word':ww,'audit':result})
    # Preserve the complete core-support endpoint families too.
    hulls=[family(E,w,R,ss,ps,main['attainers']) for R in (H,T)]
    return {'verdict':'candidate_only','main':main,'new_phases':newph,'new_rows':rows(E,new,ps,ss),'new_colors_at_old_attainers':[decode(new,ps,a) for a in main['attainers']],'transfer':transfer,'absorbed_profiles':enlarged,'core_families':hulls,'passive_completions':choices,'rejected_passive_assignments':excluded}

if __name__=='__main__':
    raw=(ROOT/'opg37271-c29-input.json').read_bytes();result=calculate(json.loads(raw));result['input_sha256']=hashlib.sha256(raw).hexdigest()
    data=pack(result);assert len(data)<1048576
    (ROOT/'opg37271-c29-certificate.json').write_bytes(data)
    print(json.dumps({'verdict':'candidate_only','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'passive_completions':len(result['passive_completions']),'minimum_support':result['main']['minimum_support']}))
