# Audit Request: V5 Schema-Slot Mechanism Test

Date: 2026-05-03

Please audit V5.

## Primary Question

Did V5 honestly test whether named-entity output schema slots increase
hallucination-positive outputs compared with neutral descriptive schema slots?

## Artifacts

Protocol and preregistration:

- `protocols/V5_PROTOCOL_SCHEMA_SLOT.md`
- `protocols/OSF_PREREG_V5_SCHEMA_SLOT.md`
- `proofs/SHA256_INPUTS_V5.txt`
- `proofs/DEVIATION_LOG_V5.md`

Corpus and validation:

- `corpus/PROMPT_CORPUS_V5_SCHEMA_SLOT.jsonl`
- `scripts/validate_corpus_v5.py`

Runs:

- Original provider run: `runs/hallucination-v5-schema-slot-20260503T065139Z`
- Truncation rerun: `runs/hallucination-v5-truncation-rerun-20260503T072229Z`
- Clean merged scoring dataset: `runs/hallucination-v5-clean-merged-20260503T072553Z`

Scoring:

- `scored/scoring-v5-openai-20260503T072610Z`
- `scored/scoring-v5-anthropic-20260503T072748Z`

Analysis:

- `analysis/analysis-v5-schema-slot-20260503T073722Z`

Memos:

- `proofs/RESULTS_MEMO_V5_SCHEMA_SLOT_20260503.md`
- `proofs/POST_RUN_SELF_AUDIT_V5_20260503.md`

## Checks Requested

1. Verify gate commit order.
2. Verify the V5 corpus really pairs 12 named-slot prompts with 12 neutral prompts.
3. Verify both arms remove false anchors and `type:` task operators.
4. Verify the only intended manipulation is named-entity schema slots.
5. Check whether the neutral arm's explicit `exclude` clause means the
   "only intended manipulation" framing should be narrowed.
6. Verify the D1 truncation rerun and clean merge are correct.
7. Verify dual-judge scoring and the AND-agreement rule.
8. Verify reported rates:
   - named entity schema: `10/36 = 0.278`
   - neutral descriptive schema: `0/36 = 0.000`
   - difference: `0.278`
9. Verify that all 10 positives are in the named-entity schema condition.
10. Verify claim boundaries.

## Claim To Audit

> In a paired 12-domain experiment across OpenAI, Anthropic, and xAI, with false
> anchors and `type:` task frames absent in both arms, named-entity output schema
> slots produced `10/36` AND-agreement hallucination-positive responses, while
> neutral descriptive schema slots produced `0/36`. This supports the claim that
> output schema shape can itself be a hallucination pressure source, while
> leaving the explicit-exclusion-clause confound for follow-up.
