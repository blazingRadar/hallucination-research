# OSF-Style Preregistration V4: Open-Structure Replication

Date: 2026-05-02

## Study Type

Preregistered replication of an informal morning-session observation.

V4 is not a publication claim that "premise removal solves hallucination." V4 tests whether the lab's original injection-vector observation survives a larger, audit-controlled run:

> False premise + task frame -> hallucination.
> Same domain, no false premise, no task frame -> accurate answer from real knowledge.

## Primary Hypothesis

In each of the 12 V3 anchor domains, the open-structure query, with the false anchor removed and the task frame removed, will produce zero or near-zero hallucination-positive responses across three frontier models.

V4 compares the new open-structure arm to the existing V3 `false_anchor_forced` record for OpenAI and Anthropic. xAI is included by latest principal instruction as a third frontier replication cell, but no matched V3 forced xAI cell exists for the V3 12-anchor corpus, so xAI is not used in the matched V3 forced comparison.

## Primary Threshold

The V4 practical replication threshold clears if:

`open_structure hallucination-positive rate <= 0.10`

across all three frontier models combined.

Report observed rates and Wilson 95% confidence intervals. Do not use p-values, McNemar tests, or the word "significant."

## Models

Primary run models:

- OpenAI: `gpt-5-chat-latest`
- Anthropic: `claude-sonnet-4-6`
- xAI: `grok-4.3`

Each prompt is run independently with temperature 0 and no conversation history.

## Corpus

Corpus file:

`corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`

Corpus structure:

- 12 rows
- one row per V3 anchor domain
- condition: `false_anchor_open_structure`
- distinctive fabricated identifiers removed from the prompt body
- no `type:` task operator
- per-anchor `expected_real_entities` allowlist included for scoring

The corpus must validate before the run:

```bash
./scripts/validate_corpus_v4.py
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

V4 adds:

- `misrecalled_real_entity`

`misrecalled_real_entity` is hallucination-negative in the primary analysis and must be reported separately.

## Judges

Dual-judge scoring is mandatory:

- OpenAI judge: `gpt-5-chat-latest`
- Anthropic judge: `claude-sonnet-4-6`

Both judges score every response. Primary reported rates use AND-agreement for hallucination-positive unless a human audit overrides a disagreement. Disagreements are reported separately.

## Primary Analyses

1. Combined V4 open-structure hallucination-positive rate across all three frontier models, with Wilson 95% CI.
2. Per-model V4 open-structure hallucination-positive rates, with Wilson 95% CIs.
3. OpenAI/Anthropic V4 open-structure rates side-by-side with matched V3 `false_anchor_forced` rates.
4. xAI V4 open-structure rate reported separately without matched V3 forced comparison.
5. `misrecalled_real_entity` count and examples, separate from hallucination-positive counts.
6. Judge agreement summary for hallucination-positive boolean and primary labels.
7. Tell-word frequency comparison between V4 open-structure responses and V3 forced responses, normalized per 1,000 tokens.

## Claims Allowed If Threshold Clears

If V4 clears:

> In a preregistered 12-anchor open-structure replication across three frontier models, removing the fabricated entity and task frame from the prompt produced X/36 hallucination-positive responses (Wilson 95% CI [lo, hi]). For OpenAI and Anthropic, this is lower than the matched V3 `false_anchor_forced` rates under the preregistered descriptive comparison. This supports the injection-vector account: the prompt schema can cause a model to complete a nonexistent object rather than retrieve real knowledge.

The results memo must include:

> This does not establish whether the false anchor or the task frame is the primary driver — that is the V5 question.

## Claims Not Allowed

- Do not claim premise removal solves hallucination generally.
- Do not claim V4 is a deployable intervention.
- Do not claim users can know which premises are false.
- Do not claim V4 separates the false-anchor effect from the task-frame effect.
- Do not make categorical vendor claims.
- Do not report xAI as part of a matched V3 forced comparison.
- Do not use p-values, McNemar tests, or "significant" language.

## Deviations

Any change after this preregistration commit must be recorded in:

`proofs/DEVIATION_LOG_V4.md`

Deviation entries must be written live, not retrospectively.
