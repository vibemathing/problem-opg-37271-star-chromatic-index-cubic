# C13: the sharp height boundary for a uniform one-edit tree repair

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `b1af2ef058f5bca3e81fa2b19fe822f72a107763`.

## 1. Scope

Let G be a finite simple subcubic TREE, v a leaf adjacent to u, and c a star edge coloring of H=G-v with available colors {1,...,6}. Define height as max distance from u over ALL vertices of G, not distance from v and not an arbitrarily rerooted height. An old-edge repair counts the number of edges of H whose FINAL colors change; it does not require valid intermediate single-edge steps.

Claim candidates:
- If height <=3, at most one old-edge change always suffices.
- A height-four, 28-vertex tree and old coloring can require exactly two old-edge changes.

Thus height four is the first possible height at which the uniform one-edit assertion fails. The order 28 is not claimed to be smallest. These are fixed-coloring statements, not root counterexamples or a universal two-edit bound. C12R already supplies a different tree attacking the universal two-edit assertion.

## 2. Height at most three: proof candidate

If the exact C01 forbidden set is not saturated, extend without changing anything. Otherwise normalize as in C01:
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6,
with distinct named vertices, and unique color-1 supports at a,b and color-2 supports at c,d. In a tree these supports go from depth-two vertices to depth-three vertices. Under height <=3, their far endpoints are leaves.

For completeness, the applicable C03 terminal-support argument is as follows. Denote the two supports aa'=1 and bb'=1, with a',b' leaves. If b has no incident color 3, consider recoloring aa'. After deleting a', the root a has at most two incident colors. The neighbor x contributes no extra forbidden color: the middle-color-1 continuation a-x-u-y has colors 3,1,2, and the middle-color-4 continuation cannot finish with 3 at b. The only other neighbor of a contributes at most two further forbidden colors. Therefore at most four colors are forbidden, leaving a legal color different from the current 1.

If b does have incident color 3, instead recolor bb'. At b after deleting b', the incident colors are 4,3. Through x the middle color 1 does not alternate through u-y, and the only other candidate middle color 3 is already forbidden by incidence. The other neighbor of b contributes at most two more colors. Again at least two colors are legal, one being the current 1, so a different one can be chosen.

The pendant-edge criterion checks the ENTIRE recolored H, including all potential paths through the edited edge. Recoloring aa' removes color 1 at a, freeing color 3 on uv; recoloring bb' similarly frees color 4. Uniqueness of the four differently colored spokes excludes a second witness forbidding the freed color. This proves the candidate bound for every old coloring and every such tree. The twelve-vertex height-three witness of C03 needs one change, so zero cannot replace one here.

The invariant is terminal support geometry, not a radius-three-only test for arbitrary edits. Height four can place new constraints beyond a support, as the next construction shows.

## 3. Explicit height-four tree

All names below are distinct. Start with edges

| edge | ux | uy | xa | xb | yc | yd |
|---|---:|---:|---:|---:|---:|---:|
| old color | 1 | 2 | 3 | 4 | 5 | 6 |

For every i in {a,b,c,d}, add four private vertices z_i,l_i,r_i,w_i and the four edges

| edge | i-z_i | z_i-l_i | z_i-r_i | i-w_i |
|---|---:|---:|---:|---:|
| color | A_i | L_i | R_i | B_i |

using

| i | A_i | L_i | R_i | B_i |
|---|---:|---:|---:|---:|
| a | 1 | 5 | 6 | 2 |
| b | 1 | 3 | 5 | 3 |
| c | 2 | 3 | 4 | 1 |
| d | 2 | 5 | 3 | 5 |

Add four more private vertices t_b,s_b,t_d,s_d with edges
w_b-t_b=2, w_b-s_b=6, w_d-t_d=1, w_d-s_d=4.
Finally add v and uncolored uv. No further edges occur.

There are 28 vertices, 27 edges, and maximum degree three. The z_i,w_i lie at distance three from u; every remaining added vertex lies at distance four. All additions are new leaves or pendant forks on a tree, so G is a tree. This differs from C11 in both certain fork colors and the placement of the four tail edges: they are now sibling leaves at w_b,w_d, not paths extending to height five.

## 4. Old star coloring and original obstructions

Properness is checked from the displayed distinct incident palettes; notably the palettes at b,z_b,w_b are {4,1,3}, {1,3,5}, {3,2,6}, respectively. Repetition of 3 at separated vertices is allowed. The symmetric c,d side is obtained by interchanging 1<->2, 3<->5, 4<->6 and x<->y, a<->c, b<->d.

For a proper coloring of a tree, each two-color component is a path. The complete maximum component edge lengths are given below, together with those for the final repair of Section 6. Both columns can be checked directly from the edge tables.

