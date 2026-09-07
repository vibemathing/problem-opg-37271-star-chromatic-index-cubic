"""Bounded generator-side audit of diamond-ended ladders; not a verifier receipt."""
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


LEFT = (4,2,3)
RIGHT = (3,4,2)
HEAD = (3,6,2,4,5)

def strip(t):
    need(isinstance(t,int) and t>=1, 'positive rung count')
    es=[('p','r'),('p','s'),('q','r'),('q','s'),('r','s')]
    cs=list(HEAD)
    a,b='p','q'
    for n in range(1,t+1):
        aa,bb=f'a{n}',f'b{n}'
        es += [(a,aa),(b,bb),(aa,bb)]
        cs += [LEFT[(n-1)%3],RIGHT[(n-1)%3],5 if n%2 else 6]
        a,b=aa,bb
    return es,cs,a,b

def pair_max(es,cs):
    rows=[]
    for x,y in combinations(range(1,7),2):
        adj={}
        for (a,b),c in zip(es,cs):
            if c in (x,y):
                adj.setdefault(a,[]).append(b)
                adj.setdefault(b,[]).append(a)
        unseen=set(adj); maximum=0
        while unseen:
            v=min(unseen); unseen.remove(v); q=[v]; degree=0
            while q:
                v=q.pop(); degree+=len(adj[v])
                for w in adj[v]:
                    if w in unseen: unseen.remove(w); q.append(w)
            maximum=max(maximum,degree//2)
        rows.append([x,y,maximum])
    return rows

def insertion(t,alpha,A,B):
    es,cs,a,b=strip(t)
    h0=5 if t%2 else 6
    i0,j0=LEFT[(t-1)%3],RIGHT[(t-1)%3]
    U,V=COLORS-{alpha}-A,COLORS-{alpha}-B
    h=min(U&V); i=min(U-{h}); j=min(V-{h,i})
    mapping={h0:h,i0:i,j0:j}
    for source,target in zip(sorted(set(range(2,7))-set(mapping)),sorted((COLORS-{alpha})-set(mapping.values()))):
        mapping[source]=target
    out=[mapping[c] for c in cs]
    need(alpha not in out, 'reserved color appears inside')
    need(not A&{mapping[h0],mapping[i0]} and not B&{mapping[h0],mapping[j0]}, 'boundary disjointness')
    need(star(es+[(a,'z'),(b,'w')],out+[alpha,alpha]), 'bad isolated insertion')
    return [mapping[x] for x in range(2,7)]

def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('wall budget')))
    signal.alarm(15)
    resource.setrlimit(resource.RLIMIT_CPU,(15,16))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024*1024,)*2)
    need(not star([('a','b'),('b','c'),('c','d'),('d','e')],[1,2,1,2]), 'path mutation')
    need(not star([('a','b'),('b','c'),('c','d'),('d','a')],[1,2,1,2]), 'cycle mutation')
    need(not star([('a','b'),('b','c')],[1,1]), 'properness mutation')
    fixtures=[]
    for t in range(1,25):
        es,cs,a,b=strip(t)
        ell,mu=LEFT[(t-1)%3],RIGHT[(t-1)%3]
        gamma=2 if t==1 else mu
        variants=[(es,cs), (es+[(a,'z')],cs+[1]),
                  (es+[(a,'z'),(b,'z')],cs+[1,ell]),
                  (es+[(a,'z'),(b,'z'),('z','leaf')],cs+[1,ell,gamma])]
        for e,c in variants: need(star(e,c),f'end fixture t={t}')
        fixtures.append([t,4+2*t,len(es),ell,mu,gamma])
    es,cs,a,b=strip(1)
    need(not star(es+[(a,'z'),(b,'z'),('z','leaf')],cs+[1,4,3]), 'one-rung naive closing mutation')
    records=[]
    for alpha in range(1,7):
        palettes=[set(xs) for n in range(3) for xs in combinations(sorted(COLORS-{alpha}),n)]
        for A in palettes:
            for B in palettes:
                mapping=insertion(4,alpha,A,B)
                records.append([alpha,sorted(A),sorted(B),mapping])
    # Explicitly test all six periodic terminal triples too, in normalized colors.
    residues=[]
    for t in range(1,7):
        for A in ({2,3},{2,4},{4,5}):
            for B in ({2,3},{2,4},{4,5}):
                residues.append([t,sorted(A),sorted(B),insertion(t,1,A,B)])
    normalized=json.dumps([r for r in records if r[0]==1],separators=(',',':')).encode()
    result={
      'verdict':'candidate_only','runtime':platform.python_version(),'trusted_receipt':False,
      'limits':{'wall_seconds':15,'cpu_soft_seconds':15,'cpu_hard_seconds':16,'address_space_mib':512,'threads':1},
      'head_edges':[list(x) for x in strip(1)[0][:5]],'head_colors':list(HEAD),
      'left_rail_period':list(LEFT),'right_rail_period':list(RIGHT),'rung_period':[5,6],
      'head_fixture_rungs':4,'head_fixture_two_color_component_maxima':pair_max(*strip(4)[:2]),
      'end_fixture_fields':['rungs','vertices','edges','left_color','right_color','closing_leaf_color'],
      'end_fixtures':fixtures,'end_colorings_checked':4*len(fixtures),
      'boundary_cases':len(records),'normalized_records':256,
      'normalized_record_fields':['alpha','outside_A','outside_B','images_of_2_through_6'],
      'normalized_recipe_rows_stored':False,
      'normalized_recipe_specification':'All alpha=1 ordered A,B subsets of size at most two; use the complete insertion(4,alpha,A,B) function in the companion source.',
      'normalized_records_sha256':hashlib.sha256(normalized).hexdigest(),
      'all_records_sha256':hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),
      'periodic_boundary_smoke_cases':len(residues),
      'mutation_fixtures_rejected':['four_edge_path','four_cycle','adjacent_equal_colors','one_rung_naive_closing_color'],
      'universal_claim_scope':'The finite prefix audit is not an all-length proof; the accompanying periodic path argument and outside-component proof are essential.'
    }
    data=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    need(len(data)<1048576,'output budget')
    Path(__file__).with_name('opg37271-c18d-diamond-chain-result.json').write_bytes(data)
    print(json.dumps({'boundary_cases':len(records),'end_colorings':4*len(fixtures),'head_maxima':result['head_fixture_two_color_component_maxima'],'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'runtime':platform.python_version(),'verdict':'candidate_only'},sort_keys=True))

if __name__=='__main__':
    main()
