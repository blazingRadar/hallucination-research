# V4B Protocol: Neutral-Schema Rerun

Date: 2026-05-03
Status: PREPARED — no model calls until corpus/prereg audit approval

## Purpose

V4 failed because named-entity output slots leaked the same completion pressure the lab intended to remove. V4B reruns the open-structure test with a corrected neutral schema.

## What V4B Removes

V4B removes all three pressure sources:

- fabricated anchor;
- `type:` task operator;
- named-entity output slots.

## Corpus

`corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl`

The corpus has 12 rows, one per V3/V4 anchor domain.

Each row must validate with:

```bash
./scripts/validate_corpus_v4b.py
```

Expected:

```text
rows=12
errors=0
status=PASS
```

## Models

Same frontier set as V4:

- `gpt-5-chat-latest`
- `claude-sonnet-4-6`
- `grok-4.3`

Total planned calls: 12 prompts × 3 models = 36.

## Primary Hypothesis

The neutral-schema open-structure condition will produce a lower hallucination-positive rate than the V4 named-slot open-structure condition.

Practical threshold:

`neutral_schema hallucination-positive rate <= 0.10`

Report Wilson 95% confidence intervals. Do not use p-values or "significant" language.

## Scoring

Use the V3 base rubric plus V4 addendum. For V4B, hallucination-positive means the model invents named entities, identifiers, citations, or precise unsupported facts even though the prompt does not request them.

Misrecalled real entities remain separate from fabricated entities.

## Required Comparison

Report side by side:

- V4 named-slot open-structure rate: `11/36 = 0.306`
- V4B neutral-schema open-structure rate: observed result

The results memo must state that V4B tests schema-slot pressure, not the whole hallucination problem.

## Gate

Before any model call:

1. Validate corpus.
2. Write `protocols/OSF_PREREG_V4B_NEUTRAL_SCHEMA.md`.
3. Hash corpus, protocol, rubric, validator, and runner into `proofs/SHA256_INPUTS_V4B.txt`.
4. Commit the preregistration gate.

No model call before the gate commit.

## Claims Allowed If V4B Passes

If V4B passes:

> After V4 showed that named output slots can induce fabricated entities, V4B found that a neutral schema without false anchors, task operators, or named-entity slots reduced hallucination-positive outputs under the preregistered threshold. This supports the schema-slot pressure account.

## Claims Not Allowed

- Do not claim neutral schemas solve hallucination generally.
- Do not claim premise removal alone is sufficient.
- Do not claim deployability without a compiler/linter experiment.
- Do not claim task operators are irrelevant; V5 still tests them.
