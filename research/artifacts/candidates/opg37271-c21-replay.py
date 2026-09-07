"""Graph-definition replay. Imports no constructor, C19, or C20 module."""
from itertools import combinations,permutations,product
from copy import deepcopy
from pathlib import Path
import json,sys,hashlib,resource,signal

def need(ok,msg):
    if not ok:raise ValueError(msg)

def make(cycles,M):
    n=sum(map(len,cycles));E=[]
    need(sorted(v for C in cycles for v in C)==list(range(n)),'cycle coverage')
    for C in cycles:E += [tuple(sorted((C[i],C[(i+1)%len(C)]))) for i in range(len(C))]
    need(sorted(v for e in M for v in e)==list(range(n)),'matching coverage')
    E += [tuple(sorted(e)) for e in M]
    need(len(set(E))==len(E),'simple edges')
    return n,E

def shapes(n,E):
    need(type(n)is int and 0<=n<=16 and len(E)<=24,'finite graph cap')
    adj=[[] for _ in range(n)];seen=set()
    for i,pair in enumerate(E):
        need(len(pair)==2,'edge arity');a,b=pair
        need(type(a)is int and type(b)is int and 0<=a<n and 0<=b<n and a!=b,'endpoints')
        k=tuple(sorted(pair));need(k not in seen,'duplicate edge');seen.add(k)
        adj[a].append((b,i));adj[b].append((a,i))
    need(all(len(ns)<=3 for ns in adj),'degree')
    found=[]
    def visit(vs,es):
        if len(es)==4:
            if vs[0]<vs[-1]:found.append(('path',vs,es))
            return
        for w,e in adj[vs[-1]]:
            if w not in vs:visit(vs+[w],es+[e])
            elif len(es)==3 and w==vs[0] and vs[0]==min(vs) and vs[1]<vs[-1]:found.append(('cycle',vs,es+[e]))
    for s in range(n):visit([s],[])
    return adj,found

def star(adj,obs,c):
    need(all(type(v)is int and 1<=v<=6 for v in c),'palette')
    if any(len({c[e] for _,e in ns})!=len(ns) for ns in adj):return False
    return all(c[es[0]]!=c[es[2]] or c[es[1]]!=c[es[3]] for _,_,es in obs)

def all_pairings(left):
    # Enumerate all pairings, including forbidden edges; filter only at the end.
    if not left:yield ();return
    a=left[0]
    for j in range(1,len(left)):
        b=left[j]
        for tail in all_pairings(left[1:j]+left[j+1:]):yield ((a,b),)+tail

def check_group(group):
    cycles=group['cycles'];n=sum(map(len,cycles));F={tuple(sorted((C[i],C[(i+1)%len(C)]))) for C in cycles for i in range(len(C))}
    expected={M for M in all_pairings(tuple(range(n))) if not(set(M)&F)}
    got=[];paths=cyc=rows=0
    for r in group['rows']:
        M=tuple(map(tuple,r['matching']));got.append(M);N,E=make(cycles,M);adj,obs=shapes(N,E)
        c=r['colors'];need(len(c)==len(E) and star(adj,obs,c),'full star coloring')
        paths+=sum(kind=='path' for kind,_,_ in obs);cyc+=sum(kind=='cycle' for kind,_,_ in obs)
        U={i for i,col in enumerate(c) if col>=5}
        if group['kind']=='square':
            need(set(c)<=set((1,2,3,5,6)),'square five-color palette')
            need(sorted(v for i in U for v in E[i])==list(range(n)),'square U matching')
            bits={v:c[i]-5 for i in U for v in E[i]}
            need(all(bits[a]!=bits[b] for i,(a,b) in enumerate(E) if i not in U),'D crosses bit cut')
            need(all(bits[C[i]]!=bits[C[i+2]] for C in cycles for i in (0,1)),'opposite port parity')
        elif group['kind']=='odd35':
            lam={v:c[n+i] for i,e in enumerate(M) for v in e}
            need(all(c[n+i]<=4 for i in range(len(M))) and all(lam[a]!=lam[b] for a,b in E[:n]),'strong four matching')
            S={i for i in range(n) if c[i]<=4}
            need(len({v for i in S for v in E[i]})==2*len(S),'S matching')
            off=0
            for C in cycles:
                sel=[i for i in range(len(C)) if off+i in S]
                need(len(sel)==(1 if len(C)==3 else 2),'special count')
                need(len({c[off+i] for i in sel})==len(sel),'special colors distinct')
                for i in sel:need(c[off+i] not in {lam[C[j%len(C)]] for j in (i-1,i,i+1,i+2)},'four-vertex separation')
                off+=len(C)
        for kind,vs,es in obs:
            free=[j for j,e in enumerate(es) if e in U]
            if free in ([0,2],[1,3]):
                fixed=[j for j in range(4) if j not in free]
                if c[es[fixed[0]]]==c[es[fixed[1]]]:
                    rows+=1
                    need(group['kind']!='odd35','odd35 mixed row must not exist')
                    need(c[es[free[0]]]!=c[es[free[1]]],'actual mixed row satisfied')
    need(len(got)==len(set(got)) and set(got)==expected,'complete matching coverage')
    return {'kind':group['kind'],'cycle_lengths':list(map(len,cycles)),'graphs_with_matching':len(got),'four_edge_paths':paths,'four_cycles':cyc,'selected_mixed_witnesses':rows}

