# C14B: bridge gluing, a cyclic core, and faithful cubic completion

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; admitted target: `obligation:opg37271-leaf-extension`.
Root under analysis: `obligation:opg37271-root`, still open.
Base: `d8b2685cc6becd6087335a6c51b944a55f1e6bd1`.

These candidate reductions examine what survives after the fixed-coloring extension route fails. They do not edit the admitted DAG or purport to close its root. Only finite-graph-basic and finite-combinatorics are used in the proofs below.

## 1. Exact bridge boundary criterion

Let xy be a bridge of a finite simple subcubic graph, with connected shores A and B. Make A+ by adding a private leaf y_A and edge x-y_A to A. Make B+ similarly with a private leaf x_B and edge x_B-y. Suppose both augmented shores are star k-edge-colored, and their stub edges have the same color a.

For b different from a, let ell_A(b) be the length of the maximal alternating {a,b}-path beginning at y_A through x. Define ell_B(b) analogously beginning at x_B through y. Properness makes each continuation unique; the pendant boundary and the star property give 1 <= ell <= 3. Each shore has at most two coordinates greater than one.

Delete the private leaves and replace the two stubs by xy of color a. This glued coloring is star if and only if

    ell_A(b) + ell_B(b) <= 4   for every b != a.                 (1)

Proof. Properness is inherited at both endpoints. Every cycle lies in one shore. A newly bad bichromatic component must use xy, so its color pair includes a. Its path through xy has exactly ell_A(b)+ell_B(b)-1 edges: the two stub edges have become one. The two tails lie in disjoint shores. Thus it contains a forbidden four-edge path exactly when the displayed sum is at least five. Other components are unchanged. This proves both directions, including cases where one tail is empty.

This is a bridge criterion, not C08's one-vertex gluing formula; the two formulas have different thresholds because a stem is identified here.

## 2. Arbitrary augmented-shore colorings can be aligned for k >= 5

Let P be the at-most-two nonunit colors on the A side and Q the corresponding colors on B, whose stub currently has color beta. Choose a permutation pi with pi(beta)=a and pi(Q) disjoint from P. It exists: at least k-3 >= 2 target colors remain outside P and {a}, and the chosen injective assignment extends to a permutation of the whole palette.

Apply pi to EVERY edge of B+, not just its boundary. This preserves its internal star property. For each b != a, at least one of ell_A(b), ell_B_after_pi(b) equals one, while the other is at most three. Equation (1) holds, proving a star k-coloring of the glued graph.

The input quantifier is over arbitrary colorings of A+ and B+. Bare-shore colorings are not a substitute for these augmented inputs. The number of recolored old edges is not bounded by a constant.

The universal palette-permutation assertion cannot replace five by four. On each augmented shore, use stub color 1 and two arms with alternating lengths three in colors 2 and 3; the remaining color has length one. Realize it as a stem p-x=1 and two disjoint paths x-r_b=b, r_b-t_b=1 for b=2,3. Each shore is a star-colored subcubic tree. Every permutation aligning the stubs maps two active colors into a three-color set, so the active sets overlap. At an overlapping color, the sum in (1) is six. Thus none of the six stub-preserving permutations works. This is an obstruction to the specified permutation operation, not a lower bound on the glued graph's best star coloring.

## 3. Consequence for trees, with existential colorings

Every finite subcubic forest admits a star five-edge-coloring. For a connected tree use induction on its order. If it has a bridge with at least two vertices on each shore, its two augmented shores have strictly smaller order. Apply induction to them and Section 2 with k=5. Otherwise every edge is pendant. Such a tree has diameter at most two (the middle edge of a four-vertex path would not be pendant), so it is a star with at most three edges and is immediately colorable. Singletons and the empty forest have no colored edges. Components reuse the same palette.

This is a constructive existence argument. It makes no assertion about extending an arbitrary fixed coloring with few changes, and therefore does not conflict with C12R or C13H.

## 4. Vertex-minimal root counterexamples: bridges and a typed core

Assume a counterexample to the frozen root exists, and choose one with minimum number of vertices. Denote it by G. Every smaller finite simple subcubic graph then admits a star six-edge-coloring.

G is connected: otherwise every component is smaller and their colorings combine. It has an edge and is not a tree by Section 3. A graph of maximum degree two has a star coloring with at most five colors: greedily distinguish edges at line-graph distance at most two, of which there are at most four other edges. Such a coloring has no alternating four-edge path or cycle. Hence G has a degree-three vertex.

Every bridge of G is pendant. Indeed, if both shores of xy have at least two vertices, each augmented shore has at most |V(G)|-1 vertices. Minimality supplies the two star six-colorings required in Section 2, a contradiction. When a shore is a singleton, the other augmented shore has the same order as G; this argument does not exclude a leaf.

