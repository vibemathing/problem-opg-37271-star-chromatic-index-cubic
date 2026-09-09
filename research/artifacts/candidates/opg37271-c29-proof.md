# C29 — a passive fourth-color blocker and an unavoidable joint repair

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT.
Best verified result: none. Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input main: d85f00bf7793de78a7d85e7d32b692925e8c2236.
Primary owner: math-proof. Transport obligation: obligation:opg37271-root.

## 1. Exact scope and dependence

ROOT asks for a proper edge coloring with colors1..6 of every finite simple
subcubic graph, with no bichromatic simple FOUR-edge path or FOUR-cycle.
Paths need not be induced. A preframe consists of a fixed star coloring of D
in A={1,2,3,4} and vertex-disjoint nonempty U paths of lengths1..3; U can also
be empty and need not span. Each U path alternates colors B={5,6}, determined
by one phase bit. Every resulting complete coloring is proper. Only mixed
alternating D/U shapes can be newly bad; equal fixed D colors and equal U
colors are exactly the condition for such a shape to be bad.

The count is over actual paths modulo reversal and cycles modulo their
dihedral symmetry. Distinct shapes with the same XOR row count separately.
For a frame F write C_F(x) for this count and mu(F)=min_x C_F(x).

C29 proves a new occurrence-specific JOINT repair in every legal completion
of an explicit nine-vertex colored motif. It therefore excludes this entire
motif family from a hypothetical positive global frame optimum, regardless
of the secondary tie-break by smallest negative core/support. It does NOT
classify all embeddings of C27's abstract pattern, or prove GLOBAL-EXCHANGE.

The finite companion class fixes a different thirteen-edge productive
embedding on TEN vertices and retains ALL possible passive D edges on those
vertices. Six completions survive. This is not an all-ten-vertex frame census.
The displayed passive completion requires a two-edge connected support to
improve at every old attaining phase. This minimum is within this one graph,
not a universal width bound or a universal single-edge strategy.

Logical dependencies: definitions -> exact seven witnesses -> passive-edge
constraints -> joint repair -> completion-uniform exclusion for this motif.
The remaining bridge is classification of other embeddings under full global
extremality. No transport check or old Result JSON closes that bridge.

## 2. A complete ten-vertex graph with a genuinely passive blocker

Use vertices0..9, ordered edges

    01,02,08,12,16,23,35,37,45,47,48,56,69,78

and word, where zero means U,

    F=(0,1,2,0,2,0,3,1,0,2,4,0,3,0).

Vertices0..8 have degree3; vertex9 has degree1. All edges are distinct, and
0-1-6-5-3-2-0 together with the connections08,37,45,47,48,69,78 proves
connectivity. This graph is subcubic, not cubic; no hidden cubic-completion
assumption is used.

U paths are T=0-1-2-3, P=4-5-6, Q=7-8 with phases t,p,q. The color bits along
these paths are (t,t+1,t), (p,p+1), q, with addition modulo2. D color classes:

    1:{02,37}; 2:{08,16,47}; 3:{35,69}; 4:{48}.

Each is a matching. Unions of each pair of classes have components of at
most three edges, proving D-star. All four A colors are already used.

The complete mixed-shape table is:

| Actual simple path | Safety equation |
|---|---|
| 0-2-3-7-8 | t XOR q=1 |
| 0-8-7-4-5 | p XOR q=1 |
| 1-0-2-3-7 | t XOR t=1 |
| 1-0-8-7-4 | t XOR q=1 |
| 2-3-5-6-9 | t XOR p=0 |
| 5-6-1-0-8 | t XOR p=0 |
| 6-1-0-8-7 | t XOR q=1 |

All other same-colored D pairs and disjoint U-edge pairs fail the four-edge
path/cycle incidence or alternating-membership test. Equivalently enumerate
all connected four-edge subsets with degree sequence1,1,2,2,2 or2,2,2,2;
the second literal checker rebuilds them by injective vertex walks. This
retains non-induced paths and all C4s. There is a chord12 in the self witness.

Hence

    C_F(t,p,q)=1+2[t!=p]+3[t=q]+[p=q].                      (1)

