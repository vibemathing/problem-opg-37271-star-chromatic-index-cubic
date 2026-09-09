"""C30 finite producer. Standalone; no prior candidate modules are imported.
Definitions: simple graphs, ordinary four-edge paths/C4, and jointly U-closed supports.
All results remain candidate_only. Invoke with the bounded companion runner.
"""
from pathlib import Path
from itertools import combinations, product
from collections import defaultdict
import json, hashlib

ROOT = Path(__file__).resolve().parent

def encoded(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':'))+'\n').encode()

def graph_shapes(n, edges):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        adj[u].append((v,i)); adj[v].append((u,i))
    found={}
    def walk(vs, es):
        if len(es)==4:
            key=tuple(sorted(es))
            if vs[-1]==vs[0]:
                cyc=vs[:-1]
                vv=min(tuple(q[k:]+q[:k]) for q in [cyc,cyc[::-1]] for k in range(4))
                kind='cycle'
            else:
                vv=min(tuple(vs),tuple(vs[::-1])); kind='path'
            lookup={tuple(sorted(e)):i for i,e in enumerate(edges)}
            pairs=list(zip(vv,vv[1:]))+([(vv[-1],vv[0])] if kind=='cycle' else [])
            found[key]=[kind,list(vv),[lookup[tuple(sorted(e))] for e in pairs]]
            return
        for u,e in adj[vs[-1]]:
            if u not in vs or (len(es)==3 and u==vs[0]):
                walk(vs+[u],es+[e])
    for v in range(n):walk([v],[])
    return [found[k] for k in sorted(found)]

