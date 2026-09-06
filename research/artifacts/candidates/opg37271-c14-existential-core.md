# C14: existential bridge gluing, cubic completion, and a two-connected core

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base revision: `d8b2685cc6becd6087335a6c51b944a55f1e6bd1`.

This cycle records what a correct leaf/root reduction may assert after fixed-coloring repair obstructions. The root and leaf obligations remain open. All universal arguments below are proof candidates, not admitted Results; finite checks are explicitly scoped. No novelty claim is made.

## 1. Frozen objects and quantifiers

Graphs are finite, simple and undirected. A star edge coloring is proper and has no two-colored simple path of four edges or cycle of four edges. Paths need not be induced. Only finite-graph-basic and finite-combinatorics are used.

Write P_k(G) for the EXISTENCE of a star edge coloring of G with colors in [k]. In Sections 2, 4 and 6, colorings of smaller graphs are allowed to be chosen and relabeled; their restrictions are not universally frozen across a whole induction. For the conditional structural statements, G is a hypothetical vertex-minimal graph with maximum degree three and not P_6(G): every smaller graph in the same class has P_6. Its existence is not asserted.

## 2. Bridge gluing for k>=5

Let uv be a bridge of a subcubic graph G, with components A containing u and B containing v after deleting uv. Form A+ by adding one new leaf at u, and B+ by adding one new leaf at v. If P_k(A+) and P_k(B+) for k>=5, then P_k(G).

Proof candidate. Take arbitrary witness colorings of the two augmented pieces. Relabel the entire B+ palette so that the two virtual pendant edges have the same color a. Let U be the remaining incident palette at u in A, and V the remaining incident palette at v in B; both have size at most two and avoid a. There is a permutation of the k-1 other colors sending V into [k] minus (U union {a}), since the latter has at least k-3>=2 colors. Extend that injection to a permutation, fixing a. Apply it to all edges of B+.

Delete the two virtual leaves and replace their stem edges by uv colored a. Properness holds. A new bad cycle cannot use a bridge. A bad four-edge path using uv as an end edge would already occur in one of the augmented pieces, with its virtual leaf replacing the opposite endpoint. A bad path using uv internally has, immediately before and after uv, edges of the same other color. This would belong to U intersect V, now empty. These exhaust all paths using uv. Hence the glued coloring is star.

This proves a gluing lemma about independently CHOSEN witnesses, using a whole-piece color permutation. It is not an extension lemma for an arbitrary already colored G-uv. It also makes no claim about two-edge cuts.

If G is vertex-minimal as above and both |A|,|B|>=2, then |A+|,|B+|<|G|, so both are colorable by minimality, contradicting the lemma. Consequently every bridge of such a G is pendant. A bridge incident with a leaf is not excluded by this argument because one augmented piece may have |G| vertices.

## 3. Two genuine degree-two reductions

### 3a. A degree-two vertex on a triangle

Let x have precisely the neighbors z,w, where zw is an edge. Every star six-coloring of H=G-x extends to G by coloring xz and xw; no old edge changes are needed.

To see this, put a=c(zw). Vertex z has at most one other neighbor p in H; denote its edge color by b and the palette at p by P. If absent, set P empty and b=0, a marker not in the color set. Similarly define q,c,Q at w (the symbol c in this paragraph is the color of wq). A nonempty P contains b and has size at most three; a nonempty Q contains c and has size at most three. The vertices p,q may coincide. Neither is x,z,w.

The following conditions on alpha=c(xz), beta=c(xw) suffice:

    alpha not in P union {a,c};
    beta not in Q union {a,alpha};
    beta != b OR a not in P.

They imply properness. An offending path with only one new edge has that edge at an endpoint. Paths starting x-z-p are stopped by alpha not in P; those starting x-z-w-q are stopped by alpha!=c. Paths starting x-w-q are stopped by beta not in Q. The only remaining endpoint type x-w-z-p-r would require beta=b and c(pr)=a in P, excluded by the third guard.

A four-edge path using both new edges contains z-x-w. It either extends one edge on each side, requiring alpha=c, or two edges on one side, requiring alpha=c or alpha in P. All are excluded. A new four-cycle has the form x-z-p-w-x with p=q and would require alpha=c. This also covers coincident external neighbors without inventing a tree assumption.

The guards are satisfiable for every permissible palette:
- If a is not in P, choose alpha outside P union {a,c}, then beta outside Q union {a,c,alpha}. Each union has at most five actual colors: if q exists then c is already in Q, and if it does not then Q is empty.
- If a is in P, choose beta outside Q union {a,b}, then alpha outside P union {c,beta}. Each union again has at most five colors, and beta!=b supplies the third guard.