In lexicographic(t,p,q) order, costs are5,1,6,4,4,6,1,5. The unique negative
one-row core is t XOR t=1. Its minimum full-U hull is

    H={01,02,12,23,37}, |H|=5.

It includes middle U edge12 although that edge is not in the self witness.
The minimum cost1 is attained at001 and110. At these phases every nonloop
row is satisfied, hence every satisfied-minus-violated cut margin is
nonnegative. Replacing q by q+1 gives exactly the signed multiplicities
of C27's two-port model. The exterior path0-8-7-4-5 is disjoint from H and
connects distinct complete U components P,Q; it is satisfied at both attainters.

Edge48, color4, belongs to NONE of the seven old mixed witnesses. Nevertheless:
recolor02 to4 creates the all-D path2-0-8-4-7 with colors4,2,4,2;
recolor37 to4 creates the all-D path3-7-4-8-0 with colors4,2,4,2.
Deleting48 to certify one of those moves would be unsound. C29 never does so.

## 3. All passive completions of this fixed productive embedding

Define a fixed thirteen-edge embedding by all the listed edges EXCEPT48,
with the same fixed colors. This defines a finite input family; it is not a
transformation permitted on F. Its only unsaturated vertices are4,8,9,
with residual degrees1,1,2. Therefore all extra D edges on these ten vertices
must be among48,49,89. They cannot involve a saturated vertex, a loop or an
already present edge. No added U edges are permitted in this family because
it is the family of passive D completions of the specified embedding.

Enumerate each extra pair as absent or colored1..4 (125 literal assignments),
retaining the full graph for properness, D-star, all mixed shapes and phases.
Degree allows only the empty set, one of the three singletons, or{49,89}.
Properness reduces the nonempty possibilities to:
48 in{1,3,4}; 49 in{1,4}; 89 in{1,4}; and(49,89)=(1,4) or(4,1).

If48=1, actual path3-7-8-4-5 adds a mixed witness. If48=3, actual path3-5-4-8-7
adds one. If89=1, actual path2-3-7-8-9 adds one, also excluding(49,89)=(4,1).
Adding edges cannot remove old ordinary paths, including paths with new chords.
These exclusions leave exactly the following six full graphs, each checked
with all old and newly possible witnesses, not only productive edges:

| Extra passive D edges | Minimum connected improving support |
|---|---:|
| none | 1 |
| 89=4 | 1 |
| 49=1 | 1 |
| 49=1,89=4 | 1 |
| 49=4 | 1 |
| 48=4 | 2 |

The first five admit02->4 at both old attaining phases. The last is F.
These six are a complete FIXED-EMBEDDING class, not all graph realizations of
the seven abstract rows. In particular, an arbitrary larger completion of the
first five graphs may create further blockers. The infinite-completion theorem
below is stated for its specified saturated motif only.

## 4. All minimum connected supports of the obstructed completion

For a support S require F and F' to agree off S and require S to contain any
whole U component it meets, at both endpoints. Arbitrarily many entries in S
may change D/U membership and A color; every B phase is considered. Neither
legality nor monotonicity of a single-edge interpolation is required.

For size1, closure leaves exactly the eight D edges and singleton U edge78.
The table lists ALL legal new entries and the least complete cost after matching
all outside colors to the old optimum001. Complementing all B colors proves
the same for110, and the checker also compares both directly. Zero here is U.

| Support edge | (new entry, least anchored cost) |
|---|---|
| 02 | (1,1),(3,2) |
| 08 | (2,1),(3,1) |
| 16 | (1,3),(2,1),(4,1) |
| 35 | (2,3),(3,1),(4,2) |
| 37 | (1,1) |
| 47 | (2,1),(3,2) |
| 48 | (3,2),(4,1) |
| 69 | (1,1),(3,1),(4,1) |
| 78 | (0,1),(3,1) |

Thus all nine singleton supports / twenty endpoints fail to improve. This is
a particular instance audit, not a revived universal greedy conjecture.

There are exactly eleven closed connected two-edge supports. Ten consist of
adjacent edges among the eight D edges and78; the remaining one is the whole
old U path{45,56}. They and all endpoint counts are:

