"""C27 separate finite checker: edge-subset shapes, literal endpoint words,
edge-by-edge B assignments, no imports from any candidate generator/compiler.
Run with the companion process limits. All output remains candidate_only.
"""
from itertools import combinations,product,permutations
from pathlib import Path
from copy import deepcopy
import hashlib,json

def need(p,msg):
 if not p:raise ValueError(msg)

def normal(w):
 lab={0:0};return tuple(lab.setdefault(x,len(lab)) for x in w)

class Direct:
 def __init__(self,n,E):
  need(type(n)is int and 0<=n<=10 and len(E)<=15,'graph limit')
  self.n=n;self.E=[tuple(e) for e in E];self.m=len(E);self.inc=[[] for _ in range(n)];self.cache={}
  need(all(len(e)==2 and all(type(v)is int and 0<=v<n for v in e) and e[0]!=e[1] for e in E),'endpoint domain')
  need(len({frozenset(e) for e in E})==self.m,'simple graph')
  for i,ab in enumerate(E):
   for v in ab:self.inc[v].append(i)
  need(all(len(es)<=3 for es in self.inc),'subcubic')
  shapes=[]
  for ids in combinations(range(self.m),4):
   verts={v for e in ids for v in E[e]};degree={v:sum(v in E[e] for e in ids) for v in verts}
   if sorted(degree.values()) not in ([1,1,2,2,2],[2,2,2,2]):continue
   reached={next(iter(verts))}
   for _ in range(4):
    reached|={v for e in ids if set(E[e])&reached for v in E[e]}
   if reached==verts:shapes.append(ids)
  self.shapes=shapes
 def proper(self,w):
  return all(len([w[e] for e in es if w[e]])==len(set(w[e] for e in es if w[e])) for es in self.inc)
 def paths(self,w):
  mask=tuple(i for i,c in enumerate(w) if c==0)
  if mask in self.cache:return self.cache[mask]
  rem=set(mask);paths=[]
  while rem:
   e=min(rem);part={e};vertices=set(self.E[e])
   for _ in range(4):
    part|={f for f in rem if set(self.E[f])&vertices};vertices|={v for f in part for v in self.E[f]}
   degrees={v:sum(v in self.E[f] for f in part) for v in vertices};ends=sorted(v for v in vertices if degrees[v]==1)
   if len(part)>3 or len(vertices)!=len(part)+1 or len(ends)!=2 or max(degrees.values())>2:
    self.cache[mask]=None;return None
   seq=[];v=ends[0]
   while len(seq)<len(part):
    f=next(f for f in part if v in self.E[f] and f not in seq);seq.append(f);v=next(x for x in self.E[f] if x!=v)
   paths.append(tuple(seq));rem-=part
  self.cache[mask]=tuple(sorted(paths,key=min));return self.cache[mask]
 def valid(self,w):
  if len(w)!=self.m or any(type(x)is not int or not 0<=x<=4 for x in w):return False
  if not self.proper(w) or self.paths(w) is None:return False
  return all(0 in (cs:={w[e] for e in es}) or len(cs)>2 for es in self.shapes)
 def cost(self,c,S=None):
  need(len(c)==self.m and all(type(x)is int and 1<=x<=6 for x in c) and self.proper(c),'full proper colors')
  return sum((S is None or bool(set(es)&S)) and len({c[e] for e in es})==2 for es in self.shapes)
 def pair_cost(self,c):
  need(self.proper(c),'pair proper')
  total=0
  for a,b in combinations(range(1,7),2):
   rem={e for e,x in enumerate(c) if x in (a,b)}
   while rem:
    part={rem.pop()};todo=list(part)
    while todo:
     e=todo.pop()
     for v in self.E[e]:
      for f in self.inc[v]:
       if f in rem:rem.remove(f);part.add(f);todo.append(f)
    verts={v for e in part for v in self.E[e]};m=len(part)
    if m<len(verts):total+=max(0,m-3)
    else:total+=1 if m==4 else (m if m>4 else 0)
  return total
 def colors(self,w):
  need(self.valid(w),'preframe premise');U=[i for i,c in enumerate(w) if c==0]
  for bs in product((5,6),repeat=len(U)):
   c=list(w)
   for e,a in zip(U,bs):c[e]=a
   if self.proper(c):yield c
 def phase(self,w,c):return sum((c[P[0]]-5)<<i for i,P in enumerate(self.paths(w)))
 def costs(self,w):
  a=[None]*(1<<len(self.paths(w)))
  for c in self.colors(w):
   s=self.phase(w,c);need(a[s] is None,'phase uniqueness');a[s]=self.cost(c)
   need(a[s]==self.pair_cost(c),'pair/shape total')
  need(None not in a,'all phases');return a
 def profile(self,w,S,ports):
  out=[None]*(1<<len(ports));att=[None]*len(out)
  for c in self.colors(w):
   b=sum((c[P[0]]-5)<<i for i,P in enumerate(ports));v=self.cost(c,S)
   if out[b] is None or v<out[b]:out[b]=v;att[b]=c
  need(None not in out,'profile coverage');return out,att
 def closed(self,w,S):return self.paths(w) is not None and all(not(set(P)&S) or set(P)<=S for P in self.paths(w))
 def connected(self,S):
  if not S:return False
  rem=set(S);seen={rem.pop()}
  while True:
   grow={f for f in rem if any(set(self.E[f])&set(self.E[e]) for e in seen)}
   if not grow:return not rem
   rem-=grow;seen|=grow
 def endpoints(self,w,S):
  ids=sorted(S)
  for a in product(range(5),repeat=len(ids)):
   q=list(w)
   for e,c in zip(ids,a):q[e]=c
   if self.valid(q) and self.closed(q,S):yield tuple(q)
 def witness(self,vs,c):
  need(len(vs) in (4,5) and len(set(vs))==len(vs),'simple witness vertices')
  pairs=[frozenset((vs[i],vs[(i+1)%len(vs)])) for i in range(4)]
  lookup={frozenset(e):i for i,e in enumerate(self.E)}
  need(all(e in lookup for e in pairs),'witness edges');es=[lookup[e] for e in pairs]
  need(tuple(sorted(es)) in self.shapes and len({c[e] for e in es})==2,'actual bad shape');return es
 def rows(self,w):
  info={e:(i,j%2) for i,P in enumerate(self.paths(w)) for j,e in enumerate(P)};out=[]
  for es in self.shapes:
   us=[e for e in es if not w[e]];ds=[e for e in es if w[e]]
   if len(us)!=2 or len(ds)!=2 or w[ds[0]]!=w[ds[1]]:continue
   if set(self.E[us[0]])&set(self.E[us[1]]):continue
   # Two disjoint edges of each palette alternate on the valid shape.
   if set(self.E[ds[0]])&set(self.E[ds[1]]):continue
   (i,p),(j,q)=[info[e] for e in us];out.append((i,j,1^p^q,es))
  return out

