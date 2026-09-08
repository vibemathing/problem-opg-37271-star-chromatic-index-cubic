"""C28 literal checker and separate small-realization audit.
Imports no candidate implementation. This is generator-domain checking only.
Run with the companion resource-limited runner.
"""
from collections import Counter
from itertools import combinations, product, permutations
from pathlib import Path
import hashlib
import json


def need(x, message):
    if not x:
        raise ValueError(message)


def dumps(x):
    return (json.dumps(x, sort_keys=True, separators=(',', ':')) + '\n').encode()


class Literal:
    def __init__(self, n, edges):
        self.n = n
        self.edges = [tuple(e) for e in edges]
        self.adj = [[] for _ in range(n)]
        used = set()
        for e, (u, v) in enumerate(self.edges):
            need(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n and u != v, 'simple endpoints')
            need(frozenset((u, v)) not in used, 'no duplicate edge')
            used.add(frozenset((u, v)))
            self.adj[u].append((v, e)); self.adj[v].append((u, e))
        need(all(len(a) <= 3 for a in self.adj), 'subcubic')
        self.walks = {}
        def walk(vertices, es):
            if len(es) == 4:
                self.walks[tuple(sorted(es))] = ('path', tuple(vertices))
                return
            for v, e in self.adj[vertices[-1]]:
                if v in vertices:
                    if len(es) == 3 and v == vertices[0]:
                        self.walks[tuple(sorted(es + [e]))] = ('cycle', tuple(vertices))
                    continue
                walk(vertices + [v], es + [e])
        for v in range(n):
            walk([v], [])

    def proper(self, colors):
        return all(len([colors[e] for _, e in a if colors[e]]) == len({colors[e] for _, e in a if colors[e]}) for a in self.adj)

    def pair_star(self, word):
        if not self.proper(word):
            return False
        for a, b in combinations(range(1, 5), 2):
            rem = {e for e, c in enumerate(word) if c in (a, b)}
            while rem:
                seed = rem.pop(); stack = [seed]; size = 1
                while stack:
                    e = stack.pop()
                    for v in self.edges[e]:
                        for _, f in self.adj[v]:
                            if f in rem:
                                rem.remove(f); stack.append(f); size += 1
                if size > 3:
                    return False
        return True

    def paths(self, word):
        rem = {e for e, c in enumerate(word) if not c}; paths = []
        while rem:
            seed = min(rem); stack = [seed]; part = {seed}; rem.remove(seed)
            while stack:
                e = stack.pop()
                for v in self.edges[e]:
                    for _, f in self.adj[v]:
                        if f in rem:
                            rem.remove(f); part.add(f); stack.append(f)
            verts = {v for e in part for v in self.edges[e]}
            deg = {v: sum(e in part for _, e in self.adj[v]) for v in verts}
            ends = sorted(v for v in verts if deg[v] == 1)
            if len(part) > 3 or max(deg.values()) > 2 or len(ends) != 2 or len(verts) != len(part) + 1:
                return None
            v = ends[0]; seq = []
            while len(seq) < len(part):
                u, e = next((u, e) for u, e in self.adj[v] if e in part and e not in seq)
                seq.append(e); v = u
            paths.append(seq)
        return paths

    def frame(self, word):
        return len(word) == len(self.edges) and all(type(c) is int and 0 <= c <= 4 for c in word) and self.pair_star(word) and self.paths(word) is not None

    def bad(self, colors):
        return sorted(key for key in self.walks if len({colors[e] for e in key}) == 2)

    def endpoint_family(self, old, support):
        """All literal 1..6 fillings, grouped only AFTER acceptance."""
        support = set(support); paths = self.paths(old)
        need(paths is not None and all(not (set(p) & support) or set(p) <= support for p in paths), 'old closure')
        outside = [p for p in paths if not set(p) & support]
        indices = sorted(support); groups = {}
        for b in range(1 << len(outside)):
            full = old.copy()
            for j, p in enumerate(outside):
                for k, e in enumerate(p):
                    full[e] = 5 + ((b >> j & 1) ^ (k % 2))
            for e in indices:
                full[e] = 0
            def fill(k):
                if k != len(indices):
                    e = indices[k]; u, v = self.edges[e]
                    for c in range(1, 7):
                        if any(full[f] == c for z in (u, v) for _, f in self.adj[z] if f != e):
                            continue
                        full[e] = c; fill(k + 1)
                    full[e] = 0; return
                word = [c if c <= 4 else 0 for c in full]
                if not self.frame(word):
                    return
                ps = self.paths(word)
                if any(set(p) & support and set(p) - support for p in ps):
                    return
                inside = [p for p in ps if set(p) & support]
                need([p for p in ps if not set(p) & support] == outside, 'outside component identity')
                a = sum((full[p[0]] - 5) << j for j, p in enumerate(inside))
                bad = self.bad(full)
                key = tuple(word)
                record = (len(bad), sum(bool(set(q) & support) for q in bad), tuple(bad), tuple(full))
                slot = (b, a)
                need(slot not in groups.setdefault(key, {}), 'unique literal phase')
                groups[key][slot] = record
            fill(0)
        return outside, groups


