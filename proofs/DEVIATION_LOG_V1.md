# Deviation Log V1

Date initialized: 2026-05-02

## D1 — Truncated-response subset rerun

- timestamp: 2026-05-02T15:50:00Z
- files changed: `scripts/rerun_truncated_subset.py`, `scripts/merge_truncation_rerun.py`, run artifacts under `runs/`
- reason: post-run audit found asymmetric max-token truncation in the locked 900-token run: OpenAI 1/50, Anthropic 15/50, xAI 1/50, local Qwen 50/50. The truncation rate is high enough to bias scoring, especially for Qwen.
- timing: after initial model collection, before primary scoring.
- action: preserve the original 900-token run unchanged; rerun rows with provider finish reason `length` or `max_tokens`; preserve failed/partial reruns; merge replacements into a clean analysis dataset while preserving the original response hashes.
  - OpenAI: 1 truncated row replaced; final OpenAI merged set is 50/50 natural stop.
  - xAI: 1 truncated row replaced; final xAI merged set is 50/50 natural stop.
  - Anthropic: 15 truncated rows replaced; accepted Claude path used `max_tokens=4000`; final Anthropic merged set is 50/50 natural stop.
  - local Qwen: 50 truncated rows rerun; accepted Qwen path used `max_tokens=2300`; final Qwen merged set is 15/50 natural stop and 35/50 still capped.
- expected effect on claims: improves scoring validity for API providers by removing asymmetric truncation bias. The original 900-token run becomes exploratory for scoring purposes. Primary claims must use the merged clean dataset, not the original truncated dataset. Qwen remains a degraded local-model cell; Qwen-specific or pooled four-provider claims require caveat/sensitivity analysis.

Any change after preregistration lock must be appended here with:

- timestamp;
- file changed;
- reason;
- whether change occurred before or after model runs;
- expected effect on claims.