def validate_info(g,r):
 w=r['word'];need(g.valid(w),'record preframe');need([list(P) for P in g.paths(w)]==r['U_paths'],'path identity')
 cs=g.costs(w);need(cs==r['phase_costs'],'cost table');need(len(r['phases'])==len(cs),'phase record coverage')
 need({q['phase'] for q in r['phases']}==set(range(len(cs))),'phase keys')
 for q in r['phases']:
  c=q['colors'];need(all(c[e]==w[e] for e in range(g.m) if w[e]),'fixed colors')
  need(g.phase(w,c)==q['phase'] and g.cost(c)==q['cost']==cs[q['phase']],'phase identity')
  if q['cost']:g.witness(q['first_bad'],c)
  else:need(q['first_bad'] is None,'zero witness')

def validate_table(g,w,r):
 S=set(r['support']);need(g.connected(S) and g.closed(w,S),'support closure/connectivity')
 ps=[P for P in g.paths(w) if not set(P)&S];need([list(P) for P in ps]==r['outside_paths'],'boundary paths')
 actual=sorted(g.endpoints(w,S));stored=r['endpoints'];detail=bool(stored and isinstance(stored[0],dict));words=[tuple(q['word']) for q in stored] if detail else list(map(tuple,stored))
 need(actual==words and len(actual)==r['count'],'endpoint family coverage')
 vals=[];mus=[]
 for j,q in enumerate(actual):
  pp,_=g.profile(q,S,ps);cc=g.costs(q);vals.append(pp);mus.append(min(cc))
  if detail:
   need(stored[j]['profile']==pp and stored[j]['mu']==min(cc),'endpoint profile');validate_info(g,stored[j])
 need(r['envelope']==[min(x[i] for x in vals) for i in range(1<<len(ps))],'envelope')
 need(r['minimum_mu']==min(mus),'family minimum')
 if r['positive'] is not None:need(tuple(r['positive']) in actual and min(g.costs(r['positive']))==0,'family positive')
 return actual

