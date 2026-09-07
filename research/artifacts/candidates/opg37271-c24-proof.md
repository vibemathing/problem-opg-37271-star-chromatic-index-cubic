# C24 — a closed positive plateau in the COMPLETE preframe space

Verdict: `candidate_only`. State: `NONTERMINAL_CHECKPOINT`.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input main: b66703bd76d56f0791ad58542ec8bc7d3b8ee35b. Target: obligation:opg37271-root.
Primary owner: math-proof. No truth record, trusted receipt or root solution is supplied.

## 1. Statement freeze: the tested EXIT claim is stronger than ROOT

ROOT is the frozen universal finite simple subcubic star-six edge-coloring statement.
A star edge coloring is proper and has no bichromatic simple FOUR-EDGE path or FOUR-CYCLE.
Paths need not be induced. No assumption of a perfect matching or supplied factor is added.

A preframe w is a word on E(G) in {0,1,2,3,4}. Its nonzero edges D are star colored;
its zero edges U form vertex-disjoint nonempty paths of length1..3. Empty U and isolated
vertices are allowed. Orient each U component from its smaller endpoint, order components
by minimum edge index, and give component i edge position p color5+((s>>i)&1 XOR (p mod2)).
All phases s are evaluated. Let mu(w) be the MINIMUM number of bichromatic actual shapes
in these decoded proper colorings, paths modulo reversal and cycles modulo dihedral symmetry.
Distinct actual supports are not deduplicated merely because their XOR equations agree.

