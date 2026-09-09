"""C30 continuation producer. Matching reduction adapted from pinned C28 source.
No claim of separate trust. The companion verifier imports no candidate code.
Exact seven-row patterns on ten vertices only; not a full ten-vertex frame census.
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
   if True: # Unused productive vertices retained for passive completion coverage.
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
 res['examples']=[]
 for sol in solutions:
  ee=U.copy();cc=[0]*len(U)
  for color,k in enumerate(sol,1):
   for e in classes[k][0]:ee.append(D[e]);cc.append(color)
  res['examples'].append({'edges':ee,'word':cc})

 return res


# All geometric isomorphisms used below are explicit reversals of designated U paths.
def canonical_skeleton(E,w,L,n):
 blocks=[];v=0
 for ell in L:blocks.append(list(range(v,v+ell+1)));v+=ell+1
 best=None
 for flip in product(range(2),repeat=3):
  mp=list(range(n))
  for B,f in zip(blocks,flip):
   for a,b in zip(B,B[::-1] if f else B):mp[a]=b
  ew=sorted((tuple(sorted((mp[a],mp[b]))),c) for (a,b),c in zip(E,w));colors={0:0};key=[]
  for e,c in ew:
   if c not in colors:colors[c]=len(colors)
   key.append((e[0],e[1],colors[c]))
  key=tuple(key)
  if best is None or key<best:best=key
 return best

def sig(E,w,ss=None):
 z=rows(E,w,ss)
 return None if z is None else Counter((min(r['i'],r['j']),max(r['i'],r['j']),r['rhs']) for r in z[1])

def complete_passive(E,w,n):
 # Every edge in the completed graph is retained in every endpoint test.
 deg=Counter(v for e in E for v in e)
 pairs=[(a,b) for a,b in combinations(range(n),2) if deg[a]<3 and deg[b]<3 and (a,b) not in E]
 target=sig(E,w)
 def rec(j,ee,ww,adds):
  if j==len(pairs):yield ee,ww,adds;return
  yield from rec(j+1,ee,ww,adds)
  a,b=pairs[j]
  if deg[a]>=3 or deg[b]>=3:return
  used={c for e,c in zip(ee,ww) if a in e or b in e}
  for color in range(1,5):
   if color in used:continue
   ew=sorted(list(zip(ee,ww))+[((a,b),color)]);ne=[e for e,c in ew];nw=[c for e,c in ew]
   if sig(ne,nw)!=target:continue
   deg[a]+=1;deg[b]+=1
   yield from rec(j+1,ne,nw,adds+[[a,b,color]])
   deg[a]-=1;deg[b]-=1
 yield from rec(0,E,w,[])

def conn(E,S):
 seen={min(S)};stack=list(seen)
 while stack:
  i=stack.pop()
  for j in S-seen:
   if set(E[i])&set(E[j]):seen.add(j);stack.append(j)
 return seen==S

def repair(E,w):
 sh=shapes(E);ps,rr=rows(E,w,sh);records=[]
 for bits in product(range(2),repeat=len(ps)):
  full=w.copy()
  for p,b in zip(ps,bits):
   for j,e in enumerate(p):full[e]=5+(b^(j%2))
  bad=[s['edges'] for s in sh if len({full[i] for i in s['edges']})==2]
  records.append((len(bad),bits,full,bad))
 minimum=min(z[0] for z in records);assert minimum==1
 att=[z for z in records if z[0]==minimum];assert len(att)==2
 old=att[0][2];selfshape=set(att[0][3][0]);m=len(E)
 adj=[{j for j in range(m) if j!=i and set(E[i])&set(E[j])} for i in range(m)]
 rel=[[s['edges'] for s in sh if i in s['edges']] for i in range(m)]
 # Literal endpoint coloring detects mu=0 directly; all B phases are included.
 tried=[]
 for k in range(1,4):
  for I in combinations(range(m),k):
   S=set(I)
   if not conn(E,S) or any(set(p)&S and set(p)-S for p in ps):continue
   if not (S&selfshape):tried.append([list(I),'unchanged_bad_shape']);continue
   c=old.copy()
   for i in I:c[i]=0
   leaves=0
   def extend(j):
    nonlocal leaves
    if j==k:
     leaves+=1;pw=[a if a<5 else 0 for a in c];np=u_paths(E,pw)
     if np is not None and not any(set(p)&S and set(p)-S for p in np):return c.copy()
     return None
    i=I[j];used={c[a] for a in adj[i]}
    for color in range(1,7):
     if color in used:continue
     c[i]=color
     if not any(all(c[a] for a in z) and len({c[a] for a in z})==2 for z in rel[i]):
      ans=extend(j+1)
      if ans is not None:return ans
     c[i]=0
    return None
   found=extend(0)
   if found is not None:
    return {'width':k,'support':list(I),'old_bits':list(att[0][1]),'colors':found,'smaller_failures':tried if k>1 else []}
   tried.append([list(I),leaves])
 raise ValueError('Exact family has an uncovered width>3 state')

def profile_data(E,w,R):
 S=set(R['support']);sh=shapes(E);oldps,oldrows=rows(E,w,sh)
 newword=[a if a<5 else 0 for a in R['colors']];newps,newrows=rows(E,newword,sh)
 selfrow=next(z for z in oldrows if z['i']==z['j'])
 H=set(selfrow['edges'])|set(oldps[selfrow['i']]);T=S|H
 assert conn(E,T)
 for pp in (oldps,newps):assert not any(set(P)&T and set(P)-T for P in pp)
 outside=[P for P in oldps if not(set(P)&S)]
 assert outside==[P for P in newps if not(set(P)&S)]
 def tables(word,pp):
  profiles={};costs=[]
  for bits in product(range(2),repeat=len(pp)):
   c=word.copy()
   for P,b in zip(pp,bits):
    for j,e in enumerate(P):c[e]=5+(b^(j%2))
   bad=[z for z in sh if len({c[i] for i in z['edges']})==2]
   key=tuple(bits[pp.index(P)] for P in outside)
   touch=sum(bool(S&set(z['edges'])) for z in bad)
   h=sum(bool(T&set(z['edges'])) and not(S&set(z['edges'])) for z in bad)
   if key not in profiles:profiles[key]=[touch,h]
   else:
    assert profiles[key][1]==h
    profiles[key][0]=min(profiles[key][0],touch)
  return profiles
 F=tables(w,oldps);Q=tables(newword,newps);remain=[j for j,P in enumerate(outside) if not(set(P)&T)]
 assert all(F[k][1]==Q[k][1] for k in F)
 m={}
 for b,(v,h) in F.items():
  key=tuple(b[j] for j in remain);m[key]=min(m.get(key,10**9),v+h)
 terms=[]
 for b in sorted(F):
  ov,h=F[b];nv=Q[b][0];key=tuple(b[j] for j in remain);r=ov+h-m[key];g=ov-nv
  terms.append({'b':b,'remaining':key,'old':ov,'new':nv,'h':h,'r':r,'g':g,'g_minus_r':g-r})
 def norm(rr):return sorted([sorted(z['edges']),min(z['i'],z['j']),max(z['i'],z['j']),z['rhs']] for z in rr)
 return {'old_U_paths':oldps,'new_U_paths':newps,'absorption_support':sorted(T),'outside_paths':outside,'retained_outside_indices':remain,'terms':terms,'old_rows':norm(oldrows),'new_rows':norm(newrows),'all_shape_edge_sets_sha256':hashlib.sha256(encode(sorted(sorted(z['edges']) for z in sh))).hexdigest()}

def encode(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def main():
 base=Path(__file__).resolve().parent;raw=(base/'opg37271-c30x-input.json').read_bytes();inp=json.loads(raw);n=inp['vertices'];cases=[];skels={}
 for p,q in product(range(1,4),repeat=2):
  if 3+(p+1)+(q+1)+1>n:continue
  L=[3,p,q]
  for a,b in product(range(2),repeat=2):
   r=model(n,L,[0,a,b],stop=False)
   case={k:v for k,v in r.items() if k!='examples'};case['skeleton_keys']=[]
   for ex in r['examples']:
    key=canonical_skeleton(ex['edges'],ex['word'],L,n);kid=hashlib.sha256(encode(key)).hexdigest()
    skels[kid]={'edges':[[a,b] for a,b,c in key],'word':[c for a,b,c in key],'lengths':L}
    case['skeleton_keys'].append(kid)
   cases.append(case)
 smaller=[]
 for nn in (8,9):
  for p,q in product(range(1,4),repeat=2):
   if p+q+6>nn:continue
   for a,b in product(range(2),repeat=2):
    rr=model(nn,[3,p,q],[0,a,b],stop=False);assert not rr['examples']
    smaller.append({k:v for k,v in rr.items() if k!='examples'})
 out=[];hist=Counter()
 for kid,sk in sorted(skels.items()):
  E=list(map(tuple,sk['edges']));w=sk['word'];comps=[]
  for ee,ww,added in complete_passive(E,w,n):
   R=repair(ee,ww);R['profiles']=profile_data(ee,ww,R);hist[R['width']]+=1
   comps.append({'added_D_edges':added,**R})
  out.append({'key':kid,**sk,'completions':comps})
 result={'verdict':'candidate_only','best_verified_result':'none','input_sha256':hashlib.sha256(raw).hexdigest(),'cases':cases,'smaller_cases':smaller,'skeletons':out,'width_histogram':dict(hist),'full_completion_records':sum(hist.values())}
 data=encode(result);assert len(data)<=1048576
 (base/'opg37271-c30x-certificate.json').write_bytes(data)
 print(json.dumps({'bytes':len(data),'cases':len(cases),'productive_representatives':len(out),'full_completion_records':sum(hist.values()),'widths':dict(hist),'sha256':hashlib.sha256(data).hexdigest()}))
if __name__=='__main__':main()
