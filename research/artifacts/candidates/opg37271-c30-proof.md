# C30 — passive blockers, width-three palette transfer, and a completion-uniform exclusion

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT. Best verified result: none.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input main: 3ee4c60c3feb274e60b9a54e430c2d135f77fed8.
Primary owner: math-proof. Transport target: obligation:opg37271-root.

## 1. Frozen scope and the remaining global quantifier

ROOT asks for a proper edge coloring in {1,...,6} of every finite simple
undirected graph of maximum degree at most three, with no bichromatic simple
FOUR-edge path or FOUR-cycle. Paths need not be induced; a chord does not
remove a path. A preframe partitions E=D disjoint-union U. D is star colored
in A={1,2,3,4}; the nonempty U components are vertex-disjoint paths of one to
three edges, colored alternately in B={5,6}. Empty U and uncovered vertices
are allowed in the general definition. Every alternating U coloring is proper
because the palettes are disjoint. Count distinct actual paths modulo reversal
and cycles modulo rotation/reversal, not deduplicated algebraic equations.
Let C_F(x) be this count and mu(F)=min_x C_F(x).

Only mixed alternating D/U shapes with two equal D colors can be forbidden:
all-D shapes are excluded by D-star; all-U shapes by the length bound. Two
opposite U edges at parities a,b in components i,j give the safety equation
x_i XOR x_j=1 XOR a XOR b. This is the exact phase interface, including loops,
parallel occurrences, C4 and non-induced paths. Each ordinary full coloring
of U corresponds to one phase per nonempty component. The graph is finite.

This candidate excludes ONE additional colored embedding family from any
global frame minimum. It does not prove that every embedding has the same
repair, or classify hypothetical positive global minima. All displayed
positive-cost frames are phase-optimal only: explicit better frames are given.
Their smallest core is smallest within that frame, not a secondary extremum
across all frames. No stipulated secondary global extremality is replaced.

Logical chain: definitions -> seven actual witnesses -> full passive D
constraints -> complete small-support endpoints -> simultaneous palette
transfer -> exclusion in every legal completion of the specified motif.
The unclosed bridge is availability of some improving configuration for all
remaining embeddings under primary and secondary global extremality.

## 2. The complete new graph and its exact witness multiplicities

Use vertices0..9, with this fixed lexicographic edge order:

    01,03,05,12,17,23,26,38,45,47,48,56,69,78.

The old word, zero denoting U, is

    F=(0,1,2,0,1,0,3,3,0,3,4,0,2,0).

Vertices0..8 have degree3 and vertex9 has degree1. The graph is simple and
connected: paths0-1-2-3-8-7-4-5-6-9 connect every vertex. It is SUBCUBIC, not
cubic; the proof makes no unsupported cubic-completion assertion.

Its U components are T=0-1-2-3, P=4-5-6, Q=7-8, with phases t,p,q. Their
B bits are (t,t+1,t), (p,p+1), q, where + denotes XOR. D color classes are

    1:{03,17}; 2:{05,69}; 3:{26,38,47}; 4:{48}.

They are matchings. Each union of two classes has components with at most
three edges, so D is star. ALL four A colors are used. The full selected
mixed-shape list, with actual multiplicity, is:

| Simple four-edge path | Safety equation |
|---|---|
| 2-3-0-1-7 | t XOR t=1 |
| 3-0-1-7-8 | t XOR q=1 |
| 1-0-5-6-9 | t XOR p=0 |
| 5-6-2-3-8 | t XOR p=0 |
| 6-2-3-8-7 | t XOR q=1 |
| 2-3-8-7-4 | t XOR q=1 |
| 3-8-7-4-5 | p XOR q=1 |

Enumerating all connected four-edge subsets of degree patterns(1,1,2,2,2)
or(2,2,2,2), or equivalently all injective vertex paths and C4, gives exactly
these seven selected shapes. The frozen geometry table also includes the
other81 actual shapes, so newly selected shapes are not silently omitted.
The only negative one-row core is the first path; it has chord12. Its least
complete-U hull is H={01,03,12,17,23}; middle U edge12 must be included.
The last witness is disjoint from H and connects TWO distinct exterior
components P,Q. At an optimal phase it is a satisfied exterior-only row.

