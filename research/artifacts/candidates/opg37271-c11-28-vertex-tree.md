# C11: a 28-vertex tree with exact old-edge repair distance two

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c11-28-vertex-tree`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `31ea4b7debb2680493aa129371590bd7d074c5b6`.

This is a manual finite construction and proof candidate, not a graph-enumeration run or mathematical receipt. Local text serialization and hashing do not verify mathematics.

## 1. Claim and scope

There is a finite simple subcubic tree G, a leaf v at u, and a star edge coloring c of H=G-v with palette {1,...,6}, such that every star coloring of G differs from c on at least two old edges, and one differs on exactly two. This witness has 28 vertices and 27 edges in G, improving the 32-vertex witnesses in C02 and C05.

No global minimum-order claim or universal two-edit upper bound is made. The fixed-coloring repair problem is distinct from the root's existence question.

## 2. Complete edge specification

Begin with u,x,y,a,b,c,d and six edges:
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6.

For every i in {a,b,c,d}, add four private vertices z_i,l_i,r_i,w_i and edges
i-z_i=A_i, z_i-l_i=L_i, z_i-r_i=R_i, i-w_i=B_i,
using the table:

| i | parent | spoke P_i | A_i | B_i | L_i | R_i |
|---|---|---:|---:|---:|---:|---:|
| a | x | 3 | 1 | 2 | 5 | 6 |
| b | x | 4 | 1 | 3 | 5 | 6 |
| c | y | 5 | 2 | 1 | 3 | 4 |
| d | y | 6 | 2 | 5 | 3 | 4 |

Only for b and d add two more private vertices t_i,s_i and edges:
w_b-t_b=2, t_b-s_b=3;
w_d-t_d=1, t_d-s_d=5.

All names are distinct and there are no other edges. This defines H on 27 vertices with 26 edges. Add v and uv to obtain G on 28 vertices with 27 edges. The graph is a tree of maximum degree three. The maximum distance from u to an old vertex is five.

Compared with C02, two private tail pairs have been removed. The third colors at b,d now equal the other spoke color on their own side; the surviving tails have been changed accordingly. This is a new fully specified coloring, not deletion from C02 with the remaining colors tacitly fixed.

## 3. The old coloring is star

Properness is checked from the displayed incident palettes. On a tree, a proper coloring is star exactly when each two-color component has at most three edges.

The following list covers all 15 color pairs.

| color pairs | maximum component length in H |
|---|---:|
| {1,2} | 2 |
| {3,4}, {5,6} | 3 |
| {1,3}, {1,4}, {2,5}, {2,6} | 3 |
| {1,5}, {2,3} | 3 |
| {1,6}, {2,4} | 2 |
| {3,5}, {3,6}, {4,5}, {4,6} | 1 |

For {1,2}, the nontrivial two-edge components are x-u-y, z_a-a-w_a and z_c-c-w_c. Remaining edges of the pair are isolated.
For {3,4}, the longest component is a-x-b-w_b; the right-side z_i stars give two-edge components, and remaining edges are isolated. The {5,6} case is symmetric.
Each root-color/own-side-spoke pair has a three-edge component u-parent-i-z_i. Any other component is shorter.
For {2,3}, the three-edge component is b-w_b-t_b-s_b; w_a-a-x has length two and the right-side support/leaf components have length two. The {1,5} case is symmetric.
For {2,4}, the right-side support/leaf components have length two and the remaining components are isolated; {1,6} is symmetric.
For every cross pair between {3,4} and {5,6}, no vertex is incident to both colors, so the components are isolated edges.

Here symmetry exchanges x with y, a with c, b with d, corresponding private vertices, and color labels 1 with 2, 3 with 5, and 4 with 6. This also specifies exactly which cases were reused. The table therefore excludes every bichromatic four-edge path. There are no cycles.

## 4. Every one-old-edge repair fails

Colors 1 and 2 on uv fail properness. For each child i, assigning uv the spoke color P_i creates v-u-parent-i-z_i, alternating P_i,A_i,P_i,A_i. Thus zero edits fail.

Let D be the two root edges, the four spokes, and the four supports i-z_i. We check that all ten are individually frozen: changing that edge alone to any different color makes H fail properness or the star condition.

### Roots
For ux, alternatives 2,3,4 are improper, while 5 and 6 create x-u-y-c-z_c and x-u-y-d-z_d respectively. These paths alternate the new color with 2. The symmetric argument freezes uy.

### Left-side spokes
For xa, alternatives 1,2,4 are improper. Changing it to 5 or 6 creates u-x-a-z_a-l_a or u-x-a-z_a-r_a, alternating 1 with the new color.
For xb, alternatives 1 and 3 are improper. Alternatives 5 and 6 are blocked in the same way via z_b. The remaining alternative 2 creates x-b-w_b-t_b-s_b with colors 2,3,2,3.
The two right-side spokes are frozen by the stated symmetry.

### Left-side supports
For a-z_a, alternatives 2,3,5,6 are improper. Its only proper different-color choice is 4, which creates z_a-a-x-b-w_b with colors 4,3,4,3. The existing sibling branch replaces a private blocking tail.
For b-z_b, alternatives 3,4,5,6 are improper. The remaining choice 2 creates z_b-b-w_b-t_b-s_b with colors 2,3,2,3.
Again symmetry covers the two right-side supports.

This checks all five alternatives for every edge of D. Any final star coloring of G restricts to a star coloring of H. A single changed edge in D is impossible by the preceding cases; a change outside D preserves all six original extension obstructions. Consequently no one-old-edge repair exists, even when uv is assigned simultaneously rather than after the old change.

## 5. A two-old-edge repair

First change b-w_b from 3 to 5. The other endpoint palettes are {4,1} at b and {2} at w_b, which are disjoint, so a new alternating four-edge path cannot have the changed edge internally. The changed color is proper. For endpoint paths:
- b-w_b-t_b-s_b begins 5,2,3 and fails alternation;
- w_b-b-x begins 5,4, and x has no other color 5;
- w_b-b-z_b-l_b has colors 5,1,5 but l_b is a leaf.
The other z_b branch has color 6 and fails the required alternation. These exhaust endpoint possibilities, so the recolored H is star.

Next change a-z_a from 1 to 4. Its other endpoint palettes are {3,2} and {5,6}, still disjoint. The new color is proper. Its endpoint paths through z_a end at l_a or r_a. From z_a through a-w_a the path ends at a leaf. The only potentially alternating continuation through x is z_a-a-x-b, with colors 4,3,4, but b now has no incident color 3. Thus the second change also preserves the star property.

Finally color uv with 3. The roots still have colors 1 and 2, the four spoke colors remain 3,4,5,6, and a no longer has any incident color 1. By C01's exact radius-three forbidden-set criterion, the only potential reason to forbid 3 has disappeared. This is a star coloring of G with exactly two old-edge changes.

Together Sections 4 and 5 give the stated exact repair distance for this witness.

## 6. Reproduction, dependencies, and next question

The edge table, four repeated branches and two explicitly listed tails specify every input. Reproduce by checking all incident palettes, the 15 two-color cases, all five alternatives at each of ten critical edges, and the two displayed recolorings. No computation or package execution is asserted.

Dependencies: finite-graph-basic, finite-combinatorics, and C01's exact forbidden criterion. C02 and C05 are previous witnesses used for the size comparison, not hidden premises for the new coloring's validity. The new vertex count is an upper bound on the smallest one-edit obstruction, not a matching lower bound.

Best verified result: none. Best verified candidate: none.
Open obligations: `obligation:opg37271-leaf-extension`, `obligation:opg37271-root`.
Next action: determine whether a tree whose vertices are all within distance four of u must admit a one-old-edge repair. The present witness has height five and only gives a negative example at that height; no height-four theorem is assumed.
State: nonterminal; verdict: candidate_only.
