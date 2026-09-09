"""Explicit C30X reuse for discovery/reference; the Z checker imports no core."""
from pathlib import Path
import importlib.util,json,hashlib,resource,signal
from itertools import product
from collections import Counter
B=Path(__file__).resolve().parent
p=B/'opg37271-c30x-produce.py'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='a7f02ae72f62585356fedd3a93d49d01726083c690900f5d4e90d2302c49a1d9'
s=importlib.util.spec_from_file_location('c30x_reuse',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
E=[(0,1),(0,2),(0,4),(1,2),(1,6),(2,3),(3,9),(3,10),(4,5),(4,10),(5,7),(5,10),(6,7),(6,11),(7,8),(8,9),(8,11),(9,11)]
U={0,3,5,8,12,14,15}

def shapes(E):
 adj={};out={}
 for i,(a,b) in enumerate(E):adj.setdefault(a,[]).append((b,i));adj.setdefault(b,[]).append((a,i))
 def dfs(vs,es):
  if len(es)==4:out[tuple(sorted(es))]=dict(vertices=vs,edges=es,kind='path');return
  for u,i in adj[vs[-1]]:
   if u not in vs:dfs(vs+[u],es+[i])
   elif len(es)==3 and u==vs[0]:out[tuple(sorted(es+[i]))]=dict(vertices=vs,edges=es+[i],kind='cycle')
 for v in adj:dfs([v],[])
 return [out[k] for k in sorted(out)]

def main():
 m.shapes=shapes;ss=shapes(E);D=[i for i in range(len(E)) if i not in U];ds=[q['edges'] for q in ss if not U.intersection(q['edges'])];w=[0]*len(E);allw=[];pairs=[];hist=Counter()
 def rec(j,top):
  if j==len(D):
   allw.append(w.copy());obj=m.rows(E,w,ss)
   assert obj is not None
   pp,rr=obj;cost=[sum((b[q['i']]^b[q['j']])!=q['rhs'] for q in rr) for b in product(range(2),repeat=len(pp))]
   if min(cost)!=1 or cost.count(1)!=2:return
   r=m.repair(E,w);pairs.append([w.copy(),r['width']]);hist[r['width']]+=1;return
  i=D[j];used={w[k] for k in D[:j] if set(E[k])&set(E[i])}
  for c in range(1,min(4,top+1)+1):
   if c in used:continue
   w[i]=c
   if not any(all(w[k] for k in I) and len({w[k] for k in I})==2 for I in ds):rec(j+1,max(top,c))
  w[i]=0
 rec(0,0)
 enc=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
 out={'all_D_star_colorings':len(allw),'eligible_phase_optimal_frames':len(pairs),'width_histogram':dict(hist),'word_width_sha256':hashlib.sha256(enc(sorted(pairs))).hexdigest(),'all_D_words_sha256':hashlib.sha256(enc(sorted(allw))).hexdigest(),'verdict':'candidate_only'}
 (B/'opg37271-c30z-reference.json').write_bytes(enc(out));print(json.dumps(out))
if __name__=='__main__':
 resource.setrlimit(resource.RLIMIT_AS,(805306368,805306368));resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576));signal.alarm(35);main()
