"""Literal replay and separate coverage reconstruction for C30 continuation.
No imports from a candidate producer or any earlier candidate module.
The trust domain remains candidate generation. Run with the bounded launcher.
"""
import json,hashlib
from pathlib import Path
from itertools import product,combinations
from collections import Counter

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(enc(x)).hexdigest()
def components(E,inds):
 remain=set(inds);ans=[]
 while remain:
  part={remain.pop()};todo=list(part)
  while todo:
   a=todo.pop()
   for b in list(remain):
    if set(E[a])&set(E[b]):remain.remove(b);part.add(b);todo.append(b)
  ans.append(part)
 return sorted(ans,key=min)
def walk_shapes(E):
 adj={};out={}
 for i,(a,b) in enumerate(E):adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
 def dfs(vs,es):
  if len(es)==4:out[tuple(sorted(es))]=('path',tuple(vs));return
  for v,i in adj[vs[-1]]:
   if v not in vs:dfs(vs+[v],es+[i])
   elif v==vs[0] and len(vs)==4:
    out[tuple(sorted(es+[i]))]=('cycle',tuple(vs))
 for v in adj:dfs([v],[])
 return out

def partial_paths(E,w):
 if len(E)!=len(w) or any(c not in range(5) for c in w):return None
 if len(set(E))!=len(E) or any(a>=b for a,b in E):return None
 deg=Counter(v for e in E for v in e)
 if max(deg.values(),default=0)>3:return None
 for v in deg:
  cs=[c for e,c in zip(E,w) if v in e and c]
  if len(set(cs))!=len(cs):return None
 for a,b in combinations(range(1,5),2):
  if any(len(C)>=4 for C in components(E,[i for i,c in enumerate(w) if c in (a,b)])):return None
 ans=[]
 for C in components(E,[i for i,c in enumerate(w) if not c]):
  ds=Counter(v for i in C for v in E[i])
  if len(C)>3 or len(ds)!=len(C)+1 or max(ds.values())>2:return None
  v=min(v for v,d in ds.items() if d==1);seq=[]
  while len(seq)<len(C):
   i=next(i for i in C if i not in seq and v in E[i]);seq.append(i);v=next(u for u in E[i] if u!=v)
  ans.append(seq)
 return ans

def signature(E,w,sh,pp):
 loc={e:(j,k%2) for j,P in enumerate(pp) for k,e in enumerate(P)};ans=Counter()
 for I in sh:
  d=[i for i in I if w[i]];u=[i for i in I if not w[i]]
  if len(d)!=2 or len(u)!=2 or w[d[0]]!=w[d[1]]:continue
  if set(E[d[0]])&set(E[d[1]]) or set(E[u[0]])&set(E[u[1]]):continue
  a,i=loc[u[0]];b,j=loc[u[1]];ans[min(a,b),max(a,b),1^i^j]+=1
 return ans

def canon(E,w,L,n):
 groups=[];a=0
 for ell in L:groups.append(tuple(range(a,a+ell+1)));a+=ell+1
 keys=[]
 for reversals in product((False,True),repeat=3):
  mp={v:v for v in range(n)}
  for G,R in zip(groups,reversals):mp.update(zip(G,reversed(G) if R else G))
  data=sorted((min(mp[a],mp[b]),max(mp[a],mp[b]),c) for (a,b),c in zip(E,w));names=[];key=[]
  for a,b,c in data:
   if c and c not in names:names.append(c)
   key.append((a,b,names.index(c)+1 if c else 0))
  keys.append(tuple(key))
 return min(keys)

