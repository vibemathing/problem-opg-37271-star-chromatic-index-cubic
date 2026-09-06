# C10: six triangle-free simultaneous extremizers, all repairable with one old change

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c10-triangle-free-extremizers`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `20cea64f60aa304294bb303dea53a117174a5648`.

Manual exhaustive structural classification, not an executed graph enumeration. No mathematical program or kernel was run.

## 1. Exact class and equivalence

Consider the fixed-coloring zero-edit obstructions (G,v,u,c) of C01: G is finite, simple and subcubic, v is a leaf at u, H=G-v is star colored with C={1,...,6}, and no color on uv extends c unchanged.

This note additionally assumes that G is triangle-free and simultaneously has EXACTLY ten vertices and eleven edges. It does not classify all ten-vertex obstructions with more edges.

Equivalence means a graph isomorphism carrying the distinguished leaf and neighbor to their counterparts, together with a single bijection of the six color labels. C01 normalizes every such object as
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6,
with u,x,y,a,b,c,d distinct. Write the two remaining vertices of H as p,q. Both a,b need a color-1 support, and both c,d a color-2 support.

## 2. Completeness of the six cases

C03 proves that triangle-freeness forces four distinct support edges and at least six support vertices outside {u,x,y}. Equality in both size bounds therefore forces H to contain exactly the six displayed root/spoke edges and the four supports. The support vertex set is exactly {a,b,c,d,p,q}.

The four-edge support subgraph is properly colored with colors 1,2 and has no alternating four-edge path or cycle. Each component is a path of length at most three. Four edges on six nonisolated vertices force exactly two components, with length split either 2+2 or 3+1.

### Split 2+2

Each component contains one color-1 edge supporting one of a,b, and one color-2 edge supporting one of c,d. An edge cannot support both same-side children, since ab or cd would create a triangle. Thus each component has one left child, one right child and one outside vertex.

On the triple (a,c,p), the three possibilities are:
D: ap=1, pc=2;
L: pa=1, ac=2;
R: ac=1, cp=2.
Use (b,d,q) for the other component. Exchanging the two components is allowed, and exchanging the root sides interchanges L with R. The unordered pairs therefore have exactly four representatives DD, DL, LL, LR.

### Split 3+1

Exchange root sides if necessary so that the long path has colors 1,2,1 and the isolated edge has color 2. The isolated edge is dq after relabeling: its other endpoint cannot be c (triangle), a or b (each needs a color-1 support and would not be isolated), so it is outside.

The middle edge of the long path must meet c. Reverse the path so that c is its second vertex. Its first vertex is then a, since the first color-1 edge must support a left child. The remaining left child b is either the third or fourth vertex. This gives exactly:
I: ac=1, cb=2, bp=1, dq=2;
II: ac=1, cp=2, pb=1, dq=2.

These six representatives are distinct under the stated equivalence. For split 2+2, the count of outside middle vertices and whether child middle vertices are on the same or opposite root sides distinguish DD, DL, LL, LR. For split 3+1, the outside vertex p is respectively an endpoint or an internal vertex of the long support path. The two component-length splits themselves are invariant.

## 3. Complete edge tables and girths

In every row add the same six root/spoke edges from Section 1 and the uncolored new edge uv. The following four support edges are ALL remaining edges.

| type | support edges with old colors | girth of G |
|---|---|---:|
| DD | ap=1, pc=2, bq=1, qd=2 | 6 |
| DL | ap=1, pc=2, qb=1, bd=2 | 5 |
| LL | pa=1, ac=2, qb=1, bd=2 | 5 |
| LR | pa=1, ac=2, bd=1, dq=2 | 5 |
| I | ac=1, cb=2, bp=1, dq=2 | 4 |
| II | ac=1, cp=2, pb=1, dq=2 | 5 |

Each graph is connected, simple and subcubic. Properness follows directly from the table. For {1,2}, the two support components and the root path x-u-y all have at most three edges. Each color among 3,4,5,6 occurs just once, so a four-edge alternating path or cycle involving such a color cannot occur. Thus all six old colorings are star. Every spoke has the required support, so C01's exact forbidden set is all six colors.

The cycle-bearing cores give another check of triangle-freeness and the displayed girths. DD has three internally disjoint x-y paths of lengths 2,4,4; DL has lengths 2,3,4; LL and LR have lengths 2,3,3. I has three internally disjoint x-c paths of lengths 2,2,3. II has x-c paths of lengths 2,3,3. Remaining edges are pendant attachments. Every cycle in one of these cores is the union of two of the three paths.

In this simultaneous-extremal class DD is consequently the unique bipartite type and the unique type of girth at least six. This uniqueness assertion is not extended to larger edge counts.

## 4. Exact one-edit repair of every type

A repair must change at least one old edge, since all six types are zero-edit obstructions. The following changes suffice:

| types | old-edge change | new uv color |
|---|---|---:|
| DD, DL, LL, LR | ap: 1 -> 4 | 3 |
| I | bp: 1 -> 3 | 4 |
| II | ac: 1 -> 4 | 3 |

Here ap and pa denote the same undirected edge. We verify star validity, not just properness.

For DD and DL, after changing ap to 4 the other endpoint palettes are {3} at a and {2} at p. A bichromatic four-edge path or four-cycle with ap internal would require equal neighboring colors at both endpoints, which these disjoint palettes exclude. With ap at an end, the orientation a-p-c-y has colors 4,2,5 and already fails alternation. In the other orientation, p-a-x-b has colors 4,3,4 but b has no incident color 3. The alternative edge xu has color 1 and does not continue the alternation.

For LL and LR, p is a leaf. Starting p-a with color 4, the continuation through x can only give p-a-x-b colored 4,3,4, and again b has no color 3. Through c, the next two colors are 2,5, so the path is not alternating. These are all possibilities.

For I, p is a leaf. After bp becomes 3, the continuation p-b-x-a is colored 3,4,3, but a has no color 4. Through c, an alternating continuation would require color 3 at c, whose palette is {1,2,5}. Thus none exists.

For II, the changed edge ac has other endpoint palettes {3} and {2,5}, which exclude every internal alternating obstruction, including four-cycles. The endpoint continuation c-a-x-b has colors 4,3,4 but b has no color 3. From a-c through p, the next colors are 2,1; through y, they are 5 followed by 2 or 6. None alternates.

All changed colors are proper at their endpoints. In each row, the selected child a or b loses its unique color-1 support while every spoke remains unchanged. The exact C01 forbidden formula therefore permits the stated new uv color. Every representative has exact old-edge edit distance one.

## 5. Scope and checkpoint

Dependencies: C01's exact saturation and forbidden set, and C03's simultaneous size lower bounds. No novelty claim or external theorem is used.

The classification covers a bounded cyclic family that the tree recurrence in C08 cannot accept. It does not prove a universal one-edit lemma, contradicted by larger tree candidates, and does not support any whole-problem completion claim.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open.
Next action: reduce the size of the existing one-edit obstruction tree while preserving an exhaustive certificate that every possible single old-edge repair fails.
State: nonterminal; verdict: candidate_only.
