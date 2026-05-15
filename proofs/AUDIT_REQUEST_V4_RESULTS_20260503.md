# Audit Request: V4 Open-Structure Results

Date: 2026-05-03

## Requested Verdict

Please audit whether V4's failed replication result is correctly scored and whether the revised claim boundary is honest.

## Files To Review First

- `protocols/OSF_PREREG_V4_OPEN_STRUCTURE.md`
- `protocols/V4_PROTOCOL_OPEN_STRUCTURE_REPLICATION.md`
- `corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`
- `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
- `scoring/SCORING_RUBRIC_V4_ADDENDUM.md`
- `proofs/DEVIATION_LOG_V4.md`
- `runs/hallucination-v4-clean-merged-20260503T034907Z/run_manifest.json`
- `runs/hallucination-v4-clean-merged-20260503T034907Z/replacement_map.json`
- `scored/scoring-v4-openai-20260503T035213Z/adjudicated_scores.jsonl`
- `scored/scoring-v4-anthropic-20260503T035315Z/adjudicated_scores.jsonl`
- `analysis/analysis-v4-open-structure-20260503T035844Z/analysis_summary.json`
- `analysis/analysis-v4-open-structure-20260503T035844Z/confabulation_log.jsonl`
- `proofs/RESULTS_MEMO_V4_OPEN_STRUCTURE_20260503.md`
- `proofs/POST_RUN_SELF_AUDIT_V4_20260503.md`

## Specific Audit Questions

1. Are the 11 AND-agreement hallucination-positive labels valid?
2. Are any labels better scored as `misrecalled_real_entity` rather than `fabricated_specifics`?
3. Did the expected-real-entities allowlists bias the judges too strictly?
4. Was D1 truncation handling clean?
5. Was D2, adding V4 scoring/analysis scripts before scoring, acceptable?
6. Is the corrected supported claim properly bounded?
7. Should V5 test schema-slot pressure in addition to task-operator pressure?

## Current Supported Claim Under Audit

> Removing the specific fabricated anchor and `type:` operator was not sufficient to eliminate hallucination in the structured open-query setting. When the output schema still requested named entities, all three frontier models produced fabricated named entities at nontrivial rates. This refines the injection-vector account: hallucination pressure can come not only from a false premise, but also from schema slots that invite named-entity completion.
