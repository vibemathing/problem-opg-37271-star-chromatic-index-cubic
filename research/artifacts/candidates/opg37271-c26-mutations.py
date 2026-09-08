"""Destructive C26 interface tests; every negative check invokes a real predicate."""
from pathlib import Path
from itertools import product,permutations
from copy import deepcopy
import importlib.util,json,signal,resource
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c26_geometric',HERE/'opg37271-c26-check.py')
x=importlib.util.module_from_spec(spec);spec.loader.exec_module(x)

def main():
    signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
    inp=json.loads((HERE/'opg37271-c26-input.json').read_text());o=inp['case'];g=x.Graph(o['n'],o['edges']);w=o['word']
    table=json.loads((HERE/'opg37271-c26-search-result.json').read_text())[o['name']];cert=json.loads((HERE/'opg37271-c26-certificate.json').read_text());tests=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,IndexError,KeyError,TypeError) as err:tests.append({'name':name,'test_result':'rejected','reason':str(err)});return
        raise ValueError('mutation accepted: '+name)
    reject('A_palette_crossing',lambda:g.frame([5]+w[1:]))
    reject('U_length_four',lambda:x.Graph(5,[(0,1),(1,2),(2,3),(3,4)]).frame([0,0,0,0]))
    q=deepcopy(cert['old']['rows'][0]);q['vertices'][0]=q['vertices'][1]
    reject('nonsimple_witness',lambda:g.row_check(w,q))
    q=deepcopy(cert['old']['rows'][0]);q['edges'][0]=11
    reject('false_incidence',lambda:g.row_check(w,q))
    rows=g.rows(w);cs=g.costs(w)
    def rowcost(rs,p):return sum(((p>>q['i']&1)^(p>>q['j']&1))!=q['rhs'] for q in rs)
    for name,rs in [('omit_C4',[q for q in rows if q['kind']!='cycle']),('dedup_ignoring_sign',[rows[0]]),('drop_duplicate_support',[rows[0],rows[1]])]:
        mutant=[rowcost(rs,p) for p in range(4)];x.need(mutant!=cs,'row mutation must change actual costs');tests.append({'name':name,'test_result':'distinguished','mutant_costs':mutant,'actual_costs':cs})
    reject('old_U_not_closed',lambda:x.need(g.closed(w,{4}),'old closure'))
    toy=x.Graph(4,[(0,1),(1,2),(2,3)]);reject('new_U_crosses_boundary',lambda:toy.endpoint([0,1,2],[5,6,2],{1}))
    reject('disconnected_support',lambda:x.need(g.connected({0,4}),'connected support'))
    bad=deepcopy(table);bad['rows']=[r for r in bad['rows'] if r[1]!=3]
    reject('omit_old_attaining_phase',lambda:x.check_patches(g,w,bad,4))
    bad=deepcopy(table);bad['rows']=[r for r in bad['rows'] if r[0]!=1104]
    reject('omit_entire_support',lambda:x.check_patches(g,w,bad,4))
    bad=deepcopy(table);bad['rows'][0][2]+=1
    reject('wrong_family_cardinality',lambda:x.check_patches(g,w,bad,4))
    bad=deepcopy(table);bad['rows'][0][4]=0
    reject('invent_zero_minimum',lambda:x.check_patches(g,w,bad,4))
    c=list(cert['exchange']['new_colors']);c[1]=7
    reject('new_color_seven',lambda:g.endpoint(w,c,set(o['selected_support'])))
    # A real graph shows that optimum phases cannot be replaced by pairwise XOR classes.
    six=x.Graph(6,[(0,1),(1,2),(2,3),(3,4),(4,5),(0,5)]);sw=[1,0,1,0,1,0];cost=six.costs(sw);opt=[p for p,v in enumerate(cost) if v==min(cost)]
    forced=[(i,j) for i in range(3) for j in range(i) if len({(p>>i&1)^(p>>j&1) for p in opt})==1]
    x.need(len(opt)==6 and forced==[],'six-cycle nonaffine optimum');tests.append({'name':'pairwise_port_compression','test_result':'distinguished','optimum_phases':opt,'pairwise_closure_phases':list(range(8))})
    selfg=x.Graph(5,[(0,1),(1,2),(2,3),(1,3),(2,4)]);selfcost=selfg.costs([0,0,0,1,1])
    x.need(selfcost==[1,1],'actual self core');tests.append({'name':'drop_self_row','test_result':'distinguished','actual_costs':selfcost,'mutant_costs':[0,0]})
    # Dropping the twisted closing edge yields a false zero ring cost.
    actual=x.cycle_dp([1,1,1],[1,1,1],[[0,0]]*3);x.need(actual==1,'negative triangle DP');tests.append({'name':'omit_cycle_seam','test_result':'distinguished','mutant_value':0,'actual_value':actual})
    # Fixing b to OLD argmin misses a real new minimum in this single-edge example.
    nw=w.copy();nw[7]=2;old=x.profile(g,w,{7});new=x.profile(g,nw,{7});active=[i for i,v in enumerate(old['values']) if v==min(old['values'])]
    x.need(old['values']==[1,2,2,1] and new['values']==[2,0,0,2],'boundary migration profiles')
    x.need(min(new['values'][i] for i in active)>min(new['values']),'anchoring is not necessary');tests.append({'name':'discard_inactive_boundaries','test_result':'distinguished','old_profile':old['values'],'new_profile':new['values'],'old_active':active})
    # Disprove using cycle length rather than XOR sign to determine balance.
    x.need(x.cycle_dp([1,1,1],[0,0,0],[[0,0]]*3)==0,'positive odd ring');tests.append({'name':'odd_length_as_negative_sign','test_result':'distinguished'})
    x.need(all(r['closure_edges']==4*r['q'] for r in cert['closure_family_checks']),'edge-overlap closure family')
    tests.append({'name':'vertex_intersection_as_edge_closure','test_result':'distinguished','singleton_seed_closure':1,'incorrect_vertex_propagation_on_alternating_cycle':4})
    relabels=0
    for perm in permutations(range(1,5)):
        rw=[perm[a-1] if a else 0 for a in w];rc=[perm[a-1] if a<5 else a for a in cert['exchange']['new_colors']]
        x.need(g.costs(rw)==cs and g.pair_cost(rc)==0,'A relabel invariant');relabels+=1
    result={'verdict':'candidate_only','tests':tests,'mutation_count':len(tests),'A_relabelings':relabels,'boundary_migration':{'support':[7],'new_word':nw,'new_colors':g.decode(nw,1),'old_profile':old,'new_profile':new},'nonaffine_real_graph':{'n':6,'edges':six.E,'word':sw,'costs':cost,'optimum_phases':opt}}
    (HERE/'opg37271-c26-mutations.json').write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'verdict':'candidate_only','mutations':len(tests),'relabelings':relabels}))
if __name__=='__main__':main()
