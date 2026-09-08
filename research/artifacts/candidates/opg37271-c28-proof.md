# C28 — a geometric C27 interface, its minimum order, and a saturated-motif exclusion

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT.
Best verified result: none. Primary owner: math-proof.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Frozen main: 69b475b0ce24540775d0f0149d446212415146b0.
Target: obligation:opg37271-root, via the still-open GLOBAL-EXCHANGE.

## 1. Statement and the unresolved conjunction

ROOT asks for a proper coloring with available colors 1..6 of every finite
simple subcubic graph, without a bichromatic simple FOUR-edge path or C4.
Paths have five distinct vertices and need not be induced. A C19 preframe
partitions E=D disjoint-union U; D is star colored in A={1,2,3,4}, and nonempty
U components are disjoint paths of one to three edges, alternating in B={5,6}.
All D/U choices, all A colors and all B phases remain available globally.

For a phase assignment x, cost_F(x) counts actual forbidden shapes, with paths
identified only with their reversals and cycles only by dihedral symmetry.
mu(F) is its minimum over phases. Actual shapes, not deduplicated algebraic
rows, are counted. No statement in this package assumes legal single-edge
interpolation of an exchange.

We resolve geometric realizability of the EXACT old C27 abstract interface:
three nonempty U components t,p,q; one negative self row at t; two equal-sign
t-p rows; three equal-sign t-q rows; one p-q row; no other selected mixed
shape. The three nonloop signs have XOR zero. Separate choices of origins
for the phase bits put all nonloop right sides at zero. The new endpoint is
required to have local profile [p=q], and the exterior to have cost [p!=q].
This exact witness-multiplicity convention matters for the minimum-order claim.
Cost-equivalent systems with extra actual rows are not covered by that claim.

C28-R: this entire specified old/new profile interface HAS a simple connected
cubic geometric realization on ten vertices, with a genuine exterior-only
one-row satisfied chain between two distinct ports.
C28-M: ten is its minimum order among simple subcubic exact realizations,
supported by the exhaustive small-skeleton certificate and its coverage proof.
C28-E: the displayed saturated colored motif cannot occur in a positive global
frame optimum, even in an arbitrary larger legal subcubic completion: an
explicit color replacement decreases every phase cost by at least one.

These do NOT decide whether a DIFFERENT geometric realization of the same
interface can satisfy the stipulated positive global optimum and secondary
extremality. That conjunction remains open. The example satisfies phase
optimality and has a unique smallest negative core, but fails primary GLOBAL
frame optimality. It is not a ROOT counterexample.

## 2. Complete graph and all actual old witnesses

Use vertices 0..9 and ordered edges

  01,02,03,12,13,24,35,46,47,56,58,69,78,79,89.

All vertices have degree three; the edges are simple. Connectivity follows,
for example, from the paths 1-0-2-4-6-9-8-5-3 and 4-7. Let zero denote U and set

  F=(1,0,0,2,3,1,2,0,3,1,0,0,2,0,3).

The U components, with the stated orientations, are
P=2-0-3 (phase p), T=4-6-9-7 (phase t), Q=5-8 (phase q).
Their B bits are respectively (p,p+1), (t,t+1,t), and q, where + is XOR.
The D color classes are
1:{01,24,56}; 2:{12,35,78}; 3:{13,47,89}; color4 is unused here.
They are matchings. In every union of two classes every component has at most
three edges, so the D coloring is star. Both new programs check these premises.

The COMPLETE selected mixed-shape list is:

| Vertex path | Equal D color | Safety equation |
|---|---:|---|
| 1-0-2-4-6 | 1 | p XOR t=1 |
| 0-2-4-6-5 | 1 | p XOR t=1 |
| 0-3-5-8-7 | 2 | p XOR q=0 |
| 2-4-6-5-8 | 1 | t XOR q=1 |
| 3-5-8-7-9 | 2 | t XOR q=1 |
| 6-4-7-9-8 | 3 | t XOR t=1 |
| 4-7-9-8-5 | 3 | t XOR q=1 |

