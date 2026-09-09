"""Negative controls for the frozen C30 addendum. No producer imports."""
from pathlib import Path
import importlib.util,json,copy
ROOT=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('local_candidate_checker',ROOT/'opg37271-c30x-check.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
data=json.loads((ROOT/'opg37271-c30x-certificate.json').read_bytes());tests=[]
def reject(name,f):
 try:f()
 except (AssertionError,KeyError,IndexError,ValueError,TypeError):tests.append({'name':name,'outcome':'rejected'});return
 raise AssertionError('mutation survived: '+name)
def expected_false(name,predicate):
 assert not predicate();tests.append({'name':name,'outcome':'distinguished'})
hard=next((sk,e) for sk in data['skeletons'] for e in sk['completions'] if e['width']==3)
sk,entry=hard
E,w=m.passive_words(sk,10)[tuple(map(tuple,entry['added_D_edges']))]
m.verify_completion(E,w,entry)
def mutated(name,edit,fixture=None):
 ee,ww,rr=fixture or (E,w,entry)
 q=copy.deepcopy(rr);edit(q);reject(name,lambda:m.verify_completion(ee,ww,q))
def find_fixture(field):
 for block in data['skeletons']:
  for rr in block['completions']:
   if any(t[field] for t in rr['profiles']['terms']):
    pairs=sorted(list(zip(map(tuple,block['edges']),block['word']))+[((a,b),c) for a,b,c in rr['added_D_edges']])
    return [e for e,c in pairs],[c for e,c in pairs],rr
 raise AssertionError('missing positive control')
mutated('drop_actual_self_witness',lambda q:q['profiles']['old_rows'].pop(next(i for i,r in enumerate(q['profiles']['old_rows']) if r[1]==r[2])))
mutated('deduplicate_parallel_equations',lambda q:q['profiles'].__setitem__('old_rows',list({tuple(r[1:]):r for r in q['profiles']['old_rows']}.values())))
mutated('wrong_XOR_sign',lambda q:q['profiles']['old_rows'][0].__setitem__(3,1-q['profiles']['old_rows'][0][3]))
mutated('nonsimple_four_edge_certificate',lambda q:q['profiles']['old_rows'][0][0].__setitem__(1,q['profiles']['old_rows'][0][0][0]))
mutated('omit_newly_touched_h',lambda q:next(z for z in q['profiles']['terms'] if z['h']).__setitem__('h',0),find_fixture('h'))
mutated('discard_positive_regret',lambda q:next(z for z in q['profiles']['terms'] if z['r']).__setitem__('r',0),find_fixture('r'))
mutated('wrong_gain',lambda q:q['profiles']['terms'][0].__setitem__('g',999))
mutated('wrong_sigma',lambda q:q['profiles']['terms'][0].__setitem__('old',999))
mutated('swap_old_phase_attainer',lambda q:q['old_bits'].__setitem__(0,1-q['old_bits'][0]))
mutated('color_outside_palette',lambda q:q['colors'].__setitem__(q['support'][0],7))
mutated('support_size_is_changed_entry_count',lambda q:q.__setitem__('width',1))
mutated('partial_old_U_closure',lambda q:q.__setitem__('support',[next(i for P in q['profiles']['old_U_paths'] if len(P)==3 for i in P)]))
mutated('wrong_absorbed_U_boundary',lambda q:q['profiles'].__setitem__('retained_outside_indices',[]))
mutated('omit_all_four_edge_shape_range',lambda q:q['profiles'].__setitem__('all_shape_edge_sets_sha256','0'*64))
# Coverage controls do not relaunch a broad census: freeze the already reconstructed domains.
assert len(data['cases'])==24
q=data['cases'][:-1];reject('missing_gauge_case',lambda:m.coverage_case_domain(q,10))
q=copy.deepcopy(sk);q['completions'].pop()
reject('missing_passive_completion',lambda:m.completion_domain(q,10))
# Semantic fixtures are checked directly rather than by equation-array agreement.
C4=[(0,1),(1,2),(2,3),(0,3)];sh=m.walk_shapes(C4)
assert len(sh)==1 and next(iter(sh.values()))[0]=='cycle'
expected_false('omit_four_cycle',lambda:m.literal_valid(C4,[1,5,1,5],set(range(4)),sh))
expected_false('U_component_length_four',lambda:m.partial_paths([(0,1),(1,2),(2,3),(3,4)],[0]*4) is not None)
expected_false('U_component_degree_three',lambda:m.partial_paths([(0,1),(0,2),(0,3)],[0]*3) is not None)
expected_false('duplicate_graph_edge',lambda:m.partial_paths([(0,1),(0,1)],[1,2]) is not None)
expected_false('properness_failure',lambda:m.literal_valid([(0,1),(1,2)],[1,1],{0,1},{}))
assert m.partial_paths([],[])==[];tests.append({'name':'empty_U_and_empty_graph','outcome':'accepted_boundary'})
# Every geometric self witness is non-induced if its missing middle U edge is a chord.
selfrow=next(r for r in entry['profiles']['old_rows'] if r[1]==r[2]);witness_edges={tuple(E[i]) for i in selfrow[0]};verts={v for e in witness_edges for v in e}
assert any(set(e)<=verts and e not in witness_edges for e in E)
tests.append({'name':'retain_noninduced_self_path','outcome':'accepted_boundary'})
result={'verdict':'candidate_only','best_verified_result':'none','tests':tests,'count':len(tests)}
(ROOT/'opg37271-c30x-mutations.json').write_bytes(m.enc(result));print(json.dumps({'count':len(tests),'verdict':'candidate_only'}))
