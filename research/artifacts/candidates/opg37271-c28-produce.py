"""C28 producer: four-edge subsets, partial endpoints, productive matching classes.
All claims remain candidate_only. No previous candidate code is imported.
The companion checker does not import this file. Use the bounded runner.
"""
from pathlib import Path
import hashlib
import json
from itertools import combinations, product
from collections import Counter

def shapes(E):
 out=[]
 for inds in combinations(range(len(E)),4):
  adj={}
  for i in inds:
   a,b=E[i];adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
  deg=sorted(map(len,adj.values()))
  if deg not in ([1,1,2,2,2],[2,2,2,2]):continue
  cyc=len(adj)==4
  start=min(adj) if cyc else min(v for v in adj if len(adj[v])==1)
  seq=[start];es=[];v=start;prev=None
  for k in range(4):
   opts=[(u,i) for u,i in adj[v] if i not in es]
   if not opts:break
   u,i=min(opts);es.append(i);seq.append(u);prev,v=v,u
  if len(es)!=4:continue
  if cyc:
   if seq[-1]!=start or len(set(seq[:-1]))!=4:continue
   seq=seq[:-1]
  elif len(set(seq))!=5:continue
  out.append(dict(vertices=seq,edges=es,kind='cycle' if cyc else 'path'))
 return out

def u_paths(E,w):
 adj={}
 for i,e in enumerate(E):
  if not w[i]:
   for a,b in (e,e[::-1]):adj.setdefault(a,[]).append((b,i))
 if any(len(v)>2 for v in adj.values()):return None
 unused={i for i,c in enumerate(w) if not c};res=[]
 while unused:
  i=min(unused);todo=list(E[i]);seen=set(todo);inds=set()
  while todo:
   a=todo.pop()
   for b,j in adj[a]:
    inds.add(j)
    if b not in seen:seen.add(b);todo.append(b)
  if len(inds)>3 or len(seen)!=len(inds)+1:return None
  a=min(v for v in seen if len(adj[v])==1);seq=[]
  while len(seq)<len(inds):
   b,j=next((b,j) for b,j in adj[a] if j not in seq);seq.append(j);a=b
  res.append(seq);unused-=inds
 return res

def proper(E,w):
 seen={}
 for (a,b),c in zip(E,w):
  if c:
   if c in seen.get(a,()) or c in seen.get(b,()):return False
   seen.setdefault(a,set()).add(c);seen.setdefault(b,set()).add(c)
 return True

def rows(E,w,ss=None):
 if ss is None:ss=shapes(E)
 if not proper(E,w):return None
 pp=u_paths(E,w)
 if pp is None:return None
 pos={e:(i,j%2) for i,P in enumerate(pp) for j,e in enumerate(P)}
 rs=[]
 for shape in ss:
  es=shape['edges'];c=[w[e] for e in es]
  if all(c) and len(set(c))==2:return None
  zz=[i for i,a in enumerate(c) if not a]
  if zz not in ([0,2],[1,3]):continue
  dd=[i for i in range(4) if i not in zz]
  if c[dd[0]]!=c[dd[1]]:continue
  i,p=pos[es[zz[0]]];j,q=pos[es[zz[1]]]
  rs.append(dict(**shape,i=i,j=j,rhs=1^p^q,alpha=c[dd[0]]))
 return pp,rs

def signature(E,w):
 obj=rows(E,w)
 if obj is None:return None
 pp,rs=obj
 return pp,Counter((min(r['i'],r['j']),max(r['i'],r['j']),r['rhs']) for r in rs)


from itertools import combinations, product
from collections import Counter
import json, time
TARGET=(1,2,3,1)

def raw_shapes(ee):
 adj={}
 for i,(a,b) in enumerate(ee):
  adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
 dd=sorted(map(len,adj.values()))
 if dd not in ([1,1,2,2,2],[2,2,2,2]):return False
 seen={next(iter(adj))};todo=list(seen)
 while todo:
  for u,_ in adj[todo.pop()]:
   if u not in seen:seen.add(u);todo.append(u)
 return len(seen)==len(adj)

