# C27 direct follow-up: what cut balance alone cannot force

Verdict: candidate_only. Best verified result: none. State: NONTERMINAL_CHECKPOINT.
Repository: vibemathing/problem-opg-37271-star-chromatic-index-cubic.
Audited candidate head: ae10c3584208290e30e2e6cdafa584f3b89c17e5 (PR40).
Read base: 2ed5df4473ff0bfa71c2b37393b5d044451d5ce4.

## 1. Scope of this continuation

The main C26 core-ports candidate and the conversation C26 support-absorption
archive are different byte sequences. PR39 transported only the former. The
latter archive has SHA-256
2cad12bcf2661fb8d9a0afd968309a9eda437974e58383b1abc279c9a72635ff.
Its eight-vertex literal interface is reconstructed below from the full graph
and words, not by importing its compiler or trusting its saved execution file.
No older candidate is overwritten or represented as newly proved by CI.

The target at a hypothetical positive GLOBAL frame optimum remains open.
The C27 concrete obstruction has one exterior port and a core-incident chain;
it is not the two-distinct-exterior-port case. The interface countermodel in
Section4 is algebraic, not a claimed graph realization. Neither constitutes
a counterexample to GLOBAL-EXCHANGE under its global-extremality premise.

## 2. New literal replay of the actual blocked family

Fix edges, in this order:
05,06,07,14,16,17,23,25,27,34,36,45.
Let F=(1,2,3,4,3,0,4,0,1,0,1,0), with zero denoting U.
The U paths are17 and2-5-4-3. D is normally star colored.
The three actual mixed paths are0-5-2-7-1,1-4-3-2-5,2-3-4-1-7.
Their rows are q XOR p=1, q XOR q=1, q XOR p=1.
The phase costs in integer-bit order are3,1,1,3.

The full self-core hull S={14,23,25,34,45} has10 legal partial endpoints at
each external bit, with envelope(1,1). T=S union{17} has16 partial endpoints
and76 full phase colorings, all with at least one actual forbidden shape.
The new checker enumerates literal support colors1..6 and groups them only
AFTER testing properness, D-star, U length and joint closure. Proper-prefix
pruning is sound because no later edge can repair equal incident assigned
colors. Every accepted literal B assignment is one of the alternating phases;
conversely every phase is a literal assignment in this enumeration. Thus this
is full endpoint/phase coverage, not a prescribed recoloring template.

All actual four-edge paths and C4s are rebuilt by injective vertex tuples;
paths with chords are retained. A separate two-color-component predicate
checks D-star. No C26 or earlier candidate implementation is imported.
The complete 16 by phase table retains an actual bad shape at every entry.
This replays only these declared families, not the older all-cubic census.

All five connected one-edge expansions of T were also reconstructed:
added edge05:169 endpoints, optimum0;
07:119,0; 16:95,0; 27:60,1; 36:116,0.
Adding06 alone is disconnected. The explicit simultaneous05:1->U,25:U->2
repair is checked; both one-edit intermediate partial colorings are invalid.

## 3. Literal C26 absorption and a nonzero-h graph control

On the same ordered graph take
F0=(1,2,0,0,0,3,3,0,4,2,0,3),
Q0=(1,2,0,2,0,3,3,0,4,0,1,3),
A={06,14,16,34,36}, B=A union{07}.
Both are valid endpoints, equal off A, and A/B are jointly U-closed.
At the remaining outside bit0 the two absorbed-bit terms are:

z=0: sigma_old=1, sigma_new=1, h=0, r=0, g=0;
z=1: sigma_old=3, sigma_new=0, h=0, r=2, g=3.

Hence max(g-r)=1. The successful absorbed value is not old-optimal. The other
outside bit gives the flipped table. Discarding old-nonoptimal absorbed bits
would incorrectly erase this real improvement.

For an ACTUAL nonzero-h control use
F1=(1,2,0,0,0,3,3,0,1,2,0,3),
Q1=(1,2,0,0,0,3,3,0,1,0,4,3),
A as above and B1=A union{07,25}.
All endpoint premises are checked. The only newly forbidden shape disjoint
from A is C4(0,5,2,7), edges05,25,27,07. It is bichromatic at equal absorbed
bits. For absorbed bits00,01,10,11 the exact arrays are

