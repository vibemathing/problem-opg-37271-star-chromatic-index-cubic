# C19-E: pointwise phase equivalence and two falsification passes

Verdict: `candidate_only`. Package state: `RESULT_CANDIDATE_READY`.
Primary owner: `math-proof`; bounded checking support: `math-computation`.
Candidate ID: `candidate:opg37271-c19e-audit-proof`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Admitted target: `obligation:opg37271-leaf-extension`; root remains open.
Frozen input revision: `cedbfc277c39317e0d2998733b2d7b45670bac63`.
Target source: `research/artifacts/candidates/opg37271-c19-phase.md`, Sections 1-3.

This package audits ONLY C19-E. Readiness concerns this candidate package, not a Result, an EvidenceLink, or closure of either admitted obligation. No premise is taken from an old chat, CI success, or a saved success field. Historical missing materials remain missing and are not inputs.

## 1. Frozen statement, including the exact negation

G is a finite simple undirected graph with maximum degree at most three. E(G)=D disjoint-union U. The given map c:D->{1,2,3,4}=A is a star edge coloring of the subgraph (V(G),D). The nonempty components of (V(G),U) are vertex-disjoint simple paths of one, two or three edges. Isolated vertices are irrelevant; the path family may be empty. Paths in G are simple, NOT required to be induced. A forbidden four-cycle has four distinct vertices. A star edge coloring is proper and has no bichromatic simple four-edge path or four-cycle.

The only allowed extension keeps every D color and gives every U edge a color in B={5,6}. Orient and order every U component P. For e in P, let p(e) be its zero-based index modulo two. Give P a bit x_P and define

    c_x(e) = c(e)                    for e in D,
    c_x(e) = 5 + (x_P XOR p(e))       for e in U belonging to P.

Enumerate ALL actual four-edge simple paths and four-cycles of G. Select a shape precisely when its memberships alternate D,U,D,U or U,D,U,D and its two D colors agree. If its U edges e,f belong to P,Q, add

    x_P XOR x_Q = 1 XOR p(e) XOR p(f).                  (E)

Selection uses the graph and the given D colors, not a guessed final coloring. 'Bichromatic shape' here means a potential mixed obstruction satisfying that explicit selection rule. Do not select only shapes that fail under one test phase.

C19-E asserts that an allowed star extension exists if and only if all equations (E) are consistent. Its exact negation is an input satisfying ALL the preceding hypotheses for which one side is true and the other false. A failed particular phase, a failed outer frame, or a graph without such a decomposition is not that negation.

## 2. Line-auditable proof and dependency chain

Only finite-graph-basic, finite-combinatorics, and explicit arithmetic on bits are used. The local claim dependency chain is H -> L1 -> L2 -> L3/L4 -> L5 -> L6. These labels are within this document, not new admitted DAG nodes.

**L1 (phase bijection; hypotheses H).** On an oriented U path, a proper coloring using exactly the available palette B is determined by its first-edge color. At index zero the formula above agrees with that choice. If it agrees at index j, properness and the fact that B has two elements force the other color at index j+1. Induction over the indices proves the formula on the whole path. Conversely, the formula alternates and is proper. Components share no vertices, so these choices impose no mutual properness constraints. Each component has a first edge, making the correspondence injective as well as surjective. For an empty family, there is exactly one empty bit assignment and one empty U coloring.

**L2 (global properness; L1 and H).** Every c_x is proper. Two incident D edges differ by the given properness of c. Two incident U edges are consecutive edges in one U path and differ by L1. An incident D/U pair uses disjoint palettes A and B. These exhaust all incident pairs.

**L3 (all possible new forbidden shapes; L2 and H).** In a proper coloring, a bichromatic four-edge path or cycle must alternate its two colors: consecutive colors differ, so each position forces the next. Each of its two colors occurs exactly twice. If both colors lie in A, all four edges lie in D, contrary to the given star property. If both lie in B, all four edges lie in a single connected U component, contrary to that component being a path of at most three edges. The remaining case has one color in A and one in B. Its D/U memberships therefore alternate, and the two D colors are equal. Thus every possible new forbidden shape is selected by the rule above. Conversely, a selected actual shape becomes forbidden exactly when its two U colors agree.

