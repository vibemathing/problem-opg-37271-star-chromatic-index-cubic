"""C20 graph-bound XOR cores. Candidate routines, not a trusted verifier.
The compiler examines four-edge subsets; it imports no prior C19/C19-E code.
Callers must impose the budgets in the companion runner.
"""
from collections import deque
from itertools import combinations, product


def need(test, message):
    if not test:
        raise ValueError(message)


def adjacency(n, edges):
    need(type(n) is int and 0 <= n <= 16, 'graph order bound')
    need(isinstance(edges, list) and len(edges) <= 24, 'graph edge bound')
    adj = [[] for _ in range(n)]
    seen = set()
    for e, pair in enumerate(edges):
        need(len(pair) == 2, 'edge arity')
        a, b = pair
        need(type(a) is int and type(b) is int and 0 <= a < n and 0 <= b < n and a != b, 'simple endpoints')
        key = tuple(sorted(pair))
        need(key not in seen, 'duplicate graph edge')
        seen.add(key)
        adj[a].append((b, e))
        adj[b].append((a, e))
    need(max(map(len, adj), default=0) <= 3, 'subcubic')
    return adj


def direct_star(n, edges, colors, partial=False):
    """Color-pair connectivity, not the compiler's four-edge-subset predicate."""
    adj = adjacency(n, edges)
    need(len(colors) == len(edges), 'color dimension')
    need(all(type(c) is int and (0 if partial else 1) <= c <= 6 for c in colors), 'color range')
    for ns in adj:
        palette = [colors[e] for _, e in ns if colors[e]]
        if len(palette) != len(set(palette)):
            return False
    for a, b in combinations(range(1, 7), 2):
        unseen = set(range(n))
        while unseen:
            root = min(unseen)
            unseen.remove(root)
            stack, degree_sum = [root], 0
            while stack:
                v = stack.pop()
                for w, e in adj[v]:
                    if colors[e] not in (a, b):
                        continue
                    degree_sum += 1
                    if w in unseen:
                        unseen.remove(w)
                        stack.append(w)
            if degree_sum >= 8:
                return False
    return True


def uncolored_paths(n, edges, colors):
    adj = adjacency(n, edges)
    need(len(colors) == len(edges) and all(type(c) is int and 0 <= c <= 4 for c in colors), 'disjoint A palette')
    need(direct_star(n, edges, colors, True), 'D star premise')
    remaining = {e for e, c in enumerate(colors) if c == 0}
    ordered = []
    while remaining:
        seed = min(remaining)
        es, vertices, stack = set(), set(edges[seed]), list(edges[seed])
        while stack:
            v = stack.pop()
            for w, e in adj[v]:
                if colors[e] != 0:
                    continue
                es.add(e)
                if w not in vertices:
                    vertices.add(w)
                    stack.append(w)
        need(1 <= len(es) <= 3, 'U length at most three')
        degrees = {v: sum(e in es for _, e in adj[v]) for v in vertices}
        ends = sorted(v for v in vertices if degrees[v] == 1)
        need(len(ends) == 2 and max(degrees.values()) <= 2 and len(vertices) == len(es) + 1, 'U simple path')
        v, sequence = ends[0], []
        for _ in range(len(es)):
            options = [(w, e) for w, e in adj[v] if e in es and e not in sequence]
            need(len(options) == 1, 'U ordering')
            v, e = options[0]
            sequence.append(e)
        remaining -= es
        ordered.append(sequence)
    return ordered


def four_edge_shapes(edges):
    """Connected four-edge subsets of degree pattern P5 or C4; chords retained."""
    for chosen in combinations(range(len(edges)), 4):
        local = {}
        for e in chosen:
            a, b = edges[e]
            local.setdefault(a, []).append((b, e))
            local.setdefault(b, []).append((a, e))
        pattern = sorted(map(len, local.values()))
        if pattern == [1, 1, 2, 2, 2]:
            kind = 'path'
            v = min(a for a in local if len(local[a]) == 1)
        elif pattern == [2, 2, 2, 2]:
            kind = 'cycle'
            v = min(local)
        else:
            continue
        vertices, sequence = [v], []
        for _ in range(4):
            options = sorted((w, e) for w, e in local[v] if e not in sequence)
            if not options:
                break
            v, e = options[0]
            vertices.append(v)
            sequence.append(e)
        if len(sequence) != 4:
            continue
        if kind == 'path' and len(set(vertices)) == 5:
            yield kind, vertices, sequence
        elif kind == 'cycle' and vertices[-1] == vertices[0] and len(set(vertices[:-1])) == 4:
            yield kind, vertices[:-1], sequence


