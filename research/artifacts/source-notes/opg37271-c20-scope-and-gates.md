# C20 scope, source lock, and admission gap

Verdict: candidate_only. Primary owner: math-proof. Base: ddc49c1978a196490702150bb75264793a658457.
This is a targeted C19-E/core continuation, not a new whole-repository transport audit.

## Inputs and faithfulness

The current main tree was freshly read. The earlier uploaded C19-E package was used only as a byte carrier: its graph input, proof, checker, execution, certificate, result, runner, source note and packet were each matched to the corresponding fresh-main Git blob identity before reading. SHA-256 values were recomputed over those exact bytes. Old success/runtime fields are not mathematical inputs. The only executable mathematical input to the new C20 check is the original C19 graph certificate, SHA-256 9e64005037bc075a78439a3c8bc49d85cf7f8a539a2b3bcba8f8eeded88c4ad3, blob10dd8d8da144381686be83164f7dd14586f614f2.

The C19-E proof at this base has SHA-256 3bca32d52a6ee9b66072c3114749c289ac4d5b87111cc3cea29ac0a18765f752. Its checker has SHA-256 2d36043e59b6d319d365be7a82ddde0a28cc541907350a7860f8ec8e12bcb3d6. They were read for scope/comparison; neither is imported or called by C20. Four-edge-subset classification in C20 is newly written. All work still belongs to the generator trust domain.

C20 retains the actual simple-graph/star-coloring semantics of the canonical contract. Its main statement is the local C19-E balance equivalence, NOT the admitted arbitrary-fixed-coloring leaf statement. The exact proposed statement and its UTF-8 text SHA-256 are in opg37271-c20-statement.json. C20 proves its local claims from definitions, not from pending C18M/C17D reductions or missing historical files. No claim of literature novelty is made. Historical six missing-material classes remain missing and unused.

The minimum core theorem concerns number/inclusion of ROWS, not smallest graph order. The order-eight assertion only concerns the explicit strong-matching/distinct-label-four-cycle class. The outer induced-matching recoloring changes D colors; it must never be presented as a completion that retains the original D. The contact-parity sufficient condition, in contrast, does retain D. Neither condition is asserted for all outer frames.

## Fresh gate observations

- research/verifiers.json, blob b93b32955eb94c3b4ee82f045f7bbb85fd900f05, registers lean-kernel, lean-axiom-auditor and lean-faithfulness-reviewer. None has a toolchain_allowlist. The registered SMT lane is a fixed QF-LRA counterexample fixture, not a general graph/XOR-proof adapter.
- scripts/vibe_mathing/lean_obligation.py, blob c2a6284e89329de8ae17d1c05ab457ceb4ecc730, first requires admitted graph/candidate identity and candidate-statement/obligation digest equality; it also checks the exact toolchain fingerprint against each selected verifier allowlist. Passing a theorem about phases as proof of the old leaf obligation would violate statement-faithfulness.
- research/records/candidate-artifacts.jsonl is empty at this base. The admitted graph still contains just the leaf and root statements, not a C19-E/C20 node. This is a local-theorem admission gap, not the historical pre-admission blocker for the existing Attempt.
- The complete fresh tree contains only .github/workflows/web-candidate-gate.yml, blob c232051b6e2332ac5e4a3a7ddde7ec542ca4d9d6. It runs snapshot, packet and diff validators on PR events, not a mathematical verifier. No permitted trusted verifier workflow was available to trigger. A generic workflow-list endpoint was rejected by the connector; the conclusion here uses the complete file tree and actual workflow source, not that endpoint error.
- The repository fixture declares leanprover/lean4:v4.33.0; lakefile.toml and lake-manifest.json pin mathlib revision db584cd6d46c92f209a44c0f1c829460d327499d. These files were read in this repository only; no other repository was accessed. Declared configuration is not a runtime fingerprint. The local probe found no Lean/Lake executable. There was no kernel build, axiom print, semantic receipt or formal toolchain fingerprint.

## Executable request and boundaries

opg37271-c20-admission-request.json freezes the natural-language local statement, candidate hashes, verifier IDs, explicit budgets, and prerequisite sequence. Run its read-only candidate preflight from a repository checkout with:

    python3 research/artifacts/candidates/opg37271-c20-run.py --admission-preflight

The preflight never dispatches a workflow, runs the registered adapter, creates an EvidenceLink or edits records. It checks source hashes and current local ledgers and reports missing gates. When a ledger is unavailable it reports that rather than guessing its contents. This preflight is supplied for execution on the future complete checkout; no successful trusted execution is asserted here. Formal source, exact admitted target and registered adapter request remain null until genuinely supplied. Inserting invented identifiers or using the old leaf node would make a misleading request, not a more complete one.

The requested future gate order is: admit the exact local statement and DAG position; register the frozen candidate; produce faithful Lean source; admit an actual toolchain fingerprint; supply a permitted verifier execution entry; obtain kernel, axiom/escape, statement-identity and separate semantic-faithfulness receipts; then invoke the trusted obligation-closure gate. User authorization to initiate this process does not upgrade the Web principal's role.

The execution JSON in this package records the actual bounded C20 Python replay only. No trusted workflow run or kernel artifact digest is invented. All controls and existing candidate files remain unchanged.
