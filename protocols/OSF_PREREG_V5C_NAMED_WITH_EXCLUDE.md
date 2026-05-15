# OSF-Style Preregistration V5C: Named Schema With Explicit Exclusions

Date: 2026-05-03

## Study Type

Preregistered missing-cell follow-up before publication.

V5 compared named-entity schema slots against neutral descriptive slots. V5B
showed that neutral descriptive slots remained at 0/36 even when explicit
anti-identifier exclusions were removed. The remaining 2x2 cell is named-entity
schema slots WITH explicit anti-identifier exclusions.

## Question

When output schema fields still request named artifacts, does adding an explicit
`exclude: { proper_nouns, identifiers, citations }` clause suppress the
hallucination-positive rate?

## Corpus

`corpus/PROMPT_CORPUS_V5C_NAMED_WITH_EXCLUDE.jsonl`

The corpus contains 12 prompts, one per V5 anchor:

- false anchor absent
- `type:` task operator absent
- named-entity output slots present
- explicit anti-identifier/proper-noun/citation exclusion present

## Models

- OpenAI: `gpt-5-chat-latest`
- Anthropic: `claude-sonnet-4-6`
- xAI: `grok-4.3`

Temperature: `0`

Total provider calls: `36`

## Scoring

Dual-judge scoring:

- OpenAI judge: `gpt-5-chat-latest`
- Anthropic judge: `claude-sonnet-4-6`

Primary outcome: AND-agreement hallucination-positive.

Disagreements must be logged. A human audit may override a disagreement if the
published claim relies on that row or if the disagreement changes the public
claim boundary. Without human override, the preregistered AND-agreement rule
remains the primary analysis.

Hallucination-positive labels:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`

`misrecalled_real_entity` is hallucination-negative and reported separately.

## Required Analyses

1. Aggregate V5C rate with Wilson 95% CI.
2. Per-model V5C rates with Wilson 95% CIs.
3. Compare V5C against the already-run cells:
   - V5 named-no-exclude: `10/36`
   - V5 neutral-with-exclude: `0/36`
   - V5B neutral-no-exclude: `0/36`
4. Judge agreement summary.
5. Disagreement, misrecall, and positive logs.

## Interpretation Rules

If V5C remains high, the explicit exclusion clause did not suppress named-slot
pressure on this corpus.

If V5C drops near zero, the social posts and LessWrong draft must be revised:
the stronger claim becomes "explicit anti-identifier exclusions can suppress the
named-slot failure mode on this corpus," not "field-label semantics is
independent of the exclusion clause."

If V5C is intermediate, publish the 2x2 as mixed evidence and do not collapse it
into a single headline number.

## Claims Not Allowed

- Do not claim production readiness.
- Do not claim generalization beyond the 12-anchor corpus.
- Do not claim prompt length has been controlled.
- Do not claim dose-response on slot count has been tested.
- Do not claim the explicit exclusion clause is irrelevant until V5C is scored.
