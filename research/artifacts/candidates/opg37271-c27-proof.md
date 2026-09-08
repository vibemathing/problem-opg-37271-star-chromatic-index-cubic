# C27: chain-absorption limits and a complete endpoint-family obstruction

Verdict: candidate_only. State: NONTERMINAL_CHECKPOINT.
Best verified result: none. Owner: math-proof; finite support: math-computation.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Input main: bf3b3306434831fd5300670fb6a2de92914787f2.
Transport base after completing the pre-existing C26 transaction:
2ed5df4473ff0bfa71c2b37393b5d044451d5ce4.

## 1. Exact target and limits

ROOT quantifies over every finite simple undirected graph of maximum degree at
most three and asks for a proper edge coloring with available colors1..6 and no
bichromatic simple FOUR-EDGE path or FOUR-cycle. A path is not required to be
induced. A preframe partitions E=D disjoint-union U; D is already star colored
in A={1,2,3,4}; nonempty U components are vertex-disjoint paths of lengths1..3,
colored alternately in B={5,6}. Empty U and uncovered vertices are permitted.

Orient each U path P. Edge e at zero-based parity p(e) has color
5+(x_P XOR p(e)). Every such full coloring is proper. A forbidden shape cannot
be all-D or all-U. Thus every forbidden shape alternates D/U, its two D edges
have equal fixed colors, and its U edges have equal colors. An actual selected
shape with U edges e in P and f in Q gives exactly

    x_P XOR x_Q = 1 XOR p(e) XOR p(f).

Count DISTINCT ACTUAL shapes, modulo reversal for paths and dihedral symmetry
for cycles; equal algebraic rows retain their geometric multiplicity. Let
cost_F(x) be the number of violations, and mu(F)=min_x cost_F(x). Then mu=0
is precisely a balanced preframe. Conversely every star-six coloring restricts
to such a preframe: any B-only connected component is alternating, is not a
cycle, and has at most three edges. Hence unrestricted frame existence is
exactly star-six existence, not a stronger perfect-matching assertion.

The desired GLOBAL-EXCHANGE at a hypothetical positive global FRAME optimum
is still OPEN. The finite obstruction below is optimal in its PHASES only;
an explicit better frame is supplied. It has ONE exterior U component relative
to its core hull. Its chosen chain is core-incident, not an exterior-only path
between two distinct boundary ports. It refutes the auxiliary rule that one
may always choose a shortest satisfied core-to-outside chain with minimum
witness hull and finish once all old U components are absorbed. It does NOT
refute the more selective two-port lemma, all shortest-chain choices, or ROOT.
These distinctions are part of the fixed statement, not later qualifications.

## 2. Exact absorption with h, r and g

Fix two valid endpoint preframes F,Q which agree outside S and for which S is
U-closed on both sides: any U component meeting S is completely included.
For a boundary phase vector b on outside components, sigma_F,S(b) minimizes
the cost of every actual shape touching S over internal phases. Include every
outside variable needed by those shapes; retaining additional irrelevant
outside variables does not alter the profile. Define sigma_Q,S similarly.
The unchanged outside shape cost is common to both endpoints.

Enlarge to a jointly U-closed T containing S. Write z for old outside variables
absorbed into T and b for those remaining outside. Let h(z,b) be the number
of violated actual shapes touching T but DISJOINT from S. All their edges and
colors are unchanged, and none contains an internal-S U edge. Therefore h is
the same at both endpoints and does not involve internal-S phases. Exhaustive
shape partition, not an assumed lack of new constraints, gives

    sigma_F,T(b)=min_z [sigma_F,S(z,b)+h(z,b)],
    sigma_Q,T(b)=min_z [sigma_Q,S(z,b)+h(z,b)].                 (1)

Put m=sigma_F,T(b), r(z)=sigma_F,S(z,b)+h(z,b)-m and
 g(z)=sigma_F,S(z,b)-sigma_Q,S(z,b). Then algebraically

    sigma_F,T(b)-sigma_Q,T(b)=max_z [g(z)-r(z)].              (2)

All sums count actual shapes even when witnesses share edges or induce the
same XOR row. Empty phase sets have one empty assignment. Formula(1) also
covers C4, chords, self rows and internal U topology changes between endpoints.
The prescribed endpoints must still agree outside S. If new recolorings in
T minus S are allowed, these form ADDITIONAL endpoints not covered by(1).

A supplied macro-exchange with positive gain at a globally attaining outside
phase strictly decreases global mu, irrespective of the existence or legality
of single-edge intermediates. Availability of such an exchange is NOT supplied
by its correct evaluation formula.

