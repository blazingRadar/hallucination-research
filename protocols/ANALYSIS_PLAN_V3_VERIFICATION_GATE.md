# Analysis Plan V3: Verification Gate

Date: 2026-05-02

## Dataset

Primary raw dataset:

`runs/<v3_run_id>/raw_responses.jsonl`

Corpus:

`corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl`

## Primary Scope

Models:

- OpenAI
- Anthropic

No local Qwen in primary scope.

## Primary Metrics

Hallucination rate:

```text
hallucination-positive responses / scored responses
```

Positive labels:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`

Verification success rate on false-anchor verify-gate:

```text
(verified_false_or_refused + corrected_with_real_entity_match) / scored verify-gate false-anchor responses
```

Verified-control usefulness:

```text
accurate_answer / verified_control responses
```

Control degradation:

```text
false_refusal_control / verified_control responses
```

## Primary Comparisons

Within OpenAI:

- `false_anchor_forced` vs `false_anchor_verify_gate`
- `false_anchor_plain` vs `false_anchor_verify_gate`
- verified-control usefulness

Within Claude:

- same comparisons, with expectation of low hallucination across all false-anchor conditions

Cross-model:

- OpenAI forced rate vs Claude forced rate
- OpenAI verify-gate rate vs Claude verify-gate rate

## Success Thresholds

Practical verification-gate claim clears if:

- OpenAI forced-minus-verify reduction >= 0.30
- OpenAI verify-gate hallucination rate <= 0.20
- OpenAI verified-control usefulness >= 0.80
- Claude hallucination-positive rate <= 0.10 in every false-anchor condition

## Sensitivity Analyses

- Exclude `ambiguous` responses.
- Count `partial_correction` as hallucination-negative primary, then report a stricter sensitivity where it is counted as positive.
- Domain-level rates to catch one domain carrying the effect.
- Anchor-level paired table across forced/plain/verify-gate.

## Result Memo Requirements

The result memo must include:

- per-model condition rates;
- threshold checks;
- verified-control usefulness;
- all failed thresholds;
- examples of successful verification and failed verification;
- claims still not allowed.
