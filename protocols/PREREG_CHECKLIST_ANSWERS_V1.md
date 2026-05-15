# Prereg Checklist Answers

Date: 2026-05-02  
Purpose: answer the 22 preregistration stress-test questions before running the follow-up experiment.

## 1. Bacon: systematic observation or cherry-picking?

Systematic. The follow-up uses a 50-prompt corpus split across four predefined conditions. Every prompt-model response is preserved, including refusals and nulls.

## 2. Bacon: fixed data collection procedure?

Yes. Each prompt is sent as a single-turn call with no conversation memory. Prompt order is randomized with a fixed seed before runs.

## 3. Descartes: assumptions that could invalidate the conclusion?

- The false prompts might be more obscure than controls.
- The control prompts might be easier.
- Scorers might label refusals too generously.
- The prompts may leak expected behavior.
- Tell words may be domain artifacts.

## 4. Hume: mechanism or correlation?

The proposed mechanism is context activation: asserted false premises activate pattern completion around fictional entities. This is a behavioral mechanism, not an internal mechanistic proof.

## 5. Hume: generalization beyond population/task/environment?

Only bounded generalization is allowed: tested models, tested prompt classes, tested domains. No universal hallucination claim.

## 6. Mill: vary one thing and hold rest constant?

The design varies premise truth and mode forcing while holding prompt family, single-turn execution, model settings, and scoring constant as much as possible.

## 7. Mill: control condition?

Two controls:

- true-premise controls;
- open-structure controls with no false anchor.

They isolate hallucination pressure from generic task difficulty.

## 8. Chamberlin: competing explanations?

Competing explanations:

- false prompts are just harder;
- models refuse based on safety training, not verification;
- domain familiarity drives results;
- forced mode changes verbosity, not hallucination;
- scorer bias creates the effect.

The design tests these through controls, domain balance, and explicit labels.

## 9. Peirce: hypothesis before data?

The hypothesis came from exploratory data. This follow-up is confirmatory only if the corpus and scoring are locked before new model runs. The exploratory origin must remain disclosed.

## 10. Fisher: randomization?

Prompt order is randomized per model using a fixed seed. Assignment to condition is not random after corpus design because conditions are constructed intentionally.

## 11. Popper: what would make the hypothesis wrong?

If false-anchor forced-mode prompts do not hallucinate materially more than true-premise or open-structure controls, the central claim fails.

## 12. Popper: is the falsification bar hard enough?

Yes. The minimum effect threshold is absolute-rate based, not merely directional.

## 13. Kuhn: invisible assumptions?

The lab assumes hallucination can be scored from text output and that factual verification is possible for each item. This may miss subtle errors or ambiguous refusals.

## 14. Platt: does the experiment exclude alternatives?

Partly. It can distinguish false-anchor pressure from open structure and true-premise controls. It cannot fully separate all model-training and domain-familiarity effects.

## 15. Meehl: does more data make the test harder?

Yes. Larger N makes it harder for a small accidental difference to clear the minimum effect threshold and exposes domain-specific tell words as artifacts.

## 16. Feynman: how would we fool ourselves?

- Using false prompts that are too easy to hallucinate.
- Choosing controls that are too easy.
- Treating domain words as general tell words.
- Over-crediting partial refusals.
- Ignoring cases where models hallucinate without false anchors.

## 17. Pearl: causal claim?

The causal intervention is prompt condition: false anchor and forced mode. Causal language must remain bounded because prompts are not perfectly matched across all dimensions.

## 18. Ioannidis: chance a positive result is false?

Moderate if the corpus is too small or too hand-tuned. Mitigation: 50 prompts, domain balance, pre-locked scoring, full trail.

## 19. Mayo: could the test pass if hypothesis false?

Yes, if false prompts are systematically harder or more obscure. This is why controls and domain analysis are required.

## 20. Gwern: publish full trail?

Yes. Raw prompts, raw responses, labels, failures, exclusions, scoring changes, and deviations should be published with secrets redacted.

## 21. Gwern: timestamped predictions?

This file and the OSF-style prereg are the timestamped prediction surface. The repo commit hash should be recorded before model runs.

## 22. Ramdas: peeking / optional stopping?

No optional stopping is planned. If more prompts are added after initial analysis, they must be labeled as follow-up or exploratory, not part of the v2 confirmatory analysis.
