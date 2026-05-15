# Hallucination V2 Clean Merged Run Summary

Run ID: `hallucination-v2-clean-merged-20260502T1648Z`

Status: merged dataset for primary scoring after D1 truncation rerun.

- Total rows: 200
- Replaced truncated rows: 67
- Errors: 0
- API model truncation after replacement: 0/150
- Local Qwen truncation after replacement: 35/50 at `max_tokens=2300`

Boundary: primary scoring should use this merged dataset. The original 900-token run is preserved but superseded for primary scoring because of asymmetric truncation. Local Qwen remains degraded because 35/50 responses still hit the token cap even after a targeted rerun; Qwen-specific claims require this caveat or exclusion/sensitivity analysis.
