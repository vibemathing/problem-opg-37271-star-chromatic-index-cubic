# C26 — shortest-core structure, boundary migration, and anchored support width

Verdict: `candidate_only`. State: `NONTERMINAL_CHECKPOINT`.
Best verified result: none. Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Frozen input main: bf3b3306434831fd5300670fb6a2de92914787f2.
Primary owner: math-proof. Target: obligation:opg37271-root.

## 1. Root and the exact remaining quantifier

ROOT quantifies over every finite simple undirected graph of maximum degree at
most three and asks for a proper edge coloring in {1,...,6} without a bichromatic
simple FOUR-edge path or FOUR-cycle. Five distinct vertices define a path;
chords do not disqualify it. Four distinct vertices define a cycle. Empty graphs
and nonsurjective color maps are allowed.

A preframe F partitions E into D and U. D has a fixed star coloring in
A={1,2,3,4}. The nonempty U components are vertex-disjoint paths of one to three
edges, colored by alternating B={5,6} with one bit per component. U can be empty
or nonspanning. The cost C_F(x) counts actual forbidden shapes, retaining distinct
witness multiplicities; mu(F)=min_x C_F(x).

Every decoded coloring is proper. A forbidden shape cannot be entirely in D
by its premise, or entirely in U by the length bound. It must alternate D/U
with equal fixed D colors. For opposite U edges e in P and f in Q at parities
p(e),p(f), its exact safety equation is x_P XOR x_Q=1 XOR p(e) XOR p(f).
Consequently mu=0 iff the frame extends. Conversely, splitting any star
six-coloring by A/B gives such a frame: the B subgraph is proper, degree at most
two, and cannot contain a path/cycle of at least four edges. Thus unrestricted
OUTER is equivalent to ROOT on a fixed graph.

CUBIC completion, OUTER selection and DECODE remain the document-local root DAG.
This packet neither closes OUTER nor uses the old leaf-extension dependency as
a positive root proof. The hypothetical positive GLOBAL frame minimum requested
in the task is not realized by any example below. The examples are phase-optimal
within their specified frames, and have separately displayed better frames.
A counterexample to a uniform bounded exchange rule on all phase-optimal frames
is NOT a counterexample to a rule restricted to hypothetical positive GLOBAL
frame minima. That distinction is maintained throughout.

## 2. Shortest negative core: a weighted cycle with exact boundary fields

In the signed equation multigraph, keep one edge per actual witness. A negative
cycle is a loop, opposite-sign parallel pair, or simple cycle with XOR of signs
one. Summing a negative cycle gives 0=1. Conversely forest propagation either
finds such a cycle or satisfies all rows; a repeated-vertex closed walk splits
into shorter cycles, with XOR additive. This proves the balance criterion
without any assertion about the original graph being planar or the equation
multigraph having maximum degree three.

Choose a negative cycle of minimum number r of row occurrences; among these
choose one whose graph-witness hull H has minimum edge count, then a fixed
lexicographic tie-break. H is the union of its actual witness edges plus every
complete U component represented by its variables. This is a connected edge
support: each witness is connected and successive witnesses are joined by the
full U path represented by their common variable. It is U-closed. Different
row witnesses may share edges; none is deleted as a duplicate shape.

**RING theorem.** For r>=3, the induced signed multigraph on the r selected
variables is exactly that cycle, with parallel copies of each cycle edge having
one common sign. It has no chord, opposite parallel signs, or negative loop.

Proof. An opposite parallel pair or negative loop would be a shorter negative
cycle. A chord splits the chosen cycle into two cycles, both shorter than r;
their sign XORs sum to one, so one is negative. Parallel copies of an existing
edge of opposite sign yield a negative two-cycle. These exhaust the other
possible rows between the selected variables. In a genuine C19 frame there are
no sign-zero self rows: two disjoint opposite U edges in one path must be its
first and third, with equal parity, giving sign one. End proof.