| colors | old H | repaired G |
|---|---:|---:|
| 1,2 | 2 | 2 |
| 1,3 | 3 | 3 |
| 1,4 | 3 | 2 |
| 1,5 | 2 | 3 |
| 1,6 | 2 | 2 |
| 2,3 | 2 | 2 |
| 2,4 | 2 | 2 |
| 2,5 | 3 | 3 |
| 2,6 | 3 | 3 |
| 3,4 | 3 | 3 |
| 3,5 | 2 | 2 |
| 3,6 | 2 | 2 |
| 4,5 | 2 | 2 |
| 4,6 | 1 | 1 |
| 5,6 | 3 | 3 |

Thus H is star colored. Colors 1,2 on uv fail properness. Colors 3,4,5,6 respectively give the alternating paths v-u-x-a-z_a, v-u-x-b-z_b, v-u-y-c-z_c, v-u-y-d-z_d. Every original obstruction lies in uv together with the ten edges consisting of the two roots, four spokes and four supports.

## 5. All ten critical edges are individually frozen

Here frozen means that changing just this old edge to a different color, leaving all other old edges fixed, cannot give a star coloring of H. It does not forbid simultaneous changes.

The following table exhausts all five different-color choices for ux,xa,xb,a-z_a,b-z_b. The palette/vertex symmetry stated above covers uy,yc,yd,c-z_c,d-z_d, so all 50 alternatives are accounted for.

| edited edge | colors failing properness | remaining alternatives and old-H witness |
|---|---|---|
| ux (old 1) | 2,3,4 | 5: x-u-y-c-z_c; 6: x-u-y-d-z_d |
| xa (old 3) | 1,2,4 | 5: u-x-a-z_a-l_a; 6: u-x-a-z_a-r_a |
| xb (old 4) | 1,3 | 2: y-u-x-b-z_b; 5: u-x-b-z_b-r_b; 6: a-x-b-w_b-s_b |
| a-z_a (old 1) | 2,3,5,6 | 4: z_a-a-x-b-w_b |
| b-z_b (old 1) | 3,4,5 | 2: t_b-w_b-b-z_b-l_b; 6: s_b-w_b-b-z_b-l_b |

Every listed witness is a simple four-edge alternating path in H after the indicated single change. In particular, the possibility of recoloring xb with the opposite root color 2 is blocked by y-u-x-b-z_b, rather than needing an additional deep branch.

Suppose an extension changed at most one old edge. If that edge is critical, the restriction to H contradicts this table. If it is not critical, all six original leaf obstructions persist. No change at all is already excluded. This proves the one-edit lower bound without extrapolating a small-instance search.

## 6. Exactly two changes suffice

Simultaneously set ux:1->3 and xa:3->5, then set uv=1. All other old colors stay fixed. The final palettes are proper, and the last column in Section 4 verifies every two-color component. For additional direct inspection, the only length-three components in the repaired graph are:

| color pair | length-three components |
|---|---|
| 1,3 | l_b-z_b-b-w_b |
| 1,5 | x-a-z_a-l_a |
| 2,5 | u-y-c-z_c; l_d-z_d-d-w_d |
| 2,6 | u-y-d-z_d |
| 3,4 | u-x-b-w_b |
| 5,6 | c-y-d-w_d |

All other components have at most two edges. This gives the upper bound two. The changes are simultaneous final-color changes; neither chosen ordering is asserted to preserve a star coloring at every intermediate stage.

## 7. Bounded executable audit

`opg37271-c13-height-check.py` is a standalone standard-library generator-side check. It constructs exactly the above tree, checks the height and old coloring, exhausts the 50 critical-edge alternatives, and directly checks all 6*(1+26*5)=786 zero-or-one-edit assignments. It then checks the explicit two-edit extension and both pair tables. Observed output is saved in `opg37271-c13-height-check-result.json`.

Actual runtime: CPython 3.13.5. Limits: wall 20 seconds, CPU soft/hard 20/21 seconds, address space 256 MiB. No solver, GPU, randomness, repository script, or kernel was used. A separate same-domain C08 dynamic-programming check also returned optimum two; the short exhaustive check and proof above do not rely on that DP. The report is a generator output, not a mathematical verifier receipt.

Reproduce from the repository root:
`python research/artifacts/candidates/opg37271-c13-height-check.py`.

## 8. Dependencies and checkpoint

C01's saturation derivation and C03's terminal-support lemma at the base above are the mathematical dependencies. C11 is the construction comparator, not an unproved minimality premise. All graph identities, color conventions, and height quantifiers are explicit.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open. No global minimal-order assertion or root implication from this repair obstruction is made.

Next action: prove root-faithful bridge gluing and cubic completion; strengthen hypothetical vertex-minimal counterexample structure without assuming a fixed deletion coloring or claiming that all leaf vertices are reducible.