def model(n,L,gauge,stop=True):
 U=[];info=[];start=0
 for comp,l in enumerate(L):
  for j in range(l):U.append((start+j,start+j+1));info.append((comp,j%2))
  start+=l+1
 assert start<=n
 D=[e for e in combinations(range(n),2) if e not in U]; idx={e:i for i,e in enumerate(D)}
 udeg=[sum(v in e for e in U) for v in range(n)]
 C={};bad=set()
 for i,j in combinations(range(len(D)),2):
  if set(D[i])&set(D[j]):continue
  counts=[0]*4;wrong=False
  for a,b in combinations(range(len(U)),2):
   if set(U[a])&set(U[b]):continue
   if not raw_shapes([D[i],D[j],U[a],U[b]]):continue
   ca,pa=info[a];cb,pb=info[b];rhs=1^pa^pb
   if ca>cb:ca,cb=cb,ca
   if ca==cb:
    if ca!=0 or rhs!=1:wrong=True;break
    t=0
   else:
    if rhs!=(gauge[ca]^gauge[cb]):wrong=True;break
    t={(0,1):1,(0,2):2,(1,2):3}[(ca,cb)]
   counts[t]+=1
  if wrong:bad.add((i,j))
  elif any(counts):C[i,j]=tuple(counts)
 # Generate every matching by smallest remaining vertex, either unmatched or paired.
 classes=[];matching_count=0
 def mats(rem,ee):
  nonlocal matching_count
  if not rem:
   matching_count+=1
   if len(ee)<2:return
   total=[0]*4;used=set()
   for i,j in combinations(sorted(ee),2):
    if (i,j) in bad:return
    c=C.get((i,j))
    if c:
     used|={i,j};total=[a+b for a,b in zip(total,c)]
   if len(used)!=len(ee) or any(x>y for x,y in zip(total,TARGET)):return
   mask=sum(1<<i for i in ee);deg=[sum(v in D[e] for e in ee) for v in range(n)]
   classes.append((tuple(ee),tuple(total),mask,tuple(deg)));return
  v=rem[0];rest=rem[1:];mats(rest,ee)
  for u in rest:
   e=tuple(sorted((u,v)))
   if e in idx:mats([a for a in rest if a!=u],ee+[idx[e]])
 mats(list(range(n)),[])
 classes.sort()
 compatibility={}
 def compat(i,j):
  a,b=classes[i],classes[j]
  if a[2]&b[2]:return False
  # Components of union of two matching colors contain <=3 edges exactly when star.
  ee=[D[e] for e in a[0]+b[0]];adj={}
  for z,(u,v) in enumerate(ee):adj.setdefault(u,[]).append(z);adj.setdefault(v,[]).append(z)
  todo=set(range(len(ee)))
  while todo:
   e=todo.pop();part={e};stack=[e]
   while stack:
    f=stack.pop()
    for v in ee[f]:
     for g in adj[v]:
      if g in todo:todo.remove(g);part.add(g);stack.append(g)
   if len(part)>3:return False
  return True
 compatsets=[set() for _ in classes]
 for i,j in combinations(range(len(classes)),2):
  if compat(i,j):compatsets[i].add(j);compatsets[j].add(i)
 visits=0;solutions=[]
 def back(chosen,allowed,tot,deg):
  nonlocal visits
  visits+=1
  if tuple(tot)==TARGET:
   if all(udeg[v]+deg[v]>0 for v in range(n)):
    solutions.append(chosen)
   return
  if len(chosen)==4:return
  for k in allowed:
   c=classes[k];tt=[a+b for a,b in zip(tot,c[1])]
   if any(a>b for a,b in zip(tt,TARGET)):continue
   dd=[a+b for a,b in zip(deg,c[3])]
   if any(a+b>3 for a,b in zip(dd,udeg)):continue
   back(chosen+[k],[j for j in allowed if j>k and j in compatsets[k]],tt,dd)
   if stop and solutions:return
 back([],list(range(len(classes))),[0]*4,[0]*n)
 class_lines=json.dumps([(a,b) for a,b,_,_ in classes],separators=(',',':')).encode();res={'class_sha256':hashlib.sha256(class_lines).hexdigest(),'n':n,'lengths':L,'gauge':gauge,'all_matchings':matching_count,'productive_classes':len(classes),'class_search_nodes':visits,'solutions_found':len(solutions)}
 if solutions:
  ee=U.copy();cc=[0]*len(U)
  for color,k in enumerate(solutions[0],1):
   for e in classes[k][0]:ee.append(D[e]);cc.append(color)
  res['example']={'edges':ee,'word':cc}
 return res


def encode(v):
    return (json.dumps(v,sort_keys=True,separators=(',',':'))+'\n').encode()

