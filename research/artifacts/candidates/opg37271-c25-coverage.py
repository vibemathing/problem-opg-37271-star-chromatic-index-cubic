"""Graph catalogue coverage without using the graph generator's search or hashes."""
from functools import lru_cache
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import json, resource, signal
HERE=Path(__file__).resolve().parent

def need(b,msg):
 if not b:raise ValueError(msg)

@lru_cache(None)
def realizations(ds):
 """Number of labelled simple realizations of this sorted degree sequence."""
 if not ds:return 1
 if ds[-1]==0:return 1
 d=ds[-1];left=list(ds[:-1]);n=len(left)
 if d>n or sum(ds)%2:return 0
 groups=[left.count(k) for k in range(4)];total=0
 for take in product(*(range(groups[k]+1) for k in (1,2,3))):
  if sum(take)!=d:continue
  count=groups.copy();weight=1
  for k,num in zip((1,2,3),take):count[k]-=num;count[k-1]+=num;weight*=comb(groups[k],num)
  residual=tuple(k for k in range(4) for _ in range(count[k]))
  total+=weight*realizations(residual)
 return total

def matrix(n,E):
 need(len(E)==3*n//2 and len({tuple(e) for e in E})==len(E),'simple size')
 a=[[0]*n for _ in range(n)]
 for u,v in E:need(type(u)is int and type(v)is int and 0<=u<v<n,'vertices');a[u][v]=a[v][u]=1
 need(all(sum(r)==3 for r in a),'cubic')
 seen={0};todo=[0]
 while todo:
  for v,b in enumerate(a[todo.pop()]):
   if b and v not in seen:seen.add(v);todo.append(v)
 need(len(seen)==n,'connected');return a

def maps(a,b,stop_first=False):
 n=len(a);f=[-1]*n;used=set();answer=0
 def rec():
  nonlocal answer
  left=[v for v in range(n) if f[v]<0]
  if not left:answer+=1;return stop_first
  v=max(left,key=lambda v:sum(a[v][u] for u in range(n) if f[u]>=0))
  for w in range(n):
   if w in used or any(a[v][u]!=b[w][f[u]] for u in range(n) if f[u]>=0):continue
   f[v]=w;used.add(w)
   if rec():return True
   used.remove(w);f[v]=-1
  return False
 rec();return answer

def check(catalog):
 n=catalog['n'];need(4<=n<=10 and n%2==0,'order')
 graphs=catalog['graphs'];need([g['index'] for g in graphs]==list(range(len(graphs))),'indices')
 aa=[matrix(n,g['edges']) for g in graphs];autos=[]
 for i,a in enumerate(aa):
  for j in range(i):need(maps(a,aa[j],True)==0,'duplicate graph orbit')
  k=maps(a,a);need(k==graphs[i]['automorphisms'],'automorphism count');autos.append(k)
 T={0:1};C={0:0}
 for s in range(1,n+1):
  T[s]=realizations((3,)*s)
  C[s]=T[s]-sum(comb(s-1,k-1)*C[k]*T[s-k] for k in range(1,s))
 total=sum(factorial(n)//a for a in autos)
 need(total==C[n]==catalog['connected_labelled_total'],'orbit total vs independent degree DP')
 return {'n':n,'types':len(graphs),'automorphisms':autos,'all_labelled_simple_cubic':T[n],'connected_labelled_cubic':C[n],'disconnected_labelled_cubic':T[n]-C[n],'orbit_sum':total,'pairwise_nonisomorphism_tests':len(graphs)*(len(graphs)-1)//2,'degree_DP_cache':realizations.cache_info().currsize}

if __name__=='__main__':
 signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
 data=json.loads((HERE/'opg37271-c25-graphs10.json').read_text());report=check(data);report['verdict']='candidate_only'
 print(json.dumps(report,sort_keys=True))
