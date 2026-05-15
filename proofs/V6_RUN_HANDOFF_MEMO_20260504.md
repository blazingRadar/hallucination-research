# V6 Run Handoff Memo

Date: 2026-05-04
Status: READY FOR POST-RUN AUDIT

## What Ran

V6 dose-response ran against the locked V6 corpus:

- corpus: `corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl`
- source run: `runs/hallucination-v6-dose-response-20260504T133149Z`
- clean merged run: `runs/hallucination-v6-dose-response-20260504T133149Z-clean-merged`
- models: `gpt-5-chat-latest`, `claude-sonnet-4-6`, `grok-4.3`
- temperature: `0`
- total clean response rows: `720`
- scoring: dual judge, OpenAI + Anthropic, AND-positive primary rule
- human overrides applied: `no`

## Integrity Summary

The first raw collection exposed the same kind of issue prior audits warned us
to catch before scoring:

- OpenAI: `240/240` responses, no capped rows.
- xAI: `234/240` responses, `6` timeout errors.
- Anthropic: `240/240` responses, `232` capped at `max_tokens=1800`.

Scoring was paused before it began. The repair path was logged in
`proofs/DEVIATION_LOG_V6.md`:

- xAI timeout rows were rerun successfully: `6/6`, all natural stops.
- Anthropic capped rows were rerun at `4000`, but that still capped `3/7`
  sampled rows, so that repair was stopped and preserved as failed repair.
- Anthropic capped rows were rerun at `8000`: `232/232` collected,
  `229` natural stops, `2` capped, `1` refusal.
- The two residual capped rows were rerun at `12000` and ended naturally.
- One Anthropic row, `V6A020_N0_R1`, remained a stable empty refusal.

Final clean merged dataset:

- `720/720` rows
- `0` provider errors
- `0` capped rows
- finish reasons:
  - OpenAI: `240 stop`
  - xAI: `240 stop`
  - Anthropic: `232 end_turn`, `8 refusal`

The eight Anthropic refusal rows are all anchor `V6A020`
(`environmental_monitoring`) and are disclosed in the clean run finish-reason
table.

## Scoring Integrity

Scoring runs:

- OpenAI judge: `scored/scoring-v6-openai-hallucination-v6-dose-response-20260504T133149Z-clean-merged`
- Anthropic judge: `scored/scoring-v6-anthropic-hallucination-v6-dose-response-20260504T133149Z-clean-merged`

Both judges produced `720/720` adjudicated score rows. Anthropic had parse
failures during scoring, but the preregistered retry path recovered them and
the final adjudicated score file is complete.

No human adjudication override was applied.

## Analysis Artifact

Use this final analysis directory:

`analysis/analysis-v6-dose-response-hallucination-v6-dose-response-20260504T133149Z-clean-merged-post-d10`

Earlier analysis directories are invalidated by logged script fixes:

- D9 fixed response-hash-only joins that collapsed identical empty-refusal rows.
- D10 fixed highest-dose anchor-fraction reporting to match the preregistered
  anchor-level weakening condition.

## Primary Results

Dual-judge AND-positive rates:

| Named slots | Positive | N | Rate | Wilson 95% CI |
|---:|---:|---:|---:|---:|
| 0 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 1 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 2 | 0 | 144 | 0.000 | [0.000, 0.026] |
| 4 | 4 | 144 | 0.028 | [0.011, 0.069] |
| 8 | 20 | 144 | 0.139 | [0.092, 0.205] |

Preregistered tests:

- Cochran-Armitage trend: `z = 7.634`, two-sided `p = 2.28e-14`
- Length-covariate logistic regression: converged
- Named-slot coefficient: `1.644`, two-sided `p = 1.91e-06`
- Prompt-length coefficient: `0.263`, two-sided `p = 0.326`
- Fisher exact 8 vs 0: `p = 9.39e-07`
- Fisher exact high dose (4/8) vs low dose (0/1): `p = 7.23e-08`

## Claim Boundary

The strongest honest reading:

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

## Anchor Distribution

At the highest dose, `12/24` anchors had at least one AND-positive response
across any provider:

`V6A001`, `V6A002`, `V6A004`, `V6A006`, `V6A008`, `V6A009`,
`V6A014`, `V6A020`, `V6A021`, `V6A022`, `V6A023`, `V6A024`.

This lands exactly at `50%`, so the preregistered "fewer than 50%" weakening
condition does not fire, but only barely.

## Audit Questions

Please specifically audit:

1. Whether the repair path from initial run to clean merged dataset is acceptable.
2. Whether stable Anthropic refusals on `V6A020` should remain included exactly
   as scored or be handled via sensitivity analysis.
3. Whether the OpenAI-concentrated effect should be framed as provider-specific
   rather than corpus-wide.
4. Whether the missed `>=0.15` effect-size threshold means "primary hypothesis
   not met" or "directionally supported but below preregistered success bar."
5. Whether the xAI provider trend should count toward the "2 of 3" headline
   boundary given that its only AND-positive row is dose 4, not dose 8.

## Bottom Line

V6 is valuable, but the result is not the simple win case. It is a disciplined
near-miss with a strong OpenAI-specific dose signal, a clean length-confound
control, and important provider heterogeneity.