def enumerate_case(n,L,gauge):
 U=[];loc=[];s=0
 for k,ell in enumerate(L):
  U.extend((s+j,s+j+1) for j in range(ell));loc.extend((k,j%2) for j in range(ell));s+=ell+1
 D=[e for e in combinations(range(n),2) if e not in U];pairs={};target=(1,2,3,1)
 for i,j in combinations(range(len(D)),2):
  if set(D[i])&set(D[j]):continue
  cnt=[0]*4;forbidden=False
  for a,b in combinations(range(len(U)),2):
   if set(U[a])&set(U[b]):continue
   four=[D[i],D[j],U[a],U[b]]
   # Two disjoint matchings form paths/even cycles. Four simple edges
   # on 4 or 5 incident vertices are exactly a C4 or four-edge path.
   if len({x for e in four for x in e}) not in (4,5):continue
   v,p=loc[a];w,q=loc[b];rhs=1^p^q
   if v==w:
    if v!=0 or rhs!=1:forbidden=True;break
    cell=0
   else:
    if rhs!=gauge[v]^gauge[w]:forbidden=True;break
    cell={(0,1):1,(0,2):2,(1,2):3}[v,w]
   cnt[cell]+=1
  pairs[i,j]=None if forbidden else tuple(cnt)
 classes=[];allmatchings=0
 def match(next_i,chosen,used):
  nonlocal allmatchings
  allmatchings+=1
  if len(chosen)>=2:
   counts=[0]*4;touched=set();ok=True
   for i,j in combinations(chosen,2):
    z=pairs.get((i,j))
    if z is None:ok=False;break
    if any(z):touched.update((i,j))
    counts=[a+b for a,b in zip(counts,z)]
   if ok and touched==set(chosen) and all(a<=b for a,b in zip(counts,target)):
    classes.append((tuple(chosen),tuple(counts)))
  for i in range(next_i,len(D)):
   if not (used&set(D[i])):match(i+1,chosen+(i,),used|set(D[i]))
 match(0,(),set());classes.sort()
 ud=Counter(v for e in U for v in e);class_deg=[Counter(v for i in I for v in D[i]) for I,c in classes]
 allowed={}
 for i,j in combinations(range(len(classes)),2):
  I,J=classes[i][0],classes[j][0]
  if set(I)&set(J):allowed[i,j]=False;continue
  edges=[D[a] for a in I+J];allowed[i,j]=all(len(C)<4 for C in components(edges,range(len(edges))))
 solutions=[];visits=0
 def choose(next_i,chosen,counts,degree):
  nonlocal visits
  visits+=1
  if counts==target:solutions.append(chosen);return
  if len(chosen)==4:return
  for j in range(next_i,len(classes)):
   if any(not allowed[i,j] for i in chosen):continue
   cc=tuple(a+b for a,b in zip(counts,classes[j][1]))
   if any(a>b for a,b in zip(cc,target)):continue
   dd=degree+class_deg[j]
   if any(dd[v]+ud[v]>3 for v in range(n)):continue
   choose(j+1,chosen+(j,),cc,dd)
 choose(0,(),(0,0,0,0),Counter())
 keys=[]
 for sol in solutions:
  E=U.copy();w=[0]*len(U)
  for col,j in enumerate(sol,1):E.extend(D[i] for i in classes[j][0]);w.extend([col]*len(classes[j][0]))
  keys.append(sha(canon(E,w,L,n)))
 # Match the source's raw class serialization solely as an artifact comparison.
 raw=json.dumps(classes,separators=(',',':')).encode()
 return {'class_sha256':hashlib.sha256(raw).hexdigest(),'all_matchings':allmatchings,'productive_classes':len(classes),'solutions_found':len(solutions),'skeleton_keys':keys,'class_search_nodes':visits}

def full_phases(E,w,pp):
 for bits in product(range(2),repeat=len(pp)):
  c=list(w)
  for P,b in zip(pp,bits):
   for j,i in enumerate(P):c[i]=5+(b^(j%2))
  yield bits,c

def literal_valid(E,c,S,sh):
 if any(c[i]==c[j] and set(E[i])&set(E[j]) for i,j in combinations(range(len(E)),2)):return False
 if any(len({c[i] for i in I})==2 for I in sh):return False
 for C in components(E,[i for i,v in enumerate(c) if v>=5]):
  if C&S and C-S:return False
 return True

def exists_star_on_support(E,w,old,S,sh):
 adj=[{j for j in range(len(E)) if j!=i and set(E[i])&set(E[j])} for i in range(len(E))]
 c=list(old);I=sorted(S)
 for i in S:c[i]=0
 def dfs(k):
  if k==len(I):return literal_valid(E,c,S,sh)
  i=I[k]
  for a in range(1,7):
   if any(c[j]==a for j in adj[i]):continue
   c[i]=a
   if not any(all(c[j] for j in z) and len({c[j] for j in z})==2 for z in sh if i in z):
    if dfs(k+1):return True
   c[i]=0
  return False
 return dfs(0)

