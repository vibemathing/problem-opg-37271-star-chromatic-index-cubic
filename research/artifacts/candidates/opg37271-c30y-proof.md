# C30Y: complete order-eleven exact-interface audit

Verdict: candidate_only. Best verified result: none.
State: NONTERMINAL_CHECKPOINT. ROOT and GLOBAL-EXCHANGE remain open.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Base main: 3ee4c60c3feb274e60b9a54e430c2d135f77fed8.
This addendum belongs to the existing C30 branch, PR43 and packet only.

## 1. Result and unfulfilled target

The requested eleven-or-more-vertex frame blocking every connected support
of size at most three was NOT found. The exact eleven-vertex domain below
was instead exhausted: every eligible connected graph/frame has a jointly
U-closed connected support of size at most three and ONE new partial endpoint
that improves both old optimal boundaries from cost one to zero.

This finite theorem candidate is not a general augmenting-chain theorem.
It rules out the requested next blocker at order eleven ONLY in this exact
seven-occurrence, three-old-U-component domain. Prior C30X addresses orders
at most ten; combined at candidate level, a blocker in this precise domain
would have at least twelve vertices. Additional old witnesses, additional U
components, arbitrary completions, and general negative cores are not covered.
No positive globally minimizing frame or ROOT counterexample is exhibited.

## 2. Definitions, phases and exact scope

G is finite, connected, simple, has exactly eleven vertices and maximum degree
at most three. All vertices, including those outside U, remain in the input.
E=D disjoint-union U. D is properly star colored in A={1,2,3,4}; U consists
of exactly three nonempty vertex-disjoint paths T,P,Q of lengths at most three.
Each U path alternates B={5,6}. A simple four-edge path has five distinct
vertices and need not be induced. A four-cycle has four distinct vertices.
Shapes are counted modulo reversal/dihedral symmetry, not modulo their
algebraic row. Shared edges cause no cancellation of different shapes.

The COMPLETE old mixed-shape multiset has one negative T self row, two T-P
rows, three T-Q rows and one P-Q row. All six nonloop rows are coherent.
No other old mixed witness is permitted. The P-Q occurrence may additionally
be required to be exterior to a chosen core hull; that requirement only
restricts the tested domain, so the conclusion still applies to that subcase.

With position parity p(e), the safety row for two U edges e,f is
x_component(e) XOR x_component(f)=1 XOR p(e) XOR p(f). Every decoded coloring
is proper. All-D bad shapes are excluded by D-star; all-U bad shapes by the
path-length bound. Hence these rows count ALL possible violations.
The self row always contributes one. The six coherent nonloop rows have
exactly two simultaneous solutions because their variable graph is connected.
Thus mu=1 and there are exactly two old optimal phases, differing by swapping
all colors5 and6. Neither phase-optimality nor this unique shortest self core
is asserted to imply GLOBAL frame optimality.

## 3. Coverage proof retaining passive D constraints

A self row uses two disjoint edges in one U path; that path must have length
three, and the edges are its first and third. T uses four vertices. Write the
other lengths p,q. At order eleven, 1<=p,q<=3 and p+q<=5, giving eight pairs.
Relabel the three paths onto consecutive vertex blocks and retain every other
vertex. Fix T's phase origin. The four coherent gauges (0,a,b) exhaust all
nonloop sign choices, so there are exactly 32 topology/gauge cases.

Represent the FULL input by its participating D-color classes and its remaining
passive D edges. Each participating color class is a matching and each edge
in it occurs with a same-colored partner in an old mixed witness. Enumerate
all such matchings, retaining the exact (1,2,3,1) row counts, all multiplicities
and signs. Enumerate compatible unions of at most four classes. Compatibility
checks distinct edges, the subcubic degree bound after adding U, and D-star.
For a union of two proper color classes, D-star is equivalent to every
component having at most three edges: a larger proper two-colored component
contains a four-edge path or cycle. This checks the complete D restriction.

