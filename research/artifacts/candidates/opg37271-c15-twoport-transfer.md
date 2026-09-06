# C15: exact two-port transfer and the six-color permutation obstruction

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; admitted target: `obligation:opg37271-leaf-extension`.
Root: `obligation:opg37271-root`, still open.
Base: `1b2e1a6fda9ee30b832aa1ec3459623838faf0c4`.

This continues C14B's bridge analysis, not the already attacked zero-, one-, or two-edit tree assertions. Only finite-graph-basic and finite-combinatorics are used. Every statement below is a candidate awaiting mathematical verification.

## 1. Frozen two-port question

Let A,B be disjoint finite simple subcubic shores. Choose distinct vertices x0,x1 in A and y0,y1 in B. Augment each shore with two PRIVATE pendant edges at its chosen vertices, retaining maximum degree three. Both augmented shores are star k-edge-colored; assume the two pendant edges on each shore have the same color. A palette permutation first aligns these two common colors to a. Delete the private leaves and add x0-y0 and x1-y1, both of color a.

The question here is whether a SINGLE permutation of all colors in B, fixing the aligned color a, can make this gluing star. All other shore colors are held fixed up to that permutation. This is stronger than the root's existential coloring requirement. The cut is a matching; shared port vertices are excluded. The same-color premise is essential.

For i in {0,1} and b != a, define L_Ai(b) as the length of the alternating {a,b}-path starting at the private leaf at xi, and define L_Bi similarly. Lengths are 1,2,3. Each row has at most two nonunit entries. Set Pi={b:L_Ai(b)>1} and Qi={b:L_Bi(b)>1}.

## 2. Exact gluing criterion, including a four-cycle

For already aligned shore colorings, the glued graph is star exactly when

    L_Ai(b) + L_Bi(b) <= 4   for every i and b != a.          (T)

Fix a pair {a,b}. Properness makes each two-color component a path or an even cycle. Components incident to a private pendant edge are paths of at most three edges. The two private edges in a shore either belong to separate paths or belong to a common path. In the common-path case the path is necessarily private-leaf--x0--x1--private-leaf, with colors a,b,a: its internal part has exactly one edge. Call that shore linked for this pair. Both its L values then equal three.

If neither shore is linked, the two glued components are separate paths with lengths L_Ai+L_Bi-1, so (T) is necessary and sufficient. If just A is linked, there is one path of length L_B0+L_B1+1. It has at most three edges exactly when both B lengths equal one, precisely (T). The same holds with A,B exchanged. If both shores are linked, the gluing is a bichromatic four-cycle and (T) fails. These cases exhaust the components touched by the cut. Other two-color components are unchanged; pairs not containing a acquire no new edge. Properness is inherited at all four distinct ports. This proves both directions and does not overlook the cycle case.

The one-port formulas therefore remain usable only as SIMULTANEOUS constraints on the SAME permutation; choosing a different permutation at each port is not a gluing operation.

## 3. A bipartite matching test for a common permutation

Let D be the k-1 colors other than a. Form a bipartite graph with B-colors q on the left and A-colors p on the right. Allow q to map to p exactly when

    L_A0(p)+L_B0(q)<=4 and L_A1(p)+L_B1(q)<=4.               (M)

The desired palette permutation exists exactly when this graph has a perfect matching. A permutation gives the matching; conversely a matching extends by a->a and (T) applies. This is a test of actual colored shore inputs, not a claim that arbitrary vectors are realizable.

We use Hall's finite matching criterion. For completeness, its sufficiency follows by induction: if a nonempty proper left subset S is tight, match S to N(S) by induction and match the complement after removing N(S); Hall for the complement follows by applying the original condition to S union each tested subset. If no such tight subset exists, fix any edge and delete its two endpoints; every remaining proper subset had at least one spare neighbor. Apply induction. Empty and singleton cases are immediate.

## 4. Complete six-color obstruction classification

For k=6, the matching test fails exactly in one of the following two configurations, together with condition (R) below:

I. P0,P1 are disjoint two-element sets, and Q0=Q1 is a two-element set.
II. Q0,Q1 are disjoint two-element sets, and P0=P1 is a two-element set.

The additional condition is

    L_Ai(p)+L_Bi(q)>4 for all p in Pi, q in Qi, i=0,1.      (R)

Equivalently, at each port, either every active A length equals three or every active B length equals three. An active length is two or three, so the only compatible active-active combination is two plus two.

Proof of completeness. A left color outside Q0 union Q1 has all five neighbors. A color in exactly one Qi has at least three neighbors. A color in Q0 intersection Q1 has at least one neighbor, and at most two colors are in that intersection.

A Hall-deficient singleton is impossible. A deficient two-set must consist of two intersection colors with the same singleton neighbor set. Thus Q0=Q1 has size two and each color forbids the same four right colors. Each Pi has size at most two, so P0,P1 are disjoint two-sets, and all the corresponding pairs must really be forbidden: (R). This is I.

A three-set contains a nonintersection color, with at least three neighbors, so it cannot be deficient. For a deficient four-set, no member can be unconstrained. Hence Q0 union Q1 has size four, both Qi have size two and are disjoint. Every member has at least three neighbors; deficiency forces all four neighbor sets to equal the same three-set. Their two forbidden colors must equal P0=P1, and (R) again holds. This is II. A five-set includes an unconstrained color and has all five neighbors. These exhaust all possible sizes.