def smaller(n, lengths, gauge):
    """D-edge-subset matching enumeration, vertex-walk pair witnesses, class cliques."""
    U = []; info = []; start = 0
    for c, length in enumerate(lengths):
        for j in range(length):
            U.append((start + j, start + j + 1)); info.append((c, j % 2))
        start += length + 1
    D = [e for e in combinations(range(n), 2) if e not in U]
    masks = [(1 << u) | (1 << v) for u, v in D]
    du = [sum(v in e for e in U) for v in range(n)]
    pair = {}; invalid = set()
    target = (1, 2, 3, 1)
    for i, j in combinations(range(len(D)), 2):
        if masks[i] & masks[j]:
            continue
        gg = Literal(n, U + [D[i], D[j]])
        # Single D color and two U colors; select alternating membership geometrically.
        hits = []
        for key in gg.walks:
            if len(U) not in key or len(U) + 1 not in key:
                continue
            ue = [k for k in key if k < len(U)]
            if len(ue) != 2 or set(U[ue[0]]) & set(U[ue[1]]):
                continue
            a, p = info[ue[0]]; b, q = info[ue[1]]
            if a > b:
                a, b = b, a
            hits.append((a, b, 1 ^ p ^ q))
        vec = [0] * 4; wrong = False
        for a, b, rhs in hits:
            if a == b:
                if a != 0 or rhs != 1:
                    wrong = True; break
                k = 0
            else:
                if rhs != (gauge[a] ^ gauge[b]):
                    wrong = True; break
                k = {(0, 1): 1, (0, 2): 2, (1, 2): 3}[a, b]
            vec[k] += 1
        if wrong:
            invalid.add((i, j))
        elif any(vec):
            pair[i, j] = tuple(vec)
    matches = []; classes = []
    def match(next_edge, occupied, chosen):
        matches.append(tuple(chosen))
        for e in range(next_edge, len(D)):
            if not masks[e] & occupied:
                match(e + 1, occupied | masks[e], chosen + [e])
    match(0, 0, [])
    for chosen in matches:
        if len(chosen) < 2:
            continue
        vec = [0] * 4; active = set()
        for i, j in combinations(chosen, 2):
            if (i, j) in invalid:
                break
            row = pair.get((i, j))
            if row:
                active.update((i, j)); vec = [a + b for a, b in zip(vec, row)]
        else:
            if len(active) == len(chosen) and all(a <= b for a, b in zip(vec, target)):
                classes.append((chosen, tuple(vec)))
    classes.sort()
    adj = [set() for _ in classes]
    for i, j in combinations(range(len(classes)), 2):
        a, b = classes[i][0], classes[j][0]
        if set(a) & set(b):
            continue
        gg = Literal(n, [D[e] for e in a + b])
        if gg.pair_star([1] * len(a) + [2] * len(b)):
            adj[i].add(j); adj[j].add(i)
    visits = 0; solutions = 0
    def extend(chosen, allowed, counts, deg):
        nonlocal visits, solutions
        visits += 1
        if tuple(counts) == target:
            if all(a + b > 0 for a, b in zip(du, deg)):
                solutions += 1
            return
        if len(chosen) == 4:
            return
        for k in allowed:
            es, cc = classes[k]; nc = [a + b for a, b in zip(counts, cc)]
            if any(a > b for a, b in zip(nc, target)):
                continue
            nd = deg.copy()
            for e in es:
                for v in D[e]:
                    nd[v] += 1
            if any(a + b > 3 for a, b in zip(du, nd)):
                continue
            extend(chosen + [k], [j for j in allowed if j > k and j in adj[k]], nc, nd)
    extend([], list(range(len(classes))), [0] * 4, [0] * n)
    sha = hashlib.sha256(json.dumps(classes, separators=(',', ':')).encode()).hexdigest()
    return {'class_sha256': sha, 'n': n, 'lengths': lengths, 'gauge': gauge, 'all_matchings': len(matches), 'productive_classes': len(classes), 'class_search_nodes': visits, 'solutions_found': solutions}


