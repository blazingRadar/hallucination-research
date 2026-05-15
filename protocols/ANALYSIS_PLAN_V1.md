# Analysis Plan V1

Date: 2026-05-02

## Primary Dataset

`runs/<run_id>/raw_responses.jsonl` scored against `corpus/PROMPT_CORPUS_V2.jsonl`.

## Primary Metrics

Hallucination rate by condition:

```text
# hallucination-positive responses / # scored responses
```

Hallucination-positive labels:

- accepted_false_premise
- fabricated_specifics
- fabricated_citation

Hallucination-negative labels include:

- corrected_with_real_entity_match
- verified_false_or_refused
- accurate_answer

`ambiguous` is hallucination-negative for the primary analysis and excluded in a sensitivity analysis.

## Primary Comparisons

1. C1 false_anchor_forced vs C3 true_premise_control.
2. C1 false_anchor_forced vs C4 open_structure_control.
3. C1 false_anchor_forced vs C2 false_anchor_plain.

Each primary comparison is reported twice:

1. full corpus;
2. new-anchors-only subset excluding rows with `provenance=inherited_from_exploratory`.

## Secondary Metrics

- verification/refusal rate;
- partial-correction rate;
- corrected-real-entity-match rate;
- ambiguous rate;
- safety-refusal / provider-loss rate by model-condition cell;
- fabricated-citation rate;
- model-family hallucination rate;
- domain-level hallucination rate;
- condition × model interaction.

## Linguistic Analysis

Run word and bigram discrimination ratios, but report two layers separately:

1. domain-specific tokens;
2. structural scaffolding tokens.

Structural patterns of interest:

- `the study`;
- `the directive`;
- `the report`;
- `supporting evidence`;
- `the finding`;
- `according to the`;
- citation-like identifiers not present in the prompt;
- certainty scores assigned to prompt-introduced false entities.

## Success Criteria

Primary claim clears if:

- C1 hallucination rate exceeds C3 by >= 0.25 absolute;
- C1 hallucination rate exceeds C4 by >= 0.25 absolute.

Mode-accelerant claim clears if:

- C1 exceeds C2 by >= 0.10 absolute.

Linguistic-fingerprint claim clears only if structural scaffold patterns survive domain filtering.

## Reporting

The result memo must include:

- all condition rates;
- per-model rates;
- per-domain rates;
- all falsification checks;
- examples of theory-confirming and theory-breaking cases;
- claims still not allowed.

## Refusal and Loss Rule

If a model-condition cell loses more than 20% of observations to provider failure or safety refusal unrelated to factuality, mark that cell degraded. Do not make a strong model-specific claim from that cell. Preserve the data and report the degraded cell instead of rerunning until it behaves.