## 3. Monotonicity of absorption and its exact ceiling

Fix an optimal phase x* for F (no global-frame optimality assumed). For a
jointly closed R containing S, let Psi_R(Q;x*) be the least TOTAL shape cost
of Q among phases equal to x* on every unchanged U component outside R.
The internal phase variables for Q can have different topology and number.
Let Delta_R=mu(F)-Psi_R(Q;x*).

If R is enlarged to R', any previously feasible Q phase remains feasible:
only fixed external phases are released. Therefore Psi_R'<=Psi_R and
Delta_R'>=Delta_R. F itself has conditional minimum mu(F) on every such R,
because x* is feasible and no phase on F beats it. At R=E,

    Delta_E=mu(F)-mu(Q).

It follows that if mu(Q)>=mu(F), NO amount of phase-only absorption of this
fixed endpoint produces positive anchored gain. For a finite endpoint family
E_S, the same conclusion holds if every Q in E_S has mu(Q)>=mu(F). The
endpoint-family transfer can minimize over both Q and z, but enlarging the
allowed recoloring support creates a genuinely larger family E_R, not merely
a new value of z. This distinction is essential for a global proof.

At a hypothetical global FRAME minimum M, every legal endpoint Q has
mu(Q)>=M by definition. This is an extremal constraint, not a proof that
such a positive minimum exists. A contradiction needs a graph-realized
construction violating that constraint. Merely exhausting exterior phase
variables cannot furnish the missing endpoint construction.

## 4. What a shortest satisfied chain does and does not measure

For a fixed signed witness system and phase x, assign each row occurrence
weight +1 if satisfied and -1 if violated. Flipping X changes cost by

    margin_x(X)=sum_{rows crossing X} weight(row).           (3)

A loop crosses no cut. Summing toggled satisfaction indicators proves(3).
Every competing phase differs by a unique X, so x minimizes cost iff every
margin is nonnegative. Consequently the satisfied-row subgraph connects each
full-row connected component: a proper satisfied component with a nonempty
boundary has only negative crossing rows and could be flipped to improve.
For fixed ports this conclusion applies to any component containing no fixed
port. A violated row can accordingly be paired with a satisfied path when
its endpoints lie in the same satisfied component, producing a negative walk.

More quantitatively, consider an exterior system and two ports p,q. Let y
minimize its cost under a fixed p XOR q value, with cost a. Every assignment
of opposite port parity is obtained by flipping a set X separating p and q.
Thus the opposite-parity optimum b satisfies the EXACT relation

    b-a=min_{X separating p,q} margin_y(X).                 (4)

The weights in(4) can be negative; no polynomial ordinary-min-cut algorithm
is claimed in that case. If the entire exterior is balanced and y satisfies
it, all weights are positive and(4) is the ordinary weighted cut capacity.
If b>a, a satisfied p-q path must exist. Otherwise the satisfied component
containing p could be flipped, changing parity at nonpositive cost.

Shortest path length alone does not determine(4): a satisfied path of any
length has unit minimum cut, while parallel witness occurrences change the
cut price without changing the underlying shortest path. Cut balance gives
nonnegative costs, not the strict inequality g>r required by(2). The two-port
argument requires TWO qualifying ports and its strict penalty premise.
The one-port fixture below is deliberately not passed off as that case.

## 5. A minimum-hull shortest-chain obstruction on eight vertices

Take the edge order

    05,06,07,14,16,17,23,25,27,34,36,45

on vertices0..7 and partial word

    F=(1,2,3,4,3,0,4,0,1,0,1,0).                          (5)

Each vertex has degree3, the graph is simple, and
0-5-4-1-7-2-3-6-0 is a spanning cycle, proving connectivity. U consists of
edge17, with phase p, and path2-5-4-3, with phase q. D colors are
1:{05,27,36}, 2:{06}, 3:{07,16}, 4:{14,23}.
They are proper; checking the six two-A-color subgraphs yields no component
with four edges, so D is star.

Exactly three selected actual shapes exist:

| Simple vertex sequence | Equation |
|---|---|
| 0-5-2-7-1 | q XOR p=1 |
| 1-4-3-2-5 | q XOR q=1 |
| 2-3-4-1-7 | q XOR p=1 |

For phases(p,q)=(0,0),(1,0),(0,1),(1,1), costs are(3,1,1,3).
Thus mu=1 and both nonloop rows are satisfied at every optimal phase.
The unique one-row negative core is the middle witness. Its complete hull

    S={14,23,25,34,45}