def validate_transfer(g,w,q,r):
 S=set(r['S']);T=set(r['T']);need(S<=T and g.closed(w,S) and g.closed(q,S) and g.closed(w,T) and g.closed(q,T),'joint U closure')
 need(all(w[e]==q[e] for e in range(g.m) if e not in S),'fixed exterior')
 op=[P for P in g.paths(w) if not set(P)&S];ip=[P for P in op if set(P)&T];bp=[P for P in op if not set(P)&T]
 need(r['absorbed_paths']==list(map(list,ip)) and r['outside_paths']==list(map(list,bp)),'absorbed variable coverage')
 a,_=g.profile(w,S,op);a2,_=g.profile(q,S,op);A,_=g.profile(w,T,bp);A2,_=g.profile(q,T,bp)
 shapes=[es for es in g.shapes if set(es)&T and not set(es)&S]
 lookup={frozenset(e):i for i,e in enumerate(g.E)}
 actual_ids=[]
 for vs in r['new_shape_vertices']:
  need(len(vs) in (4,5) and len(set(vs))==len(vs),'new shape simple')
  ids=tuple(sorted(lookup[frozenset((vs[i],vs[(i+1)%len(vs)]))] for i in range(4)));need(ids in shapes,'new actual shape');actual_ids.append(ids)
 need(sorted(actual_ids)==sorted(shapes),'all new shapes')
 need(len(r['rows'])==1<<len(bp),'transfer boundary coverage')
 for rec in r['rows']:
  b=rec['boundary'];H=[];AA=[];BB=[]
  for z in range(1<<len(ip)):
   bits={P:b>>i&1 for i,P in enumerate(bp)}|{P:z>>i&1 for i,P in enumerate(ip)};j=sum(bits[P]<<i for i,P in enumerate(op))
   c=next(c for c in g.colors(w) if all(c[P[0]]==5+t for P,t in bits.items()))
   H.append(sum(len({c[e] for e in es})==2 for es in shapes));AA.append(a[j]);BB.append(a2[j])
  R=[x+y-A[b] for x,y in zip(AA,H)];G=[x-y for x,y in zip(AA,BB)]
  need(rec['h']==H and rec['r']==R and rec['g']==G and rec['old_profile_by_z']==AA and rec['new_profile_by_z']==BB,'h/r/g identities')
  need(min(x+y for x,y in zip(AA,H))==A[b] and min(x+y for x,y in zip(BB,H))==A2[b],'transfer minima')
  need(rec['max_g_minus_r']==max(x-y for x,y in zip(G,R))==A[b]-A2[b],'gain slack identity')

def literal_frames(g):
 for w in product(range(5),repeat=g.m):
  top=0;ok=True
  for a in w:
   if a>top+1:ok=False;break
   top=max(top,a)
  if ok and g.valid(w):yield w

