"""Bounded generator-side check of the C13 height-four tree. No verifier receipt."""
import hashlib
import itertools
import json
import platform
import resource
import signal
import sys
from collections import deque
from pathlib import Path


def require(p, message):
    if not p:
        raise ValueError(message)


def edges():
    e = [['u','x',1], ['u','y',2], ['x','a',3], ['x','b',4],
         ['y','c',5], ['y','d',6]]
    table = [('a',1,2,5,6), ('b',1,3,3,5),
             ('c',2,1,3,4), ('d',2,5,5,3)]
    for i,A,B,L,R in table:
        e += [[i,'z'+i,A], ['z'+i,'l'+i,L],
              ['z'+i,'r'+i,R], [i,'w'+i,B]]
    e += [['wb','tb',2], ['wb','sb',6],
          ['wd','td',1], ['wd','sd',4]]
    return e


def adjacency(e):
    adj = {}
    seen = set()
    for k,(a,b,_) in enumerate(e):
        require(a != b and frozenset((a,b)) not in seen, 'not simple')
        seen.add(frozenset((a,b)))
        adj.setdefault(a,[]).append((b,k))
        adj.setdefault(b,[]).append((a,k))
    return adj


def violation(e):
    adj = adjacency(e)
    for a in sorted(adj):
        for (b,i),(c,j) in itertools.combinations(adj[a],2):
            if e[i][2] == e[j][2]:
                return {'kind':'incident_pair','vertices':[b,a,c], 'edges':[i,j]}
    for start in sorted(adj):
        stack = [(start, [start], [])]
        while stack:
            a,vs,es = stack.pop()
            if len(es) == 4:
                cs = [e[i][2] for i in es]
                if cs[0] == cs[2] and cs[1] == cs[3]:
                    return {'kind':'four_edge_path','vertices':vs,'edges':es}
                continue
            for b,k in adj[a]:
                if b not in vs:
                    stack.append((b,vs+[b],es+[k]))
    return None


def check_witness(e,w):
    vs,es = w['vertices'],w['edges']
    require(len(vs)==len(es)+1 and len(set(vs))==len(vs), 'non-simple path')
    for a,b,k in zip(vs,vs[1:],es):
        require(set(e[k][:2])=={a,b}, 'edge incidence mismatch')
    cs = [e[k][2] for k in es]
    if w['kind']=='incident_pair':
        require(len(es)==2 and cs[0]==cs[1], 'not improper')
    else:
        require(w['kind']=='four_edge_path' and len(es)==4, 'wrong kind')
        require(cs[0]==cs[2] and cs[1]==cs[3], 'not alternating')


def main():
    signal.alarm(10)
    resource.setrlimit(resource.RLIMIT_CPU,(10,11))
    resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
    H=edges(); G=H+[['u','v',0]]; adj=adjacency(G)
    dist={'u':0}; q=deque(['u'])
    while q:
        a=q.popleft()
        for b,_ in adj[a]:
            if b not in dist:
                dist[b]=dist[a]+1; q.append(b)
    require(len(dist)==len(adj)==28 and len(G)==27, 'wrong tree size')
    require(max(map(len,adj.values()))==3 and max(dist.values())==4, 'wrong degree/height')
    require(violation(H) is None, 'old coloring not star')
    D=list(range(6))+[6,10,14,18]
    frozen=[]
    for edge in D:
        for t in range(1,7):
            if t==H[edge][2]: continue
            changed=[x[:] for x in H]; changed[edge][2]=t
            w=violation(changed); require(w is not None, 'critical edge not frozen')
            check_witness(changed,w)
            frozen.append({'edge':edge,'new_color':t,'witness':w})
    leaf=[]
    for t in range(1,7):
        G[-1][2]=t; w=violation(G)
        require(w is not None and set(w['edges']) <= set(D+[26]), 'bad original obstruction')
        check_witness(G,w); leaf.append({'leaf_color':t,'witness':w})
    # Direct enumeration cross-check, including simultaneous leaf assignment.
    trials=0
    for edge in [-1]+list(range(len(H))):
        for t in ([0] if edge<0 else range(1,7)):
            if edge>=0 and t==H[edge][2]: continue
            for leaf_color in range(1,7):
                C=[x[:] for x in H]+[['u','v',leaf_color]]
                if edge>=0: C[edge][2]=t
                require(violation(C) is not None, 'one-edit repair found')
                trials+=1
    # b-wb:3->5, a-za:1->4, uv:3.
    final=[x[:] for x in H]+[['u','v',3]]
    for edge,t in [(13,5),(6,4)]: final[edge][2]=t
    require(violation(final) is None, 'upper witness not star')
    changed=[i for i in range(len(H)) if final[i][2]!=H[i][2]]
    require(changed==[6,13], 'wrong edit count')
    bad=[x[:] for x in final]; bad[26][2]=1
    require(violation(bad) is not None, 'mutation accepted')
    cert={'verdict':'candidate_only','edges_H':H,'new_leaf_edge':['u','v'],
          'critical_edge_indices':D,'frozen_alternatives':frozen,
          'original_leaf_obstructions':leaf,'extension':final}
    encoded=(json.dumps(cert,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    dst=Path(__file__).with_name('opg37271-c13-height-certificate.json')
    dst.write_bytes(encoded)
    result={'verdict':'candidate_only','runtime':platform.python_version(),
            'vertices_G':28,'edges_G':27,'height_from_u':4,
            'old_coloring_star':True,'frozen_alternatives_checked':len(frozen),
            'zero_or_one_edit_assignments_checked':trials,
            'two_edit_extension_checked':True,'changed_edges':changed,
            'mutation_rejected':True,'certificate_sha256':hashlib.sha256(encoded).hexdigest(),
            'limits':{'wall_seconds':10,'cpu_seconds':10,'memory_mib':256,'threads':1},
            'trusted_receipt':False}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    Path(__file__).with_name('opg37271-c13-height-result.json').write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
