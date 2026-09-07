# C19P: exact two-color completion by a signed phase graph

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt `attempt:web-20260906-opg37271-a01`; route `route:leaf-extension-six-colors-v1`.
Graph `graph:opg37271-initial-v1`; admitted target `obligation:opg37271-leaf-extension`.
Root `obligation:opg37271-root` stays open.
Base: `ff92df4363669fe1e9fc6a901cbe27251d8d14b1`.

## 1. Frozen completion question

Let G be finite, simple and subcubic. A subset D of its edges is given a star edge coloring c using A={1,2,3,4}. The uncolored edges U=E(G)-D form vertex-disjoint nonempty paths, each of length at most three; isolated vertices do not matter. Does c extend to a star edge coloring if every edge of U must use B={5,6}?

Only this specified partial coloring and residual palette are fixed. This is neither the root's unrestricted existence statement nor arbitrary full-coloring repair with a bounded old-edge edit count. No assertion is made that every root input admits such a decomposition.

## 2. Equations with actual graph witnesses

Orient and order each uncolored path P. Let p(e) be the parity, zero or one, of an edge's index starting at zero. Every proper B-coloring is uniquely given by one phase x_P in F2, with color

    c'(e) = 5 + (x_P XOR p(e)).

Enumerate every actual simple four-edge path and four-cycle in G. Paths need not be induced. Whenever its positions alternate between D and U and its two D edges have equal color, let e in P and f in Q be the two U edges. Add the equation

    x_P XOR x_Q = 1 XOR p(e) XOR p(f).                 (1)

Record the path/cycle vertex sequence, its four edge indices and the two U edge indices. Multiple equal equations may be deduplicated, retaining one witness; equations with the same variables and different right sides must both remain. P=Q is permitted.

Claim C19-E: the required completion exists exactly when all equations (1) are consistent.

Proof candidate. Properness within D is given; within U it is enforced by the phase representation; incident edges across D/U have disjoint palettes. A monochromatic pair is therefore impossible. A forbidden alternating four-edge path or cycle using two A colors would be contained in D and contradict its star property. One using two B colors would be contained in a U component, impossible because that component is a path of at most three edges. With one color from each palette, the four positions alternate D/U. Such an obstruction occurs exactly when the two D colors agree and the two U bits agree. Equation (1) excludes precisely this event. These cases cover all pairs of colors and both forbidden shapes, giving necessity and sufficiency.

The proof also applies when U is empty: there are no phases and exactly the one given coloring. No realizability assumption is hidden in an abstract vector; every equation comes from the supplied finite G.

## 3. Positive and negative certificates

Form a signed multigraph with one vertex for each nonempty U component and an edge of sign b for x_P XOR x_Q=b. Loops and parallel edges are allowed.

The system is consistent if and only if the XOR of the signs along every closed walk is zero. Necessity follows by cancelling all variables around the walk. For sufficiency, choose one root value per connected component, propagate values along a spanning tree, and use the closed-walk condition to check every remaining edge. A loop of sign one is already a contradiction.

If consistent and the signed graph has z connected components, including isolated phase variables, there are exactly 2^z completions: the root value in each component is free, all others are forced. The phase-to-edge-coloring map is injective because each path has at least one edge.

A negative certificate can consist merely of witnessed equations whose sum has zero coefficient for every phase variable and right side one. It need not claim to have enumerated every equation: this contradictory subset alone rules out completion. A positive phase list should be checked against the complete system or, more simply, decoded into a full coloring and checked directly on G. An arbitrary unsigned or coordinate-legal profile is not a valid negative certificate.

For bounded degree, enumerating paths of four edges takes linear time with a fixed constant; signed-graph propagation also takes linear time in its explicit input. These are complexity claims about the specified completion problem, not a polynomial algorithm for choosing D and c.

## 4. Connection to a four-colored matching

Suppose a perfect matching M has a specified strong four-coloring: matching edges joined by a G edge receive different A colors. Choose S to be a matching in F=G-M, and assign each edge of S an A color different from the two matching colors at its endpoints.

Then the coloring of D=M union S is automatically star. It is proper by the endpoint restrictions. Since D is the union of two matchings, any four-edge path/cycle in D alternates membership M/S and contains an M-S-M triple. The two M colors in that triple differ by the strong-matching premise, and the S color differs from both. Hence it is not bichromatic.

Whenever F-S consists of paths of length at most three, (1) is therefore an exact test for extending this chosen frame with colors 5,6. A strong same-color distance-two separation hypothesis on S is unnecessary: its actual interactions are retained as global parity constraints instead. The choices of M, its strong coloring, S and its colors remain unresolved outer existential variables. C18M handles the special three-matching-color case by a different residual three-color construction.

