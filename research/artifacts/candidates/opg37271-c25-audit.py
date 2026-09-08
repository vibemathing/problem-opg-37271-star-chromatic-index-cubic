"""C25 graph-bound witnesses and simultaneous-patch profiles. No old core imports."""
from __future__ import annotations
from itertools import permutations, combinations, product
from pathlib import Path
from copy import deepcopy
import json, hashlib, importlib.util, resource, signal
HERE=Path(__file__).resolve().parent

def need(b,msg):
 if not b:raise ValueError(msg)

class Graph:
 def __init__(self,n,edges):
  need(type(n)is int and 1<=n<=10 and len(edges)<=15,'graph bound')
  self.n=n;self.E=[tuple(e) for e in edges];self.m=len(edges);self.adj=[[] for _ in range(n)];index={}
  for i,(u,v) in enumerate(edges):
   need(type(u)is int and type(v)is int and 0<=u<v<n,'endpoints');need((u,v) not in index,'simple edges');index[u,v]=i;self.adj[u].append(i);self.adj[v].append(i)
  need(all(len(es)<=3 for es in self.adj),'subcubic');self.shapes=[]
  for k in (4,5):
   for vs in permutations(range(n),k):
    if k==4 and (vs[0]!=min(vs) or vs[1]>vs[-1]):continue
    if k==5 and vs[0]>vs[-1]:continue
    pairs=[tuple(sorted((vs[j],vs[j+1]))) for j in range(k-1)]
    if k==4:pairs.append(tuple(sorted((vs[-1],vs[0]))))
    if all(e in index for e in pairs):self.shapes.append({'kind':'cycle' if k==4 else 'path','vertices':list(vs),'edges':[index[e] for e in pairs]})
 def paths(self,w):
  pending={i for i,c in enumerate(w) if c==0};ps=[]
  while pending:
   seed=min(pending);es={seed};todo=[seed]
   while todo:
    for v in self.E[todo.pop()]:
     for e in self.adj[v]:
      if w[e]==0 and e not in es:es.add(e);todo.append(e)
   vertices={v for e in es for v in self.E[e]};deg={v:sum(e in es for e in self.adj[v]) for v in vertices}
   ends=sorted(v for v,d in deg.items() if d==1)
   need(1<=len(es)<=3 and max(deg.values())<=2 and len(ends)==2 and len(vertices)==len(es)+1,'U short paths')
   path=[];v=ends[0]
   while len(path)<len(es):
    cand=[e for e in self.adj[v] if e in es and e not in path];need(len(cand)==1,'U walk');e=cand[0];path.append(e);a,b=self.E[e];v=a^b^v
   ps.append(path);pending-=es
  return ps
 def proper(self,w):return all(len([w[e] for e in es if w[e]])==len({w[e] for e in es if w[e]}) for es in self.adj)
 def forbidden(self,c):return [i for i,s in enumerate(self.shapes) if all(c[e] for e in s['edges']) and len({c[e] for e in s['edges']})==2]
 def preframe(self,w):
  need(len(w)==self.m and all(type(c)is int and 0<=c<=4 for c in w),'A palette');ps=self.paths(w);need(self.proper(w),'D proper');need(not self.forbidden(w),'D star');return ps
 def decode(self,w,s):
  ps=self.preframe(w);need(type(s)is int and 0<=s<2**len(ps),'phase range');c=list(w)
  for j,p in enumerate(ps):
   for k,e in enumerate(p):c[e]=5+((s>>j&1)^(k%2))
  need(self.proper(c),'full proper');return c
 def describe(self,w,all_phases=True):
  ps=self.preframe(w);table=[]
  for s in range(2**len(ps)):
   c=self.decode(w,s);bad=self.forbidden(c);table.append({'phase':s,'cost':len(bad),'colors':c,'violations':[self.shapes[i] for i in bad]})
  return {'word':w,'paths':ps,'mu':min(t['cost'] for t in table),'phase_costs':[t['cost'] for t in table],**({'phases':table} if all_phases else {})}
 def pair_check(self,c):
  need(len(c)==self.m and all(type(a)is int and 1<=a<=6 for a in c),'full palette');need(self.proper(c),'full proper')
  for a,b in combinations(range(1,7),2):
   left={e for e,col in enumerate(c) if col in (a,b)}
   while left:
    stack=[left.pop()];count=0
    while stack:
     e=stack.pop();count+=1
     for v in self.E[e]:
      for f in self.adj[v]:
       if f in left:left.remove(f);stack.append(f)
    need(count<=3,'two-color component')
 def positive(self,w,s):
  c=self.decode(w,s);need(not self.forbidden(c),'positive witnesses');self.pair_check(c);return c
 def perfect_matchings(self):
  out=[]
  def rec(left,es):
   if not left:out.append(sorted(es));return
   v=min(left)
   for e in self.adj[v]:
    a,b=self.E[e];u=a^b^v
    if u in left:rec(left-{v,u},es+[e])
  rec(set(range(self.n)),[]);return sorted(out)

