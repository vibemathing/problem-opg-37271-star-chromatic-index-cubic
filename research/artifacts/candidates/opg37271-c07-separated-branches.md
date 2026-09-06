# C07: separated-branch recoloring and the actual critical-graph consequence

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c07-separated-branches`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base: `0e8d861e6aa71b08cfde899949a901a551ab32fb`.

Finite simple undirected graphs and the contract's proper star edge-coloring definition are used throughout. This is a paper derivation candidate; no graph search, solver, or kernel was executed.

## 1. Exact two-branch boundary test

Let J_X and J_Y be star-colored graphs whose vertex intersection is exactly {u}. Suppose u has precisely one neighbor x in J_X and one neighbor y in J_Y. Write c(ux)=alpha and c(uy)=beta, with alpha different from beta. Let
S_X={c(xa): xa is an edge of J_X, a different from u},
T_X={p: u-x-a-b is a simple path in J_X colored alpha,p,alpha}.
Define S_Y and T_Y similarly, with y and beta.

Claim C07-B. The union coloring on J_X union J_Y is star if and only if
beta is not in T_X, alpha is not in T_Y, and not both beta in S_X and alpha in S_Y.

Proof candidate. Properness can fail across the pieces only at u, and alpha differs from beta. A simple cycle cannot use both pieces: doing so would visit their only common vertex twice. Any new forbidden four-edge path must cross u and have a positive number of edges in each piece. The three possibilities for those edge counts are (3,1), (1,3), (2,2). The first is alternating exactly when beta belongs to T_X, the second exactly when alpha belongs to T_Y, and the third exactly when beta belongs to S_X and alpha belongs to S_Y. The paths formed in each case are simple because the pieces are otherwise vertex-disjoint. This proves both necessity and sufficiency.

In particular, beta absent from S_X and alpha absent from S_Y are sufficient, since T_X is a subset of S_X and T_Y is a subset of S_Y. The test covers crossing constraints, not just properness at u.

## 2. A corrected extension lemma with an explicit separator hypothesis

Let v be a leaf of subcubic G, with neighbor u, and let c be any star coloring of H=G-v using C={1,...,6}. Suppose either d_H(u)<=1, or d_H(u)=2 and its two neighbors lie in different connected components of H-u.

Claim C07-S. The coloring can be extended after either no old changes or a single transposition of two palette labels on all internal edges of ONE component of H-u. The edges incident with u are left unchanged.

Proof candidate. If the C01 forbidden set is not all of C, extend directly. The remaining saturated case forces
ux=1, uy=2, xa=3, xb=4, yc=5, yd=6,
with the seven named vertices distinct. Let X and Y be the different components of H-u containing x and y. All other components of H, if present, are untouched.

On every edge internal to Y, interchange colors 3 and 5. Leave all other edges, including ux and uy, fixed. The piece induced by Y together with u has undergone a uniform palette permutation: uy has color 2, which the permutation fixes. It therefore remains star. The X piece is unchanged.

After the swap, S_X={3,4} and S_Y={3,6}. Thus 2 is absent from S_X and 1 absent from S_Y; Claim C07-B proves that their union is star. No crossing cycle has been omitted. The four spokes now use only {3,4,6}, so C01's exact formula gives
F_new(u) subset of {1,2,3,4,6}.
Color 5 can consequently be assigned to uv. This proves the lemma.

When d_H(u)<=1, C01 gives at most three forbidden colors, so the zero-change case always applies.

The operation is on a whole separated component, not an arbitrary two-colored component and not a global permutation of H. It is also a simultaneous final recoloring; no claim is made that changing its edges one at a time gives valid intermediate colorings.

## 3. Quantitative cost, without a universal constant assertion

In the saturated normalization, choose any p in {3,4} and q in {5,6}. Swapping p and q throughout Y is valid by the same boundary argument and frees q for uv. Swapping them throughout X instead frees p.

For Z equal to X or Y, let m_Z(t) count internal edges with old color t and put N_Z=m_Z(3)+m_Z(4)+m_Z(5)+m_Z(6). The number of changed old edges in the corresponding transposition is exactly m_Z(p)+m_Z(q).

Claim C07-C. A repair exists with at most
min over Z in {X,Y}, p in {3,4}, q in {5,6} of (m_Z(p)+m_Z(q))
old changes. This minimum is at most min(floor(N_X/2),floor(N_Y/2)).

For a fixed Z, sum the four possible costs over the two choices of p and q. Each of the four color counts appears twice, so the sum is 2*N_Z and the average is N_Z/2. Some integer cost is no larger than its floor. Choosing either side proves the bound.

This is a graph-dependent upper bound, not a claim that every instance permits one or two old-edge changes. C02 and C05 remain compatible: their one-edge obstruction trees have separated branches, but recoloring a whole branch may change more than one edge.

## 4. Consequence for a hypothetical vertex-minimal root counterexample

Suppose G is a vertex-minimal finite simple subcubic graph without a star six-edge-coloring. The component lemma in C06 makes G connected. For any leaf v, minimality supplies a star six-coloring of H=G-v.

If d_G(u)<=2, C01 immediately extends it. Hence d_G(u)=3. If the two other neighbors x,y of u were separated in H-u, Claim C07-S would give a full coloring, again a contradiction. Thus x and y are connected in H-u, and adjoining ux and uy to a simple x-y path shows that u lies on a cycle.

For the same coloring, nonextendibility forces C01's saturation. Consequently x,y both have degree three, are not adjacent, and have no common neighbor other than u. Every cycle through u therefore has length at least five.

Claim C07-M. Every leaf in such a hypothetical minimal counterexample is adjacent to a degree-three vertex lying on a cycle of length at least five; its other two neighbors have degree three.

This does not assert minimum degree at least two. It rules out only leaves whose neighbors are outside all cycles, together with the additional local degree and short-cycle configurations already forced by saturation. The remaining cyclic case is an actual unresolved gap.

## 5. Audit, attribution, and checkpoint

Dependencies: C01's exact forbidden set and saturation, C06's component lemma and palette distinction. The prior-art comparison with Lei-Shi-Song Lemma 3.1 is recorded in C06's source note; no novelty claim is made for critical-graph structure. The new derivation here explicitly audits the separated-piece operation.

Adversarial cases addressed: disconnected H; degree-zero/one u; coinciding colors only after a bijective permutation; paths crossing u with each of the three length splits; cycles crossing a cut vertex; old roots remaining fixed; simultaneous versus sequential changes; and edit cost versus number of transpositions.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open.
Next action: derive a finite boundary signature and exact minimum-edit recurrence for trees, and investigate which additional cyclic boundary data is needed when X=Y.
State: nonterminal; verdict: candidate_only.
