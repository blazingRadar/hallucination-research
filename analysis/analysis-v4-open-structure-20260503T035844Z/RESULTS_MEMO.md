# V4 Open-Structure Results

Clean run: `runs/hallucination-v4-clean-merged-20260503T034907Z`

Threshold success: `False`

## V4 Open-Structure Rates

| Provider | Positive | N | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| anthropic | 4 | 12 | 0.333 | [0.138, 0.609] |
| openai | 4 | 12 | 0.333 | [0.138, 0.609] |
| xai | 3 | 12 | 0.250 | [0.089, 0.532] |
| ALL | 11 | 36 | 0.306 | [0.180, 0.469] |

## V3 Forced Baseline (OpenAI/Anthropic Only)

| Provider | Positive | N | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| anthropic | 0 | 12 | 0.000 | [0.000, 0.242] |
| openai | 8 | 12 | 0.667 | [0.391, 0.862] |

## Judge Agreement

- Positive-label agreement: 0.833
- Primary-label agreement: 0.750
- Cohen kappa on hallucination-positive boolean: 0.650
- Disagreements: 9

## Boundary

This does not establish whether the false anchor or the task frame is the primary driver — that is the V5 question.
