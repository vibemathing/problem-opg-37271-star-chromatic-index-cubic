# C16: distinct two-port transfer and realized boundary sets

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt `attempt:web-20260906-opg37271-a01`; Route `route:leaf-extension-six-colors-v1`.
Graph `graph:opg37271-initial-v1`; admitted target `obligation:opg37271-leaf-extension`.
Root `obligation:opg37271-root` remains open.
Base: `d18d600313481f1f03e7844c3919d9cb9b506428`.

This is a derivation candidate, not a trusted mathematical receipt. It changes the proof strategy from bounded old-color repairs to sets of achievable separator states. A fixed-coloring obstruction is never a root counterexample here.

## 1. Objects and exact quantifiers

Let A,B be disjoint finite simple subcubic graphs with distinct ports x0,x1 in A and y0,y1 in B. Each port has degree at most two within its shore. Add a separate private leaf edge at each port and choose a star k-edge-coloring of each augmented shore. Let the ordered A stub colors be a0,a1 and the B stub colors b0,b1. Every palette has k named available colors; use need not be surjective. A star coloring is proper with no bichromatic simple four-edge path or four-cycle; paths need not be induced.

Delete the four private leaves and replace corresponding stubs by two cut edges x0-y0 and x1-y1. The two cut edges form a matching. We seek ONE permutation pi of B's entire palette with pi(bi)=ai, then use ai on the corresponding cut. Such a permutation requires the stub-color equality patterns to agree.

For p!=ai let L_Ai(p) be the number of edges in the {ai,p} alternating component starting at the ith private leaf. Define L_Bi(q) analogously. These lengths are 1,2,3; each row has at most two entries above one, because the port has at most two old incident edges. All proof steps use only finite-graph-basic and finite-combinatorics.

## 2. Exact transfer for different stub colors

Assume a0!=a1 and b0!=b1. After alignment, the glued coloring is star if and only if

    L_Ai(p) + L_Bi(pi^{-1}(p)) <= 4
    for i=0,1 and every p!=ai.                              (D)

Proof. For a color pair containing neither cut color, nothing changes. For a pair containing only one cut color, the relevant two-color components meet one cut only; the joined path has length L_Ai+L_Bi-1.

For the pair {a0,a1}, the two private stubs in one shore cannot be in the same component. If they were, their component would be a path starting and ending at the two private leaves. Distinct ports make its length at least three. Its first and last edges have different colors, so the length is even, hence at least four, contradicting the shore's star coloring. Thus the two stubs lie in separate components on BOTH shores. Gluing again produces separate paths of the indicated lengths, not a cycle. This proves (D) in both directions. Properness follows because the aligned cut replaces a private stub of the same color.

For equal stub colors the same inequality is valid, but its proof must include linked stubs and the potential four-cycle; C15 supplies those missing cases. Combining the two arguments gives an exact criterion for all matching two-port inputs whose equality patterns agree.

## 3. Fixed cross tests and a residual perfect matching

With distinct stub colors, two inequalities in (D) cannot be improved by changing the remaining permutation:

    L_A0(a1) + L_B0(b1) <= 4,
    L_A1(a0) + L_B1(b0) <= 4.                               (X)

Let D_A=C_A minus {a0,a1} and D_B=C_B minus {b0,b1}. Form a bipartite graph D_B->D_A, allowing q->p exactly when

    L_A0(p)+L_B0(q)<=4 and L_A1(p)+L_B1(q)<=4.               (M)

An aligned permutation succeeds exactly when (X) holds AND (M) has a perfect matching. Necessity restricts a successful permutation to D_B; sufficiency extends the matching by b0->a0,b1->a1, then uses Section 2. At six colors this test has four colors on each side and sixteen possible pairs. Neither row is checked with a separate permutation.

Subject to (X), every such input can be aligned for k>=8. Indeed there are n=k-2>=6 residual colors. A left color active at both ports has at least n-4>=2 neighbors, and at most two left colors are shared. A color active once has at least n-2>=4 neighbors, and at most four colors are constrained in total. An unconstrained color has all n neighbors. Hall's condition follows by separating subsets containing an unconstrained color, subsets consisting solely of shared colors, and the remaining subsets of at most four constrained colors. This is the C15 Hall argument with two reserved colors, not a claim that eight is needed to color the original graph.

At k=7 the residual graph has five vertices per side. Exactly the two Hall-deficiency patterns I/II plus the forbidden-rectangle condition of C15 apply, now only to residual active sets. At k=6 the residual graph has four vertices per side; the C15 classification MUST NOT be reused without proof. The exact perfect-matching test remains valid.

## 4. Cross-color obstruction independent of palette size

For T=A,B take four vertices Tx0,Tz,Tw,Tx1, and precisely the three edges

    Tx0--Tz : 2;  Tz--Tw : 1;  Tw--Tx1 : 3.

Add private stubs with colors 1 at Tx0 and 2 at Tx1. The augmented shore is a five-edge path colored 1,2,1,3,2, which is proper and has no alternating four-edge segment. Delete the private leaves, glue the first cut with color 1 and the second with color 2. Both aligned colorings have L_0(2)=3, violating (X).

For EVERY palette size k>=3 and EVERY pi fixing 1 and 2, the simple path

    Aw, Az, Ax0, Bx0, Bz

