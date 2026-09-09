# C30 continuation: complete minimal-order exact-pattern classification

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT. Best verified result: none.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input main: 3ee4c60c3feb274e60b9a54e430c2d135f77fed8.
This is an addendum to the existing C30 transaction, not a second packet.

## 1. What was and was not obtained

The requested next embedding blocking all known supports through size three was
NOT found in this turn. Instead, the exact seven-occurrence interface was
classified completely at its minimum possible graph order. This explains why
continuing to search those particular smallest inputs cannot supply that next
blocker. No statement about arbitrary-order GLOBAL-EXCHANGE follows.

Finite theorem candidate MIN10: on a finite simple subcubic graph with exactly
ten vertices, every preframe in the exact domain below has a connected support
of at most three edges and one legal endpoint frame improving at BOTH old
minimizing phase assignments. All passive D edges of the complete graph are
retained. This is a finite certificate-supported result, not an induction.

There are no exact realizations at orders eight or nine; orders below eight
are impossible by the U-component vertex count. This minimum-order observation
is replayed here, not assumed from an old result JSON. The three-edge bound is
sharp within the stated domain. It measures a jointly closed SUPPORT, not the
number of entries that change, and not a monotone single-edge trajectory.

No globally optimal positive-cost frame is exhibited. No arbitrary completion
of the listed ten-vertex graphs is asserted to preserve the same repair.

## 2. Frozen mathematical domain

A preframe is E=D disjoint-union U. D has a proper star edge coloring with
available colors A={1,2,3,4}. Nonempty U components are vertex-disjoint simple
paths with one to three edges; each alternates B={5,6}. A four-edge simple path
has five distinct vertices and need not be induced. Four-cycles have four
distinct vertices. Reversal/dihedral duplicates are removed, but different
actual shapes inducing the same equation are counted separately.

For the finite theorem, U has exactly THREE nonempty components, designated
T,P,Q. The complete mixed-witness multiset consists of exactly seven shapes:
one negative self row on T, two T-P rows, three T-Q rows and one P-Q row.
All six nonloop rows are coherent: they can be satisfied together. No extra
mixed rows, extra phase variables or hidden fixed boundary constraints are
part of this finite domain. In particular it includes the exact C27 abstract
pattern, after phase-origin changes, but not every larger graph containing
those seven shapes as a nonexhaustive subset. Requiring the P-Q witness to
be exterior to a chosen core support only restricts this domain further; the
enumeration does not need that extra restriction.

Every decoded coloring is proper, because the palettes are disjoint and U
paths alternate. All-D forbidden shapes are excluded by D-star, and all-U
forbidden shapes by the component length. Thus all remaining bad shapes are
precisely the selected mixed witnesses. The safety row for U edges e,f is
x_component(e) XOR x_component(f)=1 XOR position_parity(e) XOR position_parity(f).

The negative self row costs one under every phase; the other six rows have a
common solution. Their variable graph is connected, so precisely two phases,
related by the global interchange of colors 5 and 6, attain the minimum one.
This follows by fixing one variable and propagating coherent equalities.

A support S is a connected nonempty edge set closed under every old and new
U component it intersects. An endpoint agrees with the old partial word off S,
but can recolor arbitrarily many D edges and reselect U inside S. At an old
attaining phase, all full colors off S are held fixed; new internal phases may
be chosen. No single-edge interpolation is required to exist or to be legal.

## 3. Exact finite coverage without removing a passive constraint in a repair

A self row must use the first and third edges of the same three-edge U path:
two opposite U edges of a selected proper four-edge shape are disjoint, and
no shorter U component has disjoint edges. T therefore occupies four vertices.
P and Q each occupy at least two more, giving at least eight vertices.

At ten vertices, write lengths as (3,p,q). The six possibilities have p,q>=1
and p+q<=4. Assign their vertices consecutive blocks. All remaining vertices
are retained, including temporarily unused vertices of a partial description.
There are four coherent sign gauges (0,a,b), a,b in {0,1}; the common global
phase flip removes the redundant choice for T. Hence 24 order-ten cases cover
all U topologies and coherent signs. The corresponding order-eight/nine
coverage has 4+12=16 cases.

