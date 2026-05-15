# V6 Dose-Response Results

Clean run: `runs/hallucination-v6-dose-response-20260504T133149Z-clean-merged`

## Dose Rates

| Named slots | Positive | N | Rate | Wilson 95% CI |
|---:|---:|---:|---:|---:|
| 0 | 0 | 141 | 0.000 | [0.000, 0.027] |
| 1 | 0 | 142 | 0.000 | [0.000, 0.026] |
| 2 | 0 | 142 | 0.000 | [0.000, 0.026] |
| 4 | 4 | 143 | 0.028 | [0.011, 0.070] |
| 8 | 20 | 142 | 0.141 | [0.093, 0.208] |

## Preregistered Tests

- Cochran-Armitage z: `7.631`, two-sided p: `0.000`
- Length-covariate logistic status: `converged`
- Logistic named-slot coefficient: `1.647`, two-sided p: `0.000`
- Logistic prompt-length coefficient: `0.255`, two-sided p: `0.342`
- Fisher exact 8 vs 0 two-sided p: `0.000001`
- Fisher exact high dose (4/8) vs low dose (0/1) two-sided p: `0.000000`

## Per-Provider Trend

| Provider | Cochran-Armitage z | Two-sided p |
|---|---:|---:|
| anthropic | NA | NA |
| openai | 7.986 | 0.000 |
| xai | 0.363 | 0.716 |

## Prompt Lengths

| Named slots | N | Mean chars | Min | Max |
|---:|---:|---:|---:|---:|
| 0 | 141 | 358.624 | 343 | 371 |
| 1 | 142 | 364.634 | 349 | 377 |
| 2 | 142 | 366.634 | 351 | 379 |
| 4 | 143 | 370.559 | 355 | 383 |
| 8 | 142 | 372.676 | 357 | 385 |

## Human Override Disclosure

- Human overrides applied: `no`
- Highest-dose anchor positive fraction: `0.167`

## Judge Agreement

- Positive-label agreement: `0.918`
- Primary-label agreement: `0.865`
- Disagreements: `96`
