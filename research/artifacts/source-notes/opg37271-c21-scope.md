# C21 source and statement-faithfulness note

Verdict: candidate_only. Input revision d4853563085f4310d1d99cb332de62f44c36fbda.

Canonical root: every finite simple subcubic graph has a star edge coloring with at most six colors. Four-edge paths mean five distinct vertices and are not required to be induced. The exact root ProblemContract and the existing C19/C20 graph witnesses were read; old CI or JSON success fields are not mathematical premises.

C20 proof hash: 90037f690f2cfe82f607412aced983020eba36cc9a0efc5e2bda84c5781d12cf.
C20 admission request hash: b0cf28cdb4260a81bca46ee2add3124b0014bf1968d5326c631f13c935d31c28.
Original C19 graph certificate hash: 9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3.

C21 does not preserve arbitrary old colors. PRE chooses D/U on all cubic inputs but does not ensure consistency. SQ changes the outer matching coloring and proves a five-color bound only when a C4-factor is supplied. ODD first preserves a specified strong-four matching coloring for a {C3,C5}-factor, then removes that premise using Brooks and explicitly covered K5 exceptions. Neither special factor is asserted to exist on every cubic graph. A mixed {3,4,5} factor is not covered by simply pasting the two proofs.

The necessary-sufficient C19 formulation is universal only after its frame premises. Unrestricted frame existence is equivalent to root; restricting U to paths of at most two edges, or to a monochromatic matching of a vertex bit cut, may be stronger. The K3,3 lower bound excludes every three-plus-two palette frame and every specified cut frame, not unrestricted four-plus-two frames. Its explicit six-color witness prevents confusing these scopes.

External theorem used: Brooks' vertex coloring theorem, as stated by Bradley Baetz and David R. Wood, arXiv:1401.8023v1 (2014), abstract at https://arxiv.org/abs/1401.8023v1 . For a connected simple conflict graph of maximum degree four, the only obstruction to at most four colors is K5; smaller cliques and odd cycles need at most four. This exact case analysis is necessary. The candidate does not infer four-colorability merely from maximum degree. The source abstract and version metadata were accessed; no claim of having replayed a formal Brooks proof is made. This is an explicit external proof dependency for ODD's unconditional version only. PRE and SQ do not use it.

Related edge-partition and list-star-coloring literature was searched. No novelty assertion is made. Publisher full-text access failures were not treated as theorem evidence; no inaccessible proof is imported. The all-triangle special case overlaps standard claw-free subcubic coloring settings, but this note does not attribute our square or pentagon recipes to an unexamined source.

Runtime fidelity: a preliminary 384 MiB address-space cap was below this instrumented Python process's observed virtual-size baseline (about 404 MiB); that run failed with MemoryError. The final recorded child cap is 768 MiB, with wall/CPU/output limits. An earlier twelve-vertex isomorphism-catalogue exploration hit resource limits and is NOT reported as complete. The committed finite stress test has a different, explicit factor/pairing domain and does not require NetworkX or graph-isomorphism software.

Gate fidelity: current .github/workflows contains only web-candidate-gate.yml (blob c232051b6e2332ac5e4a3a7ddde7ec542ca4d9d6). It performs transport validation, not mathematical verification. research/verifiers.json (blob b93b32955eb94c3b4ee82f045f7bbb85fd900f05) has no Lean toolchain allowlist. The existing C20 request remains pending. The current Web role is candidate generator/transport writer. No new record IDs or receipts are invented, and historical missing byte streams are unused.
