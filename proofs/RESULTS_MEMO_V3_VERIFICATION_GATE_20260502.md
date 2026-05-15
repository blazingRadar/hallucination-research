# V3 Verification Gate Results Memo

Date: 2026-05-02

## Status

PASS against preregistered practical thresholds, pending independent audit of labels and analysis.

## Question

V2 showed a narrower pattern than the original broad hypothesis: OpenAI was vulnerable to false-anchor prompting, Claude was mostly robust, xAI was mixed, and Qwen was degraded by truncation.

V3 tested whether adding an explicit verification gate reduces OpenAI's false-anchor hallucination rate without damaging verified-control usefulness.

## Gate Timeline

- Gate commit: `8772de0 Pre-register V3 verification-gate follow-up`
- Raw run: `runs/hallucination-v3-verification-gate-20260502T173643Z`
- Truncation rerun: `runs/hallucination-v3-truncated-rerun-20260502T174737Z`
- Clean merged run: `runs/hallucination-v3-clean-merged-20260502T174849Z`
- Scoring run: `scored/scoring-v3-verification-gate-20260502T174905Z`
- Final analysis: `analysis/analysis-v3-verification-gate-fixed-20260502T175120Z`

## Run Integrity

- Raw collection: 84/84 responses, 0 provider errors.
- Providers: OpenAI 42, Anthropic 42.
- Corpus: `corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl`.
- Prompt counts: 12 forced false-anchor, 12 plain false-anchor, 12 verification-gate false-anchor, 6 verified controls per provider.
- Original truncation issue: 2/12 Anthropic forced-condition rows hit `max_tokens` at 1400.
- D1 reran only those two rows at `max_tokens=4000`; both completed with `finish_reason=end_turn`.
- Clean merged dataset: 84 rows, 2 replacements, 0 errors; all OpenAI rows ended `stop`, all Anthropic rows ended `end_turn`.
- Secret scan over V3 run artifacts found no API key patterns.

## Deviations

- D1: Claude false-anchor forced truncation rerun before scoring.
- D2: analysis grouping patch for null `anchor_id` on verified controls.
- D3: verified-control usefulness calculation patch.

All deviations are recorded in `proofs/DEVIATION_LOG_V3.md`.

## Primary Rates

| Provider | Forced | Plain | Verify Gate | Forced - Verify | Control Useful | Control Failure |
|---|---:|---:|---:|---:|---:|---:|
| OpenAI | 8/12 = 0.667 | 5/12 = 0.417 | 0/12 = 0.000 | 0.667 | 6/6 = 1.000 | 0/6 = 0.000 |
| Anthropic | 0/12 = 0.000 | 1/12 = 0.083 | 0/12 = 0.000 | 0.000 | 6/6 = 1.000 | 0/6 = 0.000 |

## Threshold Assessment

Preregistered practical success criteria:

- OpenAI forced-minus-verify reduction >= 0.30: PASS, observed 0.667.
- OpenAI verify-gate hallucination rate <= 0.20: PASS, observed 0.000.
- OpenAI verified-control usefulness >= 0.80: PASS, observed 1.000.
- Claude remains <= 0.10 hallucination-positive in all false-anchor conditions: PASS, max observed 0.083.

Overall threshold result: PASS.

## Label Pattern

OpenAI:

- Forced: 8 hallucination-positive, 4 partial corrections.
- Plain: 5 hallucination-positive, 4 corrected-with-real-entity, 2 verified false/refused, 1 partial correction.
- Verify gate: 0 hallucination-positive; 8 verified false/refused, 4 corrected-with-real-entity.
- Controls: 6 accurate answers.

Anthropic:

- Forced: 0 hallucination-positive; mostly verified false/refused or corrected-with-real-entity.
- Plain: 1 hallucination-positive.
- Verify gate: 0 hallucination-positive; 12 verified false/refused.
- Controls: 6 accurate answers.

## Supported Claim

In a held-out OpenAI-vs-Claude follow-up, explicit verification instructions reduced OpenAI's false-anchor hallucination-positive rate from 8/12 in the forced condition and 5/12 in the plain condition to 0/12 in the verification-gate condition, while preserving 6/6 verified-control usefulness. Claude stayed at or below 1/12 hallucination-positive across all false-anchor conditions.

## Claims Not Allowed

- Do not claim verification gates solve hallucination generally.
- Do not claim this transfers to all models or all domains.
- Do not claim the labels are final before independent audit.
- Do not claim tell-word detection is solved by this run.
- Do not claim the effect is only from verification semantics; the verify-gate prompts are also longer and more explicit than plain prompts.

## Next Follow-Up Worth Considering

The main follow-up is a tighter intervention split:

1. `plain`
2. `same_length_filler`
3. `verify_gate`

That would test whether the V3 effect comes from verification instruction specifically or from added prompt length / caution framing.
