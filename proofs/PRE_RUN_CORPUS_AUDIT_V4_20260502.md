# V4 Pre-Run Corpus Audit

Date: 2026-05-02

## Status

PASS for prompt-format readiness. No model calls authorized by this memo.

## Corpus

`corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`

## Checks

- 12 rows present.
- 12 unique `prompt_id` values.
- 12 unique `anchor_id` values, `VG001` through `VG012`.
- Every row uses `condition=false_anchor_open_structure`.
- Every row uses `provenance=v4_open_structure`.
- Every row has `false_anchor_removed=true`.
- Every row has `expected_behavior=accurate_answer`.
- Every row has a non-empty `expected_real_entities` allowlist for adjudication.
- Every prompt starts with `QUERY {`.
- No prompt body includes `type:`.
- No prompt body includes the distinctive fabricated identifier for its matched V3 anchor:
  - `NARROW-19`
  - `Aquila-7`
  - `frost spectrometer`
  - `HERMES-311`
  - `10b-27`
  - `Borealis Trust Index`
  - `Tallinn-Neva`
  - `SPECTRA-12`
  - `ORCHID-RL`
  - `Oslo Model Audit Compact`
  - `Geneva Automation Memorandum`
  - `VERA-2021-1442`
  - `Adaptive Homework Transparency Act`
- Every row has a non-empty `scoring_note`.
- Every row has a non-empty `design_note`.

## Reproduction Command

```bash
./scripts/validate_corpus_v4.py
```

Expected output:

```text
rows=12
errors=0
status=PASS
```

## Boundary

This audit checks corpus formatting, false-anchor removal, and presence of per-anchor allowlists. It does not verify that every suggested real-world allowlist entity is authoritative. That remains a pre-run human/auditor review item before model calls.