| Support | Legal endpoints | Least anchored cost |
|---|---:|---:|
| 02,08 | 8 | 0 |
| 08,48 | 6 | 1 |
| 08,78 | 3 | 1 |
| 16,69 | 12 | 1 |
| 35,37 | 6 | 1 |
| 37,47 | 5 | 0 |
| 37,78 | 2 | 1 |
| 45,56 | 4 | 1 |
| 47,48 | 5 | 1 |
| 47,78 | 3 | 1 |
| 48,78 | 4 | 1 |

Exactly four new words improve at both old attainers: on02,08 set(4,1) or(4,3);
on37,47 set(2,1) or(4,1). The other entries remain fixed. All58 endpoint words
and all their phases, with actual bad-shape indices, are supplied. Supports
are counted as closed sets, not just as the list of changed entries.

For completeness the entire core hull H has25 endpoints (eight improve at
the old attainers); H union{08} has147 (sixty-nine improve). Thus the core
family is NOT an all-failure example. These full endpoint tables are additional
checks, not a silent restriction to the specified successful word.

## 5. A joint repair, exact profiles, and all newly touched shapes

Choose02:1->4 and08:2->3 simultaneously, yielding

    R=(0,4,3,0,2,0,3,1,0,2,4,0,3,0).

U and its phases are unchanged. R is proper and D-star. The sole surviving
mixed row is the old path2-3-5-6-9, requiring t=p. There are NO new mixed rows.
Therefore C_R(t,p,q)=[t!=p]. Its eight costs are0,0,1,1,1,1,0,0 and

    C_F(x)-C_R(x)=1+[t!=p]+3[t=q]+[p=q]>=1.                 (2)

Every phase improves, not merely a newly selected minimizer. At old phase001
the full star coloring is(5,4,3,6,2,5,3,1,5,2,4,6,3,6); the complementary phase
works as well. Changing08 first is a legal neutral intermediate, while changing
02 first is invalid. Neither interpolation is used as a proof premise.

Let S={02,08}; all three old U components are outside this support. Let
A=H union S absorb T's complete U path and the remaining self-witness edge37.
All shapes disjoint from S but touching A are reconstructed. Their common
cost at F and R is exactly h=[t!=p], supported by2-3-5-6-9. Thus

    sigma_F,S=1+[t!=p]+3[t=q]+[p=q], sigma_R,S=0,
    sigma_F,A(p,q)=(4,1,1,4), sigma_R,A(p,q)=(0,0,0,0).

With m(p,q)=min_t(sigma_F,S+h), r=sigma_F,S+h-m and g=sigma_F,S-sigma_R,S,
the exact table is:

| t,p,q | old sigma | new sigma | h | r | g | g-r |
|---|---:|---:|---:|---:|---:|---:|
| 000 | 5 | 0 | 0 | 1 | 5 | 4 |
| 001 | 1 | 0 | 0 | 0 | 1 | 1 |
| 010 | 5 | 0 | 1 | 5 | 5 | 0 |
| 011 | 3 | 0 | 1 | 0 | 3 | 3 |
| 100 | 3 | 0 | 1 | 0 | 3 | 3 |
| 101 | 5 | 0 | 1 | 5 | 5 | 0 |
| 110 | 1 | 0 | 0 | 0 | 1 | 1 |
| 111 | 5 | 0 | 0 | 1 | 5 | 4 |

Maximizing over t gives gains4,1,1,4 for boundary00,01,10,11. All quantities
are actual-shape sums with multiplicity. The changed edge08 also modifies the
old exterior chain; this is allowed because it is made mutable explicitly.
No fixed-endpoint phase release is mistaken for constructing this endpoint.

## 6. Completion-uniform joint-repair theorem (self-contained)

Take distinct vertices0..8 and all the prescribed colored edges above that
have both ends in0..8: thirteen edges, including the passive48=4. Place this
motif in ANY finite simple subcubic graph with a legal preframe agreeing with
its colors and U memberships. Further vertices and edges are arbitrary subject
to those premises. In particular6 may have a third incident edge of A or B
color; P=4-5-6 may then extend by one U edge. No fixed absence of a boundary
edge or a globally unused A color is assumed.