For an explicit count-by-membership audit: zero U edges are the already-valid D case; four U edges cannot fit in U; one or three U edges cannot give two occurrences of each disjoint-palette color; two U edges must occupy opposite positions. Two adjacent U positions cannot alternate membership. With two opposite U positions but different D colors there are at least three colors, so no equation should be generated. The same argument applies to the closing adjacency in a four-cycle.

**L4 (exact row algebra; definitions).** On a selected shape, the U colors differ if and only if

    (x_P XOR p(e)) XOR (x_Q XOR p(f)) = 1,

which, after XOR with p(e) XOR p(f) on both sides, is exactly (E). This manipulation is reversible, including P=Q. No row is a mere sufficient extra restriction: each is necessary and sufficient to make its own actual selected shape safe.

**L5 (pointwise equivalence; L2-L4).** For EVERY phase assignment x, c_x is star if and only if x satisfies every generated row. Forward: c_x is proper and star, so each selected shape must have unequal U colors, hence satisfy its row by L4. Reverse: c_x is proper by L2. If it had a forbidden shape, L3 would select it and L4 would make its row false, contradicting the assumed conjunction.

**L6 (existential equivalence; L1 and L5).** Every allowed star extension is proper and therefore has the phase representation from L1; L5 gives a solution of the equations. Conversely, any solution gives the explicit allowed extension c_x, which is star by L5. This proves the proposed necessary-and-sufficient condition for the frozen range, without assuming that an outer frame can always be chosen.

## 3. Boundary cases and signed contradictions

U empty: there are no variables or rows. The empty system is consistent and the given coloring is already a star coloring of all G. This includes the empty graph. D empty: the U paths may all be independently alternated; no mixed row exists.

Same U component twice: P=Q gives the literal equation 0=1 XOR p(e) XOR p(f); never discard it just because the two variable names coincide. The two U positions of a simple selected shape are disjoint edges. In a U path of at most three edges, two disjoint edges of that same component must be its first and third edges; hence their parities agree, and the row is 0=1. This possibility is realizable, as the fixture below shows. A tautological signed self-row, when encountered by a general algebraic routine, is harmless, but it is not substituted for this contradictory row.

Parallel rows: equal ordered or reversed variable pairs and the SAME right side may be deduplicated. Opposite right sides must both remain, since their sum is 0=1. Simple G does not imply a simple signed constraint graph.

Non-induced paths: additional chords neither delete a simple path nor change the colors of its four selected edges. The witnesses must keep pairwise distinct path vertices even when chords exist. A four-cycle has four, not five, distinct vertices and is checked separately.

Orientation: reversing a path of m edges changes p(e) by the constant (m-1) modulo two. Changing x_P by the same constant leaves c_x unchanged and transforms every incident row consistently. Renaming components similarly only renames variables. No quotient of old color labels is used.

For the negative certificate rule, regard each row as a signed multigraph edge. Along any closed walk, every phase variable occurs an even number of times, so consistency implies that the XOR of the signs is zero. Conversely choose a root value in each component, and assign every vertex the root bit XOR the signs on a spanning-tree path. These values satisfy all tree edges. A non-tree edge is satisfied because its fundamental closed walk has sign XOR zero. Loops and parallel edges are included in this argument. The number of unassigned vertices strictly decreases during tree propagation, so it terminates. A connected component contributes one free bit; isolated variables are included. Thus a consistent system with z components has exactly 2^z assignments, including 2^0=1 for no variables.

## 4. Falsification pass 1: definition-level and boundary attacks

The proof's complete membership classification was checked against the following actual graphs. Zeros below denote uncolored U edges, not an additional color.

**Four-cycle-only constraint.** Edges (01,12,23,30), partial colors (1,0,1,0), produce x_0 XOR x_1=1. There is no five-vertex path in this graph. Omitting four-cycles admits phase (0,0), yielding the forbidden colors (1,5,1,5).

