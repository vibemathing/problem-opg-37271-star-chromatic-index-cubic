# C25: complete global order-ten frames and phase-profile exchanges

Verdict: `candidate_only`. State: `NONTERMINAL_CHECKPOINT`.
Best verified result: none. ROOT and OUTER remain open.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Research input revision: b66703bd76d56f0791ad58542ec8bc7d3b8ee35b.
Primary owner: math-proof; computational support is candidate generation.

## 1. Frozen statements and scope

ROOT says that for every finite simple undirected graph of maximum degree at
most three there exists c:E(G)->{1,2,3,4,5,6} which is proper and has no bichromatic
simple path of FOUR EDGES or simple cycle of FOUR EDGES. A path has five distinct
vertices and need not be induced; a four-cycle has four distinct vertices.
Empty graphs and nonsurjective palette maps are permitted.

A preframe F is E=D disjoint-union U, a star coloring c_D:D->A={1,2,3,4}, and
nonempty U components which are vertex-disjoint paths of one to three edges.
Empty U and uncovered vertices are allowed. On an oriented path P, the B={5,6}
color at position j is 5+(x_P XOR (j mod2)). All component phases are free.

Count actual four-edge paths once up to reversal and actual four-cycles once up
to rotation/reversal. Write C_F(x) for the number of bichromatic shapes in the
proper decoded coloring, and mu(F)=min_x C_F(x). Multiplicities of DISTINCT
support shapes are retained even when their XOR equations coincide.

Every decoded coloring is proper. A forbidden shape with colors both in A would
be inside D, and a forbidden shape with colors both in B would be inside one U
component with at least four edges. The remaining forbidden shapes alternate
D/U and have equal D colors and equal U colors. Their equations are exactly
x_P XOR x_Q=1 XOR p(e) XOR p(f), including self and parallel rows. Thus mu(F)=0
is precisely balance. Conversely, any star six-coloring splits into a preframe:
its 5/6 subgraph is proper of degree at most two; a cycle or path of at least
four edges would violate star coloring. The nonempty components must be short
paths and the actual B coloring supplies their phases. Therefore unrestricted
balanced-preframe existence for a fixed graph is equivalent to its star
six-colorability. A bad preframe or a failed restricted U family is not a ROOT
counterexample.

The document-local proof DAG remains CUBIC + OUTER + DECODE -> ROOT. The cubic
completion reduction and C20 DECODE do not supply OUTER. This packet does not
use the legacy root-to-leaf ledger edge as a positive proof dependency.

This packet establishes the following CANDIDATES, with the proofs or exhaustive
finite certificates specified below:

* G10: every connected simple cubic graph on exactly ten vertices has a balanced
  preframe, including a vertex-spanning U with all paths of at most two edges.
* ENUM10: complete global enumeration of ALL preframes and ALL phases on all
  nineteen order-ten types. It is not a search from any initial preframe.
* MATCH: the specified order-ten graph admits no balanced frame when U is a
  perfect matching, over the complete matching AND A-coloring space. A separate
  uniform argument proves this restriction failure, and the graph has many
  unrestricted balanced frames.
* PROFILE: an exact boundary phase-profile criterion proves strict improvement
  for a simultaneous multi-edge, potentially topology-changing exchange. It
  places no requirements on single-edge interpolations. Universal availability
  of such an exchange at a positive GLOBAL minimum is not proved.

## 2. Complete graph and color domains

The graph generator recursively completes degrees on labelled vertices. With
N(0) fixed to {1,2,3}, process vertices in increasing order; at vertex v choose
every subset of its larger-index unsaturated vertices of the necessary size.
Every completion is tested for connectivity. This visits each graph with the
fixed first neighborhood exactly once: each edge is chosen at its smaller
endpoint. Pruning uses only an already impossible degree deficit. Multiplying
by C(9,3)=84 restores the full labelled connected domain, because permutations
of vertices1..9 act transitively on the possible three-element neighborhoods.

