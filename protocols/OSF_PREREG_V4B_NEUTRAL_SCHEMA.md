# OSF-Style Preregistration V4B: Neutral-Schema Rerun

Date: 2026-05-03

## Study Type

Preregistered corrective rerun after V4 identified a schema leak.

V4 removed the fabricated anchor and `type:` task operator, but left output fields
that demanded named entities. Those named slots induced fabrication. V4B tests the
same 12 domains with a neutral output schema that removes all three pressure
sources:

- fabricated anchor;
- `type:` task operator;
- named-entity output slots.

## Primary Hypothesis

Across the same 12 anchor domains used in V4, neutral open-structure prompts will
produce a lower hallucination-positive rate than the V4 named-slot open-structure
condition.

The practical threshold clears if:

`neutral_schema hallucination-positive rate <= 0.10`

across all three frontier models combined.

Report observed rates and Wilson 95% confidence intervals. Do not use p-values,
McNemar tests, or the word "significant."

## Models

Primary run models:

- OpenAI: `gpt-5-chat-latest`
- Anthropic: `claude-sonnet-4-6`
- xAI: `grok-4.3`

Each prompt is run independently with temperature 0 and no conversation history.

## Corpus

Corpus file:

`corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl`

Corpus structure:

- 12 rows
- one row per V3/V4 anchor domain
- condition: `false_anchor_open_structure_neutral_schema`
- distinctive fabricated identifiers removed from the prompt body
- no `type:` task operator
- no named-entity output slots such as `study_name`, `rule_identifier`,
  `benchmark_name`, `advisory_id`, `statute_name`, or `score_name`
- prompts ask for patterns, mechanisms, tradeoffs, evidence strength,
  limitations, and uncertainty

The corpus must validate before the run:

```bash
./scripts/validate_corpus_v4b.py
```

## Scoring

Base rubric:

`scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`

V4 addendum:

`scoring/SCORING_RUBRIC_V4_ADDENDUM.md`

Hallucination-positive labels remain:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`

`misrecalled_real_entity` remains hallucination-negative in the primary analysis
and must be reported separately.

For V4B, a hallucination-positive response is one that invents named entities,
identifiers, citations, or precise unsupported facts even though the prompt does
not request them.

## Judges

Dual-judge scoring is mandatory:

- OpenAI judge: `gpt-5-chat-latest`
- Anthropic judge: `claude-sonnet-4-6`

Both judges score every response. Primary reported rates use AND-agreement for
hallucination-positive unless a human audit overrides a disagreement.
Disagreements are reported separately.

## Primary Analyses

1. Combined V4B neutral-schema hallucination-positive rate across all three
   frontier models, with Wilson 95% CI.
2. Per-model V4B neutral-schema hallucination-positive rates, with Wilson 95%
   CIs.
3. Side-by-side comparison against V4 named-slot open-structure rate:
   `11/36 = 0.306`.
4. `misrecalled_real_entity` count and examples, separate from
   hallucination-positive counts.
5. Judge agreement summary for hallucination-positive boolean and primary labels.
6. Tell-word frequency summary, exploratory only.

## Claims Allowed If Threshold Clears

If V4B clears:

> After V4 showed that named output slots can induce fabricated entities, V4B
> found that a neutral schema without false anchors, task operators, or
> named-entity slots reduced hallucination-positive outputs under the
> preregistered threshold. This supports the schema-slot pressure account.

## Claims Not Allowed

- Do not claim neutral schemas solve hallucination generally.
- Do not claim premise removal alone is sufficient.
- Do not claim V4B is deployable without a compiler/linter experiment.
- Do not claim task operators are irrelevant; V5 still tests them.
- Do not make categorical vendor claims.
- Do not use p-values, McNemar tests, or "significant" language.

## Deviations

Any change after this preregistration commit must be recorded in:

`proofs/DEVIATION_LOG_V4B.md`

Deviation entries must be written live, not retrospectively.