**Non-induced path and contradictory self-row.** Edges (01,12,23,13,24), partial colors (0,0,0,1,1). U is the path 0-1-2-3, and D is a matching. The actual simple path 0-1-3-2-4 uses U edge indices 0 and 2, both with parity zero, and produces x_0 XOR x_0=1. The U edge 12 is a chord of that selected path. Either retaining only induced paths or dropping self-rows incorrectly accepts the colors (5,6,5,1,1).

**Opposite parallel rows.** Edges (01,12,34,03,24), partial colors (0,0,0,1,1). U components are 0-1-2 and 3-4. Path 1-0-3-4-2 requires x_0 XOR x_1=1. Path 0-3-4-2-1 requires x_1 XOR x_0=0. Collapsing rows solely by variable pair loses a real contradiction.

**Overconstraint attack.** On the path 0-1-2-3-4 use partial colors (1,0,2,0). The fixed colors differ. All four phases are valid; a compiler that ignores the fixed-color-equality guard falsely rejects phase (0,0).

Also check the empty graph, U empty on a four-colored cycle, and U paths of lengths one, two and three. There are nine boundary fixtures in total. All their phase assignments agree between the equation test and a direct two-color-component coloring test. Reversing component orientations in all 22 fixture orientation choices preserves the sets of complete colorings.

As a finite implementation pressure test, enumerate all 5^4=625 partial words in {0,1,2,3,4} on each of P5 and C4. On P5, 364 inputs meet the premises and require 736 phase trials. On C4, 312 inputs meet the premises and require 616 trials. Every one of these 1,352 phase comparisons agrees. The remaining 574 partial words fail premises and are NOT counterexamples. This is finite coverage of these two shapes, not induction on arbitrary graphs.

Six deliberately incorrect compiler variants are caught: omission of cycles, induced-only path filtering, dropping self-rows, merging opposite parallel rows, omitting the constant one in (E), and ignoring fixed-color equality. The generated audit certificate stores an actual disagreeing phase and its full colors for each variant. These are counterexamples to the altered implementations, NOT to C19-E.

Premise attacks separately reject U of length four, U a cycle, branching U, non-star D, and a reserved B color on D. Without the length premise, for example, D empty and U=P5 give an empty mixed system but no star alternating B coloring. The original theorem explicitly excludes that input.

## 5. Falsification pass 2: fresh graph-bound replay of main certificates

The only computational input is the main file `opg37271-c19-phase-certificate.json` at the frozen revision. Its 2,703 exact bytes have SHA-256

    9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3

and reproduce the fetched Git blob `10dd8d8da144381686be83164f7dd14586f614f2`. Historical runtime, success, 6,144-frame and 55,296-assignment fields are not premises or replay results.

The new checker imports neither old C19 source. It reconstructs U components from the edge table, enumerates actual shapes by vertex permutations, rebuilds the complete signed row set, and compares every phase against a separate properness/two-color-component test. Each stored witness is also checked for vertex distinctness, edge incidence, D/U alternation, fixed color equality, component indices and row parity. Equality of the complete normalized row sets is checked in both named source frames.

**Six-cycle negative certificate.** E is (01,12,23,34,45,50), partial colors (1,0,1,0,1,0), and U components are edge indices [1],[3],[5]. The three witnesses are 0-1-2-3-4, 0-5-4-3-2, and 2-1-0-5-4. Recomputed rows are

    x_0 XOR x_1=1, x_2 XOR x_1=1, x_0 XOR x_2=1.

Their sum cancels every variable and has right side one. All eight phases fail the direct coloring test. The wider-palette word (1,4,1,5,1,6) also passes direct checking, but is not a B-only extension. This is a structural obstruction for restricted completion, not for the root.

**Positive eight-vertex certificate.** In edge order

    (04,15,27,36,01,12,23,30,45,56,67,74),

the partial colors are (1,2,3,4,0,1,0,2,0,1,0,2). The U edge indices [4],[6],[8],[10] are four singleton paths. The complete recomputed equations are

    x_0 XOR x_2=1, x_2 XOR x_3=1, x_1 XOR x_0=1.

