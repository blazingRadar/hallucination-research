# V6 Dose-Response Results

Clean run: `runs/hallucination-v6-dose-response-20260504T133149Z-clean-merged`

## Dose Rates

| Named slots | Positive | N | Rate | Wilson 95% CI |
|---:|---:|---:|---:|---:|
| 0 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 1 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 2 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 4 | 4 | 144 | 0.028 | [0.011, 0.069] |
| 8 | 20 | 144 | 0.139 | [0.092, 0.205] |

## Preregistered Tests

- Cochran-Armitage z: `7.634`, two-sided p: `0.000`
- Length-covariate logistic status: `converged`
- Logistic named-slot coefficient: `1.644`, two-sided p: `0.000`
- Logistic prompt-length coefficient: `0.263`, two-sided p: `0.326`
- Fisher exact 8 vs 0 two-sided p: `0.000001`
- Fisher exact high dose (4/8) vs low dose (0/1) two-sided p: `0.000000`

## Per-Provider Trend

| Provider | Cochran-Armitage z | Two-sided p |
|---|---:|---:|
| anthropic | NA | NA |
| openai | 7.986 | 0.000 |
| xai | 0.354 | 0.723 |

## Prompt Lengths

| Named slots | N | Mean chars | Min | Max |
|---:|---:|---:|---:|---:|
| 0 | 144 | 358.625 | 343 | 371 |
| 1 | 144 | 364.625 | 349 | 377 |
| 2 | 144 | 366.625 | 351 | 379 |
| 4 | 144 | 370.625 | 355 | 383 |
| 8 | 144 | 372.625 | 357 | 385 |

## Human Override Disclosure

- Human overrides applied: `no`
- Highest-dose anchor positive fraction: `0.167`

## Judge Agreement

- Positive-label agreement: `0.919`
- Primary-label agreement: `0.865`
- Disagreements: `97`
