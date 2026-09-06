# C02: a tree whose fixed coloring requires exactly two old-edge edits

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c02-two-edit-tree`.
Primary owner: `math-derivation`.
Target: `obligation:opg37271-leaf-extension`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Base: `c48e8255ac91ca305e1ce9adffd4eeba89b26427`.

This is a manual finite construction and proof candidate. No mathematical program, enumeration, solver, or kernel has been executed. Hashing of its serialized text is transport preparation only.

## 1. Exact scope

C01 gave an eight-vertex obstruction to extending an arbitrary fixed star six-edge-coloring without changing old colors. It proposed, but did not assert, a repair using at most one old-edge change. This candidate attacks that proposal:

For every finite simple subcubic G, leaf v adjacent to u, and star coloring c of H=G-v with C={1,2,3,4,5,6}, is there a star coloring of G whose restriction to H differs from c on at most one edge?

We give a tree and coloring for which the answer is negative, together with a two-edge repair. The old-edge Hamming distance to an extendible star coloring is therefore exactly two for this witness. No global minimal vertex count for this property, universal two-edit bound, or root conclusion is asserted.

The only axioms used are finite-graph-basic and finite-combinatorics. Star coloring forbids bichromatic simple paths and cycles of four EDGES; paths need not be induced.

## 2. Complete graph and coloring specification

Start with vertices u,x,y,a,b,c,d and edges

| edge | ux | uy | xa | xb | yc | yd |
|---|---:|---:|---:|---:|---:|---:|
| color | 1 | 2 | 3 | 4 | 5 | 6 |

For each i in {a,b,c,d}, add six PRIVATE vertices z_i,l_i,r_i,w_i,t_i,s_i and precisely the six edges

| edge | i z_i | z_i l_i | z_i r_i | i w_i | w_i t_i | t_i s_i |
|---|---:|---:|---:|---:|---:|---:|
| color | A_i | L_i | R_i | B_i | Q_i | B_i |

The row parameters and parent h_i of i are:

| i | h_i | spoke color P_i | A_i | B_i | Q_i | L_i | R_i |
|---|---|---:|---:|---:|---:|---:|---:|
| a | x | 3 | 1 | 2 | 4 | 5 | 6 |
| b | x | 4 | 1 | 2 | 3 | 5 | 6 |
| c | y | 5 | 2 | 1 | 6 | 3 | 4 |
| d | y | 6 | 2 | 1 | 5 | 3 | 4 |

All named vertices are distinct. There are no further edges. This defines a tree H with 31 vertices and 30 edges. Add a new leaf v and the edge uv to define G, a tree with 32 vertices and 31 edges. Maximum degree is three. The initially colored graph is H; uv is initially uncolored.

## 3. Claim C02-S: the given coloring of H is star

Properness follows at u from {1,2}, at x from {1,3,4}, at y from {2,5,6}, at each i from {P_i,A_i,B_i}, at z_i from {A_i,L_i,R_i}, and at w_i,t_i from {B_i,Q_i}. All entries in each palette are distinct.

Since H is a tree, each two-color component of a proper coloring is a path. The following is a complete grouping of all 15 color pairs; every component has the indicated upper bound on its number of edges.

| pairs | maximum component length |
|---|---:|
| {1,2} | 2 |
| {3,4}, {5,6} | 2 |
| {1,3}, {1,4}, {2,5}, {2,6} | 3 |
| {1,5}, {1,6}, {2,3}, {2,4} | 3 |
| {3,5}, {3,6}, {4,5}, {4,6} | 1 |

Here is a direct audit of the grouping. For {1,2}, components are x-u-y, z_i-i-w_i, and the isolated edges t_i-s_i. For {3,4}, the only two-edge components are a-x-b and l_i-z_i-r_i for i=c,d; other edges of these colors are isolated. The pair {5,6} is symmetric. A pair consisting of a root color A_i and a same-side spoke color P_i gives the three-edge component u-h_i-i-z_i, with remaining components shorter. A pair consisting of B_i and Q_i gives the three-edge arm i-w_i-t_i-s_i; on the other child of the same parent the spoke-arm component has only two edges because P and Q are exchanged. On the opposite side a support followed by a leaf edge has only two edges. Cross pairs from {3,4} and {5,6} have no common incident vertex and hence only isolated edges. This checks every pair and excludes all bichromatic four-edge paths.

## 4. Six original extension obstructions

The exact forbidden criterion from C01 applies. Colors 1 and 2 fail properness at u. For each i, assigning uv color P_i creates the simple path v-u-h_i-i-z_i with colors P_i,A_i,P_i,A_i. Thus all six colors are forbidden.

Let D consist of the two roots ux,uy, the four spokes h_i-i, and the four support edges i-z_i. These are ten edges. Every displayed original obstruction uses only uv and edges in D.

## 5. Claim C02-F: all ten critical edges are individually frozen

'Frozen' means that changing just that old edge to a different color, leaving every other edge of H fixed, cannot produce a star coloring of H. This does not mean that no simultaneous multi-edge change is possible.

### Root ux

Changing ux to 2,3,4 violates properness. Changing it to 5 creates x-u-y-c-z_c with colors 5,2,5,2; changing it to 6 creates x-u-y-d-z_d. Thus ux is frozen. The symmetric argument freezes uy: colors 1,5,6 are improper and alternatives 3,4 create paths through x.

### Spoke h_i-i

At its two endpoints the other edges have colors A_i,Q_i,B_i. These three colors are forbidden by properness. Apart from its current color P_i, the only remaining alternatives are L_i,R_i. Recoloring to L_i makes the path u-h_i-i-z_i-l_i alternate A_i,L_i,A_i,L_i; the R_i alternative uses r_i. Thus all four spokes are frozen.

### Support i-z_i

Other incident edge colors are the four distinct colors P_i,B_i,L_i,R_i. Apart from its current color A_i, the only proper alternative is Q_i. Assigning Q_i creates z_i-i-w_i-t_i-s_i with colors Q_i,B_i,Q_i,B_i. Thus all four supports are frozen.

This classification lists all five different-color alternatives for each of the ten critical edges. It uses old H paths only, not the uncolored leaf edge.

## 6. Claim C02-L: one old-edge change cannot repair the coloring

Suppose a star coloring of G differs from c on at most one old edge. Its restriction to H is a star coloring. If the changed edge is in D, Section 5 is contradicted. If it is outside D, or no old edge changes, all six original extension obstructions from Section 4 persist unchanged. These cases exhaust all old edges, so an extendible coloring must change at least two old edges.

This argument also permits a hypothetical simultaneous coloring of uv; a bad path already inside H cannot be cured by assigning a pendant edge.

## 7. Claim C02-U: two old-edge edits suffice for this witness

Perform the following edits, in order:
1. Change w_a-t_a from 4 to 5.
2. Change a-z_a from 1 to 4.
3. Assign uv color 3.

We check that each intermediate old coloring is star.

For step 1, the recolored edge joins w_a and t_a, whose other incident edges both have color 2. The relevant {2,5} component becomes a-w_a-t_a-s_a, of length three. It cannot extend at a, whose other colors are 3 and 1, or at the leaf s_a. Any new bichromatic path would have to contain this changed edge and alternate with 2; no such four-edge path exists. Properness also holds.

For step 2, other incident colors at a are {3,2}, and at z_a are {5,6}, so color 4 is proper. These two sets are disjoint, excluding a bichromatic path that uses a-z_a as an internal edge. If a-z_a is an endpoint edge of a putative four-edge alternating path, orient it z_a-a-... . The continuation through a-w_a has colors 4,2,5 and stops being alternating immediately. The continuation through a-x has colors 4,3; the only next 4-edge is x-b, but b has no incident color 3, so it cannot extend to four edges. Orienting the endpoint edge a-z_a-... instead reaches l_a or r_a after the next edge and stops. No cycle exists in a tree. Thus step 2 preserves the star property.

Finally, the four spoke colors still are 3,4,5,6, but the vertex a has no incident color 1: its palette is now {3,4,2}. Hence the color-3 continuation from ux is destroyed, and no other spoke can forbid 3. Roots remain colors 1,2. By the exact leaf criterion, color 3 is available on uv. This proves the proposed upper bound of two edits for this particular witness.

Together Sections 6 and 7 give exact old-edge edit distance two.

## 8. Reproduction and boundaries

The two tables in Section 2 specify every vertex and colored edge without ambiguity. To reproduce: expand four rows; check degree and properness; form all 15 two-color component graphs; verify the 6 leaf obstructions and the 10 frozen-edge cases; then verify the two edits using Section 7. An optional finite checker may enumerate old-edge Hamming radius one, but no such execution is claimed here.

This is a new attack on the one-edit proposal, not a repetition of the already-obstructed zero-edit route. A universal two-edit repair remains an unproved next hypothesis. No smaller one-edit obstruction is asserted. The root's existence claim remains open; even this displayed G explicitly has a star six-coloring after the two edits.

## 9. Dependencies and checkpoint

Source dependencies: C01 at this base, in `research/artifacts/candidates/opg37271-c01-minimal-leaf-obstruction.md` (SHA-256 `15e625da8e15b145c580a3dd09e979542436acccc7483cba8fb70efef04eca33`), and the frozen contract and obligation graph. No external theorem is required.

Best verified result: none. Best verified candidate: none (no external mathematical receipt).
Best available new candidate: this 32-vertex tree and exact two-edit argument.
Failed proposed repair: universal one-old-edge change.
Open obligations: `obligation:opg37271-leaf-extension`, `obligation:opg37271-root`.
Next action: derive a correct simultaneous-recoloring criterion, and determine what local hypotheses guarantee two edits rather than assuming a universal bound.
State: nonterminal; verdict: candidate_only.