def audit_profile(E,w,R,sh,ps,newword,np):
 S=set(R['support']);d=R['profiles'];T=set(d['absorption_support'])
 assert d['old_U_paths']==ps and d['new_U_paths']==np
 assert S<=T and len(components(E,T))==1
 for pp in (ps,np):assert not any(set(P)&T and set(P)-T for P in pp)
 outside=[P for P in ps if not(set(P)&S)];assert outside==d['outside_paths']
 assert [P for P in np if not(set(P)&S)]==outside
 remain=[j for j,P in enumerate(outside) if not(set(P)&T)];assert remain==d['retained_outside_indices']
 def table(word,pp):
  out={}
  for bits,c in full_phases(E,word,pp):
   key=tuple(bits[pp.index(P)] for P in outside);bad=[I for I in sh if len({c[i] for i in I})==2]
   v=sum(bool(set(I)&S) for I in bad);h=sum(bool(set(I)&T) and not(set(I)&S) for I in bad)
   out.setdefault(key,[]).append((v,h))
  return {key:(min(v for v,h in vals),next(iter({h for v,h in vals}))) for key,vals in out.items()}
 F=table(w,ps);Q=table(newword,np);minima={}
 for b,(v,h) in F.items():
  key=tuple(b[i] for i in remain);minima[key]=min(minima.get(key,10**9),v+h)
 terms=[]
 for b in sorted(F):
  key=tuple(b[i] for i in remain);ov,h=F[b];nv,hh=Q[b];assert h==hh;r=ov+h-minima[key];g=ov-nv
  terms.append({'b':list(b),'remaining':list(key),'old':ov,'new':nv,'h':h,'r':r,'g':g,'g_minus_r':g-r})
 assert terms==d['terms']
 for key in minima:
  newmin=min(Q[b][0]+Q[b][1] for b in Q if tuple(b[i] for i in remain)==key)
  assert minima[key]-newmin==max(z['g_minus_r'] for z in terms if tuple(z['remaining'])==key)
 def actual_rows(word,pp):
  loc={e:(j,k%2) for j,P in enumerate(pp) for k,e in enumerate(P)};out=[]
  for I in sh:
   a=[i for i in I if word[i]];b=[i for i in I if not word[i]]
   if len(a)!=2 or len(b)!=2 or word[a[0]]!=word[a[1]]:continue
   if set(E[a[0]])&set(E[a[1]]) or set(E[b[0]])&set(E[b[1]]):continue
   v,i=loc[b[0]];z,j=loc[b[1]];out.append([list(I),min(v,z),max(v,z),1^i^j])
  return sorted(out)
 assert actual_rows(w,ps)==d['old_rows'];assert actual_rows(newword,np)==d['new_rows']
 assert sha(sorted([list(I) for I in sh]))==d['all_shape_edge_sets_sha256']

def verify_completion(E,w,entry):
 sh=walk_shapes(E);ps=partial_paths(E,w);assert ps is not None
 allold=[(bits,c,sum(len({c[i] for i in z})==2 for z in sh)) for bits,c in full_phases(E,w,ps)]
 assert min(x[2] for x in allold)==1
 ats=[x for x in allold if x[2]==1];assert len(ats)==2
 S=set(entry['support']);assert len(S)==entry['width'] and len(components(E,S))==1
 assert all(not(set(P)&S) or not(set(P)-S) for P in ps)
 assert tuple(entry['old_bits'])==ats[0][0]
 new=entry['colors'];assert len(new)==len(E) and all(1<=x<=6 for x in new)
 assert all(ats[0][1][i]==new[i] for i in range(len(E)) if i not in S)
 assert literal_valid(E,new,S,sh)
 nw=[v if v<5 else 0 for v in new];np=partial_paths(E,nw);assert np is not None
 assert all(not(set(P)&S) or not(set(P)-S) for P in np)
 audit_profile(E,w,entry,sh,ps,nw,np)
 complement=[11-v if v>=5 else v for v in new]
 assert literal_valid(E,complement,S,sh)
 assert all(ats[1][1][i]==complement[i] for i in range(len(E)) if i not in S)
 # Check all smaller geometric supports, not a walk in a reconfiguration graph.
 if entry['width']>1:
  for k in range(1,entry['width']):
   for I in combinations(range(len(E)),k):
    R=set(I)
    if len(components(E,R))!=1 or any(set(P)&R and set(P)-R for P in ps):continue
    assert not exists_star_on_support(E,w,ats[0][1],R,sh)
 return {'shapes':len(sh),'old_phase_count':len(allold)}

