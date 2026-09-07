# C20: exact signed cores, witness preservation, and outer-frame repairs

Verdict: `candidate_only`. Package state: `RESULT_CANDIDATE_READY`.
Primary owner: math-proof. Candidate: candidate:opg37271-c20-proof.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Frozen input revision: ddc49c1978a196490702150bb75264793a658457.
Transport binding: attempt:web-20260906-opg37271-a01; route:leaf-extension-six-colors-v1;
graph:opg37271-initial-v1; obligation:opg37271-leaf-extension.
This binding is transport provenance, NOT an assertion that C19-E proves the leaf obligation.
The leaf and root obligations remain open. No trusted receipt or admission is supplied.

## 1. Exact definitions and statement

Let G be a finite simple undirected graph of maximum degree at most three, with E(G)=D disjoint-union U. A coloring is proper when incident edges differ. A star edge coloring is proper and has no bichromatic simple path of FOUR EDGES (five distinct vertices) or simple cycle of FOUR EDGES (four distinct vertices). Paths need not be induced. Give D a fixed star coloring c:D->A={1,2,3,4}. The nonempty connected components of (V(G),U) are pairwise vertex-disjoint paths with one, two or three edges. The family may be empty; isolated vertices carry no variable. An allowed completion retains c and uses only B={5,6} on U.

Orient each U path P once, and let p(e) be the zero-based edge index modulo two. For each phase vector x assign

    c_x(e)=c(e) for e in D;  c_x(e)=5+(x_P XOR p(e)) for e in P.

For EVERY actual four-edge simple path or four-cycle W whose edge memberships alternate D/U and whose two D edges have equal c-color, write its U edges as e in P and f in Q and generate the labelled row

    x_P XOR x_Q = b_W,     b_W=1 XOR p(e) XOR p(f).             (1)

Retain a witness consisting of W's vertex sequence, edge indices, two U edges and two D edges. Selection is phase-independent. In this package distinct actual shapes retain distinct row occurrences, even if their algebraic rows agree. Algebraic deduplication is safe only when the FULL triple (unordered variable pair, right side) agrees; the outer repair below still tracks ALL supporting witnesses.

C20-T1: for each phase x, c_x is star iff x satisfies every row; allowed completion exists iff the signed row graph is balanced (every cycle has sign XOR zero).
C20-T2: its inclusion-minimal unsatisfiable row subsets are exactly negative simple cycles of the signed MULTIGRAPH, including a sign-one loop and a pair of opposite-sign parallel edges. A minimum-cardinality core is a shortest such cycle. The algorithms below extract both kinds and preserve actual graph witnesses.
C20-T3: the explicit spare-color/induced-matching forest condition in Section 6 allows a specified change of the outer D coloring that eliminates all cores. A second sufficient condition covers some frames using all four A colors without any D recoloring.
C20-T4: a complement four-cycle with four distinct strong matching colors and exactly one selected special edge forces a one-row core, regardless of its permissible A color. Section 7 attains the minimum order for this SPECIFIED structural class, not for all inconsistent C19 frames.

The negation of T1 requires an input satisfying all its premises with a star completion on just one side of the asserted equivalence. A failed phase, failed frame choice, or no suitable outer decomposition is not a counterexample to T1 or to the root. T3 explicitly releases some D colors and is NOT a completion of the original fixed D instance.

## 2. Definition-level reaudit of C19-E

P1. Every proper B coloring on a U path is uniquely specified by its first edge. At index zero choose its phase; if the formula holds at j, properness and the two-element palette force the opposite bit at j+1. Induction on the index gives exactly c_x. Conversely c_x alternates. The disjoint U components have separate choices. For empty U there is one empty phase and one empty U coloring.

P2. Every c_x is proper: D/D incidence is proper by hypothesis; U/U incidence lies in one path and alternates; D/U incidence has disjoint palettes. These three cases exhaust incidence.