## 5. Explicit global obstruction, not a root obstruction

Take a six-cycle with vertices 0,...,5 and edges e_i={i,i+1 mod 6}. Fix c(e_0)=c(e_2)=c(e_4)=1; leave e_1,e_3,e_5 uncolored. The fixed subgraph is a matching and is star. Each uncolored component is a single edge, with phase x_0,x_1,x_2 respectively.

The actual paths 0-1-2-3-4, 0-5-4-3-2, and 2-1-0-5-4 give respectively

    x_0 XOR x_1 = 1,
    x_2 XOR x_1 = 1,
    x_0 XOR x_2 = 1.

Adding them yields 0=1. Thus the restricted two-color completion fails, although every uncolored edge has both colors locally available for properness. With three residual colors the same partial coloring extends as [1,4,1,5,1,6] around the cycle. This graph is not a root counterexample, and its fixed matching coloring is not strong.

## 6. An actual strong-four-color positive frame

Take two four-cycles 0-1-2-3-0 and 4-5-6-7-4, with matching edges, in order,

    (0,4):1, (1,5):2, (2,7):3, (3,6):4.

Their conflict graph is K4. In the first cycle set c(1,2)=1 and c(3,0)=2. In the second set c(5,6)=1 and c(7,4)=2. These four special edges form S. Leave the other four cycle edges uncolored, indexed as

    P_0=(0,1), P_1=(2,3), P_2=(4,5), P_3=(6,7).

The complete deduplicated equation list in the certificate is

    x_2 XOR x_3=1, x_0 XOR x_2=1, x_1 XOR x_0=1.

A solution is (0,1,1,0), so the U colors are (5,6,6,5). The two cycle color words are respectively (5,1,6,2) and (6,1,5,2). The full edge/color list and actual path witnesses are included in the JSON certificate.

Every four-vertex cyclic window here uses all four matching labels. Thus an operation requiring a special edge color absent from all four nearby matching labels would reject every special location. The exact phase method nonetheless supplies the displayed full star coloring. Failure of that stronger operation cannot be substituted for failure of completion.

## 7. Bounded finite audit

The check program enumerates all 24 matching permutations between two labeled four-cycles. M gets four distinct colors. On each cycle S is any nonempty matching: four single-edge choices and two opposite-pair choices. Each special edge can use either of the two A colors absent at its endpoints. This gives 6,144 actual partial frames.

For every frame, the program compares signed-graph feasibility and the 2^z solution count with direct checks of every phase assignment. The observed total is 55,296 binary assignments: 544 frames have completions and 5,600 do not. Counts by number of special edges are 1,536 frames / zero feasible with two specials; 3,072 / zero with three; 1,536 / 544 with four. Every one of the 24 actual graphs has a supplied positive six-coloring. These are frame counts, not counts of graph isomorphism classes or non-six-colorable graphs.

The compact certificate saves one positive full coloring per matching permutation and the two fully witnessed phase frames in Sections 5-6. The separate replay imports neither the compiler nor its solver. It checks graph and component realizability, each displayed equation against the named actual path, the negative XOR sum, positive decoded colorings and all 24 graph colorings. The latter checks traverse 3,712 oriented four-edge paths and 896 oriented four-cycles. Removing part of the contradiction, changing a sign, repeating a witness vertex and corrupting a positive color are rejected. This replay does not redo the full 6,144-frame tally; the bounded check program does.

Actual observed runtime: CPython 3.13.5, standard library, one thread; per process 35-second wall alarm, 35/36-second CPU limits and 512 MiB address-space cap. Input/output JSON is capped at 262,144 bytes. All runs are local generator-side diagnostics, not an admitted adapter, repository command, kernel run or trusted receipt.

Reproduce in a disposable copy by running `opg37271-c19-phase-check.py`, then `opg37271-c19-phase-replay.py`. Both write their named result beside the source. Freeze bytes before any external replay; separately verify this universal equivalence and the graph encoding.

## 8. Scope and checkpoint

Dependencies: C18M's matching/palette distinction and the frozen ProblemContract, plus elementary finite graph and F2 reasoning supplied here. No external theorem or novelty claim is required. The direct finite certificate contains no hidden transcript.

Best verified result: none. Best verified candidate: none. Both admitted obligations stay open; state nonterminal. This advances an exact global compatibility invariant but does not close the root.

Next exact action: test the outer strong-four-matching frame construction on actual two-five-cycle graphs, with complete finite certificates for any failure. Any failed frame must be distinguished from a graph admitting no frame, and both from a graph admitting no unrestricted star six-coloring.
