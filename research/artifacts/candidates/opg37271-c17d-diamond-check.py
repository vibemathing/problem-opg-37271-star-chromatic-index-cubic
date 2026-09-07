"""Bounded generator-side audit of a diamond replacement; not a verifier receipt."""
from itertools import combinations
from pathlib import Path
import base64
import hashlib
import json
import platform
import resource
import signal
import zlib

COLORS = set(range(1, 7))
EDGES = [('a','p'), ('b','q'), ('p','r'), ('p','s'), ('q','r'), ('q','s'), ('r','s')]

def need(ok, text):
    if not ok:
        raise ValueError(text)

def star(edges, colors):
    need(len(edges) == len(colors), 'length mismatch')
    adjacency = {}
    seen = set()
    for (x,y), c in zip(edges, colors):
        need(x != y and frozenset((x,y)) not in seen, 'not simple')
        need(c in COLORS, 'palette')
        seen.add(frozenset((x,y)))
        adjacency.setdefault(x, []).append((y,c))
        adjacency.setdefault(y, []).append((x,c))
    for entries in adjacency.values():
        if len({c for _,c in entries}) != len(entries):
            return False
    # A proper two-color component is a path or an even cycle.
    # Having >=4 edges is exactly a forbidden four-edge path or cycle.
    for a,b in combinations(sorted(COLORS), 2):
        unseen = set(adjacency)
        while unseen:
            seed = min(unseen)
            unseen.remove(seed)
            stack = [seed]
            degree_sum = 0
            while stack:
                x = stack.pop()
                for y,c in adjacency[x]:
                    if c in (a,b):
                        degree_sum += 1
                        if y in unseen:
                            unseen.remove(y)
                            stack.append(y)
            if degree_sum // 2 >= 4:
                return False
    return True

def diamond(alpha, A, B):
    U, V = COLORS - {alpha} - A, COLORS - {alpha} - B
    common = min(U & V)
    left = min(U - {common})
    right = min(V - {common,left})
    middle = min(COLORS - {alpha,common,left,right})
    return [alpha,alpha,common,left,right,common,middle]

def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(15)
    resource.setrlimit(resource.RLIMIT_CPU, (15,16))
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024,)*2)
    need(star([('a','b'),('b','c'),('c','d')], [1,2,1]), 'positive path fixture')
    need(not star([('a','b'),('b','c'),('c','d'),('d','e')], [1,2,1,2]), 'negative path fixture')
    need(not star([('a','b'),('b','c'),('c','d'),('d','a')], [1,2,1,2]), 'negative cycle fixture')
    need(not star([('a','b'),('b','c')], [1,1]), 'negative properness fixture')
    records = []
    for alpha in range(1,7):
        palettes = [set(t) for n in range(3) for t in combinations(sorted(COLORS-{alpha}),n)]
        for A in palettes:
            for B in palettes:
                cs = diamond(alpha,A,B)
                need(star(EDGES,cs), 'invalid internal diamond')
                need(not A & {cs[2],cs[3]} and not B & {cs[4],cs[5]}, 'unsafe boundary')
                need(alpha not in cs[2:], 'internal cap color')
                records.append([alpha,sorted(A),sorted(B),cs])
    # Small exceptional shore with a common external neighbor, with/without a leaf.
    small_edges = [('p','r'),('p','s'),('q','r'),('q','s'),('r','s'),('a','p'),('a','q')]
    need(star(small_edges,[1,2,3,1,4,5,6]), 'common-neighbor base')
    need(star(small_edges+[('a','t')],[1,2,3,1,4,5,6,2]), 'common-neighbor leaf')
    canonical = json.dumps(records, separators=(',',':')).encode()
    normalized = json.dumps([r for r in records if r[0] == 1], separators=(',',':')).encode()
    result = {
      'verdict':'candidate_only', 'runtime':platform.python_version(),
      'method':'exact finite positive boundary audit; full graph proof is separate',
      'per_invocation_limits':{'wall_seconds':15,'cpu_soft_seconds':15,'cpu_hard_seconds':16,'address_space_mib':512,'threads':1},
      'palette_cases':len(records),'cases_per_cap_color':len(records)//6,
      'record_fields':['cap_color','outside_palette_a','outside_palette_b','colors_in_edge_order'],
      'edge_order':EDGES,
      'normalized_cap_color':1, 'stored_records':256,
      'boundary_records_zlib_base64':base64.b64encode(zlib.compress(normalized,9)).decode(),
      'uncompressed_records_bytes':len(normalized),
      'normalized_records_sha256':hashlib.sha256(normalized).hexdigest(),
      'boundary_records_sha256':hashlib.sha256(canonical).hexdigest(),
      'small_common_neighbor_colorings_checked':2,
      'mutation_fixtures_rejected':['four_edge_path','four_cycle','adjacent_equal_colors'],
      'trusted_receipt':False
    }
    data=(json.dumps(result,sort_keys=True,indent=2)+'\n').encode()
    need(len(data)<1048576,'output budget')
    target=Path(__file__).with_name('opg37271-c17d-diamond-result.json')
    target.write_bytes(data)
    print(json.dumps({'cases':len(records),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'record_sha256':result['boundary_records_sha256'],'runtime':result['runtime'],'verdict':'candidate_only'},sort_keys=True))

if __name__ == '__main__':
    main()