P3. Any bichromatic four-edge path or cycle in a proper coloring alternates two colors, each occurring twice. If both colors lie in A, the whole shape is in D, excluded by its star hypothesis. If both lie in B, its four edges lie in a single U component, impossible with at most three edges. Otherwise its memberships alternate D/U, and its D colors agree. Conversely a selected actual shape is bichromatic exactly when its two U colors agree. Equivalently, enumerate by number of U edges: zero is the old case; four violates the U premise; one or three cannot supply two occurrences of each color from disjoint palettes; two must be opposite positions, with equal D colors. This includes the closing adjacency of C4.

P4. On each selected shape, unequal U colors mean

    (x_P XOR p(e)) XOR (x_Q XOR p(f))=1,

which is equivalent, by reversible addition in F2, to (1). Thus a row is neither an omitted restriction nor a stronger arbitrary restriction: it exactly protects its own shape.

P5. If c_x is star, each selected shape is safe, hence every row holds by P4. If all rows hold, P2 gives properness; any alleged forbidden shape would be selected by P3 and violate its row by P4. This proves pointwise equivalence. Apply P1 in each direction for the existential equivalence. No coloring assertion of C18M or C17D is used.

Boundaries: U empty has no rows and the old D coloring is already full; the empty graph is included. D empty has separate alternating short paths. For P=Q do not remove the row. The two opposite U edges in a selected simple shape are disjoint. Within one path of at most three edges they must be its first and third edges; their parities are equal, and (1) is 0=1. A general algebraic sign-zero loop is tautological, but does not replace this real sign-one row. Extra graph chords do not destroy a simple path. A four-cycle's two complementary simple arcs are edge-disjoint; an alleged cycle obtained by joining arcs with overlapping edges must first be checked for four distinct vertices and four distinct edges, not treated as C4 by drawing alone.

## 3. Balance theorem, including shared arcs

The signed graph K has one vertex per U component and one distinct labelled edge per row occurrence, sign b_W. It may have loops and parallel edges, even though G is simple. A cycle is a loop, a two-edge parallel cycle, or an ordinary cycle with distinct intermediate vertices and distinct edges. Its sign is the XOR of its signs, NOT the parity of its length.

If an assignment satisfies all edges of a closed walk, summing those equations cancels each phase variable an even number of times. Its sign XOR is zero. This reasoning counts edge OCCURRENCES. Two root paths that share a prefix contribute that prefix twice, so it cancels; taking their set union instead is incorrect.

Conversely build a spanning forest of the loopless underlying graph. Fix one phase zero in each component and propagate x_v=x_u XOR b along its tree edges. The number of unassigned vertices strictly decreases at each assignment. For a non-tree edge uv, its tree path together with uv is its fundamental cycle, including the parallel-edge case. Sign-zero of that cycle is exactly x_u XOR x_v=b_uv. A loop is satisfied exactly when its sign is zero. Thus the assignment satisfies all rows. Each component allows exactly two common flips, so a consistent graph with z components has 2^z solutions, including 1 when K is empty.

Every closed walk decomposes into simple cycles and backtracks by splitting at repeated vertices. Sign XOR is additive under that splitting; a backtrack contributes b XOR b=0. Hence it is enough to test simple cycles. In particular, if two non-tree arcs share edges, cancel common occurrences modulo two, decompose the remaining Eulerian edge set into cycles, and retain one sign-one cycle when the total sign is one. There is no assumption that the original graph witnesses are disjoint. Summing ROWS cancels phase coefficients; it does not cancel colors or claim the union of their G-witnesses is a single simple path or cycle.

## 4. Exactly the minimal cores; two extraction algorithms

An unsatisfiable row set contains a sign-one simple cycle by the balance theorem and the forest conflict construction. That cycle is already unsatisfiable because its sum is 0=1. Every proper subset of its edges is a forest, possibly with isolated vertices; it is satisfiable by tree propagation. For a loop, its only proper subset is empty. Thus each sign-one cycle is inclusion-minimal unsatisfiable. Conversely an inclusion-minimal unsatisfiable set must equal its contained negative cycle, proving T2.

