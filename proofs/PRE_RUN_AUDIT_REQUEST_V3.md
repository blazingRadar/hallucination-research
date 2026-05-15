# Pre-Run Audit Request V3: Verification Gate

Date: 2026-05-02

## Request

Audit the V3 verification-gate package before any model run.

Primary files:

- `corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl`
- `protocols/OSF_PREREG_VERIFICATION_GATE_V3.md`
- `protocols/ANALYSIS_PLAN_V3_VERIFICATION_GATE.md`
- `protocols/RUN_PROTOCOL_V3_VERIFICATION_GATE.md`
- `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
- `scripts/validate_corpus_v3.py`
- `scripts/run_model_lab.py`
- `proofs/DEVIATION_LOG_V3.md`

## Audit Questions

1. Are the V3 anchors genuinely held out from V2?
2. Are any fabricated anchors accidentally real or too close to real entities?
3. Does the verify-gate condition isolate the intended intervention?
4. Are success and falsification thresholds specific enough?
5. Are verified controls adequate to catch over-refusal?
6. Does the run protocol prevent adaptive prompt tuning?
7. Is Qwen properly excluded from primary scope after the V2 truncation finding?

## Gate

Do not run models until this package is validated, hashed, committed, and audit-reviewed or self-audit-cleared with documented residual risks.