For completeness, inspect each same-colored D pair and every disjoint U-edge
pair. Their four-edge union contributes exactly when it is connected with
degree pattern (1,1,2,2,2) or (2,2,2,2), and the memberships alternate. This
finite classification produces exactly the seven rows above, including all
non-induced paths and any possible C4. There are no selected C4s in this
particular old frame; C4s are included in both enumerators and negative tests.

The self witness has chord 69, which does NOT remove the path. Its unique
minimum-row negative core has one row. Its least complete-U witness hull is

  S0={46,47,69,79,89}.

No smaller support can contain that witness and its full U component. Thus the
minimal-core choice is unambiguous inside this fixed frame; this is not a
secondary-minimum claim over all frames.

The full cost is exactly

  cost_F(p,t,q)=1+2[t=p]+3[t=q]+[p!=q].                     (1)

It has minimum1, attained precisely at (p,t,q)=(0,1,0),(1,0,1).
After replacing the abstract internal variable by t+1, this is exactly C27's
negative loop, two t=p rows, three t=q rows, and the exterior equality p=q.
At an attainer every nonloop row is satisfied. Consequently every signed cut
margin is nonnegative; a loop crosses no cut. The certificate recomputes all
8 margins from the actual row occurrences.

## 3. An actual new endpoint with exactly the allegedly problematic profile

Take connected support

  S=S0 union{56}={46,47,56,69,79,89}.

P and Q are both outside S and are different components. The external witness
0-3-5-8-7 is entirely disjoint from S. Thus it is a genuine exterior-only
one-row chain, not the core-incident one-port geometry of C27's earlier graph.
At both old attaining phases this chain is satisfied.

Simultaneously set 56:1->4, 79:U->4, and 89:3->1, obtaining

  Qstar=(1,0,0,2,3,1,2,0,3,4,0,0,2,4,1).

The internal U path is now 4-6-9, with bit s; P,Q remain unchanged. D is again
star colored, as the two programs and the explicit pair-component check show.
The COMPLETE new mixed rows are

  1-0-2-4-6: p XOR s=1;
  0-3-5-8-7: p XOR q=0 (outside S);
  7-9-6-5-8: s XOR q=0.

Therefore

  sigma_F,S(p,q)=1+min_t(2[t=p]+3[t=q])=(1,3,3,1),
  sigma_Qstar,S(p,q)=min_s([p=s]+[s!=q])=(1,0,0,1),

in port order 00,10,01,11. Both endpoint closures are checked; no single-edge
interpolant is required or used. A specified endpoint is not the whole family.

Absorb the exterior witness and every complete U component it touches:

  T=S union{02,03,35,58,78}.

It contains all three old U components. All newly touched shapes disjoint
from S are inspected. Their cost is exactly h(p,q)=[p!=q], supported by the
actual exterior path above. With m=min(sigma_old+h)=1 the complete table is

| p,q | sigma_old | sigma_new | h | r=old+h-m | g=old-new | g-r |
|---|---:|---:|---:|---:|---:|---:|
| 00 | 1 | 1 | 0 | 0 | 0 | 0 |
| 10 | 3 | 0 | 1 | 3 | 3 | 0 |
| 01 | 3 | 0 | 1 | 3 | 3 | 0 |
| 11 | 1 | 1 | 0 | 0 | 0 | 0 |

Thus max(g-r)=0 in an ACTUAL simple cubic graph. mu(F)=mu(Qstar)=1.
This makes C27's cut-only, specified-endpoint limitation genuinely geometric.
It does not promote that endpoint to a best possible exchange.

## 4. Entire minimum core-support families and the available improving endpoint

All endpoint words in {0,1,2,3,4} on the specified support are enumerated, with
the outside word fixed. D-star, U length, joint U closure and all B phases are
checked; neither a constructor nor an interpolation trajectory restricts them.

