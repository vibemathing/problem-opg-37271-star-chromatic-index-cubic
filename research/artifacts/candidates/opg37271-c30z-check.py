"""Exact auxiliary order-12 fixed-U audit; no candidate implementation imports.
This program does NOT enumerate all twelve-vertex graphs or claim root closure.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib,json,resource,signal,sys,time
E=[(0,1),(0,2),(0,4),(1,2),(1,6),(2,3),(3,9),(3,10),(4,5),(4,10),(5,7),(5,10),(6,7),(6,11),(7,8),(8,9),(8,11),(9,11)]
U={0,3,5,8,12,14,15}

def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def geometry(edges):
 # Connected four-edge subsets; not the discovery program's vertex-walk generator.
 out=[]
 for I in combinations(range(len(edges)),4):
  verts=Counter(v for i in I for v in edges[i])
  if sorted(verts.values()) not in ([1,1,2,2,2],[2,2,2,2]):continue
  seen={next(iter(verts))}
  while True:
   nxt=seen|{v for i in I if set(edges[i])&seen for v in edges[i]}
   if nxt==seen:break
   seen=nxt
  if len(seen)==len(verts):out.append(I)
 return out

def paths(edges,selected):
 adj={}
 for i in selected:
  a,b=edges[i];adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
 if any(len(x)>2 for x in adj.values()):return None
 left=set(selected);out=[]
 while left:
  i=min(left);seen=set(edges[i]);todo=list(seen);block=set()
  while todo:
   v=todo.pop()
   for u,j in adj[v]:
    block.add(j)
    if u not in seen:seen.add(u);todo.append(u)
  if len(block)>3 or len(seen)!=len(block)+1:return None
  v=min(v for v in seen if len(adj[v])==1);seq=[]
  while len(seq)<len(block):
   u,j=next((u,j) for u,j in adj[v] if j not in seq);seq.append(j);v=u
  out.append(seq);left-=block
 return out

def proper(edges,c):
 for i,j in combinations(range(len(edges)),2):
  if c[i] and c[i]==c[j] and set(edges[i])&set(edges[j]):return False
 return True

def dstar(edges,c):
 if not proper(edges,c):return False
 # Bichromatic components, not four-edge subsets, determine old D validity.
 for a,b in combinations(range(1,5),2):
  left={i for i,v in enumerate(c) if v in (a,b)}
  while left:
   seed=left.pop();block={seed};todo=[seed]
   while todo:
    i=todo.pop();more={j for j in left if set(edges[i])&set(edges[j])}
    left-=more;block|=more;todo.extend(more)
   if len(block)>3:return False
 return True

def connected_support(edges,S):
 if not S:return False
 seen={min(S)};todo=list(seen)
 while todo:
  i=todo.pop();n={j for j in S-seen if set(edges[i])&set(edges[j])};seen|=n;todo.extend(n)
 return seen==S

def endpoint(old,oldpaths,shapes,S):
 if any(set(P)&S and set(P)-S for P in oldpaths):return None
 c=list(old);order=sorted(S)
 for i in order:c[i]=0
 def dfs(j):
  if j==len(order):
   pp=paths(E,{i for i,v in enumerate(c) if v>=5})
   if pp is None or any(set(P)&S and set(P)-S for P in pp):return None
   return list(c)
  i=order[j]
  used={c[k] for k in range(len(E)) if k!=i and set(E[k])&set(E[i])}
  for col in range(1,7):
   if col in used:continue
   c[i]=col
   if not any(i in I and all(c[k] for k in I) and len({c[k] for k in I})==2 for I in shapes):
    got=dfs(j+1)
    if got is not None:return got
   c[i]=0
  return None
 return dfs(0)

def phase_colors(word,pp):
 for bits in product(range(2),repeat=len(pp)):
  c=list(word)
  for P,b in zip(pp,bits):
   for j,e in enumerate(P):c[e]=5+(b^(j%2))
  yield bits,c

def profile(word,newcolors,S,sh,pp):
 nw=[c if c<5 else 0 for c in newcolors];np=paths(E,{i for i,c in enumerate(newcolors) if c>=5})
 def rows(w,ps):
  loc={e:(i,j%2) for i,P in enumerate(ps) for j,e in enumerate(P)};out=[]
  for I in sh:
   d=[e for e in I if w[e]];u=[e for e in I if not w[e]]
   if len(d)!=2 or len(u)!=2 or w[d[0]]!=w[d[1]]:continue
   if set(E[d[0]])&set(E[d[1]]) or set(E[u[0]])&set(E[u[1]]):continue
   a,j=loc[u[0]];b,k=loc[u[1]];out.append([list(I),a,b,1^j^k])
  return out
 oldrows=rows(word,pp);newrows=rows(nw,np);cores=[]
 for size in (1,2,3):
  for comb in combinations(range(len(oldrows)),size):
   parity=rhs=0;H=set()
   for j in comb:
    I,a,b,v=oldrows[j];parity^=(1<<a)^(1<<b);rhs^=v;H.update(I);H.update(pp[a]);H.update(pp[b])
   if parity==0 and rhs==1:cores.append((len(H),sorted(H),list(comb)))
  if cores:break
 assert cores
 _,H,C=min(cores);T=S|set(H)
 assert connected_support(E,T)
 assert not any(set(P)&T and set(P)-T for ps in (pp,np) for P in ps)
 outside=[P for P in pp if not(set(P)&S)];assert outside==[P for P in np if not(set(P)&S)]
 keep=[j for j,P in enumerate(outside) if not(set(P)&T)]
 def tab(w,ps):
  ans={};direct={}
  for bits,c in phase_colors(w,ps):
   b=tuple(bits[ps.index(P)] for P in outside);key=tuple(b[j] for j in keep)
   bad=[I for I in sh if len({c[i] for i in I})==2]
   v=sum(bool(set(I)&S) for I in bad);h=sum(bool(set(I)&T) and not(set(I)&S) for I in bad)
   if b in ans:assert h==ans[b][1];ans[b]=(min(v,ans[b][0]),h)
   else:ans[b]=(v,h)
   direct[key]=min(direct.get(key,1000),v+h)
  return ans,direct
 F,fd=tab(word,pp);Q,qd=tab(nw,np);terms=[];gains={}
 for b,(ov,h) in sorted(F.items()):
  nv,qh=Q[b];assert qh==h;key=tuple(b[j] for j in keep);r=ov+h-fd[key];g=ov-nv
  terms.append([list(b),list(key),ov,nv,h,r,g,g-r]);gains[key]=max(gains.get(key,-1000),g-r)
 assert all(gains[b]==fd[b]-qd[b] for b in fd)
 return {'minimum_negative_core_rows':C,'core_hull':H,'absorption_support':sorted(T),'old_rows':oldrows,'new_rows':newrows,'old_U':pp,'new_U':np,'terms_columns':['outside','remaining','old_sigma','new_sigma','h','r','g','g_minus_r'],'terms':terms}

def audit():
 sh=geometry(E);pp=paths(E,U);D=[i for i in range(len(E)) if i not in U];word=[0]*len(E)
 totals=Counter();records=[];all_D=[]
 def visit(j,top):
  if j<len(D):
   i=D[j];used={word[k] for k in D[:j] if set(E[k])&set(E[i])}
   for col in range(1,min(top+1,4)+1):
    if col in used:continue
    word[i]=col
    if dstar(E,word):visit(j+1,max(top,col))
   word[i]=0;return
  all_D.append(list(word));phase=[]
  for bits in product(range(2),repeat=len(pp)):
   c=list(word)
   for P,b in zip(pp,bits):
    for k,i in enumerate(P):c[i]=5+(b^(k%2))
   bad=[I for I in sh if len({c[i] for i in I})==2]
   phase.append((len(bad),bits,c,bad))
  mu=min(r[0] for r in phase)
  att=[r for r in phase if r[0]==mu]
  if mu!=1 or len(att)!=2:return
  old=att[0][2];bad=set(att[0][3][0]);found=None
  for k in (1,2,3):
   for I in combinations(range(len(E)),k):
    S=set(I)
    if not S&bad or not connected_support(E,S):continue
    c=endpoint(old,pp,sh,S)
    if c is not None:found=(k,I,c);break
   if found:break
  if found is None:raise ValueError('New blocker: requires separate complete endpoint certificate')
  k,I,c=found;S=set(I);nw=[v if v<=4 else 0 for v in c];np=paths(E,{i for i,v in enumerate(c) if v>=5})
  assert dstar(E,nw) and not any(len({c[i] for i in p})==2 for p in sh)
  flipped=[11-v if v>=5 else v for v in c]
  assert all(flipped[i]==att[1][2][i] for i in range(len(E)) if i not in S)
  assert not any(len({flipped[i] for i in p})==2 for p in sh)
  totals[k]+=1;records.append({'word':list(word),'width':k,'support':list(I),'old_bits':list(att[0][1]),'colors':c,'old_phase_costs':[p[0] for p in phase],'profile':profile(list(word),c,S,sh,pp)})
 visit(0,0)
 pairs=sorted([[r['word'],r['width']] for r in records]);data={'verdict':'candidate_only','best_verified_result':'none','scope':'One complete cubic graph of order12 with fixed U; all normalized D-star A colorings are scanned, only mu1 with two old optimal phases are claimed. All U reselections inside supports are allowed. Not the exact-seven-only domain.','edges':E,'U':sorted(U),'all_four_edge_shapes':[list(I) for I in sh],'all_D_star_colorings':len(all_D),'eligible_phase_optimal_frames':len(records),'width_histogram':dict(totals),'word_width_sha256':sha(enc(pairs)),'all_D_words_sha256':sha(enc(sorted(all_D))),'records':records}
 return data

def tests():
 assert not proper([(0,1),(1,2)],[1,1])
 assert paths([(0,1),(1,2),(2,3),(3,4)],{0,1,2,3}) is None
 assert paths([(0,1),(1,2),(2,0)],{0,1,2}) is None
 assert paths([(0,1),(0,2),(0,3)],{0,1,2}) is None
 c4=[(0,1),(1,2),(2,3),(3,0)];assert len(geometry(c4))==1
 assert not dstar(c4,[1,2,1,2])
 chorded=[(0,1),(1,2),(2,3),(3,4),(1,3)]
 assert (0,1,2,3) in geometry(chorded)
 assert connected_support(c4,{0,1}) and not connected_support(c4,{0,2})
 assert paths(E,U)==[[0,3,5],[8],[12,14,15]]
 assert not connected_support(E,set())
 assert len(geometry([(0,1),(2,3),(4,5),(6,7)]))==0
 assert paths(E,set())==[]
 return 12

if __name__=='__main__':
 resource.setrlimit(resource.RLIMIT_AS,(805306368,805306368));resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));signal.alarm(35)
 start=time.monotonic();n=tests();d=audit();out=Path(__file__).with_name('opg37271-c30z-result.json');b=enc(d);assert len(b)<1048576;out.write_bytes(b)
 print(json.dumps({'D':d['all_D_star_colorings'],'eligible':d['eligible_phase_optimal_frames'],'widths':d['width_histogram'],'word_width_sha256':d['word_width_sha256'],'result_sha256':sha(b),'tests':n,'elapsed':time.monotonic()-start}))
