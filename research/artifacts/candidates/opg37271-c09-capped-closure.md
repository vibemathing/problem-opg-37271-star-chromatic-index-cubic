# C09: finite capped-cost closure for the universal k-edit tree question

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c09-capped-closure`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `79d16a8a904f256fd4eac988ef8ceeb5913c3756`.

This is a finite-state reduction and certificate specification, not a closure computation. All claims remain candidates. No mathematical program, solver, or kernel was executed.

## 1. Freeze the weakened question

For a fixed integer k>=0, Q_k asks: for every finite simple subcubic TREE G, leaf v with neighbor u, and star coloring c of H=G-v using C={1,...,6}, is there a star coloring of G differing from c on at most k old edges?

The final coloring, not a sequence of individually valid recolorings, defines the edit budget. The new edge uv is not charged. Q_0 is the tree restriction of the original target. Q_k for k>0 explicitly permits old changes and is not the admitted no-recoloring statement. No value of k is proved universally sufficient here.

## 2. Exact capped branch profiles

Use C08's 306 labeled pendant signatures S. A signature's arity j is its number of nonunit alternating-length coordinates, so |S_0|=6, |S_1|=60, |S_2|=240.

For a fully old-star-colored pendant TREE branch B, including its old colored stem, let sigma be the old signature and let D(s) be the exact minimum number of old edge changes needed to realize target signature s on the same tree. Define tau_k(d)=min(d,k+1), including tau_k(infinity)=k+1. The capped profile is
P(B)=(sigma, (tau_k(D(s)))_(s in S)).

If sigma has arity j, all states outside S_j have value k+1. The sigma coordinate is zero, and every other coordinate in S_j has a value in {1,...,k+1}: zero changes preserve the whole old coloring and hence its signature.

Claim C09-N. The total number of possible profiles is at most
N_k = 6*(k+1)^5 + 60*(k+1)^59 + 240*(k+1)^239.

This counts the choice of old signature and the remaining coordinates in its arity class. It is a finite upper bound, not the number of reachable profiles or a tractability estimate. For k=0 it reduces to 306.

Claim C09-T. Capping preserves every threshold comparison D<=k in the C08 recurrence. It commutes with finite minimum and with nonnegative addition followed by capping:
tau_k(min_i d_i)=min_i tau_k(d_i),
tau_k(sum_i d_i)=tau_k(sum_i tau_k(d_i)).
The identities also cover infinite/unattainable entries. Nonnegativity is essential; there are no negative rebates that could bring a value above k back below the threshold.

## 3. A finite grammar generating exactly the realizable profiles

Seed profiles are the six single-edge old-colored branches. For old color alpha, each all-unit target signature with stem a has cost tau_k([a differs from alpha]); other signatures have value k+1.

For a new internal branch node, choose one or two child profiles and an OLD stem color alpha. Check C08's transition conditions on alpha and the old child signatures. If they fail, do not generate an old branch. If they hold, they determine its old output signature sigma.

For every NEW stem color a and every tuple of target child signatures, apply the same C08 transition. For each accepted output state s take the capped minimum of
[a differs from alpha] + sum_i (child capped cost at its target signature).
Unattainable outputs receive k+1. This produces a unique parent profile determined by the input profiles and alpha. No unrecorded interior information is required, because C08 proved the full cost recurrence.

Let R_k be the least set containing the seed profiles and closed under these unary and binary transitions.

Claim C09-R. R_k is exactly the set of capped profiles of all finite old-star-colored subcubic pendant trees.

Soundness. A seed is a real colored edge. Given real child witnesses, take disjoint copies and attach them to a new stem. The old transition makes the old coloring star. C08's exact recurrence and Claim C09-T produce the stated cost vector. Thus every generated profile has a real finite witness.

Completeness. Every such tree branch is either a seed or decomposes into a stem and one or two smaller child branches. Induction on its number of edges and the same recurrence put its profile in R_k.

A closure procedure that inserts only new profiles terminates after at most N_k distinct insertions, although the transition work can be enormous. First-discovery backpointers can be acyclic: the children already existed before the newly inserted profile. When reconstructing a witness, repeated child profiles must be copied as disjoint trees, not identified into a cyclic graph.

## 4. The exact final-root test

At u in H there are j=0,1,2 child branches and no old parent edge. Choose a tuple of profiles from R_k. It is a valid old root configuration exactly when the old child stem colors are distinct and, for j=2, their two cross-color alternating-arm lengths sum to at most three. Inside the children the old colorings are already star.

For this valid tuple, try every new color a on uv and every tuple of target child signatures satisfying C08's transition conditions. The new stem uv has cost zero. Let M_k be the minimum capped sum of the child costs over these choices, with value k+1 when there is no choice within the threshold.

Claim C09-Q. Q_k holds if and only if M_k<=k for EVERY valid old root tuple over R_k.

For the forward direction, realize any tuple by disjoint child trees at u and apply Q_k. Its repair induces a choice counted by the root minimum. For the reverse direction, decompose any actual (H,c,u) into its child branches, use their reachable profiles, and reconstruct minimizing target witnesses. The cost and gluing arguments are exactly C08. The j=0 root case gives cost zero and includes a one-edge G.

This is a finite decision reduction for each fixed k, not a reported decision for k=2 or for unbounded k.

## 5. Positive and negative certificate requirements

A positive finite certificate may provide a transition-closed SUPERSET A of the reachable profiles. A checker must verify the profile format, inclusion of all seeds, closure under every valid old unary/binary transition and old stem color, and M_k<=k for every valid old root tuple over A. Then R_k is a subset of A by induction, so Claim C09-Q proves the tree statement. A superset may cause false alarms, but cannot make a checked positive certificate unsound.

A negative certificate must instead provide a failing root tuple of genuinely reachable profiles, with acyclic seed/transition backpointers. A checker must recompute the complete capped vectors at each derivation step, not merely inspect a proposed expensive recoloring. It then reconstructs an old-star-colored tree and verifies that its root minimum is k+1. A coloring using more than k changes by itself is NOT a lower-bound certificate.

An abstract profile satisfying the coordinate range constraints need not be realizable. A failed root test on such an unproved profile is therefore not a counterexample.

## 6. Paper regression and limitations

At k=0, C03's small tree has a left branch with old stem 1 and lengths ell_3=ell_4=3, and a right branch with old stem 2 and lengths ell_5=ell_6=3; all other lengths are one. Their old root gluing is valid. New colors 1,2 violate properness; colors 3,4 violate the left stem-arm test; colors 5,6 violate the right one. This is a direct paper check of the zero-edit obstruction, not a run of the closure algorithm.

C02 already supplies a one-edit obstruction candidate. Neither that fact nor the finite-state reduction decides Q_2. A certificate would still require a bounded admitted implementation, frozen inputs, actual runtime identity and output, and mathematical verification. The present channel supplies none of those execution claims.

The reduction is only for trees. It also quantifies over fixed old colorings and an edit budget; it is not a proof or disproof of the root's existential six-color statement for all subcubic graphs.

## 7. Checkpoint

Dependencies: C08's exact state and cost recurrence; C03 and C02 only as explicitly delimited regression candidates.
Best verified result: none. Best verified candidate: none. Both admitted obligations remain open.
New candidate result: a finite, realizability-aware closure criterion and separate positive/negative certificate obligations for each fixed k.
Next action: complete a direct classification and repair audit for the triangle-free zero-edit obstructions attaining both ten vertices and eleven edges, rather than claim that the large closure was executed.
State: nonterminal; verdict: candidate_only.