def check_exception_table(cert):
    listed={row['permutation_index']:row for row in cert['k5_exceptions']}
    need(len(listed)==len(cert['k5_exceptions']),'exception uniqueness');actual=[]
    cycles=[list(range(5)),list(range(5,10))];shapes_count=[0,0]
    for pi,p in enumerate(permutations(range(5))):
        M=[(i,5+p[i]) for i in range(5)];n,E=make(cycles,M)
        owner={v:i for i,e in enumerate(M) for v in e}
        pairs={tuple(sorted((owner[a],owner[b]))) for a,b in E[:n]}
        if pairs!=set(combinations(range(5),2)):continue
        actual.append(pi);need(pi in listed,'missing K5 exception')
        r=listed[pi];need(r['permutation']==list(p),'permutation identity');adj,obs=shapes(n,E)
        need(len(r['colors'])==15 and star(adj,obs,r['colors']),'K5 full coloring')
        for k in (0,1):shapes_count[k]+=sum(kind==('path' if k==0 else 'cycle') for kind,_,_ in obs)
    need(set(listed)==set(actual),'exact exception coverage')
    return {'indices':actual,'graphs':len(actual),'four_edge_paths':shapes_count[0],'four_cycles':shapes_count[1]}

def partial(n,E,c):
    adj,obs=shapes(n,E);need(len(c)==len(E) and all(type(a)is int and 0<=a<=4 for a in c),'disjoint palette')
    need(all(len([c[e] for _,e in ns if c[e]])==len({c[e] for _,e in ns if c[e]}) for ns in adj),'D proper')
    need(all(any(c[e]==0 for e in es) or c[es[0]]!=c[es[2]] or c[es[1]]!=c[es[3]] for _,_,es in obs),'D star')
    free={e for e,a in enumerate(c) if a==0};info={};ps=[]
    while free:
        first=min(free);todo=list(E[first]);V=set(todo);es=set()
        while todo:
            v=todo.pop()
            for w,e in adj[v]:
                if c[e]!=0:continue
                es.add(e)
                if w not in V:V.add(w);todo.append(w)
        need(len(es)<=3 and len(V)==len(es)+1,'U short path')
        ends=sorted(v for v in V if sum(e in es for _,e in adj[v])==1)
        need(len(ends)==2 and all(sum(e in es for _,e in adj[v])<=2 for v in V),'U path')
        seq=[];v=ends[0]
        while True:
            ns=[(w,e) for w,e in adj[v] if e in es and e not in seq]
            if not ns:break
            v,e=ns[0];info[e]=(len(ps),len(seq)%2);seq.append(e)
        ps.append(seq);free-=es
    rows=[]
    for kind,vs,es in obs:
        pos=[i for i,e in enumerate(es) if c[e]==0]
        if pos not in ([0,2],[1,3]):continue
        fx=[i for i in range(4) if i not in pos]
        if c[es[fx[0]]]!=c[es[fx[1]]]:continue
        i,p=info[es[pos[0]]];j,q=info[es[pos[1]]]
        rows.append({'i':i,'j':j,'b':1^p^q,'kind':kind,'vertices':vs,'edges':es})
    return ps,info,rows,adj,obs

