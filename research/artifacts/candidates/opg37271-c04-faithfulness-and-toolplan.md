# C04: finite certificate design and statement-faithfulness map

Verdict: `candidate_only`. Candidate ID: `candidate:opg37271-c04-faithfulness`.
Primary owner: `math-derivation`; supporting formalization and ToolPlan design only.
Attempt: `attempt:web-20260906-opg37271-a01`. Route: `route:leaf-extension-six-colors-v1`.
Graph: `graph:opg37271-initial-v1`. Target: `obligation:opg37271-leaf-extension`.
Base: `4d57f83eb62528991f56ed29c219e5ed5507726e`.

## 1. Frozen input and deliverable

The local target quantifies over every finite simple subcubic graph, every leaf v adjacent to u, and every star edge coloring of G-v, asking for an extension with all old colors unchanged. C01 supplies one finite witness attacking that quantifier.

This package gives an UNEXECUTED Lean source draft, not a successful compilation or a verifier receipt:
`research/artifacts/candidates/opg37271-c04-finite-leaf-certificate.lean`, SHA-256 `6a7078906a68934931b8449d51a16649886c4beb7ff653203907c94ceea67ef9`.

The source is a finite certificate of the displayed graph, not a formalization of a universal graph theorem. It neither encodes nor proves a negative answer to the root's existential six-coloring question. A separate semantic bridge is required before using a checked finite certificate against the admitted local statement.

## 2. Definition map

| mathematical object | encoding |
|---|---|
| v,u,x,y,a,b,c,d | Fin 8 values 0,1,2,3,4,5,6,7 |
| absent unordered edge | symmetric value 0 |
| an edge with a palette color | symmetric value in 1,...,6 |
| H=G-v | hColour on the same eight labels with label 0 isolated |
| a choice for uv | t:Fin 6, encoded as t.val+1 |
| G with this edge color | gColour t |
| maximum degree at most three | Subcubic excludes four distinct neighbors |
| properness | distinct incident edges with nonzero codes have distinct colors |
| bichromatic four-edge path | five distinct vertices, four nonzero edges, alternating equality |
| bichromatic four-cycle | four distinct vertices, four nonzero edges including the closing edge, alternating equality |

The code zero is not a seventh available edge color: adjacency is defined by being nonzero, and SimplePalette bounds codes by six. Edges are undirected because symmetry is checked, and diagonal zero excludes loops. Fin 8 and the exclusion of four distinct neighbors exactly model finiteness and the required degree bound for this graph.

The isolated label 0 in hColour may be deleted without affecting properness or any forbidden path/cycle, because all their edges must be nonzero. Conversely, a violation in the seven-vertex restriction is a violation on the eight labels. This is the explicit bridge from the implementation convenience to G-v.

Paths are simple, not necessarily induced. The last three vertices of the C01 witness form a triangle; encoding an induced-path requirement would change the target. Both path and cycle clauses are separately present.

## 3. Named checks requested

- h_simple_palette, h_star, h_isolated_leaf_vertex.
- g_simple_palette, g_subcubic, g_leaf, g_same_adjacency.
- g_agrees_after_vertex_deletion, no_fixed_extension.
- repaired_star, repaired_same_graph, repaired_palette.

The g_same_adjacency theorem asks that all six choices describe the same underlying graph, avoiding a hidden change of graph with the color choice. The deletion-agreement theorem asks that every old edge retains its color. Since every available color is t.val+1 for some t:Fin 6, no_fixed_extension covers all six permitted choices, not just a sample.

The repaired coloring is a positive control: it changes xa from 3 to 5 and uv to 3 on that same graph. This makes it especially clear that the finite obstruction is not a graph needing more than six colors.

The Lean draft uses ordinary `decide` proofs and requests `#print axioms` for the main declarations. It does not use native code evaluation to assert a proof, introduce an axiom, or leave a placeholder proof. This is a source-design observation, not an axiom-audit receipt. Elaboration, reduction cost, imports, and generated proof dependencies remain unchecked.

## 4. ToolPlan, not execution

Registered family: T18, Lean 4/Mathlib; proposed principals: lean-kernel, lean-axiom-auditor, lean-faithfulness-reviewer. These principal names are requests from research/verifiers.json, not identities of actions performed here.

Declared target: leanprover/lean4:v4.33.0, from fixtures/lean-proof/lean-toolchain at the base. Import is Std; no Mathlib import or external package is required by the source. The existing lean-mathlib-local source profile is quarantined, including its high-assurance route. Omitting Mathlib is not permission to bypass that quarantine.

Execution status: not_executed. The current Web profile does not authorize mathematical command execution. No version probe, Lean invocation, exit code, stdout, or receipt has been generated.

Before any later execution, an authorized runtime must confirm its toolchain allowlist, exact version and Std identity, permissions, and quarantine status. If these fail, record an infrastructure block, not a mathematical conclusion. A candidate sandbox replay and an admissible verifier replay are distinct operations.

Proposed command after those gates:
`lean research/artifacts/candidates/opg37271-c04-finite-leaf-certificate.lean`

Budget: one process, one CPU thread, 1024 MiB memory, 120 seconds wall time, 65536 bytes combined output, one attempt. The external runner must enforce the limits; the file additionally requests maxHeartbeats=5000000 and maxRecDepth=100000. If reduction exceeds these limits, split the finite checks by fixed starting vertex or color without weakening their statements. Do not substitute a timeout for a counterexample.

Required recorded outputs after a real run: exact argv and runner version, toolchain identity, all input hashes, exit status, output digest, complete declared theorem names, axiom/escape audit, and separate statement-faithfulness assessment. Any output or error belongs to a future receipt, not this package.

## 5. Source comparison

Official Lean reference, Tactic Reference, accessed 2026-09-06:
https://lean-lang.org/doc/reference/latest/Tactic-Proofs/Tactic-Reference/
This documents `decide` as a tactic based on decidability. Its availability is not evidence that this source compiles.

Official Lean 4.22.0 release notes, accessed 2026-09-06:
https://lean-lang.org/doc/reference/latest/releases/v4.22.0/
These document the finite existential Decidable instance used by the design.

Official Lean 4.33.0 release notes, accessed 2026-09-06:
https://lean-lang.org/doc/reference/latest/releases/v4.33.0/
The version is also named by the repository fixture; it is not claimed to be the current latest release or locally installed.

Repository method and controls: .codex/skills/math-formalization/SKILL.md, .codex/skills/math-toolchain/SKILL.md, governance/control-plane/math-knowledge-source.v1.json, governance/control-plane/math-knowledge-operators.v1.json, governance/control-plane/math-tool-maturity.v1.json, research/verifiers.json. Only the relevant entries were consumed; no executable permission is inferred from a surveyed or quarantined entry.

## 6. Remaining obligations and checkpoint

Best verified result: none. Best verified candidate: none.
New available candidate: the finite Lean source plus this explicit semantic bridge.
Open admitted obligations: `obligation:opg37271-leaf-extension`, `obligation:opg37271-root`.
Remaining work: actual bounded replay by a permitted runtime, axiom/escape audit, and semantic verification of the bridge. Even successful transport checks do not perform these steps.
Next derivation: exact validation radius for a prescribed simultaneous recoloring, including paths that cross its boundary.
State: nonterminal; verdict: candidate_only.