def word(code,m):return [code//(5**(m-1-e))%5 for e in range(m)]

def patch_profiles(g,old,new,S):
 """Exact minimization over inside phases, retaining every outside boundary phase."""
 need(all(old[e]==new[e] for e in range(g.m) if e not in S),'outside fixed')
 pa=g.preframe(old);pb=g.preframe(new)
 for ps in (pa,pb):
  need(all(not(set(p)&S) or set(p)<=S for p in ps),'U-closed patch')
 outside_a=[p for p in pa if not(set(p)&S)];outside_b=[p for p in pb if not(set(p)&S)]
 need(outside_a==outside_b,'same exterior components');outside=outside_a
 touched=[i for i,a in enumerate(g.shapes) if set(a['edges'])&S]
 contact={e for i in touched for e in g.shapes[i]['edges']}
 boundary=[p for p in outside if set(p)&contact]
 def profile(w,paths):
  inside=[p for p in paths if set(p)<=S];out=[];attainers=[]
  for b in range(1<<len(boundary)):
   candidates=[]
   for x in range(1<<len(inside)):
    colors=list(w)
    for ps,t in ((boundary,b),(inside,x)):
     for j,p in enumerate(ps):
      for k,e in enumerate(p):colors[e]=5+((t>>j&1)^(k%2))
    # Components not incident to a touched shape can have arbitrary phase zero.
    for p in outside:
     if p not in boundary:
      for k,e in enumerate(p):colors[e]=5+(k%2)
    count=sum(len({colors[e] for e in g.shapes[i]['edges']})==2 for i in touched);candidates.append(count)
   out.append(min(candidates));attainers.append(candidates.index(min(candidates)))
  return out,attainers
 a,ax=profile(old,pa);b,bx=profile(new,pb)
 return {'patch_edges':sorted(S),'boundary_paths':boundary,'old_inside':[p for p in pa if set(p)<=S],'new_inside':[p for p in pb if set(p)<=S],'touched_witnesses':[g.shapes[i] for i in touched],'old_profile':a,'new_profile':b,'old_attainers':ax,'new_attainers':bx,'strict_uniform_gain':min(x-y for x,y in zip(a,b))}

def main():
 signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
 catalog=json.loads((HERE/'opg37271-c25-graphs10.json').read_text());positives=[];pm_failure=[];graphs={}
 for obj in catalog['graphs']:
  j=obj['index'];g=Graph(10,obj['edges']);graphs[j]=g;res=json.loads((HERE/f'opg37271-c25-space10-{j:02d}.json').read_text());candidates=[]
  for U,c,b,mu,v,s in res['U_rows']:
   if not b:continue
   w=word(v,g.m);ps=g.paths(w);spans=len({z for p in ps for e in p for z in g.E[e]})==10
   candidates.append(((not spans,max(map(len,ps),default=0)>2,U),w,s))
  need(candidates,'missing global solution');_,w,s=min(candidates);c=g.positive(w,s);positives.append({'index':j,'word':w,'phase':s,'paths':g.paths(w),'colors':c})
  pm=g.perfect_matchings();byU={row[0]:row for row in res['U_rows']};table=[]
  for M in pm:
   row=byU[sum(1<<e for e in M)];table.append({'U_edges':M,'normal_A_frames':row[1],'balanced_A_frames':row[2],'minimum_mu':row[3]})
  if all(t['balanced_A_frames']==0 for t in table):pm_failure.append({'index':j,'matchings':table})
 need([x['index'] for x in pm_failure]==[18],'perfect matching failure domain')
 # Map every one of the six perfect matchings to a two-C5 decomposition of K5.
 p=graphs[18];fold=[]
 for row in pm_failure[0]['matchings']:
  M=row['U_edges'];owners={v:i for i,e in enumerate(M) for v in p.E[e]};rest=set(range(15))-set(M);cycles=[]
  while rest:
   seed=min(rest);v=p.E[seed][0];start=v;vs=[];es=[];last=-1
   while not vs or v!=start:
    vs.append(v);e=min(e for e in p.adj[v] if e not in M and e!=last);es.append(e);a,b=p.E[e];v=a^b^v;last=e
   need(len(vs)==5 and len(set(vs))==5,'C5 complement');cycles.append(vs);rest-=set(es)
  pairs=[tuple(sorted((owners[a],owners[b]))) for e,(a,b) in enumerate(p.E) if e not in M]
  need(len(cycles)==2 and set(pairs)==set(combinations(range(5),2)),'K5 folded edges')
  fold.append(row|{'complement_cycles':cycles,'folded_cycle_words':[[owners[v] for v in C] for C in cycles]})
 # Known C24 raw state is a negative control, not a new global obstruction.
 E=[[0,5],[0,6],[0,7],[1,4],[1,6],[1,7],[2,3],[2,5],[2,7],[3,4],[3,6],[4,5]]
 g=Graph(8,E);a=[1,0,2,3,2,4,2,0,3,1,0,0];b=[4,0,2,3,1,4,2,0,3,1,0,0]
 pp=patch_profiles(g,a,b,{0,1,4,10});need(pp['old_profile']==[1,1] and pp['new_profile']==[0,0],'phase-optimized simultaneous gain')
 # Reselect a two-edge U path by one genuinely simultaneous fork switch.
 t=a.copy();t[1]=4;t[4]=0
 tp=patch_profiles(g,a,t,{1,4,10});need(tp['old_profile']==[1,1] and tp['new_profile']==[0,0],'topology switch profile')
 rejected_intermediates=[]
 for e,c in ((1,4),(4,0)):
  v=a.copy();v[e]=c
  try:g.preframe(v)
  except ValueError as exc:rejected_intermediates.append({'edit':[e,c],'reason':str(exc)})
  else:raise ValueError('single switch intermediate unexpectedly valid')
 out={'verdict':'candidate_only','global_positive_certificates':positives,'perfect_matching_failure':fold,'simultaneous_patch_example':{'n':8,'edges':E,'old':g.describe(a),'new':g.describe(b),'profile':pp},'graph_18':p.E,'topology_switch':{'n':8,'edges':E,'old':g.describe(a),'new':g.describe(t),'profile':tp,'invalid_single_intermediates':rejected_intermediates}}
 (HERE/'opg37271-c25-witnesses.json').write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'verdict':'candidate_only','global_positive_graphs':len(positives),'all_spanning_short2':all(max(map(len,c['paths']))<=2 and len({v for P in c['paths'] for e in P for v in graphs[c['index']].E[e]})==10 for c in positives),'all_perfect_matching_excluded_graphs':[18],'six_folds_checked':len(fold),'patch_uniform_gain':pp['strict_uniform_gain']}))

if __name__=='__main__':main()
