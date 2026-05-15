# Audit Request: V4B Neutral-Schema Rerun

Date: 2026-05-03

Please audit V4B.

## Primary Question

Did V4B honestly correct the V4 schema leak and support the claim that
named-entity output slots were the likely source of the V4 open-structure
hallucinations?

## Artifacts

Preregistration and protocol:

- `protocols/V4B_PROTOCOL_NEUTRAL_SCHEMA_RERUN.md`
- `protocols/OSF_PREREG_V4B_NEUTRAL_SCHEMA.md`
- `proofs/SHA256_INPUTS_V4B.txt`
- `proofs/DEVIATION_LOG_V4B.md`

Corpus and validator:

- `corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl`
- `scripts/validate_corpus_v4b.py`

Run:

- `runs/hallucination-v4b-neutral-schema-20260503T054605Z`

Scoring:

- `scored/scoring-v4b-openai-20260503T055931Z`
- `scored/scoring-v4b-anthropic-20260503T060219Z`
- Failed preserved Anthropic scoring attempts:
  - `scored/scoring-v4b-anthropic-20260503T060020Z`
  - `scored/scoring-v4b-anthropic-20260503T060048Z`

Analysis:

- `analysis/analysis-v4b-neutral-schema-20260503T060618Z`

Memos:

- `proofs/V4_SCHEMA_LEAK_POSTMORTEM_20260503.md`
- `proofs/PRE_RUN_CORPUS_AUDIT_V4B_20260503.md`
- `proofs/RESULTS_MEMO_V4B_NEUTRAL_SCHEMA_20260503.md`
- `proofs/POST_RUN_SELF_AUDIT_V4B_20260503.md`

## Checks Requested

1. Verify gate commit order: preregistration before provider calls.
2. Verify corpus neutrality: no false anchors, no `type:`, no named-entity output slots.
3. Verify run integrity: 36 responses, 0 errors, natural stop/end_turn.
4. Verify scoring integrity: dual judges, 36 rows each, AND-agreement rule.
5. Verify the Anthropic malformed-JSON deviation is fully disclosed and acceptable.
6. Verify the reported result: `0/36`, Wilson 95% CI `[0.000, 0.096]`.
7. Verify the comparison framing against V4's `11/36` named-slot result.

## Claim To Audit

> After V4 showed that named output slots can induce fabricated entities, V4B
> found that a neutral schema without false anchors, task operators, or
> named-entity slots produced `0/36` AND-agreement hallucination-positive
> responses across OpenAI, Anthropic, and xAI frontier models (Wilson 95% CI
> `[0.000, 0.096]`). This supports the schema-slot pressure account.
