# C17: matching-conflict K5 is a completely covered positive cubic subclass

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt `attempt:web-20260906-opg37271-a01`; Route `route:leaf-extension-six-colors-v1`.
Graph `graph:opg37271-initial-v1`; admitted target `obligation:opg37271-leaf-extension`.
Root `obligation:opg37271-root` remains open.
Base: `adb8fde9b329be300ce16385385bfcab5e7c048c`.

This advances a global matching/2-factor route rather than the false fixed-old-coloring extension route. It includes a manual coverage proof, a finite constructive coloring table, and two algorithmically different generator-side checks. None is a trusted mathematical receipt.

## 1. Frozen statements

Let G be a finite simple connected cubic graph and M a perfect matching. Define X_M to have vertex set M; distinct e,f in M are adjacent if an edge of G joins an endpoint of e to an endpoint of f. This is precisely edge distance two in G, or distance two in its line graph. All graphs here are undirected. A star edge coloring is proper and has no bichromatic simple path or cycle of four edges. Paths need not be induced. Colors are in {1,2,3,4,5,6}, without a surjectivity requirement.

C17-A: maximum degree at most four in X_M does NOT imply a four-coloring of X_M. An explicit connected simple cubic input below has X_M=K5.

C17-B: every such pair (G,M) with X_M=K5 has a star six-edge-coloring, including one extending any injective assignment of five colors to M. This is a positive finite-subclass claim about actual graphs. Its exhaustive certificate remains candidate-only pending the declared verification gates.

Only finite-graph-basic and finite-combinatorics are used. This does not assume that every cubic graph has a perfect matching, and it does not claim that all possible X_M are K5.

## 2. The explicit auxiliary obstruction and a root coloring

Take V(G0)={0,...,9}, cycle edges i--(i+1 mod 10), and

    M=[(0,7),(1,4),(2,9),(3,6),(5,8)].

Name these matching edges e0,...,e4 in the displayed order. Each vertex has degree three. The cycle makes G0 connected and has every vertex in exactly one cycle, so it is also a valid spanning cactus with remaining matching M'=M.

The ten cycle edges witness the following ten distinct conflict pairs:

| cycle edge | pair | cycle edge | pair |
|---|---|---|---|
| 0--1 | e0,e1 | 5--6 | e3,e4 |
| 1--2 | e1,e2 | 6--7 | e0,e3 |
| 2--3 | e2,e3 | 7--8 | e0,e4 |
| 3--4 | e1,e3 | 8--9 | e2,e4 |
| 4--5 | e1,e4 | 9--0 | e0,e2 |

These are all pairs in a five-element set, hence X_M=K5. A coloring assigning different colors to distance-two matching edges needs five colors, despite every matching edge having only four conflicts. This directly attacks the auxiliary inference identified in the bounded source note.

The graph itself has a star six-coloring. In matching-edge order use 1,2,3,4,5. In cyclic edge order 0--1,1--2,...,9--0 use

    3,4,1,3,6,3,2,6,2,5.

The supplied generator checked all fifteen two-color component graphs for this coloring. Thus the auxiliary counterexample is explicitly NOT a root counterexample. The source's later use of five matching colors for G0 is also distinct from the four-color inference; it is not silently discarded.

## 3. Why exactly 243 split constructions cover the entire subclass

Since X_M has five vertices and M is perfect, G has ten vertices. It is cubic, so E(G) has fifteen edges and F=G-M has ten. Each of the ten pairs of matching edges must have at least one F edge joining their endpoints. Every F edge joins distinct matching edges: a loop is excluded and an extra edge joining the endpoints of one matching edge would violate simplicity. Ten F edges serving ten distinct pairs means exactly one F edge for each pair.

At the two endpoints of matching edge i, the four other matching labels are split into two groups of size two. As the two endpoints can be interchanged, an unordered split of four labeled objects into two pairs has precisely three possibilities. Label the endpoint containing the least other label as 2i, the other endpoint as 2i+1. Sorting the other labels as ns[0],...,ns[3], the first pair is

    {ns[0], ns[di+1]},  di in {0,1,2}.

Each of the five matching edges chooses one of three splits, giving exactly 3^5=243 labeled descriptions. Label permutations can identify descriptions; no claim of 243 isomorphism types is made.