def components(n,edges,w):
    adj=[[] for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        if w[i]==0:adj[u].append((v,i));adj[v].append((u,i))
    if any(len(a)>2 for a in adj):return None
    todo={i for i,c in enumerate(w) if not c}; parts=[]
    while todo:
        first=min(todo); seen=set(edges[first]); pending=list(seen); es=set()
        while pending:
            for u,e in adj[pending.pop()]:
                es.add(e)
                if u not in seen:seen.add(u);pending.append(u)
        if not 1<=len(es)<=3 or len(es)+1!=len(seen):return None
        v=min(v for v in seen if len(adj[v])==1); ordered=[]
        while len(ordered)<len(es):
            u,e=next((u,e) for u,e in adj[v] if e not in ordered)
            ordered.append(e);v=u
        parts.append(ordered);todo-=es
    return parts

def proper(edges,w):
    used=defaultdict(set)
    for (u,v),c in zip(edges,w):
        if c:
            if c in used[u] or c in used[v]:return False
            used[u].add(c);used[v].add(c)
    return True

def preframe(n,edges,w,sh):
    if not all(isinstance(c,int) and 0<=c<=4 for c in w) or not proper(edges,w):return None
    pp=components(n,edges,w)
    if pp is None:return None
    if any(all(w[e] for e in s[2]) and len({w[e] for e in s[2]})==2 for s in sh):return None
    return pp

def closed(pp,S):
    return all(not(set(p)&S) or set(p)<=S for p in pp)

def connected(edges,S):
    if not S:return False
    left=set(S);stack=[left.pop()]
    while stack:
        e=stack.pop(); nxt={f for f in left if set(edges[e])&set(edges[f])}
        left-=nxt;stack.extend(nxt)
    return not left

def decode(w,pp,x):
    c=w.copy()
    for p,b in zip(pp,x):
        for k,e in enumerate(p):c[e]=5+(b^(k%2))
    return c

def bad_ids(c,sh):
    return [i for i,s in enumerate(sh) if len({c[e] for e in s[2]})==2]

def records(w,pp,sh):
    return sorted([''.join(map(str,c)),bad_ids(c,sh)] for c in
                  (decode(w,pp,x) for x in product(range(2),repeat=len(pp))))

def family(n,E,w,sh,S):
    ids=sorted(S); table=[]
    for vals in product(range(5),repeat=len(ids)):
        v=w.copy()
        for e,c in zip(ids,vals):v[e]=c
        pp=preframe(n,E,v,sh)
        if pp is not None and closed(pp,S):
            table.append([''.join(map(str,v)),records(v,pp,sh)])
    return sorted(table)

def good_at_old_attainers(table,S,old_records):
    mu=min(len(r[1]) for r in old_records)
    olds=[r[0] for r in old_records if len(r[1])==mu]
    m=len(olds[0]); outside=[i for i in range(m) if i not in S]
    return [w for w,rr in table if all(any(len(bad)<mu and all(c[i]==old[i] for i in outside)
                                         for c,bad in rr) for old in olds)]

def signature(n,E,w,sh):
    pp=preframe(n,E,w,sh)
    if pp is None:return None
    pos={e:(i,k%2) for i,p in enumerate(pp) for k,e in enumerate(p)};rows=[]
    for sid,s in enumerate(sh):
        ids=s[2];zero=[k for k,e in enumerate(ids) if w[e]==0]
        if zero not in ([0,2],[1,3]):continue
        ds=[ids[k] for k in range(4) if k not in zero]
        if w[ds[0]]!=w[ds[1]]:continue
        a,pa=pos[ids[zero[0]]];b,pb=pos[ids[zero[1]]]
        rows.append([sid,min(a,b),max(a,b),1^pa^pb])
    return rows

def all_supports(E,pp,k):
    return [set(s) for s in combinations(range(len(E)),k) if closed(pp,set(s)) and connected(E,set(s))]

def profile(n,E,w,sh,S,outpaths):
    pp=preframe(n,E,w,sh); assert pp is not None and closed(pp,S)
    out=[]
    for bits in product(range(2),repeat=len(outpaths)):
        vals=[]
        for c,bad in records(w,pp,sh):
            if all(int(c[p[0]])==5+b for p,b in zip(outpaths,bits)):
                vals.append(sum(bool(set(sh[i][2])&S) for i in bad))
        assert vals
        out.append(min(vals))
    return out

def transfer(n,E,w,new,sh,S,A):
    pp=preframe(n,E,w,sh); npp=preframe(n,E,new,sh)
    assert pp is not None and npp is not None
    assert closed(pp,S) and closed(npp,S) and closed(pp,A) and closed(npp,A)
    outside=[p for p in pp if not set(p)&S]
    so=profile(n,E,w,sh,S,outside);sn=profile(n,E,new,sh,S,outside)
    terms=[]
    for key,bits in enumerate(product(range(2),repeat=len(outside))):
        vals=[]
        for c,bad in records(w,pp,sh):
            if all(int(c[p[0]])==5+b for p,b in zip(outside,bits)):
                vals.append([i for i in bad if set(sh[i][2])&A and not set(sh[i][2])&S])
        assert vals and all(v==vals[0] for v in vals)
        remain=tuple(b for p,b in zip(outside,bits) if not set(p)&A)
        terms.append({'bits':list(bits),'remaining':list(remain),'old':so[key],'new':sn[key],
                      'h':len(vals[0]),'h_shapes':vals[0]})
    for t in terms:
        mm=min(z['old']+z['h'] for z in terms if z['remaining']==t['remaining'])
        t['r']=t['old']+t['h']-mm;t['g']=t['old']-t['new'];t['gain_term']=t['g']-t['r']
    return terms

def minimum_text(n,E,doc):
    lines=['# C30 complete size<=3 support tables; zero-based edge/shape IDs.',
           '# S: support. Each following line: entries : bad IDs by phase 0..2^k-1.',
           '# Phase bit i belongs to U path i, paths ordered by least edge ID,',
           '# each path starts at its least endpoint. Phase bit is color(first)-5.',
           '# Entries replace the input old word on sorted support IDs. -=no bad shape.']
    for i,(kind,vs,es) in enumerate(doc['shapes']):
        lines.append('H '+str(i)+' '+kind+' '+','.join(map(str,vs))+' '+','.join(map(str,es)))
    for S,tab in doc['families']:
        if len(S)>3:continue
        lines.append('S '+','.join(map(str,S)))
        for word,rr in tab:
            ps=components(n,E,list(map(int,word)))
            byindex={sum((int(col[q[0]])-5)<<i for i,q in enumerate(ps)):bad for col,bad in rr}
            assert len(byindex)==1<<len(ps)
            entries=''.join(word[e] for e in S)
            lines.append(entries+' : '+';'.join(','.join(map(str,byindex[i])) or '-' for i in range(1<<len(ps))))
    return ('\n'.join(lines)+'\n').encode()

def calculate():
    raw=(ROOT/'opg37271-c30-input.json').read_bytes();inp=json.loads(raw)
    E=list(map(tuple,inp['edges']));w=inp['old'];new=inp['joint_new'];n=inp['n']
    assert len(set(E))==len(E) and all(0<=a<b<n for a,b in E)
    assert max(sum(v in e for e in E) for v in range(n))<=3
    sh=graph_shapes(n,E);pp=preframe(n,E,w,sh);assert pp is not None
    oldrec=records(w,pp,sh);families=[]
    for k in [1,2,3]:
        for S in all_supports(E,pp,k):families.append([sorted(S),family(n,E,w,sh,S)])
    for key in ['core_support','expanded_support']:
        S=set(inp[key]);assert closed(pp,S) and connected(E,S)
        if not any(row[0]==sorted(S) for row in families):families.append([sorted(S),family(n,E,w,sh,S)])
    sig=signature(n,E,w,sh)
    passive=[];choices=[]
    base=[(e,c) for e,c in zip(E,w) if e!=(4,8)]
    desired=sorted(r[1:] for r in sig)
    for vals in product(range(5),repeat=3):
        pairs=base+[(e,c) for e,c in zip([(4,8),(4,9),(8,9)],vals) if c]
        pairs.sort();ee=[p[0] for p in pairs];v=[p[1] for p in pairs]
        accepted=False
        if max(sum(a in e for e in ee) for a in range(n))<=3:
            ss=graph_shapes(n,ee);rs=signature(n,ee,v,ss)
            accepted=rs is not None and sorted(r[1:] for r in rs)==desired
        choices.append([list(vals),accepted])
        if not accepted:continue
        ps=preframe(n,ee,v,ss);oldrr=records(v,ps,ss);answer=None
        for k in [1,2,3]:
            for S in all_supports(ee,ps,k):
                tab=family(n,ee,v,ss,S); good=good_at_old_attainers(tab,S,oldrr)
                if good:answer=[k,sorted(S),good[0]];break
            if answer:break
        assert answer is not None
        passive.append({'added':[[list(e),c] for e,c in zip([(4,8),(4,9),(8,9)],vals) if c],
                        'edges':ee,'old':v,'repair':answer})
    result={'verdict':'candidate_only','input_sha256':hashlib.sha256(raw).hexdigest(),
            'shapes':sh,'old_paths':pp,'old_rows':sig,'old_phases':oldrec,
            'new_paths':preframe(n,E,new,sh),'new_rows':signature(n,E,new,sh),
            'new_phases':records(new,preframe(n,E,new,sh),sh),'families':families,
            'transfer':transfer(n,E,w,new,sh,set(inp['joint_support']),set(inp['expanded_support'])),
            'passive_choices':choices,'passive_completions':passive}
    summary={'verdict':'candidate_only','best_verified_result':'none','by_size':[],
             'passive_completions':passive,'transfer':result['transfer']}
    for k in [1,2,3]:
        fs=[r for r in families if len(r[0])==k]
        summary['by_size'].append({'size':k,'supports':len(fs),'endpoints':sum(len(t) for _,t in fs),
                                  'improving':[[S,good_at_old_attainers(t,set(S),oldrec)] for S,t in fs if good_at_old_attainers(t,set(S),oldrec)]})
    summary['full_phase_records']=sum(len(rr) for _,tab in families for _,rr in tab)
    summary['extra_families']=[[S,len(tab),len(good_at_old_attainers(tab,set(S),oldrec))] for S,tab in families if len(S)>3]
    rraw=encoded(result);assert len(rraw)<1048576
    table=minimum_text(n,E,result)
    (ROOT/'opg37271-c30-minimum-tables.txt').write_bytes(table)
    summary['minimum_tables_sha256']=hashlib.sha256(table).hexdigest()
    (ROOT/'opg37271-c30-certificate.json').write_bytes(rraw)
    summary['certificate_sha256']=hashlib.sha256(rraw).hexdigest();summary['certificate_bytes']=len(rraw)
    (ROOT/'opg37271-c30-summary.json').write_bytes(encoded(summary))
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':calculate()