def check_small(g,rec):
 states=list(literal_frames(g));need(len(states)==rec['frames'],'small full words');h=hashlib.sha256();cases=[];trials=0
 for w in states:
  cs=g.costs(w);trials+=len(cs);h.update((''.join(map(str,w))+':'+','.join(map(str,cs))+'\n').encode());mu=min(cs)
  if mu==0:continue
  ps=g.paths(w)
  # Producer orders by vertex witnesses. Sort each self witness by its canonical vertex sequence.
  self_shapes=[]
  for i,j,b,es in g.rows(w):
   if i!=j:continue
   vsset={v for e in es for v in g.E[e]};cycle=len(vsset)==4
   valid=[]
   for vs in permutations(sorted(vsset)):
    if cycle and (vs[0]!=min(vs) or vs[1]>vs[-1]):continue
    if not cycle and vs[0]>vs[-1]:continue
    pairs={frozenset((vs[k],vs[(k+1)%len(vs)])) for k in range(4)}
    if pairs=={frozenset(g.E[e]) for e in es}:valid.append(vs)
   need(len(valid)==1,'canonical shape');self_shapes.append((valid[0],i,es))
  for vs,i,es in sorted(self_shapes):
   S=set(es)|set(ps[i]);ports=[P for P in ps if not set(P)&S];old,_=g.profile(w,S,ports)
   eps=sorted(g.endpoints(w,S));pp=[g.profile(q,S,ports)[0] for q in eps]
   colors={g.phase(w,c):c for c in g.colors(w)}
   for s,cost in enumerate(cs):
    if cost!=mu:continue
    b=sum((colors[s][P[0]]-5)<<j for j,P in enumerate(ports));good=next((q for q,pr in zip(eps,pp) if pr[b]<old[b]),None)
    need(good is not None,'small repair exists');cases.append({'word':w,'support':sorted(S),'phase':s,'replacement':good})
 need(trials==rec['phase_trials'] and h.hexdigest()==rec['stream_sha256'],'small complete stream')
 need(len(cases)==rec['self_core_attaining_cases'],'small core occurrences')
 need(hashlib.sha256((json.dumps(cases,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()==rec['case_stream_sha256'],'small endpoint stream')
 return {'n':g.n,'frames':len(states),'phases':trials,'core_attainers':len(cases)}

def validate_chain_input(g,d,cert):
 w=d['old'];rows=g.rows(w);ps=g.paths(w);S=set(d['S']);T=set(d['T'])
 need(all(len(es)==3 for es in g.inc) and g.connected(set(range(g.m))),'connected cubic input')
 def shape_ids(vs):
  need(len(vs) in (4,5) and len(set(vs))==len(vs),'chain simple vertices')
  lookup={frozenset(e):i for i,e in enumerate(g.E)}
  ids=tuple(sorted(lookup[frozenset((vs[j],vs[(j+1)%len(vs)]))] for j in range(4)))
  need(ids in g.shapes,'chain actual shape');return ids
 stored=[]
 for r in cert['rows']:
  ids=shape_ids(r['vertices']);need(ids==tuple(sorted(r['edges'])),'stored row incidence')
  i,j,b=r['i'],r['j'],r['sign']
  need(any({a,c}=={i,j} and t==b and es==ids for a,c,t,es in rows),'stored row semantics')
  stored.append(ids)
 need(sorted(stored)==sorted(es for i,j,b,es in rows),'all actual rows')
 core=shape_ids(d['core_vertices']);self_rows=[r for r in rows if r[0]==r[1] and r[2]==1]
 need(len(self_rows)==1 and self_rows[0][3]==core,'unique minimum one-row core')
 variable=self_rows[0][0]
 need(S==set(core)|set(ps[variable]),'complete core hull')
 opt=[s for s,c in enumerate(g.costs(w)) if c==min(g.costs(w))]
 chains=[]
 for i,j,b,es in rows:
  if i==j or variable not in (i,j):continue
  need(all((((s>>i)^(s>>j))&1)==b for s in opt),'shortest chain satisfied at every attainer')
  hull=S|set(es)|set(ps[i])|set(ps[j]);chains.append((es,hull))
 need(len(chains)==2,'all shortest one-edge chains')
 chosen=shape_ids(d['selected_satisfied_chain_vertices']);other=shape_ids(d['alternative_chain_vertices'])
 need(chosen!=other and {chosen,other}=={es for es,H in chains},'chain coverage')
 need(next(H for es,H in chains if es==chosen)==T,'chosen absorption hull')
 need(len(T)==min(len(H) for es,H in chains),'minimum-hull tie-break')
 need(all(set(P)<=T for P in ps),'all old U components absorbed')
 need(sum(w[e]!=d['repair'][e] for e in range(g.m))==2 and set(e for e in range(g.m) if w[e]!=d['repair'][e])<=set(d['repair_support']),'joint two-edge repair')
 return {'shortest_core_rows':1,'shortest_core_incident_chains':len(chains),'selected_hull_edges':len(T),'alternative_hull_edges':max(len(H) for es,H in chains),'exterior_only_two_port_hypothesis':False}

def reject(name,fn,mut):
 try:fn()
 except (ValueError,TypeError,KeyError,IndexError,StopIteration):mut.append(name);return
 raise ValueError('mutation accepted: '+name)

def main():
 here=Path(__file__).parent;raw=(here/'opg37271-c27-input.json').read_bytes();d=json.loads(raw);blob=(here/'opg37271-c27-expanded.json').read_bytes();cert=json.loads(blob)
 need((here/'opg37271-c27-certificate-replay.json').read_bytes()==(here/'opg37271-c27-certificate.json').read_bytes(),'immutable compact certificate')
 need(cert['input_sha256']==hashlib.sha256(raw).hexdigest(),'fixed input hash');g=Direct(d['n'],d['edges']);w=d['old'];S=set(d['S']);T=set(d['T']);validate_info(g,cert['initial'])
 chain_report=validate_chain_input(g,d,cert)
 A=validate_table(g,w,cert['S_table']);B=validate_table(g,w,cert['T_table'])
 for rec in cert['expansions']:validate_table(g,w,rec)
 expected={tuple(sorted(T|{e})) for e in range(g.m) if e not in T and g.connected(T|{e})};need({tuple(r['support']) for r in cert['expansions']}==expected,'all connected one-edge enlargements')
 validate_table(g,w,cert['alternate_shortest_chain']);validate_info(g,cert['repair'])
 for rec in cert['fixed_endpoint_absorptions']:validate_transfer(g,w,rec['word'],rec['transfer'])
 need({tuple(r['word']) for r in cert['fixed_endpoint_absorptions']}==set(A),'all fixed endpoints')
 exhaustive=[]
 for mask in range(1<<g.m):
  R={e for e in range(g.m) if mask>>e&1}
  if S<=R and g.connected(R) and g.closed(w,R):exhaustive.append(tuple(sorted(R)))
 need([tuple(r['support']) for r in cert['phase_exhaustion_supports']]==exhaustive,'all absorptions')
 for row in cert['phase_exhaustion_supports']:
  R=set(row['support']);ports=[P for P in g.paths(w) if not set(P)&R];old,_=g.profile(w,R,ports)
  gain=max(max(x-y for x,y in zip(old,g.profile(q,R,ports)[0])) for q in A)
  need(gain==row['maximum_gain_over_S_endpoints']<=0,'absorption no gain')
 ctrl=d['c26_absorption_control'];validate_table(g,ctrl['old'],cert['c26_control']['S_table']);validate_table(g,ctrl['old'],cert['c26_control']['T_table']);validate_transfer(g,ctrl['old'],ctrl['new'],cert['c26_control']['transfer'])
 six=Direct(6,[(i,(i+1)%6) for i in range(6)]);cw=[1,0,1,0,1,0];cq=[2,0,1,0,1,0];validate_transfer(six,cw,cq,cert['nonzero_h_control'])
 small=[check_small(Direct(r['n'],r['edges']),q) for r,q in zip(d['small_graphs'],cert['small_coverage'])];need(len(small)==3,'small graph coverage')
 mut=[]
 q=deepcopy(d);q['selected_satisfied_chain_vertices']=q['alternative_chain_vertices'];reject('wrong_shortest_chain_hull',lambda:validate_chain_input(g,q,cert),mut)
 q=deepcopy(cert);q['rows'].pop();reject('missing_actual_chain_support',lambda:validate_chain_input(g,d,q),mut)
 for name,edit in [('missing_endpoint',lambda q:q['endpoints'].pop()),('wrong_minimum',lambda q:q.update(minimum_mu=0)),('wrong_envelope',lambda q:q['envelope'].__setitem__(0,0)),('missing_phase',lambda q:q['endpoints'][0]['phases'].pop()),('wrong_U_path',lambda q:q['endpoints'][0]['U_paths'][0].append(11)),('false_cost',lambda q:q['endpoints'][0]['phase_costs'].__setitem__(0,0))]:
  q=deepcopy(cert['T_table']);edit(q);reject(name,lambda:validate_table(g,w,q),mut)
 q=deepcopy(cert['T_table']['endpoints'][0]);q['phases'][0]['first_bad'][1]=q['phases'][0]['first_bad'][0];reject('repeated_vertex',lambda:validate_info(g,q),mut)
 q=w.copy();q[0]=5;reject('palette_crossing',lambda:need(g.valid(q),'palette'),mut)
 line=Direct(5,[(0,1),(1,2),(2,3),(3,4)]);reject('U_length_four',lambda:need(line.valid([0]*4),'U length'),mut)
 q=deepcopy(cert['nonzero_h_control']);q['rows'][0]['h']=[0,0];reject('omit_new_h',lambda:validate_transfer(six,cw,cq,q),mut)
 q=deepcopy(cert['nonzero_h_control']);q['new_shape_vertices']=[];reject('omit_new_shape',lambda:validate_transfer(six,cw,cq,q),mut)
 q=deepcopy(cert['c26_control']['transfer']);q['rows'][0]['r']=[0,0];reject('ignore_port_slack',lambda:validate_transfer(g,ctrl['old'],ctrl['new'],q),mut)
 q=deepcopy(cert['c26_control']['transfer']);q['rows'][0]['max_g_minus_r']=0;reject('only_old_minimizing_ports',lambda:validate_transfer(g,ctrl['old'],ctrl['new'],q),mut)
 reject('all_U_inside_implies_balanced',lambda:need(cert['T_table']['minimum_mu']==0,'complete U is not a solution'),mut)
 q=deepcopy(cert['S_table']);q['support'].remove(11);reject('omit_U_middle_edge',lambda:validate_table(g,w,q),mut)
 sq=Direct(4,[(0,1),(1,2),(2,3),(3,0)]);need(sq.cost([1,5,1,5])==1,'C4');mut.append('omit_C4_distinguished')
 costs=g.costs(w);no_self=[]
 for s in range(4):no_self.append(sum((((s>>i)^(s>>j))&1)!=b for i,j,b,_ in g.rows(w) if i!=j))
 need(min(no_self)==0 and min(costs)==1,'self deletion');mut.append('delete_self_row_distinguished')
 triples=list(dict.fromkeys((min(i,j),max(i,j),b) for i,j,b,_ in g.rows(w)));ded=[sum((((s>>i)^(s>>j))&1)!=b for i,j,b in triples) for s in range(4)]
 need(ded!=costs,'witness multiplicity');mut.append('deduplicate_support_distinguished')
 reject('pretend_legal_single_edit_05',lambda:need(g.valid([0]+w[1:]),'U branch'),mut)
 q=w.copy();q[7]=2;reject('pretend_legal_single_edit_25',lambda:need(g.valid(q),'D forbidden path'),mut)
 for perm in permutations(range(1,5)):
  ren=[0]+list(perm);v=[ren[c] for c in w];need(g.valid(v) and g.costs(v)==costs,'A rename')
 cut_tests=0
 atoms=[(i,i,1) for i in range(3)]+[(i,j,b) for i in range(3) for j in range(i+1,3) for b in range(2)]
 for mask in range(512):
  rs=[r for i,r in enumerate(atoms) if mask>>i&1];cs=[sum((((x>>i)^(x>>j))&1)!=b for i,j,b in rs) for x in range(8)]
  for x in range(8):
   margins=[]
   for Y in range(8):
    delta=sum((1 if (((x>>i)^(x>>j))&1)==b else -1) for i,j,b in rs if ((Y>>i)^(Y>>j))&1)
    need(delta==cs[x^Y]-cs[x],'signed cut');margins.append(delta)
   need((cs[x]==min(cs))==(min(margins)>=0),'cut iff optimum');cut_tests+=1
 report={'verdict':'candidate_only','best_verified_result':'none','certificate_sha256':hashlib.sha256(blob).hexdigest(),'S_endpoints':len(A),'T_endpoints':len(B),'all_absorption_supports':len(exhaustive),'small_coverage':small,'mutations':mut,'A_relabelings':24,'cut_phase_systems':cut_tests,'chain_validation':chain_report,'global_exchange':'open','limitations':'All finite replay is in the generator domain. Core-incident one-port chain fixture is not a two-distinct-port exterior-only chain and not a positive global-frame minimum.'}
 (here/'opg37271-c27-check-result.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
