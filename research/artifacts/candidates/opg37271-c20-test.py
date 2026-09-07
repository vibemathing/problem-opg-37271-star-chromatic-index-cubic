"""Bounded new C20 replay and mutation tests; no old C19 implementation imports."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import resource
import signal

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('c20', HERE / 'opg37271-c20-core.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
LIMIT = 262144
INPUT = '9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3'


def compare(n, edges, colors):
    paths, rows = c.compile_rows(n, edges, colors)
    good = []
    for phase in itertools.product((0, 1), repeat=len(paths)):
        full = c.decode(colors, paths, phase)
        a, b = c.direct_star(n, edges, full), c.satisfies(rows, phase)
        c.need(a == b, 'graph/row discrepancy')
        if a:
            good.append(list(phase))
    solution, core = c.forest_solution_or_core(len(paths), rows)
    minimum = c.shortest_core(len(paths), rows)
    c.need((solution is not None) == bool(good), 'forest solver disagreement')
    out = dict(n=n, edges=edges, partial_colors=colors, paths=paths, rows=rows,
               phase_trials=2**len(paths), good_phases=good, forest_core=core,
               shortest_core=minimum)
    if minimum is not None:
        out['deletion_assignments'] = c.validate_core(len(paths), rows, minimum)
        c.validate_core(len(paths), rows, core)
        for row in rows:
            c.check_witness(n, edges, colors, paths, row)
        used_variables = sorted({v for t in minimum for v in (rows[t]['i'], rows[t]['j'])})
        support = sorted({e for t in minimum for e in rows[t]['edges']} |
                         {e for i in used_variables for e in paths[i]})
        out['support_edge_indices'] = support
        c.need(len(support) <= 7 * len(minimum), 'core support bound')
        out['mapped_core_witnesses'] = [rows[t] for t in minimum]
    return out


def rejection(name, action):
    try:
        action()
    except (ValueError, IndexError, KeyError, TypeError) as error:
        return dict(name=name, result='rejected', reason=str(error))
    raise ValueError('mutation accepted: ' + name)


def mutant_disagreement(name, result, altered):
    n, edges, colors, paths = (result[t] for t in ('n', 'edges', 'partial_colors', 'paths'))
    for phase in itertools.product((0, 1), repeat=len(paths)):
        full = c.decode(colors, paths, phase)
        direct, wrong = c.direct_star(n, edges, full), c.satisfies(altered, phase)
        if direct != wrong:
            return dict(name=name, result='distinguished', phase=list(phase), full_colors=full,
                        true_star=direct, mutated_rows_accept=wrong)
    raise ValueError('compiler mutation undetected: ' + name)


def shared_arc_audit():
    # Two conflicting root-to-vertex walks share row0 and row1; only their
    # symmetric difference and the closing edge give the three-row core.
    triples = [(0,1,1), (1,2,0), (2,3,0), (2,4,0), (3,4,1)]
    rows = [dict(i=i, j=j, rhs=b) for i,j,b in triples]
    val, core = c.forest_solution_or_core(5, rows)
    c.need(val is None and set(core) == {2,3,4}, 'shared-prefix cancellation')
    good = c.validate_core(5, rows, core)
    bad = rejection('shared_root_arcs_union_instead_of_cancellation', lambda: c.validate_core(5, rows, [0,1,2,3,4]))
    return dict(rows=rows, core=core, deletions=good), bad


def signed_exhaustion():
    atoms = [dict(i=i,j=i,rhs=1) for i in range(3)] + [dict(i=i,j=j,rhs=b) for i,j in itertools.combinations(range(3),2) for b in (0,1)]
    cases = sat = unsat = 0
    min_histogram = {}
    for mask in range(1 << len(atoms)):
        rows = [q for t,q in enumerate(atoms) if mask >> t & 1]
        phase, core = c.forest_solution_or_core(3, rows)
        minimum = c.shortest_core(3, rows)
        oracle = c.brute_minimum(3, rows)
        c.need((None if minimum is None else len(minimum)) == oracle, 'shortest versus brute subset')
        if phase is None:
            c.validate_core(3, rows, core)
            c.validate_core(3, rows, minimum)
            unsat += 1
            min_histogram[str(oracle)] = min_histogram.get(str(oracle),0) + 1
        else:
            c.need(minimum is None and c.satisfies(rows, phase), 'positive signed system')
            sat += 1
        cases += 1
    extra = []
    # Sign, not the NUMBER of edges, controls obstruction.
    for triples in [[(0,1,0),(1,2,0),(2,0,0)],[(0,1,0),(1,2,0),(2,3,0),(3,0,1)],[(0,0,0)]]:
        rows = [dict(i=i,j=j,rhs=b) for i,j,b in triples]
        k = 1+max(max(i,j) for i,j,_ in triples)
        m = c.shortest_core(k,rows)
        c.need((None if m is None else len(m)) == c.brute_minimum(k,rows), 'sign boundary')
        extra.append(dict(rows=rows, shortest_core=m))
    return dict(cases=cases, satisfiable=sat, unsatisfiable=unsat, minimum_histogram=min_histogram, sign_boundaries=extra)


def outer_positive_controls():
    # Positive frame with all four A colors, coherent contact parity and a
    # bipartite interaction graph; tested separately from spare-color theorem.
    edges = [[0,4],[1,5],[2,7],[3,6],[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4]]
    colors = [1,2,3,4,0,1,0,2,0,1,0,2]
    paths, rows = c.compile_rows(8,edges,colors)
    info = {e:(i,t%2) for i,seq in enumerate(paths) for t,e in enumerate(seq)}
    contacts = [set() for _ in paths]
    for row in rows:
        c.need(row['i'] != row['j'], 'outer no self contact')
        for e in row['free_edges']:
            i,p = info[e]; contacts[i].add(p)
    c.need(all(len(ps)<=1 for ps in contacts),'contact parity coherence')
    bip, bad = c.forest_solution_or_core(len(paths),[dict(i=q['i'],j=q['j'],rhs=1) for q in rows])
    c.need(bip is not None and not bad,'interaction bipartite')
    t = [next(iter(ps)) if ps else 0 for ps in contacts]
    phase = [a^b for a,b in zip(bip,t)]
    c.need(c.direct_star(8,edges,c.decode(colors,paths,phase)), 'contact condition coloring')
    # Nonempty U components of length2/3 need not satisfy this extra condition;
    # no universal outer-frame claim follows.
    return dict(contact_parities=t,bipartition=bip,phase=phase,full_colors=c.decode(colors,paths,phase))


def matching_four_cycle_obstruction(positive):
    """The least order for a four-cycle with four distinct matching labels is 8."""
    es=positive['edges']
    records=[]
    for a,b in itertools.product((2,3),(2,4)):
        col=[1,2,3,4,0,0,0,a,0,0,0,b]
        r=compare(8,es,col)
        c.need(len(r['paths'])==2 and all(len(p)==3 for p in r['paths']), 'two three-edge remainders')
        c.need(r['shortest_core'] is not None and len(r['shortest_core'])==1, 'singleton-special self core')
        q=r['mapped_core_witnesses'][0]
        c.need(q['i']==q['j'] and q['rhs']==1, 'real self equation')
        records.append(dict(partial_colors=col,paths=r['paths'],core_witness=q))
    return dict(n=8,edges=es,matching_edges=[0,1,2,3],special_edges=[7,11],cases=records,
                restored_positive_colors=positive['full_colors'],
                minimality_scope='Minimum order among perfect-matching frames containing a complement four-cycle with four distinct matching colors.')


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35)
    resource.setrlimit(resource.RLIMIT_CPU,(30,31))
    resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE,(LIMIT,)*2)
    raw=(HERE/'opg37271-c19-phase-certificate.json').read_bytes()
    c.need(len(raw)<=LIMIT and hashlib.sha256(raw).hexdigest()==INPUT,'frozen source input')
    d=json.loads(raw)
    results={}
    for name in ('negative_six_cycle_frame','positive_k4_frame'):
        obj=d[name];n,edges,colors=obj['n'],obj['edges'],obj['partial_colors']
        out=compare(n,edges,colors)
        c.need(out['paths']==obj['uncolored_paths'],'old component list')
        for row in obj['equations']:
            c.check_witness(n,edges,colors,out['paths'],row)
        c.need({c.row_triple(q) for q in out['rows']}=={c.row_triple(q) for q in obj['equations']},'regenerated complete algebraic rows')
        if name.startswith('positive'):
            c.need(obj['full_colors']==c.decode(colors,out['paths'],obj['phase']),'stored coloring binding')
        results[name]=out
    c.need(results['negative_six_cycle_frame']['good_phases']==[], 'negative phases')
    c.need(results['positive_k4_frame']['good_phases']==[[0,1,1,0],[1,0,0,1]],'positive phases')
    fixtures={
        'cycle4':(4,[[0,1],[1,2],[2,3],[3,0]],[1,0,1,0]),
        'self':(5,[[0,1],[1,2],[2,3],[1,3],[2,4]],[0,0,0,1,1]),
        'parallel':(5,[[0,1],[1,2],[3,4],[0,3],[2,4]],[0,0,0,1,1]),
        'unequal':(5,[[0,1],[1,2],[2,3],[3,4]],[1,0,2,0]),
        'empty_U':(4,[[0,1],[1,2],[2,3],[3,0]],[1,2,3,4]),
        'empty_graph':(0,[],[]),
        'path3':(4,[[0,1],[1,2],[2,3]],[0,0,0])}
    fixture_results={name:compare(*args) for name,args in fixtures.items()}
    mutations=[]
    for name,fixture,keep in [('omit_4cycle','cycle4',lambda q:q['kind']!='cycle'),('delete_self_row','self',lambda q:q['i']!=q['j'])]:
        r=fixture_results[fixture];mutations.append(mutant_disagreement(name,r,[q for q in r['rows'] if keep(q)]))
    r=fixture_results['parallel'];wrong={}
    for q in r['rows']:wrong.setdefault(c.row_triple(q)[:2],q)
    mutations.append(mutant_disagreement('dedup_without_sign',r,list(wrong.values())))
    r=fixture_results['self'];mutations.append(mutant_disagreement('induced_paths_only',r,[]))
    r=fixture_results['cycle4'];wrong=[dict(q,rhs=0) for q in r['rows']]
    mutations.append(mutant_disagreement('xor_constant_removed',r,wrong))
    neg=d['negative_six_cycle_frame'];paths=results['negative_six_cycle_frame']['paths']
    badrow=dict(neg['equations'][0]);badrow['vertices']=[0,1,2,1,4]
    mutations.append(rejection('path_vertex_repetition',lambda:c.check_witness(6,neg['edges'],neg['partial_colors'],paths,badrow)))
    for name,n,e,col in [('palette_crossing',2,[[0,1]],[5]),('U_component_length4',5,[[0,1],[1,2],[2,3],[3,4]],[0]*4),('D_bichromatic_cycle',4,[[0,1],[1,2],[2,3],[3,0]],[1,2,1,2])]:
        mutations.append(rejection(name,lambda n=n,e=e,col=col:c.compile_rows(n,e,col)))
    shared,bad=shared_arc_audit();mutations.append(bad)
    rn=results['negative_six_cycle_frame'];core=rn['shortest_core']
    mutations.append(rejection('core_duplicate_row',lambda:c.validate_core(3,rn['rows'],core+[core[0]])))
    mutations.append(rejection('core_missing_row',lambda:c.validate_core(3,rn['rows'],core[:-1])))
    # Recoloring a single D edge erases the C6 obstruction under the outer theorem.
    outer=c.erase_to_forest(6,neg['edges'],neg['partial_colors'],[0],2)
    mutations.append(rejection('outer_nonspare_color',lambda:c.erase_to_forest(6,neg['edges'],neg['partial_colors'],[0],1)))
    mutations.append(rejection('outer_unhit_core',lambda:c.erase_to_forest(6,neg['edges'],neg['partial_colors'],[],2)))
    mutations.append(rejection('outer_noninduced_matching',lambda:c.erase_to_forest(6,neg['edges'],neg['partial_colors'],[0,2],2)))
    signed=signed_exhaustion()
    matching_obstruction=matching_four_cycle_obstruction(d['positive_k4_frame'])
    positive=outer_positive_controls()
    source=hashlib.sha256((HERE/'opg37271-c20-core.py').read_bytes()).hexdigest()
    certificate=dict(verdict='candidate_only',input_sha256=INPUT,core_source_sha256=source,
                     frames=results,boundaries=fixture_results,shared_arc_test=shared,
                     mutations=mutations,signed_exhaustion=signed,outer_erasure=outer,outer_contact=positive,matching_frame_obstruction=matching_obstruction,
                     scope='Graph-bound local certificates and bounded exact algebra tests; no trusted admission.')
    data=(json.dumps(certificate,sort_keys=True,separators=(',',':'))+'\n').encode()
    c.need(len(data)<=LIMIT,'certificate cap')
    (HERE/'opg37271-c20-certificate.json').write_bytes(data)
    summary=dict(verdict='candidate_only',runtime=platform.python_version(),input_sha256=INPUT,
                 certificate_sha256=hashlib.sha256(data).hexdigest(),certificate_bytes=len(data),
                 mutations=len(mutations),matching_frame_cases=len(matching_obstruction['cases']),signed_cases=signed['cases'],signed_unsat=signed['unsatisfiable'],
                 negative_minimum_core=len(results['negative_six_cycle_frame']['shortest_core']),
                 positive_solutions=results['positive_k4_frame']['good_phases'],
                 self_minimum_core=len(fixture_results['self']['shortest_core']),
                 parallel_minimum_core=len(fixture_results['parallel']['shortest_core']),
                 outer_rows_before=outer['old_row_count'],outer_rows_after=outer['new_row_count'],
                 outer_coloring=outer['full_colors'],proof_status='candidate_only')
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':
    main()