For coverage only, distinguish the D edges that participate in an old selected
witness from the other D edges. This is a decomposition of the FULL input, not
a deletion step used to justify an exchange. Each nonempty participating color
class is a matching, and each of its edges is used with another same-color edge
in a selected shape. Enumerate all matchings on available non-U pairs, retain
exact row counts and signs, and take every compatible union of at most four
classes. Compatibility means no repeated graph edge, degree at most three
after adding U, and D-star between every two classes. The four required counts
are (1,2,3,1). Nonempty participating classes get canonical distinct A names.
Classes containing only passive edges are allowed later using the remaining
names; a class may also acquire passive edges of its existing name.

Why is this complete? The participating parts of the color classes of any full
input appear in that list after a global A-name permutation. Every passive edge
of that input joins an available non-U pair whose endpoints have remaining
degree. The second stage enumerates ALL such additional D edges, absent or with
any A color, retaining full properness, D-star and the exact seven occurrences.
The original full input consequently occurs in this second stage. Conversely,
every accepted full completion has all required premises by direct testing.
No passive edge is omitted when testing any proposed endpoint on that graph.

Four-edge paths cannot disappear when more edges are added: they need not be
induced. Thus early rejection of an additional unwanted witness is sound.
Normal-color conflicts, excessive degree and existing D-star violations also
cannot be repaired by adding further passive edges. The first producer uses
these prefix rejections; the separate checker instead first enumerates every
residual-degree-feasible uncolored extra graph and then all of its A colorings.
Both preserve the same full final domain.

The only symmetry reduction is explicit reversal of the three designated U
paths and global A-name normalization. Each transformation is a graph/colored
frame isomorphism and maps every actual shape, support and phase extension
bijectively. Full graph-automorphism quotienting is not used. Counts below are
records in this declared representation, not counts of graph isomorphism types.

## 4. Two separately implemented geometry checks

The producer's matching-class reduction is adapted from the pinned C28 source
(aeb9f7f26e57e96e4ff40fb578a97ac641dd7b2ef06f55a63762783330191ad1).
That reuse is explicit; it is not claimed to be unrelated discovery code.
It classifies four-edge subsets by degree/connectivity and uses a least-vertex
matching recursion. Its endpoint search enumerates literal six-color support
assignments with properness and completed-shape prefix pruning.

The companion checker imports no producer or prior candidate module. It lists
matchings as increasing disjoint-edge subsets. For its small class geometry it
uses the following elementary lemma: the union of two disjoint two-edge
matchings in a simple graph is a four-edge path or C4 exactly when it has four
or five incident vertices. Indeed, every component has degree at most two and
is properly two-colored, so cycles are even. A disconnected four-edge union
cannot contain an even cycle and another edge. If it consists of at least two
paths it has at least six vertices. Four and five vertices therefore give C4
and a connected four-edge path respectively. All premises, including distinct
edges and matching disjointness, are checked before using the lemma.

For FULL graphs the checker separately rebuilds every actual four-edge path
and C4 by injective vertex walks. It checks D-star via two-color components,
reconstructs the passive completion domain independently, tests every saved
literal successful coloring, and exhausts all smaller closed supports for
records whose claimed minimum is two or three. It checks old/new U closure,
fixed external colors, and the complementary old attainer explicitly.

## 5. Complete results and what the certificate contains

All 16 smaller cases have zero exact realizations. The 24 ten-vertex cases have
600 participating-class solution records. Only length patterns (3,1,2) and
(3,2,1) occur. Under the declared path-reversal/A-name normalization these yield
75 representative participating skeletons. Their COMPLETE passive-D completion
lists contain 732 records, including any declared equivalent color records:

| Minimum attaining-boundary closed support | Full completion records |
|---|---:|
| 1 | 727 |
| 2 | 4 |
| 3 | 1 |
| greater than 3 | 0 |

The lone width-three record is the already known C30 class, not a new claimed
four-edge obstruction. The table excludes an unexamined minimum-order exact
seven-row family, rather than announcing another individual example.

