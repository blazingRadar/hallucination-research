# V4B Post-Run Self-Audit

Date: 2026-05-03

## Status

PASS for run integrity and preregistered threshold.

## Gate Discipline

Gate commit:

`0cd1ce0 Pre-register V4B neutral-schema rerun`

The gate commit preceded all provider calls.

Post-gate deviation commit:

`8e2f1f1 Log and retry malformed V4B judge JSON`

This commit happened after two Anthropic judge JSON failures and before final
Anthropic scoring completed. The deviation is logged in `proofs/DEVIATION_LOG_V4B.md`.

## Corpus Check

Validator:

```bash
./scripts/validate_corpus_v4b.py
```

Observed:

```text
rows=12
errors=0
status=PASS
```

## Provider Run Check

Raw run:

`runs/hallucination-v4b-neutral-schema-20260503T054605Z`

- Rows: `36`
- Errors: `0`
- Providers: OpenAI 12, Anthropic 12, xAI 12
- Condition: `false_anchor_open_structure_neutral_schema` for all 36 rows
- Finish reasons: all natural stop/end_turn

## Scoring Check

OpenAI judge:

`scored/scoring-v4b-openai-20260503T055931Z`

- Scores: `36`
- Labels: `accurate_answer` for all 36
- Hallucination-positive: `0`

Anthropic judge:

`scored/scoring-v4b-anthropic-20260503T060219Z`

- Scores: `36`
- Labels: `accurate_answer` for all 36
- Hallucination-positive: `0`
- Parse failures preserved: `2`
- Final retries succeeded

## Analysis Check

Analysis:

`analysis/analysis-v4b-neutral-schema-20260503T060618Z`

- AND-agreement positives: `0/36`
- Aggregate rate: `0.000`
- Wilson 95% CI: `[0.000, 0.096]`
- Threshold success: `true`
- Judge disagreements: `0`
- Misrecalls: `0`
- Confabulation log rows: `0`

## Boundary Check

The supported claim is schema-specific:

> Jointly neutralizing named-entity output slots and adding explicit
> anti-identifier exclusions removed the observed V4 named-slot failure on this
> 12-domain corpus.

The unsupported claim would be:

> Neutral schemas solve hallucination generally.

That stronger claim remains disallowed.

Also unsupported:

> V4B alone isolates named-slot semantics from the explicit exclusion clause.
