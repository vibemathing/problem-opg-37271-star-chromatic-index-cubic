# C18M: a strong three-colored perfect matching extends through five-cycles

Verdict: `candidate_only`. Primary owner: `math-derivation`.
Attempt `attempt:web-20260906-opg37271-a01`; Route `route:leaf-extension-six-colors-v1`.
Graph `graph:opg37271-initial-v1`; admitted target `obligation:opg37271-leaf-extension`.
Root `obligation:opg37271-root` remains open.
Base: `7cb2aa0c860a95a5693300d4153f9d794ac90a40`.

This is an existence/partial-precoloring extension candidate, not a repair of an arbitrary full old coloring. It does not replace or edit the admitted DAG. Only finite-graph-basic and finite-combinatorics are used.

## 1. Exact theorem candidate

Let G be any finite simple subcubic graph with a specified perfect matching M. Give M colors in A={1,2,3}, so that any two distinct matching edges joined by a G edge have different colors. Equivalently, this is a proper three-vertex-coloring of the matching conflict graph J_M defined in C17K. Then this specified coloring of M extends to a star edge coloring of G using {1,...,6}.

The complement F=G-M may have five-cycles. G need not be connected, cubic, planar, or triangle-free. The condition on M is stronger than proper edge coloring of M. No existence of such an M or its three-coloring is asserted for a general root instance.

Write lambda(v) for the color of the unique matching edge at v. Each F edge uv has lambda(u) different from lambda(v): its endpoints cannot belong to the same matching edge in a simple graph. Thus lambda is a proper three-vertex-coloring on each component of F. The components of F are isolated vertices, paths and cycles.

## 2. Complement paths and non-five-cycles

Use B={4,5,6} on a path by repeating 4,5,6. For a cycle of length n other than five, write n=3r+4s with r>=0 and s in {0,1,2}: use s=0,1,2 for n congruent to 0,1,2 modulo three. The only excluded n>=3 is five.

Color the cycle by concatenating r copies of the block 456 and s copies of 4546. Properness holds both inside the blocks and across their boundaries. Every four consecutive cyclic edges use at least three colors: this can be checked on the interiors and the four ordered pairs of block types, since each block has length at least three. On a triangle no four-edge simple path or four-cycle exists. On a four-cycle the block 4546 uses three colors. Thus these are star colorings. An isolated F vertex needs no color.

## 3. The five-cycle patch

On a five-cycle C=v0 v1 v2 v3 v4 v0, every color of a proper three-vertex-coloring occurs at most twice. Hence the multiplicities are 2,2,1. Rotate the notation so lambda(v0)=a is the unique color occurring once. In particular none of lambda(v1),...,lambda(v4) equals a.

Color the opposite edge s=v2v3 with a. The remaining four edges, in path order from v3 to v2 through v4,v0,v1, receive 4,5,6,4. Let S consist of the one selected edge in each five-cycle.

The key property is stronger than properness: s has no matching edge of color a incident with either endpoint, or separated from s by a single B-colored edge. Indeed those possible matching edges occur at v1,v2,v3,v4, whose lambda colors all differ from a. Call this property the same-color matching separation condition. It refers to distance in the actual graph, not to an abstract branch profile.

S is a matching, since F components are vertex-disjoint and only one edge is chosen per five-cycle. No two S edges can be separated by a single B edge, since B edges stay inside F components.

## 4. Complete global star audit

The resulting coloring is proper. A matching edge and a B edge have disjoint palettes; an S edge differs from the matching colors at both endpoints by Section 3. Properness within F follows from Sections 2 and 3.

Consider a purported bichromatic simple path or cycle of four edges. Properness forces alternating colors. Partition the possibilities by the two palettes.

Both colors in B: all four edges lie in F-S, whose paths and cycles were star colored in Sections 2 and 3.

Both colors in A: all four edges lie in M union S, the union of two matchings, so their membership alternates. Among the four edges there is a consecutive M-S-M triple. Its two M edges have different colors because the intervening S edge is an F edge and the precoloring is proper on J_M. Its S color differs from both endpoint matching colors. This triple already has three colors, a contradiction.

