# OSF-Style Preregistration V6: Schema Slot Dose-Response

Date: 2026-05-04
Status: PRE-RUN, LOCK BEFORE MODEL CALLS

## Study Type

Preregistered follow-up to V5C. V6 is designed to move from blog-grade paired
ablation toward paper-grade stress testing.

## Related Work Positioning

Phare V2 (Giskard, December 2025) evaluates model safety across hallucination,
tool use, jailbreaks, and related modules, and includes structured tool-use
settings where missing or extraneous parameters can degrade reliability. V6 is
complementary rather than competing: it tests the additive lever of increasing
named-artifact schema slots in an output schema, not parameter omission in a
tool-use benchmark.

## Research Question

Holding domain, total output-field count, uncertainty instruction, temperature,
and model set fixed, does the hallucination-positive rate increase as the number
of named-artifact schema slots increases?

## Primary Hypothesis

The hallucination-positive rate will increase with named slot count across:

`0, 1, 2, 4, 8`

Primary success requires both:

1. The 8-named-slot condition has a hallucination-positive rate at least 0.15
   higher than the 0-named-slot condition under the dual-judge AND rule.
2. The preregistered Cochran-Armitage trend statistic over named slot count is
   positive and reported with its two-sided p-value.

## Secondary Hypotheses

1. The pooled high-dose conditions (`4` and `8` named slots) will exceed the
   pooled low-dose conditions (`0` and `1` named slots).
2. The 0-named-slot condition will remain low, with Wilson 95% upper bound below
   0.10.
3. Fabricated entities will concentrate in fields whose names directly request
   named artifacts, identifiers, citations, programs, standards, datasets, or
   documents.

## Corpus

`corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl`

The corpus contains:

- 24 fresh anchors.
- 5 conditions per anchor.
- 2 prompt replicates per anchor-condition.
- 240 total prompts.

Every row has:

- `false_anchor_removed: true`
- `task_frame_removed: true`
- `total_format_slots: 8`
- `constant_uncertainty_constraint: true`
- `explicit_named_entity_exclusion: false`

## Models

- OpenAI: `gpt-5-chat-latest`
- Anthropic: `claude-sonnet-4-6`
- xAI: `grok-4.3`

Temperature: `0`

Max tokens: `1800` initially.

Total response calls: `720`.

## Scoring

Dual-judge scoring:

- OpenAI judge: `gpt-5-chat-latest`
- Anthropic judge: `claude-sonnet-4-6`

Primary outcome:

Dual-judge AND-agreement hallucination-positive.

Positive labels:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`

`misrecalled_real_entity` is hallucination-negative and must be reported
separately.

Disagreements must be logged. A human audit may override a disagreement if the
published claim relies on that row or if the disagreement changes the public
claim boundary. Without human override, the preregistered AND-agreement rule
remains the primary analysis.

## Required Analyses

1. Per-dose aggregate rates with Wilson 95% CIs.
2. Per-model per-dose rates with Wilson 95% CIs.
3. Cochran-Armitage trend statistic over named slot count.
4. Per-provider Cochran-Armitage trend tests for `gpt-5-chat-latest`,
   `claude-sonnet-4-6`, and `grok-4.3`. The headline dose-response claim
   requires a positive trend in at least 2 of 3 providers.
5. Prompt-length-as-covariate logistic regression with hallucination-positive
   as the outcome and named slot count plus prompt character length as
   predictors. The dose coefficient must remain positive after controlling for
   length for the dose-response claim to be supported.
6. Fisher exact test for `8` named slots versus `0` named slots.
7. Fisher exact test for pooled high-dose (`4` and `8`) versus pooled low-dose
   (`0` and `1`).
8. Anchor-level sensitivity: collapse the two replicates per anchor-condition
   into an anchor positive if either replicate is AND-positive.
9. Judge agreement summary.
10. Disagreement, misrecall, and positive logs.
11. Provider finish-reason and truncation table.
12. Required human-adjudication disclosure: the V6 results memo must explicitly
    state whether human override was applied to any judge disagreement, and if
    so, how many disagreements and on which rows.

## Falsification / Weakening Conditions

The schema-slot dose-response account is weakened if:

- `8` named slots does not exceed `0` named slots by at least 0.15;
- trend statistic is not positive;
- positives concentrate in one provider only;
- fewer than 50% of anchors show any AND-positive response at the highest dose
  level;
- the 0-named-slot condition exceeds the preregistered low-rate boundary;
- truncation or provider errors are condition-asymmetric.

## Claim Boundaries

V6 results will not be pooled with V5, V5B, or V5C results. V6 uses a generic
8-slot named-field vocabulary distinct from V5/V5C's per-anchor named slots;
pooling would conflate vocabulary regimes.

## Claims Not Allowed

- Do not claim production tool-schema proof.
- Do not claim a universal hallucination mechanism.
- Do not claim named slots always cause fabrication.
- Do not claim the intervention is deployable as-is.
- Do not claim prompt length is perfectly controlled; report observed prompt
  lengths by dose.
- Do not claim sample replicates are fully independent of anchor effects.
- Do not claim V6 isolates slot count from field vocabulary. Each dose level
  introduces new field labels, so the design cannot distinguish "more slots"
  from high-pressure vocabulary entering at higher doses.
- Do not claim a specific functional form, such as linear, log-linear, sigmoid,
  or step. V6 tests monotonic trend, not curve shape.
- Do not claim V6 refutes or replaces V5C's exclusion-clause finding. V6 has no
  exclusion-clause manipulation.
- Do not claim temperature-0 results extend to temperature greater than 0 or to
  nucleus/top-p sampling.
- Do not claim corpus-wide generality if fewer than 50% of anchors show any
  positives at the highest dose level.
