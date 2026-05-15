# V4B Pre-Run Corpus Audit

Date: 2026-05-03

## Status

PASS for corrected neutral-schema prompt readiness. No model calls authorized by this memo.

## Corpus

`corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl`

## Why This Corpus Exists

V4 removed the fabricated anchors and `type:` operator but left named-entity output slots in the schema. Those slots triggered fabrication. V4B corrects that leak.

## Checks

- 12 rows present.
- 12 unique `prompt_id` values.
- 12 anchor domains preserved from V3/V4.
- Every row uses `condition=false_anchor_open_structure_neutral_schema`.
- Every row uses `provenance=v4b_neutral_schema`.
- Every row has `false_anchor_removed=true`.
- Every row has `task_frame_removed=true`.
- Every row has `named_entity_slots_removed=true`.
- Every prompt starts with `QUERY {`.
- No prompt body includes `type:`.
- No prompt body includes the distinctive fabricated identifier for its matched anchor.
- No prompt body includes forbidden named-entity schema fields such as:
  - `study_name`
  - `rule_identifier`
  - `benchmark_name`
  - `advisory_id`
  - `statute_name`
  - `framework_name`
  - `mission_name`
  - `document_name`
  - `standard_name`
  - `score_name`
  - `cve_number`
  - `bill_number`
- Every row has a non-empty `scoring_note`.
- Every row has a non-empty `design_note`.

## Reproduction Command

```bash
./scripts/validate_corpus_v4b.py
```

Observed:

```text
rows=12
errors=0
status=PASS
```

## Boundary

This audit verifies schema neutrality and formatting. It does not authorize a model run. The next required step is a V4B preregistration gate commit.