Exact adjacency-preserving bijection search, not a hash, partitions these
completions into nineteen types. Signatures only organize comparison buckets.
A second checker does not trust the generator's graph count or isomorphism
code. It enumerates all compatible bijections between pairs of representatives,
counts each automorphism group, and computes labelled graph counts using a
separate degree-sequence recurrence. For a residual sequence, remove one vertex
of degree d, select every combination of neighbor degree groups, decrement the
selected degrees, and multiply by the binomial choices within each group.
The recurrence counts each simple labelled realization once, by its removed
vertex's exact neighbor set. Sorting residual degrees is valid by relabelling.

Let T_n be the resulting number of all labelled simple cubic graphs, T_0=1.
The number C_n of connected ones satisfies

  C_n = T_n - sum_{1<=k<n} binom(n-1,k-1) C_k T_(n-k),

by the unique component containing vertex0. At n=10 this gives T_10=11180820,
C_10=11166120. Pairwise nonisomorphism and the independently counted
sum(10!/|Aut(G_i)|)=11166120 prove that no connected orbit is missing. Bridges
are not excluded. The graph list, all automorphism counts and checks are saved.

On each fixed labelled representative, A colors alone are normalized in order
of first occurrence, with zero reserved for U. A word using q A colors has
4!/(4-q)! raw representatives. No graph automorphism quotient is taken for
frames. Every allowed labelled frame has exactly one such canonical word;
renaming A does not change phases or the actual forbidden-shape counts.

U paths are ordered by their minimum edge index and oriented from their smaller
endpoint. A path has exactly two proper B colorings, by induction on successive
edges. Thus k components have precisely 2^k phases, including one when k=0.
Changing that orientation only permutes the enumerated assignments.

## 3. Two complete enumerations and exact finite findings

The new `global.cpp` enumerates FULL proper six-color assignments, not partial
words or a greedy frame trajectory. Only A names are normalized. It rejects a
prefix exactly when an all-A bichromatic four-shape or an all-B bichromatic
four-shape already exists. Such a prefix cannot be repaired by assigning later
edges. It does NOT reject mixed forbidden shapes. Completed assignments are in
bijection with preframe/phase pairs from Section1.

For each four-edge subset it tests the connectivity and degree pattern of a
simple P5 or C4. A subset-zeta transform computes the number of actual shapes
contained in each edge mask. On a full assignment, summing this table on the
eight A/B color-pair unions counts each mixed forbidden shape once. Normality
prevents a one-color connected shape. Each frame's phase entries are collected,
and the implementation checks that every one of its 2^k phases appears once.

The separately written `replay.cpp` instead scans all U edge masks, validates
short-path components, and assigns every normal-form D coloring. It generates
actual shapes by vertex-simple walks, not the subset transform or the six-color
prefix code. It rejects only a completed D violation. For each surviving frame
it explicitly evaluates both possible colors on every U edge for every phase.
Neither program imports or copies any C20, C23R or C24 core implementation.

Each program sorts records by the full base-five word code and hashes the same
specified transcript: decimal word code, colon, two lowercase hex digits per
phase's cost, and newline. Their exact counts, per-U tables and whole transcript
SHA-256 agree for each graph. The complete output streams are deterministic
reproduction outputs, not hidden solver inputs. Compact committed summaries
bind their hashes; the optional replay outputs need not be trusted to rerun.

Across the nineteen fixed graph representatives the actual totals are:

  normalized preframes       20511356
  raw A-labelled preframes  492272544
  normalized phase trials  198694304
  raw phase trials        4768663296
  balanced normal frames     4935898
  balanced spanning-short2    121213
  balanced perfect-U            27198

Every one of the nineteen graphs has a positive witness. The witness checker
rebuilds each graph, its D/U, phases and coloring and separately checks all
actual four-shapes and all two-color components. These nineteen explicit
colorings, together with the graph coverage argument, prove the FINITE G10
candidate; the enumeration totals are not used as an induction to arbitrary
order. No conclusion for all subcubic graphs of order<=10 is inferred from a
cubic-host reduction which might increase their orders.

