# C01: exact leaf obstruction and a smallest witness

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c01-minimal-leaf-obstruction`.
Primary owner: `math-derivation`.
Target: `obligation:opg37271-leaf-extension`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Base: `d833da5eba1e9510ea968dfc05b519016b911ccd`.
Target statement SHA-256: `2dfdd4a9bbaeaf9b3d94c55e0ef98bb3d4c5f9059f4c3d05a687e3421823e852`.

This is a derivation and counterexample candidate, not a verifier receipt. No mathematical command, solver, or kernel was run for this artifact. Local text serialization and SHA-256 calculation are transport preparation only.

## 1. Frozen statement and definitions

For every finite simple undirected G with maximum degree at most three, every leaf v with neighbor u, and every star edge coloring c:E(G-v)->C={1,2,3,4,5,6}, there exists t in C such that assigning c(uv)=t, with all old edge colors unchanged, gives a star edge coloring of G.

A star edge coloring is proper and has no bichromatic simple path of four edges and no bichromatic cycle of four edges. Paths are not required to be induced. Set H=G-v. Only finite-graph-basic and finite-combinatorics are used.

The root instead asks whether every G has SOME such coloring. Its existential quantifier over old colors must not be replaced by the universal fixed-coloring quantifier above.

## 2. Claim C01-F: exact forbidden set

Write I_c(u)={c(ux):x in N_H(u)} and
B_c(u)={c(xy): u,x,y,z are pairwise distinct; ux,xy,yz are edges of H; c(ux)=c(yz)}.

Then the forbidden set for uv is exactly F_c(u)=I_c(u) union B_c(u).

Proof candidate. Colors in I violate properness. If t is in B, the simple path v,u,x,y,z has colors t,a,t,a. Conversely, if t is not in I, the extension is proper. An offending path or cycle must use the only newly colored edge uv because H was star colored. No cycle contains the pendant edge. On a simple path containing uv, v is an endpoint, so a four-edge offending path is v,u,x,y,z and properness forces its colors to alternate t,a,t,a. This gives t in B, contradiction. This covers both the path and cycle clauses.

All three old edges of such a witness lie inside the radius-three ball of u. No longer-range data is needed when old colors remain fixed.

## 3. Claim C01-S: saturation structure

Each neighbor x of u contributes at most d_H(x)-1 colors to B. Hence
|F_c(u)| <= d_H(u) + sum_{x in N_H(u)} (d_H(x)-1) <= 3 d_H(u) <= 6.

Equality F_c(u)=C forces all of the following:
(a) d_H(u)=2, with neighbors x,y and distinct root colors alpha,beta.
(b) d_H(x)=d_H(y)=3.
(c) The four spoke incidences at x,y other than ux,uy are four distinct edges with pairwise distinct colors, exactly C minus {alpha,beta}.
(d) Each spoke x-a of color p has an alpha-colored continuation a-z forming a simple u,x,a,z path; similarly each y-c has a beta continuation.

In particular xy is absent: otherwise it is counted twice among the four incidences and cannot supply four distinct colors.

## 4. Claim C01-M: lower bounds and explicit witness

Write the spokes as xa,xb,yc,yd. Their four far endpoints a,b,c,d are all distinct. Within each pair this follows from simplicity. If, for example, a=c, that vertex has two spoke edges with colors outside {alpha,beta} and also needs both an alpha edge and a beta edge by (d). These are four different incident edges, contradicting maximum degree three. None of these vertices is u,x,y. Thus H has at least seven vertices and G at least eight.

At least two further edges are required in H beyond the two roots and four spokes: an alpha support and a beta support. They are distinct and are not roots or spokes. Thus |E(G)|>=9. At equality the alpha edge must cover both a and b, and the beta edge both c and d. On eight vertices this forces precisely the witness below, up to vertex and color permutations.

Take V(G)={v,u,x,y,a,b,c,d}. The old coloring on H has exactly these edges:

| edge | color |
|---|---:|
| ux | 1 |
| uy | 2 |
| xa | 3 |
| xb | 4 |
| ab | 1 |
| yc | 5 |
| yd | 6 |
| cd | 2 |

Add just the uncolored edge uv. This is a finite simple connected subcubic graph, with eight vertices and nine edges.

### Complete check that H is star colored

Incident palettes are u:{1,2}, x:{1,3,4}, y:{2,5,6}, a:{1,3}, b:{1,4}, c:{2,5}, d:{2,6}; hence properness holds. In each two-color subgraph, every nontrivial component is a path. The maximum component edge lengths, covering all 15 pairs, are:

| pair | max length | pair | max length | pair | max length |
|---|---:|---|---:|---|---:|
| 1,2 | 2 | 1,3 | 3 | 1,4 | 3 |
| 1,5 | 1 | 1,6 | 1 | 2,3 | 1 |
| 2,4 | 1 | 2,5 | 3 | 2,6 | 3 |
| 3,4 | 2 | 3,5 | 1 | 3,6 | 1 |
| 4,5 | 1 | 4,6 | 1 | 5,6 | 2 |

For pairs 1,3 and 1,4 the length-three paths are u-x-a-b and u-x-b-a. For pairs 2,5 and 2,6 they are u-y-c-d and u-y-d-c. Pair 1,2 has the path x-u-y plus disjoint edges ab and cd. All other entries follow from the listed one-edge color classes. Thus neither a four-edge bichromatic path nor a four-cycle exists.

### Six explicit obstructions on uv

| proposed color | obstruction |
|---|---|
| 1 | adjacent to ux of color 1 |
| 2 | adjacent to uy of color 2 |
| 3 | v-u-x-a-b, colors 3,1,3,1 |
| 4 | v-u-x-b-a, colors 4,1,4,1 |
| 5 | v-u-y-c-d, colors 5,2,5,2 |
| 6 | v-u-y-d-c, colors 6,2,6,2 |

These are ordinary simple paths even though each last three vertices lie in a triangle. The witness attacks exactly the no-recoloring local statement.

## 5. Claim C01-R: one-edge repair of this witness

Change xa from 3 to 5 and assign uv color 3, leaving everything else fixed. This is proper. Colors 3,4,6 now each occur on only one edge, so they cannot participate in an alternating four-edge obstruction. The only remaining color pairs needing examination are {1,2}, {1,5}, {2,5}. Their components have length at most 2,3,3 respectively: {1,5} has u-x-a-b and the disjoint edge yc; {2,5} has u-y-c-d and the disjoint edge xa. The repaired coloring is therefore a star six-coloring of G.

Thus the graph is not a witness against the root. Zero old-edge changes fail and one old-edge change suffices for this particular coloring.

## 6. Repair proposal and limits

The smallest positive edit budget to test next is: every nonextendible (H,c,u) can be repaired by changing at most one old edge before coloring uv. This is a PROPOSAL, not an asserted lemma, not a new admitted obligation, and not implied by the example. It remains within the present target as an attack on what a corrected extension argument must allow.

The exact criterion is: find a star coloring c' of H within the allowed edit budget with F_{c'}(u) != C. Mere properness of c' is insufficient; recoloring can create paths away from u. A subsequent cycle must attack the one-edge proposal rather than repeat the zero-edit route.

This candidate alone does not establish minimum degree at least two in a hypothetical root counterexample. It only eliminates the naive argument using an arbitrary coloring of G-v without recoloring. If d_H(u)<=1 the proved counting argument does give immediate extension, but it does not cover all leaf neighbors.

## 7. Reproduction and verification request

From the edge table: check degrees and incident palettes; for each of the 15 color pairs form its connected components and count edges, rejecting a cycle or a path of at least four edges; test the six displayed extensions; repeat after the one-edge repair. Separately audit the equality and lower-bound arguments.

Requested capabilities remain kernel_check, axiom_escape_audit, statement_faithfulness, with a finite witness check as an additional useful precursor. No receipt, EvidenceLink, or obligation closure is supplied here. Both existing obligations remain open.

## 8. Checkpoint

Best verified result: none. Best verified candidate: none (no external mathematical receipt).
Best available candidate: this exact eight-vertex witness plus the forbidden-set and minimality derivations.
Failed direction: zero-edit arbitrary-coloring extension (counterexample proposal).
Next action: attack the universal one-old-edge repair proposal; examine triangle-free, bipartite, and tree witnesses.
Sources: frozen contract and graph at the base above; see `research/artifacts/source-notes/opg37271-c01-statement-scope.md`.