has colors 1,2,1,2. Thus no palette size guarantees arbitrary fixed-shore alignment with distinct boundary colors. Additional unused colors cannot change this invariant obstruction.

The glued graph is just an eight-cycle, with cyclic vertex order

    Ax0, Az, Aw, Ax1, Bx1, Bw, Bz, Bx0.

Color its consecutive edges 1,2,3,4,1,2,3,4. Every consecutive four-edge segment has four colors, so this is a star four-edge-coloring. Hence the fixed-shore failure is not a failure of root coloring.

## 5. Sharp conditional threshold eight

For each shore T use Tx0,Tx1 and Trij,Ttij for i,j=0,1. Add Txi-Trij of color cij, and Trij-Ttij of color 1 when i=0 and color 7 when i=1. Add connector Tt00-Tt10. Use rows

| shore | c00 | c01 | c10 | c11 | connector |
|---|---:|---:|---:|---:|---:|
| A | 2 | 3 | 4 | 5 | 6 |
| B | 2 | 3 | 2 | 3 | 4 |

The two private stubs have colors 1 and 7. Each augmented shore is a star-colored tree: same-root-color/spoke components have length three, the connector joins a color-1 and a color-7 support but cannot produce a two-color four-path, and pairs of spoke colors have components of length at most two. The exact companion checker also checks every color pair.

Both fixed cross lengths on both sides are one. The residual active sets are P0={2,3}, P1={4,5}, Q0=Q1={2,3}, with active lengths three. At seven colors the two Q colors have only residual color 6 available, so no permutation works. At eight colors they can map to 6 and 8. A full successful permutation is

    1->1, 2->6, 3->8, 4->2, 5->3, 6->4, 7->7, 8->5.

This is a realizable twenty-vertex input, not an abstract profile. It proves sharpness of the universal palette threshold UNDER condition (X), and does not assert any root lower bound.

## 6. Root-faithful attainable-set reduction

For a shore A with two ordered distinct ports, let S_6(A) be the set of ordered signature pairs arising from ACTUAL star six-edge-colorings of its augmented shore. Each pendant signature consists of a stem color and five lengths in {1,2,3}, at most two above one. There are

    6 * [1 + 5*2 + choose(5,2)*4] = 306

such raw single-port signatures. Thus S_6(A) is a subset of a space of 306^2=93,636 ordered pairs: 15,606 same-stem and 78,030 distinct-stem pairs. This bound DOES NOT assert that arbitrary pairs are jointly realizable on A. The exact graph A and its actual colorings define the set.

For G obtained by joining A,B with the matching two-edge cut,

    G has a star six-edge-coloring
    iff some sigma in S_6(A) and tau in S_6(B) are compatible.

Compatibility means matching equality patterns and the successful exact permutation test from C15 (equal colors) or Sections 2-3 (distinct colors).

Proof of necessity. Restrict a coloring of G to A and its two cut edges; their two distinct B endpoints become the two private leaves, so this is a subgraph of G. Do the same on B. The two realized signature pairs are compatible under the identity permutation. Sufficiency picks realizing augmented-shore colorings and a successful common permutation, then invokes the exact gluing theorem. Both directions preserve the existential quantifier over shore colorings rather than freezing an arbitrary choice.

If G is a vertex-minimal counterexample to the root and each shore has at least three vertices, both augmented shores have fewer vertices than G. Therefore their attainable sets are nonempty, but EVERY pair across the two sets must fail compatibility. The examples above prove that nonemptiness plus one arbitrary choice is not enough. A genuine two-cut reduction must prove some compatible pair exists in the realized sets, or identify an excluded structural configuration. No general two-cut reducibility is asserted here.

An immediate sufficient condition is an actual same-stem pair for which one of the four active sets has size at most one. Neither C15 obstruction pattern is then possible. Existence of such a pair is a separate obligation, not an automatic consequence of minimality.

## 7. Finite diagnostics and checkpoint

A bounded local standard-library run checked the eight-cycle obstruction for all aligned permutations in palettes 6,7,8 (24,120,720 cases respectively); none succeeded and all agreed with the exact transfer inequalities. It checked the conditional-threshold example in palettes 7 and 8: 0/120 and 48/720 permutations succeeded respectively. It verified the supplied free four-coloring. Separately, all 7,776 colorings of an actual five-edge path were screened: 3,480 were star (600 equal end colors, 2,880 distinct), yielding 1,980 actual signature pairs with sample explicit backpointers. This is a bounded realizability check for one shore graph, not a universal closure of arbitrary profiles.

Runtime was CPython 3.13.5, standard library, one thread, 20-second wall alarm, CPU limits 20/21 seconds, address-space limit 512 MiB, output cap 262,144 bytes. The program uses explicit exceptions and fixed finite loops. It writes the result beside itself; replay in a disposable copy. No repository script, trusted verifier, or theorem prover ran.

Dependencies: C15 at the exact base above, C08's single-branch signature idea, and the frozen contract/graph. No external proof is claimed. Both admitted obligations remain open. Best verified result: none. Best verified candidate: none. State: nonterminal.

Next precise action: audit the newly located full Fernando-Athapattu article against its Theorem 18, not merely its abstract; retain the attainable-set separator invariant while checking proposed local reductions. A forthcoming source note must distinguish a false intermediate claim from a counterexample to the root theorem.
