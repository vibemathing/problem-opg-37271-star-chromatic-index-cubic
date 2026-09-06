# C03: sharp girth-class sizes and a terminal-support repair lemma

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c03-girth-terminal-repair`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Target: `obligation:opg37271-leaf-extension`.
Base: `a5830873b03169b7bc17636ae6e1070a97f7bfc7`.

Manual finite-graph derivation, not an executed enumeration or verifier receipt. All claims below are candidates. No mathematical program or kernel was run.

## 1. Definitions and reused saturation statement

A zero-edit obstruction is (G,v,u,c), where G is finite, simple, subcubic, v is a leaf adjacent to u, H=G-v has a star edge coloring c with available palette C={1,...,6}, and no color on uv extends c unchanged. Star excludes bichromatic simple paths and cycles of four edges. Give forests girth infinity.

C01 derived the exact leaf forbidden set and the following forced normalization for every obstruction:
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6;
u,x,y,a,b,c,d are distinct; x,y have degree three; each of a,b has an incident support edge of color 1, and each of c,d an incident support edge of color 2. Properness makes each required support unique at its child endpoint. An edge may support both same-side children only by joining those children.

The root remains the separate existence question. Changing its quantifiers to universal preservation of a given coloring is not allowed.

## 2. Claim C03-G: sharp order bounds for zero-edit obstructions

| restriction on G | smallest possible vertex count | smallest possible edge count |
|---|---:|---:|
| none beyond simple subcubic | 8 | 9 |
| triangle-free | 10 | 11 |
| bipartite | 10 | 11 |
| girth at least 5 or at least 6 | 10 | 11 |
| girth at least 7 | 12 | 11 |
| tree | 12 | 11 |

Every row's two minima are attained simultaneously. The unrestricted row is C01. These are minima for a fixed-coloring extension obstruction, not for the star chromatic index being greater than six.

### Triangle-free lower bound

The support for a and that for b are different edges: a shared edge would be ab and form triangle xab. Likewise the two color-2 supports are different. Thus four distinct support edges are needed, in addition to the six root/spoke edges and uv, giving at least eleven edges in G.

Consider the subgraph consisting of just those four support edges. It is a proper two-colored subgraph of H, hence each component is a path of at most three edges: a cycle of length four or a longer path is forbidden, and a longer two-colored cycle also contains a forbidden four-edge path. With four edges it therefore has at least two components and at least six vertices. None of these vertices is u,x,y, whose relevant color incidences or degrees are already occupied. Together with u,x,y and v this gives at least ten vertices.

This argument applies to every triangle-free graph, not just bipartite graphs.

### Girth at least seven lower bound

The seven-vertex root/spoke skeleton is a tree. A support from a child to another child would close a triangle (same parent) or a five-cycle (opposite parent), so its other endpoint must be outside this skeleton. Two same-color supports cannot share an outside endpoint, by properness. Two opposite-color supports sharing an outside endpoint would close a six-cycle, since their child endpoints are distance four apart in the skeleton. Thus all four outside support endpoints are distinct. H has at least eleven vertices and G at least twelve.

Trees are included, and need at least eleven edges by the preceding argument.

## 3. Explicit sharp witnesses

### Ten-vertex bipartite witness

Let H have vertices u,x,y,a,b,c,d,p,q, all distinct, with exactly the following ten colored edges:

| edge | ux | uy | xa | xb | yc | yd | ap | bq | cp | dq |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| color | 1 | 2 | 3 | 4 | 5 | 6 | 1 | 1 | 2 | 2 |

Add the new leaf v at u to obtain G. Its bipartition is {u,a,b,c,d} and {v,x,y,p,q}. H consists of the three internally disjoint x-y paths x-u-y, x-a-p-c-y, and x-b-q-d-y, of lengths 2,4,4. Consequently its cycles have lengths 6,6,8 and its girth is six.

The coloring is proper. For colors {1,2}, the components are x-u-y, a-p-c, b-q-d, all of length two. Colors 3,4,5,6 each appear on one edge. For a pair consisting of one of these colors P and either 1 or 2, a four-edge alternating path would require two P-edges, which do not exist. Pairs among {3,4,5,6} are equally harmless. Thus H is star colored.

Colors 1 and 2 on uv are improper. Colors 3,4,5,6 respectively create:
v-u-x-a-p, v-u-x-b-q, v-u-y-c-p, v-u-y-d-q.
Each path alternates its proposed color with the corresponding root color. This achieves ten vertices and eleven edges in G.

### Twelve-vertex tree witness

Use the same root/spoke skeleton, but make four private new leaves a',b',c',d' and support edges aa'=1, bb'=1, cc'=2, dd'=2. Add v at u. All vertices are distinct and there are no other edges.

Then G is a twelve-vertex, eleven-edge tree. In H the {1,2} components are x-u-y and four isolated support edges; colors 3,4,5,6 again occur once each. Thus H is star. The same four displayed obstruction paths use the appropriate private support leaf as the last vertex. This attains the girth-at-least-seven and tree rows, with girth infinity by convention.

## 4. Claim C03-R: a valid one-edit repair under terminal supports

Lemma candidate. In any normalized saturated obstruction, suppose the two color-1 supports at a and b are a-a' and b-b', where a' and b' are leaves of H. There is a star six-coloring of G obtained by changing just one of these two support-edge colors and then coloring uv. All other old edges are preserved.

There is an analogous statement for the color-2 side. No restriction is imposed on the rest of H. This is an explicit sufficient local hypothesis; it is not asserted to be the unique or logically weakest possible hypothesis among all formulations.

### Proof by two cases

For a pendant support a-a', delete a' and use the exact forbidden criterion from C01 at a to test new colors. The current color 1 is legal because the old H is star.

Case A: vertex b has no incident color 3. Through neighbor x, a three-edge alternating continuation starting at a cannot use middle color 1, since a-x-u-y has colors 3,1,2. It also cannot use middle color 4, because b has no color 3. These are x's only two possibilities. Besides ax there is at most one other edge a-w, and w contributes at most two middle colors. Including the at most two incident colors at a after deleting a', the forbidden set has size at most four. At least two colors remain available, including 1. Choose an available t different from 1 and recolor a-a' with t.

Case B: vertex b has incident color 3. After deleting b', the two incident colors at b are 4 and 3. Through neighbor x, middle color 1 again cannot contribute: b-x-u-y has colors 4,1,2. The only other possible middle color through x is 3, which is already an incident forbidden color at b. The other neighbor of b contributes at most two further middle colors. Again the forbidden set has size at most four. Choose an available t different from 1 and recolor b-b' with t.

In either case the pendant-edge criterion proves that the recolored H remains star, not merely proper. In Case A, color 1 has disappeared from a's palette, so the unique color-3 spoke no longer has its required color-1 continuation. No other spoke can forbid 3. The exact leaf criterion therefore permits color 3 on uv. Case B similarly permits color 4.

This proves the candidate lemma without a claim that arbitrary one-edge repair always works. C02's counterexample does not satisfy the hypothesis: all four support endpoints z_i there have degree three, not one.

## 5. What this does and does not repair

The smallest tree witness in Section 3 satisfies the terminal-support hypothesis and therefore has a one-edit repair. One explicit choice is aa':1->4, followed by uv=3. Its possible alternating continuation through a-x-b stops because b has no color 3.

The ten-vertex bipartite witness does not have terminal supports, but ap:1->4 followed by uv=3 is also directly valid: other colors at a and p are respectively 3 and 2, excluding an internal alternating obstruction; the endpoint continuation p-a-x-b has colors 4,3,4 and cannot take a color-3 edge at b; the other orientation a-p-c-y has colors 4,2,5 and already fails alternation.

For induction, the lemma allows removal and reinsertion of v under the stated support-leaf hypothesis for the chosen coloring of H. It does not establish minimum degree two for every hypothetical root counterexample. A general argument must still handle saturated neighborhoods lacking these terminal supports, such as C02.

## 6. Dependencies, reproduction, and checkpoint

Dependencies: C01's exact forbidden set and saturation argument at this base; C02 is used only as an adversarial scope comparison. No external theorem is needed.

Reproduce the lower bounds by inspecting the four support edges, not by extrapolating from enumerations. Check the two explicit edge tables and all two-color components. For the positive lemma, check both color-3-at-b cases and the fact that the old color 1 remains available before recoloring.

Best verified result: none. Best verified candidate: none. No external mathematical receipt.
Open obligations: `obligation:opg37271-leaf-extension`, `obligation:opg37271-root`.
Next action: formulate an exact finite boundary test for simultaneous recolorings, preserving all paths that cross the boundary; avoid assuming a universal two-edit bound.
State: nonterminal; verdict: candidate_only.
