"""Exact singleton-SCC certificate and mutation audit. Candidate-only.
Uses only this turn's alternate graph definition checker, not old modules.
"""
import importlib.util,json,hashlib
from copy import deepcopy
from itertools import permutations
from pathlib import Path
H=Path(__file__).parent
spec=importlib.util.spec_from_file_location('c24check',H/'opg37271-c24-check.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
W=[0,1,0,2,1,3,0,3,4,4,2,0]
E=[[0,1],[0,2],[0,3],[1,2],[1,4],[2,5],[3,4],[3,6],[4,7],[5,6],[5,7],[6,7]]

def rowset(g,w):
    t=g.topology(sum(1<<e for e,a in enumerate(w) if not a));rows=[]
    for a,b,mask,shape in t[4]:
        if w[a]!=w[b]:continue
        free=[e for e in shape['edges'] if not w[e]];i,p=t[1][free[0]];j,q=t[1][free[1]]
        rows.append(dict(**shape,i=i,j=j,rhs=1^p^q,fixed_edges=[a,b],free_edges=free))
    return rows

def explain(g,w):
    if any(a not in range(5) for a in w):return dict(valid=False,reason='A_palette')
    # Properness witnesses are local at a vertex.
    for ns in g.by:
        for i in ns:
            for j in ns:
                if i<j and w[i]!=0 and w[i]==w[j]:return dict(valid=False,reason='D_incidence',edges=[i,j])
    mask=sum(1<<i for i,a in enumerate(w) if not a);t=g.topology(mask)
    if t is None:return dict(valid=False,reason='U_not_short_paths',U=[i for i,a in enumerate(w) if not a])
    for shape in g.shapes:
        es=shape['edges']
        if all(w[e] for e in es) and len({w[e] for e in es})==2:return dict(valid=False,reason='D_bichromatic_shape',witness=shape)
    costs=g.costs(w);phases=[]
    for s,cost in enumerate(costs):
        full=g.decode(w,s);needcost=g.direct_cost(full);v.need(needcost==cost,'direct every phase')
        bad=[q for q in g.shapes if len({full[e] for e in q['edges']})==2]
        phases.append(dict(phase=s,colors=full,violations=bad))
    return dict(valid=True,U_paths=t[0],mu=min(costs),phase_costs=costs,phases=phases,rows=rowset(g,w))

def table(g,w):
    out=[]
    for e,old in enumerate(w):
        for a in range(5):
            if old!=a:
                q=w.copy();q[e]=a;out.append(dict(edit=[e,a],**explain(g,q)))
    return out

def validate(g,cert):
    w=cert['word'];v.need(g.valid(w),'frozen premise');cost=g.costs(w);v.need(cert['phase_costs']==cost and cert['mu']==min(cost),'frozen phase/mu')
    v.need(cert['n']==g.n and cert['edges']==[list(e) for e in g.E],'frozen graph identity')
    for key,value in explain(g,w).items():v.need(cert[key]==value,'initial witness/color field: '+key)
    wanted={(i,a) for i,old in enumerate(w) for a in range(5) if a!=old};rows=cert['neighbors']
    v.need(len(rows)==len(wanted) and {tuple(r['edit']) for r in rows}==wanted,'complete edit domain')
    for r in rows:
        q=w.copy();i,a=r['edit'];q[i]=a;truth=explain(g,q);v.need(r==dict(edit=[i,a],**truth),'neighbor classification and witness bytes')
        v.need(not truth['valid'] or truth['mu']>cert['mu'],'singleton is closed')
    v.need(cert['closed_members']==[w],'singleton membership')
    v.need(cert['expanded_phase_members']==list(range(len(cost))),'complete phase-reset SCC')

def mutations(g,cert):
    out=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError) as e:out.append(dict(name=name,outcome='rejected',diagnostic=str(e)));return
        raise ValueError('mutation survived: '+name)
    def difference(name,a,b):
        v.need(a!=b,'mutation indistinguishable '+name);out.append(dict(name=name,outcome='distinguished',correct=a,mutant=b))
    cyc=v.Model(4,[[0,1],[1,2],[2,3],[0,3]]);w=[1,0,1,0];full=cyc.decode(w,0)
    difference('omit_4cycle',cyc.direct_cost(full),sum(sh['kind']=='path' and len({full[e] for e in sh['edges']})==2 for sh in cyc.shapes))
    selfg=v.Model(5,[[0,1],[1,2],[2,3],[1,3],[2,4]]);sw=[0,0,0,1,1];full=selfg.decode(sw,0)
    induced=[]
    for sh in selfg.shapes:
        verts=set(sh['vertices']);extra=[e for e,p in enumerate(selfg.E) if set(p)<=verts and e not in sh['edges']]
        if not extra:induced.append(sh)
    difference('induced_paths_only',selfg.direct_cost(full),sum(len({full[e] for e in sh['edges']})==2 for sh in induced))
    def costs_rows(rs,k):return [sum(((s>>q['i']&1)^(s>>q['j']&1))!=q['rhs'] for q in rs) for s in range(1<<k)]
    rs=cert['rows'];difference('delete_self_equations',min(cert['phase_costs']),min(costs_rows([q for q in rs if q['i']!=q['j']],2)))
    prism=v.Model(6,[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]);pw=[0,0,1,0,2,0,3,3,4];rr=rowset(prism,pw);dd={}
    for q in rr:dd[tuple(sorted((q['i'],q['j'])))]=q
    difference('deduplicate_without_sign',min(prism.costs(pw)),min(costs_rows(list(dd.values()),2)))
    dd={}
    for q in rr:dd[(*sorted((q['i'],q['j'])),q['rhs'])]=q
    difference('deduplicate_actual_shape_multiplicity',prism.costs(pw),costs_rows(list(dd.values()),2))
    qq=deepcopy(rs);qq[0]['rhs']^=1;difference('flip_self_rhs',cert['phase_costs'],costs_rows(qq,2))
    reject('cross_palette',lambda:v.need(g.valid([5]+W[1:]),'A palette'))
    reject('U_length_four',lambda:v.need(v.Model(5,[[0,1],[1,2],[2,3],[3,4]]).valid([0]*4),'U length four'))
    reject('U_cycle',lambda:v.need(cyc.valid([0]*4),'U cycle'))
    x=deepcopy(cert);x['rows'][0]['vertices'][1]=x['rows'][0]['vertices'][0];reject('non_simple_witness',lambda:validate(g,x))
    x=deepcopy(cert);x['neighbors'].pop();reject('omit_one_edit',lambda:validate(g,x))
    x=deepcopy(cert);next(r for r in x['neighbors'] if r['valid'])['mu']=0;reject('invent_lower_exit',lambda:validate(g,x))
    x=deepcopy(cert);x['mu']=0;reject('false_zero_mu',lambda:validate(g,x))
    x=deepcopy(cert);x['phase_costs']=x['phase_costs'][:2];reject('omit_phase_assignments',lambda:validate(g,x))
    x=deepcopy(cert);x['expanded_phase_members'].pop();reject('omit_expanded_SCC_phase',lambda:validate(g,x))
    x=deepcopy(cert);x['closed_members'].append(cert['escape'][-1]['word']);reject('add_false_SCC_member',lambda:validate(g,x))
    reject('two_edits_as_one',lambda:v.need(sum(a!=b for a,b in zip(W,cert['escape'][-1]['word']))==1,'one coordinate per move'))
    difference('swap_zero_and_A_in_canonicalization',[i for i,a in enumerate(W) if not a],[i for i,a in enumerate([1 if a==0 else 0 if a==1 else a for a in W]) if not a])
    z=deepcopy(cert);r=next(q for q in z['neighbors'] if q['valid']);r['phases'][0]['colors'][0]=7;reject('corrupt_full_coloring',lambda:validate(g,z))
    # Missing a state must fail complete-set comparison, not just tally checks.
    k4=v.Model(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]);st,_=k4.all_states();damaged=dict(st);damaged.pop(next(iter(damaged)))
    reject('omit_entire_preframe',lambda:v.need(damaged==st,'full state coverage'))
    # A wrong raw/quotient orbit convention cannot identify a frozen singleton.
    expected=[]
    for p in permutations(range(1,5)):
        w=[0 if a==0 else p[a-1] for a in W];v.need(v.norm(w)==tuple(W),'color orbit normalization');v.need(g.costs(w)==cert['phase_costs'],'orbit phase costs')
        v.need(all(not g.valid(q:=w[:i]+[a]+w[i+1:]) or min(g.costs(q))>1 for i,old in enumerate(w) for a in range(5) if a!=old),'raw orbit closure');expected.append(w)
    v.need(len({tuple(w) for w in expected})==24,'full orbit24')
    return out