def calculate():
    root=Path(__file__).resolve().parent
    raw=(root/'opg37271-c28-input.json').read_bytes();inp=json.loads(raw)
    E=list(map(tuple,inp['edges']));w=inp['old'];ss=shapes(E);m=len(E)
    oldps,oldrs=rows(E,w,ss)
    def phased(v,S):
        ob=rows(E,v,ss)
        if ob is None:return None
        ps,rr=ob
        if any(set(P)&S and set(P)-S for P in ps):return None
        ins=[i for i,P in enumerate(ps) if set(P)&S]
        out=[i for i,P in enumerate(ps) if not set(P)&S]
        rec=[];sigma=[]
        for b in range(1<<len(out)):
            costs=[];touch=[];fulls=[];badsets=[]
            for a in range(1<<len(ins)):
                bits={i:b>>j&1 for j,i in enumerate(out)}
                bits.update({i:a>>j&1 for j,i in enumerate(ins)})
                full=v.copy()
                for i,P in enumerate(ps):
                    for j,e in enumerate(P):full[e]=5+(bits[i]^(j%2))
                bad=[j for j,z in enumerate(ss) if len({full[e] for e in z['edges']})==2]
                costs.append(len(bad));touch.append(sum(bool(set(ss[j]['edges'])&S) for j in bad))
                fulls.append(full);badsets.append(bad)
            sigma.append(min(touch))
            rec.append({'boundary':b,'total_costs':costs,'touch_costs':touch,'colors':fulls,'bad_shapes':badsets})
        return {'word':v,'paths':ps,'outside_paths':[ps[i] for i in out],'inside_paths':[ps[i] for i in ins],'sigma':sigma,'phases':rec}
    def endpoint_family(S):
        es=sorted(S);res=[]
        for entries in product(range(5),repeat=len(es)):
            v=w.copy()
            for e,c in zip(es,entries):v[e]=c
            z=phased(v,S)
            if z is not None:res.append(z)
        return res
    families={}
    for key in ['core_support','model_support','alternate_model_support']:
        S=set(inp[key]);fam=endpoint_family(S)
        families[key]={'support':sorted(S),'endpoints':fam,'envelope':[min(v['sigma'][b] for v in fam) for b in range(4)]}
    single=[]
    for e in range(m):
        S={e}
        if any(set(P)&S and set(P)-S for P in oldps):continue
        fam=endpoint_family(S)
        for z in fam:
            b=sum(inp['old_attainer'][oldps.index(P)]<<j for j,P in enumerate(z['outside_paths']))
            z['anchored_minimum']=min(z['phases'][b]['total_costs'])
        single.append({'support':[e],'endpoints':fam})
    old=phased(w,set(inp['model_support']));new=phased(inp['specified_new'],set(inp['model_support']))
    S=set(inp['model_support']);T=set(inp['absorbed_support']);terms=[]
    for b in range(4):
        # Full old phase with internal t=0 suffices for h, which is disjoint from S.
        colors=old['phases'][b]['colors'][0]
        hs=[j for j,z in enumerate(ss) if set(z['edges'])&T and not set(z['edges'])&S and len({colors[e] for e in z['edges']})==2]
        terms.append({'boundary':b,'old':old['sigma'][b],'new':new['sigma'][b],'h':len(hs),'h_shapes':hs})
    mm=min(z['old']+z['h'] for z in terms)
    for z in terms:z.update(r=z['old']+z['h']-mm,g=z['old']-z['new'])
    oldfull=phased(w,set(range(m)))
    repair=phased(inp['improving_new'],set(range(m)))
    margins=[];x=inp['old_attainer']
    for mask in range(8):
        delta=0
        for r in oldrs:
            if ((mask>>r['i'])^(mask>>r['j']))&1:
                delta+=1 if (x[r['i']]^x[r['j']])==r['rhs'] else -1
        margins.append(delta)
    dist={14:0};todo=[14]
    while todo:
        e=todo.pop(0)
        if dist[e]==2:continue
        for f in range(m):
            if f not in dist and set(E[e])&set(E[f]):dist[f]=dist[e]+1;todo.append(f)
    lower=[]
    for n in inp['smaller_orders']:
        for a in range(1,4):
            for b in range(1,4):
                if 4+(a+1)+(b+1)>n:continue
                for x,y in product(range(2),repeat=2):lower.append(model(n,[3,a,b],[0,x,y]))
    return {'verdict':'candidate_only','input_sha256':hashlib.sha256(raw).hexdigest(),'shapes':ss,'old_rows':oldrs,'old_paths':oldps,'old_full':oldfull,'repair_full':repair,'specified_new':new,'families':families,'single_supports':single,'absorption_terms':terms,'gain':max(z['g']-z['r'] for z in terms),'cut_margins':margins,'line_distance_two':sorted([e,d] for e,d in dist.items()),'smaller_realizations':lower}

if __name__=='__main__':
    result=calculate();raw=encode(result)
    assert len(raw)<1048576
    (Path(__file__).resolve().parent/'opg37271-c28-certificate.json').write_bytes(raw)
    print(json.dumps({'verdict':'candidate_only','certificate_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'families':{k:len(v['endpoints']) for k,v in result['families'].items()},'smaller_cases':len(result['smaller_realizations']),'gain':result['gain']},sort_keys=True))
