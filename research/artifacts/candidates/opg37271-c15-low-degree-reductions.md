# C15L: complete low-degree extension rules and a tagged cubic core

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; admitted target: `obligation:opg37271-leaf-extension`.
Root: `obligation:opg37271-root`, still open.
Base: `1b2e1a6fda9ee30b832aa1ec3459623838faf0c4`.

## 1. Frozen quantifiers and notation

Every graph below is finite, simple, undirected and of maximum degree at most three. A star edge coloring is proper and excludes bichromatic simple four-edge paths and four-cycles; paths need not be induced. For a fixed old coloring c of H, write c_H(w) for the palette of its incident old edges.

Each local lemma quantifies over EVERY star coloring of the indicated vertex-deleted graph. Only the missing edges are colored, and all old edges retain their colors. This is a valid way to exclude the specified configurations from a vertex-minimal counterexample to the existential root; it does not resurrect the failed universal leaf-extension claim.

The general path proofs below use only finite-graph-basic and finite-combinatorics. The palette computation is a positive audit of sufficient choices, not a proof that every abstract palette is realizable and not a universal graph enumeration.

## 2. Lemma T: a degree-two vertex on a triangle

Let x have degree two with neighbors z,w and zw an edge. Every star six-edge-coloring of H=G-x extends to G unchanged on H.

Put p=c(zw). If z has another old neighbor z*, let a=c(zz*) and A=c_H(z*); otherwise omit a and set A empty. Define b,B at w in the same way. Each nonempty A contains a and has size at most three; similarly for B. Properness gives p different from a and b. The outside vertices z*,w* may coincide; neither is x,z,w.

We seek t=c(xz) and s=c(xw). Define

    T = C \ (A union {p,b}),     S = C \ (B union {p,a}),

where C={1,...,6} and absent colors are omitted. Both sets are nonempty. If there are distinct t in T and s in S, choose them. If not, necessarily T=S={r}. Then a,b both exist, a differs from b, p,b are outside A, and p,a are outside B: otherwise an excluded union would have size at most four and its complement would not be a singleton. In this exceptional case choose t=b and s=r.

In both cases the choice satisfies:
(i) t avoids A and p, s avoids B and p, and t differs from s;
(ii) t=b implies p is outside B; s=a implies p is outside A, whenever the mentioned old color exists;
(iii) not both t=b and s=a.
These conditions include properness because a is in A and b is in B whenever present. In the exceptional case s=r differs from a,b,p; p is outside B, as required.

Here is an exhaustive obstruction check. Old paths and cycles remain valid. If a new four-edge path contains exactly one new edge, x is its endpoint. Its old continuation either first goes to the corresponding outside neighbor, in which case alternation would require t in A or s in B, or traverses zw and then the opposite outside edge. In the latter case it requires t=b and p in B, or s=a and p in A. These are excluded by (i)-(ii).

If a new four-edge path contains both new edges, x is internal. With one old edge on each side its colors are a,t,s,b, which alternate only when s=a and t=b. If both remaining old edges are on one side, alternation requires t in A or s in B. These are excluded by (i) and (iii). A four-cycle using x contains both new edges and arises only from a common outside neighbor; its same opposite-color equalities are covered by (iii). Identifications that destroy simplicity remove cases rather than add any. This exhausts every path and cycle involving a new edge.

For a concrete exceptional palette, p=1, a=2, b=3, A={2,4,5}, B={3,4,5}. The naive sets both equal {6}; the corrected choice is t=3, s=6. A proof that merely chooses two distinct colors from T and S would miss this case.

## 3. Lemma P: three consecutive degree-two vertices

Let x have degree two and both its neighbors z,w have degree two. Every old star five-edge-coloring of H=G-x extends to G with the same five colors; the rule also works with six colors.

Let zz* and ww* be the remaining old edges, colored p and q. Put A=c_H(z*) and B=c_H(w*). Choose

    t in C \ (A union {q}),     s in C \ (B union {t}).

Both choices exist with five colors because each excluded union has size at most four. They give t outside A, s outside B, t different from s, and t different from q. Properness follows from p in A and q in B.

If z and w are adjacent, G's component at these vertices is the triangle xzw, all of whose vertices have degree two. Here p=q and A=B={p}; the rule gives a proper three-color triangle and no other new path. Otherwise a path with exactly one new edge and x as endpoint would need its color in A or B. A path with both new edges and two further old edges on one side has the same forbidden equality. With one old edge on each side, the colors are p,t,s,q; alternation requires t=q, excluded. A four-cycle through x, when z*=w*, has the same equality. Thus all obstructions are covered.

## 4. Lemma C: a degree-three vertex with three nonadjacent low-degree neighbors

Let x have three pairwise nonadjacent neighbors v1,v2,v3, each of degree at most two. Every old star six-edge-coloring of H=G-x extends unchanged on H.

