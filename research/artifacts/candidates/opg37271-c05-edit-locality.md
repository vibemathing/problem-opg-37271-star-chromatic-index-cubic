# C05: exact one-edit criterion, sharp radius six, and bounded-edit locality

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c05-edit-locality`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`. Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`. Target: `obligation:opg37271-leaf-extension`.
Base: `5500c6fe1f16715cff9d7bcd6b747748cda64c50`.

All proofs and witnesses below are candidates. No mathematical program, graph enumeration, solver, or kernel was executed. The root remains a separate existence question.

## 1. Setup and exact one-edit criterion

Let H=G-v be globally star edge colored with the six-color palette C, where v is a leaf adjacent to u in a finite simple subcubic G. Assume the old coloring does not extend with zero old-edge changes. Normalize C01's forced saturation data as
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6.
The seven vertices u,x,y,a,b,c,d are distinct. Each of a,b has a unique incident color-1 support and each of c,d a unique color-2 support.

Let K be the set of the four spokes xa,xb,yc,yd together with their support edges. Identical same-side support edges are included just once. Thus K has at most eight edges and is disjoint from ux,uy.

Call an old edge frozen when no nontrivial recoloring of that edge alone preserves the star property of H.

### Claim C05-F: the two root edges are always frozen

For ux, alternatives 2,3,4 violate properness. Alternative 5 creates the old path x-u-y-c-z, where cz is the color-2 support of c; its colors become 5,2,5,2. Alternative 6 uses d instead. These paths are simple: the saturation data and the full degree of x prevent the support endpoint from being x. The same argument freezes uy.

### Claim C05-E: necessary and sufficient one-edit test

There is a star coloring of G differing from the old coloring on at most one old edge if and only if at least one edge of K is not frozen.

Necessity. A final color 1 or 2 on uv would require recoloring the corresponding root edge, which is impossible by C05-F. For a final color P in {3,4,5,6}, its displayed original alternating path consists of uv, one root, its P-spoke, and that spoke's support. At least one of those three old edges must change. The root cannot change alone, so the changed edge is in K and its recoloring must leave H star.

Sufficiency. If a P-spoke is legally recolored, no spoke at x or y retains color P. The exact leaf forbidden-set formula then permits P on uv. If a support is legally recolored away from its root color, that root color disappears from the corresponding child's palette, by properness of the old coloring. The unique P-spoke therefore loses its alternating continuation. Again P is available on uv. The same reasoning works when one support serves both same-side children.

This is an equivalence, not the false universal assertion that K always contains a nonfrozen edge.

### Search size

There are at most eight edges and five different-color alternatives per edge: at most 40 raw single-edge trials. Properness reduces this to at most 28 trials. Each spoke has the root color and sibling-spoke color forbidden at its parent, leaving at most three nontrivial alternatives. Each support has at least its child's spoke color forbidden, leaving at most four. Hence 4*3+4*4=28 is a valid upper bound; shared supports only reduce it.

## 2. Claim C05-R: radius six is sufficient

A changed edge can introduce a new violation only if the violation contains that edge. Such a violation is either an incident equal-colored edge pair, a simple four-edge path, or a four-cycle. Every vertex of a violation containing an edge of K is at distance at most six from u: K's endpoints are at distance at most three, and a four-edge path has at most three further edges beyond the changed edge.

Consequently, for a globally star-colored H, the entire one-old-edge repair question is determined by the induced colored ball H[B_6(u)] and the distinguished leaf to be inserted. All 28 properness-filtered trials may be tested there. One must keep the original colors throughout this ball, not discard its outer layers.

Since d_H(u)<=2 and the graph is subcubic, B_6(u) has at most 1+2+4+8+16+32+64=127 vertices. Including v gives at most 128 vertices. This is a worst-case finite bound, not an executed classification.

The global-star assumption on the original H is essential. An arbitrary locally colored ball with no specified extension is not automatically a valid input witness.

## 3. Claim C05-S: radius five is insufficient, even on the same tree

We give two star colorings of the SAME tree H, agreeing on the induced colored radius-five ball around u, for which the one-edit answers differ. All underlying degrees, including boundary degrees, are identical. Thus six is sharp for this information model.

### Complete tree specification

Use the root/spoke skeleton from Section 1. For every i in {a,b,c,d}, add six private vertices z_i,l_i,r_i,w_i,t_i,s_i and precisely these edges:

| edge | i-z_i | z_i-l_i | z_i-r_i | i-w_i | l_i-t_i | t_i-s_i |
|---|---:|---:|---:|---:|---:|---:|
| color in c_bad | A_i | L_i | R_i | B_i | Q_i | L_i |

Parameters, including parent h_i and spoke color P_i, are:

| i | h_i | P_i | A_i | B_i | Q_i | L_i | R_i |
|---|---|---:|---:|---:|---:|---:|---:|
| a | x | 3 | 1 | 2 | 4 | 5 | 6 |
| b | x | 4 | 1 | 2 | 3 | 5 | 6 |
| c | y | 5 | 2 | 1 | 6 | 3 | 4 |
| d | y | 6 | 2 | 1 | 5 | 3 | 4 |

All named vertices are distinct and there are no further edges. H has 31 vertices and 30 edges; adding uv makes G a 32-vertex tree. The levels from u are: x,y at 1; a,b,c,d at 2; z_i,w_i at 3; l_i,r_i at 4; t_i at 5; s_i at 6.

This is a NEW outward-blocking variant of C02, not a silent revision of the C02 witness.

### The old coloring c_bad is star

Properness follows from the incident palettes. Because H is a tree, it suffices to bound all two-color path components.

For {1,2}, the components are x-u-y and z_i-i-w_i, of length two. For {3,4}, the two-edge components are a-x-b and l_i-z_i-r_i on the right side; the remaining edges are isolated. The pair {5,6} is symmetric. For one color from {1,2} and one from {3,4,5,6}, the longest components are the root-spoke-support paths u-h_i-i-z_i of length three; all other components have at most two edges. Finally, for cross pairs {3,5},{3,6},{4,5},{4,6}, the only possible longer components are z_i-l_i-t_i-s_i with colors L_i,Q_i,L_i, of length three. Other components are isolated edges. These cases cover all 15 pairs and exclude every bichromatic four-edge path.

### No one-edit repair exists for c_bad

Both roots are frozen by C05-F. A spoke of color P_i has A_i,Q_i,B_i forbidden by properness; its only nontrivial proper alternatives are L_i and R_i. These create u-h_i-i-z_i-l_i or u-h_i-i-z_i-r_i, alternating A_i with the new color. Thus each spoke is frozen.

A support i-z_i has the four distinct other incident colors P_i,B_i,L_i,R_i. Its only nontrivial proper alternative is Q_i. That recoloring creates the path i-z_i-l_i-t_i-s_i with colors Q_i,L_i,Q_i,L_i. Thus every support is frozen. C05-E excludes every one-old-edge repair, including changes far from u.

### Define c_good and check its repair

Change only t_a-s_a from 5 to 1 in c_bad, obtaining c_good. This changed edge joins levels five and six, so the induced colored ball B_5(u) is unchanged. Properness holds. Any new forbidden path would have to start at the leaf s_a and pass through t_a,l_a,z_a. Its first three edge colors are 1,4,5, which already fail alternation. There is no cycle in the tree. Hence c_good is star.

Now, starting from c_good, change a-z_a from 1 to 4. Its two endpoint sets of other incident colors are {3,2} and {5,6}, which are disjoint; this excludes an alternating four-edge path with the changed edge internally. If the changed edge is an endpoint edge, the possibilities are:
- a-z_a-l_a-t_a-s_a has colors 4,5,4,1, not alternating;
- a-z_a-r_a stops at a leaf;
- z_a-a-w_a stops at a leaf;
- z_a-a-x-b has colors 4,3,4, and b has no incident color 3 to continue.
Thus this recoloring preserves the star property. Color 1 is absent at a, so uv can receive color 3 by C01's exact criterion.

Therefore c_good admits one old-edge change, whereas c_bad does not, despite identical radius-five colored balls on the same underlying tree. Zero edits fail for both because the saturated core is unchanged. The c_bad witness also has exact edit distance two: first make the outside tail change producing c_good, then recolor a-z_a and add uv.

## 4. Exact boundary criterion for simultaneous changes

Let S be a prescribed set of old edges, T=S union {uv}, and let a proposed full coloring agree with c on E(H) minus S. It is star if and only if every properness pair and every four-edge simple path or four-cycle meeting T satisfies the star conditions.

Proof. Every constraint disjoint from T lies in H and retains its valid old colors. Every constraint meeting T is explicitly tested. These are all types of forbidden configurations.

Use L(G) for the line graph: vertices are edges of G; two are adjacent when they share an endpoint. Every edge of a four-edge path or four-cycle is within line-graph distance at most three of every specified edge of that configuration. Hence the tests above are contained in the edge neighborhood of radius three around T. This is a boundary-inclusive test, not a claim that an arbitrary recoloring of the interior preserves the exterior constraints.

## 5. Claim C05-K: finite locality for a fixed edit budget k

If any star coloring of G differs from c on at most k old edges, then there is one whose changed old edges all have line-graph distance at most 3k from uv.

Proof candidate. Among all such colorings choose one with the minimum number of changed old edges, S. Form an auxiliary graph on S union {uv}, joining two edges whenever their distance in L(G) is at most three. This auxiliary graph must be connected. Otherwise, let D be a component not containing uv and restore all edges of D to their old colors simultaneously. A newly violated properness pair, four-edge path, or four-cycle would have to meet D. It cannot meet another component of changed edges or uv, since two edges in the same constraint have line-graph distance at most three. All its edges consequently have their original colors and lie in H, contradicting that H was star. Restoration therefore gives a valid coloring with fewer changes, contradicting minimality.

A simple auxiliary path from uv to any changed edge uses at most |S| links, each of line-graph length at most three. Thus the required distance is at most 3|S|<=3k.

To decide whether a repair with budget k exists, it therefore suffices to search subsets of at most k old edges in the line-graph radius-3k neighborhood of uv, and validate them using the additional radius-three boundary from Section 4. In vertex-distance terms, the colored ball H[B_(3k+3)(u)] is sufficient. With the new leaf included it contains at most 2^(3k+4) vertices in a subcubic graph. For k=1 and k=2 this gives at most 128 and 1024 vertices, respectively.

This reduction is conditional on the given old H being globally star colored. It does not prove that a repair exists for any fixed universal k. It also does not require the individual recolorings to be valid intermediate steps: the edit budget concerns the final coloring, and the restoration argument changes a whole component simultaneously.

## 6. Dependencies, attacks, and checkpoint

Dependencies: C01's exact forbidden set and saturation description. C02 supplies an earlier one-edit obstruction, while this document supplies a different complete outward-blocking witness. No external theorem or execution is required by the proof drafts.

Adversarial checks addressed: all five alternatives for each frozen critical edge; changes outside the critical set; duplicate same-side supports; four-cycles as well as paths; identical full graph and boundary degrees in the sharpness pair; old/global versus merely local star assumptions; and simultaneous versus sequential recoloring.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open.
Best new candidates: the exact finite one-edit criterion, the sharp radius-six locality theorem, and the bounded-k connected-support reduction.
Next action: encode the sharpness pair and the bounded-edit constraints as a frozen finite verification request; compare the new source's claimed all-connected-graphs theorem with the root without importing it as a proof.
State: nonterminal; verdict: candidate_only.
