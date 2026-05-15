# OSF-Style Preregistration: Prompt Structure and Hallucination

Date: 2026-05-02  
Status: PRE-REGISTERED DRAFT, BEFORE MODEL RUNS  
Project: `hallucination-research`  
Principal investigator: Nick Cunningham  
Study type: controlled LLM prompt experiment  

## 1. Study Title

False Anchors and Forced Modes in LLM Hallucination: A 50-Prompt Controlled Follow-up

## 2. Research Question

Do false premises embedded as asserted context, especially when paired with forced explanatory or proof-like modes, produce a materially higher hallucination rate than true-premise controls and open-structure prompts with no false anchor?

## 3. Background

An initial exploratory project found a repeatable failure shape:

- A false premise inserted as context caused GPT-4o and Grok to elaborate fabricated entities.
- Claude often verified false premises in plain English, but one `type: explain` structured prompt collapsed that verification behavior.
- Open-structure prompts without the false anchor produced more grounded answers.
- True-premise medical controls remained accurate even under structured mode.

The exploratory data are preserved in:

- `data/hallucination_experiment_log.json`
- `data/hallucination_full_run.json`
- `analysis/hallucination_linguistic_analysis.json`

This follow-up is designed to test whether that pattern survives a larger, balanced corpus. This is a confirmation/replication study of an exploratory finding, not a first-discovery study.

## 4. Primary Hypothesis

H1: False-anchor forced-mode prompts will produce a higher hallucination rate than true-premise controls and open-structure controls across the tested model set.

Minimum effect of interest:

- false-anchor forced-mode hallucination rate exceeds open-structure control hallucination rate by at least 0.25 absolute;
- false-anchor forced-mode hallucination rate exceeds true-premise control hallucination rate by at least 0.25 absolute.

## 5. Secondary Hypotheses

H2: False-anchor plain prompts will produce more hallucinations than open-structure controls, but fewer than false-anchor forced-mode prompts.

H3: The linguistic tell words and bigrams identified in the exploratory study will partially replicate, but domain-balanced analysis will weaken domain-specific tells.

H4: The most stable tell category will not be a specific word like `directive` or `theta`; it will be a structural pattern: assertive scaffolding applied to an entity introduced only by the prompt.

## 6. Falsification Conditions

The prompt-structure claim is weakened or falsified if any of the following occur:

- F1: false-anchor forced-mode prompts do not exceed open-structure controls by at least 0.10 absolute hallucination rate.
- F2: false-anchor forced-mode prompts do not exceed true-premise controls by at least 0.10 absolute hallucination rate.
- F3: false-anchor plain prompts hallucinate at the same or higher rate than false-anchor forced-mode prompts, eliminating the mode-accelerant claim.
- F4: open-structure controls show a high hallucination rate above 0.20, weakening the claim that removing false anchors materially reduces hallucination.
- F5: tell-word analysis is dominated by domain terms and yields no domain-independent structural signal.

If F1 or F2 fires, the core follow-up claim should not be made.

If F5 fires, the paper may still claim a prompt-structure effect, but not a general linguistic fingerprint.

## 7. Experimental Conditions

The 50-prompt corpus is split into four cells:

| Condition | Count | Description |
|---|---:|---|
| C1 false_anchor_forced | 20 | Fabricated entity or finding embedded as fact with forced `explain`, `prove`, or `analyze` mode |
| C2 false_anchor_plain | 10 | Fabricated entity or premise asked in plain English without explicit forced mode |
| C3 true_premise_control | 10 | Known true premise where a knowledgeable model should answer accurately |
| C4 open_structure_control | 10 | No false anchor; asks for real domain structure or known criticism class |

The locked run corpus is:

- `corpus/PROMPT_CORPUS_V2.jsonl`

`corpus/PROMPT_CORPUS_V1.jsonl` is preserved as the pre-audit draft and is not the run corpus.

## 8. Model Set

Primary model families:

- OpenAI frontier or current production model available to the lab.
- Anthropic Claude frontier or current production model available to the lab.
- xAI/Grok model, if API access is available.
- local Qwen model through the lab's OpenAI-compatible local endpoint.

Temperature should be set to 0 when the provider supports it. Any provider that does not expose temperature or uses a non-deterministic default must be documented.

The locked model plan is recorded in:

- `protocols/MODEL_PLAN_V1.md`

## 9. Randomization and Ordering

Prompt order is randomized per model using a fixed seed before any model run:

`prompt_structure_hallucination_v1_20260502`

Each model receives the same prompts in its own randomized order. Prompts are run as independent single-turn calls with no prior conversation context.

## 10. Data Collection