| Support | All legal partial endpoints | Endpoints with profile (1,0,0,1) | Family envelope |
|---|---:|---:|---|
| S0 (5 edges) | 82 | 0 | (0,0,0,0) |
| S0 union{24} | 161 | 2 | (0,0,0,0) |
| S0 union{56} | 144 | 4 | (0,0,0,0) |

These are all MINIMUM connected supports containing S0 which realize the
exact old/new profile pair while preserving the displayed exterior path and
both outside U ports. Indeed, S0 is the mandatory five-edge hull; it has no
such endpoint. Of one-edge enlargements, closure forbids partially including
P and preservation forbids absorbing Q; preserving the exterior path forbids
35 and78. The only remaining incident D edges are24 and56. Thus no smaller
or unlisted minimum support is omitted. This minimum concerns realization of
the SPECIFIED zero-gain profile pair, not the size of an improving exchange.

For strict improvement there is already a ONE-edge support. Replace only
89:3->4, preserving D/U and every other color. Call this endpoint R. Its old
seven rows lose precisely the self row and the last t-q row. Hence

  cost_R(p,t,q)=2[t=p]+2[t=q]+[p!=q],

with minimum0 attained at (0,1,0) and its common complement. One full star
coloring is

  (1,5,6,2,3,1,2,6,3,1,5,5,2,6,4).

The distinct singleton change47:3->4 also improves. The certificate exhausts
all TEN old-U-closed singleton supports (nine D edges and U edge58), all21
legal partial endpoints, every outside boundary and every inside B phase.
Only those two changed endpoints attain cost0 at the old optimal boundary.
Thus the minimum nonempty improving support has size1. A claim that ALL
minimum core-support endpoints fail would be false on this realization.
This is not a universal greedy rule: only this explicitly bounded geometry
has been evaluated, and the proof below explains its particular safe color.

## 5. Saturated-motif theorem: exclusion from global minima in every completion

A stronger statement avoids extrapolating from the ten-vertex calculation.
Retain the thirteen edges of the displayed graph other than12 and13, with
exactly their old D colors and the three complete U components P,T,Q. Embed
this colored motif on distinct vertices in ANY finite simple subcubic graph
whose remaining edges form a legal preframe. Additional U components are
allowed, but P,T,Q remain whole components. Arbitrary legal D structure may
be attached at the unsaturated vertices1,2,3. The conclusion is:

  recoloring89 from3 to4 is legal and lowers EVERY phase cost by at least1.

Proof. Vertices5,6,7,8,9 already have all three incident edges in the motif.
Consequently the edges at line-graph distance at most2 from89 are fixed:

  distance1: 58(U),69(U),78(color2),79(U);
  distance2: 35(color2),46(U),47(color3),56(color1).

No external edge can enter this list because its required incident vertex
would exceed degree3. None of these D edges has color4. Coloring89 with4
therefore preserves properness. A newly bichromatic four-edge path/C4 using
89 would require another edge of color4 at distance two along that shape.
That edge would be in the displayed distance-two list, which is impossible.
Shapes not using89 are unchanged. This argument applies to every actual path
and C4, not just the seven rows of the isolated graph.

The actual path6-4-7-9-8 always was bad: its two U edges are the first/third
edges of the same alternating three-edge component T, so have the same B
color, while47 and89 both had color3. After the change it is not bad. Thus
at least this one old violation disappears and no new one is created.
D-star is preserved by the same argument restricted to D; U and its closures
are unchanged. The phase spaces are identical, so minimizing proves

  mu(R)<=mu(F)-1.

This proves the theorem for arbitrary legal completions of the motif, even
when color4 occurs elsewhere, without any assumption that an external chain
can be released or that a sequence of single-edge moves exists. It is an
explicit occurrence-specific rule, not a return to unconditional local descent.

Accordingly, this colored motif CANNOT occur in a positive globally minimizing
frame, regardless of the secondary core extremality used to break ties.
Its single improving endpoint already contradicts primary minimality.
The larger class of all other geometric realizations of the abstract rows
has NOT been reduced to this motif. That missing classification is not hidden
in the saturated-degree hypothesis.

