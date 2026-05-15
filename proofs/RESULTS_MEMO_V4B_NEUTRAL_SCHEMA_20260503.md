# V4B Results Memo: Neutral-Schema Rerun

Date: 2026-05-03

## Verdict

V4B clears the preregistered threshold.

The corrected neutral-schema corpus produced:

- AND-agreement hallucination-positive: `0/36`
- Rate: `0.000`
- Wilson 95% CI: `[0.000, 0.096]`
- Threshold: `<= 0.10`

Both judges labeled all 36 responses `accurate_answer`.

## Why V4B Was Needed

V4 removed the fabricated anchors and removed the `type:` task operator, but it
left named-entity output slots such as `study_name`, `rule_identifier`,
`benchmark_name`, and `advisory_id`. Those slots recreated the completion
pressure the experiment was trying to remove.

V4B removed three pressure sources and added one explicit prohibition:

1. fabricated anchor;
2. `type:` task operator;
3. named-entity output slots;
4. explicit exclusions such as `proper_nouns`, `identifiers`, and `citations`.

That fourth change matters for claim boundaries. V4B is a joint-removal result,
not a single-variable isolation of named-slot semantics.

## Run Artifacts

Raw provider run:

`runs/hallucination-v4b-neutral-schema-20260503T054605Z`

Scoring:

- OpenAI judge: `scored/scoring-v4b-openai-20260503T055931Z`
- Anthropic judge: `scored/scoring-v4b-anthropic-20260503T060219Z`

Analysis:

`analysis/analysis-v4b-neutral-schema-20260503T060618Z`

## Run Integrity

- Provider responses: `36/36`
- Provider errors: `0`
- OpenAI model responses: `12/12`
- Anthropic model responses: `12/12`
- xAI model responses: `12/12`
- Finish reasons:
  - OpenAI: `stop` for `12/12`
  - Anthropic: `end_turn` for `12/12`
  - xAI: `stop` for `12/12`
- Temperature: `0`
- Credential values saved: `false`
- Secret scan over V4B run/scoring/analysis artifacts: no API key pattern found

No truncation rerun was needed.

## Results

| Provider | Positive | N | Rate | Wilson 95% CI |
|---|---:|---:|---:|---:|
| Anthropic | 0 | 12 | 0.000 | [0.000, 0.242] |
| OpenAI | 0 | 12 | 0.000 | [0.000, 0.242] |
| xAI | 0 | 12 | 0.000 | [0.000, 0.242] |
| ALL | 0 | 36 | 0.000 | [0.000, 0.096] |

Judge agreement:

- Positive-label agreement: `1.000`
- Primary-label agreement: `1.000`
- Cohen kappa on hallucination-positive boolean: degenerate single-class
  agreement. Both judges labeled every row `accurate_answer`; the analysis
  script reports `1.000` by convention, but this value does not test
  disagreement behavior.
- Disagreements: `0`
- Misrecalled real entities: `0`

## Comparison To V4

V4 named-slot open-structure result:

- `11/36 = 0.306`

V4B neutral-schema result:

- `0/36 = 0.000`

The change between V4 and V4B is not the domain set, not the model set, and not
the absence of the fabricated anchor. V4 had already removed the fabricated
anchor. The material changes are that V4B removed named-entity output slots and
added explicit anti-identifier exclusions.

This supports the schema-slot pressure account:

> Output schemas demanding named artifacts appear to be a load-bearing
> hallucination pressure source in this corpus, but V4B alone does not isolate
> named-slot removal from the explicit exclusion clause.

## Deviations

Two scoring-process deviations were logged:

- D1: Anthropic judge returned malformed JSON on the first scoring attempt at
  batch size 2.
- D2: Anthropic judge still returned malformed JSON at batch size 1, so the
  scorer was narrowly hardened to preserve malformed judge output and retry with
  a valid-JSON repair prompt.

Preserved failed scoring directories:

- `scored/scoring-v4b-anthropic-20260503T060020Z`
- `scored/scoring-v4b-anthropic-20260503T060048Z`

Final Anthropic scoring preserved two parse-failure rows in:

`scored/scoring-v4b-anthropic-20260503T060219Z/judge_parse_failures.jsonl`

The deviations affected judge-output formatting only. They did not change the
corpus, model responses, rubric labels, judge model, or primary AND-agreement
analysis.

## Claim Now Allowed

> On the 12-anchor V3/V4 corpus, replacing named-entity output slots with
> descriptive ones and adding `exclude: proper_nouns, identifiers, citations`
> produced `0/36` AND-agreement positives across OpenAI, Anthropic, and xAI
> frontier models (Wilson 95% CI `[0.000, 0.096]`), contrasting with V4's
> `11/36` named-slot rate. This supports a schema-slot pressure account but does
> not isolate the slot effect from the explicit-prohibition effect, does not
> establish generalization, and does not establish deployability without a
> prompt compiler.

## Claims Still Not Allowed

- Do not claim neutral schemas solve hallucination generally.
- Do not claim premise removal alone is sufficient.
- Do not claim V4B is deployable without a compiler/linter experiment.
- Do not claim task operators are irrelevant; V5 still tests them.
- Do not make categorical vendor claims.
- Do not claim this proves organic user prompts will be safe.
- Do not claim V4B alone isolates named-slot semantics from explicit
  anti-identifier exclusions.

## Next Step

Independent audit should focus on:

1. whether the V4B prompts truly removed named-entity schema pressure;
2. whether the 0/36 AND-agreement result is supported by the raw responses;
3. whether the Anthropic judge JSON retry deviation is acceptable;
4. whether the comparison against V4's 11/36 named-slot result is framed
   honestly.