Let L be the set of leaves and S their neighbor set. Apply C01's saturation equality to any star six-coloring of G-v for each v in L. It yields:
- every vertex of S has degree three and exactly one leaf neighbor;
- its other two neighbors have degree three;
- those neighbors each have two further incident spokes whose far endpoints have degree at least two (a root-colored support is required).

Consequently S is an independent set in G. If s,t in S were adjacent, applying the preceding last condition at s would require the leaf adjacent to t to support a further edge. This is impossible. Vertices of S also have no original degree-two neighbor.

Set K=G-L, deleting all original leaves simultaneously. K is connected, and its minimum degree is at least two: original degree-two vertices lose no edges, while a degree-three vertex loses at most its unique leaf edge. Thus this one-shot deletion already is the 2-core. It contains a cycle and has at least three vertices.

K has no bridge. A bridge in K would remain a bridge after attaching leaves, and its endpoints are nonleaves of G, contradicting the pendant-bridge conclusion. A connected bridgeless graph of maximum degree three and at least three vertices has no cut vertex: each component after deleting a cut vertex would require at least two incident edges to avoid a bridge, demanding degree at least four. Therefore K is 2-connected.

Each vertex of S has degree two in K, and its two K-neighbors have degree three in K because S is independent. K's other degree-two vertices were already degree two in G. These two types must be retained separately in later reductions; an original-degree assertion must not silently be applied after stripping leaves.

Finally each s in S lies on a cycle of length at least five. It lies on a cycle in K; a triangle through s would join its two other neighbors, and a four-cycle would identify two opposite-side spoke endpoints. Both are excluded by C01's saturation argument.

## 5. Cubic completion without a fixed-coloring requirement

For a nonempty finite simple subcubic graph F, perform this operation: take two disjoint copies of F and join corresponding vertices exactly when their current degree is less than three. The new cross edges form a matching. No loop or parallel edge is created, and every deficient degree increases by one while degree-three vertices remain unchanged.

Repeat r=max_v(3-d_F(v)) times. Induction shows that a descendant of v has degree min(d_F(v)+i,3) after i rounds. The final graph J is simple and cubic, has exactly 2^r |V(F)| <= 8|V(F)| vertices, and retains the original F as an induced subgraph. If F is connected, every nontrivial doubling step has at least one cross edge, so J stays connected. If F is already cubic, r=0. The empty graph needs no completion.

Star edge-colorability is hereditary under taking subgraphs: any incident pair, simple four-edge path, or four-cycle in the subgraph is also present in its host. Consequently the frozen root is equivalent to:

    Every finite connected simple cubic graph has a star six-edge-coloring.

One implication is specialization. For the reverse implication, complete each connected component as above, color the connected cubic completion, restrict, and reuse the palette among components. Equivalently any root counterexample yields a connected cubic counterexample by completing a bad component.

This equivalence does NOT say a smallest counterexample among all subcubic graphs is itself cubic, or that the completion is bridgeless. A smallest counterexample has minimum degree at least one and thus admits the sharper completion size bound 4|V(G)|; with minimum degree at least two the bound is 2|V(G)|. As a finite-search consequence, certified six-colorability of all connected simple cubic graphs up to order 4N suffices for all subcubic graphs up to order N, after ignoring isolated components. No such exhaustive coloring search is reported here.

## 6. Finite audit and source comparison

The companion `opg37271-c14-bridge-completion-check.py` enumerates the exact pendant signatures for k=5 and k=6, constructs a permutation for each ordered pair, and checks (1). Observed counts are 165^2=27,225 and 306^2=93,636 pairs. It also rejects all six stub-preserving permutations for the four-color example.

For completion it checks every labeled simple subcubic graph of orders one through five: respectively 1,2,8,64,768 inputs. Each output is checked for simplicity, degree three, the induced embedding, exact number of rounds and connectedness when appropriate. Three explicit completion edge lists, including the isolated vertex and a five-cycle, are retained in the result. These finite checks support, but do not replace, the general arguments above.

Observed runtime: CPython 3.13.5, standard library, one thread, fifteen-second wall/CPU limits and 256 MiB address-space cap. These are generator-side observations, not trusted verifier receipts. Replay writes a result beside the script and should use a disposable copy.

For comparison with the seven-color literature, see the bounded source note. Its distance-two spare-color argument is not assumed to work with six colors. The bridge-stub premise and the strict-order comparison above are explicit instead. No novelty assertion is made for these elementary constructions.

## 7. Checkpoint and admission boundary

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open. The existing root dependency on the false zero-edit proposal cannot be treated as positive proof closure; any replacement DAG is a proposal for the trusted coordinator, not a record edit by this candidate.

Next action: audit universal extension at a degree-two vertex on a triangle, a run of three degree-two vertices, and a degree-three vertex with three low-degree neighbors. Then examine two-edge cuts without assuming that independent one-port permutations can be combined.