## 6. Minimum order of exact geometric realization: finite coverage proof

A genuine self row uses disjoint U edges in one component, necessarily the
first and third edges of a three-edge path. That component needs4 vertices;
the distinct ports each need at least2. Thus n>=8.

For n=8 or9 the possible U path lengths, with t first and p carrying weight2,
are exactly (3,1,1), (3,1,2), (3,2,1), subject to their vertex sum<=n.
The endpoints can be relabeled into consecutive path blocks. Vertices not in
U are retained as possible D-only endpoints. Phase origins for p,q give four
sign gauges after a common flip fixes t's origin, so all16 n/topology/gauge
cases are covered. No external catalogue or cubic-only restriction is used.

Here is an exact finite reduction. From a putative realization delete every
D edge belonging to no selected mixed witness. This changes the graph, NOT a
frame on a fixed graph; it is used ONLY for the order lower bound. Deletion
preserves D-star and all seven selected shapes and introduces none (paths
need not be induced). Drop resulting isolated D-only vertices. Every remaining
D edge belongs to a selected witness with another D edge of the same color.

Each nonempty D color class is therefore a productive matching. For fixed U,
list ALL matchings on the available non-U vertex pairs. For each pair of its
edges and each pair of U edges classify their four-edge union as above. Reject
any wrong-sign/wrong-variable row, any row multiplicity exceeding (1,2,3,1),
and any D edge contributing no row. Record the resulting four-entry count.
A full realization is the union of at most FOUR productive matchings, with
no shared D edge, degree bound3 after adding U, and no bicolored D component
having four or more edges. Its row counts are the SUM of the class counts,
because every witness has two equal-colored D edges. Pairwise checking the
D color classes suffices for D-star. These conditions are also sufficient.

The producer enumerates matchings by the least available vertex; the separate
checker enumerates increasing disjoint edge subsets. Pair witnesses are found
by four-edge degree/connectivity tests in the producer and injective vertex
walks in the checker. Both enumerate all compatible at-most-four-class unions,
and agree on the complete class-list hashes, branch counts and zero solution
counts in all16 cases. The exact counts are in the bound certificate.
Their combined class-search node count is12,976; this is not an all-frame or
all-graph census.

With no exact realization at8 or9 and the explicit cubic realization at10,
minimum order is10 for the precisely frozen actual-row interface. This is a
finite certificate-backed theorem candidate, not an arbitrary-order induction.
Deleting unproductive D edges would be INVALID for preserving the exchange
family or global optimality: those edges may constrain other colors. We do
not use that reduction for the global-minimum claim in Section5.

## 7. Replay, falsification and the first open global lemma

Run python3 research/artifacts/candidates/opg37271-c28-run.py in a writable
disposable checkout. The producer deterministically regenerates the complete
endpoint/phase certificate. The checker imports no producer or older candidate
source; it enumerates individual colors1..6, verifies D-star by two-color
components, U closure by direct connectivity, and costs by actual vertex walks.
It also reconstructs the entire small-realization search by a separate matching
enumeration. The complete generated table is frozen by SHA-256 in a compact
binding file and included in the recovery archive; it is not a hidden input.

Twenty mutations test palettes, repeated graph edges, excess degree, U length
and closure, missing endpoint/gauge cases, nonsimple paths, C4 omission,
induced-only filtering, self deletion, witness deduplication, omission of h,
false all-endpoint failure, phase/global conflation, wrong sign and removal of
positive-regret choices. Local tests and command exits stay in the generator
trust domain. The exact Lean/semantic request has no fabricated formal source,
trusted workflow, axiom/escape audit, or closure receipt.

Resolved here: the abstract specified-endpoint cost pattern is geometrically
possible; the displayed saturated realization is incompatible with GLOBAL
minimality in any legal completion. Still OPEN: must every geometric
realization satisfying the stipulated global extremality contain an analogous
improving structure, or can another realization persist against its full
joint endpoint family? No positive global minimum is exhibited. OUTER/ROOT
and statement-faithfulness/trusted closure remain unclosed.
