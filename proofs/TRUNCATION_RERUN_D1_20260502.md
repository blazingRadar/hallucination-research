# D1 Truncation Rerun Report

Date: 2026-05-02

## Reason

The post-run audit found asymmetric truncation in the initial `max_tokens=900` collection:

- OpenAI: 1/50 truncated
- Anthropic: 15/50 truncated
- xAI: 1/50 truncated
- local Qwen: 50/50 truncated

This was recorded as deviation `D1` before primary scoring. The original run remains preserved, but it is superseded for primary scoring by a merged dataset with replacement responses.

## Actions

1. Preserved failed attempt `runs/hallucination-v2-truncated-rerun-20260502T1555Z`.
   - API replacements reached 17 rows.
   - First Qwen `max_tokens=2400` request timed out under the original local timeout.

2. Preserved second partial attempt `runs/hallucination-v2-truncated-rerun-20260502T1605Z`.
   - OpenAI replacement: natural stop.
   - xAI replacement: natural stop.
   - Anthropic replacements: 14/15 natural stops, 1/15 still `max_tokens`.
   - First Qwen `max_tokens=2400` request returned HTTP 408 from LM Studio.

3. Restarted LM Studio after the Qwen high-cap request wedged the local server.

4. Ran Qwen feasibility probes on the first truncated Qwen prompt.
   - `max_tokens=1200`: `length`
   - `max_tokens=1600`: `length`
   - `max_tokens=2000`: `length`
   - `max_tokens=2200`: `stop`
   - `max_tokens=2300`: `stop`

5. Ran `runs/hallucination-v2-qwen-rerun-20260502T1625Z` with `max_tokens=2300`.
   - 50/50 Qwen rows collected.
   - 0 provider errors.
   - 15/50 natural stops.
   - 35/50 still `length`.

6. Ran `runs/hallucination-v2-claude-rerun-20260502T1638Z` with `max_tokens=4000`.
   - 15/15 Claude rows collected.
   - 0 provider errors.
   - 15/15 natural stops.

7. Built merged scoring dataset `runs/hallucination-v2-clean-merged-20260502T1648Z`.
   - 200 total rows.
   - 67 replacements.
   - 0 errors.
   - OpenAI: 50/50 natural stops.
   - Anthropic: 50/50 natural stops.
   - xAI: 50/50 natural stops.
   - local Qwen: 15/50 natural stops, 35/50 still capped at 2300.

## Interpretation

The truncation defect is fixed for the three API providers. It is not fully fixed for local Qwen on this machine. Qwen's verbosity makes natural-stop collection unstable at the needed cap; a 2400-token attempt produced local server timeouts, while 2300 completed but still left 35 capped responses.

## Scoring Boundary

Primary scoring should use:

`runs/hallucination-v2-clean-merged-20260502T1648Z/raw_responses.jsonl`

Claims allowed:

- API-provider scoring is no longer biased by token truncation.
- The merged dataset preserves all original rows and explicitly replaces the 67 originally truncated rows.
- Qwen is included as a degraded local-model cell with residual truncation disclosed.

Claims not allowed:

- Do not claim Qwen natural-stop behavior was fully observed.
- Do not make strong Qwen-specific hallucination-rate claims without a sensitivity analysis excluding capped Qwen rows.
- Do not treat the original `max_tokens=900` run as the primary scoring dataset.
