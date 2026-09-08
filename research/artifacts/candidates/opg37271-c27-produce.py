"""C27 finite support producer. No earlier compiler imports. Candidate only."""
from itertools import permutations,combinations,product
from collections import defaultdict,deque
from pathlib import Path
import json,hashlib
class G:
 def __init__(self,n,E):
  self.n=n;self.E=tuple(map(tuple,E));self.m=len(E);self.inc=[[] for _ in range(n)];self.lookup={frozenset(e):i for i,e in enumerate(E)};self.pc={}
  for e,ab in enumerate(E):
   for v in ab:self.inc[v].append(e)
  self.shapes=[]
  for k in (4,5):
   for vs in permutations(range(n),k):
    if k==5 and vs[0]>vs[-1]:continue
    if k==4 and (vs[0]!=min(vs) or vs[1]>vs[-1]):continue
    pairs=[frozenset((vs[i],vs[(i+1)%k])) for i in range(k if k==4 else k-1)]
    if all(p in self.lookup for p in pairs):self.shapes.append((vs,tuple(self.lookup[p] for p in pairs)))
 def paths(self,w):
  mask=sum((1<<e) for e,c in enumerate(w) if c==0)
  if mask in self.pc:return self.pc[mask]
  rem={e for e in range(self.m) if mask>>e&1};out=[]
  while rem:
   part={rem.pop()};todo=list(part)
   while todo:
    for v in self.E[todo.pop()]:
     for f in self.inc[v]:
      if f in rem:rem.remove(f);part.add(f);todo.append(f)
   vs={v for e in part for v in self.E[e]};deg={v:sum(e in part for e in self.inc[v]) for v in vs};ends=sorted(v for v in vs if deg[v]==1)
   if len(part)>3 or len(vs)!=len(part)+1 or len(ends)!=2 or max(deg.values())>2:self.pc[mask]=None;return None
   v=ends[0];seq=[]
   while len(seq)<len(part):
    e=next(e for e in self.inc[v] if e in part and e not in seq);seq.append(e);v=next(t for t in self.E[e] if t!=v)
   out.append(tuple(seq))
  out=tuple(sorted(out,key=lambda P:min(P)));self.pc[mask]=out;return out
 def proper(self,w):return all(len([w[e] for e in es if w[e]])==len({w[e] for e in es if w[e]}) for es in self.inc)
 def valid(self,w):return self.paths(w) is not None and self.proper(w) and all(not all(w[e] for e in es) or not(w[es[0]]==w[es[2]] and w[es[1]]==w[es[3]]) for _,es in self.shapes)
 def rows(self,w):
  ps=self.paths(w);info={e:(i,p%2) for i,P in enumerate(ps) for p,e in enumerate(P)};rows=[]
  for vs,es in self.shapes:
   z=[p for p,e in enumerate(es) if not w[e]]
   if z not in ([0,2],[1,3]):continue
   ds=[e for e in es if w[e]]
   if w[ds[0]]!=w[ds[1]]:continue
   (i,p),(j,q)=[info[es[t]] for t in z];rows.append((i,j,1^p^q,vs,es))
  return rows
 def costs(self,w):
  k=len(self.paths(w));rows=self.rows(w)
  return [sum((((s>>i)^(s>>j))&1)!=b for i,j,b,_,_ in rows) for s in range(1<<k)]
 def closed(self,w,S):return all(not (set(P)&S) or set(P)<=S for P in self.paths(w))
 def endpoints(self,w,S):
  inds=sorted(S);q=list(w)
  def rec(i):
   if i==len(inds):
    if self.valid(q) and self.closed(q,S):yield tuple(q)
    return
   e=inds[i]
   for a in range(5):
    if a and any(q[f]==a for v in self.E[e] for f in self.inc[v] if f!=e and (f not in S or f in inds[:i])):continue
    q[e]=a;yield from rec(i+1)
   q[e]=w[e]
  yield from rec(0)
def canon(w):
 d={0:0};return tuple(d.setdefault(c,len(d)) for c in w)
def decodecode(code,m):
 w=[]
 for _ in range(m):w.append(code%5);code//=5
 return tuple(w)
def full(g,w,s):
 c=list(w)
 for i,P in enumerate(g.paths(w)):
  for j,e in enumerate(P):c[e]=5+((s>>i&1)^(j%2))
 return c

def profile(g,w,S,outside):
 ps=g.paths(w);cost=[None]*(1<<len(outside));att=[None]*len(cost)
 for s in range(1<<len(ps)):
  c=full(g,w,s);b=sum((c[P[0]]-5)<<i for i,P in enumerate(outside))
  bad=[vs for vs,es in g.shapes if set(es)&S and c[es[0]]==c[es[2]] and c[es[1]]==c[es[3]]]
  if cost[b] is None or len(bad)<cost[b]:cost[b]=len(bad);att[b]=c
 return cost,att

