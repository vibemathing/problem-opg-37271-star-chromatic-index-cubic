"""C29 literal replay. Imports no producer or earlier candidate implementation.
Graph walks and two-color components replace the producer's subset predicates.
"""
from pathlib import Path
from itertools import product, combinations
from collections import Counter
import hashlib,json,copy

ROOT=Path(__file__).resolve().parent

def canonical_json(v):return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()

class Graph:
    def __init__(self,edges):
        self.edges=[tuple(e) for e in edges];self.m=len(edges)
        assert all(a<b for a,b in self.edges) and len(set(self.edges))==self.m
        self.n=1+max(v for e in self.edges for v in e);self.adj=[[] for _ in range(self.n)]
        for k,(a,b) in enumerate(self.edges):self.adj[a].append((b,k));self.adj[b].append((a,k))
        assert all(len(x)<=3 for x in self.adj)
        found={}
        def visit(vs,es):
            if len(es)==4:
                if vs[-1]==vs[0]:
                    ring=vs[:-1];vv=min(tuple(z[k:]+z[:k]) for z in (ring,ring[::-1]) for k in range(4));kind='cycle'
                else:vv=min(tuple(vs),tuple(vs[::-1]));kind='path'
                found[kind,vv]={'kind':kind,'vertices':list(vv),'edges':sorted(es)};return
            for b,e in self.adj[vs[-1]]:
                if b not in vs or (len(es)==3 and b==vs[0]):visit(vs+[b],es+[e])
        for v in range(self.n):visit([v],[])
        self.shapes=[found[k] for k in sorted(found)]
    def proper(self,c):
        for inc in self.adj:
            cc=[c[e] for v,e in inc if c[e]]
            if len(cc)!=len(set(cc)):return False
        return True
    def partition(self,c):
        # Edge-connected U components, assembled without vertex-walk shape code.
        remaining={i for i,a in enumerate(c) if a==0};result=[]
        while remaining:
            component={min(remaining)};vertices=set(self.edges[min(remaining)])
            while True:
                more={e for e in remaining-component if set(self.edges[e])&vertices}
                if not more:break
                component|=more;vertices|={v for e in more for v in self.edges[e]}
            ds=Counter(v for e in component for v in self.edges[e])
            if max(ds.values())>2 or len(component)>3 or len(vertices)!=len(component)+1:return None
            ends=sorted(v for v,d in ds.items() if d==1);v=ends[0];order=[]
            while len(order)<len(component):
                nxt=[(b,e) for b,e in self.adj[v] if e in component and e not in order]
                if len(nxt)!=1:return None
                v,e=nxt[0];order.append(e)
            result.append(order);remaining-=component
        return result
    def D_star(self,c):
        if not self.proper(c):return False
        for a,b in combinations(range(1,5),2):
            left={i for i,k in enumerate(c) if k in (a,b)}
            while left:
                group={left.pop()};vs=set(self.edges[next(iter(group))]);todo=list(vs)
                while todo:
                    for v,e in self.adj[todo.pop()]:
                        if e in left:left.remove(e);group.add(e);todo.append(v)
                if len(group)>3:return False
        return True
    def frame(self,c):
        if len(c)!=self.m or any(a not in range(5) for a in c) or not self.D_star(c):return None
        return self.partition(c)
    def bad(self,c):
        assert self.proper(c)
        return [i for i,s in enumerate(self.shapes) if len({c[e] for e in s['edges']})==2]
    def full(self,c,paths,bits):
        ans=c.copy()
        for path,b in zip(paths,bits):
            for j,e in enumerate(path):ans[e]=5+(b^(j%2))
        return ans
    def all_phases(self,c,paths):
        return [{'bits':list(b),'cost':len(self.bad(self.full(c,paths,b))),'bad':self.bad(self.full(c,paths,b))} for b in product((0,1),repeat=len(paths))]
    def actual_rows(self,c,paths):
        loc={e:(i,j%2) for i,p in enumerate(paths) for j,e in enumerate(p)};index={e:i for i,e in enumerate(self.edges)};ans=[]
        for k,s in enumerate(self.shapes):
            vs=s['vertices'];pairs=list(zip(vs,vs[1:]))
            if s['kind']=='cycle':pairs.append((vs[-1],vs[0]))
            ee=[index[tuple(sorted(e))] for e in pairs];zz=[j for j,e in enumerate(ee) if c[e]==0]
            if zz not in ([0,2],[1,3]):continue
            dd=[e for e in ee if c[e]]
            if c[dd[0]]!=c[dd[1]]:continue
            (i,a),(j,b)=(loc[ee[z]] for z in zz)
            ans.append({'shape':k,'variables':sorted([i,j]),'rhs':1^a^b,'D_edges':sorted(dd)})
        return ans
    def is_connected_support(self,S):
        vertices={v for e in S for v in self.edges[e]};seen={min(vertices)}
        while True:
            more={v for e in S if set(self.edges[e])&seen for v in self.edges[e]}
            if more<=seen:break
            seen|=more
        return seen==vertices
    def literal_family(self,old,S,attainers):
        oldpaths=self.frame(old);outside=[p for p in oldpaths if not(set(p)&S)]
        assert all(not(set(p)&S) or set(p)<=S for p in oldpaths)
        indices=sorted(S);groups={}
        for boundary in product((0,1),repeat=len(outside)):
            full=old.copy()
            for p,b in zip(outside,boundary):
                for j,e in enumerate(p):full[e]=5+(b^(j%2))
            for e in S:full[e]=0
            def fill(j):
                if j==len(indices):
                    partial=[a if a<5 else 0 for a in full];paths=self.frame(partial)
                    if paths is None or any(set(p)&S and not set(p)<=S for p in paths):return
                    bits=[full[p[0]]-5 for p in paths]
                    assert self.full(partial,paths,bits)==full
                    bad=self.bad(full);key=tuple(partial)
                    group=groups.setdefault(key,{'word':partial,'paths':paths,'phase_map':{}})
                    bkey=tuple(bits);rec={'bits':bits,'cost':len(bad),'bad':bad}
                    assert bkey not in group['phase_map'];group['phase_map'][bkey]=rec;return
                e=indices[j];u,v=self.edges[e]
                used={full[f] for t in (u,v) for z,f in self.adj[t] if f!=e and full[f]}
                for color in range(1,7):
                    if color not in used:full[e]=color;fill(j+1)
                full[e]=0
            fill(0)
        ans=[]
        for key in sorted(groups):
            g=groups[key];records=[g['phase_map'][k] for k in sorted(g['phase_map'])];assert len(records)==2**len(g['paths'])
            amin=[]
            for a in attainers:
                oldfull=self.full(old,oldpaths,a);available=[]
                for r in records:
                    col=self.full(g['word'],g['paths'],r['bits'])
                    if all(col[e]==oldfull[e] for e in range(self.m) if e not in S):available.append(r['cost'])
                assert available;amin.append(min(available))
            ans.append({'word':g['word'],'paths':g['paths'],'phases':records,'anchored_minima':amin})
        return {'support':indices,'endpoints':ans}
    def audit_minimum(self,word,expected):
        assert self.shapes==expected['shapes'];paths=self.frame(word);assert paths==expected['paths']
        phases=self.all_phases(word,paths);assert phases==expected['old_phases'];mu=min(r['cost'] for r in phases)
        att=[r['bits'] for r in phases if r['cost']==mu];assert att==expected['attainers'];assert self.actual_rows(word,paths)==expected['rows']
        families=[];repairs=[];minimum=None
        for size in (1,2):
            for inds in combinations(range(self.m),size):
                S=set(inds)
                if any(set(p)&S and not set(p)<=S for p in paths) or not self.is_connected_support(S):continue
                fam=self.literal_family(word,S,att);families.append(fam)
                for k,e in enumerate(fam['endpoints']):
                    if all(c<mu for c in e['anchored_minima']):repairs.append({'support':list(inds),'endpoint':k,'word':e['word']})
            if repairs:minimum=size;break
        assert mu==expected['mu'] and minimum==expected['minimum_support']
        assert families==expected['families'] and repairs==expected['repairs']
        return sum(len(e['phases']) for f in families for e in f['endpoints'])