def phase_compare(n,E,c,mutate=None):
    ps,info,rows,adj,obs=partial(n,E,c);used=deepcopy(rows)
    if mutate=='omit_c4':used=[r for r in used if r['kind']!='cycle']
    if mutate=='drop_self':used=[r for r in used if r['i']!=r['j']]
    if mutate=='collapse_sign':
        d={}
        for r in used:d.setdefault(tuple(sorted((r['i'],r['j']))),r)
        used=list(d.values())
    good=[];bad=[]
    for x in product((0,1),repeat=len(ps)):
        full=[a if a else 5+(x[info[e][0]]^info[e][1]) for e,a in enumerate(c)]
        direct=star(adj,obs,full);xor=all(x[r['i']]^x[r['j']]==r['b'] for r in used)
        if direct:good.append(list(x))
        if xor!=direct:bad.append({'phase':list(x),'colors':full,'rows_accept':xor,'direct_accept':direct})
    return {'rows':rows,'good':good,'mismatch':bad,'trials':2**len(ps)}

def tests(cert,old):
    out={};mut=[]
    for key in ('negative_six_cycle_frame','positive_k4_frame'):
        r=old[key];d=phase_compare(r['n'],r['edges'],r['partial_colors']);need(not d['mismatch'],'old frame equivalence');out[key]=d
    fixtures=[('omit_c4',4,[(0,1),(1,2),(2,3),(3,0)],[1,0,1,0]),('drop_self',5,[(0,1),(1,2),(2,3),(1,3),(2,4)],[0,0,0,1,1]),('collapse_sign',5,[(0,1),(1,2),(3,4),(0,3),(2,4)],[0,0,0,1,1])]
    for name,n,E,c in fixtures:
        x=phase_compare(n,E,c,name);need(x['mismatch'],'mutant not distinguished');mut.append({'name':name,'witness':x['mismatch'][0],'actual_rows':x['rows']})
    def rejected(name,fn):
        try:fn()
        except (ValueError,AssertionError,IndexError) as e:mut.append({'name':name,'error':str(e)});return
        raise ValueError('accepted invalid mutation '+name)
    rejected('palette_crossing',lambda:partial(2,[(0,1)],[5]))
    rejected('U_length_four',lambda:partial(5,[(0,1),(1,2),(2,3),(3,4)],[0,0,0,0]))
    rejected('U_cycle',lambda:partial(4,[(0,1),(1,2),(2,3),(3,0)],[0]*4))
    def witness(vs):need(len(vs)==5 and len(set(vs))==5,'simple witness vertices')
    rejected('non_simple_path',lambda:witness([0,1,2,1,4]))
    x=deepcopy(cert);x['k5_exceptions'].pop();rejected('missing_exception_row',lambda:check_exception_table(x))
    x=deepcopy(cert);x['k5_exceptions'][0]['colors'][0]=7;rejected('invalid_exception_color',lambda:check_exception_table(x))
    for key in ('empty_graph','empty_U'):
        d=phase_compare(0,[],[]) if key=='empty_graph' else phase_compare(4,[(0,1),(1,2),(2,3),(3,0)],[1,2,3,4]);need(d['good']==[[]],'empty case');out[key]=d
    r=cert['k33'];adj,obs=shapes(r['n'],r['edges']);need(star(adj,obs,r['colors']),'K33 root coloring')
    cuts=[]
    for bit in product((0,1),repeat=6):
        U=[e for e,(a,b) in enumerate(r['edges']) if bit[a]==bit[b]]
        if len({v for e in U for v in r['edges'][e]})==2*len(U):cuts.append({'bits':list(bit),'U':U})
    need(len(cuts)==2 and all(not r['U'] for r in cuts),'K33 complete cut space')
    out['k33_cut_assignments']=cuts;out['mutations']=mut
    counts={}
    for palette in (4,5):
        word=[0]*9;count=0;accept=0
        def assign(e):
            nonlocal count,accept
            if e==9:
                count+=1;accept+=int(star(adj,obs,word));return
            a,b=r['edges'][e]
            forbidden={word[f] for v in (a,b) for _,f in adj[v] if f<e}
            for col in range(1,palette+1):
                if col not in forbidden:word[e]=col;assign(e+1)
            word[e]=0
        assign(0);need(accept==0,'K33 unexpectedly star five')
        counts[str(palette)]={'proper_colorings':count,'star_colorings':accept}
    out['k33_complete_small_palette_counts']=counts
    # All cyclic four-windows in the two block types; a window touches at most two blocks.
    for a,b in product(([1,2,3],[1,2,1,3]),repeat=2):
        w=a+b
        need(all(w[i]!=w[i+1] for i in range(len(w)-1)),'block proper')
        need(all(w[i]!=w[i+2] or w[i+1]!=w[i+3] for i in range(len(w)-3)),'block star')
    return out