def info(g,w):
 ps=g.paths(w);records=[]
 for s in range(1<<len(ps)):
  c=full(g,w,s);bad=[list(vs) for vs,es in g.shapes if c[es[0]]==c[es[2]] and c[es[1]]==c[es[3]]]
  records.append({'phase':s,'colors':c,'cost':len(bad),'first_bad':bad[0] if bad else None})
 return {'word':list(w),'U_paths':[list(P) for P in ps],'phase_costs':[r['cost'] for r in records],'phases':records}

def connected(g,S):
 if not S:return False
 seen={next(iter(S))};stack=list(seen)
 while stack:
  e=stack.pop()
  for f in S-seen:
   if set(g.E[e])&set(g.E[f]):seen.add(f);stack.append(f)
 return seen==S

def table(g,w,S,details=False):
 eps=sorted(g.endpoints(w,S));out=[P for P in g.paths(w) if not set(P)&S]
 rows=[]
 for v in eps:
  p,_=profile(g,v,S,out);row={'word':list(v),'profile':p,'mu':min(g.costs(v))}
  if details:row.update(info(g,v))
  rows.append(row)
 assert rows
 return {'support':sorted(S),'outside_paths':[list(P) for P in out],'count':len(rows),'envelope':[min(r['profile'][i] for r in rows) for i in range(1<<len(out))], 'minimum_mu':min(r['mu'] for r in rows),'endpoints':rows if details else [r['word'] for r in rows],'positive':next((r['word'] for r in rows if r['mu']==0),None)}

def transfer(g,w,v,S,T):
 oldps=g.paths(w);op=[P for P in oldps if not set(P)&S];outs=[P for P in op if not set(P)&T];ins=[P for P in op if set(P)&T]
 a,_=profile(g,w,S,op);a2,_=profile(g,v,S,op);A,_=profile(g,w,T,outs);A2,_=profile(g,v,T,outs)
 new_shapes=[(vs,es) for vs,es in g.shapes if set(es)&T and not set(es)&S]
 rows=[]
 for b in range(1<<len(outs)):
  hz=[];az=[];bz=[]
  for z in range(1<<len(ins)):
   phase={tuple(P):(b>>i&1) for i,P in enumerate(outs)}|{tuple(P):(z>>i&1) for i,P in enumerate(ins)}
   j=sum(phase[tuple(P)]<<i for i,P in enumerate(op));s=sum(phase.get(tuple(P),0)<<i for i,P in enumerate(oldps));c=full(g,w,s)
   h=sum(c[es[0]]==c[es[2]] and c[es[1]]==c[es[3]] for vs,es in new_shapes)
   hz.append(h);az.append(a[j]);bz.append(a2[j])
  r=[az[j]+hz[j]-A[b] for j in range(len(hz))];gain=[az[j]-bz[j] for j in range(len(hz))]
  assert A[b]==min(x+y for x,y in zip(az,hz)) and A2[b]==min(x+y for x,y in zip(bz,hz))
  assert A[b]-A2[b]==max(x-y for x,y in zip(gain,r))
  rows.append({'boundary':b,'h':hz,'old_profile_by_z':az,'new_profile_by_z':bz,'r':r,'g':gain,'max_g_minus_r':A[b]-A2[b]})
 return {'S':sorted(S),'T':sorted(T),'absorbed_paths':[list(P) for P in ins],'outside_paths':[list(P) for P in outs],'new_shape_vertices':[list(vs) for vs,es in new_shapes],'rows':rows}

def small_frames(g):
 w=[0]*g.m
 def rec(e,k):
  if e==g.m:
   if g.valid(w):yield tuple(w)
   return
  for a in range(min(4,k+1)+1):
   if a and any(w[f]==a for v in g.E[e] for f in g.inc[v] if f<e):continue
   w[e]=a;yield from rec(e+1,max(k,a))
  w[e]=0
 yield from rec(0,0)