def compile_rows(n, edges, colors):
    paths = uncolored_paths(n, edges, colors)
    info = {e: (i, j % 2) for i, seq in enumerate(paths) for j, e in enumerate(seq)}
    rows = []
    for kind, vertices, sequence in four_edge_shapes(edges):
        free_positions = [j for j, e in enumerate(sequence) if colors[e] == 0]
        if free_positions not in ([0, 2], [1, 3]):
            continue
        fixed = [e for e in sequence if colors[e] != 0]
        if colors[fixed[0]] != colors[fixed[1]]:
            continue
        e, f = [sequence[j] for j in free_positions]
        i, p = info[e]
        j, q = info[f]
        # Keep EVERY actual shape, even algebraically identical parallel rows.
        rows.append(dict(i=i, j=j, rhs=1 ^ p ^ q, kind=kind, vertices=vertices,
                         edges=sequence, free_edges=[e, f], fixed_edges=fixed))
    return paths, rows


def row_triple(row):
    return min(row['i'], row['j']), max(row['i'], row['j']), row['rhs']


def check_witness(n, edges, colors, paths, row):
    need(row['kind'] in ('path', 'cycle'), 'witness kind')
    vs, es = row['vertices'], row['edges']
    cycle = row['kind'] == 'cycle'
    need(len(vs) == (4 if cycle else 5) and len(set(vs)) == len(vs), 'simple witness vertices')
    need(len(es) == 4 and len(set(es)) == 4, 'four distinct witness edges')
    for t, e in enumerate(es):
        need(type(e) is int and 0 <= e < len(edges), 'witness edge index')
        w = vs[(t + 1) % 4] if cycle else vs[t + 1]
        need(set(edges[e]) == {vs[t], w}, 'witness incidence')
    free = [t for t, e in enumerate(es) if colors[e] == 0]
    need(free in ([0, 2], [1, 3]), 'witness alternation')
    fixed = [e for e in es if colors[e] != 0]
    need(colors[fixed[0]] == colors[fixed[1]] and colors[fixed[0]] in (1, 2, 3, 4), 'fixed equality and palette')
    info = {e: (i, t % 2) for i, seq in enumerate(paths) for t, e in enumerate(seq)}
    e, f = [es[t] for t in free]
    i, p = info[e]
    j, q = info[f]
    need(row['free_edges'] == [e, f] and (row['i'], row['j'], row['rhs']) == (i, j, 1 ^ p ^ q), 'row fidelity')


def decode(colors, paths, phase):
    need(len(phase) == len(paths) and all(type(b) is int and b in (0, 1) for b in phase), 'phase vector')
    out = list(colors)
    for i, seq in enumerate(paths):
        for j, e in enumerate(seq):
            out[e] = 5 + (phase[i] ^ (j % 2))
    return out


def satisfies(rows, phase):
    return all(phase[q['i']] ^ phase[q['j']] == q['rhs'] for q in rows)


def signed_adjacency(k, rows):
    need(type(k) is int and 0 <= k <= 16 and len(rows) <= 4096, 'signed input bound')
    adj = [[] for _ in range(k)]
    for e, q in enumerate(rows):
        i, j, b = q['i'], q['j'], q['rhs']
        need(all(type(t) is int for t in (i, j, b)) and 0 <= i < k and 0 <= j < k and b in (0, 1), 'signed row')
        adj[i].append((j, b, e))
        adj[j].append((i, b, e))
    return adj


