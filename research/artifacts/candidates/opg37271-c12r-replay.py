"""Stdlib replay of a reachable capped-profile tree certificate (candidate-only).
Recomputes every coordinate; never treats an arbitrary abstract vector as realizable.
"""
from __future__ import annotations
import base64, itertools, json, resource, signal, sys, time, zlib
from pathlib import Path

def require(test, message):
    if not test: raise ValueError(message)

def state_space():
    states=[]
    for a in range(1,7):
        for j in range(3):
            for chosen in itertools.combinations([b for b in range(1,7) if b!=a],j):
                for vals in itertools.product((2,3),repeat=j):
                    d=[1]*6;d[a-1]=0
                    for b,v in zip(chosen,vals):d[b-1]=v
                    states.append((a,tuple(d)))
    return states

def join(a,children):
    colors=[s[0] for s in children]
    if len(set([a]+colors))!=len(colors)+1:return None
    if any(s[1][a-1]>2 for s in children):return None
    if len(children)==2 and children[0][1][colors[1]-1]+children[1][1][colors[0]-1]>3:return None
    lengths=[1]*6;lengths[a-1]=0
    for b,d in children:lengths[b-1]=1+d[a-1]
    return a,tuple(lengths)

def check_star(edges,colors,omit_new=False):
    # Direct two-color component audit, with no use of DP or join().
    for a,b in itertools.combinations(range(1,7),2):
        adj={}
        for i,(x,y,c) in enumerate(edges):
            if omit_new and i==0:continue
            if colors[i] not in (a,b):continue
            adj.setdefault(x,[]).append((y,colors[i]));adj.setdefault(y,[]).append((x,colors[i]))
        require(all(len(v)<=2 and len({c for y,c in v})==len(v) for v in adj.values()),'improper coloring')
        seen=set()
        for x in adj:
            if x in seen:continue
            todo=[x];size=0
            while todo:
                y=todo.pop()
                if y in seen:continue
                seen.add(y);size+=len(adj[y]);todo.extend(z for z,c in adj[y] if z not in seen)
            require(size//2<=3,'long two-color component')

def replay(cert,cap=None):
    es=cert['edges']; names=cert['vertices'];n=len(names);m=len(es)
    require(n<=500 and m==n-1 and len(set(names))==n,'tree size or names')
    require(es[0]==[0,1,0],'new leaf convention')
    require(all(len(e)==3 and all(type(x) is int for x in e) for e in es),'edge format')
    require(all(0<=x<n and 0<=y<n and x!=y for x,y,c in es),'edge endpoints')
    require(all(1<=c<=6 for x,y,c in es[1:]),'palette')
    require(len({tuple(sorted(e[:2])) for e in es})==m,'parallel edge')
    adj={i:[] for i in range(n)}
    for e,(x,y,c) in enumerate(es):adj[x].append((y,e));adj[y].append((x,e))
    require(len(adj[0])==1 and all(1<=len(v)<=3 for v in adj.values()),'degree')
    order=[];children={};visited={0};endpoints={}
    def dfs(p,x,e):
        require(x not in visited,'cycle');visited.add(x);endpoints[e]=(p,x)
        ch=[(y,f) for y,f in adj[x] if y!=p]
        for y,f in ch:dfs(x,y,f)
        children[e]=[f for y,f in ch];order.append(e)
    dfs(0,1,0);require(len(visited)==n,'disconnected')
    require(cert['postorder']==order,'postorder/backpointer mismatch')
    require(cert['children']==[children[e] for e in range(m)],'child/backpointer mismatch')
    old=[e[2] for e in es];check_star(es,old,True)
    S=state_space();idx={s:i for i,s in enumerate(S)};require(len(S)==306,'state count')
    stored_cap=cert['cap'];require(stored_cap==4,'stored cap')
    k=stored_cap if cap is None else cap;require(k in (3,4),'replay cap')
    # Decompression bounded by the already bounded vertex/edge count.
    comp=base64.b64decode(cert['profiles_zlib_base64'],validate=True)
    decoder=zlib.decompressobj();raw=decoder.decompress(comp,m*306+1)
    require(len(raw)==m*306 and decoder.eof and not decoder.unused_data,'profile length or compression')
    require(all(0<=c<=stored_cap for c in raw),'cost range')
    D={};oldsig={}
    for row,e in enumerate(order):
        ch=children[e];out=[k]*306
        choices=[[(j,v) for j,v in enumerate(D[f]) if v<k] for f in ch]
        for tup in itertools.product(*choices):
            childstates=[S[j] for j,v in tup]; subtotal=sum(v for j,v in tup)
            if subtotal>=k:continue
            for a in range(1,7):
                value=subtotal+(0 if e==0 or a==old[e] else 1)
                if value>=k:continue
                s=join(a,childstates)
                if s is not None:
                    j=idx[s]
                    if value<out[j]:out[j]=value
        expect=[min(x,k) for x in raw[row*306:(row+1)*306]]
        require(out==expect,f'cost mismatch at edge {e}')
        D[e]=out
        if e!=0:
            s=join(old[e],[oldsig[f] for f in ch]);require(s is not None,'unrealizable old transition')
            oldsig[e]=s
            require(out[idx[s]]==0,'old signature lacks zero cost')
    minimum=min(D[0]);require(minimum==3,'unexpected optimum or root threshold')
    colors=cert['extension'];require(len(colors)==m and all(1<=a<=6 for a in colors),'extension format')
    check_star(es,colors)
    edits=[e for e in range(1,m) if colors[e]!=old[e]];require(len(edits)==3,'upper edit count')
    return {'vertices':n,'edges':m,'coordinates_recomputed':m*306,'cap':k,'root_value':minimum,
            'changed_edge_ids':edits,'leaf_color':colors[0],'old_star':True,'extension_star':True}

if __name__=='__main__':
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('wall limit')));signal.alarm(40)
    resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,768*1024**2))
    resource.setrlimit(resource.RLIMIT_CPU,(40,41))
    start=time.monotonic();cert=json.loads(Path(sys.argv[1]).read_text())
    reports=[replay(cert,k) for k in (3,4)]
    mutations=[]
    bad=json.loads(json.dumps(cert));data=bytearray(zlib.decompress(base64.b64decode(bad['profiles_zlib_base64'])))
    data[0]=(data[0]+1)%5;bad['profiles_zlib_base64']=base64.b64encode(zlib.compress(data)).decode()
    for label,obj in [('cost_coordinate',bad),('cyclic_child',{**cert,'children':[[0]]+cert['children'][1:]})]:
        try:replay(obj);raise AssertionError('mutation accepted')
        except ValueError as err:mutations.append({'mutation':label,'rejected':str(err)})
    print(json.dumps({'verdict':'candidate_only','reports':reports,'mutations':mutations,'seconds':time.monotonic()-start},sort_keys=True))
