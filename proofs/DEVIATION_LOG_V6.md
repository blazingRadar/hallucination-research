# Deviation Log V6

Date opened: 2026-05-04

Protocol:

- `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md`
- `protocols/V6_PROTOCOL_DOSE_RESPONSE.md`

## D0: Pre-Run State

No deviations at preregistration time.

Any corpus edits, provider substitutions, token-cap changes, scoring-rule
changes, reruns, or human adjudication overrides must be logged here at the
moment of decision.

## D1: Pre-Run Audit Tightening

Date: 2026-05-04

Before any model calls, two independent auditors returned `READY_AFTER_FIXES`.
The following editor-only changes were applied:

- added length-as-covariate logistic regression to required analyses;
- added per-provider Cochran-Armitage trend tests;
- added explicit no-pooling boundary for V5/V5B/V5C versus V6;
- added required human-override disclosure in the results memo;
- added field-vocabulary, functional-form, exclusion-clause, temperature, and
  anchor-concentration anti-claims;
- added Phare V2 related-work positioning;
- fixed cosmetic Greek-letter target typos in V6A008-V6A024 and regenerated the
  corpus from `scripts/create_v6_dose_response_corpus.py`.

No model calls had been made before these changes.

## D2: Initial Collection Integrity Repair

Date: 2026-05-04

Initial raw collection run:

- run id: `hallucination-v6-dose-response-20260504T133149Z`
- corpus: `corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl`
- providers: `openai`, `anthropic`, `xai`
- temperature: `0`
- initial max token cap: `1800`

Integrity check before scoring found:

- `714/720` successful raw response rows;
- `6/720` provider errors, all xAI `TimeoutError` rows;
- OpenAI: `240/240` responses, `0` capped rows;
- xAI: `234/240` responses, `0` capped rows, `6` timeout errors;
- Anthropic: `240/240` responses, `232/240` rows stopped at
  `max_tokens`, plus `7/240` empty refusal rows on anchor `V6A020`.

Protocol trigger:

- `protocols/V6_PROTOCOL_DOSE_RESPONSE.md` requires pausing scoring if any
  provider has more than 5% capped/truncated rows.
- Anthropic capped rate was `232/240 = 96.7%`, so scoring is paused.

Repair decision before scoring:

- Preserve the initial run unchanged as the exploratory/raw first pass.
- Rerun only Anthropic rows that stopped at `max_tokens` with a higher token
  cap.
- Rerun only the six xAI timeout rows.
- Build a clean merged response file that substitutes repaired rows for the
  capped Anthropic rows and xAI timeout rows while preserving all original
  natural-stop rows.
- Report the original cap failure, repair run ids, and final stop-reason table
  in the V6 results memo.

No scoring had begun before this deviation was logged.

## D8: Analysis Script Anchor-Level Key Fix

Date: 2026-05-04

After dual-judge scoring completed and before any V6 result was interpreted,
`scripts/analyze_scored_results_v6.py` failed while computing the preregistered
anchor-level sensitivity table. The row-level analysis key was named
`and_hallucination_positive`, while anchor-level rows used
`anchor_condition_positive`.

Decision:

- Add `and_hallucination_positive` as an alias on anchor-level rows, equal to
  `anchor_condition_positive`.
- Do not change raw responses, judge scores, scoring labels, primary
  dose-response calculations, or statistical tests.

No results memo was produced before this fix.

## D9: Analysis Key Fix for Identical Empty-Response Hashes

Date: 2026-05-04

The first V6 analysis run completed but revealed an analysis-key defect before
interpretation: rows were keyed only by `response_hash`. Stable empty Anthropic
refusals share the same empty-string response hash, so multiple refusal rows
were collapsed in the analysis layer and per-dose denominators fell below the
expected `144`.

Decision:

- Replace response-hash-only joins with a composite key:
  `(provider, prompt_id, response_hash)`.
- Keep raw responses and judge score files unchanged.
- Discard the first analysis output as invalid and regenerate the analysis
  after this fix.

No public result interpretation was made before this fix.

## D10: Highest-Dose Anchor Fraction Reporting Fix

Date: 2026-05-04

After the post-D9 analysis regenerated, the result table was inspected before
audit handoff. The script's existing `highest_dose_anchor_positive_fraction`
was computed over anchor-provider rows (`24 anchors x 3 providers = 72`), while
the preregistered weakening condition says "fewer than 50% of anchors show any
AND-positive response at the highest dose level."

Decision:

- Preserve the anchor-provider fraction as a separate diagnostic.
- Add the preregistered anchor-level any-provider fraction:
  `highest_dose_anchor_any_provider_positive_fraction`.
- Add explicit primary claim-check fields for:
  - 8-slot minus 0-slot rate difference versus the `>=0.15` threshold;
  - number of providers with a positive trend versus the `>=2 of 3` headline
    boundary.