Only reversals of the three designated U paths and global A-name permutations
are quotiented. They are explicit graph/color isomorphisms preserving all
shapes, phases, supports and endpoint conditions. Remaining D-only vertices
are not silently identified. The resulting counts are representation records,
not unlabelled graph-isomorphism counts.

For EACH participating description, enumerate all residual-degree-feasible
additional D edges on the same eleven vertices, including absence and all
four A colors. Keep the COMPLETE graph for degree, connectedness, properness,
D-star, exact old witness signature and every repair check. In particular,
passive edges sharing an existing color class or using a previously unused
color are both included. No passive edge is removed from a fixed-frame repair.

Completeness: every eligible frame splits into these two parts, so its
participating classes occur after a permitted A renaming. Every remaining
edge is one of the residual-degree pairs and has one of the enumerated colors.
The accepted completion therefore reproduces the FULL original frame. The
reverse implication is checked directly on each accepted complete graph.
Adding edges cannot erase an ordinary path merely by adding a chord, and
cannot repair an already excessive degree or improper/star-invalid coloring;
thus the producer's prefix pruning removes no eligible completion.

The checker reconstructs these domains by a different enumeration: increasing
disjoint edge subsets for color classes; then uncolored residual graphs first,
then proper color prefixes and full D-star/signature checks. Its class geometry
uses two disjoint two-edge matchings: their four-edge union is a path/C4 exactly
when it has five/four vertices. A disconnected four-edge union of paths has at
least six vertices; a proper even cycle already consumes at least four edges.
The matching and distinct-edge premises are checked before this lemma is used.
On complete graphs it rebuilds actual shapes by injective vertex walks.

## 4. Endpoint certificate and minimum support

A support is a connected nonempty set S, closed for every old and new U path
it touches. Outside full colors are fixed to an old optimal phase. Inside S,
all literal colors1..6 are allowed, with arbitrary simultaneous D/U changes.
The new frame may have a DIFFERENT number of U components. No legal or
monotone single-edge interpolation is assumed.

The producer searches all supports of sizes1,2,3 in order and all literal
colorings on each, retaining properness, absence of ALL bad shapes and new
U closure. Since old mu=1, an anchored strict improvement is exactly a
star-six coloring. Any such coloring's A restriction is star and its B
components are alternating paths of length<=3; cycles or longer paths would
contain a forbidden four-edge shape. Conversely every balanced endpoint
at this boundary appears as a literal coloring in that enumeration.
A support disjoint from the unique old bad shape cannot improve because
all four colors of that shape would remain fixed outside it.

For every completed frame, the saved literal coloring is checked from the
edge table, not just from XOR rows. For claimed width2 or3, the checker
exhausts every smaller connected old-U-closed support and its literal color
assignments, with an explicit new-U-closure test at each accepted leaf.
Pruning a completed bad shape is sound because all its assigned colors are
fixed in that branch. Thus those widths are minima for the pointed frame.
Width denotes the CLOSED SUPPORT size, not the number of altered entries.

Swap5 and6 everywhere in the saved new coloring. It remains star, its partial
D/U frame and A colors stay identical, and its outside colors now match the
second old optimum. Therefore the SAME partial endpoint improves BOTH old
optimal phases. A pointwise assertion at all eight nonoptimal old phases is
not made for the arbitrary certificates in this classification.

## 5. Complete finite result

All32 topology/gauge cases and all315 canonical participating representatives
were reconstructed. Their full CONNECTED passive completions give:

| Minimum closed connected support | Full completion records |
|---|---:|
| 1 | 17433 |
| 2 | 132 |
| 3 | 6 |
| greater than3 | 0 |

Total17571 records; all passive constraints were retained. The checker rebuilt
1359135 actual four-edge shape occurrences over those records, with repetition
across distinct inputs. That is not a count of unlabelled shapes or graphs.
Each record tests all eight old phases and both optimal boundary extensions;
only actual smaller-support searches are used for the claimed minima.