Algorithm A (linear-time inclusion-minimal extraction). Run breadth-first tree propagation, storing the parent vertex and row index when assigning each vertex. On the first inconsistent row uv, extract the root-to-u and root-to-v TREE row sets. Return their SYMMETRIC DIFFERENCE plus this inconsistent row. The shared prefix cancels, leaving precisely the unique u-to-v tree path and its closing row. A self-loop returns just itself. It is a negative simple cycle and therefore an inclusion-minimal core. Work is O(k+m) and memory O(k+m), including extraction; k is the number of variables and m the number of row occurrences. This core need not have globally fewest rows.

Algorithm B (minimum-cardinality extraction). Form the parity double cover with vertices (v,t), t in {0,1}. A row uv of sign b creates transitions (u,t)--(v,t XOR b) for both bits, retaining its row index. For each base vertex v run BFS from (v,0) to (v,1); take a shortest of ALL successful searches. Project its row sequence to K. It is a closed walk of sign one. If it repeated any base vertex internally, splitting there gives two shorter closed walks, at least one of sign one. That would give a shorter successful BFS path from some (w,0) to (w,1), contradicting the GLOBAL minimum. The projection is consequently a negative simple cycle (loops and parallel pairs included). Every unsatisfiable subset contains such a cycle, and every such cycle is an unsatisfiable subset, so this is globally minimum in NUMBER OF ROWS. Complexity O(k(k+m)), memory O(k+m) when searches are sequential. It does not minimize the number of G vertices or unique G edges used by witnesses.

Algorithm outputs retain row indices and actual witness records. For each returned core, check each row's four graph edges, vertex distinctness, D/U alternation, fixed-color equality and index parities anew. Verify the row sum 0=1 and supply a satisfying phase after deletion of each core row. Positive assignments are decoded and directly checked on G. For a negative certificate, a witnessed inconsistent subset suffices; for positive acceptance, the complete row family or the full coloring must be checked.

For r core rows, a bounded actual obstruction subgraph is obtained by taking all their witness edges and ALL U edges in every represented variable component. A simple core cycle has r represented variables (including the loop and parallel conventions), so this union uses at most 4r+3r=7r distinct graph edges. Restriction preserves the D-star coloring; the included full U paths preserve all recorded p(e) and connectivity. Every core witness remains. The union is therefore a genuine uncompletable restricted frame. The bound can overcount shared edges, and is not a claim of smallest graph order.

## 5. Graph-bound replay and attacks

The input is the main C19 certificate with SHA-256
`9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3`.
The new compiler imports neither old C19 program nor the C19-E audit. It classifies FOUR-EDGE SUBSETS by connectivity and degree pattern, rather than generating their shapes by the old vertex-permutation or path DFS code. It retains chords in G and all support occurrences. The direct coloring predicate instead explores each two-color connected component after testing properness. It is still in the SAME generator trust domain; algorithmic diversity does not confer a stronger role.

The six-cycle has six actual mixed path rows but three distinct algebraic inequalities. The minimum extracted core has three rows, each a real four-edge path; they share original G edges. Its sum is 0=1. All eight phases fail direct coloring. The stored eight-vertex positive graph produces eight support rows, three distinct algebraic rows and exactly two phases, (0,1,1,0) and (1,0,0,1). Each stored old witness is checked from its edge table, and the complete algebraic row set is compared, without trusting old success fields.

Real self-loop and contradictory-parallel fixtures have minimum row cores one and two respectively. A separate shared-root-prefix signed graph detects an erroneous UNION extraction and returns only the three cycle rows. A positive all-zero-sign triangle and a negative four-cycle with signs 0,0,0,1 show why ordinary odd graph length is not the criterion. A zero-sign loop is harmless. Empty U, empty G, and a three-edge U path are positive controls.

