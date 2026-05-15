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

## Provider Boundary

The strongest honest reading is provider-conditional:

> V6 shows a clear ordered increase in dual-judge hallucination-positive rate
> as named-artifact schema slots increase, and the effect survives prompt-length
> adjustment. The result is concentrated in OpenAI outputs, with xAI producing
> one low/mid-dose positive and Anthropic producing none under the AND-positive
> rule.

The preregistered primary success condition was not fully met:

- Required 8-slot minus 0-slot difference: `>= 0.15`
- Observed 8-slot minus 0-slot difference: `0.139`
- Therefore: primary effect-size threshold narrowly missed.

The trend test condition was met, and the provider-trend headline boundary is
technically met under "positive trend in at least 2 of 3 providers," but this
needs caveat:

- OpenAI: strong positive trend.
- xAI: weak positive z driven by a single dose-4 positive, not a dose-8 effect.
- Anthropic: no positives, trend undefined.

Do not frame V6 as a clean cross-provider dose-response win without that
qualification.

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
- Highest-dose anchor-provider positive fraction: `0.167`
- Highest-dose anchor any-provider positive fraction: `0.500`

## Preregistered Claim Check

- 8-slot minus 0-slot rate difference: `0.139`
- Meets preregistered >=0.15 difference threshold: `False`
- Providers with z > 0 trend: `2/3`
- Providers with significant positive trend: `1/3`

Provider qualifier: the provider-trend boundary should not be framed as a clean
cross-provider win. OpenAI carried the dose-response signal. xAI's weak positive
z was driven by a single dose-4 positive and no dose-8 positives, and Anthropic
produced zero positives at every dose.

## Judge Agreement

- Positive-label agreement: `0.919`
- Primary-label agreement: `0.865`
- Disagreements: `97`
