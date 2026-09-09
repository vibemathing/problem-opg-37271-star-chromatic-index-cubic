# C30Z: bounded twelve-vertex continuation, not a new obstruction

Verdict: candidate_only. Best verified result: none. NONTERMINAL_CHECKPOINT.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
This addendum uses the existing C30 branch, PR43 and packet. It creates no packet.

## 1. Exact progress and scope

No example blocking every jointly closed connected support of size at most
three was found. C30Y already records the complete exact-seven-pattern audit
at order eleven. This continuation does not repeat its census or the earlier
order-ten full-frame census. It audits ONE complete cubic graph of order twelve,
with its old U fixed, and allows arbitrary new U choices inside tested supports.
Its larger old-row domain is stated explicitly; it is not the entire order-twelve
graph/frame space and gives no new general order lower bound.

The ordered edges are
01,02,04,12,16,23,39,(3,10),45,(4,10),57,(5,10),67,(6,11),78,89,(8,11),(9,11).
Parentheses disambiguate vertices ten and eleven. Every vertex has degree three.
The U paths are T=0-1-2-3, P=4-5, Q=6-7-8-9. The graph is connected: T meets
P through04, Q through16 and39, vertex10 through(3,10), and vertex11 through(6,11).
All other edges are D. Every proper star A-coloring of this entire D is included.
No passive D edge is deleted. Only global A-name permutations are quotiented.

An eligible old frame has minimum actual forbidden-shape count one and exactly
two attaining B phases. This includes but is not restricted to exact seven-row
interfaces. Simple four-edge paths need not be induced; four-cycles are included.
The minima count distinct actual shapes, not deduplicated XOR equations.

## 2. Finite statement and complete domain

There are 1522 normalized star A-colorings of D; 256 are eligible. Every eligible
frame has a jointly old/new-U-closed connected support of size at most three and
ONE partial endpoint which improves BOTH old optimal exterior colorings to zero.
The minimum-support distribution is 159 of width1, 91 of width2 and 6 of width3.
This is a finite theorem candidate for the displayed graph and fixed old U only.
It neither exhibits a positive global frame optimum nor settles GLOBAL-EXCHANGE.

A-colorings are enumerated in fixed D-edge order. The first encountered color
is named1 and each subsequent first occurrence receives the next unused name,
with at most four names. Every color-permutation orbit has exactly one such
restricted-growth word. Incident equal colors and already completed bichromatic
D shapes cannot be repaired by later assignments. Thus proper-prefix and D-star
prefix rejections do not omit a valid complete word. At each complete word every
one of the eight B phases is explicitly decoded and every actual shape counted.

For each eligible frame enumerate connected supports of sizes1,2,3 in increasing
size, including all old U paths that they intersect. On a support every literal
color1..6 is tried; colors outside remain fixed to the first old attainer. A
completed bichromatic shape cannot be repaired deeper in that branch. At each
accepted literal leaf reconstruct ALL new B components and enforce their length,
acyclicity and support closure. A star-six coloring automatically has star A
restriction and B components that are paths of at most three edges, but the
component/closure check is performed explicitly. Conversely every valid balanced
endpoint has a literal coloring among these assignments. Thus exhausting smaller
supports proves the claimed minimum, rather than merely failure of a template.
A support disjoint from the sole old bad shape cannot yield zero, because that
shape's full colors remain fixed outside the support.

Global B complementation preserves every bad-shape count and has no fixed point
on the three phase bits. Exactly two old attainers therefore complement each
other. Complementing B in the saved new coloring produces the SAME partial
endpoint and matches the other old exterior coloring. Both are checked directly.
The endpoint is not claimed to improve all nonoptimal old phases pointwise.

## 3. Actual witnesses, negative cores and profiles

The checker constructs four-edge subsets. Exactly the connected subsets with
degree multiset(1,1,2,2,2) or(2,2,2,2) are ordinary four-edge paths or C4s.
This characterization retains paths with chords, and distinguishes disconnected
edge collections. All such subsets, and the full edge list, are in the result.
The reference producer instead uses injective vertex walks. It explicitly reuses
C30X for the remaining reference calculations; no separate trust is asserted.

