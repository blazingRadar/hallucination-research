# Audit Request: V3 Verification Gate Results

Date: 2026-05-02

## Requested Verdict

Please audit whether V3 supports the claimed verification-gate result and whether any claim boundary needs tightening.

## Files To Review First

- `protocols/OSF_PREREG_VERIFICATION_GATE_V3.md`
- `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
- `proofs/DEVIATION_LOG_V3.md`
- `proofs/RESULTS_MEMO_V3_VERIFICATION_GATE_20260502.md`
- `runs/hallucination-v3-clean-merged-20260502T174849Z/run_manifest.json`
- `runs/hallucination-v3-clean-merged-20260502T174849Z/replacement_map.json`
- `scored/scoring-v3-verification-gate-20260502T174905Z/adjudicated_scores.jsonl`
- `analysis/analysis-v3-verification-gate-fixed-20260502T175120Z/analysis_summary.json`

## Specific Audit Questions

1. Did D1 appropriately handle the two Anthropic truncations before scoring?
2. Are D2 and D3 harmless analysis-tooling fixes, or do they affect the claim boundary?
3. Are the judge labels plausible under `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`?
4. Does the OpenAI verify-gate result survive a hand audit of the 12 OpenAI verify-gate rows?
5. Does the single Anthropic plain-condition positive label look valid?
6. Is the supported claim in `proofs/RESULTS_MEMO_V3_VERIFICATION_GATE_20260502.md` appropriately narrow?
7. Is the proposed follow-up, separating verification semantics from prompt length/caution framing, the right next experiment?

## Known Boundary

This is a prompt-intervention result on a held-out synthetic-anchor corpus. It is not a general hallucination solution, not a production safety result, and not a tell-word detector.
