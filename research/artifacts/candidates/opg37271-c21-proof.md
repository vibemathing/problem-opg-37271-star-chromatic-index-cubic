# C21 — outer choices from the root: universal preframes and two positive factor classes

Verdict: `candidate_only`. State: `NONTERMINAL_CHECKPOINT`.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input revision: d4853563085f4310d1d99cb332de62f44c36fbda.
Attempt: attempt:web-20260906-opg37271-a01; route: route:leaf-extension-six-colors-v1.
Graph: graph:opg37271-initial-v1. Current target: obligation:opg37271-root.
Issue: 6. Primary owner: math-proof. These are proof candidates, not admitted Results.
The legacy route name does not make a frame theorem a proof of the zero-edit leaf claim.

## 1. Frozen root and shortest dependency proposal

ROOT: For every finite simple undirected G with maximum degree at most three, there exists c:E(G)->{1,...,6} that is proper and has no bichromatic simple path of FOUR EDGES or simple cycle of FOUR EDGES. A path has five distinct vertices and need not be induced. A four-cycle has four distinct vertices. Palette maps need not be surjective. Empty graphs are allowed.

A C19 preframe means E=D disjoint-union U, a specified star coloring of D with A={1,2,3,4}, and U components that are vertex-disjoint paths of one to three edges. A balanced preframe has a consistent full system of ACTUAL mixed-witness rows

    x_P XOR x_Q = 1 XOR p(e) XOR p(f).

C20 supplies a proof candidate that precisely these balanced preframes extend using B={5,6}. Conversely any star six-coloring splits into such a frame: restrict colors 1..4 to D; the 5/6 subgraph is proper of maximum degree two and has no cycle or path with four or more edges, so its nonempty components are paths of at most three edges. Its actual coloring supplies the phases. Thus unrestricted balanced-frame existence is EQUIVALENT to root, not a new weaker subproblem.

Minimal proposed proof DAG (document-local labels, not record edits):
- R depends on CUBIC, OUTER, and DECODE.
- CUBIC: reduction from arbitrary subcubic graphs to connected simple cubic graphs.
- OUTER: every connected simple cubic graph has a balanced preframe.
- DECODE: C19-E/C20 pointwise equivalence and explicit phase decoding.
- PRE below supplies admissible, self-row-free preframes, but does NOT supply OUTER.
- SQ and ODD below discharge OUTER only on specified factor subclasses.
- External assurance of every needed node is separate and still pending.

For CUBIC, double a connected nonempty subcubic graph and join corresponding deficient vertices. The cross edges form a matching, no multiple edge or loop is created, and each deficient degree increases by one. After r=max(3-d(v))<=3 rounds all degrees are three. Each nontrivial round has a cross edge, preserving connectivity; the original graph is induced in the result of size 2^r|V|. Restrict a host star coloring to recover one on the original graph. Apply componentwise; the empty case is immediate. This rederives the C14 completion step and does not assume a perfect matching in an arbitrary cubic graph. The existing root-to-leaf ledger dependency is not used as a positive proof edge.

## 2. PRE: every simple cubic graph has a self-row-free preframe

Build a bipartite double cover with left/right copies of V and edge v_L w_R exactly when vw is an edge of G. It is three-regular. For S on the left, counting incident edges gives 3|S|<=3|N(S)|. A maximum bipartite matching cannot leave a left vertex unmatched: alternating reachability from it would either reach a free right vertex and augment, or yield a left set S with |S|>|N(S)|, contrary to the count. Thus it is perfect. An implementation augments one left vertex at a time; matching size increases strictly, for at most |V| augmentations. Reachability examines finite vertices/edges and terminates. No probabilistic choice is used.

Write the resulting permutation as pi(v)=w when v_L is matched to w_R. Each pi(v) is adjacent to v; there are no fixed points. Decompose pi into disjoint directed cycles. A two-cycle supplies one undirected single-edge path. On an even cycle partition its cyclic vertex order into consecutive pairs. On an odd cycle take its first three consecutive vertices as a two-edge path, then partition the remaining vertices into consecutive pairs. The selected undirected edges U form a vertex-spanning family of disjoint paths of one or two edges.

Every vertex of G now has U degree one or two, so D=E-U has degree one or two. Its components are paths or simple cycles. Paths are star colored by repeating 123. For a cycle of length n>=3 other than five, write n=3r+4s with r>=0 and s in {0,1,2}, chosen by n modulo three. Concatenate r blocks 123 and s blocks 1213. Properness and the star property follow from the four ordered block junctions: every consecutive four-edge window has at least three colors. A window touches at most two blocks because blocks have length at least three. Closing windows are also junction windows; the triangle has no four-edge forbidden shape. For n=5 use 12134; its five cyclic four-windows each contain at least three colors. Thus D is star colored with at most four A colors.