The 32 model outputs, complete ordered catalog, 40 completion batches and 40
replay summaries regenerate from committed source. Each batch binds full
input edge/color data, added passive edges, old phase, support, successful
new coloring, and exact profile digest. The certificate binding records the
ordered output manifest digest. Expanded tables and the detailed execution
journal are retained in the recovery archive, not falsely described as main
files. There is no uncommitted mathematical input needed for reproduction.

## 6. Exact sigma,h,r,g for every saved exchange

For each support S, let H be the whole old self-core witness plus its complete
U path and put T=S union H. S touches the old bad shape, so T is connected.
H is old-U-closed; S is jointly closed and both endpoints agree outside it.
Every new U path outside S is therefore an unchanged old path, so T is closed
at the new endpoint too. These premises are checked in both implementations.

For all outside-S phase assignments b, separately minimize internal phases
to obtain sigma_old,S(b) and sigma_new,S(b) from actual shapes touching S.
The common h(b) counts all bad shapes touching T but disjoint from S. They
contain no internal-S U edge and all their edges/colors are unchanged, so h
is independent of the internal minimization and identical at both endpoints.
Partition b into absorbed z and retained y, and define
m(y)=min_z(sigma_old,S(z,y)+h(z,y)),
r(z,y)=sigma_old,S(z,y)+h(z,y)-m(y),
g(z,y)=sigma_old,S(z,y)-sigma_new,S(z,y).
Direct subtraction of the two minima proves
sigma_old,T(y)-sigma_new,T(y)=max_z(g(z,y)-r(z,y)).

Every term, old/new selected row, U component, and complete geometric shape
set is rebuilt by the checker and compared with the producer's profile digest.
No new witness is omitted and no geometric multiplicity is collapsed. This
is an evaluation of supplied endpoints, not a claim that releasing phases
constructs new endpoints or exhausts all endpoints on larger T.

## 7. Reproduction, provenance and remaining gap

Run python3 research/artifacts/candidates/opg37271-c30y-run.py in a disposable
POSIX checkout. It reproduces ONLY this order-eleven classification and its
negative tests; it does not run C30X's old order-ten main program. Each child
has wall35s, CPU30/31s,768MiB address-space,1MiB file and single-thread limits.
The portable runner also enforces64KiB stdout and16KiB stderr limits and a
1800-second total wall bound. It writes a new observation, never truth records.

Actual work in this continuation was executed in bounded batches:32 producer
case jobs,40 completion jobs,32 separately reconstructed case jobs and40
endpoint/profile replay jobs, plus a bounded catalog reproducibility check and
one final24-test diagnostic stage. All completed jobs returned0 with empty
stderr. During development, profile serialization was normalized to JSON lists
and the checker passive-domain search was optimized; pre-edit generation
observations retain their actual source digests. The final checker reconstructs
the full domains and results. No claim of a single unchanged development source
or a fresh execution of the old order-ten census is made.

A small number of preliminary discovery/outer orchestration cutoffs are not
included as successful final stages. Separate order-twelve probes found no
new width>3 example, but did not cover the full order-twelve domain and are
NOT used for the theorem or its lower bound. Twenty-four final negative and
boundary checks include wrong h/r/g, lost self/multiple rows, wrong optimal
phase, missing support closure, palette violations, non-simple shape records,
and literal C4/noninduced-path controls.

C30X's original proof/code/input and observation are preserved as distinct
recovery artifacts. The remote C30 package and older conversation C30 package
are different byte sequences and neither overwrites the other. This extension
adds compatible entries to the existing PR43 packet; it creates no new packet.
All computation and proof remain in the generator trust domain. No trusted
verifier, statement-faithfulness, axiom audit or obligation closure has run.

First open global lemma: an actual order-twelve-or-larger exact embedding,
or a separately frozen larger interface, with all passive constraints and
all supports<=3 unsuccessful, followed by a legitimate larger joint repair
or a precisely scoped failure certificate. More generally the existence of
an improving joint endpoint at a hypothetical positive GLOBAL minimum remains
open. Finite success here is neither an induction nor a universal exit lemma.
