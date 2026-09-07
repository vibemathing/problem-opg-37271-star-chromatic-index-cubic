# C19-E source and encoding map

Verdict: `candidate_only`. Primary owner: `math-proof`.
Input revision: `cedbfc277c39317e0d2998733b2d7b45670bac63`.
Issue: #6. Current task: audit C19-E only. The older missing-material checkpoint is preserved and supplies no mathematical input.

## Fixed source locators

All paths below are in `vibemathing/problem-opg-37271-star-chromatic-index-cubic` at the input revision.

| Path under research/artifacts/candidates/ | Git blob | Role |
|---|---|---|
| opg37271-c19-phase.md | d42f7d4cc92c2cca84c916c1076d87305dce5059 | Exact target, Sections 1-3; later outer-frame claims are excluded |
| opg37271-c19-phase-certificate.json | 10dd8d8da144381686be83164f7dd14586f614f2 | Sole executable data input; exact bytes rehashed |
| opg37271-c19-phase-check.py | 6ce1d44c69b208c7f9e617a199ed7f51d0a750c2 | Source inspection only, not imported or executed |
| opg37271-c19-phase-replay.py | 7867b97a04e42bda6f96deee48f81a7c6dfd6fa4 | Source inspection only, not imported or executed |
| opg37271-c19-phase-replay-result.json | 717b558bf8b1634dc72c11d438f1423728c455ba | Historical output read, not trusted as a new run |
| opg37271-c18-matching3.md | 03a2186956fa6fdc931424c7b637e9b5752f3082 | Context only; its strong-three-matching premise is not assumed |
| opg37271-c17d-diamond-replacement.md | 757e4bf32ede2d09ecf2cd6e9bf4ea0a18ab06f7 | Context only; no diamond-reduction theorem is imported |
| opg37271-c17-k5-matching.md | 0602e4ebf25c2fa12e7bf46d1f11df6fc4d0e979 | Context for C18M's matching-conflict definition |
| opg37271-c14-root-reductions.md | b8c3584238dce8bbb7d2d6a569177d325f9a9de6 | C17D dependency read; not a premise of C19-E |
| opg37271-c15-low-degree-reductions.md | 94961ecda2356852c06d8b9a9268ebe66c1ed0c0 | C17D dependency read; not a premise of C19-E |

The input certificate SHA-256 is `9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3`. Its raw byte length is 2,703. A local SHA-1 over the Git blob header plus those bytes matches the fetched blob identity above. No new digest of an unread original file is asserted.

## Definition-to-code mapping

`n` denotes vertices 0 through n-1. Graph order zero is accepted. Each edge row gives two distinct integer endpoints; duplicate unordered pairs and degree above three are rejected. `partial_colors[e]=0` means edge e belongs to U, not that zero is a color. Positive partial entries belong to A. The partial coloring is checked on D itself, not on an arbitrary completion.

The new `premise` function uses U-edge endpoint unions to recover components from the graph, then demands each has two endpoints, at most three edges, maximum degree two and one fewer edge than vertices. Components are canonically ordered by minimum edge index; their least endpoint chooses orientation. Only U edges are used to find a component. D chords do not make a U path invalid.

`shapes` enumerates all distinct-vertex 5-tuples forming simple four-edge paths and 4-tuples forming four-cycles. It removes orientation duplicates but never requires a path to be induced. For a cycle it also removes rotation duplicates; these identifications preserve all four edges and color equalities. `equations` checks alternating membership and equal D colors, computes edge parity within its U component (not position in the tested shape), and deduplicates by (unordered variable pair, right side). The `mode` parameter is used only for deliberately defective implementations in mutation tests; main replays use `exact`.

`star_by_components` imports neither equation routine nor old C19 code. It checks incident palettes and the sizes of every two-color connected component directly. The proof document gives the elementary equivalence between this component criterion and the frozen path/cycle definition. This is algorithmic separation within one generator trust domain, not a stronger trust claim.

The source certificate's two complete equation lists are regenerated, compared as signed sets and checked witness by witness. Every phase is then compared with the direct coloring predicate. The old 6,144/55,296 tallies are ignored. The other 24 full colorings are checked, but their reported feasible/infeasible frame counts are not used. A certificate with only a contradictory subset can be mathematically sufficient; the equality-of-complete-sets requirement here is an intentional stronger check of these two particular source records, not an additional hypothesis in C19-E.

## Evidence and runtime boundary

Only the current main certificate bytes and explicit small mutation fixtures enter execution. The final run uses the new standard-library sources and real local timeout/memory/output bounds; its execution JSON records input/source/runner/output hashes and actual return code. The runner and checker do not execute repository scripts, access a network, or call a solver. The available local command tool was used under the direct replay request; the profile's repository-command flag was not altered or treated as a trusted runtime grant.

A first developmental run passed before tightening integer equation field validation and separating the machine field `finite_audit_pass` from package readiness. All published execution bindings refer to the rerun of the final source. No result is inferred from the earlier developmental run or from prior JSON success fields.

The mathematical dependency chain starts from the frozen definitions, not from C18M/C17D, missing historical certificates, matching existence, or a trusted Result. The current main still binds the original admitted leaf target and root; this package introduces local claim IDs only, not ledger records. All historical missing-material entries remain pending and are outside the atomic target.