One color a in A and one b in B: the two a edges are separated by a B edge somewhere on the four-edge path or cycle. If both are in M, the J_M condition makes their colors different. If exactly one is in S, the same-color matching separation condition excludes this. If both are in S, the single B edge would connect two selected edges in the same F component, impossible. These three cases exhaust the locations of the two a edges.

This excludes all forbidden paths and cycles. It covers matching chords inside an F cycle and matching edges joining different patched five-cycles; the argument does not assume the cycles are induced or far apart.

The proof is componentwise and constructive. Once M and its coloring are supplied, the described work is linear in graph size. With a fixed ordering, traversal and the rare color select a deterministic output. No search for a good full old coloring is hidden in the construction.

## 5. Finite realized certificate and replay

The companion check implements the construction, not a coloring search. For two disjoint labeled five-cycles joined by an arbitrary perfect matching, there are 120 matching permutations and 243 prospective matching color words per permutation. The first-cycle proper words are exactly 30. After checking BOTH cycle conditions there are 1,200 eligible graph/precolor pairs on 110 distinct labeled graphs. The ten remaining matching permutations have no eligible three-color precoloring; their exclusion is a failed premise, not a root obstruction.

The certificate contains all 1,200 complete fifteen-edge colorings, in a bounded zlib-compressed JSON table with explicit decoding. For each row the first five edges form the specified matching and retain its colors. The replay does not import the construction or search for colors: it enumerates all 120*243 prospective inputs to determine eligibility, checks exact table coverage, reconstructs the actual graph, and tests all simple four-edge paths and four-cycles from adjacency lists.

Observed solver-free replay: 256,800 oriented simple four-edge paths and 31,200 oriented four-cycles, with every supplied coloring passing. Removing a row, duplicating a row, and inserting color 7 are rejected. The constructor additionally checks 98 prism fixtures with cycle lengths 3 through 100 and 30 path fixtures. The finite certificate supports this proof; it is not an exhaustive test of all subcubic graphs or of arbitrary realizable matching-conflict graphs.

Observed local runtime: CPython 3.13.5; standard library; one thread. Each script enforces a 35-second wall alarm, 35/36-second CPU limits, and 512 MiB address-space limit. Certificate input, decompressed table and generated certificate are bounded by 262,144 bytes. These are generator-domain diagnostics, not an admitted adapter, repository command, kernel run, or trusted receipt. The profile's command_execution declaration has not been changed.

Reproduction in a disposable copy: run `opg37271-c18-matching3-check.py`, then `opg37271-c18-matching3-replay.py`. Each script writes its named output beside itself. The replay alone only needs its source and the frozen certificate. Freeze input/source hashes before any external verification and separately audit the universal proof and graph encoding.

## 6. Prior art, limits and checkpoint

Casselgren, Granholm and Raspaud, arXiv:1912.02467v2, Proposition 3.2 uses contraction of a perfect matching and a disjoint three-plus-three coloring under planar girth-seven assumptions. Lemma 2.9 gives three-star-list-colorability for cycles other than C5. The explicit five-cycle patch here is a separate argument; no assertion is made that the cited proposition contains it or that this candidate is novel. See the bounded source note.

Consequently any hypothetical root counterexample with a perfect matching must have J_M not three-colorable for EVERY such matching, subject to verification of this candidate. C17K separately covers the connected cubic K5-conflict case. Neither fact makes the remaining four-color conflict case automatic, nor supplies a perfect matching when none exists. In particular, splitting the six colors into four for M and two for F fails on a four-cycle complement; sharing colors requires a new invariant.

Best verified result: none. Best verified candidate: none. Both admitted obligations remain open. State: nonterminal.
Next exact action: derive a same-color-separated special-edge criterion for four matching colors plus two free colors; determine which cyclic label words satisfy it, and test its failure on actual realizable inputs rather than treating formal words as root counterexamples.