if __name__=='__main__':
    g=v.Model(8,E);d=explain(g,W);cert=dict(verdict='candidate_only',n=8,edges=E,word=W,closed_members=[W],expanded_phase_members=list(range(len(d['phase_costs']))),neighbors=table(g,W),**d)
    v.need(d['phase_costs']==[2,1,1,2],'frozen costs')
    escape=[W,[0,1,0,2,1,0,0,3,4,4,2,0],[0,1,4,2,1,0,0,3,4,4,2,0]]
    cert['escape']=[dict(word=w,phase_costs=g.costs(w),mu=min(g.costs(w))) for w in escape]
    v.need([r['mu'] for r in cert['escape']]==[1,2,0],'exact barrier escape');cert['escape_coloring']=g.decode(escape[-1],g.costs(escape[-1]).index(0))
    globalw=[0,1,2,2,3,0,0,3,1,1,2,0];cert['global_matching_frame']=dict(word=globalw,**explain(g,globalw))
    v.need(min(g.costs(globalw))==0 and all(len(p)==1 for p in g.topology(sum(1<<i for i,a in enumerate(globalw) if not a))[0]),'global matching alternative')
    validate(g,cert);mut=mutations(g,cert);cert['mutations']=mut
    p=H/'opg37271-c24-certificate.json';p.write_text(json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(verdict='candidate_only',mutations=len(mut),raw_orbit_rechecks=24,edits=48,legal=sum(r['valid'] for r in cert['neighbors']),mu=d['mu'],certificate_bytes=p.stat().st_size,certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),sort_keys=True))