Consequently

    C_F(t,p,q)=1+2[t!=p]+3[t=q]+[p=q].                       (1)

In lexicographic(t,p,q) order the costs are(5,1,6,4,4,6,1,5). The minimum is1,
attained at001 and110. Every nonloop row is satisfied there, so every cut
has nonnegative satisfied-minus-violated margin. Flipping a cut toggles
exactly its crossing rows; loops cross none. This does not imply that F is
a global frame minimum. Replacing q by q+1 gives the coherent C27 signature.

## 3. Passive blockers: known one- and two-edge recolorings really fail

The edge48:A4 belongs to NONE of the old seven mixed witnesses. It is
nevertheless retained in every fixed-frame check. Recoloring03 alone to4
gives the all-D path0-3-8-4-7, colors4,3,4,3. Recoloring17 alone to4 gives
1-7-4-8-3 with the same colors. Deleting48 would certify invalid repairs.

Even the natural two-edge change03->4,38->1 fails. It is a valid preframe,
but it CREATES the actual paths

    0-1-7-8-3: t XOR q=1,
    2-1-7-8-3: t XOR q=0,
    1-7-8-3-2: t XOR q=1.

Together with the surviving t=p row these have minimum cost1. The middle U
edge12, which has the opposite parity, is responsible for the opposite-sign
parallel row. Only tracking destroyed old witnesses would miss it. Choosing
38->2 instead is invalid:4-8-3-0-5 becomes all-D colors4,2,4,2.
The complete support audit below is stronger than testing these examples.

## 4. Complete passive family on the fixed ten-vertex embedding

As a SEPARATE finite input family, fix all thirteen old edges other than48,
with their colors and U memberships; allow every extra D edge on these same
ten vertices. Only4,8,9 have residual degrees1,1,2. Hence extra edges are among
48,49,89, each absent or assigned A1..4: exactly125 literal inputs. No added
U edges are allowed in this declared passive-D family. This is not a deletion
operation on the graph F used for an improvement proof.

Degree admits the empty set, single edges and{49,89}. Properness leaves
48 in{1,2,4},49 in{1,4},89 in{1,4}, and the two unequal(49,89) choices.
48=1 creates path1-7-8-4-5;48=2 creates path0-5-4-8-7;89=1 creates
0-1-7-8-9. These add mixed witness occurrences, so exclude these inputs
(and the pair49=4,89=1) from the EXACT seven-witness family. New edges do
not delete old non-induced paths. Direct full-graph D-star/shape inspection
leaves exactly six completions:

| Extra passive D edges | Minimum connected closed improving support |
|---|---:|
| none | 1 |
| 89=4 | 1 |
| 49=1 | 1 |
| 49=1,89=4 | 1 |
| 49=4 | 1 |
| 48=4 | 3 |

For the first five,03->4 improves. The last is F. All125 choices and all
accepted full graphs are in the certificate; both programs enumerate them.
This is a complete FIXED-EMBEDDING family, not an all-embedding or all-order-ten
census. Arbitrary larger completions are handled only by Section7's stated
motif theorem, not by extrapolating this table.

## 5. All minimum connected-support endpoints, including U reselection

For S require both old and new U closure: every U component meeting S is
wholly in S. Endpoints agree off S; ALL entries on S may be reselected from
0..4. D-star, U lengths and every B phase are checked. There is no prescribed
constructor or requirement on single-edge interpolation. Improvement means
strict improvement at EACH old optimal exterior coloring, allowing the new
internal phases to be chosen separately for those exterior colorings.

All9 closed singleton supports have20 legal endpoints, none improving. All11
connected closed two-edge supports have59 endpoints, none improving. Their
coverage is structural: a size<=2 support cannot meet the three-edge T;
it is either contained in the eight D edges plus singleton Q, or is the whole
two-edge P. The adjacent pairs among those nine eligible edges number10;
adding P gives11. No other support of these sizes exists.

