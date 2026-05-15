# Post-D1 Pre-Scoring Audit

Date: 2026-05-02

Scope: `hallucination-research` after D1 truncation reruns and clean merged dataset creation.

Reviewed state:

- HEAD: `d3dad03 Rerun truncated responses and build clean dataset`
- Clean merged dataset: `runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`
- Deviation log: `proofs/DEVIATION_LOG_V1.md`
- D1 report: `proofs/TRUNCATION_RERUN_D1_20260502.md`

## Verdict

Conditional pass.

Status after audit: the required D1 deviation-log cleanup was completed in commit `58e5eaf` (`Tighten D1 scoring readiness boundary`). Scoring may proceed under the API-first/Qwen-degraded rule described below.

The lab is ready for API-provider scoring against the clean merged dataset. It is not ready for unrestricted four-provider pooled scoring because local Qwen remains a degraded cell with residual truncation concentrated in the false-anchor conditions.

Scoring may proceed only if:

1. API-provider results are reported separately from Qwen.
2. Qwen-specific claims explicitly disclose residual truncation.
3. Any pooled all-provider claim includes sensitivity analysis excluding capped Qwen rows, or excludes Qwen from the primary pooled result.
4. `proofs/DEVIATION_LOG_V1.md` is updated to match the actual accepted rerun path.

## Audit Inputs

Two independent audit agents reviewed the current lab state read-only.

Agent A verdict:

> Not ready for unrestricted scoring. It is ready for API-provider scoring, and for Qwen only as a degraded/sensitivity cell. Pooled all-model primary scoring is blocked unless Qwen capped rows are excluded or explicitly sensitivity-analyzed.

Agent B verdict:

> Conditional pass. The clean merged dataset exists and its core counts are supported, but scoring should only proceed with the stated Qwen caveat and with API/Qwen claims separated.

Local verification was also performed against `raw_responses.jsonl`, `run_manifest.json`, `RUN_SUMMARY.md`, `replacement_map.json`, and preserved rerun directories.

## Verified Counts

Clean merged dataset:

- Total rows: 200
- Providers:
  - OpenAI: 50
  - Anthropic: 50
  - xAI: 50
  - local Qwen: 50
- Replacements: 67
- Errors: 0

Finish reasons after merge:

- OpenAI: 50 `stop`
- Anthropic: 50 `end_turn`
- xAI: 50 `stop`
- local Qwen: 15 `stop`, 35 `length`

Evidence:

- `runs/hallucination-v2-clean-merged-20260502T1648Z/RUN_SUMMARY.md`
- `runs/hallucination-v2-clean-merged-20260502T1648Z/run_manifest.json`
- `runs/hallucination-v2-clean-merged-20260502T1648Z/replacement_map.json`
- `runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`

## High Finding: Qwen Truncation Is Condition-Confounded

The remaining Qwen truncation is not evenly distributed across conditions. It is concentrated in the hallucination-pressure cells:

- false-anchor forced: 20/20 capped
- false-anchor plain: 10/10 capped
- true-premise control: 4/10 capped
- open-structure control: 1/10 capped

This blocks unrestricted four-provider pooled scoring. If Qwen is pooled naively, condition-level comparisons may reflect response-length/cap behavior rather than hallucination behavior.

Allowed treatment:

- API-provider primary scoring may proceed.
- Qwen may be reported as a degraded local-model cell.
- Pooled claims must either exclude Qwen or include sensitivity analysis excluding capped Qwen rows.

Blocked claims:

- "All providers are clean/natural-stop."
- "Qwen natural-stop behavior was fully observed."
- Strong Qwen-specific hallucination-rate claims without sensitivity analysis.
- Unqualified four-provider pooled effect claims.

## Material Finding: Canonical Deviation Log Is Inexact

`proofs/DEVIATION_LOG_V1.md` records D1 and correctly states that the change happened after model collection but before primary scoring. That is the important integrity point.

However, the canonical D1 entry says the truncated rows were rerun at `max_tokens=2400` and describes the expected effect as removing asymmetric truncation bias.

The final accepted path was more nuanced:

- OpenAI truncated row: fixed.
- xAI truncated row: fixed.
- Claude rows: fixed at `max_tokens=4000`.
- Qwen rows: collected at `max_tokens=2300`, with 35/50 still capped.