For every record the certificate specifies its complete participating graph,
all added passive edges/colors, an actual successful full coloring, the support
and the old attaining phase. All old mixed rows, new mixed rows, old/new U path
lists, and full geometric shape-set digest are recorded. The checker rebuilt
54,061 actual shape occurrences over the 732 completed inputs, with declared
repetitions across different inputs. That is not 54,061 distinct unlabelled
shapes. All full graph edge lists regenerate without external or hidden data.

A literal star-six coloring is a valid endpoint certificate: its A restriction
is star, and its B restriction has maximum degree two, no cycle, and no path of
four edges. The explicit closure test also ensures a newly chosen B component
does not cross the support boundary. Conversely, a balanced legal endpoint at
the old boundary is one of the literal assignments being searched. Therefore
failure of every smaller-support literal search proves the claimed minimum
for the fixed pointed frame; it is not failure of an arbitrary selected move.

The second old optimum is the global B complement of the first. Complementing
only B in the new coloring preserves its partial frame and star condition and
matches the second old boundary. Thus the SAME partial endpoint improves both
old minimizing phases. No assertion about pointwise improvement at all eight
nonminimizing old phases is made for these arbitrary saved endpoints.

## 6. Profiles and every newly touched shape

For each saved support S, let H be the complete old self-core hull and put
T=S union H. The support intersects the unique old bad shape at the chosen
attainer, and is connected, so T is connected. H is old-U-closed. Since S is
closed for both endpoints and endpoints agree outside S, T is also closed for
both. No closure completion is silently discarded.

Outside-S U components are identical at both endpoints. For each full exterior
phase b, both sigma values are calculated by minimizing inside phases over all
actual bad shapes touching S. The common h(b) is the count of actual bad shapes
touching T but disjoint from S, evaluated on unchanged outside edges. Their
phase variables all lie outside S; unchanged edges are not assumed to mean
h=0. Every actual witness occurrence contributes separately.

Partition b into absorbed phases z and retained phases y. Set
m(y)=min_z(sigma_old(z,y)+h(z,y)),
r(z,y)=sigma_old(z,y)+h(z,y)-m(y),
g(z,y)=sigma_old(z,y)-sigma_new(z,y).
Then exact finite minimization gives
sigma_old,T(y)-sigma_new,T(y)=max_z(g(z,y)-r(z,y)).
The checker re-evaluates every table entry, all new selected shapes and both
sides of this identity from the complete graph. These are fixed-endpoint
profiles; additional endpoints on T are not assumed covered by the formula.

## 7. Consequence for the current atomic question

Within EXACTLY this seven-occurrence/three-variable domain, no unexamined graph
of order at most ten can block every connected support of size at most three
at the old optimum. In particular a new obstruction satisfying those precise
requirements must have at least eleven vertices. This lower bound does NOT
apply to a larger interface with additional witness occurrences or additional
U components, even on fewer vertices. It also is not an arbitrary-completion
version of the finite repair certificates.

The user's positive GLOBAL minimum assumption has NOT been shown contradictory
at all larger embeddings. Secondary minimum core/support does not fill that
gap. Enlarging the mutable support is a finite search operation, not a proof
of endpoint availability. No well-founded distance to an unproved exit is used.
No unconditional single-edge, nonincreasing-SCC or perfect-matching-U route is
revived. ROOT and GLOBAL-EXCHANGE remain open.

## 8. Replay and assurance

Run python3 research/artifacts/candidates/opg37271-c30x-run.py in a disposable
POSIX checkout. The source-frozen final replay has separate producer, checker
and mutation stages, with per-stage wall/CPU/memory/output limits and genuine
exit records. Two preliminary flat passive-space checks reached CPU limit;
they are disclosed, not included as successful final stages. An initially
inapplicable h-mutation fixture was replaced by an actual nonzero-h record.
The final negative-test module uses the checker's actual verification routines.

The original C30 conversation ZIP was separately hash-checked and replayed.
Its bytes and 2,368-phase observation are NOT the different remote PR43 package
claiming an 8,508-record scope. No silent overwrite or identity substitution is
permitted. These new files must be appended to the one existing C30 transaction
with an update of its existing packet; no second packet is created here.
All proofs, code and observations remain in the candidate-generation trust
domain. No trusted kernel, semantic/axiom audit or closure gate has run.
