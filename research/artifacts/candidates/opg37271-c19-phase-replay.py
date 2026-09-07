"""Solver-free C19 certificate audit: real paths, phase witnesses, XOR refutation."""
from copy import deepcopy
import hashlib
import itertools as it
import json
from pathlib import Path
import platform
import resource
import signal


def require(ok,msg):
    if not ok: raise ValueError(msg)


def graph(n,edges):
    require(type(n) is int and n>=1,'order')
    adj=[[] for _ in range(n)]; unique=set()
    for e,(u,v) in enumerate(edges):
        require(type(u) is int and type(v) is int and 0<=u<n and 0<=v<n and u!=v,'endpoints')
        key=frozenset((u,v)); require(key not in unique,'duplicate edge'); unique.add(key)
        adj[u].append((v,e));adj[v].append((u,e))
    require(all(len(ns)<=3 for ns in adj),'degree')
    return adj


def star(adj,c,partial=False):
    require(all(type(a) is int and int(not partial)<=a<=6 for a in c),'color range')
    require(all(len([c[e] for _,e in ns if c[e]])==len({c[e] for _,e in ns if c[e]}) for ns in adj),'properness')
    counts=[0,0]
    def walk(vs,es):
        if len(es)==4:
            counts[0]+=1
            require(not all(c[e] for e in es) or c[es[0]]!=c[es[2]] or c[es[1]]!=c[es[3]],'bad path')
            return
        for v,e in adj[vs[-1]]:
            if v not in vs:walk(vs+[v],es+[e])
            elif len(es)==3 and v==vs[0]:
                counts[1]+=1; z=es+[e]
                require(not all(c[x] for x in z) or c[z[0]]!=c[z[2]] or c[z[1]]!=c[z[3]],'bad cycle')
    for v in range(len(adj)):walk([v],[])
    return counts


def frame(obj):
    n=obj['n'];E=obj['edges'];c=obj['partial_colors'];adj=graph(n,E)
    require(len(c)==len(E) and all(type(a) is int and 0<=a<=4 for a in c),'partial colors')
    star(adj,c,True); info={}; vertices=set()
    for i,seq in enumerate(obj['uncolored_paths']):
        require(1<=len(seq)<=3 and len(set(seq))==len(seq),'short path')
        require(all(type(e) is int and 0<=e<len(E) and c[e]==0 and e not in info for e in seq),'free edge list')
        if len(seq)==1:vs=list(E[seq[0]])
        else:
            common=set(E[seq[0]])&set(E[seq[1]])
            require(len(common)==1,'path ordering');mid=next(iter(common))
            vs=[next(v for v in E[seq[0]] if v!=mid),mid]
            for e in seq[1:]:
                require(vs[-1] in E[e],'path adjacency')
                vs.append(next(v for v in E[e] if v!=vs[-1]))
        require(len(set(vs))==len(vs) and not vertices&set(vs),'disjoint simple paths')
        vertices|=set(vs)
        for p,e in enumerate(seq):info[e]=(i,p%2)
    require(set(info)=={e for e,a in enumerate(c) if not a},'uncolored coverage')
    for q in obj['equations']:
        es=q['edges'];vs=q['vertices'];kind=q['kind']
        require(kind in ('path','cycle') and len(es)==4 and len(set(es))==4,'obstruction type')
        require(len(vs)==(5 if kind=='path' else 4) and len(set(vs))==len(vs),'simple vertices')
        for t,e in enumerate(es):
            require(type(e) is int and 0<=e<len(E),'witness edge')
            require(set(E[e])=={vs[t],vs[t+1] if kind=='path' else vs[(t+1)%4]},'edge incidence')
        free=[t for t,e in enumerate(es) if not c[e]]
        require(free in ([0,2],[1,3]),'alternating fixed/free')
        fixed=[t for t in range(4) if t not in free]
        require(c[es[fixed[0]]]==c[es[fixed[1]]] and c[es[fixed[0]]]>0,'fixed equality')
        e,f=[es[t] for t in free];i,p=info[e];j,r=info[f]
        require(q['free_edges']==[e,f] and q['i']==i and q['j']==j and q['rhs']==1^p^r,'equation fidelity')
    if obj['phase'] is None:
        ids=obj['contradiction_rows'];require(ids and len(set(ids))==len(ids),'contradiction rows')
        variables=set();rhs=0
        for row in ids:
            require(type(row) is int and 0<=row<len(obj['equations']),'row index')
            q=obj['equations'][row]
            for v in (q['i'],q['j']):variables.symmetric_difference_update({v})
            rhs^=q['rhs']
        require(not variables and rhs==1,'XOR contradiction')
        return 'negative'
    phase=obj['phase'];require(len(phase)==len(obj['uncolored_paths']) and set(phase)<=set((0,1)),'phase dimensions')
    full=[a if a else 5+(phase[info[e][0]]^info[e][1]) for e,a in enumerate(c)]
    require(full==obj['full_colors'],'full color reconstruction')
    require(all(phase[q['i']]^phase[q['j']]==q['rhs'] for q in obj['equations']),'phase equation')
    star(adj,full)
    return 'positive'


def main():
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(35,36));resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    p=Path(__file__).with_name('opg37271-c19-phase-certificate.json');raw=p.read_bytes();require(len(raw)<262144,'input size');d=json.loads(raw)
    require(frame(d['positive_k4_frame'])=='positive','positive')
    require(frame(d['negative_six_cycle_frame'])=='negative','negative')
    neg=d['negative_six_cycle_frame'];star(graph(6,neg['edges']),d['six_cycle_wider_palette'])
    rows=d['permutation_rows'];require(len(rows)==24 and [r[0] for r in rows]==list(range(24)),'permutation coverage')
    count=[0,0]
    for row,perm in zip(rows,it.permutations(range(4))):
        E=[(i,4+perm[i]) for i in range(4)]+[(i,(i+1)%4) for i in range(4)]+[(4+i,4+(i+1)%4) for i in range(4)]
        require(row[4][:4]==[1,2,3,4] and len(row[4])==12,'matching retention')
        a,b=star(graph(8,E),row[4]);count[0]+=a;count[1]+=b
    mutations=[]
    for name in ('repeated_vertex','wrong_rhs','incomplete_contradiction','outside_palette'):
        x=deepcopy(neg if name!='outside_palette' else d['positive_k4_frame'])
        if name=='repeated_vertex':x['equations'][0]['vertices'][1]=x['equations'][0]['vertices'][0]
        elif name=='wrong_rhs':x['equations'][0]['rhs']^=1
        elif name=='incomplete_contradiction':x['contradiction_rows']=x['contradiction_rows'][:-1]
        else:x['full_colors'][0]=7
        try:frame(x)
        except ValueError as exc:mutations.append([name,str(exc)])
        else:raise ValueError('accepted mutation')
    out={'verdict':'candidate_only','scope':'solver-free generator-domain certificate replay, not trusted verification',
         'input_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'runtime':platform.python_version(),'frame_witnesses':2,'positive_graph_colorings':24,
         'oriented_four_edge_paths_in_24_colorings':count[0],'oriented_four_cycles_in_24_colorings':count[1],
         'mutation_rejections':mutations,'not_replayed':'The full 6144-frame exhaustive tally requires the separate bounded check program.',
         'budgets':{'wall_seconds':35,'cpu_seconds':35,'memory_mib':512,'threads':1}}
    text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n'
    Path(__file__).with_name('opg37271-c19-phase-replay-result.json').write_text(text)
    print(text,end='')
if __name__=='__main__':main()