## 4. A uniform full-space obstruction to fixing U as a perfect matching

Graph18 has edge list

  01,02,03,14,15,26,27,38,39,46,48,57,59,69,78.

Its six perfect matchings, encoded by edge-index masks, are
3361,4801,9300,10378,17170,20524. The graph-bound witness file lists each matching,
the two complementary five-cycles, and their five contracted matching labels.
For EVERY matching, the complement is two disjoint C5s, and contraction of the
matching identifies their union with two edge-disjoint Hamilton C5s partitioning
K5. These are six small directly checkable structural facts, not assumptions
about the unknown A colors. The matching recursion is exhaustive: match the
least unmatched vertex to each of its available neighbors, and recurse. Every
perfect matching chooses exactly one such neighbor at each step. The saved
matching list is also recovered independently from all U masks in both global
frame enumerations.

We prove the following uniform lemma, which covers all six structures without
enumerating A colors:

**Folded-five lemma.** If D consists of two C5s whose contraction by a perfect
matching U is an edge decomposition of K5 into two Hamilton cycles, then no
star A={1,2,3,4} coloring of D has a B={5,6} completion.

First, a star coloring of C5 needs all four A colors. With at most three, two
colors each occur twice. Their four edges form the four-edge path obtained by
deleting the singleton-color edge, hence a forbidden shape. Four colors on five
edges consequently have multiplicities2,1,1,1.

Give each contracted vertex the B color of its matching edge. If a folded D edge
ij joins equal B colors, its A color must be unique among ALL D edges incident
to each of i and j. An equal-colored edge at the same original vertex violates
D properness. An equal-colored edge at the other endpoint of matching edge i
produces the actual four-edge path

  k-port -- i-other-port -- i-port -- j-port -- j-other-port

with colors A,B,A,B. The K5 contraction has no parallel edge, so k differs from
j; the displayed five original vertices are distinct. The same argument applies
at j. Thus this uniqueness condition is necessary. Partition the five contracted
vertices by their B colors into5+0,4+1 or3+2.

**5+0.** All K5 edges must be normally A-colored. Each color class is a matching
of size at most two, so four colors can cover at most eight of the ten edges.

**4+1.** Let S be the four-vertex side and t the singleton. Every S vertex sees
all four A colors: its three internal edges are mutually distinct, and their
colors cannot occur on its t edge. For each A color, if it occurs on i internal
S edges and j edges to t, then2i+j=4. The four edges to t therefore have either
one color four times or two colors twice each. The first possibility violates
properness of each Hamilton C5 at t. In the second, let ta,tb have color alpha
and tc,td color beta. Internal ab has color beta and cd color alpha; the four
remaining S edges split into two cross perfect matchings colored gamma,delta.
Every Hamilton C5 must leave t using one alpha and one beta edge. Its internal
S path has three edges and endpoints in different pairs {a,b},{c,d}. It uses
one or three cross edges. With one, it uses ab and cd as well, so the C5 has only
three colors, impossible. With three, its complementary Hamilton C5 uses ab,cd
and the one remaining cross edge, giving the same impossibility there.

**3+2.** Name the internal triangle S={a,b,c} so ab=1,bc=2,ca=3; put T={d,e}.
At a,b,c the permitted cross-edge colors are respectively{2,4},{3,4},{1,4}.
The color tau of de is excluded from every cross edge by uniqueness at d,e.
If tau=4, both cross edges at each S vertex have its single missing triangle
color. Each Hamilton C5 must split these equal-colored pairs, hence would use
one internal triangle edge at every S vertex: an odd total of three incidences,
impossible. Otherwise rename the triangle so tau=1. Then cd=ce=4. The only
color1 edges are ab and de; each Hamilton C5 needs color1, so they lie in
different cycles. The cycle containing ab and not de uses four cross edges
(since d,e each have degree two) and exactly one internal S edge, namely ab.
Thus it contains both cd and ce, contradicting properness at c.

