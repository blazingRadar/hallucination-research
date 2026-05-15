# AsPredicted-Style Summary

Date: 2026-05-02  
Project: Hallucination Prompt-Structure Lab

## 1. What is the main question?

Do false premises embedded as asserted context, especially when paired with forced explanatory modes, produce more hallucinations than open-structure or true-premise prompts?

## 2. What are the hypotheses?

Primary: false-anchor forced-mode prompts will produce a materially higher hallucination rate than true-premise controls and open-structure controls.

Secondary: false-anchor plain prompts will produce more hallucinations than open-structure controls, but fewer than false-anchor forced-mode prompts.

Secondary: domain-independent structural tells will be more stable than domain-specific tell words.

## 3. What are the conditions?

- C1: false anchor + forced mode, n=20
- C2: false anchor + plain English, n=10
- C3: true premise control, n=10
- C4: open-structure control, n=10

Each prompt is sent independently to each model.

## 4. What are the outcome measures?

Primary: hallucination label per response.

Hallucination-positive labels:

- accepted false premise;
- fabricated specifics;
- fabricated citation.

Control-success labels:

- accurate answer;
- verified false or refused;
- corrected with real entity match;
- partial correction.

## 5. How many observations?

Prompt count: 50.

With four model families: 200 model responses.

The fourth model family is local Qwen. If Qwen is unavailable, the deviation must be recorded before running.

## 6. What are the exclusion rules?

Exclude only:

- provider transport errors;
- malformed empty responses;
- safety refusals unrelated to factuality;
- accidental duplicate calls detected before scoring.

Do not exclude surprising or hypothesis-breaking responses.

Ambiguous responses stay in the primary denominator as hallucination-negative and are excluded in a sensitivity analysis.

If one model-condition cell loses more than 20% of observations to provider failure or safety refusal unrelated to factuality, report that cell as degraded.

## 7. What analysis will be run?

Compute hallucination rates by condition and model family.

Primary comparisons:

- C1 vs C3;
- C1 vs C4;
- C1 vs C2.

Run each primary comparison on both:

- full corpus;
- new-anchors-only subset excluding inherited exploratory anchors.

Then run domain-balanced linguistic analysis:

- word ratios;
- bigram ratios;
- structural scaffold phrases;
- citation-fabrication markers.

## 8. What would falsify the claim?

The claim is weakened if false-anchor forced prompts do not produce meaningfully higher hallucination rates than true-premise or open-structure controls.

The linguistic-fingerprint claim is weakened if tell words are dominated by domain-specific terms and no structural pattern survives.
