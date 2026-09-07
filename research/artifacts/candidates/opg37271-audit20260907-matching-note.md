# Recovered matching-strategy candidate

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`.
Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`.
Target: `obligation:opg37271-leaf-extension`; root remains open.
Provenance: Issue #6 comment 5560144235, created 2026-09-06T15:12:09Z.
Source locator: https://github.com/vibemathing/problem-opg-37271-star-chromatic-index-cubic/issues/6#issuecomment-5560144235

This is transport of an existing, previously Issue-only proof proposal. The following argument and examples were already recorded in that comment. They have not been newly derived or computationally replayed in the transport audit. The requested standalone checker was a future action in the source, not an existing executable or receipt; none is invented here. C19P subsequently covers the general disjoint-palette phase mechanism; the explicit K3,3 obstruction and the two supplied matrices are retained here with their original scope.

## Monochromatic perfect-matching obstruction

Take G=K_{3,3}, with bipartition {u1,u2,u3}, {v1,v2,v3}. For ANY perfect matching M, relabel so M={ui vi}. Suppose all M edges have color alpha in a star edge coloring. Every other edge avoids alpha by properness. Moreover the six edges of F=G-M must have pairwise different colors.

To prove the latter, adjacent F edges already differ. For disjoint e=ui vj and f=uk vl, with i!=j, k!=l, i!=k, j!=l, the three index values imply j=k or l=i. Reverse the pair if needed to assume j=k. If e and f had the same color beta, the sequence vi,ui,vj,uj,vl would be an alternating alpha,beta,alpha,beta four-edge path when i!=l, or the corresponding four-cycle when i=l. Both are forbidden. Therefore a monochromatic perfect matching forces at least seven total colors, regardless of which of the six perfect matchings was chosen.

This is NOT a root counterexample. A star six-coloring of K_{3,3} is the row-by-column matrix

    4 3 2
    3 1 5
    2 6 1.

Colors 4,5,6 are singletons. The three double color classes have different missing rows and different missing columns. The union of any two covers all six vertices and has only two degree-two vertices, so it cannot contain a four-edge path or four-cycle. Properness is immediate from the matrix.

The same observation gives a short lower bound of six for this graph. In a coloring with at most five colors, no color class can have size three, since such a class is a monochromatic perfect matching. There can be at most three double classes: two double classes with the same missing row occupy only two rows and their union is a four-edge path or four-cycle. Thus five colors cover at most 3*2+2=8 of the nine edges. The matrix attains six. No novelty claim or external verifier claim is made.

Failed-direction proposal: universal root construction using one color on a perfect matching and at most five disjoint colors on its complement. Its obstruction is to ALL perfect matchings of K_{3,3}, not merely to a badly selected matching or an unrealizable boundary profile. C17's exact fixed-M criterion itself remains valid; the universal existence strengthening is what fails.

## Two matching colors and four complement colors

For a graph with a specified perfect matching M, let F=G-M have a star coloring phi using {1,2,3,4}. Define a graph B_phi on the matching edges. For each xy in F, join the matching edges m_x and m_y when phi(xy) also appears on an F edge at the mate of x or at the mate of y. Then coloring M from the disjoint palette {5,6} completes a star coloring exactly when that assignment is a proper vertex coloring of B_phi; such an assignment exists exactly when B_phi is bipartite.

Indeed a new bichromatic four-edge obstruction must alternate two matching edges of the same reserved color with two equally colored F edges. Its condition is exactly an edge of B_phi; the four-cycle identification is included. Zero-matching-edge obstructions are excluded by phi being star, and one matching edge cannot supply two occurrences of a reserved color. This is an exact criterion for this two-plus-four palette split, not an equivalence with the unrestricted root.

For K_{3,3}, take F in cyclic order u1-v2-u3-v1-u2-v3-u1 with colors 1,2,3,1,2,4, and the diagonal matching colors 5,6,5. B_phi is a path, and the resulting star six-coloring is

    5 1 4
    1 6 2
    3 2 5.

## Limits retained from the source

Audit and external verification of the proposal remain pending. Do not assume every cubic graph has a perfect matching. Do not identify the two-plus-four palette split, a failing frame, or a fixed-coloring repair obstruction with failure of the unrestricted root. The fixed-exterior triangle-contraction attack remains a separate unclosed direction. No new admitted Route or Obligation, execution receipt, EvidenceLink, Result or Solution is supplied.
