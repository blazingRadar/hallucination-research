# V5B Post-Run Self-Audit

Date: 2026-05-03

## Status

PASS for the V5B neutral-no-exclude threshold.

## Gate Discipline

Gate commit:

`e5a5068 Pre-register V5B neutral no-exclude follow-up`

The gate preceded V5B provider calls.

## Corpus Check

Command:

```bash
./scripts/validate_corpus_v5b.py
```

Observed:

```text
rows=12
conditions={'neutral_descriptive_schema_no_exclude': 12}
errors=0
status=PASS
```

## Run Check

Primary scoring dataset:

`runs/hallucination-v5b-clean-merged-20260503T080926Z`

- Rows: `36`
- Final provider cells: OpenAI 12, Anthropic 12, xAI 12
- Final finish reasons: all natural stop/end_turn
- Replacement rows: 5

Original timeout/truncation artifacts are preserved.

## Scoring Check

- OpenAI judge rows: 36
- Anthropic judge rows: 36
- AND-agreement positives: 0
- Judge disagreements: 1

## Boundary

Supported:

> Removing the explicit anti-named-entity exclusions did not cause the neutral
> descriptive schema condition to start fabricating under AND-agreement scoring.

Not supported:

> Neutral schemas are generally safe.