Claim: the simultaneous changes02:1->4 and08:2->3 preserve a legal preframe
and reduce EVERY full phase coloring's number of bad shapes by at least1.

Proof. Every motif vertex except6 already has degree3. Thus outside edges
cannot change the prescribed neighborhoods of0,1,2,3,4,5,7,8. All U edges
are unchanged. T=0-1-2-3 is already a complete length3 U component, so its
first and third edges have the same B color in every phase.

The new coloring is proper: at0 the two D colors are4 and3 and the other edge
is U; at2 the other two edges are U; at8 the other edges are48=4 and78 in U.
All other incident-color comparisons are unchanged.

A newly bad four-edge path or C4 must contain02 or08. In a proper bichromatic
four-edge shape, each color appears twice and the equal-colored edges are
separated by one edge along that shape, hence have line-graph distance at most2.

For changed edge08, whose new color is3, its complete distance-at-most2 edge
neighborhood is fixed by saturated endpoints. Apart from08 itself it contains
01(U),02(new4),48(4),78(U),12(U),16(2),23(U),45(U),47(2),37(1).
None has color3. Therefore no new bad shape contains08.

For changed edge02, whose new color is4, the ONLY other color4 edge at distance
at most2 is48. The only one-edge connection between them is08, now color3.
A four-edge alternating shape containing02,08,48 would need a further color3
edge incident with an available end of this three-edge path. Those ends are
2 and4. Vertex2 has only12(U),23(U) besides02. Vertex4 has only45(U),47(2)
besides48. Neither has a color3 edge. Closing to a C4 would require24, which
is absent and cannot be added at the saturated endpoints. Consequently no
new bad shape contains02 either. This also covers non-induced paths and
shared-edge witnesses; it counts shapes rather than deduplicated equations.

Shapes containing neither changed edge are identical before and after. The
old actual self-witness path1-0-2-3-7 always was bad:01 and23 have the same B
color, and02 and37 both had color1. It ceases to be bad. Thus at least one
old violation disappears and none is created, for every assignment of ALL
old and external phase variables. D-star follows by restricting the no-new-
bad-shape argument to D. U topology is unchanged, so all closure and length
premises persist even when P has a third edge at6. This proves the claim.

Minimizing the pointwise inequality yields mu(R)<=mu(F)-1. Hence no legal
completion containing this motif can be a global frame minimum. This already
contradicts primary global minimality, so no secondary minimum can restore it.
This is an explicit geometric family exclusion, NOT the unproved assertion
that every negative core or every seven-row embedding has this repair.

## 7. Validation scope, provenance, and remaining obligation

The final producer uses connected four-edge subsets and partial0..4 endpoints.
The separately written checker imports no candidate module: it uses injective
vertex walks, two-color connected components for D-star and literal1..6
support assignments, grouping partial endpoints only AFTER admissibility.
It compares full word/phase/bad-shape tables, not just aggregate minima.

The bounded discovery probe used C28's published matching-class routine to
find alternative embeddings; it was not claimed a new checker. A subsequent
broad discovery completion scan reached its35-second limit. Its incomplete
all-embedding counts are not a C29 theorem or final census. C29 instead freezes
the concrete new motif and the COMPLETE125-choice passive family above.
No ten-vertex full-frame census was repeated. No unproductive D edge was
removed from a fixed-frame repair argument. Source/receipt identity is kept
separate from mathematical validity and trusted admission.

Finite tests support the displayed tables only. Section6 is the arbitrary-
completion proof and does not extrapolate a finite count. Its conclusion is
stronger than improvement at old optimal phases, but its geometric hypothesis
is narrower than unrestricted GLOBAL-EXCHANGE. Other embeddings and larger
passive neighborhoods remain unclassified.

First open global lemma: under the stipulated global optimum and secondary
minimal negative-core support, prove that every remaining geometric embedding
contains an improving joint configuration, or rule out persistent pressure
by another geometric argument. No distance-to-exit definition is used.
The witnessed macro-step strictly decreases the natural number mu; universal
availability and a root-ending iteration remain OPEN.

No faithful Lean source, trusted axiom/escape audit, semantic review or
obligation-closure receipt is supplied. Requested admission remains pending.
All files remain candidate_only; best_verified_result=none.