def passive_words(sk,n):
 E=list(map(tuple,sk['edges']));w=sk['word'];ps=partial_paths(E,w);assert ps is not None
 target=signature(E,w,walk_shapes(E),ps);d=Counter(v for e in E for v in e)
 pairs=[e for e in combinations(range(n),2) if e not in E and all(d[v]<3 for v in e)]
 out={}
 # First enumerate every residual-degree-feasible uncolored passive graph.
 # This is separate from producer's edge/color/row-prefix search.
 graphs=[]
 def edge_sets(j,chosen,degree):
  if j==len(pairs):graphs.append(chosen);return
  edge_sets(j+1,chosen,degree)
  a,b=pairs[j]
  if degree[a]<3 and degree[b]<3:
   nd=degree.copy();nd[a]+=1;nd[b]+=1
   edge_sets(j+1,chosen+[pairs[j]],nd)
 edge_sets(0,[],d)
 for added in graphs:
  for values in product(range(1,5),repeat=len(added)):
   adds=tuple((a,b,c) for (a,b),c in zip(added,values))
   ee=sorted(list(zip(E,w))+[((a,b),c) for a,b,c in adds]);edges=[e for e,c in ee];word=[c for e,c in ee]
   pp=partial_paths(edges,word)
   if pp is None:continue
   if signature(edges,word,walk_shapes(edges),pp)!=target:continue
   out[adds]=(edges,word)

 return out

def coverage_case_domain(cases,n):
 expected=[([3,p,q],[0,a,b]) for p,q in product(range(1,4),repeat=2) if p+q+6<=n for a,b in product(range(2),repeat=2)]
 assert [(x['lengths'],x['gauge']) for x in cases]==expected

def completion_domain(sk,n):
 c=passive_words(sk,n)
 assert set(c)=={tuple(map(tuple,e['added_D_edges'])) for e in sk['completions']}
 return c

def main():
 root=Path(__file__).resolve().parent;raw=(root/'opg37271-c30x-input.json').read_bytes();data=json.loads((root/'opg37271-c30x-certificate.json').read_bytes());n=json.loads(raw)['vertices']
 assert data['input_sha256']==hashlib.sha256(raw).hexdigest();assert n==10
 cases_expected=[([3,p,q],[0,a,b]) for p,q in product(range(1,4),repeat=2) if p+q<=4 for a,b in product(range(2),repeat=2)]
 coverage_case_domain(data['cases'],n)
 expected_small=[(nn,[3,p,q],[0,a,b]) for nn in (8,9) for p,q in product(range(1,4),repeat=2) if p+q+6<=nn for a,b in product(range(2),repeat=2)]
 assert [(x['n'],x['lengths'],x['gauge']) for x in data['smaller_cases']]==expected_small
 for old in data['smaller_cases']:
  rr=enumerate_case(old['n'],old['lengths'],old['gauge'])
  assert rr['solutions_found']==0
  for key in ('class_sha256','all_matchings','productive_classes','solutions_found','class_search_nodes'):assert rr[key]==old[key]
 allkeys=set()
 for old in data['cases']:
  r=enumerate_case(n,old['lengths'],old['gauge'])
  for key in ('class_sha256','all_matchings','productive_classes','solutions_found','class_search_nodes'):
   assert r[key]==old[key],(old['lengths'],old['gauge'],key,r[key],old[key])
  assert sorted(r['skeleton_keys'])==sorted(old['skeleton_keys']);allkeys.update(r['skeleton_keys'])
 assert allkeys=={sk['key'] for sk in data['skeletons']}
 h=Counter();count=0;shape_count=0
 for sk in data['skeletons']:
  assert sk['key']==sha(list(zip([e[0] for e in sk['edges']],[e[1] for e in sk['edges']],sk['word'])))
  candidates=completion_domain(sk,n)
  for entry in sk['completions']:
   E,w=candidates[tuple(map(tuple,entry['added_D_edges']))];r=verify_completion(E,w,entry);shape_count+=r['shapes'];count+=1;h[entry['width']]+=1
 assert {str(k):v for k,v in h.items()}==data['width_histogram'];assert count==data['full_completion_records']
 result={'verdict':'candidate_only','best_verified_result':'none','certificate_sha256':hashlib.sha256((root/'opg37271-c30x-certificate.json').read_bytes()).hexdigest(),'coverage_cases':len(data['cases']),'lower_order_cases':len(data['smaller_cases']),'productive_representatives':len(allkeys),'complete_passive_records':count,'width_histogram':dict(h),'actual_four_edge_shape_occurrences_rebuilt':shape_count,'trusted_execution':False}
 (root/'opg37271-c30x-check-result.json').write_bytes(enc(result));print(json.dumps(result))
if __name__=='__main__':main()