If vi has an old edge vi-wi, denote its color pi and set Ai=c_H(wi). Otherwise omit pi and set Ai empty. Choose successively

    t1 in C \ (A1 union {p2,p3}),
    t2 in C \ (A2 union {t1,p3}),
    t3 in C \ (A3 union {t1,t2}),

again omitting absent old colors. Each excluded set has size at most five. Set c(xvi)=ti. The ti are pairwise distinct and each avoids Ai, so properness holds. For i<j, ti differs from pj whenever pj exists.

Every new simple path uses either one or two edges incident with x; it cannot use three. With just one such edge, x is an endpoint and an alternating continuation would require ti in Ai. With two new edges and two old edges on one side, the same condition is necessary for the color of the other new edge on that side's internal position: for a path vj-x-vi-wi-r, the third and first colors can agree, but the fourth would need to equal ti in Ai. It is therefore excluded. With one old edge on each side, the path wi-vi-x-vj-wj alternates only if ti=pj and tj=pi, contradicted by the ordered choice. The same equalities exclude a four-cycle when wi=wj. Nonadjacency of the vi ensures there is no omitted old edge directly between two arms. These cases are exhaustive.

## 5. Consequences under the root's minimum-order hypothesis

Assume G is vertex-minimal among counterexamples to the root. Minimality supplies a star six-coloring after any vertex deletion. Lemmas T, P and C imply:

- No triangle contains an original degree-two vertex.
- No degree-two vertex has two degree-two neighbors. Thus the subgraph induced by original degree-two vertices is a matching plus isolated vertices.
- Every degree-three vertex has at least one original degree-three neighbor. Otherwise all its neighbors have degree at most two; any adjacency between two neighbors gives a triangle with a degree-two vertex, already excluded, and the remaining case is Lemma C.

Combine this with C14B. Delete all leaves to obtain the 2-connected core K. Let S be the former leaf neighbors. Each vertex of S now has degree two in K but originally had degree three; it has two degree-three K-neighbors. S is nonadjacent to all other degree-two K-vertices. All other degree-two K-vertices originally had degree two, and form only isolated vertices or adjacent pairs.

K contains a degree-three vertex. If it were a cycle, no S could exist because members of S require degree-three K-neighbors. Then G itself would be a cycle, already star six-colorable.

Suppress every maximal path whose internal vertices have degree two in K. The result is a connected bridgeless cubic MULTIGRAPH M. It has no loop: a path returning to the same degree-three endpoint would form a cycle attached to the rest only at that endpoint, contradicting 2-connectivity of K. Parallel edges are NOT excluded. No simple-graph theorem may be applied to M without an additional argument.

Every edge of M has exactly one of four reconstruction types:
(0) an unchanged single edge;
(1) a two-edge path with one original degree-two internal vertex;
(2) a three-edge path with two adjacent original degree-two internal vertices;
(L) a two-edge path with one former leaf-support internal vertex and its single attached leaf restored.
There are no longer degree-two paths by the two preceding restrictions. Each degree-three vertex of M is incident to at least one edge of type (0) or (L): its original degree-three neighbor is either a core degree-three vertex or a former leaf support. This is a tagged template reduction, not a coloring theorem for every such template.

The original graph is recovered exactly by these subdivisions and attached leaves. C14B's different cubic COMPLETION is simple and may be larger; this cubic SUPPRESSION can have parallel edges. They must not be conflated.

## 6. Reproducible positive boundary audit

The companion script `opg37271-c15-palette-check.py` represents colors by bits and enumerates all palette supersets of size at most three containing the required incident color; absent arms are represented separately. It checks the displayed sufficient choices on all abstract boundaries, even those not realizable by a graph. Because the check is positive for the whole superset, no unrealizable profile is being used as a negative witness.

Observed standard-library CPython 3.13.5 run, with 15-second wall/CPU limits, 256 MiB address-space limit and one thread:
- 39,366 triangle boundaries, including 360 singleton-set fallback cases;
- 3,025 five-color chain boundaries;
- 912,673 six-color low-neighbor triples from 97 arm options.
All sufficient-choice conditions passed. The exceptional triangle fixture was checked explicitly. Results are in `opg37271-c15-palette-result.json`. This is generator-side computation, not an admitted adapter, kernel run, graph-enumeration certificate, or trusted receipt. Replay writes the result beside the script; use a disposable copy.

## 7. Prior art, remaining work and checkpoint

These configurations overlap published critical-graph reductions of Lei, Shi and Song; see the separate bounded source note. The present artifact supplies explicit simple-graph extension choices, the missing greedy fallback, full new-path/four-cycle cases, and a positive palette audit. No novelty or six-color theorem is attributed to a search hit or abstract.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open. No DAG or truth ledger was modified.

Next action: test two-edge-cut gluing using two-port states. A permutation that solves each port separately need not solve both simultaneously. Build a real connected-shore witness or a complete compatibility proof rather than infer two-cut reducibility from C14B's one-bridge lemma.
