# V5 Post-Run Self-Audit

Date: 2026-05-03

## Status

PASS for preregistered V5 mechanism threshold.

## Gate Discipline

V5 gate commit:

`ba9434b Pre-register V5 schema-slot mechanism test`

The gate commit preceded all V5 provider calls.

Provider collection and truncation rerun commit:

`5c4c451 Collect V5 provider responses and truncation rerun`

## Corpus Check

Command:

```bash
./scripts/validate_corpus_v5.py
```

Observed:

```text
rows=24
conditions={'named_entity_schema': 12, 'neutral_descriptive_schema': 12}
errors=0
status=PASS
```

## Run Check

Original run:

`runs/hallucination-v5-schema-slot-20260503T065139Z`

- 72 rows
- 0 provider errors
- 36 named-entity schema rows
- 36 neutral descriptive schema rows

D1 truncation rerun:

`runs/hallucination-v5-truncation-rerun-20260503T072229Z`

- 4 Anthropic rows rerun
- all replacement rows ended with `end_turn`

Primary scoring dataset:

`runs/hallucination-v5-clean-merged-20260503T072553Z`

- 72 rows
- 4 replacements
- 0 errors
- all final finish reasons natural stop/end_turn

## Scoring Check

OpenAI judge:

`scored/scoring-v5-openai-20260503T072610Z`

- 72 scores
- 12 hallucination-positive

Anthropic judge:

`scored/scoring-v5-anthropic-20260503T072748Z`

- 72 scores
- 13 hallucination-positive
- 1 malformed JSON response preserved and repaired by retry

AND-agreement positives:

- 10 rows

## Analysis Check

Analysis:

`analysis/analysis-v5-schema-slot-20260503T073722Z`

- named entity schema: `10/36 = 0.278`
- neutral descriptive schema: `0/36 = 0.000`
- named-minus-neutral difference: `0.278`
- threshold success: `true`
- judge disagreements: `8`
- misrecalls: `0`

## Boundary

Supported:

> Named-entity output slots increased hallucination-positive outputs on this
> paired 12-domain corpus when compared against the V4B neutral descriptive
> schema that also carried explicit anti-fabrication exclusions.

Not supported:

> Neutral schemas solve hallucination generally.

Also not supported:

> V5 fully isolates field-label semantics from explicit exclusion clauses.

The neutral arm includes `exclude: proper_nouns, identifiers, citations` style
constraints inherited from V4B. A smaller follow-up should test neutral
descriptive schema without those exclusions.