def forest_solution_or_core(k, rows):
    """O(k+m) traversal plus one tree-path extraction; inclusion-minimal core."""
    adj = signed_adjacency(k, rows)
    values, parent, parent_edge = [None] * k, [-1] * k, [-1] * k
    for root in range(k):
        if values[root] is not None:
            continue
        values[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v, b, e in adj[u]:
                if values[v] is None:
                    values[v], parent[v], parent_edge[v] = values[u] ^ b, u, e
                    queue.append(v)
                elif values[u] ^ values[v] != b:
                    # Shared root prefixes cancel; a set UNION would be wrong.
                    path_u, path_v = set(), set()
                    for x, path in ((u, path_u), (v, path_v)):
                        while parent[x] != -1:
                            path.add(parent_edge[x])
                            x = parent[x]
                    return None, sorted((path_u ^ path_v) | {e})
    return values, []


def shortest_core(k, rows):
    """Minimum NUMBER of row occurrences: shortest odd walk in parity cover."""
    adj = signed_adjacency(k, rows)
    best = None
    for root in range(k):
        start, goal = (root, 0), (root, 1)
        previous = {start: None}
        queue = deque([start])
        while queue and goal not in previous:
            u, bit = queue.popleft()
            for v, b, e in adj[u]:
                state = (v, bit ^ b)
                if state not in previous:
                    previous[state] = ((u, bit), e)
                    queue.append(state)
        if goal not in previous:
            continue
        trail, state = [], goal
        while state != start:
            state, e = previous[state]
            trail.append(e)
        trail.reverse()
        if best is None or len(trail) < len(best):
            best = trail
    return best


def validate_core(k, rows, core):
    need(core is not None and len(core) > 0 and len(core) == len(set(core)), 'distinct nonempty core rows')
    need(all(type(e) is int and 0 <= e < len(rows) for e in core), 'core indices')
    counts, parity = [0] * k, 0
    sub = [rows[e] for e in core]
    for q in sub:
        counts[q['i']] += 1
        counts[q['j']] += 1
        parity ^= q['rhs']
    need(all(c % 2 == 0 for c in counts) and parity == 1, 'odd Eulerian row sum')
    # Exact inclusion minimality; deletion certificates are returned explicitly.
    deletion_assignments = []
    for e in core:
        val, bad = forest_solution_or_core(k, [rows[t] for t in core if t != e])
        need(val is not None and not bad, 'core not inclusion minimal')
        deletion_assignments.append(dict(deleted_row=e, phase=val))
    return deletion_assignments


def brute_minimum(k, rows):
    """Small-input oracle by subsets and Boolean assignments; not used by extractor."""
    for size in range(1, len(rows) + 1):
        for chosen in combinations(range(len(rows)), size):
            if not any(satisfies([rows[e] for e in chosen], x) for x in product((0, 1), repeat=k)):
                return size
    return None


def forest_row_indices(k, rows):
    parent = list(range(k))
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    chosen = []
    for e, q in enumerate(rows):
        u, v = root(q['i']), root(q['j'])
        if u != v:
            parent[u] = v
            chosen.append(e)
    return chosen


def erase_to_forest(n, edges, colors, selected, fresh_color):
    """Outer operation: freely recolor selected OLD D edges; not fixed extension."""
    paths, rows = compile_rows(n, edges, colors)
    need(type(fresh_color) is int and fresh_color in (1, 2, 3, 4) and fresh_color not in colors, 'unused A color')
    need(len(selected) == len(set(selected)) and all(type(e) is int and 0 <= e < len(edges) and colors[e] != 0 for e in selected), 'selected D edges')
    ends = [set(edges[e]) for e in selected]
    for a, b in combinations(ends, 2):
        need(not a & b and not any((u in a and v in b) or (u in b and v in a) for u, v in edges), 'selected induced matching')
    hit = lambda q: bool(set(selected) & set(q['fixed_edges']))
    order = sorted(range(len(rows)), key=lambda e: (hit(rows[e]), e))
    forest = [order[t] for t in forest_row_indices(len(paths), [rows[e] for e in order])]
    forest_keys = {row_triple(rows[e]) for e in forest}
    for row in rows:
        need(row_triple(row) in forest_keys or hit(row), 'nonforest witness unhit')
    new = list(colors)
    for e in selected:
        new[e] = fresh_color
    newpaths, after = compile_rows(n, edges, new)
    need(newpaths == paths, 'unchanged U paths')
    surviving = [q for q in rows if not set(selected) & set(q['fixed_edges'])]
    need(after == surviving, 'exact witness deletion')
    phase, core = forest_solution_or_core(len(paths), after)
    need(phase is not None and not core, 'forest repair equation')
    full = decode(new, paths, phase)
    need(direct_star(n, edges, full), 'forest repair full coloring')
    return dict(selected_D_edges=selected, fresh_color=fresh_color, forest_rows=forest,
                old_row_count=len(rows), new_row_count=len(after), partial_colors=new,
                phase=phase, full_colors=full)
