# Scoring Readiness After D1 Audit

Date: 2026-05-02

## Verdict

Conditional pass for scoring readiness.

The clean merged dataset is real and should be used for scoring:

`runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`

Do not run unrestricted pooled four-provider scoring as the primary claim. The correct scoring posture is API-first, with Qwen handled as a degraded local-model cell.

## Evidence State

Merged dataset:

- rows: 200
- replacements: 67
- errors: 0
- OpenAI: 50/50 natural stop
- Anthropic: 50/50 natural stop
- xAI: 50/50 natural stop
- local Qwen: 15/50 natural stop, 35/50 still capped at `max_tokens=2300`

Qwen residual truncation is condition-concentrated:

- false-anchor forced: 20/20 capped
- false-anchor plain: 10/10 capped
- true-premise control: 4/10 capped
- open-structure control: 1/10 capped

This concentration means Qwen cannot be pooled into the primary four-provider condition-level claim without bias risk.

## Scoring Rule

Primary scoring:

1. Score API providers normally: OpenAI, Claude, xAI.
2. Report API-pooled condition rates as the primary interpretable result.
3. Report Qwen separately as degraded local-model evidence.

Required sensitivity analyses:

1. API-only primary analysis.
2. All providers with Qwen included but caveated.
3. Exclude capped Qwen rows, or exclude Qwen entirely, before making any pooled claim.

## Claims Allowed

After asymmetric truncation was discovered, the original run and failed reruns were preserved, and a merged dataset was built replacing all 67 originally truncated rows. API-provider truncation is resolved at 0/150. Local Qwen remains degraded with 35/50 capped responses, so Qwen-specific or pooled four-provider claims require caveat/sensitivity analysis.

## Claims Not Allowed

- Do not claim four-provider pooled hallucination rates as the main result without sensitivity analysis.
- Do not claim Qwen natural-stop behavior was fully observed.
- Do not treat capped Qwen pressure-condition responses as equivalent to natural-stop API responses.
- Do not score the original `max_tokens=900` run as the primary dataset.

## Next Step

Proceed to scoring only after this memo and `proofs/DEVIATION_LOG_V1.md` are committed. Scoring scripts should make the primary API-only analysis explicit and should put Qwen in a separate degraded-cell section.