This proves PRE for every finite simple cubic G, including graphs without perfect matchings. The empty graph gives the empty preframe. The construction is deterministic after choosing vertex/edge order. Augmenting paths use O(|V||E|) work with a conventional implementation; all subsequent traversals are linear. This bound is not a claim about solving the eventual XOR compatibility problem through new outer choices.

Every selected mixed witness uses two opposite, hence disjoint, U edges. In a component of at most two edges, distinct edges are incident, so the witness cannot use that component twice. Consequently PRE eliminates ALL self-row obstructions universally. This is not an assumption about induced paths.

A further specialization: if a perfect matching M is supplied, set U=M and D=E-M. The same cycle coloring supplies a preframe; every U parity is zero. Each row has right side one and distinct endpoints. Opposite-sign parallel rows are then impossible, even if multiple actual supports connect the same pair. Only odd cycles in the ordinary contact graph can obstruct. This specialization is not available on every cubic graph, and no claim that its contact graph can always be made bipartite is made.

## 3. Real surviving cores, not abstract obstructions

The replay reconstructs four PRE outputs from their original edge lists. K4 extends. The specified K3,3 and ten-vertex inputs have three-row negative cores; the sixteen-vertex input has a two-row core. The complete row lists and phase enumeration are saved in the new result. These are failed particular outputs, not graphs without a good frame.

For K3,3, use lexicographic edges (0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5). PRE gives D colors (1,3,0,2,0,3,0,2,1), U paths [2],[4],[6]. Actual four-cycles 0-3-2-5-0, 0-4-1-5-0, and 1-3-2-4-1 give the three distinct pair inequalities on these variables, summing to 0=1. There are no self or negative parallel rows. Changing edge (0,3) to the spare A color 4 gives a feasible frame, as direct reconstruction confirms. Thus merely removing the two smallest core types does not finish OUTER.

The sixteen-vertex cubic input is explicit in the input JSON: three copies of K4 with one edge subdivided, each subdivision vertex joined to one new central vertex. Each five-vertex lobe forces its unique cut edge into any perfect matching by odd-order counting. All three would meet at the center, impossible. PRE nevertheless exists and contains two-edge U paths. In its recorded ordering, witness 0-5-2-4-3 gives x_1 XOR x_0=0, while four-cycle 1-3-2-5-1 gives x_0 XOR x_1=1. These are real graph paths/cycles and explain the surviving two-row core.

## 4. SQ: every simple cubic graph with a C4-factor is star five-edge-colorable

Let F be a specified spanning disjoint union of four-cycles, and M=E-F its perfect matching. No coloring of M is fixed. On each four-cycle abcd add the AUXILIARY opposite matching {ac,bd}, denoted O. The typed multigraph M disjoint-union O is a union of alternating even cycles; if an M edge is also an O pair, retain the two typed parallel edges as a digon. Hence choose vertex bits sigma that differ across every M and every O edge.

Opposite vertices of a four-cycle have opposite bits. Its bit word is therefore one of 0011,0110,1001,1100 after choosing a starting vertex. Exactly two opposite F edges have equal endpoint bits. Put these in U; the other two are S. Globally U and S are perfect matchings, and every edge of D=M union S crosses the bit cut.

D is a simple bipartite two-regular graph, hence a union of even cycles of length at least four. Color it with 123/1213 as in PRE; no fifth-length exception occurs, so only THREE A colors are used. Color each U edge vw by 5+sigma(v)=5+sigma(w).

Properness follows from the D coloring, U being a matching, and disjoint palettes. A forbidden shape contained in D is excluded; one contained in U is impossible. A mixed alternating four-edge path or cycle contains a consecutive U-D-U triple. The central D edge has opposite endpoint bits, and its adjacent U edges have those respective bits. They therefore have DIFFERENT B colors. This rules out every mixed bichromatic shape. It proves a star coloring with colors {1,2,3,5,6}, i.e. five colors, without retaining a previous matching coloring.

For C20, U variables are single edges and all row signs are one. The bit of each monochromatic U edge supplies a bipartition of every actual contact edge, so all negative cycles, not merely loops or parallel pairs, disappear. Distinct witnesses may share graph edges without affecting this argument. The construction works componentwise and in linear traversal time once F is given. No claim that every cubic graph has a C4-factor is made.