Fifteen fresh test invocations distinguish or reject: omitted C4, deleted self rows, deduplication ignoring signs, induced-only paths, removed XOR constant, repeated witness vertex, palette crossing, U length four, nonstar D, wrong shared-prefix cancellation, duplicate core row, missing core row, nonspare outer recoloring, unhit outer core and a non-induced recoloring matching. Exact error/disagreement witnesses are in the certificate. All 512 subsets of the nine signed atoms on three variables (three sign-one loops, both signs of each distinct pair) compare Algorithm B with exhaustive row subsets and Boolean assignments. The extra sign tests above add length-four and tautological-loop coverage. These are bounded diagnostics, not an arbitrary-size proof.

## 6. Two explicit sufficient outer-frame conditions

### T3a: safely erase all cores using a spare color

Assume the fixed D coloring omits some alpha in A. Let R be an INDUCED MATCHING of D edges in G: their endpoint sets are disjoint and no graph edge joins endpoints of two different R edges. Let T be a set of algebraically distinct rows whose underlying multigraph is a spanning forest of K; a spanning forest need not retain loops, and it retains at most one edge per variable pair.

Hypothesis: for EVERY actual witness row whose full triple (unordered variable pair, sign) is NOT the triple of a T edge, at least one of that witness's two D edges lies in R. The universal quantifier is over all support witnesses, not just a chosen representative. Exact parallel duplicates of a T row may remain.

Simultaneously recolor every R edge with alpha, retaining all other D edges and retaining D/U. This new D coloring is proper because alpha was unused and R is a matching. A new two-color forbidden shape in D would have to use two alpha edges separated by a single graph edge, impossible for an induced matching. Forbidden shapes with no alpha would already have existed. Thus D stays star.

A newly selected mixed witness would have equal D colors. If neither D edge changed, its selection is unchanged. If exactly one changed, equality is impossible because alpha was unused. If both changed, the two R edges are separated by one U edge of this alternating shape, again impossible for an induced matching. Consequently the new support-row list is EXACTLY the old list with all witnesses touching R removed; no sign or U parity changes. Every remaining algebraic row is a T row. The remaining system is a subset of a forest, with harmless identical duplicates, and is consistent. T1 decodes a star completion of the modified frame.

This operation terminates after at most |R| prescribed recolorings. Properness, D-star validity, unchanged U and absence of new support rows are invariants. The number of unrecolored R edges strictly decreases. Finding an R meeting the hypothesis is an OUTER existence question left open; the theorem does not assume every frame has a spare A color. It does not promise to preserve the original fixed D coloring or retain its prescribed matching colors.

On the six-cycle, recolor edge01 from 1 to 2, with R={01}. Of the six actual rows, four disappear; the remaining two are x_0 XOR x_1=1 and x_2 XOR x_1=1, a two-edge tree. The full cycle coloring becomes (2,5,1,6,1,5). The certificate checks the hypothesis and direct star property. Recoloring just one representative's D edge is NOT valid evidence of erasing an algebraic row when another witness survives.

### T3b: contact parity coherence with all four A colors

For each U component P, suppose every edge of P occurring in any selected witness has the same parity t_P (choose t_P=0 for no contact). Suppose no selected row is a self-row and the graph of contacts BETWEEN U components is bipartite, with vertex bit y_P differing across every contact. Then every row sign is 1 XOR t_P XOR t_Q. Put x_P=y_P XOR t_P. Across a contact, x_P XOR x_Q=1 XOR t_P XOR t_Q, so all rows hold. This gives an allowed star extension without changing D, and permits all four colors in A. It is a concrete sufficient condition, not a necessity or universal outer-frame theorem. The original positive eight-vertex frame satisfies it with all t_P=0.

## 7. An exact minimum-order obstruction to a stronger local frame rule

Let M be a specified perfect matching with colors lambda(v) in A, such that matching edges joined by any G edge have different colors (strong matching coloring). Put F=G-M. Let S be a matching of F edges assigned A colors avoiding their two endpoint matching colors; D=M union S is star: it is a union of two matchings, and any four-edge D shape contains an M-S-M triple with distinct M colors. This last assertion is proved here and not imported from a previous candidate. Assume F-S consists of paths of at most three edges, so C19 applies.

