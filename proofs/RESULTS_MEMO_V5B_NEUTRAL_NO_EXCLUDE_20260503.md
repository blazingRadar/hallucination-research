# V5B Results Memo: Neutral Schema Without Explicit Exclusions

Date: 2026-05-03

## Verdict

V5B clears the preregistered threshold and addresses the main V4B/V5 confound.

Neutral descriptive schemas stayed at the floor even after removing the explicit
`proper_nouns`, `identifiers`, `citations`, and similar exclusions.

## Primary Result

Neutral descriptive schema without explicit named-entity exclusions:

- AND-agreement hallucination-positive: `0/36`
- Rate: `0.000`
- Wilson 95% CI: `[0.000, 0.096]`
- Threshold: `<= 0.10`

Per provider:

- OpenAI: `0/12`
- Anthropic: `0/12`
- xAI: `0/12`

## Comparison

| Condition | Positive | N | Rate |
|---|---:|---:|---:|
| V5 named-entity schema | 10 | 36 | 0.278 |
| V5 neutral schema with explicit exclusions | 0 | 36 | 0.000 |
| V5B neutral schema without explicit exclusions | 0 | 36 | 0.000 |

This narrows the V5 caveat. The explicit exclusion clause was not necessary for
the neutral descriptive schema to stay at floor on this corpus.

## What This Means

The result strengthens the schema-slot pressure account:

> The risky feature is not merely absence or presence of an explicit
> anti-fabrication instruction. On this corpus, descriptive schemas stayed low
> even without that instruction, while named-entity schemas produced positives.

## Run Integrity

Initial provider run:

`runs/hallucination-v5b-neutral-no-exclude-20260503T074113Z`

The initial run produced one xAI timeout and five Anthropic truncations. These
were logged in `proofs/DEVIATION_LOG_V5B.md`.

Corrections:

- xAI timeout row retried with `--resume`.
- Five Anthropic truncated rows rerun at `max_tokens=6000`.
- One long Anthropic replacement row required extended API timeout.

Primary scoring dataset:

`runs/hallucination-v5b-clean-merged-20260503T080926Z`

Clean merged dataset:

- Rows: `36`
- Replacement rows: `5`
- Final finish reasons:
  - OpenAI: `stop` for `12/12`
  - Anthropic: `end_turn` for `12/12`
  - xAI: `stop` for `12/12`

The merged errors file preserves the original timeout attempts; the primary raw
response dataset has complete replacement rows.

## Scoring Integrity

Scoring:

- OpenAI judge: `scored/scoring-v5b-openai-20260503T080946Z`
- Anthropic judge: `scored/scoring-v5b-anthropic-20260503T081037Z`

Judge agreement:

- Positive-label agreement: `0.972`
- Primary-label agreement: `0.972`
- Disagreements: `1`

The single disagreement was xAI `VG005_NX`. Anthropic judge marked fabricated
specifics because the response included unsupported quantitative claims
(`15-25% drops`), while OpenAI judge marked it accurate. Under the preregistered
AND-agreement rule, this row is hallucination-negative but should be reviewed by
auditors.

The V5B prereg omitted the human-adjudication-on-disagreement clause that V4B
had restored after the V3 audit. This regression is now logged in
`proofs/DEVIATION_LOG_V5B.md`; no labels were retroactively changed.

## Claim Now Allowed

> In the V5B follow-up, neutral descriptive schemas without explicit
> anti-proper-noun/identifier/citation exclusions produced `0/36`
> AND-agreement hallucination-positive responses. Compared with V5's `10/36`
> named-entity schema result, this supports the claim that named-entity schema
> slots, not merely absence of an explicit exclusion clause, are a load-bearing
> hallucination pressure source on this corpus.

## Claims Still Not Allowed

- Do not claim all named-entity slots are unsafe.
- Do not claim all neutral descriptive schemas are safe.
- Do not claim this generalizes beyond this corpus.
- Do not claim production readiness without a compiler/linter experiment.
- Do not claim there is no residual risk of unsupported quantitative claims;
  the single judge disagreement points directly at that boundary.
- Do not hide the V5B human-adjudication-clause regression; it is part of the
  audit trail.
