# C06: connected scope, fixed-color quantifiers, and source-faithfulness

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c06-scope`.
Primary owner: `math-derivation`.
Attempt: `attempt:web-20260906-opg37271-a01`; Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`; target: `obligation:opg37271-leaf-extension`.
Base revision: `4c6e557f708f7df83487567320df9ff72a840b9c`.

This is a statement-comparison and derivation candidate. It neither supplies a proof of the root nor changes either admitted obligation. No mathematical command, solver, or kernel was executed.

## 1. Exact predicates

Let C={1,2,3,4,5,6}. A coloring is star when it is proper and every simple four-edge path and four-cycle uses at least three colors. The paths need not be induced. All graphs here are finite, simple and undirected.

P(G) means there exists c:E(G)->C that is star.
L(G,v,c) means there exists t in C such that c together with uv=t is star on G, where v is a leaf with neighbor u and c is a star coloring of H=G-v.

The root is universal P(G) over subcubic G. The local target is universal L(G,v,c) over all admissible triples. In particular, the local target quantifies universally, not existentially, over c.

## 2. Claim C06-C: connected versus unrestricted scope

For components G_1,...,G_m of G, P(G) holds if and only if P(G_i) holds for every i.

Proof candidate. Restricting a star coloring preserves properness and excludes all forbidden paths and cycles in each component. Conversely choose a C-coloring of each component and take their union, using the same palette. Each incident edge pair and each connected path or cycle is contained in one component. Thus all star conditions are preserved. Isolated vertices require no edge colors; the empty graph is covered by the empty coloring.

Consequently a universal six-color theorem for all finite connected simple subcubic graphs would cover the exact root, not merely a connected special case. This equivalence is conditional on identical star-coloring definitions and a finite graph domain. It does not verify that any external proof establishes the connected theorem.

## 3. Claim C06-Q: existence does not force fixed-color extension

C01 gives a graph G for which P(G) has an explicit coloring but L(G,v,c) fails for its displayed old coloring. Its eight old edges are ux=1,uy=2,xa=3,xb=4,ab=1,yc=5,yd=6,cd=2. C01 checks every color on uv and gives the repair xa=5,uv=3.

Therefore the implication P(G) implies L(G,v,c), even with c star on G-v, is invalid. An external assertion of universal P cannot be substituted for a proof of universal L. Conversely, this local obstruction does not attack P(G).

## 4. Claim C06-P: global palette permutations cannot repair saturation

Let pi:C->C be a bijection. For every star-colored H and distinguished u, the exact C01 forbidden set satisfies F_(pi o c)(u)=pi(F_c(u)).

Proof candidate. An incident color is transformed by pi. For a three-edge old path, equality of its first and third colors holds after applying pi exactly when it held before, and its middle color is transformed by pi. Taking the union in C01's exact formula proves the identity.

Hence F_c(u)=C is invariant under a global relabeling. In particular, permuting all six labels of the C01 obstruction never repairs its unchanged-color extension problem. Recoloring an appropriate part of H is a different operation and needs a boundary argument.

## 5. External-source comparison and reuse gap

The accompanying source note records a 2025 conference abstract whose final sentence asserts the connected six-color bound. Only an abstract has been obtained for that claimed general theorem. Its brief definition does not explicitly state properness, and its graph domain does not explicitly state finiteness. A full proof and definition audit are therefore still needed before even a statement-faithfulness conclusion can be upgraded.

A same-author journal paper has a different title and lists particular graph families in its abstract; this is not evidence that it is the full proof of the conference claim.

Lei, Shi and Song's earlier Lemma 3.1(a)-(c) contains closely related leaf-neighborhood structure under the additional assumption that the whole graph is star k-critical. C01's local saturation argument must be compared with that prior art, not advertised as new. Their criticality premise concerns failure of every full coloring; C01 concerns one fixed old coloring. The source note gives the precise locator and renaming.

## 6. Checkpoint and verification request

Best verified result: none. Best verified candidate: none. Both existing obligations remain open.
New candidates: the componentwise scope equivalence, the explicit quantifier separation, and the palette-equivariance formula.
Source gap: no full proof of the 2025 general claim has been obtained; no conclusion about its correctness follows from that absence.
Next action: seek a boundary-safe partial recoloring when the two old neighbors of u lie in different components of H-u, rather than repeat global palette relabeling or the already-attacked one-edge hypothesis.
Requested review: definitions, quantifiers, component gluing, C01 witness faithfulness, and the prior-art comparison. No receipt or Result is supplied.
