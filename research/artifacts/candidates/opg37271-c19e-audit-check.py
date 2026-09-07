"""C19-E definition-first bounded audit. Candidate output, not an admission receipt.
No imports from the C19 compiler/replay. Input is the frozen main certificate.
"""
from __future__ import annotations
from copy import deepcopy
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import platform
import resource
import signal
import sys

INPUT_SHA256 = '9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3'
LIMIT = 262144


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def graph(n, edges):
    require(type(n) is int and 0 <= n <= 10, 'bounded order')
    require(type(edges) is list and len(edges) <= 15, 'bounded edge list')
    adj = [[] for _ in range(n)]
    lookup = {}
    for e, pair in enumerate(edges):
        require(len(pair) == 2, 'edge arity')
        a, b = pair
        require(type(a) is int and type(b) is int and 0 <= a < n and 0 <= b < n and a != b, 'endpoints')
        key = tuple(sorted(pair))
        require(key not in lookup, 'duplicate edge')
        lookup[key] = e
        adj[a].append(e)
        adj[b].append(e)
    require(all(len(es) <= 3 for es in adj), 'subcubic')
    return adj, lookup


def star_by_components(n, edges, colors, partial=False):
    """Direct coloring test: properness plus sizes of all two-color components."""
    adj, _ = graph(n, edges)
    require(len(colors) == len(edges), 'color dimensions')
    require(all(type(c) is int and int(not partial) <= c <= 6 for c in colors), 'color range')
    for es in adj:
        cs = [colors[e] for e in es if colors[e] != 0]
        if len(cs) != len(set(cs)):
            return False
    for a, b in combinations(range(1, 7), 2):
        todo_edges = {e for e, c in enumerate(colors) if c in (a, b)}
        while todo_edges:
            first = min(todo_edges)
            todo_edges.remove(first)
            todo = [first]
            size = 0
            while todo:
                e = todo.pop()
                size += 1
                for v in edges[e]:
                    for f in adj[v]:
                        if f in todo_edges:
                            todo_edges.remove(f)
                            todo.append(f)
            if size >= 4:
                return False
    return True


@lru_cache(maxsize=64)
def shapes(n, edge_tuple):
    """All simple paths/cycles, from vertex permutations rather than a DFS."""
    lookup = {tuple(sorted(e)): i for i, e in enumerate(edge_tuple)}
    out = []
    for vs in permutations(range(n), 5):
        if vs[0] > vs[-1]:
            continue
        pairs = [tuple(sorted((vs[i], vs[i+1]))) for i in range(4)]
        if all(p in lookup for p in pairs):
            out.append(('path', vs, tuple(lookup[p] for p in pairs)))
    for vs in permutations(range(n), 4):
        if vs[0] != min(vs) or vs[1] > vs[-1]:
            continue
        pairs = [tuple(sorted((vs[i], vs[(i+1) % 4]))) for i in range(4)]
        if all(p in lookup for p in pairs):
            out.append(('cycle', vs, tuple(lookup[p] for p in pairs)))
    return tuple(out)


def premise(n, edges, partial):
    adj, _ = graph(n, edges)
    require(len(partial) == len(edges) and all(type(c) is int and 0 <= c <= 4 for c in partial), 'A palette')
    require(star_by_components(n, edges, partial, True), 'D not star')
    parent = list(range(n))
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for e, (a, b) in enumerate(edges):
        if partial[e] == 0:
            parent[root(a)] = root(b)
    groups = {}
    for e, c in enumerate(partial):
        if c == 0:
            groups.setdefault(root(edges[e][0]), []).append(e)
    paths = []
    for es in sorted(groups.values(), key=min):
        require(1 <= len(es) <= 3, 'U length bound')
        incident = {}
        for e in es:
            for v in edges[e]:
                incident.setdefault(v, []).append(e)
        ends = sorted(v for v, fs in incident.items() if len(fs) == 1)
        require(len(ends) == 2 and len(incident) == len(es)+1 and max(map(len, incident.values())) <= 2, 'U path shape')
        v = ends[0]
        seq = []
        for _ in es:
            fs = [f for f in incident[v] if f not in seq]
            require(len(fs) == 1, 'U path traversal')
            e = fs[0]
            seq.append(e)
            v = next(w for w in edges[e] if w != v)
        paths.append(seq)
    return paths