| Two-edge support | All legal partial endpoints | Best old-attainer cost |
|---|---:|---:|
| 03,05 |6|1|
| 03,38 |5|1|
| 17,47 |8|1|
| 17,78 |3|1|
| 26,69 |12|1|
| 38,48 |5|1|
| 38,78 |3|1|
| 45,56 |4|1|
| 47,48 |6|1|
| 47,78 |3|1|
| 48,78 |4|1|

All17 connected closed three-edge supports have187 endpoints. Exactly FOUR
endpoints improve at both old attainers:

| Support | New entries on the displayed support |
|---|---|
| 01,12,23 |(4,0,0) or(4,2,0)|
| 03,38,78 |(4,1,2)|
| 17,47,78 |(4,1,2)|

Thus the minimum nonempty connected closed SUPPORT is3. It is NOT a lower
bound of three changed entries: the first endpoint changes only01 but its
whole old U component must be in S. This distinction is retained in the
formal request and in every finite count. The chosen repair below changes
three entries and removes Q from U.

The text minimum-tables file on main lists EVERY endpoint and EVERY phase's
actual forbidden-shape IDs for all37 supports of sizes1..3 (2032 phase
records). Decoding the displayed new entries and canonically ordered U paths
uniquely reconstructs the full coloring; no witness counts are hidden.
The expanded certificate additionally checks all34 H-endpoints (9 improve)
and all781 endpoints on H union{38,78} (232 improve). Therefore neither full
core family is an all-failure example. All39 families contain8508 phase
records with explicitly declared repetitions between different supports.

## 6. Joint palette transfer and exact sigma,h,r,g

Simultaneously set03:A1->A4,38:A3->A1 and78:U->A2. The new word is

    R=(0,4,2,0,1,0,3,1,0,3,4,0,2,2).

T and P remain, Q disappears. A natural map from every old full phase
coloring changes just these three edge colors and keeps all other colors;
it forgets q. No bijection between old and new phase spaces is asserted.
The ONLY remaining mixed row is1-0-5-6-9, requiring t=p. Thus

    C_R(t,p)=[t!=p],
    C_F(t,p,q)-C_R(t,p)=1+[t!=p]+3[t=q]+[p=q]>=1.           (2)

In particular, both old attainers map to star colorings. At001 one is

    (5,4,2,6,1,5,3,1,5,3,4,6,2,2).

Now S={03,38,78} has Q inside and T,P outside. Partition actual shapes by
whether they touch S. The old/new optimized boundary profiles are

    sigma_F,S(t,p)=1+2[t!=p],       sigma_R,S(t,p)=0.

Let A=H union S={01,03,12,17,23,38,78}, absorbing all of T. The newly touched
shape disjoint from S is1-0-5-6-9, and its common cost is h(t,p)=[t!=p].
All other newly touched shapes are checked, not presumed absent. With
m(p)=min_t(sigma_F,S+h)=1, the complete transfer table is

| t,p | old sigma | new sigma | h | r=old+h-m | g=old-new | g-r |
|---|---:|---:|---:|---:|---:|---:|
|00|1|0|0|0|1|1|
|01|3|0|1|3|3|0|
|10|3|0|1|3|3|0|
|11|1|0|0|0|1|1|

Consequently expanded profiles are(1,1) and(0,0), and max_t(g-r)=1 for
BOTH remaining boundary phases p. This constructs a new legal endpoint;
phase release is not used to repair a fixed zero-gain endpoint. Interpolating
single-entry states, whether legal or not, is not a premise.

## 7. Completion-uniform exclusion theorem (self-contained)

Retain on DISTINCT vertices0..8 all thirteen listed edges except69, with
exactly the prescribed old colors and U memberships, INCLUDING passive48:A4.
Embed this motif in ANY finite simple subcubic graph and ANY legal preframe
extending it. The remaining graph is arbitrary. Vertex6 can have a further
incident A or U edge; in particular P=4-5-6 may extend to a three-edge U path.
Every other motif vertex is already degree3. T and Q are complete U components.
No globally unused color or absence of unknown edges at6 is assumed.

Apply the three simultaneous changes of Section6. The result is a legal
preframe and EVERY old phase coloring maps to a coloring with at least one
fewer forbidden actual shape.

