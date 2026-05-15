# V4B Neutral-Schema Results

Clean run: `runs/hallucination-v4b-neutral-schema-20260503T054605Z`

Threshold success: `True`

## V4B Neutral-Schema Rates

| Provider | Positive | N | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| anthropic | 0 | 12 | 0.000 | [0.000, 0.242] |
| openai | 0 | 12 | 0.000 | [0.000, 0.242] |
| xai | 0 | 12 | 0.000 | [0.000, 0.242] |
| ALL | 0 | 36 | 0.000 | [0.000, 0.096] |

## V3 Forced Baseline (OpenAI/Anthropic Only)

| Provider | Positive | N | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| anthropic | 0 | 12 | 0.000 | [0.000, 0.242] |
| openai | 8 | 12 | 0.667 | [0.391, 0.862] |

## Judge Agreement

- Positive-label agreement: 1.000
- Primary-label agreement: 1.000
- Cohen kappa on hallucination-positive boolean: degenerate single-class agreement. The script reports 1.000 by convention because both judges labeled every row negative.
- Disagreements: 0

## Boundary

This does not establish whether the false anchor or the task frame is the primary driver — that is the V5 question.