def run(inp,cert):
    graph=Graph(inp['edges']);old=inp['old'];new=inp['new'];assert cert['input_sha256']==hashlib.sha256((ROOT/'opg37271-c29-input.json').read_bytes()).hexdigest()
    phase_trials=graph.audit_minimum(old,cert['main']);paths=graph.frame(old)
    assert graph.frame(new)==paths;newph=graph.all_phases(new,paths);assert newph==cert['new_phases']
    assert graph.actual_rows(new,paths)==cert['new_rows']
    assert all(b['cost']<a['cost'] for a,b in zip(cert['main']['old_phases'],newph))
    S={graph.edges.index(tuple(e)) for e in inp['joint_support']};H={graph.edges.index(tuple(e)) for e in inp['core_hull']};T=H|S
    for support,expected in zip((H,T),cert['core_families']):
        got=graph.literal_family(old,support,cert['main']['attainers']);assert got==expected
        phase_trials+=sum(len(e['phases']) for e in got['endpoints'])
    terms=[]
    for r in cert['main']['old_phases']:
        full=graph.full(old,paths,r['bits']);other=graph.full(new,paths,r['bits']);a=graph.bad(full);b=graph.bad(other)
        h=[i for i in a if set(graph.shapes[i]['edges'])&T and not(set(graph.shapes[i]['edges'])&S)]
        assert h==[i for i in b if set(graph.shapes[i]['edges'])&T and not(set(graph.shapes[i]['edges'])&S)]
        sig=sum(bool(set(graph.shapes[i]['edges'])&S) for i in a);sn=sum(bool(set(graph.shapes[i]['edges'])&S) for i in b)
        terms.append({'bits':r['bits'],'old_sigma':sig,'new_sigma':sn,'h':len(h),'h_shapes':h,'g':sig-sn})
    profiles=[]
    for p,q in product((0,1),repeat=2):
        cells=[t for t in terms if t['bits'][1:]==[p,q]];base=min(t['old_sigma']+t['h'] for t in cells)
        for t in cells:t['r']=t['old_sigma']+t['h']-base;t['net']=t['g']-t['r']
        profiles.append({'boundary':[p,q],'old':base,'new':min(t['new_sigma']+t['h'] for t in cells),'gain':max(t['net'] for t in cells)})
    assert terms==cert['transfer'] and profiles==cert['absorbed_profiles']
    base=list(zip(map(tuple,inp['fixed_edges']),inp['fixed_colors']));passing=[];rejected=[]
    target=Counter({(a,b,s):n for a,b,s,n in inp['exact_row_counts']})
    for colors in product(range(5),repeat=3):
        ec=sorted(base+[(tuple(e),c) for e,c in zip(inp['passive_candidates'],colors) if c]);es=[e for e,c in ec];w=[c for e,c in ec]
        ds=Counter(v for e in es for v in e)
        if max(ds.values())>3:rejected.append([list(colors),'degree']);continue
        g=Graph(es);ps=g.frame(w)
        if ps is None:rejected.append([list(colors),'preframe']);continue
        rr=g.actual_rows(w,ps)
        if Counter((r['variables'][0],r['variables'][1],r['rhs']) for r in rr)!=target:rejected.append([list(colors),'witness_count']);continue
        passing.append((list(colors),es,w,g))
    assert rejected==cert['rejected_passive_assignments'];assert len(passing)==len(cert['passive_completions'])==6
    for (colors,es,w,g),expected in zip(passing,cert['passive_completions']):
        assert colors==expected['passive_colors'] and list(map(list,es))==expected['edges'] and w==expected['word']
        phase_trials+=g.audit_minimum(w,expected['audit'])
    # Completion controls leave the degree-one vertex9 genuinely available.
    controls=[]
    for extras in ([],[((9,10),0)],[((9,10),0),((10,11),0)],[((9,10),0),((10,11),0),((11,12),0)],[((9,10),1),((9,11),2)]):
        es=graph.edges+[e for e,c in extras];wo=old+[c for e,c in extras];wn=new+[c for e,c in extras];g=Graph(es);ps=g.frame(wo)
        assert ps is not None and g.frame(wn)==ps
        losses=[a['cost']-b['cost'] for a,b in zip(g.all_phases(wo,ps),g.all_phases(wn,ps))]
        assert min(losses)>=1;controls.append({'added_edges':list(map(list,[e for e,c in extras])),'colors':[c for e,c in extras],'phases':len(losses),'minimum_loss':min(losses)})
    # A third U edge at6 is allowed in the nine-vertex completion theorem.
    idx=graph.edges.index((6,9));wu=old.copy();nu=new.copy();wu[idx]=nu[idx]=0
    ups=graph.frame(wu);assert ups is not None and max(map(len,ups))==3
    assert min(a['cost']-b['cost'] for a,b in zip(graph.all_phases(wu,ups),graph.all_phases(nu,ups)))>=1
    relabel=[]
    for perm in __import__('itertools').permutations((1,2,3,4)):
        d={0:0,**{i+1:v for i,v in enumerate(perm)}};wo=[d[x] for x in old];wn=[d[x] for x in new]
        ps=graph.frame(wo);assert ps==paths and graph.frame(wn)==paths
        assert graph.all_phases(wo,ps)==cert['main']['old_phases'] and graph.all_phases(wn,ps)==newph;relabel.append(list(perm))
    tests=[]
    def check(name,condition):assert condition,name;tests.append({'test':name,'detected':True})
    check('retain_passive_color4_blocker',passing[0][3].audit_minimum(passing[0][2],cert['passive_completions'][0]['audit'])>0 and cert['passive_completions'][0]['audit']['minimum_support']==1)
    only02=old.copy();only02[1]=4
    check('old_single_02_recolor_creates_actual_D_path',graph.frame(only02) is None)
    only37=old.copy();only37[7]=4
    check('old_single_37_recolor_creates_actual_D_path',graph.frame(only37) is None)
    only08=old.copy();only08[2]=3;p08=graph.frame(only08)
    check('legal_intermediate_not_assumed_improving',p08 is not None and min(r['cost'] for r in graph.all_phases(only08,p08))==1)
    dup=False
    try:Graph(graph.edges+[graph.edges[0]])
    except AssertionError:dup=True
    check('duplicate_graph_edge',dup)
    deg=False
    try:Graph(graph.edges+[(0,10)])
    except AssertionError:deg=True
    check('unsaturated_completion_not_allowed_at_vertex0',deg)
    palette=old.copy();palette[1]=5
    check('cross_palette_partial_word',graph.frame(palette) is None)
    path4=Graph([(0,1),(1,2),(2,3),(3,4)])
    check('U_length_four',path4.frame([0,0,0,0]) is None)
    claw=Graph([(0,1),(0,2),(0,3)])
    check('U_degree_three',claw.frame([0,0,0]) is None)
    check('missing_middle_U_closure',any(set(p)&{0,5} and not set(p)<={0,5} for p in paths))
    check('missing_whole_outside_phase',len(cert['main']['old_phases'])==8 and len(cert['main']['attainers'])==2)
    check('deduplicate_parallel_witnesses',len(cert['main']['rows'])==7 and len(target)==4)
    selfrow=next(r for r in cert['main']['rows'] if r['variables']==[0,0]);sh=graph.shapes[selfrow['shape']]
    check('induced_only_loses_self_witness',sh['vertices']==[1,0,2,3,7] and (1,2) in graph.edges)
    check('delete_negative_self_row',selfrow['rhs']==1 and all(selfrow['shape'] in r['bad'] for r in cert['main']['old_phases']))
    check('non_simple_path_rejected',[1,0,2,0,8] not in [s['vertices'] for s in graph.shapes])
    c4=Graph([(0,1),(0,3),(1,2),(2,3)])
    check('omit_four_cycles',len(c4.bad([1,5,5,1]))==1 and c4.shapes[0]['kind']=='cycle')
    check('omit_nonzero_h',any(t['h'] for t in terms) and any(t['old_sigma']!=t['old_sigma']+t['h'] for t in terms))
    check('wrong_g_minus_r_sign',any(t['r']>0 and t['g']-t['r']!=t['g']+t['r'] for t in terms))
    check('cannot_replace_all_endpoints_with_one_failed_change',len(cert['main']['repairs'])==4)
    check('minimum_support_counts_closed_not_changed_only',cert['main']['minimum_support']==2 and len(cert['main']['families'])==20)
    return {'verdict':'candidate_only','best_verified_result':'none','passive_cases':len(passing),'minimum_connected_support':2,'literal_phase_records_compared':phase_trials,'hull_family_sizes':[len(f['endpoints']) for f in cert['core_families']],'mutations':tests,'A_relabelings':len(relabel),'completion_controls':controls,'third_U_edge_completion_checked':True,'root_closed':False,'trusted_execution':False}

if __name__=='__main__':
    inp=json.loads((ROOT/'opg37271-c29-input.json').read_bytes());raw=(ROOT/'opg37271-c29-certificate.json').read_bytes();cert=json.loads(raw)
    result=run(inp,cert);result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    data=canonical_json(result);(ROOT/'opg37271-c29-check-result.json').write_bytes(data)
    print(json.dumps({'verdict':'candidate_only','literal_phase_records':result['literal_phase_records_compared'],'mutation_count':len(result['mutations']),'result_sha256':hashlib.sha256(data).hexdigest()}))
