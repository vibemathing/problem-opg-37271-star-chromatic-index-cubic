# C18D: diamond-ended ladders and disjoint triangles in a minimal counterexample

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; admitted target: `obligation:opg37271-leaf-extension`.
Root: `obligation:opg37271-root`, still open.
Base: `7cb2aa0c860a95a5693300d4153f9d794ac90a40`.

## 1. Exact scope and the finite fragment

This candidate completes the adjacent-external-neighbor case deliberately left open in C17D. The conclusion is conditional: if a minimum-order counterexample to the root exists, its triangles are pairwise vertex-disjoint. This is not a theorem that the whole graph is triangle-free, nor a root coloring theorem.

Let S_t, t>=1, consist of a diamond p,q,r,s with edges pr,ps,qr,qs,rs, followed by t ladder rungs. Put a_0=p,b_0=q. For j=1,...,t introduce distinct new vertices a_j,b_j and edges a_(j-1)a_j, b_(j-1)b_j, a_jb_j. All names are distinct. S_t has 4+2t vertices and 5+3t edges. Every vertex except a_t,b_t has degree three inside the fragment; its two terminals have degree two and are adjacent.

## 2. An explicit five-color periodic coloring

Color the diamond edges in the order pr,ps,qr,qs,rs by

    3,6,2,4,5.

The left rail colors ell_j have period (4,2,3); the right rail colors mu_j have period (3,4,2). The rung color h_j is 5 for odd j and 6 for even j. In formulas:

    c(a_(j-1)a_j)=ell_j,
    c(b_(j-1)b_j)=mu_j,
    c(a_jb_j)=h_j.

Only colors 2,...,6 occur. At the terminals the palettes are {ell_t,h_t} and {mu_t,h_t}, where these three colors are distinct.

Claim L. This is a star edge coloring for every integer t>=1.

Properness follows from the displayed head and rail periods; every two consecutive rail colors differ, and rung colors are outside the three rail colors. To audit the head completely, in S_4 the maxima of the edge counts of two-color components are:

    pairs 12,13,14,15,16: 1,1,1,1,1;
    pairs 23,24,25,26:    3,2,2,3;
    pairs 34,35,36:       3,3,2;
    pairs 45,46:          3,3;
    pair 56:             2.

Every four-edge path or four-cycle touching a diamond edge is contained in the head and at most the first four rungs. For t<4 it is a subgraph of this fixture. The table therefore covers all head cases, not an induction based only on experiments at several lengths.

For the remaining paths wholly in the ladder, classify by the number of rung edges. With no rung, a simple path follows one rail, and four consecutive rail colors use all three rail colors. With one rung, its color occurs only once along the path, precluding a two-color alternating four-edge path. With two rungs their indices differ by one or two. For consecutive rungs there is one rail edge between them: the rung positions have the same parity but their colors differ. For rungs two indices apart there are two rail edges between them: the rung positions have opposite parity but their colors agree. Both contradict alternation. Three rungs require at least five edges because distinct rungs are vertex-disjoint. This exhausts four-edge paths. A four-cycle in the ladder is one cell; its adjacent rung colors differ, excluding alternation. Thus Claim L holds for arbitrary length.

## 3. Root-faithful edge replacement for every S_t

Let H be any star six-edge-colored finite simple subcubic graph and zw an actual edge with color alpha. Delete zw, insert a fresh S_t, and add z-a_t and w-b_t. This replacement preserves every old color on H-zw.

Write A=c_H(z)-{alpha}, B=c_H(w)-{alpha}. Put U=C-({alpha} union A), V=C-({alpha} union B). Both sets have at least three elements in the five-element set C-{alpha}. Choose h in U intersection V, i in U-{h}, and j in V-{h,i}. Rename the five internal colors so that (h_t,ell_t,mu_t) maps to (h,i,j), extending the injective assignment to a bijection onto C-{alpha}. Color both new cap edges alpha.

The internal coloring is star by Claim L and contains no alpha. At z and w properness follows from the removed edge. The internal terminal palettes avoid A and B.

Here is the complete outside argument. A pair not involving alpha cannot cross a cap edge. For {alpha,beta}, the old component through zw was a path of at most three edges. Removing zw leaves distinct endpoint arms, each with at most two edges; there is no old alternating connection between z and w, which would have made the old component a cycle. Inside the fragment the beta edges form a matching because there is no alpha and the coloring is proper.

If the two caps are joined internally, the connecting edge is the terminal rung. Its color is h, which avoids both A and B. Both outside arms are empty, so this component is exactly alpha,h,alpha, of length three. Otherwise a component through one cap has either an outside arm of length at most two OR one internal beta edge, never both, by palette disjointness. Its length is at most three. The two caps cannot connect outside by the old-component argument. There is no omitted crossing cycle. This proves universal extension of the reduced coloring through S_t.

The input is a coloring of the SMALLER graph with an actual edge zw. This is not an assertion that arbitrary fixed colorings on two large shores can be aligned by one permutation.

## 4. Closing fragments and all terminal exceptions

A fragment S_t by itself has Claim L's coloring. A single leaf at either terminal can receive color 1, which is absent internally. Since a bichromatic alternating four-edge path/cycle needs each color at least twice, that addition is harmless.