Their graph is connected. All sixteen phases were directly tested; exactly (0,1,1,0) and (1,0,0,1) pass. The first gives the complete edge-color word

    (1,2,3,4,5,1,6,2,6,1,5,2).

The source's other 24 supplied complete colorings were also reconstructed on their actual matching-permutation graphs and checked directly. This does not redo the full historical partial-frame tally.

Eight certificate corruptions are rejected: incorrect row sign, repeated witness vertex, invalid edge index, incomplete contradiction, a missing positive equation, wrong phase, wrong full coloring, and an incorrect U-path list. With the five premise mutations in Section 4, thirteen malformed inputs are rejected. Tests do not prove that every possible checker defect is absent.

## 6. Execution, reproducibility and limits

Files: `opg37271-c19e-audit-check.py`, `opg37271-c19e-audit-run.py`, `opg37271-c19e-audit-certificate.json`, `opg37271-c19e-audit-result.json`, and `opg37271-c19e-audit-execution.json`, all beside this document.

From the repository root run:

    python3 research/artifacts/candidates/opg37271-c19e-audit-run.py

The runner verifies the input digest before launching the checker, verifies the returned source/input/certificate digest bindings, and records the actual exit code, interpreter, timing and output hashes. It uses the standard library only. The final frozen run used CPython 3.13.5, returned zero with empty stderr, and was not timed out. Read the execution JSON for exact timestamps and hashes rather than treating this paragraph as an execution receipt.

Bounds: checker wall alarm 35 seconds, CPU soft/hard 30/31 seconds, address-space cap 256 MiB, one thread, 262,144 bytes per generated certificate file, 16,384 stdout bytes; runner outer timeout 40 seconds and bounded captures. The actual checker certificate is 4,971 bytes. Inputs beyond ten vertices or fifteen edges are rejected by this audit implementation. Its exhaustive path enumeration is O(n^5); phase checking is exponential in the number of U paths. This checker is deliberately a small-instance cross-check, not the linear-time signed-graph solver described in Section 3.

The proof is for all finite inputs in the frozen range, and does not infer that range from these bounds. No GPU, solver, kernel, admitted adapter or repository verification script was run. These are actual local generator-domain checks, not trusted mathematical receipts. The profile's repository-command capability was not changed. The direct user request authorizes this bounded local replay; no unavailable compute-plan or adapter execution is claimed.

## 7. Dependency and discipline audit

C18M, C17D, C17's matching-conflict definition, C14B and C15L were read at the frozen main revision. They explain neighboring routes, but NONE of their coloring/reduction conclusions is a premise of L1-L6. D being star is supplied explicitly here; it is not obtained by assuming a matching construction succeeds. The two-color-component test is justified directly: properness bounds a two-color component's degree by two; a cycle in a simple proper two-color graph has at least four edges, and any path with at least four edges is forbidden. Thus components must have at most three edges. This rederivation avoids importing a pending candidate lemma.

Definitions/negation: frozen in Section 1. Witnesses and counterexample pressure: Sections 4-5. Invariant: the phase formula retains all D colors and properness; every row has a concrete graph witness. Termination: finite traversal/enumeration and a decreasing unassigned-vertex count in the constructive signed argument. Induction: only the explicit edge-index induction in L1 is used. No converse or quantifier reversal is assumed. Symmetry: orientation and component renaming are handled explicitly. Extremal and probabilistic methods are not needed, since no extremal object or random existence assertion is used. Scale: finite tests and the arbitrary-finite proof are separate.

No C19-E counterexample was found in the two stated attacks, and no natural-language proof step is left as an unstated external lemma. Residual assurance tasks are an external check of this fixed package, formalization of phase/witness semantics if desired, and the declared axiom/statement-faithfulness gates. They remain open and are not replaced by this package's readiness.

Best available candidate: L1-L6 plus the regenerated finite certificate, checker, mutants and execution record. Best admitted mathematical result: none. Both existing obligations remain open. Next obligation within this audit: external checking/formalization of the pointwise equivalence against the same frozen definitions, NOT an outer-frame existence theorem or a root coloring claim.
