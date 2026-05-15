# Results Memo: V5C Named Schema With Explicit Exclusions

Date: 2026-05-03

## Status

V5C closes the missing named-WITH-exclude cell. The result is
ready for independent audit.

## Question

When output schema fields still request named artifacts, does adding an explicit
`exclude: { proper_nouns, identifiers, citations }` clause suppress the
hallucination-positive rate?

## Run Integrity

- Corpus: `corpus/PROMPT_CORPUS_V5C_NAMED_WITH_EXCLUDE.jsonl`
- Gate commit: `8f45df2 Pre-register V5C named-with-exclude cell`
- Provider run:
  `runs/hallucination-v5c-named-with-exclude-20260503T202759Z`
- Responses: `36/36`
- Provider errors: `0`
- Empty responses: `0`
- Finish reasons:
  - OpenAI: `12/12 stop`
  - Anthropic: `12/12 end_turn`
  - xAI: `12/12 stop`
- Credential values saved: `false`

## Scoring

Dual-judge scoring:

- OpenAI judge:
  `scored/scoring-v5c-openai-20260503T204232Z`
- Anthropic judge:
  `scored/scoring-v5c-anthropic-batch1-20260503T204341Z`

Primary rule: AND-agreement hallucination-positive.

One Anthropic judge attempt failed closed after returning an invalid
`response_hash`; the failed partial scoring directory is preserved and the
successful rerun used batch size 1. Logged in `proofs/DEVIATION_LOG_V5C.md` D1.

## Result

V5C named-with-exclude:

- AND-agreement hallucination-positive: `14/36`
- Rate: `0.389`
- Wilson 95% CI: `[0.248, 0.551]`

Per provider:

- OpenAI: `6/12`, Wilson 95% `[0.254, 0.746]`
- Anthropic: `5/12`, Wilson 95% `[0.193, 0.680]`
- xAI: `3/12`, Wilson 95% `[0.089, 0.532]`

Judge agreement:

- Positive-label agreement: `0.750`
- Primary-label agreement: `0.694`
- Disagreements: `11`

## Comparison To Prior Cells

- V5 named-no-exclude: `10/36`
- V5 neutral-with-exclude: `0/36`
- V5B neutral-no-exclude: `0/36`
- V5C named-with-exclude: `14/36`

This closes the previously missing 2x2 cell. On this corpus, explicit
anti-identifier exclusions did not suppress named-slot pressure. The public
claim can now say that named slots produced hallucination-positive responses
both with and without explicit anti-identifier exclusions, while neutral slots
stayed at zero both with and without those exclusions.

## Important Caveats

- V5C was a follow-up run, not part of the original V5 provider batch.
- Prompt length is still not controlled.
- Dose-response on number of named slots is still not tested.
- Generalization beyond the 12-anchor synthetic corpus is still not tested.
- Judge disagreement is non-trivial (`11/36`); the AND-agreement result is the
  preregistered primary rule, but a stricter or different adjudication policy
  should be reported separately if used.

## Claim Boundary After V5C

Allowed:

> On a 12-anchor synthetic corpus across three frontier models, with false
> anchors and `type:` operators absent in every cell, named-entity output schema
> slots produced hallucination-positive responses both without explicit
> anti-identifier exclusions (`10/36`) and with explicit anti-identifier
> exclusions (`14/36`). Neutral descriptive schema slots produced `0/36` both
> with and without those exclusions. This supports a schema-slot pressure
> account on this corpus.

Not allowed:

- Do not claim production readiness.
- Do not claim neutral schemas solve hallucination.
- Do not claim length-matched controls were run.
- Do not claim dose-response on slot count was tested.
- Do not claim generalization beyond this corpus and model set.

## Artifact Index

- Analysis:
  `analysis/analysis-v5c-named-with-exclude-20260503T204940Z`
- Positive log:
  `analysis/analysis-v5c-named-with-exclude-20260503T204940Z/positive_log.jsonl`
- Disagreement log:
  `analysis/analysis-v5c-named-with-exclude-20260503T204940Z/judge_disagreements.jsonl`
- Source responses:
  `runs/hallucination-v5c-named-with-exclude-20260503T202759Z/raw_responses.jsonl`