## 5. ODD: every simple cubic graph with a {C3,C5}-factor is star six-edge-colorable

First suppose M=E-F is supplied with a strong A coloring lambda: matching edges joined by any F edge have different colors. Regard lambda as a proper vertex coloring of each F cycle, constant on M endpoints.

For each cycle choose the following matching S of special F edges. Each special edge v_i v_(i+1) receives a color absent from the four labels at v_(i-1),v_i,v_(i+1),v_(i+2).
- On a triangle choose one edge and use the fourth label color, absent from the whole triangle.
- On a pentagon with three labels, the multiplicities are 2,2,1. Rotate its unique label a to position 0. Assign edge v2v3 color a and edge v4v0 the unused fourth A color d. They are disjoint and differently colored; both satisfy the displayed four-vertex exclusion.
- On a pentagon with four labels, rotate/reverse to the word (a,b,a,c,d). Assign v0v1 color c and v3v4 color b. Again these edges are disjoint, differently colored, and each chosen color is absent from its four-vertex window.
The multiplicity cases exhaust proper A colorings of C5, since each color occurs at most twice and at least three colors are needed.

Now D=M union S is properly colored, U=F-S consists of paths of one or two edges, and D is star: every four-edge D shape alternates the two matchings and contains an M-S-M triple whose two M colors differ. For a prospective mixed shape, its two equal A-colored edges are separated by a U edge. If both are M, strong coloring excludes equality. If one is M and the other S, the four-vertex exclusion excludes equality. If both are S, they lie in the same F component, where all chosen S colors differ. Thus NO mixed row exists at all. Alternate 5/6 independently on all U components. This proves the specified strong-four-matching extension for arbitrary numbers of triangles/pentagons, including matching chords and non-induced witnesses.

To remove the strong-coloring premise for this factor class, let X_M be the simple conflict graph on matching edges. Its maximum degree is at most four, and it is connected when G is connected. Brooks' theorem implies a four-coloring unless X_M=K5: degree at most three is also handled greedily with four colors; smaller complete graphs and odd cycles need at most four. This is an explicit external theorem dependency, not the invalid inference 'maximum degree four alone implies four colors'. Source: Baetz and Wood, arXiv:1401.8023v1, abstract's precise Brooks statement and algorithmic proof description. No claim of a new Brooks theorem is made.

If X_M=K5, M has five edges, G has ten vertices, and F has ten edges serving ten distinct conflict pairs. Therefore each pair is served exactly once. With cycle lengths restricted to 3 or 5, F must consist of two five-cycles. An M chord inside either five-cycle would join vertices at distance two; the two F edges through their common intermediate vertex then serve the same conflict pair twice, impossible. Thus all matching edges join the two cycles.

Label the cycles 0..4 and 5..9 in cyclic order. Every exceptional pair (G,M) is represented by one of the 120 permutations p with matching (i,5+p(i)). The separately implemented replay checks the actual conflict pairs for all 120. Exactly indices 10,13,36,44,50,69,75,83,106,109 are K5 cases. The compact certificate has an explicit full fifteen-edge six-coloring for EACH, directly checked from its edge list. This is a finite exceptional coverage argument, not an extrapolation to arbitrary graphs. The colorings may use five different colors on M and are not advertised as strong-four precoloring extensions. General C19 frames can still be obtained by splitting their full six-colorings. Together with Brooks and the local recipes this proves the ODD candidate componentwise.

## 6. Complete-space barriers: K3,3 is not a root counterexample

The supplied K3,3 coloring in the edge order of Section 3 is (1,4,5,4,2,6,5,6,3); direct path/cycle replay confirms a star six-coloring.

No star five-coloring exists. A color class of size three is a perfect matching. If another color class has at least two edges, their union with that perfect matching contains a four-cycle or a five-edge alternating path (contract the three matching edges: the two additional disjoint edges either join the same pair of blocks, or form a two-edge path through all three). Either contains a forbidden shape. The remaining six edges cannot then be covered by four other colors, each of size at most one. Hence all color classes would have size at most two.

Nine edges in at most five such classes require at least four classes of size two. Each two-edge matching misses one of the three left vertices. Two of those four classes miss the same left vertex. Their four edges use the same two left vertices, each of degree two in the two-color subgraph. The right degrees are either (2,2,0), giving C4, or (2,1,1), giving a simple four-edge path. Both are forbidden. This contradiction proves the lower bound six, paired with the explicit positive witness.

