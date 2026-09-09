"""C30 separate literal replay. No producer/earlier-candidate imports.
Four-edge subsets and literal six-color assignments implement different entry points.
The evidence ceiling remains candidate_only, not a trusted verifier invocation.
"""
from pathlib import Path
from itertools import combinations, product, permutations
from collections import defaultdict, Counter
import json, hashlib, copy
P=Path(__file__).resolve().parent

def dump(o):return (json.dumps(o,sort_keys=True,separators=(',',':'))+'\n').encode()

class Audit:
    def __init__(self,n,E):
        self.n=n;self.E=[tuple(e) for e in E];self.m=len(E)
        assert len(set(self.E))==self.m and all(0<=a<b<n for a,b in self.E)
        self.inc=[[i for i,e in enumerate(self.E) if v in e] for v in range(n)]
        assert max(map(len,self.inc),default=0)<=3
        self.sh=[]
        for ids in combinations(range(self.m),4):
            a=defaultdict(list)
            for e in ids:
                u,v=self.E[e];a[u].append((v,e));a[v].append((u,e))
            ds=sorted(map(len,a.values()))
            if ds not in ([1,1,2,2,2],[2,2,2,2]):continue
            seen={min(a)};todo=list(seen)
            while todo:
                for v,_ in a[todo.pop()]:
                    if v not in seen:seen.add(v);todo.append(v)
            if seen!=set(a):continue
            cyclic=ds==[2,2,2,2];start=min(a) if cyclic else min(v for v in a if len(a[v])==1)
            seq=[start];ee=[]
            for _ in range(4):
                v,e=min((v,e) for v,e in a[seq[-1]] if e not in ee);seq.append(v);ee.append(e)
            if cyclic:seq.pop()
            self.sh.append(['cycle' if cyclic else 'path',seq,ee])

    def proper(self,c):
        return all(len([c[e] for e in ii if c[e]])==len({c[e] for e in ii if c[e]}) for ii in self.inc)

    def twocolor_cost(self,c):
        total=0
        for aa,bb in combinations(range(1,7),2):
            left={i for i,a in enumerate(c) if a in (aa,bb)}
            while left:
                i=left.pop();part={i};stack=[i]
                while stack:
                    j=stack.pop()
                    for v in self.E[j]:
                        for k in self.inc[v]:
                            if k in left:left.remove(k);part.add(k);stack.append(k)
                degrees=Counter(v for e in part for v in self.E[e]);L=len(part)
                cyclic=all(d==2 for d in degrees.values())
                total+=(1 if L==4 else L) if cyclic and L>=4 else max(0,L-3)
        return total

    def paths(self,w):
        parent=list(range(self.n))
        def root(v):
            while v!=parent[v]:v=parent[v]
            return v
        selected=[i for i,a in enumerate(w) if a==0]
        for i in selected:
            u,v=self.E[i];parent[root(v)]=root(u)
        groups=defaultdict(list)
        for i in selected:groups[root(self.E[i][0])].append(i)
        result=[]
        for es in sorted(groups.values(),key=min):
            deg=Counter(v for e in es for v in self.E[e])
            if len(es)>3 or max(deg.values())>2 or len(deg)!=len(es)+1:return None
            v=min(v for v,d in deg.items() if d==1);seq=[]
            for _ in es:
                j=next(i for i in es if i not in seq and v in self.E[i]);seq.append(j)
                v=next(u for u in self.E[j] if u!=v)
            result.append(seq)
        return result

    def valid(self,w):
        if len(w)!=self.m or any(type(c)!=int or not 0<=c<=4 for c in w) or not self.proper(w):return None
        if self.twocolor_cost(w):return None
        return self.paths(w)

    @staticmethod
    def closure(paths,S):return all(not (set(q)&S) or not(set(q)-S) for q in paths)

    def connected(self,S):
        vertices=set();first=next(iter(S));vertices.update(self.E[first]);edges=set(S)-{first}
        for _ in S:
            take={i for i in edges if any(v in vertices for v in self.E[i])}
            edges-=take
            for e in take:vertices.update(self.E[e])
        return not edges

    def score(self,c):
        assert self.proper(c) and all(1<=a<=6 for a in c)
        bad=[i for i,(_,_,es) in enumerate(self.sh) if len(set(c[e] for e in es))==2]
        assert len(bad)==self.twocolor_cost(c)
        return bad

    def phase_records(self,w):
        pp=self.valid(w);assert pp is not None
        # All literal B-edge assignments; reject nonalternation by full properness.
        ids=[e for e,a in enumerate(w) if a==0];rr=[]
        for vals in product((5,6),repeat=len(ids)):
            c=w.copy()
            for e,a in zip(ids,vals):c[e]=a
            if self.proper(c):rr.append([''.join(map(str,c)),self.score(c)])
        return sorted(rr)

    def literal_family(self,w,S):
        pp=self.valid(w);assert pp is not None and self.closure(pp,S)
        outside=[q for q in pp if not set(q)&S];groups=defaultdict(dict);ids=sorted(S)
        for bits in product((5,6),repeat=len(outside)):
            c=w.copy()
            for path,b in zip(outside,bits):
                for k,e in enumerate(path):c[e]=b if k%2==0 else 11-b
            for e in ids:c[e]=0
            def rec(k):
                if k==len(ids):
                    v=[a if a<5 else 0 for a in c];qs=self.valid(v)
                    if qs is None or not self.closure(qs,S):return
                    word=''.join(map(str,v));full=''.join(map(str,c));groups[word][full]=self.score(c)
                    return
                e=ids[k];u,v=self.E[e]
                forbidden={c[j] for j in self.inc[u]+self.inc[v] if j!=e and c[j]}
                for a in range(1,7):
                    if a not in forbidden:c[e]=a;rec(k+1)
                c[e]=0
            rec(0)
        return [[w,[[c,b] for c,b in sorted(rr.items())]] for w,rr in sorted(groups.items())]

    def supports(self,w,k):
        qs=self.valid(w);assert qs is not None
        return [set(S) for S in combinations(range(self.m),k) if self.closure(qs,set(S)) and self.connected(set(S))]

    def rows(self,w):
        qs=self.valid(w);assert qs is not None
        pos={e:(i,j&1) for i,q in enumerate(qs) for j,e in enumerate(q)};ans=[]
        for j,s in enumerate(self.sh):
            a=[w[e] for e in s[2]]
            z=[k for k in range(4) if a[k]==0]
            if z not in ([0,2],[1,3]):continue
            rest=[a[k] for k in range(4) if k not in z]
            if rest[0]!=rest[1]:continue
            p,i=pos[s[2][z[0]]];q,k=pos[s[2][z[1]]]
            ans.append([j,min(p,q),max(p,q),1^i^k])
        return ans