sigma_old=(1,3,3,1), sigma_new=(1,2,2,1), h=(1,0,0,1),
r=(0,1,1,0), g=(0,1,1,0).

The gain is zero: both enlarged profiles have value2. h was obtained from
actual graph shapes, not added as an abstract penalty. This is a fixed-endpoint
control only; it does not exclude all larger endpoints or assert that this
particular external row is satisfied at the old optimum.

An earlier proposed variant of Q1 failed the D-star premise. It was rejected,
not used as a mathematical counterexample; the final Q1 above was selected
from the literal legal endpoint enumeration. The final source was then rerun.

## 4. A cut-only implication is false, even with a shortest satisfied chain

The following is explicitly a SIGNED-INTERFACE model, not a subcubic graph.
Use internal variable t and ports p,q. The old local system contains one
negative loop at t, two copies of t XOR p=0 and three copies of t XOR q=0.
Its profile is
sigma_old(p,q)=1+min_t(2[t!=p]+3[t!=q])=(1,3,3,1).
A proposed new local endpoint has profile sigma_new=[p=q]=(1,0,0,1).
Outside put the single equation p XOR q=0, with cost h=[p!=q].

The old full assignment t=p=q=0 has cost1. It is optimal: the loop costs1
for every assignment, and every other equation is satisfied there. Every cut
has nonnegative satisfied-minus-violated margin (the negative loop crosses no
cut). The exterior has a shortest SATISFIED p-q chain of one edge, positive
opposite-parity price1, and no omitted witness multiplicity.

Nevertheless, m=1 and the four boundary records are:

p,q | old | new | h | r | g | g-r
00  |  1  |  1  | 0 | 0 | 0 | 0
01  |  3  |  0  | 1 | 3 | 3 | 0
10  |  3  |  0  | 1 | 3 | 3 | 0
11  |  1  |  1  | 0 | 0 | 0 | 0.

Thus shortest satisfied-chain existence and all cut inequalities DO NOT imply
positive gain for a specified endpoint. Dropping h would predict gain1 and
would be wrong. Three parallel copies raise the separator price to3 without
altering shortest chain length; all copies count.

This rules out only that algebraic implication. It is not an obstruction to
the whole family of graph-realized U/color exchanges. In particular, no graph
with positive globally minimum frame cost is exhibited. Additional geometric
information constructing a NEW endpoint is indispensable.

## 5. The precise remaining global proof obligation

For fixed endpoints F,Q agreeing outside S, enlarging a jointly closed support
releases phase constraints but never changes the endpoint. At every enlarged
R the anchored gain is at most mu(F)-mu(Q), with equality when R=E.
This follows because the constrained phase assignments are a subset of all
Q phases; enlarging R only enlarges that set. The same ceiling applies after
minimizing over a fixed endpoint family. It cannot be escaped by declaring a
distance to an unproved exit.

At a hypothetical positive global frame minimum, proving a gain requires a
geometrically constructed endpoint contradicting that extremality, not just
phase release. For a shortest exterior chain, all newly touched shapes and
newly contacted complete U components must be incorporated into h. If it
fails, enlarging mutable support reduces |E minus support|; this terminates
the finite search, but says nothing about positivity at its last state.
The pair(mu,|E minus support|) therefore is a search measure, not a proof that
every terminal support admits an improvement.

The first open lemma is still: under the prescribed global optimum and
secondary extremality, construct a jointly closed geometric endpoint with
max_z(g-r)>0 after genuine two-port exterior-chain absorption, or exclude the
persistent boundary pattern. None of the one-port family, the abstract model,
or the finite positive examples supplies that implication.

## 6. Reproduction and assurance

Run python3 research/artifacts/candidates/opg37271-c27-direct-run.py in a
writable disposable checkout. The self-contained checker regenerates the full
16-endpoint/76-phase JSON including actual witnesses. The runner records the
source/interpreter/output SHA-256, UTC times, exit status and limits. The full
regenerated JSON is supplied in the conversation recovery archive; its digest
is in the committed execution observation. It is an output, not a hidden input.
The pre-existing C27 expanded certificate has different encoding and is not
silently overwritten.

All observations are in the generator trust domain. No trusted mathematical
workflow, statement-faithfulness receipt, axiom audit or closure gate is
asserted. Existing truth ledgers and admitted statements are unchanged.
