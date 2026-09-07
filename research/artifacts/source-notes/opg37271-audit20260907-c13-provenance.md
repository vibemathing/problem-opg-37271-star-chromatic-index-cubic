# C13 original-variant transport provenance

Verdict: `candidate_only`. Audit: `transport-audit-20260907-r01`.
Source: PR #19 at immutable head `85499c0d2f44c165611c66f8f0bd72b8f37536c9`.
Comparison target: main `07336a2e31928b1972e93cd44037c57f5f397510`.

PR #19 was previously closed after PR #20 transported C13H. The broad height theorem and graph overlap, but the original proof, standalone checker and result are different byte versions. In particular the original final repair changes ux from 1 to 3 and xa from 3 to 5, then colors uv with 1. C13H instead records a support-edge repair. The original result's final pair table therefore is not duplicated by the C13H result.

This transport preserves the three original blobs without alteration under `research/artifacts/candidates/opg37271-c13-original/`. It does not overwrite C13H's same-basename main files or claim a newly derived theorem. The existing branch and PR #19 are reused after non-force synchronization. Exactly one packet, `research/artifacts/web-inbox/opg37271-c13.packet.json`, transports this archival variant.

The original document's historical reproduction command names the then-current root-level checker. For this archived variant, use `python research/artifacts/candidates/opg37271-c13-original/opg37271-c13-height-check.py`. The archived checker is standalone. The result file is preserved historical generator output, not newly observed output or a trusted receipt. No mathematical checker, dynamic program, solver or Lean source was executed during this reconciliation. All mathematical claims and historic execution claims remain pending external review.

The source packet, original paths and original metadata remain accessible at the source head. Both admitted obligations remain open. This provenance note is a transport distinction, not mathematical evidence.
