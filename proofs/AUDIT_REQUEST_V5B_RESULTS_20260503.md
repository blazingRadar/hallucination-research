# Audit Request: V5B Neutral No-Exclude Follow-Up

Date: 2026-05-03

Please audit V5B.

## Primary Question

Did V5B resolve the V5 explicit-exclusion-clause confound by showing that neutral
descriptive schemas remain low-risk even without `proper_nouns`, `identifiers`,
and `citations` exclusions?

## Artifacts

Protocol/preregistration:

- `protocols/OSF_PREREG_V5B_NEUTRAL_NO_EXCLUDE.md`
- `proofs/SHA256_INPUTS_V5B.txt`
- `proofs/DEVIATION_LOG_V5B.md`

Corpus:

- `corpus/PROMPT_CORPUS_V5B_NEUTRAL_NO_EXCLUDE.jsonl`
- `scripts/validate_corpus_v5b.py`

Runs:

- Original run: `runs/hallucination-v5b-neutral-no-exclude-20260503T074113Z`
- Truncation rerun: `runs/hallucination-v5b-truncation-rerun-20260503T075928Z`
- Clean merged scoring dataset: `runs/hallucination-v5b-clean-merged-20260503T080926Z`

Scoring:

- `scored/scoring-v5b-openai-20260503T080946Z`
- `scored/scoring-v5b-anthropic-20260503T081037Z`

Analysis:

- `analysis/analysis-v5b-neutral-no-exclude-20260503T081453Z`

Memos:

- `proofs/RESULTS_MEMO_V5B_NEUTRAL_NO_EXCLUDE_20260503.md`
- `proofs/POST_RUN_SELF_AUDIT_V5B_20260503.md`

## Checks Requested

1. Verify gate ordering.
2. Verify the corpus has neutral descriptive schemas with no false anchors, no
   `type:`, no named-entity slots, and no explicit named-entity exclusions.
3. Verify timeout/truncation deviations and clean merge.
4. Verify dual-judge scoring.
5. Verify reported result: `0/36`, Wilson 95% CI `[0.000, 0.096]`.
6. Review the single judge disagreement on xAI `VG005_NX`.
7. Verify the comparison against:
   - V5 named schema: `10/36`
   - V5 neutral with exclusions: `0/36`

## Claim To Audit

> V5B found `0/36` AND-agreement hallucination-positive responses for neutral
> descriptive schemas without explicit anti-named-entity exclusions, narrowing
> the V5 caveat and strengthening the schema-slot pressure account.
