# Audit Request V6 Pre-Run: Schema Slot Dose-Response

Date: 2026-05-04
Status: REQUESTED BEFORE ANY MODEL CALLS

## Audit Scope

Please audit whether V6 is ready to run. No model calls have been made.

## Files To Review

- `corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl`
- `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md`
- `protocols/V6_PROTOCOL_DOSE_RESPONSE.md`
- `scoring/SCORING_RUBRIC_V6_ADDENDUM.md`
- `proofs/DEVIATION_LOG_V6.md`
- `proofs/SHA256_INPUTS_V6.txt`
- `scripts/create_v6_dose_response_corpus.py`
- `scripts/validate_corpus_v6.py`
- `scripts/hash_v6_inputs.sh`
- `scripts/analyze_scored_results_v6.py`

## Checks Requested

1. Does the corpus actually test dose-response over named schema slot count?
2. Are the 24 anchors fresh enough relative to V3-V5C?
3. Do any prompts accidentally introduce false anchors, task frames, or explicit
   anti-identifier exclusions?
4. Are prompt lengths sufficiently controlled for a pre-run design?
5. Is the `do_not_invent` / uncertainty constraint appropriate, or does it
   obscure the mechanism under test?
6. Are two replicates per anchor-condition worth the 720 response calls, or
   should V6 reduce scope before running?
7. Are the primary hypothesis, falsification rules, and required analyses clear?
8. Does the scoring rubric avoid counting real-entity misrecall as fabrication?
9. Are the stop conditions sufficient for truncation/provider asymmetry?
10. Is this ready to run, or should the corpus/protocol be fixed first?

## Current Validator Output

`python3 scripts/validate_corpus_v6.py` reports:

- rows: 240
- anchors: 24
- conditions: 48 rows each for 0, 1, 2, 4, and 8 named slots
- prompt-length means by named count after the pre-run typo cleanup: 358.6,
  364.6, 366.6, 370.6, 372.6
- warnings: 0
- errors: 0
- status: PASS

## Non-Negotiable Gate

Do not run V6 until this pre-run audit returns `READY` or
`READY_AFTER_FIXES` and the named fixes are committed.