def main():
 here=Path(__file__).parent;raw=(here/'opg37271-c27-input.json').read_bytes();d=json.loads(raw);g=G(d['n'],d['edges']);w=d['old'];S=set(d['S']);T=set(d['T'])
 assert g.valid(w) and connected(g,S) and g.closed(w,S)
 cert={'verdict':'candidate_only','input_sha256':hashlib.sha256(raw).hexdigest(),'initial':info(g,w),'rows':[{'i':i,'j':j,'sign':b,'vertices':vs,'edges':es} for i,j,b,vs,es in g.rows(w)],'S_table':table(g,w,S,True),'T_table':table(g,w,T,True)}
 cert['expansions']=[]
 for e in range(g.m):
  if e not in T and connected(g,T|{e}):cert['expansions'].append(table(g,w,T|{e}))
 cert['alternate_shortest_chain']=table(g,w,S|{0,5,8})
 cert['repair']=info(g,d['repair'])
 cert['fixed_endpoint_absorptions']=[{'word':v,'transfer':transfer(g,w,v,S,T)} for v in g.endpoints(w,S)]
 cert['phase_exhaustion_supports']=[]
 for mask in range(1<<g.m):
  R={e for e in range(g.m) if mask>>e&1}
  if not S<=R or not connected(g,R) or not g.closed(w,R):continue
  maximum=-99
  for v in g.endpoints(w,S):
   rr=transfer(g,w,v,S,R);maximum=max(maximum,max(row['max_g_minus_r'] for row in rr['rows']))
  cert['phase_exhaustion_supports'].append({'support':sorted(R),'maximum_gain_over_S_endpoints':maximum})
 ctrl=d['c26_absorption_control'];cert['c26_control']={'S_table':table(g,ctrl['old'],set(ctrl['S'])),'T_table':table(g,ctrl['old'],set(ctrl['T'])),'transfer':transfer(g,ctrl['old'],ctrl['new'],set(ctrl['S']),set(ctrl['T']))}
 six=G(6,[(i,(i+1)%6) for i in range(6)]);a=[1,0,1,0,1,0];b=[2,0,1,0,1,0];cert['nonzero_h_control']=transfer(six,a,b,{0},{0,1})
 cert['small_coverage']=[]
 for spec in d['small_graphs']:
  h=G(spec['n'],spec['edges']);states=list(small_frames(h));digest=hashlib.sha256();checked=0;cases=[]
  for v in states:
   cs=h.costs(v);digest.update((''.join(map(str,v))+':'+','.join(map(str,cs))+'\n').encode());mu=min(cs)
   if not mu:continue
   ps=h.paths(v)
   for i,j,sign,vs,es in h.rows(v):
    if i!=j:continue
    H=set(es)|set(ps[i]);out=[P for P in ps if not set(P)&H]
    ep=list(h.endpoints(v,H));prof=[profile(h,u,H,out)[0] for u in ep]
    for s,c in enumerate(cs):
     if c!=mu:continue
     full0=full(h,v,s);bi=sum((full0[P[0]]-5)<<k for k,P in enumerate(out));oldval=profile(h,v,H,out)[0][bi]
     good=next((u for u,pp in zip(ep,prof) if pp[bi]<oldval),None)
     assert good is not None,('smaller self-core blocked',v,H,s)
     checked+=1;cases.append({'word':v,'support':sorted(H),'phase':s,'replacement':good})
  cert['small_coverage'].append({'n':spec['n'],'frames':len(states),'phase_trials':sum(1<<len(h.paths(v)) for v in states),'stream_sha256':digest.hexdigest(),'self_core_attaining_cases':checked,'case_stream_sha256':hashlib.sha256((json.dumps(cases,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()})
 text=json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n';(here/'opg37271-c27-expanded.json').write_text(text)
 compact={'schema_version':'c27-compact-certificate-1','verdict':'candidate_only','input_sha256':cert['input_sha256'],'expanded_sha256':hashlib.sha256(text.encode()).hexdigest(),'initial':cert['initial'],'actual_rows':cert['rows'],'core_support':sorted(S),'absorbed_support':sorted(T),'core_endpoint_words':[[r['word'][e] for e in sorted(S)] for r in cert['S_table']['endpoints']],'core_endpoint_profiles':[r['profile'] for r in cert['S_table']['endpoints']],'absorbed_endpoint_rows':[{'entries':[r['word'][e] for e in sorted(T)],'phase_costs':r['phase_costs'],'first_bad_by_phase':[x['first_bad'] for x in r['phases']]} for r in cert['T_table']['endpoints']],'expansions':[{'support':r['support'],'count':r['count'],'minimum_mu':r['minimum_mu'],'positive':r['positive'],'endpoint_words_sha256':hashlib.sha256((json.dumps(r['endpoints'],separators=(',',':'))+'\n').encode()).hexdigest()} for r in cert['expansions']],'alternate_shortest_chain':{k:cert['alternate_shortest_chain'][k] for k in ('support','count','minimum_mu','positive')},'repair':cert['repair'],'all_fixed_endpoint_absorption_masks':[sum(1<<e for e in r['support']) for r in cert['phase_exhaustion_supports']],'all_fixed_endpoint_absorption_maximum_gains':[r['maximum_gain_over_S_endpoints'] for r in cert['phase_exhaustion_supports']],'c26_gain_slack_control':cert['c26_control']['transfer']['rows'],'nonzero_h_control':cert['nonzero_h_control'],'small_coverage':cert['small_coverage']}
 (here/'opg37271-c27-certificate-replay.json').write_text(json.dumps(compact,sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'verdict':'candidate_only','S_endpoints':cert['S_table']['count'],'T_endpoints':cert['T_table']['count'],'expansions':[(r['support'],r['count'],r['minimum_mu']) for r in cert['expansions']],'all_phase_absorption_supports':len(cert['phase_exhaustion_supports']),'small_frames':[r['frames'] for r in cert['small_coverage']],'small_cases':[r['self_core_attaining_cases'] for r in cert['small_coverage']],'certificate_bytes':len(text.encode()),'certificate_sha256':hashlib.sha256(text.encode()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