contains all four witness edges and the middle U edge45. It is connected and
U-closed. Since the core has a single row, it is a minimum-cardinality core;
S is the least support containing this witness and its entire U component.

Both core-to-outside satisfied chains have one row and are therefore shortest.
The chain2-3-4-1-7 has hull

    T=S union {17},       |T|=6.                            (6)

The other chain0-5-2-7-1 has hull S union {05,17,27}, of size8.
Hence(6) is the unique minimum-hull shortest-chain choice. T contains every
old U component, so no outside phase remains. The outside-T D edges
in fact number six:05,06,07,16,27,36; all retain their specified colors.

There are exactly10 legal endpoint assignments on S, and exactly16 on T.
Here ALL entries on the support may independently be0..4; both endpoint
preframes must be valid and jointly closed, with the exterior word fixed.
This is not a restricted recoloring template or a single-entry neighborhood.
The certificate lists all10 S words and their profiles; their envelope is
(1,1). The COMPLETE T table follows. Entry order is14,17,23,25,34,45, and
phase columns follow endpoint U components ordered by least edge index,
oriented from their least endpoint. Every actual B phase is included.

| Six entries | Complete phase costs |
|---|---|
| 000034 | 2,1,1,2 |
| 000430 | 1,1,1,1 |
| 000440 | 2,1,1,2 |
| 004004 | 2,1,1,2 |
| 004034 | 1,1,1,1 |
| 040034 | 1,1,1,1 |
| 100004 | 4,2,2,4 |
| 100040 | 4,2,2,4 |
| 100400 | 4,2,2,4 |
| 100440 | 5,1,2,2,2,2,1,5 |
| 104000 | 4,2,2,4 |
| 104004 | 5,1,2,2,2,2,1,5 |
| 400030 | 1,1,1,1 |
| 400400 | 3,1,1,3 |
| 400430 | 3,1,1,1,1,1,1,3 |
| 404000 | 3,1,1,3 |

Every entry has minimum at least1. Completeness is certified in two ways:
proper-color prefix backtracking plus full phase enumeration, and a separate
literal5^6 endpoint scan with edge-by-edge B assignments. For every phase of
every surviving endpoint, an actual bad simple path or C4 is recorded and
rechecked. It is a finite exhaustive certificate, not an arbitrary-order
nonconstructive assertion.

All119 connected old-U-closed supports R containing S have also been tested
for the FIXED ten-endpoint family E_S: the maximum profile gain over the
family is0 on each R. Every absorbed-variable and newly touched-shape term
is re-evaluated. This agrees with Section3; it is not an enumeration of the
much larger E_R families. For S->T, h is zero only AFTER enumerating all
newly touched shapes, not by presumption. Full E_T contains six additional
endpoints but still has optimum1.

## 6. Enlarging the mutable D support repairs the same graph

All connected one-edge supersets of T are exhausted:

| Added edge | Number of jointly closed endpoints | Minimum mu |
|---|---:|---:|
| 05 | 169 | 0 |
| 07 | 119 | 0 |
| 16 | 95 | 0 |
| 27 | 60 | 1 |
| 36 | 116 | 0 |

Adding06 alone is disconnected and is outside this declared family. Thus the
minimum SUCCESSFUL support containing T has size7. This is not a minimum
among arbitrary supports, nor a universal width bound.

In R=T union {05}, simultaneously set05:1->U and25:U->2. The new word is

    Q=(0,2,3,4,3,0,4,2,1,0,1,0).

U path2-5-4-3 becomes0-5-4-3; edge17 is unchanged. All phases have costs
(2,0,0,2). One full star coloring is

    (6,2,3,4,3,5,4,2,1,6,1,5).

Both single-edge intermediates are INVALID. Setting05 to U first gives
U-degree3 at5; coloring25 with2 first creates the D-path6-0-5-2-7 with
colors2,1,2,1. Only the two legal joint endpoints are used in the proof.
The alternative one-row shortest chain, with the larger size8 hull, has556
legal endpoints and optimum0. Thus NOT ALL shortest-chain choices fail.

This example is not a positive global FRAME optimum and not a root example:
Q explicitly beats F. It shows why 'number of unabsorbed old U components'
can reach zero with positive optimum for the allowed endpoint family.
A strictly decreasing counter for absorption terminates that operation, but
its terminal state need not have the required mathematical property. More
mutable D edges, not merely additional free phase variables, are necessary
for this particular frozen family.

## 7. Small-order completeness and mutation scope

