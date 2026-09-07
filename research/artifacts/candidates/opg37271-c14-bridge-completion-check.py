"""Finite candidate audit of palette gluing and elementary cubic completion.
No trusted mathematical receipt or repository command execution is asserted.
"""
import hashlib
import itertools
import json
import platform
import resource
import signal
from pathlib import Path


def require(p, text):
    if not p:
        raise ValueError(text)


def signatures(k):
    states = []
    for a in range(k):
        colors = [b for b in range(k) if b != a]
        for j in range(3):
            for active in itertools.combinations(colors, j):
                for lengths in itertools.product((2, 3), repeat=j):
                    ell = [1] * k
                    ell[a] = 0
                    for b, d in zip(active, lengths):
                        ell[b] = d
                    states.append((a, tuple(ell)))
    return states


def align(left, right, k):
    a, L = left
    b, R = right
    P = {c for c in range(k) if L[c] > 1}
    Q = sorted(c for c in range(k) if R[c] > 1)
    available = sorted(set(range(k)) - P - {a})
    require(len(available) >= len(Q), 'insufficient palette')
    image = {b: a}
    image.update(zip(Q, available))
    rest_domain = sorted(set(range(k)) - image.keys())
    rest_range = sorted(set(range(k)) - set(image.values()))
    image.update(zip(rest_domain, rest_range))
    return tuple(image[c] for c in range(k))


def compatible(left, right, permutation):
    a, L = left
    b, R = right
    if permutation[b] != a:
        return False
    return all(L[permutation[c]] + R[c] <= 4 for c in range(len(R)) if c != b)


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    seen = set()
    for a, b in edges:
        require(0 <= a < n and 0 <= b < n and a != b, 'invalid edge')
        key = tuple(sorted((a, b)))
        require(key not in seen, 'parallel edge')
        seen.add(key)
        adj[a].add(b)
        adj[b].add(a)
    return adj


def connected(n, edges):
    if n == 0:
        return False
    adj = adjacency(n, edges)
    seen = {0}
    todo = [0]
    while todo:
        a = todo.pop()
        for b in adj[a] - seen:
            seen.add(b)
            todo.append(b)
    return len(seen) == n


def cubic_completion(n, edges):
    initial_n, original = n, set(tuple(sorted(e)) for e in edges)
    rounds = 0
    while n and any(len(s) < 3 for s in adjacency(n, edges)):
        require(rounds < 3, 'too many rounds')
        adj = adjacency(n, edges)
        require(max(map(len, adj)) <= 3, 'not subcubic')
        deficient = [v for v in range(n) if len(adj[v]) < 3]
        edges = list(edges) + [(a+n, b+n) for a,b in edges] + [(v,v+n) for v in deficient]
        n *= 2
        rounds += 1
    require(all(len(s) == 3 for s in adjacency(n, edges)), 'not cubic')
    induced = {tuple(sorted((a,b))) for a,b in edges if a < initial_n and b < initial_n}
    require(induced == original and n <= 8*initial_n, 'embedding/size failure')
    return n, edges, rounds


def main():
    signal.alarm(15)
    resource.setrlimit(resource.RLIMIT_CPU, (15, 16))
    resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
    gluing = []
    for k in (5, 6):
        states = signatures(k)
        checked = 0
        for s in states:
            for t in states:
                pi = align(s, t, k)
                require(sorted(pi) == list(range(k)), 'not a permutation')
                require(compatible(s, t, pi), 'gluing boundary failure')
                checked += 1
        gluing.append({'palette_size':k,'states':len(states),'pairs_checked':checked})
    # Two arms of length three on each side; no stub-preserving 4-color permutation works.
    four = (0, (0, 3, 3, 1))
    trials = [(0,)+p for p in itertools.permutations((1,2,3))]
    require(all(not compatible(four, four, p) for p in trials), '4-color obstruction failed')
    counts = []
    for n in range(1, 6):
        possible = list(itertools.combinations(range(n), 2))
        checked = 0
        for mask in range(1 << len(possible)):
            E = [e for i,e in enumerate(possible) if mask >> i & 1]
            if any(len(s) > 3 for s in adjacency(n, E)):
                continue
            N, F, r = cubic_completion(n, E)
            require(r == max(3-len(s) for s in adjacency(n, E)), 'wrong round count')
            if connected(n, E):
                require(connected(N, F), 'lost connectedness')
            checked += 1
        counts.append({'order':n,'labeled_subcubic_graphs_checked':checked})
    examples = []
    for name,n,E in [('isolated_vertex',1,[]),('three_vertex_path',3,[(0,1),(1,2)]),
                     ('five_cycle',5,[(0,1),(1,2),(2,3),(3,4),(4,0)])]:
        N,F,r = cubic_completion(n,E)
        examples.append({'input_name':name,'input_vertices':n,'input_edges':E,
                         'output_vertices':N,'output_edges':F,'rounds':r})
    result = {'verdict':'candidate_only','runtime':platform.python_version(),
              'gluing_checks':gluing,'four_color_rejected_permutations':len(trials),
              'completion_checks':counts,'explicit_completions':examples,
              'limits':{'wall_seconds':15,'cpu_seconds':15,'memory_mib':256,'threads':1},
              'trusted_receipt':False,
              'scope':'Finite audit supports separately stated general proofs; no root coloring certificate.'}
    text = json.dumps(result, sort_keys=True, indent=2)+'\n'
    Path(__file__).with_name('opg37271-c14-bridge-completion-result.json').write_text(text)
    print(json.dumps({k:result[k] for k in ('verdict','runtime','gluing_checks',
          'four_color_rejected_permutations','completion_checks','trusted_receipt')}, sort_keys=True))


if __name__ == '__main__':
    main()