def check_domain(data,spec):
    want=[('square',tuple([4]*k)) for k in spec['square_cycle_counts']]+[('odd35',tuple(x)) for x in spec['odd_factor_lengths']]+[('odd35_full',(5,5))]
    need([(g['kind'],tuple(map(len,g['cycles']))) for g in data['groups']]==want,'complete factor-domain coverage')
    need([(r['n'],r['edges']) for r in data['general_preframes']]==[(r['n'],r['edges']) for r in spec['general_cubic_inputs']],'complete general-input coverage')


def main():
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,768*1024**2))
    raw=sys.stdin.buffer.read(1048577);need(len(raw)<=1048576,'stress stream cap');data=json.loads(raw)
    here=Path(__file__).parent;cert_raw=(here/'opg37271-c21-certificate.json').read_bytes();cert=json.loads(cert_raw)
    old_raw=(here/'opg37271-c19-phase-certificate.json').read_bytes()
    need(hashlib.sha256(old_raw).hexdigest()=='9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3','old input identity')
    spec=json.loads((here/'opg37271-c21-input.json').read_text());check_domain(data,spec)
    summary=[check_group(g) for g in data['groups']];exc=check_exception_table(cert);detail=tests(cert,json.loads(old_raw))
    damaged=dict(data);damaged['groups']=data['groups'][:-1]
    try:check_domain(damaged,spec)
    except ValueError as e:detail['mutations'].append({'name':'missing_factor_group','error':str(e)})
    else:raise ValueError('missing group accepted')
    expected_words={w for m in (3,5) for w in product(range(1,5),repeat=m) if all(w[i]!=w[(i+1)%m] for i in range(m))}
    actual_words=[]
    for record in data['local_words']:
        w=record['word'];m=len(w);S=record['specials'];actual_words.append(tuple(w))
        need(len(S)==(1 if m==3 else 2),'word special count')
        need(len({v for i,c in S for v in (i,(i+1)%m)})==2*len(S),'word matching')
        need(len({c for i,c in S})==len(S),'word distinct S colors')
        for i,c in S:need(c in range(1,5) and c not in {w[j%m] for j in (i-1,i,i+1,i+2)},'word safe window')
    need(len(actual_words)==len(set(actual_words)) and set(actual_words)==expected_words,'all proper local words')
    detail['local_words_checked']={str(m):sum(len(w)==m for w in actual_words) for m in (3,5)}
    detail['general_preframes']=[]
    for r in data['general_preframes']:
        n,E,c=r['n'],r['edges'],r['partial_colors'];adj,obs=shapes(n,E)
        need(all(len(ns)==3 for ns in adj),'general cubic')
        need(sorted(r['successor'])==list(range(n)) and all(tuple(sorted((v,w))) in set(map(tuple,map(sorted,E))) for v,w in enumerate(r['successor'])),'double cover matching')
        ps,info,rows,_,_=partial(n,E,c)
        need(all(len(P)<=2 for P in ps),'general U two edge limit')
        need(sorted({v for P in ps for i in P for v in E[i]})==list(range(n)),'U spans vertices')
        need(all(sum(c[i]!=0 for _,i in ns)<=2 for ns in adj),'D degree two')
        need(all(row['i']!=row['j'] for row in rows),'no self row')
        tested=phase_compare(n,E,c);need(not tested['mismatch'],'general phase equivalence')
        core=None
        for size in range(1,len(rows)+1):
            if tested['good']:break
            for ids in combinations(range(len(rows)),size):
                mask=rhs=0
                for i in ids:
                    row=rows[i];mask^=(1<<row['i'])^(1<<row['j']);rhs^=row['b']
                if mask==0 and rhs==1:core=[rows[i] for i in ids];break
            if core is not None:break
        need(bool(tested['good'])==(core is None),'finite core alternative')
        detail['general_preframes'].append({'minimum_core':core,'n':n,'edges':E,'successor':r['successor'],'U_paths':ps,'partial_colors':c,'rows':rows,'phase_trials':tested['trials'],'good_phases':tested['good']})
    report={'verdict':'candidate_only','groups':summary,'k5_exceptions':exc,'tests':detail,'stream_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),'limitations':'Finite generator-domain replay, no trusted receipt; universal claims rely on the separate proofs, Brooks dependency and finite exceptional coverage argument.'}
    text=json.dumps(report,sort_keys=True,separators=(',',':'))+'\n';need(len(text.encode())<=65536,'result cap');print(text,end='')
if __name__=='__main__':main()