Conversely I has its common two left colors confined to the one color outside P0 union P1. In II the four constrained left colors have only the three colors outside P0. These are explicit Hall-deficient subsets. Thus the criterion is exact, not merely a sufficient obstruction pattern.

## 5. Seven colors always suffice for this restricted operation

For k>=7 a common permutation always exists under the same-color two-stub premise. It suffices to avoid all active-active matches, a stronger constraint than (M). A shared active left color forbids at most four right colors, leaving at least k-5>=2; there are at most two such left colors. A left color active at only one port leaves at least k-3>=4 neighbors. There are at most four constrained left colors altogether. Hall follows: subsets containing an unconstrained color have all k-1 neighbors; subsets of shared colors have size at most two; all other constrained subsets have size at most four and a member with at least four neighbors. Section 3 finishes the proof.

The following realizable six-color example shows that seven is the smallest palette threshold for this universal SAME-COLOR, SINGLE-PERMUTATION assertion. This says nothing about a seventh color being necessary for the graph itself.

## 6. Explicit twenty-vertex witness and its six-color repair

Names and all edges are specified as follows. For T=A,B use distinct vertices Tx0,Tx1 and Trij,Ttij for i,j in {0,1}. Each shore has ten vertices. Add edges Txi-Trij of color cij and Trij-Ttij of color 1, plus Tt00-Tt10 of the connector color below.

| shore | c00 | c01 | c10 | c11 | connector |
|---|---:|---:|---:|---:|---:|
| A | 2 | 3 | 4 | 5 | 6 |
| B | 2 | 3 | 2 | 3 | 4 |

Add the two private stubs of color 1 when checking each augmented shore. Each augmented shore is a subcubic tree. In A all colors except 1 occur once, and each {1,cij} component has at most three edges. In B the {1,2} and {1,3} components at the two ports are separate three-edge paths; the {2,3} components have two edges; the connector gives only a three-edge {1,4} component. Other pairs cannot have four edges. Both augmented colorings are star.

Remove the private stubs and add Ax0-Bx0 and Ax1-Bx1, both with color 1. The result has twenty vertices and twenty edges. Its boundary signatures have all four active lengths equal to three on each side, with P0={2,3}, P1={4,5}, Q0=Q1={2,3}. This is obstruction I.

For ANY permutation pi fixing 1, some q in {2,3} maps into Pi at some port i. Let j_A locate pi(q) in the A row and j_B locate q in [2,3]. The simple four-edge path

    Ar(i,j_A), Ax(i), Bx(i), Br(i,j_B), Bt(i,j_B)

then has colors pi(q),1,pi(q),1. These formulas are a full certificate for all 120 possible aligned permutations. The result JSON additionally packs the 120 explicit path records as zlib-compressed UTF-8 JSON, encoded in base64; its decompressed objects have pi_2_to_6, path, and colors fields.

The graph itself has a six-star-coloring: permute B by (2 4)(3 5), keep A fixed, retain the first cut color 1, and change the second cut color to 6. Each two-color component of this explicit full coloring has at most three edges, checked in the companion program. A hand check also follows: the endpoints of the color-6 cut have other colors {4,5}, and its possible extensions stop after one edge on each side; the other color-6 edge is the A connector, whose endpoints have other color 1. No new alternating four-path can connect these two 6-edges. Paths through the first cut obey (T), and a path using both cuts would require a shore path between its ports of length at most two, whereas both such distances are five. The unique cycle has twelve edges. Thus this example attacks only the proposed fixed-shore gluing strengthening, not the root.

## 7. Finite diagnostics, limitations, and next obligation

The companion standard-library program checked both augmented shore colorings, all 120 permutations with explicit simple path obstructions, the supplied free-boundary six-coloring, and a four-cycle mutation. It also checked 10,201 ordered canonical length-profile cases for each of six and seven colors. There are 101 profile representatives before further residual-symmetry identifications: support sizes and intersection are canonicalized independently on the two sides, and each active incidence receives length two or three. At six colors all 98 incompatible cases agree with I/II+(R); at seven none fail. These are symmetry-reduced algebraic diagnostics, NOT a count of all realizable graph inputs. The general proofs above do not rely on them.

Observed runtime: CPython 3.13.5, standard library, one thread, wall alarm 30 seconds, CPU limits 30/31 seconds, final address-space limit 512 MiB. An initial 256 MiB run completed the uncompressed checks; a later compressed-output attempt failed in zlib with MemoryError. Increasing the final explicit limit to 512 MiB produced the saved result. This transport-output failure was not treated as a mathematical counterexample. The script enforces a 262,144-byte output bound and uses explicit exceptions, not assert statements. Replay writes the result beside the script; use a disposable copy.

These are local generator-side observations, not repository-script execution, an admitted verifier run, or a change to command_execution in the Web profile. No EvidenceLink or Result is supplied. C14B and the frozen contract/graph are the repository dependencies; no claim of novelty is made.

A two-edge-cut reduction for a vertex-minimal root counterexample now needs control over the SET of achievable boundary signatures, not just arbitrary augmented-shore colorings plus one palette permutation. The next falsifiable target is to show that one shore admits a coloring escaping I and II, or to give an explicit obstruction to that escape premise. Distinct stub colors need a separate theorem; they are not covered by Sections 4-5.

Best verified result: none. Best verified candidate: none. Open obligations remain the admitted leaf target and root. State: nonterminal.