def equations(n, edges, partial, paths, mode='exact'):
    info = {e: (i, j % 2) for i, seq in enumerate(paths) for j, e in enumerate(seq)}
    rows = {}
    lookup = {tuple(sorted(e)) for e in edges}
    for kind, vs, es in shapes(n, tuple(map(tuple, edges))):
        if mode == 'omit_cycles' and kind == 'cycle':
            continue
        if mode == 'induced_only' and kind == 'path':
            if any(tuple(sorted((vs[i], vs[j]))) in lookup for i in range(5) for j in range(i+2, 5)):
                continue
        free = [i for i, e in enumerate(es) if partial[e] == 0]
        if free not in ([0, 2], [1, 3]):
            continue
        fixed = [i for i in range(4) if i not in free]
        if mode != 'ignore_fixed_equality' and partial[es[fixed[0]]] != partial[es[fixed[1]]]:
            continue
        e, f = [es[i] for i in free]
        i, p = info[e]
        j, q = info[f]
        rhs = 1 ^ p ^ q
        if mode == 'omit_one':
            rhs ^= 1
        if mode == 'drop_loops' and i == j:
            continue
        key = (min(i, j), max(i, j), rhs)
        if mode == 'collapse_parallel':
            key = key[:2]
        if key not in rows:
            rows[key] = dict(i=i, j=j, rhs=rhs, kind=kind, vertices=list(vs), edges=list(es), free_edges=[e, f])
    return list(rows.values())


def decode(partial, paths, phase):
    out = partial.copy()
    for i, seq in enumerate(paths):
        for j, e in enumerate(seq):
            out[e] = 5 + (phase[i] ^ (j % 2))
    return out


def satisfies(rows, phase):
    return all((phase[r['i']] ^ phase[r['j']]) == r['rhs'] for r in rows)


def compare_all(n, edges, partial, mode='exact', paths=None):
    if paths is None:
        paths = premise(n, edges, partial)
    rows = equations(n, edges, partial, paths, mode)
    good = []
    mismatches = []
    for phase in product((0, 1), repeat=len(paths)):
        full = decode(partial, paths, phase)
        direct = star_by_components(n, edges, full)
        signed = satisfies(rows, phase)
        if direct:
            good.append(list(phase))
        if direct != signed:
            mismatches.append(dict(phase=list(phase), direct=direct, equation_test=signed, colors=full))
    return dict(paths=paths, equations=rows, phase_trials=2**len(paths), valid_phases=good, mismatches=mismatches)


def witness_check(n, edges, partial, paths, row):
    require(all(type(row[k]) is int for k in ('i', 'j', 'rhs')), 'integer equation fields')
    kind, vs, es = row['kind'], row['vertices'], row['edges']
    require(kind in ('path', 'cycle'), 'witness kind')
    require(len(vs) == (5 if kind == 'path' else 4) and len(set(vs)) == len(vs), 'simple witness vertices')
    require(len(es) == 4 and len(set(es)) == 4, 'four distinct witness edges')
    for t, e in enumerate(es):
        require(type(e) is int and 0 <= e < len(edges), 'witness edge index')
        target = vs[t+1] if kind == 'path' else vs[(t+1) % 4]
        require(set(edges[e]) == {vs[t], target}, 'witness edge incidence')
    info = {e: (i, j % 2) for i, seq in enumerate(paths) for j, e in enumerate(seq)}
    free = [t for t, e in enumerate(es) if partial[e] == 0]
    require(free in ([0, 2], [1, 3]), 'witness D/U alternation')
    fixed = [t for t in range(4) if t not in free]
    require(partial[es[fixed[0]]] == partial[es[fixed[1]]], 'witness fixed color equality')
    e, f = [es[t] for t in free]
    i, p = info[e]
    j, q = info[f]
    require(row['free_edges'] == [e, f] and row['i'] == i and row['j'] == j and type(row['rhs']) is int and row['rhs'] == (1 ^ p ^ q), 'witness equation fidelity')


def row_key(row):
    return min(row['i'], row['j']), max(row['i'], row['j']), row['rhs']


