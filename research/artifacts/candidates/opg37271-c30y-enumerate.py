"""C30 order-eleven extension. Explicit reuse of C30X, no new trust principal.
Run via the bounded driver. Outputs regenerate without external data.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,importlib.util,json,sys
BASE=Path(__file__).resolve().parent

def load(name):
 s=importlib.util.spec_from_file_location(name,BASE/(name+'.py'))
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(enc(x)).hexdigest()
def save(name,x):
 data=enc(x)
 if len(data)>1048576:raise ValueError('per-output limit')
 (BASE/name).write_bytes(data)

def connected(E,n):
 adj={v:set() for v in range(n)}
 for a,b in E:adj[a].add(b);adj[b].add(a)
 seen={0};todo=[0]
 while todo:
  for v in adj[todo.pop()]:
   if v not in seen:seen.add(v);todo.append(v)
 return len(seen)==n

def fast_shapes(E):
 # Discovery/production speed-up; coverage checker below uses separate C30X routines.
 adj={};out={}
 for i,(a,b) in enumerate(E):adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
 def dfs(vs,es):
  if len(es)==4:out[tuple(sorted(es))]=dict(vertices=vs,edges=es,kind='path');return
  for v,e in adj[vs[-1]]:
   if v not in vs:dfs(vs+[v],es+[e])
   elif len(es)==3 and v==vs[0]:out[tuple(sorted(es+[e]))]=dict(vertices=vs,edges=es+[e],kind='cycle')
 for v in adj:dfs([v],[])
 return [out[k] for k in sorted(out)]

CASES=[([3,p,q],[0,a,b]) for p,q in product(range(1,4),repeat=2) if p+q<=5 for a,b in product(range(2),repeat=2)]

def case(k):
 m=load('opg37271-c30x-produce');L,g=CASES[k];r=m.model(11,L,g,stop=False);sk={}
 for ex in r.pop('examples'):
  key=m.canonical_skeleton(ex['edges'],ex['word'],L,11);kid=digest(key)
  sk[kid]={'key':kid,'edges':[[a,b] for a,b,c in key],'word':[c for a,b,c in key],'lengths':L}
 r['skeleton_keys']=sorted(sk);r['skeletons']=[sk[k] for k in sorted(sk)]
 save('opg37271-c30y-case-%02d.json'%k,r)
 print(json.dumps({'stage':'case','index':k,'representatives':len(sk),'solutions':r['solutions_found']}))

def catalog():
 out={};cs=[]
 for k in range(len(CASES)):
  r=json.loads((BASE/('opg37271-c30y-case-%02d.json'%k)).read_text());cs.append({a:b for a,b in r.items() if a!='skeletons'})
  for s in r['skeletons']:out[s['key']]=s
 data={'vertices':11,'cases':cs,'skeletons':[out[k] for k in sorted(out)]}
 save('opg37271-c30y-catalog.json',data);print(json.dumps({'catalog_cases':len(cs),'skeletons':len(out)}))

def batch(start,end):
 m=load('opg37271-c30x-produce');m.shapes=fast_shapes
 cat=json.loads((BASE/'opg37271-c30y-catalog.json').read_text());skels=cat['skeletons'];result=[];h=Counter()
 for sk in skels[start:end]:
  E=list(map(tuple,sk['edges']));entries=[]
  for ee,ww,adds in m.complete_passive(E,sk['word'],11):
   if not connected(ee,11):continue
   try:r=m.repair(ee,ww)
   except ValueError:
    save('opg37271-c30y-obstruction.json',{'vertices':11,'edges':ee,'word':ww,'skeleton':sk['key']})
    raise ValueError('width over three candidate; requires separate full endpoint audit')
   r.pop('smaller_failures',None);pd=m.profile_data(ee,ww,r)
   entries.append({'added_D_edges':adds,**r,'profile_sha256':digest(pd)})
   h[r['width']]+=1
  result.append({'key':sk['key'],'completions':entries})
 data={'range':[start,min(end,len(skels))],'skeletons':result,'width_histogram':dict(h)}
 save('opg37271-c30y-batch-%03d.json'%start,data)
 print(json.dumps({'range':data['range'],'records':sum(h.values()),'widths':dict(h)}))

def check_case(k):
 m=load('opg37271-c30x-check');r=json.loads((BASE/('opg37271-c30y-case-%02d.json'%k)).read_text());L,g=CASES[k]
 assert r['lengths']==L and r['gauge']==g
 q=m.enumerate_case(11,L,g)
 for key in ('class_sha256','all_matchings','productive_classes','solutions_found','class_search_nodes'):assert q[key]==r[key],key
 assert sorted(set(q['skeleton_keys']))==r['skeleton_keys']
 print(json.dumps({'checked_case':k,'class_digest':q['class_sha256']}))

def profile(E,w,r,m,sh,ps,np):
 S=set(r['support']);nw=[c if c<5 else 0 for c in r['colors']]
 def actual_rows(word,pp):
  loc={e:(i,j%2) for i,P in enumerate(pp) for j,e in enumerate(P)};rs=[]
  for I in sh:
   d=[e for e in I if word[e]];u=[e for e in I if not word[e]]
   if len(d)!=2 or len(u)!=2 or word[d[0]]!=word[d[1]]:continue
   if set(E[d[0]])&set(E[d[1]]) or set(E[u[0]])&set(E[u[1]]):continue
   a,i=loc[u[0]];b,j=loc[u[1]];rs.append([list(I),min(a,b),max(a,b),1^i^j])
  return sorted(rs)
 oldrs=actual_rows(w,ps);newrs=actual_rows(nw,np);sr=next(z for z in oldrs if z[1]==z[2]);T=S|set(sr[0])|set(ps[sr[1]])
 outside=[P for P in ps if not(set(P)&S)];assert outside==[P for P in np if not(set(P)&S)]
 remain=[j for j,P in enumerate(outside) if not(set(P)&T)]
 def tab(word,pp):
  records={}
  for bits,c in m.full_phases(E,word,pp):
   key=tuple(bits[pp.index(P)] for P in outside);bad=[I for I in sh if len({c[i] for i in I})==2]
   v=sum(bool(set(I)&S) for I in bad);hh=sum(bool(set(I)&T) and not(set(I)&S) for I in bad)
   if key in records:assert records[key][1]==hh;records[key]=(min(v,records[key][0]),hh)
   else:records[key]=(v,hh)
  return records
 F=tab(w,ps);Q=tab(nw,np);mins={}
 for b,(v,hh) in F.items():
  key=tuple(b[j] for j in remain);mins[key]=min(mins.get(key,10**9),v+hh)
 terms=[]
 for b,(v,hh) in sorted(F.items()):
  key=tuple(b[j] for j in remain);nv,nh=Q[b];assert hh==nh;regret=v+hh-mins[key];gain=v-nv
  terms.append({'b':b,'remaining':key,'old':v,'new':nv,'h':hh,'r':regret,'g':gain,'g_minus_r':gain-regret})
 data={'old_U_paths':ps,'new_U_paths':np,'absorption_support':sorted(T),'outside_paths':outside,'retained_outside_indices':remain,'terms':terms,'old_rows':oldrs,'new_rows':newrs,'all_shape_edge_sets_sha256':digest(sorted([list(I) for I in sh]))}
 data=json.loads(enc(data))
 r['profiles']=data
 m.audit_profile(E,w,r,sh,ps,nw,np)
 assert digest(data)==r['profile_sha256']
 return data


def passive_domain(sk,m):
 from itertools import combinations
 E=list(map(tuple,sk['edges']));w=sk['word'];ps=m.partial_paths(E,w)
 target=m.signature(E,w,m.walk_shapes(E),ps);degree=Counter(v for e in E for v in e)
 pairs=[e for e in combinations(range(11),2) if e not in E and all(degree[v]<3 for v in e)]
 def graphs(j,added):
  if j==len(pairs):yield added;return
  yield from graphs(j+1,added)
  a,b=pairs[j]
  if degree[a]<3 and degree[b]<3:
   degree[a]+=1;degree[b]+=1
   yield from graphs(j+1,added+[pairs[j]])
   degree[a]-=1;degree[b]-=1
 out={}
 for added in graphs(0,[]):
  used={v:set() for v in range(11)}
  for (a,b),c in zip(E,w):
   if c:used[a].add(c);used[b].add(c)
  def colors(j,values):
   if j==len(added):
    adds=tuple((a,b,c) for (a,b),c in zip(added,values));ew=sorted(list(zip(E,w))+[((a,b),c) for a,b,c in adds])
    ee=[e for e,c in ew];ww=[c for e,c in ew]
    if not connected(ee,11):return
    pp=m.partial_paths(ee,ww)
    if pp is not None and m.signature(ee,ww,m.walk_shapes(ee),pp)==target:out[adds]=(ee,ww)
    return
   a,b=added[j]
   for c in range(1,5):
    if c in used[a] or c in used[b]:continue
    used[a].add(c);used[b].add(c);colors(j+1,values+[c]);used[a].remove(c);used[b].remove(c)
  colors(0,[])
 return out

def check_batch(start):
 m=load('opg37271-c30x-check');cat=json.loads((BASE/'opg37271-c30y-catalog.json').read_text());bykey={s['key']:s for s in cat['skeletons']}
 data=json.loads((BASE/('opg37271-c30y-batch-%03d.json'%start)).read_text());lo,hi=data['range'];assert lo==start
 assert [x['key'] for x in data['skeletons']]==[x['key'] for x in cat['skeletons'][lo:hi]]
 hist=Counter();shape_count=0
 for record in data['skeletons']:
  sk=bykey[record['key']];domain=passive_domain(sk,m)
  assert set(domain)=={tuple(map(tuple,e['added_D_edges'])) for e in record['completions']}
  for r in record['completions']:
   E,w=domain[tuple(map(tuple,r['added_D_edges']))];sh=m.walk_shapes(E);ps=m.partial_paths(E,w)
   np=m.partial_paths(E,[c if c<5 else 0 for c in r['colors']]);assert ps is not None and np is not None
   profile(E,w,r,m,sh,ps,np);checked=m.verify_completion(E,w,r);shape_count+=checked['shapes'];hist[r['width']]+=1
 assert {str(k):v for k,v in hist.items()}==data['width_histogram']
 out={'range':[lo,hi],'records':sum(hist.values()),'widths':dict(hist),'actual_shapes':shape_count,'verdict':'candidate_only'}
 save('opg37271-c30y-replay-%03d.json'%start,out);print(json.dumps(out))

if __name__=='__main__':
 action=sys.argv[1];args=list(map(int,sys.argv[2:]));globals()[action](*args)
