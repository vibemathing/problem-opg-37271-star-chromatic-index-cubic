# C08: 306 exact pendant-boundary signatures and minimum-edit tree recurrence

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c08-tree-signatures`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `06e58e796b3412ce62583570d8df1be10d0157d4`.

These are finite-graph derivations and an algorithm specification, not executed calculations. No implementation, solver output, or kernel receipt is claimed.

## 1. A precise boundary object

A pendant branch B is a finite connected simple subcubic graph with distinguished boundary vertex p of degree one, neighbor r, and a proper star edge coloring using C={1,...,6}. Its stem color is a=c(pr). For each b different from a, let ell_b be the length of the maximal alternating {a,b}-path starting at p with first edge pr.

Properness makes the prescribed-color continuation unique. The path has length at most three because B is star, and at least one because pr exists. Furthermore ell_b>1 exactly when r has another incident edge of color b. There are at most two such colors.

The signature is s=(a,(ell_b)_(b different from a)).
Thus ell_b is in {1,2,3}, with at most two entries greater than one. The empty branch is a separate absent-input case, not a colored pendant signature.

Claim C08-S. Exactly
6*(1 + 5*2 + binomial(5,2)*2^2) = 306
signatures are realizable. With j=0,1,2 nonunit coordinates there are respectively 6,60,240 signatures.

For realizability, start with pr colored a. For every selected b, add r-s_b colored b; when ell_b=3, also add s_b-t_b colored a. All introduced vertices are distinct. This is a subcubic tree. Its {a,b} component through p has the desired length, and components involving two distinct selected colors have length two. Any other two-color component is shorter. Hence it is star. These witness trees have at most six vertices.

## 2. Exact compatibility and minimality under fixed labels

Consider star-colored pieces otherwise disjoint and glued only at p, so their union remains subcubic. Each piece contributes one or more uniquely colored arms at p. For a pair {a,b} whose edges lie on different sides, a new alternating path exists precisely when the two maximal arm lengths have sum at least four. Properness at p must also hold. No simple cycle crosses a one-vertex separator.

Consequently a pendant signature determines compatibility with every star-colored exterior glued only at p: the new stem color must differ from all exterior incident colors, and each relevant pair of arm lengths must sum to at most three.

Claim C08-M. Distinct members of the 306-state set are distinguishable by star-colored path exteriors. Therefore 306 is the exact number of fixed-label compatibility classes for these branches, not just an upper bound.

If two signatures have the same stem color a and differ at b, let their lengths be d<e. Use a path exterior starting at p with colors b,a,... of length 4-e. This length is either one or two. Its sum with e is four, while its sum with d is at most three. The two unions therefore differ in star validity.

Now let the stem colors be a and a', with a different from a'. If the a' branch has ell_a<=2, an exterior consisting of one a-colored edge is compatible with it and improper with the a branch. The symmetric argument applies when the a branch has ell_(a')<=2.

The remaining case has both cross-lengths equal to three. Each signature then has at most one other nonunit coordinate. Choose b outside {a,a'} and outside those at most two other coordinates. Such a color exists in the six-color palette. Both branches have ell_b=1. The exterior three-edge path colored b,a,b is incompatible with the a branch, since 1+3=4, but compatible with the a' branch, since its relevant exterior arm has length one. This separates the last case.

This is a boundary-information statement, not a lower bound on every conceivable algorithm. The six unlabeled length-pattern orbits cannot simply replace the 306 labeled states in an old-color edit-cost calculation.

## 3. Exact rooted-tree transition

For a tree, orient edges away from an external boundary p. The branch with stem p-r consists of that stem and j<=2 child branches rooted at r. A child signature is s_i=(b_i,ell^i). Choose a proposed new stem color a.

The combination is valid exactly when:
(A) a,b_1,...,b_j are pairwise distinct;
(B) ell^i_a<=2 for each child i;
(C) if j=2, ell^1_(b_2)+ell^2_(b_1)<=3.

Condition (B) checks an alternating child arm against the single stem edge. Condition (C) checks the two child arms against each other. All forbidden paths not contained in a child must pass through r and are covered by these pairs. There are no tree cycles.

For a valid combination, the outgoing signature has stem a and
ell_(b_i)=1+ell^i_a
for each child; all other coordinates are one. In particular, its number of nonunit coordinates is exactly j. This also proves the 6/60/240 per-arity state restriction used below.

## 4. Minimum number of changed old edges

Given a finite subcubic tree G with leaf v and neighbor u, root it at v. Let c be the old star coloring of H=G-v. Each old edge e has weight
w_e(t)=0 if t=c(e), and 1 otherwise.
For the new edge uv, set w_uv(t)=0 for every t.

Let D_(p,r)[s] be the minimum total weight among star colorings of the branch p-r with outgoing signature s. Unattainable states have value infinity. For every valid transition in Section 3, update its output state by
D_(p,r)[s] = min(D_(p,r)[s], w_pr(a) + sum_i D_(r,child_i)[s_i]).

The zero-child case initializes the six all-unit signatures with their stem weights. Empty minima are infinity. After processing toward v, the exact optimum number of old-edge changes is
min_s D_(v,u)[s].
The new leaf edge is not counted as an old change. Store a minimizing transition as a backpointer to recover an actual coloring.

Claim C08-D. This recurrence gives the exact optimum, not only an upper bound.

Induction proof candidate. Every star coloring restricts to child star colorings. Its stem and child signatures satisfy (A)-(C), and their cost sum counts each edge exactly once. Hence the recurrence's minimum is no larger than the true optimum. Conversely each accepted transition glues child witnesses into a star coloring by the boundary criterion and creates its stated outgoing signature with the stated summed cost. Backpointers construct a witness for every finite table entry. Hence no table value is smaller than the true optimum. The two inequalities prove equality at every branch and at the final root.

With S=306 states, at most 6*S^2 candidate combinations are needed per binary node before constant-size checks. This gives a direct O(|V(G)|*6*S^2) time and O(|V(G)|*S) storage bound for the specification, including backpointers. It is not a measured performance claim.

## 5. Scope, attacks, and reproduction

The boundary signature itself applies to any already-star-colored pendant piece. The recurrence requires an actual tree decomposition into child branches intersecting only at r. It must not be applied to a cyclic graph by discarding extra edges. In a forest, only the component containing v needs consideration; other components retain their old coloring at zero cost.

A single old signature does NOT determine recoloring cost. The entire table of minimum costs over target signatures is required. Thus the deeper distinction in C05 is preserved, not erased by a shallow signature.

The following are proposed regression obligations, not tests performed here: C03's twelve-vertex tree has optimum one; C02 and C05's bad trees have the displayed optimum two; the eight-vertex C01 graph is cyclic and must fail the tree-domain precondition. A separate checker must enumerate incident pairs and all simple four-edge paths in any returned coloring and recount changed old edges.

All labels are retained in the state. Palette symmetry may be used only with explicit transformations of both boundary labels and reference costs. A valid final recoloring does not require valid intermediate one-edge edits.

## 6. Checkpoint

Dependencies: C07's exact separator reasoning and the contract definitions; C02/C03/C05 only supply future regression examples. No external theorem or novelty assertion is needed.
Best verified result: none. Best verified candidate: none. Both admitted obligations remain open.
Next action: cap these exact edit-cost vectors at k+1 and derive a finite closure criterion for the universal k-edit tree question; do not report a closure run or a universal two-edit bound without execution and verification.
State: nonterminal; verdict: candidate_only.