These cases exhaust all B choices and prove the lemma. All obstructions invoked
in its uniqueness step are actual four-edge paths, including non-induced ones.
It follows that no amount of simultaneous D recoloring or switching among ALL
six perfect matchings solves this restricted route. The two full enumerators
also give600 normalized star-D colorings and minimum mu1 for EACH matching,
with zero balanced frames in all3600 such cases.

This is not a new claim of a ROOT counterexample. Graph18 has164715 unrestricted
balanced normal frames, including1200 with spanning paths of length<=2; explicit
colorings are saved. It is the same perfect-matching-only barrier already
proposed in the earlier C22 Issue checkpoint, now given complete global census
and a uniform self-contained folded-five proof. It is used as a negative control
against silently restricting the NEW global selection space.

## 5. Exact simultaneous exchange theorem from boundary profiles

This theorem is for arbitrary finite simple subcubic graphs, not only the tested
orders. Let F,F' be valid preframes on the same graph. Let S be an edge patch
containing every edge whose D/U membership or fixed A color changes. Require S
to be U-CLOSED for both frames: any nonempty U path meeting S has all its edges
in S. Closure can be explicitly obtained by repeatedly adding such path edges;
the process terminates after at most|E| additions, but no small bound on the
resulting patch is assumed.

All outside U components are then identical and have a common orientation. Let
B be those outside components with an edge in some actual four-edge shape
meeting S. Let I,I' be the inside phase variables for F,F'. For a boundary
assignment b on B, define

  sigma_F(b) = min_i number of forbidden actual shapes meeting S,

where i ranges over all inside phases. Define sigma_F' similarly, allowing a
DIFFERENT number and topology of inside U components. Other outside variables
r do not occur in a shape meeting S. Empty phase families have their unique
empty assignment. All profile entries are finite nonnegative integers.

A shape disjoint from S has identical edges, fixed colors and phase variables
in the two frames. Its total cost is a common function rho(b,r). Consequently

  mu(F)  = min_(b,r) [rho(b,r)+sigma_F(b)],
  mu(F') = min_(b,r) [rho(b,r)+sigma_F'(b)].

These equations follow simply by partitioning actual shapes into those touching
S and those disjoint from S, then minimizing the independent inside variables.
Shared graph edges or duplicate algebraic equations cause no cancellation:
actual shapes are counted separately. This covers paths, C4s, chords, self rows,
parallel rows, empty U and changes in the number of U components.