Consequently the complete route 'D star colored with only three colors, U alternating with two disjoint colors' fails for EVERY D/U choice on this graph. This is the ENTIRE three-plus-two frame space, not one frame. It is minimum order among nonempty simple cubic graphs failing that five-color target: such graphs have even order at least four, and the unique order-four simple cubic graph is K4, colored by SQ. This does NOT disprove the root's four-plus-two route.

A separate stronger cut-based four-plus-two condition also fails on every choice for K3,3. Require U to consist exactly of edges whose endpoints share a vertex bit, and require U a matching. If l and r are the counts of bit-zero vertices in the two bipartition classes, U is the union of K_(l,r) and K_(3-l,3-r). Unless all original left vertices have one bit and all right vertices the other, one of these complete bipartite subgraphs has degree at least two. Thus the only valid two bit assignments give U empty and D=K3,3, which is not star four-colorable by the stronger five-color lower bound. The replay checks all 64 bit assignments, not just selected cuts. Failure of this sufficient cut construction is not failure of general frames: the six-color witness splits into a valid D/U with two-edge U components.

## 7. Algorithms, bounded tests, and exact remaining gap

The constructor and replay import no C20 code. The replay enumerates simple paths/cycles directly from adjacency, whereas C20 generated four-edge subsets. It reconstructs matching and factor coverage independently, checks complete pairing domains, and checks every produced full coloring. It also replays the two frozen C19 input frames, retains actual core witnesses, rejects ten mutation cases, and covers empty U and the empty graph.

The finite stress domains are every legal perfect matching complementing 1,2,3 fixed labelled squares, and factors of lengths (3,3),(3,5),(3,3,3,3). Their numbers are 1,33,3329 and 6,30,3348. All 295 legal matching complements of two labelled five-cycles are also checked by the componentwise unconditional constructor, including the ten K5 cases. Disconnected inputs are retained; these are labelled graph/factor descriptions, not graph isomorphism counts. The additional 24 proper triangle label words and 240 proper pentagon label words are exhaustively checked. The exceptional ten colorings are persisted explicitly. A deterministic normalized stress stream is regenerated by the committed constructor and fed to the replay; its exact SHA-256 is recorded, rather than treating old result JSON as execution. Counts only audit finite interfaces; PRE, SQ and ODD have the general proofs above.

The implementation has finite input caps (at most sixteen vertices and twenty-four edges for the replay fixtures), wall/CPU/memory/output limits in the runner, and no unbounded solver invocation. The matching-label backtracking in the diagnostic implementation is finite but exponential; the universal existence argument uses the separately identified Brooks theorem. No linear-time claim is made for that diagnostic backtracker. The K5 coloring search routine is bounded to 100000 nodes and was only used to prepare explicit finite witnesses; replay performs no such search.

The first still-open root obligation is OUTER for arbitrary cubic graphs: choose an admissible D/U and A coloring with no negative parallel or longer XOR cycle. PRE removes self rows, not that remaining obligation. The stronger option U having at most two edges per component is only a proposed search route, not asserted equivalent to root. Mixed factors containing both four-cycles and other lengths are not covered merely by combining SQ and ODD. Graphs with no such special factor also remain. The exact premise gap of the proposed spare-color repair is unchanged: a spare A color and a suitable induced matching hitting all relevant support witnesses need not be available.

A broad exploration of strong-four M/S frames found positive small instances and the already-known K5 matching-color obstruction, not a new graph excluding the entire unrestricted four-plus-two space. A larger isomorphism-catalogue experiment hit resource limits and is not an exhaustive result. These exploratory directions are not substituted for a general OUTER proof.

## 8. Assurance request and nonterminal checkpoint

Only the candidate lane is used. Main has the transport-only workflow and no matching exact local obligation/registered candidate/toolchain allowance for a C20 or C21 kernel request. The request binds exact statement and file hashes and keeps the unavailable execution fields null. No workflow or truth file is modified, no verifier identity is impersonated, and no old JSON or CI check closes mathematics. Historical missing material is not an input.

Best current candidate: PRE plus SQ, ODD and the sharp K3,3 five-color/cut barriers, with executable graph replay. First open mathematical node: OUTER. Next atomic action: on the universal short-path preframe class, search complete A-coloring/path-factor choices for an unremovable negative parallel core, or prove a witnessed core-removal rule with a well-founded global progress measure. Preserve the distinction between 'this preframe fails', 'every frame in a declared restriction fails', and a genuine root counterexample.

State stays NONTERMINAL_CHECKPOINT. A front-end response boundary or candidate merge does not stop the research problem or supply terminal closure.