Proof. Normality at0,3,7,8 follows from their complete incident lists. U only
loses its singleton component78; every other path and its colors stay fixed.
Hence length and closure premises persist, including a possible third U edge
at6. Any new bad path/C4 must contain one of the changed edges. In a proper
bichromatic four-edge shape, a second edge of the same color lies two edges
away along the shape, at line-graph distance at most2.

First consider78, now A2. Its entire distance<=2 neighborhood lies at the
saturated vertices7,8,1,4,3. Besides itself the edges are17(A1),47(A3),
38(new A1),48(A4),01(U),12(U),45(U),03(new A4),23(U). None has A2.
No outside edge can enter without exceeding degree3. Thus no new bad shape
contains78.

For38, now A1, the sole other A1 edge at distance<=2 is17; the only connector
between their endpoints is78, now A2. The three-edge path3-8-7-1 cannot extend
by an A2 edge at3 or1: their remaining edges are03(A4),23(U),01(U),12(U).
A C4 would require13, absent and forbidden by saturation. Thus no new bad
shape contains38. This inspection includes the newly colored edge78 rather
than treating the two edits separately.

For03, now A4, the sole other A4 edge at distance<=2 is48; their only connector
is38, now A1. The three-edge path0-3-8-4 cannot extend by A1 at0 or4: their
remaining edges are01(U),05(A2),45(U),47(A3). A C4 would require04, again
absent and impossible at the saturated endpoints. Thus no new bad shape
contains03 either. The neighborhoods used here do not depend on an unknown
edge at6 or any farther completion.

All shapes not using a changed edge are identical. The old path2-3-0-1-7
was unavoidably bad in EVERY phase:23 and01 are the third/first edges of T,
so have the same B color, and03,17 both had A1. It is no longer bad. No new
bad shape was created, so the total count drops by at least1 pointwise.
Restricting this no-new-bad-shape argument to D proves D-star as well.
This proves the theorem, retaining witness multiplicity and non-induced paths.

Minimization gives mu(R)<=mu(F)-1 in every such completion. Thus none can
be a global frame minimum; the primary minimum is already contradicted,
regardless of the secondary shortest-core/support choice. This is an
occurrence-specific, completion-uniform exclusion, not an unconditional
one-step/two-step/three-step greedy algorithm for arbitrary preframes.

## 8. Reproduction, finite scope, and unresolved work

The new producer uses injective vertex walks, partial0..4 endpoints and
phase decoding. The separate checker imports no candidate implementation:
four-edge subsets, degree/connectivity tests, union-find U decomposition,
literal1..6 support assignments and two-color-component scoring. It checks
the ENTIRE declared endpoint tables, not only their minima. All125 passive
inputs,22 diagnostics,24 A relabelings and a third-U-edge completion control
are included. The expanded witness data regenerate from frozen input/source;
the full minimum-support failure certificate is committed as readable text.

Discovery reused C28's matching-class routine from the SHA-bound archive to
select an alternative skeleton. The final proof and two finite validators do
not use that code. The discovery prefix is not an all-embedding classification.
No ten-vertex full-frame enumeration, greedy reconfiguration or neutral-SCC
search was repeated. Passive edges are never removed in fixed-frame audits.

Run python3 research/artifacts/candidates/opg37271-c30-run.py in a writable
POSIX checkout. Each child has wall35s,CPU30/31s,768MiB address space,1MiB file
limit and explicit stdout/stderr caps. The runner binds input, source and
interpreter digests and records actual exit/timeout observations. A syntax
typo in a preliminary checker was corrected before the final source-frozen
replay; the failed preliminary invocation is not counted as successful.

All statements remain candidate_only. No registered trusted verifier,
statement-faithfulness, axiom/escape or obligation-closure gate has completed
this candidate. The exact admission request remains pending. The old leaf
ledger edge is not used as a positive root implication and is not edited.

First open global lemma: classify the REMAINING actual witness embeddings
and their full passive D neighborhoods under the stipulated positive global
minimum and secondary core/support extremality. The current family is
excluded, but there is no proof that every other embedding has a palette
transfer or some safe joint U/color endpoint. No root counterexample or
universal width bound is claimed. Research remains NONTERMINAL_CHECKPOINT.