For a common external vertex z joined to both terminals, use the unrenamed coloring in Section 2 and set

    a_t-z=1, b_t-z=ell_t.

If z has one further leaf w, set

    z-w=mu_t for t>=2;
    z-w=2 for t=1.

These colorings are proper. Color 1 occurs once and cannot participate in an alternating four-edge obstruction. Ignore that edge for the rest of the check. The newly attached path at b_t has first color ell_t and, when the leaf is present, second color gamma.

For a potential four-edge path whose endpoint edge is b_t-z, a continuation through the rung has colors ell_t,h_t,ell_t, and would require an h_t edge at a_(t-1). There is none: at t>=2 the previous rung uses the opposite rung color, and its rails have colors 2,3,4; for t=1, p has no color h_1=5. A continuation through the incoming right rail cannot continue with ell_t at b_(t-1) when t>=2, since mu_(t-1) differs from ell_t and the previous rung color is 5 or 6. For t=1, the only such continuation goes through q-s of color 4, but s has no color mu_1=3. Thus no endpoint obstruction is possible.

When z-w is present and t>=2, the only potential alternating continuation from that new leaf starts with mu_t,ell_t,mu_t and would again need ell_t at b_(t-1), absent as just shown. For t=1 the special choice gamma=2 is not incident at b_1, whose old palette is {3,5}, so no alternating continuation can start. No other case contains two new edges after ignoring the unique color-1 edge. There are no new cycles without that edge. This verifies both common-neighbor closures for all t.

The one-rung exception is necessary for this formula: the naive gamma=mu_1=3 creates the path w-z-b_1-q-s colored 3,4,3,4. The companion checker rejects this mutation and accepts gamma=2.

## 5. Exhaustive finite-chain reduction

Suppose G is a vertex-minimal counterexample to the root. C15L-T excludes an original degree-two vertex on a triangle. Therefore an induced diamond has external neighbors at both of its terminals. C17D excludes distinct nonadjacent external neighbors and common external neighbors. The remaining possibility is a distinct adjacent pair, creating S_1.

Starting from S_t, every earlier vertex has degree three inside the fragment. An additional terminal neighbor cannot be an earlier vertex, the terminal itself, or the other terminal (whose edge is already present). Thus every exposed external vertex is new. When both exposed neighbors are distinct and adjacent, absorb them as the next rung S_(t+1). Each absorption adds two vertices, so finiteness forces termination.

There are exactly four termination types:

(1) Neither terminal has an external neighbor. Connectedness gives G=S_t, colored in Section 2.

(2) Exactly one terminal has an external neighbor. The sole exit is a bridge. If the other shore has at least two vertices, it is a non-pendant bridge, excluded by C14B. Otherwise G is S_t with a single leaf, colored in Section 4.

(3) Both terminals have the same external neighbor z. This enlarged piece has at most one exit at z. A nontrivial other shore is again excluded by C14B. The remaining connected graphs are precisely S_t+z or S_t+z plus a leaf; both were colored in Section 4.

(4) Both external neighbors z,w exist, are distinct, and are not adjacent. Delete all of S_t and add zw. The resulting graph is simple and subcubic, and has fewer vertices. Minimality gives a star six-coloring; Section 3 lifts it to G, contradiction.

These types exhaust every terminal possibility. No loop or parallel edge is added tacitly, and no cyclic return along the exposed chain is missed. Hence G has no induced diamond.

If two triangles share an edge and their other vertices are adjacent, the component is K4, whose six differently colored edges give a star coloring. In a subcubic graph two triangles sharing a vertex must share an edge: their two incident-edge sets are two-element subsets of a set of size at most three and must intersect. The induced diamond and K4 alternatives now both are excluded. Thus triangles in a minimum-order root counterexample are pairwise vertex-disjoint.

## 6. Actual finite checks and limitations

The self-contained companion uses standard-library CPython 3.13.5, one thread, a 15-second wall alarm, CPU limits 15/16 seconds and a 512 MiB address-space cap. The checker tests 96 concrete end colorings for t=1,...,24, all 1536 ordered outside palette cases for one four-rung fixture, 54 further periodic boundary smoke cases, and four rejected mutations. It freezes the digest of the 256-row normalized positive palette table, the complete generating recipe in the source, and the full head-component table. The result summary does not store the normalized recipe rows; replay regenerates them deterministically. These are generator-side checks, not a trusted receipt, repository-script execution, or an exhaustive search over all graphs. Finite prefix success alone would not imply the all-length claim; Section 2's rung classification supplies that missing argument.

Reproduce with the companion in a disposable directory; its result file is written beside it. Integer colors and finite combinatorial tests only are used. The proof uses finite-graph-basic and finite-combinatorics. Minimality consequences depend on C14B, C15L-T and C17D, all still candidate arguments. No external theorem or novelty claim is used here.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open; no Result, EvidenceLink or DAG record is changed.
Next action: attack the now natural contraction of an isolated triangle. A smaller graph's arbitrary coloring need not lift through triangle expansion, so test its three-port boundary before assuming triangle-free reduction. Maintain the distinction between these fixed-exterior failures and the root existential question.