Suppose abcd is a four-cycle in F, its matching labels lambda(a),lambda(b),lambda(c),lambda(d) are all four distinct A colors, and exactly one of its edges belongs to S, say da. Its U path is a-b-c-d. Properness allows the color of da to be only lambda(b) or lambda(c).

If c(da)=lambda(b), the actual path mate(b)-b-a-d-c has edge types D,U,D,U. If c(da)=lambda(c), use b-a-d-c-mate(c), with types U,D,U,D. In both cases the U edges are ab and cd, the first and third edges of the SAME U path. Their parities agree. Each displayed path gives x_P XOR x_P=1. The matching mates used lie outside the four-cycle: otherwise two of its lambda values would agree. The witnesses really have five distinct vertices, even if other graph edges add chords.

Therefore NO permissible special-edge color repairs this one-special-edge frame. To avoid this particular core while retaining the matching and labels, the four-cycle needs two opposite special edges, rather than merely a different color on the one selected edge. This attacks a more restrictive local construction, not unrestricted star six-colorability or C19-E.

The main eight-vertex positive graph realizes the smallest possible order for this distinct-label four-cycle class. Its matching is (0,4),(1,5),(2,7),(3,6), colored 1,2,3,4; its complement is the two four-cycles already in C19. Choose only S={(3,0),(7,4)}. The four available S-color pairs are (2,2),(2,4),(3,2),(3,4), and every one has a one-row contradictory core, explicitly recorded. Restoring S={(1,2),(3,0),(5,6),(7,4)} with colors1,2,1,2 gives the original positive frame and its full coloring. Lower bound eight in the stated class: the four cycle vertices have four distinct matching edges, and their four mates are distinct vertices outside the cycle. No global minimum-order claim for all bad frames is made.

## 8. Discipline, execution, and next gate

The proof dependency chain is definitions -> phase bijection/properness -> full forbidden-shape classification -> exact row algebra -> balance -> cycle-core classification -> algorithms and witness map -> T3 outer conditions. T4 uses the definitions and a separately proved matching-frame D-star premise. Every universal assertion above has a supplied mathematical argument; executable tests are limited to their declared sizes. Only finite graph reasoning and F2 arithmetic are used. No external theorem, unproved probabilistic assertion, limit passage, hidden induction or extreme-order assumption is needed. Symmetry is limited to proven phase orientation changes and componentwise bit flips; no isomorphism quotient is used in testing.

The implementation caps graph order at16, graph size at24 and signed rows at4096. Four-edge subset enumeration costs O(|E|^4) in this diagnostic implementation; it is not the bounded-degree linear compiler claimed by an optimized traversal. Algorithm A/B complexities refer to their explicit signed input. Test process budgets are wall35s, CPU30/31s, address space256MiB, one thread, output files at most262144 bytes; the runner enforces outer40s and bounded stdout/stderr. The exact actual invocation is saved separately with source, input, output and interpreter fingerprints. No Lean, kernel, registered verifier or repository adapter was executed.

The registered Lean adapter requires a registered candidate, an exactly corresponding admitted obligation, source/declaration identity, an allowlisted toolchain fingerprint, and semantic review. Current records do not contain a C19-E/C20 obligation; reusing the leaf statement would be a semantic error. The current sole GitHub workflow is transport-only. The executable admission preflight request documents these gaps and requests trusted coordination and a future matching formalization; it does not manufacture them or edit truth files.

Best available candidate: T1-T4 plus exact graph-bound core and mutation data. No root solution or trusted admission. Historical missing-material classes remain unchanged and unused. Next gate: trusted admission of the exact local statements and corresponding formal source/candidate, toolchain allowlisting, a permitted verifier execution entry, separate statement-faithfulness and axiom/escape review, and only then obligation closure. The failed local one-special-edge rule is a proposal in this packet, not a direct failed-route ledger edit.