**PROFILE theorem.** If a positive integer delta satisfies
sigma_F'(b)<=sigma_F(b)-delta for EVERY boundary assignment b, then
mu(F')<=mu(F)-delta. Apply the inequality at an old minimizing (b,r).

This is a genuine simultaneous exchange criterion: no single-edge interpolation
is required to be proper, to be a preframe, or to have nonincreasing mu. At the
endpoints of a sequence of such exchanges, mu is a strictly descending natural
number. Hence at most the initial mu exchanges are possible before zero, IF an
appropriate exchange continues to exist. A state with no certified exchange is
not thereby balanced. The statement supplies correctness and a well-founded
measure, not universal availability.

Profiles can be computed from the finite neighborhood consisting of all actual
four-edge shapes touching S and the full U components they reference. No shape
uses more than three edges outside S. This is an exact finite interface, not a
claim of a polynomial-time global solver.

## 6. A topology-changing fork exchange that cannot be split into legal steps

Use the known C24 no-self-loop graph, with ordered edges

  05,06,07,14,16,17,23,25,27,34,36,45,

and old word

  (1,0,2,3,2,4,2,0,3,1,0,0).

Its U paths are P=0-6-3 and Q=2-5-4. The old equations, in these orientations,
come from actual paths0-5-4-3-6,1-6-3-2-5,3-4-5-0-6 and are respectively
x XOR y=1,0,0. Thus its four phase costs are1,2,2,1.

Make ONE simultaneous change:

  06: U -> A color4,
  16: A color2 -> U.

The new word is(1,4,2,3,0,4,2,0,3,1,0,0); P is replaced by1-6-3 and Q remains.
Take the three-edge patch S={06,16,36}. It is U-closed on both sides. The only
outside boundary variable is y on Q. Direct witness classification gives

  sigma_old(0)=sigma_old(1)=1,
  sigma_new(0)=sigma_new(1)=0.

The new sole mixed row is x XOR y=1, supported by0-5-4-3-6. Choose the inside
phase opposite to y. Both D colorings are normally star colored; all touched
shapes and every attaining inside phase are listed in the certificate and
rechecked from graph edges. PROFILE gives a strict reduction1->0.

Neither order of performing the two edits separately is legal. Removing16 from
D first gives U degree three at vertex6. Coloring06 first gives the actual
bichromatic D four-cycle0-6-1-7-0 with colors4,2,4,2. Thus this exchange cannot
be justified by the dead nonincreasing single-entry route, even if that route
were allowed a temporary increase. It is a real endpoint-to-endpoint topology
exchange, not an abstract edit of XOR rows.

The separate example changing05:1->4 and16:2->1 keeps U unchanged. After including
P in the patch it has the same profile improvement. Its specified single-edge
interpolation has mu1,2,0. The new general theorem handles both examples by
inside phase optimization, which is stronger than requiring pointwise loss
under an unchanged full phase assignment.

## 7. Global extremality: exactly the unproved bridge

For a graph with at least one preframe, the finite full frame space has a global
mu minimum. A globally minimizing preframe cannot admit a PROFILE exchange of
positive gain, irrespective of whether the exchange is reachable through legal
single-entry states. This necessary extremal condition follows directly from
Section5; it is not an assertion that local optimality implies global optimality.
There is a useful sharper pointed version. Fix any globally minimizing FULL
phase assignment of a globally minimizing frame, and restrict it to a patch's
outside boundary b*. Its inside assignment attains sigma_F(b*), since otherwise
changing the inside phases alone would lower the global cost. Therefore ANY
valid endpoint exchange with sigma_F'(b*)<sigma_F(b*) contradicts global
minimality, even without domination on other boundary assignments. The inside
profiles remain local finite objects. Proving that such an exchange necessarily
exists at a positive global optimum is an existence lemma, not a consequence
of this extremality observation.

The first open GLOBAL lemma is to exhibit, from a hypothetical positive global
minimum on an arbitrary connected simple cubic graph, a graph-realized joint
path-factor/color exchange with strict profile domination, or a different
strictly improving global construction. No universal augmenting-chain existence,
patch-size bound, or bound on intermediate barrier height is proved here.
The nineteen order-ten optima are positive examples, NOT an induction step.
Perfect-matching-only selection is explicitly inadequate by Section4. The
unrestricted OUTER quantifier must be retained.

## 8. Reproduction, sources, and assurance boundary

The bounded runner pins input streams, exact source and executable hashes,
Python/compiler/crypto-library fingerprints, resource ceilings, exit codes and
output hashes. Mathematical programs use one thread,35-second wall limits,
CPU30/31seconds,768MiB address space and1MiB output-file/stdout ceilings.
SHA-256 is provided by the observed OpenSSL library only for artifact identity,
not for mathematical predicates. Exact graph coverage uses no external catalogue,
nauty, graph library or theorem lookup. All candidate algorithms are supplied.

Compact per-graph summaries, positive colorings, matching decompositions,
exchange profiles and mutation diagnostics are frozen in the packet. Running
the provided programs regenerates complete per-U summaries and the full ordered
frame/phase hash transcript. The latter is hashed online, not asserted stored
as a repository file. Optional local reproduction outputs are not hidden inputs.

C24 historical files were not presumed delivered: the live PR37 and the separate
attachment have different content digests and are kept distinct in the source
note. Known C23R/C24 route failures are negative controls, not routes retried as
positive assertions. No protected file or truth ledger is changed.

No trusted verifier, statement-faithfulness admission, axiom/escape audit or
obligation-closure gate has run for C25. The frozen admission request does not
substitute a local statement for ROOT or impersonate a verifier. State remains
NONTERMINAL_CHECKPOINT and best_verified_result=none.