def run():
    root = Path(__file__).resolve().parent
    iraw = (root / 'opg37271-c28-input.json').read_bytes()
    raw = (root / 'opg37271-c28-certificate.json').read_bytes()
    inp, cert = json.loads(iraw), json.loads(raw)
    binding = json.loads((root/'opg37271-c28-certificate-binding.json').read_bytes())
    need(hashlib.sha256(raw).hexdigest() == binding['expanded_sha256'], 'frozen expanded certificate')
    need(hashlib.sha256(iraw).hexdigest() == cert['input_sha256'], 'input digest')
    g = Literal(inp['n'], inp['edges']); old = inp['old']
    need(g.frame(old) and g.frame(inp['specified_new']) and g.frame(inp['improving_new']), 'endpoint premises')
    keys = [tuple(sorted(z['edges'])) for z in cert['shapes']]
    need(len(keys) == len(set(keys)) and set(keys) == set(g.walks), 'all shapes')
    for z in cert['shapes']:
        vs, es = z['vertices'], z['edges']; cyc = z['kind'] == 'cycle'
        need(len(vs) == (4 if cyc else 5) and len(set(vs)) == len(vs), 'injective witnesses')
        for j, e in enumerate(es):
            need(set(g.edges[e]) == {vs[j], vs[(j + 1) % len(vs)]}, 'witness incidence')
    families_checked = 0; full_phases = 0
    def compare_family(support, stored):
        nonlocal families_checked, full_phases
        outside, actual = g.endpoint_family(old, support)
        need(set(actual) == {tuple(z['word']) for z in stored}, 'complete endpoint family')
        for z in stored:
            need(z['outside_paths'] == outside, 'boundary convention')
            expect = {}
            for b, row in enumerate(z['phases']):
                for a, total in enumerate(row['total_costs']):
                    bad = tuple(sorted(keys[j] for j in row['bad_shapes'][a]))
                    expect[b, a] = (total, row['touch_costs'][a], bad, tuple(row['colors'][a]))
            need(expect == actual[tuple(z['word'])], 'all literal colors, costs and witnesses')
            need(z['sigma'] == [min(row['touch_costs']) for row in z['phases']], 'profile minima')
            full_phases += len(expect)
        families_checked += 1
        return actual
    for name, family in cert['families'].items():
        actual = compare_family(family['support'], family['endpoints'])
        need(family['envelope'] == [min(z['sigma'][b] for z in family['endpoints']) for b in range(4)], 'family envelope')
    for family in cert['single_supports']:
        compare_family(family['support'], family['endpoints'])
    need(len(cert['single_supports']) == 10, 'all old-closed singleton supports')
    need(len(cert['smaller_realizations']) == 16, 'all smaller topology/gauge cases')
    lower = [smaller(z['n'], z['lengths'], z['gauge']) for z in cert['smaller_realizations']]
    need(lower == cert['smaller_realizations'] and all(z['solutions_found'] == 0 for z in lower), 'complete smaller realization check')
    # Literal computation of sigma/h/r/g for the specified endpoints.
    S, T = set(inp['model_support']), set(inp['absorbed_support'])
    oldrows = cert['old_full']['phases'][0]
    need(min(oldrows['total_costs']) == 1 and min(cert['repair_full']['phases'][0]['total_costs']) == 0, 'not a global minimum')
    for b, term in enumerate(cert['absorption_terms']):
        oldsigma = next(z for z in cert['families']['model_support']['endpoints'] if z['word'] == old)['sigma'][b]
        newsigma = next(z for z in cert['families']['model_support']['endpoints'] if z['word'] == inp['specified_new'])['sigma'][b]
        need((oldsigma, newsigma, term['h'], term['r'], term['g']) == ((1 if b in (0, 3) else 3), (1 if b in (0, 3) else 0), (0 if b in (0, 3) else 1), (0 if b in (0, 3) else 3), (0 if b in (0, 3) else 3)), 'exact C27 numeric table')
        need(term['old'] == oldsigma and term['new'] == newsigma, 'table binding')
        colors = next(z for z in cert['families']['model_support']['endpoints'] if z['word'] == old)['phases'][b]['colors'][0]
        hs = [q for q in g.bad(colors) if set(q) & T and not set(q) & S]
        need(hs == sorted(keys[j] for j in term['h_shapes']), 'all newly touched h shapes')
    need(cert['gain'] == max(z['g'] - z['r'] for z in cert['absorption_terms']) == 0, 'gain zero')
    # Detect attacks on the frozen interfaces and representation.
    mutations = []
    def reject(name, fn):
        try:
            fn()
        except (ValueError, IndexError, KeyError, TypeError):
            mutations.append(name); return
        raise ValueError('mutation survived: ' + name)
    reject('cross_palette_A', lambda: need(g.frame([5] + old[1:]), 'palette'))
    reject('U_length_four', lambda: need(Literal(5, [(0,1),(1,2),(2,3),(3,4)]).frame([0]*4), 'length'))
    reject('U_degree_three', lambda: need(Literal(4, [(0,1),(0,2),(0,3)]).frame([0]*3), 'branch'))
    reject('duplicate_graph_edge', lambda: Literal(inp['n'], inp['edges'] + [inp['edges'][0]]))
    reject('exterior_color_edge_exceeds_saturated_degree', lambda: Literal(11, inp['edges'] + [[8,10]]))
    reject('missing_middle_U_closure', lambda: g.endpoint_family(old, set(inp['core_support']) - {11}))
    reject('partly_absorbed_port', lambda: g.endpoint_family(old, T - {1}))
    reject('missing_legal_endpoint', lambda: need(len(cert['families']['core_support']['endpoints'][:-1]) == 82, 'endpoint coverage'))
    reject('missing_gauge_case', lambda: need(len(lower[:-1]) == 16, 'gauge coverage'))
    core = inp['core_vertices']
    reject('nonsimple_witness', lambda: need(len(set([core[0]] + core[:-1])) == 5, 'distinct vertices'))
    reject('path_called_cycle', lambda: need(any({core[0],core[-1]} == set(e) for e in g.edges), 'closing edge'))
    chord = any(abs(core.index(u)-core.index(v)) > 1 for u,v in g.edges if u in core and v in core)
    need(chord, 'noninduced self fixture'); mutations.append('induced_only_would_remove_self')
    cyc = Literal(4, [(0,1),(1,2),(2,3),(3,0)])
    need(len(cyc.bad([1,5,1,5])) == 1, 'C4 retained'); mutations.append('omit_C4')
    # Recompute old row algebra from actual alternating shapes.
    ps = g.paths(old); info = {e:(i,j%2) for i,p in enumerate(ps) for j,e in enumerate(p)}
    rs = []
    for key in g.walks:
        ue = [e for e in key if old[e] == 0]; de = [e for e in key if old[e]]
        if len(ue) != 2 or len(de) != 2 or set(g.edges[ue[0]]) & set(g.edges[ue[1]]) or old[de[0]] != old[de[1]]:
            continue
        i,p = info[ue[0]]; j,q = info[ue[1]]; rs.append((min(i,j),max(i,j),1^p^q))
    need(Counter(rs) == Counter({(1,1,1):1,(0,1,1):2,(1,2,1):3,(0,2,0):1}), 'exact seven witness counts')
    def value(rows, bits):
        return sum((bits[i]^bits[j]) != r for i,j,r in rows)
    costs = [value(rs, [(a>>i)&1 for i in range(3)]) for a in range(8)]
    need(costs == oldrows['total_costs'], 'literal/XOR correspondence')
    need(min(value([r for r in rs if r[0] != r[1]], [(a>>i)&1 for i in range(3)]) for a in range(8)) == 0, 'loop deletion diagnosed');mutations.append('delete_self_row')
    need([value(list(set(rs)),[(a>>i)&1 for i in range(3)]) for a in range(8)] != costs, 'multiplicity changes costs');mutations.append('deduplicate_geometric_witnesses')
    reject('omit_h_false_positive', lambda: need(max(z['g']-(z['old']-1) for z in cert['absorption_terms']) == cert['gain'], 'h matters'))
    reject('all_endpoint_optima_equal_specified_Q', lambda: need(cert['families']['model_support']['envelope'] == [1]*4, 'new endpoint family'))
    reject('frame_phase_optimum_is_global_optimum', lambda: need(min(cert['repair_full']['phases'][0]['total_costs']) >= 1, 'better frame'))
    reject('wrong_XOR_sign', lambda: need(Counter(rs) == Counter((i,j,r^1) for i,j,r in rs), 'sign'))
    reject('delete_all_positive_regret_terms', lambda: need(sum(z['r'] > 0 for z in cert['absorption_terms']) == 0, 'retain nonattainers'))
    relabel_checks = 0
    for perm in permutations(range(1, 5)):
        mapped = [[perm[c-1] if c else 0 for c in inp[k]] for k in ('old','specified_new','improving_new')]
        for word in mapped:
            need(g.frame(word), 'A-label invariance')
        relabel_checks += 1
    variant = old.copy(); variant[3] = 4
    variant_new = variant.copy(); variant_new[14] = 4
    need(set(variant) == set(range(5)) and g.frame(variant) and g.frame(variant_new), 'all A colors used control')
    ps = g.paths(variant)
    for mask in range(1 << len(ps)):
        a, b = variant.copy(), variant_new.copy()
        for i,p in enumerate(ps):
            for j,e in enumerate(p):
                a[e] = b[e] = 5 + ((mask >> i & 1) ^ (j % 2))
        need(len(g.bad(b)) <= len(g.bad(a))-1, 'completion control pointwise improvement')
    distance = {14: 0}; frontier = [14]
    while frontier:
        e = frontier.pop(0)
        if distance[e] == 2:
            continue
        for v in g.edges[e]:
            for _, f in g.adj[v]:
                if f not in distance:
                    distance[f] = distance[e]+1; frontier.append(f)
    need(sorted(distance.items()) == [tuple(z) for z in cert['line_distance_two']], 'geometric radius-two identity')
    need(all(old[e] != 4 for e in distance), 'forced missing local color')
    result = {'verdict':'candidate_only','best_verified_result':'none','certificate_sha256':hashlib.sha256(raw).hexdigest(),'input_sha256':hashlib.sha256(iraw).hexdigest(),'families_checked':families_checked,'full_phase_colorings_checked':full_phases,'smaller_cases_checked':len(lower),'smaller_realizations_found':0,'exact_model_gain':0,'global_model_conjunction':'open_for_other_realizations; displayed motif excluded by explicit improvement','mutations':mutations,'A_relabelings_checked':relabel_checks,'all_A_colors_used_control':True}
    (root/'opg37271-c28-check-result.json').write_bytes(dumps(result))
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    run()