All connected simple cubic graph types below8 are K4 and the two six-vertex
types K3,3 and the triangular prism. There is no smaller nonempty order by
the handshake identity and degree3. At order6 the complement is2-regular,
and its cycle lengths are6 or3+3, yielding exactly these two types.

The two implementations enumerate all normalized0..4 preframes and every B
phase on these three representatives. Only global A names are quotiented:
a restricted-growth word using k nonzero names has4!/(4-k)! raw realizations.
No graph-automorphism quotient or restricted PRE constructor is used.

| Type | Normalized frames | Phase trials | Self-core/attaining-phase cases |
|---|---:|---:|---:|
| K4 |69|156|24|
| K3,3 |1260|5040|720|
| Prism |1122|4464|624|

Every actual self-core occurrence at every attaining phase has an improving
endpoint in its bare full-core support. The record counts1368 occurrences,
not1068 old package cases with a different case convention. Full word/cost
stream hashes and ordered endpoint-witness-case hashes agree between the
implementations. This gives minimum graph order8 for the SPECIFIED self-core,
minimum-hull, core-incident-chain failure. It does not establish a smallest
failure for genuine two-exterior-port chains or for arbitrary core types.

The fresh checker uses four-edge subsets with connected degree patterns,
not the producer's vertex-permutation shapes. It enumerates individual B
edge colors and compares the component formula for total forbidden shapes:
a two-color path with m edges contributes max(0,m-3); C4 contributes1; a longer
two-color cycle contributes m four-edge paths. It checks all endpoint families,
all absorption supports, geometric chain identities, minimum-hull tie-breaking,
all attaining phases and graph simplicity/connected cubicity.

Twenty-two mutation tests cover absent endpoints/phases/support rows, false
minimum/envelope/cost/U path, repeated witness vertices, palette crossing,
U length4, missing h/new shapes, ignored slack, using only old optimizing
ports, falsely concluding zero cost from complete U absorption, omission of
middle U edges/C4/self rows/witness multiplicity and alleged legal single
intermediates. All24 A permutations preserve the fixture. All512 three-variable
signed systems with8 phases each compare the cut identity against every
flip, for4096 phase-system tests. These algebraic tests do not assert arbitrary
signed systems are geometrically realizable as subcubic preframes.

## 8. Nonzero h and real slack controls

The distinct C26 conversation absorption fixture is replayed from its frozen
edge table and words, with no source import. Its S/T endpoint counts are28/48.
For one remaining boundary bit0, old profile by z is(1,3), new(1,0), h=(0,0),
r=(0,2), g=(0,3), and max(g-r)=1. The winning z is NOT an old optimizer.

On a six-cycle, use old word(1,0,1,0,1,0), new(2,0,1,0,1,0), S={01}, and
T={01,12}. The newly touched four-edge path1-2-3-4-5 is counted in h. In
boundary order00,10,01,11, h vectors are(1,0),(0,1),(1,0),(0,1); gains are
1,2,2,1. The certificate gives all old/new/r/g values and actual new shape
vertices. Omitting h or its witness is caught by mutations. Thus the zero-h
value of the main fixture is not an untested simplifying convention.

## 9. First open global lemma and provenance

GLOBAL-EXCHANGE still asks for an improving graph-realized endpoint from a
hypothetical positive global minimum, with the user's secondary extrema.
This package neither constructs such a positive minimum nor assumes it exists.
A genuine two-port satisfied chain requires its separate strict exterior-price
hypothesis; applying it to a one-port core is invalid. A proposed chain-extension
proof must keep new geometric constraints and justify both availability of
strict support enlargement and an improving terminal condition. Distance to
an unproved exit cannot be used to define the purported progress measure.

Next atomic target: a genuine two-port exterior chain with its signed separator
price, all newly touched D constraints, and an expanded endpoint-family envelope.
Prove the family creates gain exceeding that price under actual global-extremal
structure, or exhibit a precisely scoped failure with all supports covered.
The finite one-port failure is negative knowledge, not a substitute for this
open node. No repeated order-ten census or dead single-entry route is used.

The existing remote C26 core-ports PR39 and the conversation support-absorption
archive have different content. PR39 was completed separately; the archive
SHA256 is2cad12bcf2661fb8d9a0afd968309a9eda437974e58383b1abc279c9a72635ff.
C27 reuses their mathematical context but does not overwrite either's files.
No trusted verifier, formal source admission, axiom/semantic review or root
closure is supplied. The bounded execution receipt reports actual versions,
source/input/output hashes, process limits and exits; all remain in the
candidate-generation trust domain.