A move changes ONE word entry among all five possibilities, preserves the preframe premises,
and freely reoptimizes all phases. In the directed nonincreasing graph, w->w' iff the edit
is legal and mu(w')<=mu(w). A directed cycle has constant mu. Hence its SCCs are precisely
the connected components of the equal-mu edit graph. The tested EXIT claim says that EVERY
positive-mu SCC has an outgoing edge to a smaller value.

Equivalently, expand each w into all its phases with free phase-reset arcs and potential
mu(w), not the unoptimized cost at a particular phase. Our counterexample is a singleton
PROJECTED preframe SCC, or FOUR states in this explicit phase expansion. This distinction
prevents suppressing phase choices. Restricting to optimal phases gives two states instead;
closure still follows because no legal new preframe has smaller or equal mu.

The root candidate DAG remains CUBIC + OUTER + DECODE -> ROOT. CUBIC embeds a subcubic graph
in a cubic graph by at most three deficient-vertex doubling rounds and then restricts its
coloring. DECODE is the exact C19/C20 local equivalence. OUTER asks for one balanced preframe
for each connected simple cubic graph. EXIT would be a sufficient global strategy from PRE,
but its universal quantifier ranges over more states than PRE outputs. We negate EXIT, not OUTER.

## 2. The finite cubic graph and a complete phase obstruction

Vertices are0..7. Edges, in the fixed order used in every certificate, are

    01,02,03,12,14,25,34,36,47,56,57,67.

This is simple and connected. The neighbor triples are
0:{1,2,3}, 1:{0,2,4}, 2:{0,1,5}, 3:{0,4,6},
4:{1,3,7}, 5:{2,6,7}, 6:{3,5,7}, 7:{4,5,6}.
Thus it is a COMPLETE connected cubic graph, not a cut-out local gadget.
Take

    w=(0,1,0,2,1,3,0,3,4,4,2,0).

The U paths are1-0-3-4 and6-7; vertices2 and5 are not incident with U.
On the first path the B bits are x,x+1,x, and on the second the bit is y.
Each of the four A color classes in D has two edges: {02,14}, {12,57}, {25,36}, {47,56}.
They are matchings. Any bichromatic shape in D would have to use all four edges of two
classes. For each of the six pairs this four-edge subgraph is disconnected, so D is star.

The entire selected mixed support family is:

| Shape | Vertex sequence | Row |
|---|---|---|
| path | 2-0-1-4-3 | x XOR x=1 |
| path | 3-4-7-6-5 | x XOR y=1 |

To check completeness without trusting a compiler, equal A pairs of colors2 and3 have no
U edge connecting their endpoints. The color1 pair has connector01; its only alternating
four-edge extension uses34 and is the first displayed path. The color4 pair has connector67;
its only alternating extension uses34 and is the second path. No such pair closes a C4.
Every other prospective shape either uses unequal A colors or is excluded by D-star/U-length.
The phase costs, in order s=0,1,2,3, are(2,1,1,2). In particular mu(w)=1.

## 3. ALL48 single-entry modifications: a singleton with no exit

Each of12 entries has exactly four alternatives. The only legal preframe neighbors are:

| Changed edge | Old -> new | ALL phase costs | mu |
|---|---|---|---|
| 25 | 3 -> 0 | 6,3,2,3,3,2,3,6 | 2 |
| 36 | 3 -> 1 | 4,3,3,4 | 3 |
| 56 | 4 -> 0 | 2,2,2,2 | 2 |
| 57 | 2 -> 0 | 2,2,2,2 | 2 |

For completeness the other44 choices divide into26 incident-color violations, five invalid
U topologies and13 bichromatic D shapes. Incidence is checked by the displayed neighbor triples.
The five invalid U insertions are02,12,14,36,47: respectively a branch at0, the FOUR-edge
path2-1-0-3-4, the cycle1-0-3-4-1, a branch at3, and the five-edge path1-0-3-4-7-6.

The13 D-shape obstructions, after the indicated edit, are explicit:

    01->3: 0-1-2-5-7 (3,2,3,2)
    01->4: 2-0-1-4-7 (1,4,1,4)
    02->4: 0-2-5-6-3 (4,3,4,3)
    03->2: 3-0-2-1-4 (2,1,2,1)
    03->4: 0-3-6-5-2 (4,3,4,3)
    12->4: 0-2-1-4-7 (1,4,1,4)
    14->3: 4-1-2-5-7 (3,2,3,2)
    34->2: 0-2-1-4-3 (1,2,1,2)
    36->2: 3-6-5-7-4 (2,4,2,4)
    47->3: 1-2-5-7-4 (2,3,2,3)
    56->1: 0-2-5-6-3 (1,3,1,3)
    57->1: 1-4-7-5-6 (1,4,1,4)
    67->1: 1-4-7-6-5 (1,4,1,4).

Every sequence uses five distinct vertices and four actual edges. The attached certificate
records one witness for each invalid edit and, for every legal edit and EVERY phase, its
complete coloring and every forbidden shape. The neighbor table's phase costs can thus be
checked by the elementary definition alone, not an abstract XOR assertion.

All four legal changes raise mu. Therefore there are no nontrivial equal-value or decreasing
arcs leaving w. Its neutral SCC is {w}, with no lower exit. Any nonincreasing sequence starting
at w is stationary up to phase resets. This is the exact counterexample to the frozen universal
EXIT claim. It excludes all allowed first moves, not just a particular PRE constructor's output.

## 4. Barrier escape and a different global frame: ROOT stays open

There IS an explicit escape, but it must increase mu:

    w
 -> (0,1,0,2,1,0,0,3,4,4,2,0)       [25:3->0, mu=2]
 -> (0,1,4,2,1,0,0,3,4,4,2,0)       [03:0->4, mu=0].

A full star coloring of the final frame is

    (5,1,4,2,1,6,6,3,4,4,2,5).

Thus the minimum attainable maximum-mu along an unrestricted edit escape from this w is
EXACTLY2: every first move is at least2, and this path attains2. Two edits are also optimal.
This is a tight energy-barrier certificate, not a terminal root obstruction.

After EXIT failed, the bounded search switched to global frame selection on the same graph.
Choosing U={01,25,34,67}, a perfect matching, yields the balanced frame

    (0,1,2,2,3,0,0,3,1,1,2,0),

with full colors(5,1,2,2,3,6,6,3,1,1,2,5). It even uses only five distinct colors.
The global choice changes the U topology instead of insisting on a descent from the bad state.
Each of the ten used color pairs has components with at most three edges; the direct checker
also enumerates all four-edge paths and C4s. This is a positive control for this whole cubic graph.
It does not reassert the already challenged universal perfect-matching-U route.

No augmenting-chain lemma of the requested universal nonincreasing kind can now be proved:
its EXIT premise fails here. Nor can distance-to-exit repair the lexicographic potential,
because this positive level component has NO such exit. A different selection theorem or
controlled uphill/multi-edge exchange is needed. Availability from a specifically restricted
PRE-reachable family remains a separate open question, not disproved merely by this example.

## 5. Complete finite coverage and minimum order

The new catalogue enumerates simple cubic graphs with vertex0 neighbors exactly1,2,3.
Every nonempty simple cubic graph admits that relabeling. At vertex i all already fixed
incidences are retained and EVERY possible set of later neighbors filling degree3 is chosen.
The feasibility pruning uses all still-unprocessed possible neighbors, never only later
neighbors of an unprocessed vertex. This is a proved necessary condition, not a heuristic.
At completion connectivity is tested. Isomorphism testing tries every root image, all six
neighbor permutations and all permutations of nonneighbors. Thus it cannot silently merge
nonisomorphic graphs. Counts are:

    order4: 1 rooted labelled graph, 0 disconnected, 1 connected type;
    order6: 7 rooted labelled graphs, 0 disconnected, 2 connected types;
    order8: 553 rooted labelled graphs, 1 disconnected, 5 connected types.

No external catalogue or perfect-matching existence theorem is used. On six vertices the
classification is also immediate by complementing: a two-regular graph is C6 or two triangles.
Odd cubic orders are excluded by the degree sum, and nonempty simple cubic order is at least4.

For EACH of these eight connected types, all D/U partitions, every admissible A coloring
and every phase are covered, not merely PRE outputs. Only global A permutations are quotiented.
A canonical word numbers nonzero classes by first occurrence, fixes zero, and has orbit
4!/(4-q)! if q colors occur. Because validity and mu are color-invariant, quotient edges lift:
apply the current partial color bijection to the one changed entry, completing it on unused
colors as necessary. Repeating lifts a quotient path to genuine one-entry edits in fixed labels.
There is no graph-automorphism quotient inside the state calculation.

The C++ enumerator assigns five-symbol prefixes and prunes only hereditary invalid D/U
subgraphs. It computes phase costs via two-color COMPONENTS, without a witness/XOR compiler:
a two-color path with l>=4 edges has l-3 forbidden four-edge subpaths; a C4 has one forbidden
cycle; a longer even cycle of l edges has l distinct four-edge subpaths. Properness ensures
these are the only possibilities. All-A and all-B shapes are excluded by the preframe premises.

The separately written Python checker chooses U subsets, partitions D in reverse edge order,
and generates actual shapes from distinct vertex tuples. It calculates every phase cost from
actual U-edge equality masks, checks each supplied optimal FULL coloring directly, regenerates
all neighbors, and checks the parent forest and reverse nonincreasing reachability. Neither
new implementation imports C20, C23 or C23R core code. They remain in the same generator trust domain.

The two implementations agree on all190945 normalized frames /4581192 raw A-colored frames
and1159326 normalized-frame phase choices in this finite domain. The eight state counts are
69,1122,1260,46572,35883,33462,40524,32053. All positive states at orders4/6 have downward paths.
The five order8 types have respectively0,4,12,0,32 closed positive blocks. All48 are projected
singletons at mu1. This complete smaller-order coverage makes order8 minimal for EXIT failure
as a finite computation-backed candidate. The explicit counterexample itself does not depend
on accepting the catalogue or the minimum-order computation.

Each generated .states stream stores code,mu,phase,parent,distance,block. Every reachable
positive state has a parent with nonlarger mu and distance one smaller; zero states terminate.
Each .blocks stream lists the whole block size and an exit pair if present. All closed members
are recorded in the summary. Hashes bind the exact streams and the scripts regenerate them;
full streams are supplied in the companion replay-output archive, not silently inferred from
counts. They are mathematical data, not raw host logs. The corpus is finite only through order8.

## 6. Mutations, limits and the next obligation

Twenty actual mutation checks cover C4 omission, induced-path-only filtering, dropped self rows,
parallel-sign collapse, support-multiplicity collapse, wrong RHS, palette crossing, U length4,
U cycle, nonsimple witnesses, omitted edits/phases/whole frames, invented exits, false SCC members,
a multi-edge jump mislabeled as one edit, a canonicalizer moving zero, and corrupt full colors.
All24 raw A-color permutations of the primary singleton are also checked, including all48 edits.

C19-E and C20 regression programs were rerun separately with their frozen input/source hashes;
old result JSON was not evidence. The C21 compact propositions and C23R Issue note are context,
not imported code or assumed universal escape lemmas. Historical unavailable files remain unavailable.

All child processes are bounded by CPU35/36 seconds, wall40 seconds,768MiB, one thread,
5MiB file output and16KiB stderr, with stricter limits inside old regression programs.
Actual compiler/interpreter fingerprints, exit codes, elapsed times and input/output digests
are recorded. No Lean, SMT adapter, trusted math workflow or closure gate was run.
An exact local admission request is supplied; its missing formal/semantic/trusted gates stay null.
The legacy root-to-leaf record dependency is not used to claim the root from a false leaf lemma.

Best candidate: exact order8 closed positive SCC and sharp barrier2; complete finite scope through8;
a positive global perfect-matching frame for the same graph. Failed-route proposal: universal
nonincreasing neutral-plateau EXIT. First open node: OUTER. Next atomic action: develop a globally
selected short-path frame or a controlled multi-edge/uphill exchange from an explicit starting
family, without assuming the disproved all-preframe EXIT statement or universal matching-only U.