def improves(tab,S,old):
    best=min(map(lambda r:len(r[1]),old));att=[c for c,b in old if len(b)==best]
    off=[i for i in range(len(att[0])) if i not in S]
    return [w for w,rr in tab if all(any(len(b)<best and all(c[i]==a[i] for i in off) for c,b in rr) for a in att)]

def check_family_table(g,w,doc):
    rr=g.phase_records(w);allS=[]
    for k in (1,2,3):allS +=[sorted(S) for S in g.supports(w,k)]
    allS+=[s for s,_ in doc['families'] if len(s)>3]
    assert len({tuple(s) for s in allS})==len(allS)
    assert allS==[s for s,_ in doc['families']]
    for S,tab in doc['families']:
        assert g.literal_family(w,set(S))==tab
    return rr

def validate():
    inpraw=(P/'opg37271-c30-input.json').read_bytes();d=json.loads(inpraw)
    cert_raw=(P/'opg37271-c30-certificate.json').read_bytes();c=json.loads(cert_raw)
    summary=json.loads((P/'opg37271-c30-summary.json').read_bytes());w=d['old'];new=d['joint_new']
    g=Audit(d['n'],d['edges']);pp=g.valid(w);assert pp is not None
    assert hashlib.sha256(inpraw).hexdigest()==c['input_sha256']
    assert g.sh==c['shapes'] and pp==c['old_paths'] and g.rows(w)==c['old_rows']
    old=check_family_table(g,w,c);assert old==c['old_phases']
    assert g.phase_records(new)==c['new_phases'] and g.rows(new)==c['new_rows']
    counts=[]
    for k in (1,2,3):
        fs=[(S,tab) for S,tab in c['families'] if len(S)==k]
        counts.append((len(fs),sum(len(tab) for S,tab in fs),sum(len(improves(tab,set(S),old)) for S,tab in fs)))
    assert counts==[(9,20,0),(11,59,0),(17,187,4)]
    # Pointwise graph-color map: all old B phases, not just minimizers.
    loss=[]
    for color,bad in old:
        a=list(map(int,color))
        for e in d['joint_support']:a[e]=new[e]
        assert [x if x<=4 else 0 for x in a]==new
        loss.append(len(bad)-len(g.score(a)))
    assert min(loss)>=1
    # Compute old/new profiles by directly fixing surviving exterior colors.
    S=set(d['joint_support']);A=set(d['expanded_support'])
    outpaths=[q for q in pp if not set(q)&S];allnew=g.phase_records(new);terms=[]
    for bits in product(range(2),repeat=len(outpaths)):
        def rows_at(rr):return [(list(map(int,a)),bs) for a,bs in rr if all(int(a[q[0]])==5+b for q,b in zip(outpaths,bits))]
        ro=rows_at(old);rn=rows_at(allnew);assert ro and rn
        so=min(sum(bool(S&set(g.sh[i][2])) for i in bs) for _,bs in ro)
        sn=min(sum(bool(S&set(g.sh[i][2])) for i in bs) for _,bs in rn)
        hh=[[i for i in bs if A&set(g.sh[i][2]) and not S&set(g.sh[i][2])] for _,bs in ro+rn]
        assert all(v==hh[0] for v in hh)
        terms.append({'bits':list(bits),'remaining':[b for q,b in zip(outpaths,bits) if not set(q)&A],
                      'old':so,'new':sn,'h':len(hh[0]),'h_shapes':hh[0]})
    for z in terms:
        minimum=min(a['old']+a['h'] for a in terms if a['remaining']==z['remaining'])
        z.update(r=z['old']+z['h']-minimum,g=z['old']-z['new']);z['gain_term']=z['g']-z['r']
    assert terms==c['transfer']
    # All passive choices are inputs to full-graph checking, not edge deletions during a repair.
    base=[(tuple(e),a) for e,a in zip(g.E,w) if tuple(e)!=(4,8)]
    desired=sorted(r[1:] for r in g.rows(w));passive=[];choices=[]
    for vals in product(range(5),repeat=3):
        pairs=sorted(base+[(e,a) for e,a in zip([(4,8),(4,9),(8,9)],vals) if a]);ee=[e for e,a in pairs];v=[a for e,a in pairs]
        ok=False
        if max(sum(vtx in e for e in ee) for vtx in range(d['n']))<=3:
            gg=Audit(d['n'],ee);qs=gg.valid(v)
            ok=qs is not None and sorted(r[1:] for r in gg.rows(v))==desired
        choices.append([list(vals),ok])
        if not ok:continue
        original=gg.phase_records(v);sol=None
        for k in (1,2,3):
            for SS in gg.supports(v,k):
                tab=gg.literal_family(v,SS);good=improves(tab,SS,original)
                if good:sol=[k,sorted(SS),good[0]];break
            if sol:break
        passive.append({'added':[[list(e),a] for e,a in zip([(4,8),(4,9),(8,9)],vals) if a],
                        'edges':[list(e) for e in ee],'old':v,'repair':sol})
    assert choices==c['passive_choices'] and passive==c['passive_completions'] and len(passive)==6
    # Diagnostics are named by the actual erroneous predicate or input exercised.
    tests=[]
    def test(name,predicate):assert predicate;tests.append(name)
    def invalid_edges(ee):
        try:Audit(d['n'],ee)
        except AssertionError:return True
        return False
    test('duplicate_edge',invalid_edges(d['edges']+[d['edges'][0]]))
    test('degree_four',invalid_edges(d['edges']+[[0,9]]))
    vv=w.copy();vv[1]=5;test('A_palette_crossing',g.valid(vv) is None)
    vv=w.copy();vv[6]=0;test('U_degree_three',g.valid(vv) is None)
    gg=Audit(5,[(0,1),(1,2),(2,3),(3,4)]);test('U_length_four',gg.valid([0]*4) is None)
    gg=Audit(4,[(0,1),(1,2),(2,3),(0,3)]);test('U_cycle',gg.valid([0]*4) is None)
    test('missing_C4',len(gg.score([1,2,1,2]))==1)
    seq=[2,3,0,1,7];loop_id=next(i for i,s in enumerate(g.sh) if s[1]==seq or s[1]==seq[::-1])
    test('induced_only_loses_self',set((1,2))<=set(seq) and loop_id in old[0][1])
    test('nonsimple_path',[2,3,0,1,2] not in [s[1] for s in g.sh])
    test('drop_self_row',sum(r[1]==r[2] for r in c['old_rows'])==1)
    test('deduplicate_parallel_rows',len(set(tuple(r[1:]) for r in c['old_rows']))<len(c['old_rows']))
    test('incomplete_old_U_closure',not g.closure(pp,{0}))
    vv=w.copy();vv[1]=4;test('delete_passive_edge_false_repair',g.valid(vv) is None)
    vv=w.copy();vv[1]=4;vv[7]=1;rr=g.phase_records(vv)
    test('two_A_recolorings_leave_conflict',min(len(b) for _,b in rr)==1)
    for name,mask in [('missing_endpoint',0),('missing_phase',1),('wrong_bad_shape',2)]:
        src=c['families'][-1][1];alter=copy.deepcopy(src)
        if mask==0:alter.pop()
        elif mask==1:alter[0][1].pop()
        else:alter[0][1][0][1]=[-1]
        test(name,alter!=g.literal_family(w,set(c['families'][-1][0])))
    test('omit_nonzero_h',any(t['h'] for t in terms))
    test('phase_min_is_not_frame_min',min(len(b) for _,b in old)==1 and min(len(b) for _,b in allnew)==0)
    test('old_new_U_dimensions_differ',len(pp)==3 and len(g.valid(new))==2)
    # Every A permutation preserves the complete finite shape predicates and pointwise improvement.
    for perm in permutations(range(1,5)):
        for color,bad in old:
            a=[perm[int(x)-1] if int(x)<5 else int(x) for x in color]
            v=a.copy()
            for e in d['joint_support']:v[e]=perm[new[e]-1]
            assert len(g.score(v))<len(g.score(a))
    test('A_relabeling24',True)
    # Saturated motif allows a third U edge at6; explicitly check both phases of the extended path.
    ee=[e for e in g.E if e!=(6,9)]+[(6,9)]
    pairs=sorted((e,(0 if e==(6,9) else w[g.E.index(e)])) for e in ee)
    ge=Audit(10,[e for e,_ in pairs]);ve=[a for _,a in pairs];re=ve.copy()
    for edge,col in [((0,3),4),((3,8),1),((7,8),2)]:re[ge.E.index(edge)]=col
    for color,bad in ge.phase_records(ve):
        cc=list(map(int,color))
        for edge,col in [((0,3),4),((3,8),1),((7,8),2)]:cc[ge.E.index(edge)]=col
        assert len(ge.score(cc))<len(bad)
    test('third_U_edge_at6',True)
    # Parse the committed readable minimum tables and check EVERY listed phase witness.
    text=(P/'opg37271-c30-minimum-tables.txt').read_text().splitlines()
    seen_shapes={};seen_tables=defaultdict(dict);current=None
    for line in text:
        if line.startswith('#') or not line:continue
        if line.startswith('H '):
            _,sid,kind,vs,es=line.split();seen_shapes[int(sid)]=[kind,list(map(int,vs.split(','))),list(map(int,es.split(',')))]
        elif line.startswith('S '):current=tuple(map(int,line[2:].split(',')))
        else:
            assert current is not None
            entries,bads=line.split(' : ');v=w.copy()
            for e,a in zip(current,map(int,entries)):v[e]=a
            assert len(entries)==len(current)
            qs=g.valid(v);assert qs is not None
            raw=[([] if x=='-' else list(map(int,x.split(',')))) for x in bads.split(';')]
            assert len(raw)==1<<len(qs)
            for mask,bb in enumerate(raw):
                cc=v.copy()
                for i,q in enumerate(qs):
                    for j,e in enumerate(q):cc[e]=5+((mask>>i&1)^(j&1))
                assert g.score(cc)==bb
            seen_tables[current][entries]=raw
    assert [seen_shapes[i] for i in range(len(g.sh))]==g.sh
    for SS,tab in c['families']:
        if len(SS)>3:continue
        expect={''.join(word[e] for e in SS) for word,rr in tab}
        assert set(seen_tables[tuple(SS)])==expect
    assert len(seen_tables)==37
    result={'verdict':'candidate_only','best_verified_result':'none','input_sha256':hashlib.sha256(inpraw).hexdigest(),
            'certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),'family_count':len(c['families']),
            'full_phase_records':sum(len(rr) for _,tab in c['families'] for _,rr in tab),
            'support_counts':counts,'minimum_pointwise_loss':min(loss),'passive_completions':len(passive),
            'mutation_checks':tests,'A_relabelings':24,'global_exchange':'open_for_other_embeddings','trusted_execution':False}
    (P/'opg37271-c30-check-result.json').write_bytes(dump(result));print(json.dumps(result,sort_keys=True))

if __name__=='__main__':validate()