Write a_i for the multiplicity of cycle edge i and s_i for its sign. For a fixed
outside boundary b, ALL rows touching H decompose exactly into:
(1) internal cycle rows; (2) one-internal/one-external rows; and (3) rows with
both variables external whose actual witness nevertheless touches a D edge of H.
The last category is essential. Let h_i(t;b) count violations of category (2)
at internal variable i=t, and k(b) count category (3). Then

  sigma_F,H(b) = k(b) + min_(t_0,...,t_(r-1))
      sum_i [ h_i(t_i;b) + a_i * [t_i XOR t_(i+1) != s_i] ].

Indices are cyclic. This identity follows by disjoint partition of actual rows,
not by a relaxed abstraction. All external components meeting a touched shape
remain boundary variables, even when they are not incident with a chosen core
row. Repeated algebraic rows increase a_i or h_i; overlapping graph edges do
not cancel their costs.

For r=2 retain both parallel weights a_0,a_1, giving
k+h_0+h_1+a_0[t_0 XOR t_1 != 0]+a_1[t_0 XOR t_1 != 1].
For r=1 the genuine self rows contribute a constant number of violations,
plus the one-variable boundary field. Empty internal/boundary families have
their single empty assignment.

The r>=3 profile for a fixed b is computed by two two-state dynamic programs:
fix t_0=0 or1; at step i retain the least prefix cost for t_i=0,1; at the end add
the closing cycle edge. The recurrence is
D_i(v)=h_i(v;b)+min_u(D_(i-1)(u)+a_(i-1)[u XOR v != s_(i-1)]).
Induction on prefix length proves exactness; the final minimum proves the
profile formula. This is O(r) for one fixed b after the fields are built, not
an O(r) algorithm for all exponentially many boundary assignments or for OUTER.

## 3. Necessary optimality inequalities, and what port equalities lose

For a phase assignment x, call a row good if satisfied and bad otherwise. Flip
all variables in a set T. Precisely the rows crossing its cut toggle status;
loops never cross. Therefore

  C_F(x XOR 1_T)-C_F(x)=#good_cut_rows-#bad_cut_rows.             (CUT)

Every phase assignment differs from x by exactly one set T. Thus x is a global
phase minimum iff all these cut differences are nonnegative. This concerns
phase optimization of a FIXED frame, not preframe reconfiguration.

At such an optimum, the satisfied-row subgraph spans each connected component
of the full row graph. Otherwise a satisfied component with outgoing rows has
only bad outgoing rows and flipping it strictly improves CUT. Every violated
nonloop row consequently has a satisfied path joining its endpoints; adjoining
that row gives an actual negative-cycle certificate. The original graph
witnesses remain attached to all rows of this overlap structure.

On a shortest r>=3 ring with b fixed, put epsilon_i=+a_i for a satisfied cycle
edge and -a_i otherwise, and d_i=h_i(1-t_i;b)-h_i(t_i;b). Flipping a proper cyclic
interval [l,u] changes the cost by

  epsilon_(l-1)+epsilon_u+sum_(i=l..u) d_i.                     (INTERVAL)

Flipping the whole ring changes it by sum_i d_i. All subsets are disjoint unions
of cyclic intervals, whose contributions add. Nonnegativity of all INTERVAL
expressions and the whole-ring expression is therefore necessary and sufficient
for conditional optimality on this ring. These are explicit boundary pressure
inequalities. They do not assert that a legal D/U exchange must exist.

Define two boundary ports equivalent when their phase XOR has one fixed value
across ALL minimizing assignments. Transitivity follows by XOR addition, so
signed equivalence classes are well-defined. They do not describe the entire
minimizer set. In the actual six-cycle with alternating D-color1 and singleton
U edges, the three variables have all three pair inequalities. Exactly six of
the eight phases have minimum cost; no pair XOR is fixed. Pairwise classes
would admit all eight. An affine XOR solution set has a power-of-two size
(by free-variable elimination), so these six minimizers cannot be any XOR
system. This is a precise failure of equality-only port compression; retain
full costs or the field profile above. It is not a new ROOT counterexample.

## 4. Entire exchange-family envelopes and the global optimum boundary