Thus a vertex-minimal root counterexample has no degree-two vertex on a triangle. The six-color critical-graph exclusion has relevant prior art in Lei--Shi--Song, Lemma 3.2(a); the complete simple-graph extension argument is supplied here rather than importing an unspecified criticality premise.

### 3b. A degree-two vertex with two low-degree neighbors

Suppose x has neighbors z,w and both have degree at most two in G. If zw is an edge, the connected component is a triangle and is immediately colorable; otherwise z,w are nonadjacent. In H=G-x, let zz' and ww' be their possible remaining edges, with colors b,c. Let P,Q be the palettes at z',w', taking them empty and the missing colors zero when an edge is absent.

Choose alpha outside P union {c}, and beta outside Q union {alpha}. At most four actual colors are excluded in either choice, so five available colors already suffice. Put xz=alpha, xw=beta. A bad four-edge path using only one new edge must start at x and is stopped by alpha not in P or beta not in Q. One using both new edges either requires alpha=c, or requires an alpha-colored continuation incident with z'; both are excluded. The possible four-cycle when z'=w' likewise requires alpha=c. Properness follows because b is in P and c is in Q whenever those colors exist.

Hence the induced subgraph on degree-two vertices of a vertex-minimal root counterexample has maximum degree one. This is compatible with, and not claimed novel over, the k=6 specialization of Lei--Shi--Song Lemma 3.2(b).

## 4. Explicit cubic completion: an equivalence of universal questions

For any nonempty finite simple subcubic graph F on n vertices, construct a simple cubic graph K on 4n vertices containing four induced copies of F.

Vertices are (x,i) with x in V(F), i in {0,1,2,3}. For each edge xy of F, add (x,i)(y,i) for all four i. At each x let d=3-degree_F(x). Among its four copies add a fixed d-regular simple graph J_d on the four indices:

    J_0 = empty;
    J_1 = {01,23};
    J_2 = {01,12,23,30};
    J_3 = K_4.

All added fiber edges have identical first coordinate and different second coordinates; all copied edges have different first coordinates and identical second coordinate. Thus these sets do not overlap, and no loops or repeated edges occur. Every vertex has degree degree_F(x)+d=3. Fixing one index i gives an induced copy of F. Restriction of a star coloring to any subgraph remains star, since each forbidden path/cycle of that subgraph is also present in the supergraph.

It follows that the frozen root is equivalent to the universal six-color assertion for finite SIMPLE CUBIC graphs. The forward direction is specialization; the reverse is completion followed by restriction. Disconnected cubic graphs can be handled componentwise using the same palette, so connected cubic graphs also suffice. The empty graph is trivial. Any actual subcubic obstruction would transfer to a cubic one with at most four times as many vertices, but no bounded search range follows because n is unknown.

The completion need not be connected, bridgeless, triangle-free, planar, or girth-preserving. It does NOT prove that a vertex-minimal subcubic counterexample is cubic. Confusing these two statements would repeat the quantifier error of the original leaf route.

## 5. A self-contained global four-color template for trees

This known type of positive result is included to demonstrate a fresh-coloring invariant, not as a claimed discovery. Let Q have bipartition {L_i:i in GF(4)} and {R_j:j in GF(4)}, with edges L_i R_j exactly when i!=j. Identify GF(4) with {0,1,2,3}, addition XOR, and multiplication by an element theta not in {0,1} given by [0,2,3,1]. Color L_i R_j by i+theta*j (then label the four field elements by colors 1,...,4).

The coloring is proper because both affine maps in i or j are injective. An alternating four-edge simple path L_i-R_j-L_k-R_l-L_m would imply i+k=theta*(j+l)=k+m, forcing i=m; the symmetric orientation gives the same contradiction. On a four-cycle L_i-R_j-L_k-R_l-L_i, all four cross inequalities mean {i,k} and {j,l} partition GF(4). Hence their nonzero sums are equal, say d; alternation would require d=theta*d, impossible. So Q is star four-colored.

Map an arbitrary subcubic tree into Q locally injectively. Choose the image of a root; send its at most three children to distinct neighbors. Recursively, a nonroot vertex has at most two children and its image has exactly two neighbors other than the parent's image, so extend the map to those children injectively. Pull back the edge colors. They are proper by local injectivity. A simple four-edge path maps to a nonbacktracking four-edge walk in the bipartite simple graph Q. Such a walk is either a simple four-edge path or a four-cycle: an internal repeat would force immediate backtracking or a triangle. Both types are non-bichromatic in Q. Thus every finite subcubic tree has a fresh star four-coloring.