Selected mixed rows require two disjoint U edges and two disjoint equal-colored
D edges. The row sign is1 XOR the two positions' parities. Every actual row is
retained. A minimum negative core is a negative loop, an opposite parallel pair,
or a negative triangle because there are only three variables. The checker tries
row subsets of sizes1,2,3, requires XOR variable coefficients zero and RHS one,
then minimizes the whole witness/U hull size and a deterministic lexicographic
key. A negative cycle always exists in an inconsistent parity system: propagate
along a forest and add a disagreeing edge. Its elementary cycle has at most three
vertices here. Any negative closed walk splits into such cycles. This proves the
coverage of the core search, including loops and repeated geometric rows.

For each saved successful support S, the chosen core hull H contains the sole
old violated row: otherwise every core row would be satisfied at that phase,
contradicting their sum0=1. S intersects that violated shape, so S union H is
connected. H contains all old U components it touches. Since S is jointly closed
and the endpoints agree off S, the enlarged T=S union H is jointly closed too.
These properties are checked, not inferred from support size.

For every outside-S phase assignment, separately minimize inside phases to obtain
old/new sigma from all bad shapes touching S. The common h counts all bad shapes
touching T but disjoint from S. Outside U components and their orientations are
identical at both endpoints, so h is identical and independent of inside phases.
With outside phases split into absorbed z and retained b, put
m(b)=min_z(sigma_old(z,b)+h(z,b)),
r=sigma_old+h-m, and g=sigma_old-sigma_new.
Then subtracting the two exact minima gives
sigma_old,T(b)-sigma_new,T(b)=max_z(g-r).
Every table entry and both sides are rebuilt from actual shapes; shared edges do
not cancel witness multiplicities. New U topology and phase dimension may differ.
No legal single-entry interpolation or phase-only endpoint construction is used.

## 4. Replay and observations

Run python3 research/artifacts/candidates/opg37271-c30z-run.py. It executes an
explicit C30X-based reference and a standalone checker that imports no candidate
implementation. The complete normalized D-word stream and word/minimum-width
stream SHA256 agree, not merely their counts. The checker additionally records
every successful literal coloring, old costs, smallest core/hull, old/new U,
all selected actual rows and all sigma/h/r/g tables.

The final bounded run returns zero in both stages, empty stderr and no limit
event. Each process is limited to35 wall seconds, CPU30/31 seconds,768MiB address
space,1MiB file output,64KiB stdout,16KiB stderr and one thread. Exact interpreter,
source, output hashes and real timing are recorded in the execution artifact.
Twelve positive/negative boundary assertions include C4s, noninduced paths,
long/cyclic/branching U and support connectedness. They are diagnostic assertions,
not a claim of twelve external verifier runs or a trusted mutation certification.

Exploratory twelve-vertex productive-class scans and a rejected triangle-expansion
probe did not locate a new blocker. They were not a complete order-twelve census.
A broad probe reached its execution limit. None of their unfinished aggregates
is used in the finite statement above. The final Z run is frozen and separate.

The full Z result is204116 bytes, SHA256
01fda2515a9aeda6f3e31d67e2a2a5bca4ea8a7cbbac0b77c1164749805eb63f.
It is regenerated without hidden input and supplied in the recovery package.
The word/width stream SHA256 is
663a1aa3793fb3cc1b65de5638208cff0238389bc01353f12b0bb1156c9116a5.
No old C30/C30X/C30Y run is described as freshly repeated by this small audit.
No trusted formal, axiom, semantic or closure receipt is supplied.

First open obligation: find or exclude a genuinely larger embedding whose ALL
supports<=3 fail, retaining all passive constraints. C30Y covers the exact
order-eleven interface; Z covers only the displayed order-twelve graph and old U.
ROOT/general GLOBAL-EXCHANGE remain open, and no second packet is created.