def replay(obj):
    n, es, c = obj['n'], obj['edges'], obj['partial_colors']
    paths = premise(n, es, c)
    require(obj['uncolored_paths'] == paths, 'canonical U components')
    for row in obj['equations']:
        witness_check(n, es, c, paths, row)
    result = compare_all(n, es, c)
    require(not result['mismatches'], 'C19-E phase mismatch')
    require({row_key(q) for q in obj['equations']} == {row_key(q) for q in result['equations']}, 'complete equation set')
    if obj['phase'] is None:
        ids = obj['contradiction_rows']
        require(ids and len(set(ids)) == len(ids), 'contradiction row selection')
        variables, bit = set(), 0
        for t in ids:
            require(type(t) is int and 0 <= t < len(obj['equations']), 'contradiction row index')
            q = obj['equations'][t]
            for i in (q['i'], q['j']):
                variables.symmetric_difference_update({i})
            bit ^= q['rhs']
        require(not variables and bit == 1, 'parity contradiction')
        require(not result['valid_phases'], 'negative phase enumeration')
        result['negative_sum'] = dict(remaining_variables=[], rhs=1)
    else:
        phase = obj['phase']
        require(len(phase) == len(paths) and all(type(x) is int and x in (0, 1) for x in phase), 'phase bits')
        full = decode(c, paths, phase)
        require(full == obj['full_colors'], 'decoded full coloring')
        require(star_by_components(n, es, full), 'positive coloring')
        require(satisfies(result['equations'], phase), 'positive phase equations')
        result['full_colors'] = full
    return result


def fixtures():
    return {
        'empty_graph': (0, [], []),
        'U_empty': (4, [[0,1],[1,2],[2,3],[3,0]], [1,2,3,4]),
        'U_one_edge': (2, [[0,1]], [0]),
        'U_two_edges': (3, [[0,1],[1,2]], [0,0]),
        'U_three_edges': (4, [[0,1],[1,2],[2,3]], [0,0,0]),
        'four_cycle_only': (4, [[0,1],[1,2],[2,3],[3,0]], [1,0,1,0]),
        'noninduced_same_component': (5, [[0,1],[1,2],[2,3],[1,3],[2,4]], [0,0,0,1,1]),
        'opposite_parallel': (5, [[0,1],[1,2],[3,4],[0,3],[2,4]], [0,0,0,1,1]),
        'unequal_D_colors': (5, [[0,1],[1,2],[2,3],[3,4]], [1,0,2,0]),
    }


