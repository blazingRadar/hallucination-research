# V3 Verification Gate Results

Score root: `scored/scoring-v3-verification-gate-20260502T174905Z`

Success threshold met: `False`

## Condition Rates

| Provider | Condition | Positive | N | Rate |
|---|---|---:|---:|---:|
| anthropic | false_anchor_forced | 0 | 12 | 0.000 |
| anthropic | false_anchor_plain | 1 | 12 | 0.083 |
| anthropic | false_anchor_verify_gate | 0 | 12 | 0.000 |
| anthropic | verified_control | 0 | 6 | 0.000 |
| openai | false_anchor_forced | 8 | 12 | 0.667 |
| openai | false_anchor_plain | 5 | 12 | 0.417 |
| openai | false_anchor_verify_gate | 0 | 12 | 0.000 |
| openai | verified_control | 0 | 6 | 0.000 |

## Thresholds

| Provider | Forced | Plain | Verify | Forced-Verify | Control Useful | Control Failure |
|---|---:|---:|---:|---:|---:|---:|
| anthropic | 0.000 | 0.083 | 0.000 | 0.000 | 0.000 | 0.000 |
| openai | 0.667 | 0.417 | 0.000 | 0.667 | 0.000 | 0.000 |

## Claims Still Not Allowed

- Do not claim verification gates solve hallucination generally.
- Do not claim cross-model generality beyond OpenAI and Claude.
- Do not claim final labels until independent audit.