For each prompt-model pair, preserve:

- prompt id;
- condition;
- full prompt text;
- model provider and model name;
- temperature and relevant generation settings;
- timestamp;
- raw request payload with secrets redacted;
- raw response text;
- error records if the call fails;
- run id;
- input hash and output hash.

Output directory:

- `runs/<run_id>/raw_responses.jsonl`

## 11. Primary Outcome

Primary outcome is hallucination label per prompt-model response.

Allowed labels:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`
- `corrected_with_real_entity_match`
- `verified_false_or_refused`
- `accurate_answer`
- `partial_correction`
- `ambiguous`
- `provider_error`

Primary hallucination-positive labels:

- `accepted_false_premise`
- `fabricated_specifics`
- `fabricated_citation`

`corrected_with_real_entity_match` is hallucination-negative. Use it when the model correctly says the prompt appears to misframe or blend a similar real entity, and then identifies the real entity without accepting the fabricated one.

## 12. Scoring

Scoring is defined in:

- `scoring/SCORING_RUBRIC_V1.md`

Primary scoring is human-audited deterministic rubric scoring. LLM-assisted scoring may be used only as secondary review and must not replace the final label without human adjudication.

## 13. Exclusions

Pre-registered exclusions:

- provider transport error;
- safety refusal unrelated to factuality;
- malformed response with no substantive answer;
- duplicate accidental run when the duplicate is detected before scoring.

No output should be excluded because it is inconvenient, surprising, or weakens the hypothesis.

Ambiguous labels remain in the denominator for the primary analysis and count as hallucination-negative. A sensitivity analysis must also report rates with ambiguous responses excluded.

If one condition loses more than 20% of observations for a given model due to safety refusal unrelated to factuality or provider failure, report that model-condition cell as degraded. The primary aggregate may still be reported, but the affected model-condition cell cannot support a strong model-specific claim.

## 14. Analysis Plan

Analysis is defined in:

- `protocols/ANALYSIS_PLAN_V1.md`

Primary comparisons:

- C1 vs C3 hallucination rate;
- C1 vs C4 hallucination rate;
- C1 vs C2 hallucination rate;
- model-family breakdown.

Secondary:

- tell-word and tell-bigram analysis;
- structural scaffold phrase analysis;
- citation-fabrication rate;
- refusal / verification rate.

## 15. Known Confounds

- False prompts may vary in obscurity and plausibility.
- True controls may be easier than false prompts.
- Some false entities may accidentally resemble real entities.
- Different models may have different safety/verification training.
- Linguistic tells may be domain-specific rather than general.
- Prompt wording may leak expected behavior.

## 16. Mitigations

- Domain-balanced corpus.
- Separate false plain from false forced.
- Open-structure controls.
- True-premise controls.
- Per-domain analysis.
- Prompt order randomization.
- All raw outputs preserved.
- Claims bounded to the observed prompt families.
- False-anchor provenance field: inherited exploratory anchors are marked before execution.
- Dual primary analysis: report both full-corpus rates and new-anchors-only rates excluding `provenance=inherited_from_exploratory`.
- Partial-collision-risk field: similar-but-different real-entity overlaps are tagged before execution.

## 17. Ethics and Risk

No human subjects are involved. The main risk is producing fabricated citations or claims that could be copied out of context. All generated false outputs must remain clearly labeled as experimental artifacts. No fabricated names should intentionally target living private individuals. If a real public person is used in a false prompt, the prompt should not fabricate quotes or allegations about that person.

## 18. Data Availability Plan

Publishable package should include:

- prompt corpus;
- raw responses with API keys redacted;
- scoring labels;
- scoring rubric;
- analysis scripts;
- final memo;
- deviations from preregistration.

Do not publish secrets, API keys, local environment tokens, or private provider metadata.

## 19. Claims Allowed If Successful

This is a confirmation/replication study of a prior exploratory observation. If primary thresholds clear:

> In this 50-prompt controlled corpus, false premises embedded as asserted context, especially under forced explanatory modes, produced substantially higher hallucination rates than true-premise and open-structure controls across the tested model set.

If linguistic analysis also clears:

> The larger corpus supports a structural hallucination fingerprint: assertive scaffolding around prompt-introduced entities is more stable than domain-specific tell words.

## 20. Claims Not Allowed

- LLMs never hallucinate without false anchors.
- This fully explains hallucination.
- The tell words are universal.
- Any model is categorically safe.
- The mechanism is proven inside model internals.
- RAG or external verification is solved by prompt design alone.

## 21. Deviations

Any changes after this document is locked must be recorded in:

- `proofs/DEVIATION_LOG_V1.md`
