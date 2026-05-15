# Data Dictionary V1

Date: 2026-05-02

## `corpus/PROMPT_CORPUS_V2.jsonl`

Each line is one prompt object.

`corpus/PROMPT_CORPUS_V1.jsonl` is preserved as the pre-audit draft and is not used for the run.

### Fields

`prompt_id`

- Stable unique id.
- Prefixes:
  - `HF`: hallucination-pressure false-anchor forced-mode
  - `HP`: hallucination-pressure false-anchor plain
  - `HT`: true-premise control
  - `HO`: open-structure control

`condition`

- One of:
  - `false_anchor_forced`
  - `false_anchor_plain`
  - `true_premise_control`
  - `open_structure_control`

`domain`

- Broad subject area used for balance and subgroup analysis.

`expected_behavior`

- Pre-run expected behavior class.
- This is not the observed model label.

`false_anchor`

- The fabricated entity or premise for false-anchor conditions.
- Must be `null` for controls.

`prompt`

- Exact text sent to the model.

`scoring_note`

- Human-readable scoring guidance.

`provenance`

- For false-anchor rows, one of:
  - `inherited_from_exploratory`
  - `new_for_followup`
  - `new_for_followup_after_pre_run_audit`
- For controls: `control_new_for_followup`.

`partial_collision_risk`

- Boolean flag for false anchors that intentionally remain in the corpus but overlap with a similar real entity or literature cluster.

`partial_collision_note`

- Human-readable note naming the overlap.
- `null` when no specific partial-collision risk is tagged.

## Future `runs/<run_id>/raw_responses.jsonl`

Each line should contain one model response.

Required fields:

- `run_id`
- `prompt_id`
- `condition`
- `domain`
- `provider`
- `model`
- `model_version_returned`
- `temperature`
- `timestamp_utc`
- `request_hash`
- `response_hash`
- `prompt`
- `response_text`
- `error`

## Future `runs/<run_id>/scored_responses.jsonl`

Each line should contain one scored response.

Required fields:

- `run_id`
- `prompt_id`
- `provider`
- `model`
- `primary_label`
- `secondary_labels`
- `hallucination_positive`
- `quote_evidence`
- `scorer_note`
- `scorer_confidence`
