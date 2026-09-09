"""Actual negative tests for the order-eleven certificate interface; candidate_only."""
from pathlib import Path
from itertools import combinations
import copy, hashlib, importlib.util, json
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c30y',BASE/'opg37271-c30y-enumerate.py')
y=importlib.util.module_from_spec(spec);spec.loader.exec_module(y)
m=y.load('opg37271-c30x-check')
cat=json.loads((BASE/'opg37271-c30y-catalog.json').read_text());skels={s['key']:s for s in cat['skeletons']}
fixtures=[]
for f in sorted(BASE.glob('opg37271-c30y-batch-*.json')):
 for rec in json.loads(f.read_text())['skeletons']:
  for r in rec['completions']:
   if r['width']==3:
    sk=skels[rec['key']];ew=sorted(list(zip(map(tuple,sk['edges']),sk['word']))+[((a,b),c) for a,b,c in r['added_D_edges']])
    E=[e for e,c in ew];w=[c for e,c in ew];r=copy.deepcopy(r);ps=m.partial_paths(E,w);np=m.partial_paths(E,[c if c<5 else 0 for c in r['colors']]);sh=m.walk_shapes(E)
    y.profile(E,w,r,m,sh,ps,np);fixtures.append((E,w,r,ps,np,sh))
assert len(fixtures)==6
E,w,R,ps,np,sh=fixtures[0]
assert m.verify_completion(E,w,R)
passed=[]
def reject(name,fun):
 try:fun()
 except (AssertionError,ValueError):passed.append(name);return
 raise AssertionError('mutation escaped: '+name)
def changed(name,edit):
 r=copy.deepcopy(R);edit(r)
 reject(name,lambda:m.verify_completion(E,w,r))
changed('color_outside_1_to_6',lambda r:r['colors'].__setitem__(0,7))
changed('old_phase_not_an_attainer',lambda r:r['old_bits'].__setitem__(0,1-r['old_bits'][0]))
changed('empty_support',lambda r:r.__setitem__('support',[]))
changed('incorrect_support_cardinality',lambda r:r.__setitem__('width',2))
changed('omitted_self_row',lambda r:r['profiles'].__setitem__('old_rows',[z for z in r['profiles']['old_rows'] if z[1]!=z[2]]))
changed('wrong_XOR_sign',lambda r:r['profiles']['old_rows'][0].__setitem__(3,1-r['profiles']['old_rows'][0][3]))
changed('nonsimple_recorded_shape',lambda r:r['profiles']['old_rows'][0][0].__setitem__(1,r['profiles']['old_rows'][0][0][0]))
changed('wrong_all_shape_digest',lambda r:r['profiles'].__setitem__('all_shape_edge_sets_sha256','0'*64))
changed('wrong_new_U_components',lambda r:r['profiles'].__setitem__('new_U_paths',[]))
changed('incorrect_sigma',lambda r:r['profiles']['terms'][0].__setitem__('old',r['profiles']['terms'][0]['old']+1))
changed('incorrect_newly_touched_h',lambda r:r['profiles']['terms'][0].__setitem__('h',r['profiles']['terms'][0]['h']+1))
changed('incorrect_regret_r',lambda r:r['profiles']['terms'][0].__setitem__('r',r['profiles']['terms'][0]['r']+1))
changed('incorrect_gain_g',lambda r:r['profiles']['terms'][0].__setitem__('g',r['profiles']['terms'][0]['g']+1))
changed('omitted_boundary_assignment',lambda r:r['profiles']['terms'].pop())
changed('duplicate_geometric_rows_collapsed',lambda r:r['profiles'].__setitem__('old_rows',list({(z[1],z[2],z[3]):z for z in r['profiles']['old_rows']}.values())))
old=next(c for bits,c in m.full_phases(E,w,ps) if list(bits)==R['old_bits'])
outside=next(i for i in range(len(E)) if i not in R['support'])
changed('outside_color_altered',lambda r:r['colors'].__setitem__(outside,1+old[outside]%6))
# Structural predicates are exercised on literal invalid inputs, not merely compared hashes.
assert m.partial_paths(E+[E[0]],w+[w[0]]) is None;passed.append('duplicate_graph_edge')
assert m.partial_paths([(0,1),(1,2),(2,3),(3,4)],[0]*4) is None;passed.append('U_length_four')
assert m.partial_paths([(0,1),(0,2),(0,3)],[0]*3) is None;passed.append('U_degree_three')
assert m.partial_paths([(0,1),(0,2),(0,3),(0,4)],[1,2,3,4]) is None;passed.append('graph_degree_four')
assert m.partial_paths([(0,1),(1,2)],[5,1]) is None;passed.append('A_B_palette_crossing')
# Negative controls for cyclic versus ordinary-path geometry.
C=[(0,1),(1,2),(2,3),(0,3)];sc=m.walk_shapes(C)
assert (0,1,2,3) in sc and sc[(0,1,2,3)][0]=='cycle';passed.append('C4_not_omitted')
P=[(0,1),(1,2),(2,3),(3,4),(1,3)];sp=m.walk_shapes(P)
assert (0,1,2,3) in sp;passed.append('noninduced_path_retained')
# Closure is a support condition, not changed-entry count.
part=next(set(P) for P in ps if len(P)>1)
badS={min(part)}
r=copy.deepcopy(R);r['support']=sorted(badS);r['width']=1
reject('partial_U_support_rejected',lambda:m.verify_completion(E,w,r))
result={'verdict':'candidate_only','best_verified_result':'none','tests':passed,'tests_count':len(passed),'positive_width_three_fixtures':len(fixtures),'fixture_sha256':hashlib.sha256(y.enc([E,w,R])).hexdigest(),'trusted_execution':False}
(BASE/'opg37271-c30y-mutation-result.json').write_bytes(y.enc(result))
print(json.dumps(result))