For the C12R tree, the saved program produces the full four-color assignment and vertex map. It changes 49 old edges. This is not an optimal-edit claim; it shows concretely why a lower bound of three on fixed-old-color repair says nothing against the root existence statement.

## 6. The core of a hypothetical vertex-minimal counterexample

Let G satisfy the conditional minimality hypothesis of Section 1. Then G is connected and has no isolated vertex, since components color separately and an isolated vertex needs no edge color. Every leaf neighbor has degree three: otherwise C01's exact leaf forbidden count is at most three. There is at most one leaf at each neighbor. In fact, restoring one of two leaves at the same vertex leaves another degree-one neighbor, giving a forbidden bound at most four.

Let L be the set of all leaves of G, and T=G-L, deleting them simultaneously rather than repeatedly pruning. T is connected. A former leaf neighbor loses exactly one edge from degree three; other retained vertices lose none and already have degree at least two. Hence minimum degree of T is at least two, and |T|>=3. A bridge of T would also be a nonpendant bridge of G because a path between retained vertices cannot use a leaf internally. Section 2 therefore makes T bridgeless.

If a connected bridgeless graph of maximum degree three had a cut vertex t, each of at least two components of T-t would require at least two edges to t, since a unique edge would be a bridge. That would require degree at least four. Therefore T is TWO-VERTEX-CONNECTED. Cut vertices of G are exactly its leaf neighbors: deleting any other vertex keeps the two-connected T and its remaining attached leaves connected, whereas deleting a leaf neighbor isolates its leaf.

For a leaf v with neighbor u, take any star six-coloring of G-v (available by minimality). Since it cannot extend unchanged, C01 saturation applies. The other two neighbors x,y of u are degree three and their four other neighbors are distinct and each has a root-color support. None is a leaf. Thus x,y have degree three already in T, u has degree two in T, and no triangle or four-cycle of T passes through u. These statements concern the graph structure and therefore do not depend on which coloring was chosen.

Let S be the leaf-neighbor vertices (degree two in T but degree three in G), and D be the degree-two vertices of G. No vertex of S is adjacent in T to any degree-two vertex of T, by the previous paragraph. Section 3b implies that D induces at most a matching. Consequently all degree-two vertices of T induce a matching plus isolated vertices; no unqualified minimum-degree-three conclusion follows.

Finally, if T has a star five-coloring, color every removed leaf edge with color 6. Properness holds because leaf neighbors are distinct. A four-edge path using a leaf color once cannot alternate; if it uses that color twice, both pendant edges must be its first and last edges, positions that have DIFFERENT colors in a proper alternating four-edge path. No cycle uses a leaf. Hence G would be six-colorable. Thus T is not star five-colorable; when L is nonempty, minimality also supplies a six-coloring of T, so its star index is exactly six at this conditional candidate level.

In particular T cannot be just a cycle. A cycle C_n has a star coloring on colors {1,2,3,4}: write n=3q+r, use the cyclic word (123)^q for r=0, (123)^q4 for r=1, and (123)^q42 for r=2. Every cyclic four-edge window either lies in the period-three part, contains the unique color 4, or is the boundary window 2,1,2,3. It has at least three colors. Properness and the triangle case are immediate. The leaf-color argument then covers cycles with attached leaves.

These exclusions provide a two-connected core with constrained degree-two threads. They do not eliminate all leaves, two-edge cuts, degree-two pairs, triangles with all vertices cubic, or arbitrary cubic cores.

## 7. Audit and status

`opg37271-c14-structural-check.py` is a bounded standard-library generator-side check, CPython 3.13.5, wall 20 seconds, CPU soft/hard 20/21 seconds, address space 256 MiB. It exhausts 121 bridge-palette pairs for k=5 and 256 for k=6, and all 6,561 normalized external-palette cases for the triangle rule. The palette set is a positive overapproximation; unrealizable palettes are not used as negative witnesses. It also checks the explicit template including four-cycles, outputs a fresh coloring of C12R, checks cycles with leaves for n=3,...,60, and checks five completion examples. These finite diagnostics do not replace the universal arguments.

The output is saved in `opg37271-c14-structural-result.json`. Reproduce from the repository root:
`python research/artifacts/candidates/opg37271-c14-structural-check.py research/artifacts/candidates/opg37271-c12r-q2-certificate.json`.

No repository script, admitted adapter, mathematical verifier, or kernel was executed. Best verified result/candidate: none. Both existing obligations remain open. Sources and exact scope differences are in `research/artifacts/source-notes/opg37271-c14-sources.md`.

Next action: attack extending the bridge permutation argument to a two-edge cut; track attainable TWO-port boundary states rather than assuming one chosen pair of colorings can always be aligned. Preserve the cubic completion equivalence without pretending it is a cubic minimality theorem.