def expect_rejection(label, action):
    try:
        action()
    except ValueError as exc:
        return dict(name=label, error=str(exc))
    raise ValueError('mutation survived: ' + label)


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(35)
    resource.setrlimit(resource.RLIMIT_CPU, (30,31))
    resource.setrlimit(resource.RLIMIT_AS, (256*1024**2,)*2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT,)*2)
    require(len(sys.argv) == 2, 'usage: check.py INPUT_CERTIFICATE')
    raw = Path(sys.argv[1]).read_bytes()
    require(len(raw) <= LIMIT and hashlib.sha256(raw).hexdigest() == INPUT_SHA256, 'frozen input digest')
    d = json.loads(raw)
    replayed = {name: replay(d[name]) for name in ('negative_six_cycle_frame', 'positive_k4_frame')}
    require(star_by_components(6, d['negative_six_cycle_frame']['edges'], d['six_cycle_wider_palette']), 'wider-palette example')
    tested_fixtures = {}
    reverse_trials = 0
    for name, (n, es, c) in fixtures().items():
        r = compare_all(n, es, c)
        require(not r['mismatches'], 'fixture mismatch: ' + name)
        originals = {tuple(decode(c, r['paths'], p)) for p in r['valid_phases']}
        for flips in product((0,1), repeat=len(r['paths'])):
            ps = [seq[::-1] if flip else seq[:] for seq, flip in zip(r['paths'], flips)]
            rr = compare_all(n, es, c, paths=ps)
            require(not rr['mismatches'] and {tuple(decode(c, ps, p)) for p in rr['valid_phases']} == originals, 'orientation invariance')
            reverse_trials += 1
        tested_fixtures[name] = dict(n=n, edges=es, partial_colors=c, **r)
    shape_audits = []
    for name, n, es in [('P5',5,[[0,1],[1,2],[2,3],[3,4]]),('C4',4,[[0,1],[1,2],[2,3],[3,0]])]:
        valid = invalid = trials = 0
        for c in product(range(5), repeat=4):
            try:
                ps = premise(n, es, list(c))
            except ValueError:
                invalid += 1
                continue
            r = compare_all(n, es, list(c), paths=ps)
            require(not r['mismatches'], 'four-edge exhaustive mismatch')
            valid += 1
            trials += r['phase_trials']
        shape_audits.append(dict(shape=name, partial_inputs=625, admitted_inputs=valid, rejected_premise_inputs=invalid, phase_trials=trials))
    corruptions = []
    for label in ('wrong_rhs','repeated_vertex','wrong_edge','incomplete_contradiction','missing_equation','wrong_phase','wrong_full_color','wrong_U_path_list'):
        obj = deepcopy(d['positive_k4_frame'] if label in ('missing_equation','wrong_phase','wrong_full_color') else d['negative_six_cycle_frame'])
        if label == 'wrong_rhs': obj['equations'][0]['rhs'] ^= 1
        elif label == 'repeated_vertex': obj['equations'][0]['vertices'][1] = obj['equations'][0]['vertices'][0]
        elif label == 'wrong_edge': obj['equations'][0]['edges'][0] = len(obj['edges'])
        elif label == 'incomplete_contradiction': obj['contradiction_rows'].pop()
        elif label == 'missing_equation': obj['equations'].pop()
        elif label == 'wrong_phase': obj['phase'][0] ^= 1
        elif label == 'wrong_full_color': obj['full_colors'][0] = 7
        elif label == 'wrong_U_path_list': obj['uncolored_paths'] = [[1,3],[5]]
        corruptions.append(expect_rejection(label, lambda obj=obj: replay(obj)))
    premise_failures = [
        ('U_length_four',5,[[0,1],[1,2],[2,3],[3,4]],[0]*4),
        ('U_is_cycle',3,[[0,1],[1,2],[2,0]],[0]*3),
        ('U_branches',4,[[0,1],[0,2],[0,3]],[0]*3),
        ('D_not_star',5,[[0,1],[1,2],[2,3],[3,4]],[1,2,1,2]),
        ('D_uses_reserved_color',2,[[0,1]],[5]),
    ]
    for label, n, es, c in premise_failures:
        corruptions.append(expect_rejection(label, lambda n=n,es=es,c=c: premise(n,es,c)))
    killed = []
    for mode, name in [('omit_cycles','four_cycle_only'),('induced_only','noninduced_same_component'),('drop_loops','noninduced_same_component'),('collapse_parallel','opposite_parallel'),('omit_one','four_cycle_only'),('ignore_fixed_equality','unequal_D_colors')]:
        n, es, c = fixtures()[name]
        r = compare_all(n, es, c, mode)
        require(bool(r['mismatches']), 'compiler mutant survived: ' + mode)
        killed.append(dict(mutation=mode, fixture=name, witness=r['mismatches'][0]))
    positive_rows = 0
    require(len(d['permutation_rows']) == 24, 'positive row coverage')
    for index, (row, perm) in enumerate(zip(d['permutation_rows'], permutations(range(4)))):
        es = [[i,4+perm[i]] for i in range(4)] + [[i,(i+1)%4] for i in range(4)] + [[4+i,4+(i+1)%4] for i in range(4)]
        require(row[0] == index and row[4][:4] == [1,2,3,4], 'positive row binding')
        require(star_by_components(8, es, row[4]), 'positive row direct coloring')
        positive_rows += 1
    certificate = dict(verdict='candidate_only', input_sha256=INPUT_SHA256, frame_replays=replayed, boundary_fixtures=tested_fixtures,
                       exhaustive_shape_audits=shape_audits, orientation_trials=reverse_trials, certificate_mutations=corruptions, compiler_mutations=killed,
                       positive_rows_directly_checked=positive_rows, ignored_prior_claims=['6144-frame tally','55296-phase tally','prior runtime and success fields'])
    encoded = (json.dumps(certificate, sort_keys=True, separators=(',',':'))+'\n').encode()
    require(len(encoded) <= LIMIT, 'certificate output limit')
    outpath = Path(__file__).with_name('opg37271-c19e-audit-certificate.json')
    outpath.write_bytes(encoded)
    result = dict(verdict='candidate_only', status='finite_audit_pass', runtime=platform.python_version(), input_sha256=INPUT_SHA256,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), certificate_sha256=hashlib.sha256(encoded).hexdigest(), certificate_bytes=len(encoded),
                  negative_phase_trials=replayed['negative_six_cycle_frame']['phase_trials'], positive_phase_trials=replayed['positive_k4_frame']['phase_trials'],
                  positive_solutions=replayed['positive_k4_frame']['valid_phases'], boundary_fixtures=len(tested_fixtures),
                  exhaustive_shape_audits=shape_audits, orientation_trials=reverse_trials, certificate_mutations_rejected=len(corruptions), compiler_mutants_killed=len(killed),
                  positive_rows_directly_checked=positive_rows, limits=dict(wall_seconds=35,cpu_soft_seconds=30,cpu_hard_seconds=31,memory_mib=256,output_bytes=LIMIT,threads=1),
                  limitations='Finite generator-domain audit; no trusted receipt, full historical tally, kernel run, outer-frame existence or root closure.')
    text = json.dumps(result, sort_keys=True, separators=(',',':'))+'\n'
    require(len(text.encode()) <= 16384, 'stdout limit')
    print(text, end='')


if __name__ == '__main__':
    main()