For old-U-closed connected S, let E_S(F) be ALL legal endpoint preframes F'
that equal F outside S and are also U'-closed on S. U can be reselected and
any number of D edges recolored. No intermediate single-entry states are
required. Let tau_S(b)=min_(F' in E_S(F)) sigma_F',S(b).
Every boundary assignment is retained. Let rho_S*(b) be the minimum cost of
shapes disjoint from S over the remaining external phases. The outside frame
is unchanged. Independent inside/outside minimization gives exactly

  min_(F' in E_S(F)) mu(F') = min_b (rho_S*(b)+tau_S(b)).         (ENVELOPE)

Finite minimization over endpoints and phases can be interchanged. This proves
both directions, including that an attaining endpoint and its phase provide
an actual graph coloring. It is not a claim of a polynomial-time algorithm.

At a global frame minimum M with attaining boundary b*, the old inside profile
attains its minimum and any lower profile at b* is a contradiction, as in C25.
More generally, global minimality forces

  tau_S(b) >= M-rho_S*(b) for EVERY boundary b and EVERY S.      (PRESSURE)

Failure of strict improvement at old attaining b* alone does not establish
PRESSURE at other b. The example below demonstrates why this distinction is
necessary. Secondary minimization by shortest-core row count, hull size and a
canonically ordered profile is legitimate because the frame set is finite, but
it does not imply an improving endpoint. At equal global cost, an exchange
would also have to improve the declared secondary quantity to contradict that
choice; no such universal availability is asserted here.

For a fixed old FULL phase coloring c*, let L_S(c*) be the minimum total cost
among legal endpoints with all outside colors held exactly to c*. If S is
contained in T and both are old-U-closed, every S endpoint is a T endpoint: a
new U component inside S stays inside T, and all other components are unchanged
old components. Therefore L_T(c*)<=L_S(c*). This is the correct monotonicity under
support EXPANSION, not the disproved monotonicity of single-edge paths.

A procedure which enlarges a failed support by at least one edge has a strictly
decreasing unexposed-edge counter |E minus S|. Combined with successful endpoint
improvements, (mu,|E minus S|) is lexicographically well-founded. Termination of
that search does not prove its last state is balanced: at S=E, a failure might
still be a hypothetical positive global optimum. Excluding that outcome is
exactly the open root bridge, not a corollary of the potential.

## 5. Exact smallest-order anchored-width-four obstruction

Graph G has ordered edges
05,06,07,14,16,17,23,25,27,34,36,45.
It is simple connected cubic (for example 0-5-4-1-7-2-3-6-0 is a spanning cycle).
Use the NEW word, zero denoting U,

  w=(0,1,0,2,0,3,0,3,4,3,0,0).

U consists of P=4-5-0-7 and Q=1-6-3-2, so it spans every vertex. There is no
phase self row. D consists of isolated edge06(color1) and path
3-4-1-7-2-5 with colors3,2,3,4,3; it is star.

The COMPLETE selected witness list is
- path0-5-2-3-4: x_P XOR x_Q=0;
- cycle2-3-4-5-2: x_P XOR x_Q=1;
- path2-5-4-3-6: x_P XOR x_Q=0.

Thus the costs for phase integers0,1,2,3 are (1,2,2,1). Integers encode the
bit of P first. The first two rows give a minimum-row negative core. Its
minimum U-closed witness hull among the shortest cores has eight edges:
05,07,16,23,25,34,36,45. This is a genuine path/C4 core with actual shared edges,
not an abstract signed example.

Define ANCHORED-WIDTH-k to permit every connected support of at most k edges,
closed for both U endpoints, with arbitrary endpoint D/U and colors, but
strict profile improvement must hold at the restriction of at least ONE old
mu-attaining full phase. ALL old attaining phases are checked. This is the
pointed search target in the task. It is stronger than merely lowering mu
while changing which exterior phase is optimal.

The exact family table covers all29 old-closed supports of sizes1..4 and all
four old phases, hence116 support/phase interfaces. Direct cartesian enumeration
of all six colors on a support, explicit new-U decomposition and two-color
component checking reconstruct all2616 valid endpoint assignments across those
interfaces. These are interface counts with declared repetitions when two old
phases induce the same outside colors, not distinct global endpoint frames.
At the old attaining phases0,3, every support of size<=3 has minimum total cost1;
some four-edge supports have minimum0. Thus the anchored minimum size is FOUR.

The complete support counts are6,4,5,14 by size. For sizes<=3 their structural
coverage is particularly small: U has two three-edge components, so a closed
support is either a connected interval of the D components or one whole U
path. D has six single edges, four two-edge intervals, and three three-edge
intervals; the other two size-three supports are P,Q. This proves that no
unlisted small support can occur. Since U spans every vertex, D-only supports
cannot acquire B edges without joining an outside U component, so all their
allowed endpoints are exactly the checked A recolorings. Empty/unchanged
assignments are included; all inequalities and ties are retained.

A concrete boundary-pressure explanation occurs on S0=Q={16,36,23}. Fix P's
phase to0, so45,05,07 have colors5,6,5. Properness allows A-color4 on16 only, but
that gives the all-D path6-1-7-2-5 with colors4,3,4,3; hence16 is FORCED to remain
in U. Edge23 could use A-colors1,2, but color2 gives all-D path1-4-3-2-5 with
colors2,3,2,3; so only A-color1 survives. Edge36 could use A-colors2,4, but color2
gives all-D path6-3-4-1-7 with colors2,3,2,3. If23=1 and36=4, the all-D path
0-6-3-2-7 has colors1,4,1,4. These exclusions and properness leave exactly these
EIGHT triples (c16,c23,c36):

  (5,1,6), (5,5,4), (5,5,6), (5,6,4),
  (6,1,5), (6,5,4), (6,6,4), (6,6,5).

Each is a valid endpoint but still has respectively1,3,1,1,2,2,2,2 forbidden
shapes. Actual witnesses are saved in the geometric certificate. Globally
swapping5 and6 proves the other boundary case. Thus the entire component
exchange family on S0 has envelope[1,1], not just one failed replacement.

Expand by edge06 to S1={06,16,23,36}. Simultaneously set06=2,16=1,23=1 and leave
36 in U. The new word is

  (0,2,0,2,1,3,1,3,4,3,0,0).

Its U paths are P and the singleton36; vertices1,2 are allowed to be uncovered.
The old/new profiles at P's boundary are[1,1] and[0,0]. One actual full coloring is

  (6,2,5,2,1,3,1,3,4,3,6,5).

All actual shapes touching S1 and both attaining boundary extensions are in the
certificate. The old saturated port on16 is freed by recoloring its previously
blocking boundary edge06. This is an actual support expansion with strict gain,
not the deletion of an abstract XOR row. FOUR counts the closed support,
including unchanged36, not the number of entries that change.

For minimum GRAPH order, the search and a separate whole-word checker cover ALL
preframes on K4 and both six-vertex types. They cover69,1260,1122 A-normalized
states respectively, every B phase, and an improving support of size<=3 for
every positive state. Completeness is rechecked against all five-symbol words,
not inferred from C24's old counts. Nonempty simple cubic graphs have even
order>=4. At4 the graph is K4; at6 its complement is two-regular, hence C6 or
C3+C3, giving the prism or K3,3. Therefore8 is minimum order for this declared
ANCHORED-WIDTH-3 failure, with finite certificate-backed lower-order coverage.
No statement of minimum support or graph order outside this precise family is
made. The example is NOT a positive global frame minimum.

## 6. Boundary migration: why anchored failure is not exchange failure

On the SAME word w, take T={25} and recolor25 from3 to2, leaving D/U unchanged.
All three old selected shapes touch25, so the old exterior cost is zero. In
phase order0,1,2,3 the old and new profiles are

  old: [1,2,2,1],       new: [2,0,0,2].

The new rows, both with right side1, are the actual paths2-5-4-1-6 and1-4-5-2-3.
The new minimum is0 at the old NONattaining phases1,2, although both old
attaining boundaries0,3 have become worse. One full coloring is

  (5,1,6,2,5,3,5,2,4,3,6,6).

Therefore a one-D-edge frame change improves the GLOBAL mu here. The anchored
width-four result must NEVER be advertised as a four-edge lower bound for
unrestricted mu improvement, or as a new nonincreasing reconfiguration trap.
It instead refutes necessity of improvement at an old attaining boundary and
explains why ENVELOPE must retain inactive boundary phases. C25 claimed the
pointed condition only as sufficient; this is not a counterexample to C25.
The full single-support family envelope here is[1,0,0,1].

## 7. Alternating closure chains have no constant length bound

U-closure uses EDGE intersection, not shared vertices. In particular, two
perfect matchings do NOT make a growing closure: their components are singleton
edge sets. An earlier proposed matching-only illustration is rejected for this
reason and is not part of the theorem.

A correct unbounded family uses overlapping THREE-edge paths. For q>=1 use the
prism on two cycles of length4q with matching rungs, giving8q vertices. On each
layer U0 consists of all horizontal edges except indices3 modulo4; U1 consists
of all horizontal edges except indices1 modulo4. Thus U0 components have edge
blocks(4j,4j+1,4j+2), and U1 components have blocks(4j+2,4j+3,4j+4), modulo4q.
Each is a vertex-spanning family of disjoint three-edge paths.

For either choice, D consists of the rungs and the omitted horizontal matching.
Each omitted horizontal edge and its counterpart on the other layer, together
with their two rungs, is a D four-cycle. All other D components are isolated
rungs. Color each four-cycle cyclically1,2,1,3 and each remaining rung1. These
are proper star D colorings, so both endpoints are valid preframes.

Starting with horizontal edge0 on one layer, closure under U0 includes edges1,2.
The overlapping U1 block then includes3,4; the next U0 block includes5,6; continue
by induction until the entire layer cycle is included. Its4q edges form a closed
set for both partitions and no U component leaves that layer. Hence the least
closure has exactly4q edges, unbounded in q despite individual U components
having only three edges. These are genuine EDGE-overlap transitions. This
proves only that this two-partition closure operation has no universal constant
bound. It neither asserts a lower bound on an improving exchange support nor
provides a ROOT obstruction.

## 8. Execution, failed family, and first open global lemma

The C++ search enumerates prefix A words for the smaller graphs and explores
six-color endpoint completions. The new Python checker enumerates all literal
five-symbol words, independently decomposes U, evaluates two-color component
costs, and uses four-edge subsets for actual witnesses. It imports no older
candidate and no search core. The full small catalogues and their per-state
improvement witnesses are regenerated, checked and hashed; their bytes are
retained in the recovery archive. The full116-interface table is committed.
Mutations attack support completeness, both U-closure directions, phase coverage,
C4/self/parallel rows, costs, multiplicities, bad endpoints, and boundary-phase
migration. The finite192 weighted-cycle comparisons diagnose the transfer code;
they do not replace the general RING proof.

The failed-route proposal is exactly: every phase-optimal preframe admits a
strict pointed repair on a connected jointly U-closed support of at most three
edges. It does NOT assert failure at a hypothetical positive GLOBAL frame
minimum. No previous single-edge, neutral-SCC, safe-eraser reachability or fixed
perfect-matching route is reinstated.

First open global lemma: at a hypothetical positive global frame minimum, with
shortest negative core and the specified secondary extrema, prove that its
boundary pressure can be relieved by some graph-realized expanded support,
or otherwise force a contradiction. RING, CUT and PRESSURE are necessary
structural conditions; none supplied here proves this universal availability.
The anchored example supplies a precise finite family failure and an actual
expansion; it cannot stand in for that missing universal argument.

All local work is generator-domain. No Lean kernel, axiom/escape audit, semantic
admission, EvidenceLink or closure gate is claimed. The user-authorized admission
request keeps missing bindings and receipts null. PR37 is a separate older
C24 transport tail, not included or silently replaced. State remains
NONTERMINAL_CHECKPOINT; best_verified_result=none.