Conversely, every tuple (d0,...,d4) gives an actual graph: add five edges (2i,2i+1), then for each i<j join the unique endpoint at i assigned label j to the unique endpoint at j assigned label i. No loop or duplicate edge is introduced. Each endpoint has two nonmatching edges plus its matching edge, so the graph is cubic. It is connected because contraction of M gives K5, and the two endpoints in each contracted block are joined. Its matching conflict graph is K5. This proves realizability as well as exhaustive coverage, not just coordinate-wise validity.

## 4. The complete coloring certificate

The file `opg37271-c17-k5-matching-certificate.json` contains one ten-digit color word for every ternary tuple in lexicographic order. Index is sum(di*3^(4-i)). Matching edges receive 1,...,5. The ten remaining edges are ordered by K5 pair (i,j), i<j, lexicographically; the word gives their colors in {1,...,6}.

Each row reconstructs an explicit graph and a complete coloring. The table has 243 rows with no missing or substituted abstract states. Any injective assignment of five of the six named colors to M is obtained by one global permutation of the canonical coloring, fixing the unused-color mapping as well; a permutation preserves every star-coloring constraint.

Generator `opg37271-c17-k5-matching-check.py` enumerates every tuple, searches the ten uncolored edges with matching colors fixed, and screens all incident-edge pairs plus all simple four-edge paths and four-cycles. It then checks the candidate coloring by a different method: every two-color connected component must be an acyclic path with at most three edges. Observed total search nodes: 3,026; maximum for one tuple: 32. These counts describe this deterministic generator, not a trusted solver or a graph-isomorphism enumeration.

## 5. Solver-free replay and exact scope of validation

`opg37271-c17-k5-matching-replay.py` does not import the generator, invoke search, or infer acceptance from its success fields. It reads the 243 words, decodes each index, reconstructs the graph, checks simplicity, cubic degree, properness, connectivity and the K5 conflict relation, then enumerates ALL ordered five-vertex tuples and ordered four-vertex tuples. Whenever they form a four-edge simple path or four-cycle, its alternating color equalities must fail.

Observed replay totals: 243 graph/coloring pairs; 52,020 oriented simple four-edge paths; 4,680 oriented four-cycles. All supplied colorings passed. Mutation fixtures remove one row, insert color 7, force an incident color clash, and shorten a row; all were rejected with explicit errors. Both path and cycle tests occur in the source; the mutations do not claim to test every possible defect class.

A solver-free replay is algorithmic separation, NOT a separate trust domain. The result lives under candidates, not receipts. It records the exact input and replay-source SHA-256 values. Both programs use CPython 3.13.5 and the standard library, one thread, wall alarm 30 seconds, CPU limits 30/31 seconds, address-space limit 512 MiB. Generator and certificate input are bounded to 262,144 bytes; replay output to 65,536 bytes. A separate bounded G0 check took eleven search nodes. No repository verifier, Lean command, EvidenceLink or Result admission was run.

Reproduction: in a disposable copy of these candidate files, run the generator once, then run the solver-free replay. The files write their outputs beside themselves. For certificate verification alone, only the certificate and replay program are needed. External checking should freeze both hashes first and separately audit the manual coverage argument, graph encoding, quantifiers and permitted axioms.

## 6. Consequence, unresolved route and source boundary

Within the connected simple cubic / perfect-matching route, a hypothetical root counterexample cannot belong to the fully covered K5-conflict subclass, subject to verification of this candidate. If a connected cubic graph has a K5 component in X_M, it is the whole conflict graph: connectivity of G implies connectivity after contracting M. Thus this statement also excludes a hidden K5 conflict component in that setting.

The remaining route is not settled by replacing four matching colors with five: the complement still needs a compatible star coloring using only six colors in TOTAL, with colors potentially shared across the decomposition. Counting colors of two parts separately does not give that conclusion. No unrestricted matching-precoloring extension theorem is assumed.

The full source's root theorem is not accepted or rejected from one auxiliary error. The new positive result is our finite coverage/certificate candidate, not an attribution of these 243 constructions to the paper. No novelty claim is made. C14's cubic-completion reduction and the existing root contract remain relevant; fixed-coloring tree obstructions are not re-used as root witnesses.

Best verified result: none. Best verified candidate: none. Open obligations: the admitted leaf target and root. State: nonterminal.
Next exact action: derive the matching-color/complement interaction constraints, test a restricted cycle-precoloring extension invariant on actual realizable inputs, and continue the source theorem audit without inferring global closure from its title or abstract.