The detailed D1 report states this honestly in `proofs/TRUNCATION_RERUN_D1_20260502.md`, but the canonical deviation log should be updated so it can stand alone.

Required cleanup:

- Amend D1 to say the initial plan was 2400-token rerun.
- Record that the accepted final path used Claude `max_tokens=4000` and Qwen `max_tokens=2300`.
- Record that Qwen remains degraded with 35/50 capped responses.
- Replace "removing asymmetric truncation bias" with "removing API-provider truncation bias while leaving Qwen as a disclosed degraded cell."

## Material Finding: Clean Dataset Is Correct Input For API Scoring

The clean merged dataset is the correct scoring input for API-provider analysis.

Supported facts:

- The original 900-token run is preserved.
- Failed and partial rerun attempts are preserved.
- All 67 originally truncated rows were replaced in the merged dataset.
- API providers are now natural-stop/end-turn across 150/150 rows.
- `errors.jsonl` for the clean merged run is empty.

Evidence:

- `runs/hallucination-v2-full-20260502T145359Z/`
- `runs/hallucination-v2-truncated-rerun-20260502T1555Z/`
- `runs/hallucination-v2-truncated-rerun-20260502T1605Z/`
- `runs/hallucination-v2-claude-rerun-20260502T1638Z/`
- `runs/hallucination-v2-qwen-rerun-20260502T1625Z/`
- `runs/hallucination-v2-clean-merged-20260502T1648Z/`

## Material Finding: Failed And Partial Attempts Were Preserved

The failed and partial attempts were not hidden.

Preserved artifacts include:

- `runs/hallucination-v2-truncated-rerun-20260502T1555Z`
- `runs/hallucination-v2-truncated-rerun-20260502T1605Z`
- `runs/hallucination-v2-qwen-rerun-20260502T1625Z`
- `runs/hallucination-v2-claude-rerun-20260502T1638Z`

This supports the integrity claim that D1 was handled as a documented correction rather than silent result massaging.

## Minor Findings

1. `README.md` still describes the repository as a pre-run experimental scaffold. It is stale relative to the completed v2 model collection and clean merged dataset.

2. The D1 report mentions Qwen feasibility probes at multiple token caps, but the raw probe artifacts are thinner than the rest of the proof chain. This is not a blocker because the accepted Qwen rerun artifact is preserved.

3. The clean merged run id includes `1648Z`, while `run_manifest.json` records `created_at_utc` as `2026-05-02T16:40:22Z`. Low severity, but future scripts should avoid confusing timestamp drift.

4. `scripts/merge_truncation_rerun.py` appears to collect `errors.jsonl` only from the source run and the final rerun argument. The current merged dataset's `errors=0` is still consistent because accepted reruns had no errors, but the script should be hardened before reuse.

## Exact Honest Claim Allowed Now

After the initial 900-token run showed asymmetric truncation, the original run and failed/partial reruns were preserved. A clean merged dataset was built at `runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`, replacing all 67 originally truncated rows. API-provider truncation is resolved at 0/150 after replacement. Local Qwen remains degraded with 35/50 responses still capped at `max_tokens=2300`, concentrated in false-anchor conditions. Therefore API-provider scoring can proceed, while Qwen-specific or pooled four-provider claims require explicit degraded-cell disclosure and sensitivity analysis excluding capped Qwen rows.

## Claims Not Allowed

- Do not claim all four providers are natural-stop clean.
- Do not claim Qwen was fixed by the rerun.
- Do not claim Qwen-specific hallucination rates without caveat and sensitivity analysis.
- Do not use the original 900-token run as the primary scoring dataset.
- Do not make pooled four-provider headline claims without showing the result is robust to excluding capped Qwen rows.

## Recommended Next Steps

1. Update `proofs/DEVIATION_LOG_V1.md` to match the final accepted D1 path.
2. Score the API providers first.
3. Add one explicit Qwen sensitivity path:
   - API-only primary result;
   - API + Qwen natural-stop-only sensitivity;
   - optional all-Qwen degraded appendix, clearly marked.
4. Update `README.md` status after scoring or before any external sharing.

## Final Scoring Gate

Proceed to scoring after D1 log cleanup.

Primary scoring dataset:

`runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`

Primary reporting scope:

API providers first. Qwen separated or sensitivity-tested.
