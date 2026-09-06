"""Local candidate generator: exact tree checks, bounded edit search, 306-state DP.
Not a trusted verifier. Uses no repository scripts, credentials, or remote execution.
"""
from __future__ import annotations
import itertools as it
import base64, zlib, json, signal, resource, sys, time
from pathlib import Path
import numpy as np

def limits(seconds=40):
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall limit')))
    signal.alarm(seconds)
    resource.setrlimit(resource.RLIMIT_AS,(1536*1024**2,1536*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(40,41))

def c11():
    es=[['v','u',0],['u','x',1],['u','y',2],['x','a',3],['x','b',4],['y','c',5],['y','d',6]]
    for i,A,B,L,R in [('a',1,2,5,6),('b',1,3,5,6),('c',2,1,3,4),('d',2,5,3,4)]:
        es += [[i,'z'+i,A],['z'+i,'l'+i,L],['z'+i,'r'+i,R],[i,'w'+i,B]]
    es += [['wb','tb',2],['tb','sb',3],['wd','td',1],['td','sd',5]]
    return es

def topology(es):
    adj={}
    for e,(x,y,_) in enumerate(es):
        assert x!=y
        adj.setdefault(x,[]).append((y,e)); adj.setdefault(y,[]).append((x,e))
    assert len(es)==len(adj)-1 and all(len(v)<=3 for v in adj.values())
    seen=set(); todo=[next(iter(adj))]
    while todo:
        x=todo.pop()
        if x in seen: continue
        seen.add(x); todo.extend(y for y,e in adj[x] if y not in seen)
    assert len(seen)==len(adj)
    assert len({tuple(sorted((x,y))) for x,y,c in es})==len(es)
    return adj

def constraints(es):
    adj=topology(es)
    pairs=sorted({tuple(sorted((e,f))) for vs in adj.values() for (_,e),(_,f) in it.combinations(vs,2)})
    paths=set()
    def walk(x,visited,edges):
        if len(edges)==4:
            paths.add(min(tuple(edges),tuple(reversed(edges)))); return
        for y,e in adj[x]:
            if y not in visited: walk(y,visited|{y},edges+[e])
    for x in adj: walk(x,{x},[])
    return pairs,sorted(paths)

def conflict(cols, pairs, paths):
    for i,j in pairs:
        if cols[i] and cols[i]==cols[j]: return (i,j)
    for i,j,k,l in paths:
        if cols[i] and cols[j] and cols[i]==cols[k] and cols[j]==cols[l]: return (i,j,k,l)
    return None

def star(es):
    p,q=constraints(es)
    return conflict([c for x,y,c in es],p,q) is None

def edit_solutions(es,budget=2,stop_first=False):
    p,q=constraints(es); old=tuple(c for x,y,c in es)
    assert old[0]==0 and conflict(old,p,q) is None
    ans=set(); visited=set()
    def rec(t,mods):
        key=(t,tuple(sorted(mods.items())))
        if key in visited: return
        visited.add(key)
        col=list(old); col[0]=t
        for e,a in mods.items(): col[e]=a
        bad=conflict(col,p,q)
        if bad is None:
            ans.add(key)
            return
        if len(mods)==budget: return
        for e in sorted(set(bad)):
            if e==0 or e in mods: continue
            for a in range(1,7):
                if a!=old[e]: rec(t,{**mods,e:a})
            if stop_first and ans: return
    for t in range(1,7):
        rec(t,{})
        if stop_first and ans: break
    return sorted(ans),len(visited)

def matrix_solutions(es,ans):
    rows=[]
    for t,mods in ans:
        col=[c for _,_,c in es];col[0]=t
        for e,a in mods: col[e]=a
        rows.append(col)
    return np.array(rows,dtype=np.int16)

def batch_valid(a,p,q):
    valid=np.ones(a.shape[0],dtype=bool)
    for i,j in p: valid &= (a[:,i]==0)|(a[:,i]!=a[:,j])
    for i,j,k,l in q: valid &= (a[:,i]==0)|(a[:,j]==0)|(a[:,i]!=a[:,k])|(a[:,j]!=a[:,l])
    return valid

def attach_step(es,ans,max_length=3):
    # Every <=2 repair already changes two C11 edges. Added edges stay old.
    m=len(es); adj=topology(es); sol=matrix_solutions(es,ans)
    weights=np.array([100 if bool({e for e,a in mods} & {1,2}) else 1 for t,mods in ans])
    old=np.array([c for x,y,c in es],dtype=np.int16)
    best=None
    for size in range(1,max_length+1):
        for x in sorted(adj):
            if x=='v' or len(adj[x])>=3:continue
            extra=[]; prev=x
            for j in range(size):
                y=f'n{m+j}';extra.append([prev,y,1]);prev=y
            p,q=constraints(es+extra)
            p=[z for z in p if max(z)>=m];q=[z for z in q if max(z)>=m]
            for cs in it.product(range(1,7),repeat=size):
                if any(cs[j]==cs[j+1] for j in range(size-1)):continue
                arr=np.concatenate([old,np.array(cs,dtype=np.int16)])
                if conflict(arr,p,q) is not None:continue
                a=np.concatenate([sol,np.tile(cs,(len(ans),1))],axis=1)
                valid=batch_valid(a,p,q); kill=int((~valid).sum())
                if not kill:continue
                key=(int(weights[~valid].sum())/size,kill,-size)
                if best is None or key>best[0]:
                    chosen=[[z[0],z[1],c] for z,c in zip(extra,cs)]
                    best=(key,chosen,valid)
        # A short path with complete elimination is enough; otherwise compare sizes.
        if best is not None and best[0][1]==len(ans):break
    if best is None:return None
    return es+best[1],[x for x,v in zip(ans,best[2]) if v],best[1]

# Canonical 306 states: (stem color, six coordinates; stem coordinate=0).
def signatures():
    S=[]
    for a in range(1,7):
        others=[b for b in range(1,7) if b!=a]
        for j in range(3):
            for bs in it.combinations(others,j):
                for ds in it.product((2,3),repeat=j):
                    L=[1]*6;L[a-1]=0
                    for b,d in zip(bs,ds):L[b-1]=d
                    S.append((a,tuple(L)))
    assert len(S)==306
    return S

def transitions(S):
    index={s:i for i,s in enumerate(S)}
    T=[[],[],[]]
    for a in range(1,7):
        L=[1]*6;L[a-1]=0;T[0].append((index[a,tuple(L)],a,0,0))
        for i,(b,B) in enumerate(S):
            if b==a or B[a-1]>2:continue
            out=L.copy();out[b-1]=1+B[a-1]
            T[1].append((index[a,tuple(out)],a,i,0))
            for j,(c,C) in enumerate(S):
                if c in (a,b) or C[a-1]>2 or B[c-1]+C[b-1]>3:continue
                out2=out.copy();out2[c-1]=1+C[a-1]
                T[2].append((index[a,tuple(out2)],a,i,j))
    return [np.array(t,dtype=np.int32).T for t in T]

def dp(es,cap=4,cert=False):
    adj=topology(es); S=signatures();T=transitions(S)
    assert es[0]==['v','u',0] and len(adj['v'])==1
    records=[];table={};backs={}
    def visit(parent,x,e):
        ch=[(y,f) for y,f in adj[x] if y!=parent]
        for y,f in ch:visit(x,y,f)
        ar=len(ch);o,a,i,j=T[ar]
        cost=(a!=es[e][2]).astype(np.int16) if e!=0 else np.zeros(len(a),dtype=np.int16)
        if ar>=1:cost+=table[ch[0][1]][i]
        if ar==2:cost+=table[ch[1][1]][j]
        cost=np.minimum(cost,cap)
        d=np.full(306,cap,dtype=np.int16);np.minimum.at(d,o,cost)
        table[e]=d
        # Acyclic topology; exact min costs, not a proposed coloring alone.
        rec={'edge':e,'parent':parent,'vertex':x,'children':[f for y,f in ch],
             'costs':''.join(str(int(z)) for z in d)}
        records.append(rec)
        if cert:
            b={}
            for n,s in enumerate(o):
                if int(s) not in b and cost[n]==d[s] and d[s]<cap:
                    b[int(s)]=(int(a[n]),int(i[n]),int(j[n]))
            backs[e]=(ch,b)
    visit('v','u',0)
    optimum=int(table[0].min()); result={'cap':cap,'minimum':optimum,'states':306,'nodes':records}
    if cert and optimum<cap:
        coloring={}
        def unwind(e,s):
            ch,b=backs[e];a,i,j=b[s];coloring[e]=a
            if ch:unwind(ch[0][1],i)
            if len(ch)==2:unwind(ch[1][1],j)
        unwind(0,int(np.argmin(table[0])))
        result['coloring']=[coloring[e] for e in range(len(es))]
        result['changes']=[[e,es[e][2],coloring[e]] for e in range(1,len(es)) if es[e][2]!=coloring[e]]
        p,q=constraints(es);assert conflict(result['coloring'],p,q) is None
        assert len(result['changes'])==optimum
    return result

def dump(path,obj):
    text=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
    assert len(text.encode())<1_000_000
    Path(path).write_text(text)

if __name__=='__main__':
    limits(); mode=sys.argv[1]; start=time.monotonic()
    if mode=='baseline':
        es=c11(); ans,nodes=edit_solutions(es)
        r=dp(es,4,True)
        dump('baseline.json',{'edges':es,'solutions':ans,'search_nodes':nodes,'dp':r})
        print(json.dumps({'mode':mode,'vertices':len(es)+1,'solutions':len(ans),'search_nodes':nodes,'dp_min':r['minimum'],'seconds':time.monotonic()-start}))
    elif mode=='grow':
        src=json.loads(Path(sys.argv[2]).read_text()); es=src['edges'];ans=src['solutions']
        trace=src.get('attachment_trace',[])
        for step in range(1,21):
            if not ans:break
            z=attach_step(es,ans)
            if z is None:print('NO_IMPROVEMENT',len(ans));break
            es,ans,new=z;trace.append({'added':new,'remaining':len(ans)})
            dump('grown.json',{'edges':es,'solutions':ans,'attachment_trace':trace})
            print(json.dumps({'step':len(trace),'vertices':len(es)+1,'remaining':len(ans),'added':new}),flush=True)
    elif mode=='certify':
        src=json.loads(Path(sys.argv[2]).read_text());es=src['edges'];assert star(es)
        ans,n=edit_solutions(es,2)
        r=dp(es,4,True);dump('certificate.json',{'edges':es,'dp':r,'budget2_solutions':len(ans),'search_nodes':n})
        print(json.dumps({'vertices':len(es)+1,'budget2_solutions':len(ans),'dp_min':r['minimum'],'changes':r.get('changes'),'leaf_color':r.get('coloring',[None])[0],'search_nodes':n,'seconds':time.monotonic()-start}))

    elif mode=='prune':
        es=json.loads(Path(sys.argv[2]).read_text())['edges'];removed=[]
        while True:
            adj=topology(es);success=False
            for leaf in sorted(adj,reverse=True):
                if leaf=='v' or len(adj[leaf])!=1:continue
                _,e=adj[leaf][0]
                if e==0:continue
                sub=[z for f,z in enumerate(es) if f!=e]
                ans,n=edit_solutions(sub,2,True)
                if not ans:
                    removed.append(es[e]);es=sub;success=True;break
            if not success:break
        r=dp(es,4,True);dump('reduced.json',{'edges':es,'removed':removed,'dp':r})
        print(json.dumps({'mode':mode,'vertices':len(es)+1,'removed':len(removed),'minimum':r['minimum']}))
    elif mode=='pack':
        src=json.loads(Path(sys.argv[2]).read_text());es=src['edges'];r=dp(es,4,True)
        names=['v','u']
        for x,y,c in es:
            for z in (x,y):
                if z not in names:names.append(z)
        children=[None]*len(es)
        for rec in r['nodes']:children[rec['edge']]=rec['children']
        raw=bytes(int(x) for rec in r['nodes'] for x in rec['costs'])
        cert={'schema':'opg37271-reachable-tree-profile-v1','verdict':'candidate_only','vertices':names,
            'edges':[[names.index(x),names.index(y),c] for x,y,c in es],
            'postorder':[z['edge'] for z in r['nodes']],'children':children,'cap':4,
            'profiles_zlib_base64':base64.b64encode(zlib.compress(raw,9)).decode(),
            'extension':r['coloring']}
        dump('q2-certificate.json',cert)
        print(json.dumps({'mode':mode,'vertices':len(names),'minimum':r['minimum'],'cells':len(raw)}))
