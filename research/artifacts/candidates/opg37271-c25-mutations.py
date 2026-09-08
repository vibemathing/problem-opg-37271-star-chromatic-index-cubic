"""Corrupt actual graph-bound certificates; all intended faults must be rejected."""
from pathlib import Path
import importlib.util,json,hashlib,signal,resource
from copy import deepcopy
from itertools import permutations
HERE=Path(__file__).resolve().parent

def load(name):
 s=importlib.util.spec_from_file_location(name,HERE/f'opg37271-c25-{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 signal.alarm(35);resource.setrlimit(resource.RLIMIT_CPU,(30,31));resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,)*2)
 a=load('audit');cov=load('coverage');cert=json.loads((HERE/'opg37271-c25-witnesses.json').read_text());cat=json.loads((HERE/'opg37271-c25-graphs10.json').read_text());tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,AssertionError,KeyError,IndexError,TypeError) as exc:tests.append({'name':name,'test_result':'rejected','reason':str(exc)});return
  raise ValueError('mutation survived: '+name)
 for name,edit in [('missing_graph',lambda x:x['graphs'].pop()),('duplicate_graph',lambda x:x['graphs'].__setitem__(1,dict(x['graphs'][0],index=1))),('wrong_automorphism_count',lambda x:x['graphs'][0].__setitem__('automorphisms',1)),('wrong_connected_count',lambda x:x.__setitem__('connected_labelled_total',1))]:
  c=deepcopy(cat);edit(c);reject(name,lambda c=c:cov.check(c))
 g=a.Graph(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
 reject('duplicate_edge',lambda:a.Graph(4,[[0,1],[0,1]]))
 reject('loop_edge',lambda:a.Graph(4,[[0,0]]))
 reject('degree_four',lambda:a.Graph(5,[[0,1],[0,2],[0,3],[0,4]]))
 reject('D_palette_crossing',lambda:g.preframe([5,0,1,2,3,4]))
 line=a.Graph(5,[[0,1],[1,2],[2,3],[3,4]])
 reject('U_length_four',lambda:line.preframe([0,0,0,0]))
 reject('nonstar_D',lambda:line.preframe([1,2,1,2]))
 ring=a.Graph(4,[[0,1],[0,3],[1,2],[2,3]])
 reject('U_cycle',lambda:ring.preframe([0,0,0,0]))
 colors=[1,2,2,1];a.need(len(ring.forbidden(colors))==1,'C4 direct control');a.need(not [s for s in ring.shapes if s['kind']=='path'],'C4 no four-edge path');tests.append({'name':'omit_four_cycle','test_result':'distinguished','actual_forbidden':1,'paths_only':0})
 good=cert['global_positive_certificates'][18];pg=a.Graph(10,cat['graphs'][18]['edges'])
 c=good['colors'].copy();c[0]=7;reject('full_palette_seven',lambda:pg.pair_check(c))
 c=good['colors'].copy();c[1]=c[0];reject('incident_same_color',lambda:pg.pair_check(c))
 reject('out_of_range_phase',lambda:pg.decode(good['word'],32))
 patch=cert['topology_switch'];h=a.Graph(8,patch['edges']);old=patch['old']['word'];new=patch['new']['word']
 reject('omit_U_component_edge',lambda:a.patch_profiles(h,old,new,{1,4}))
 reject('hide_changed_outside_edge',lambda:a.patch_profiles(h,old,new,{1,10}))
 prof=a.patch_profiles(h,old,new,{1,4,10});damaged=deepcopy(prof);damaged['new_profile'][0]=1
 reject('false_strict_profile_claim',lambda:a.need(min(x-y for x,y in zip(damaged['old_profile'],damaged['new_profile']))>=1,'strict profile gap'))
 reject('drop_boundary_assignment',lambda:a.need(len(prof['new_profile'][:-1])==2**len(prof['boundary_paths']),'boundary coverage'))
 # Genuine graph-shape corruption, not accepting arbitrary walks.
 s=deepcopy(h.shapes[0]);s['vertices'][1]=s['vertices'][0]
 reject('non_simple_witness',lambda:a.need(len(set(s['vertices']))==len(s['vertices']),'distinct vertices'))
 # Global color quotient must preserve zero and lift every A relabeling.
 checked=0
 for p in permutations((1,2,3,4)):
  w=[0 if c==0 else p[c-1] for c in old]
  a.need(h.describe(w,False)['phase_costs']==patch['old']['phase_costs'],'color orbit costs');checked+=1
 tests.append({'name':'quotient_over_zero','test_result':'distinguished','correct_A_orbit_rechecks':checked,'zero_is_not_an_A_color':True})
 # The fork swap cannot be justified by an admissible single-entry interpolation.
 a.need(len(patch['invalid_single_intermediates'])==2,'both orders fail');tests.append({'name':'assume_valid_single_edge_interpolation','test_result':'distinguished','invalid_first_moves':patch['invalid_single_intermediates']})
 out={'verdict':'candidate_only','mutations':tests,'count':len(tests),'A_orbit_rechecks':checked,'input_sha256':hashlib.sha256((HERE/'opg37271-c25-witnesses.json').read_bytes()).hexdigest()}
 (HERE/'opg37271-c25-mutations.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'verdict':'candidate_only','count':len(tests),'A_orbit_rechecks':checked}))

if __name__=='__main__':main()