No audit handoff or public interpretation had been made before this fix.

## D7: Scorer Manifest V6 Addendum Correction

Date: 2026-05-04

Before scoring, `scripts/adjudicate_scores_v4.py` was checked and found to use
scoring language compatible with open-structure/schema-slot rows, but its
manifest still named `scoring/SCORING_RUBRIC_V4_ADDENDUM.md`.

Decision:

- Update the adjudicator docstring and scoring prompt wording from V4-specific
  to open-structure/schema-slot wording.
- Update the scoring manifest addendum reference to
  `scoring/SCORING_RUBRIC_V6_ADDENDUM.md`.
- Keep labels, positive-label definitions, judge models, response rows, corpus,
  and analysis plan unchanged.

No scoring had begun before this deviation was logged.

## D6: Final Anthropic Residual Repair Outcome

Date: 2026-05-04

Repair run:

- run id: `hallucination-v6-dose-response-20260504T133149Z-repair-anthropic-residual-12000`
- subset: `runs/hallucination-v6-dose-response-20260504T133149Z/repair_inputs/anthropic_residual_subset.jsonl`
- provider: `anthropic`
- max token cap: `12000`
- timeout override: `HALLUCINATION_ANTHROPIC_TIMEOUT=360`

Outcome:

- `3/3` rows collected;
- `V6A010_N1_R1` ended naturally with `end_turn`;
- `V6A010_N1_R2` ended naturally with `end_turn`;
- `V6A020_N0_R1` again returned an empty refusal.

Decision:

- Use the 12000-cap repair rows for `V6A010_N1_R1` and `V6A010_N1_R2`
  in the clean merged dataset.
- Treat `V6A020_N0_R1` as a stable Anthropic refusal, not a truncation
  artifact. It will remain in the merged dataset as a refusal row and be
  disclosed in the finish-reason/refusal table before scoring.

No scoring had begun before this deviation was logged.

## D5: Anthropic 8000-Cap Repair Residual Subset

Date: 2026-05-04

Repair run:

- run id: `hallucination-v6-dose-response-20260504T133149Z-repair-anthropic-8000`
- subset: `runs/hallucination-v6-dose-response-20260504T133149Z/repair_inputs/anthropic_capped_subset.jsonl`
- provider: `anthropic`
- max token cap: `8000`
- timeout override: `HALLUCINATION_ANTHROPIC_TIMEOUT=240`

Integrity check after the 8000-cap repair:

- `232/232` rows collected;
- `229/232` ended naturally with `end_turn`;
- `2/232` still stopped at `max_tokens`;
- `1/232` returned an empty refusal.

Decision:

- Preserve the 8000-cap repair run unchanged.
- Rerun only the three residual rows:
  - `V6A010_N1_R1`
  - `V6A010_N1_R2`
  - `V6A020_N0_R1`
- Use a higher cap for the two capped rows and give the refusal row one clean
  rerun attempt before final merged-dataset construction.

No scoring had begun before this deviation was logged.

## D4: Transport Timeout Override for High-Cap Anthropic Repair

Date: 2026-05-04

The initial runner used fixed provider request timeouts. Because the Anthropic
repair requires a higher token cap than the preregistered first pass, the runner
was updated to allow provider-specific timeout overrides via environment
variables:

- `HALLUCINATION_OPENAI_TIMEOUT`
- `HALLUCINATION_ANTHROPIC_TIMEOUT`
- `HALLUCINATION_XAI_TIMEOUT`
- `HALLUCINATION_QWEN_TIMEOUT`

Decision:

- Use `HALLUCINATION_ANTHROPIC_TIMEOUT=240` for the high-cap Anthropic repair.
- Keep prompts, corpus rows, provider, model, temperature, scoring rubric, and
  analysis plan unchanged.

No scoring had begun before this deviation was logged.

## D3: Anthropic 4000-Cap Repair Stopped

Date: 2026-05-04

Repair run:

- run id: `hallucination-v6-dose-response-20260504T133149Z-repair-anthropic-4000`
- subset: `runs/hallucination-v6-dose-response-20260504T133149Z/repair_inputs/anthropic_capped_subset.jsonl`
- provider: `anthropic`
- max token cap: `4000`

After 7 rows, live metadata showed the 4000-token cap was still insufficient:

- `7/232` rows collected before stopping;
- `4/7` ended naturally with `end_turn`;
- `3/7` still stopped at `max_tokens`.

Decision:

- Stop the 4000-cap repair before completing the full subset because it would
  likely preserve a material truncation problem.
- Preserve the partial repair artifact as an exploratory failed repair.
- Rerun the capped Anthropic subset with a higher cap and a longer provider
  timeout before scoring.

No scoring had begun before this deviation was logged.
