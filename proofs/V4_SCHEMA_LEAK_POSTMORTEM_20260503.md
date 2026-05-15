# V4 Schema-Leak Postmortem

Date: 2026-05-03

## Verdict

The V4 run was validly executed but did not test the condition we intended.

The prompts removed the V3 fabricated anchors and removed the `type:` task operator, but the output schema still contained named-entity demand slots. Those slots recreated the completion pressure the experiment was trying to remove.

## What We Intended To Test

The intended V4 claim was:

> False premise + task frame causes hallucination; same domain without the false premise and without the task frame should let models answer from real knowledge.

That requires a prompt where the model is not forced to produce named entities unless it already knows them.

## What We Actually Tested

The V4 prompts still asked for fields like:

- `study_name`
- `rule_identifier`
- `benchmark_name`
- `advisory_id`
- `statute_name`
- `framework_name`
- `mission_name`
- `document_name`

Those fields are not neutral. They tell the model that the answer should contain named artifacts. In low-recall domains, that creates a strong incentive to fabricate plausible names and identifiers.

## What We Missed

We checked the obvious leak paths:

- The distinctive fake anchors were removed.
- The `type:` operator was removed.
- The prompts stayed in the same broad domain.

We did not check the third leak path:

> Does the output schema itself demand named entities?

That was the miss.

## Why The Run Still Mattered

The run was not wasted. It found a third injection vector.

Before V4, the working account had two obvious pressure sources:

1. false premise injection;
2. task-frame / task-operator pressure.

V4 revealed a third:

3. named-output-slot pressure.

Even when the false anchor is gone, a schema field such as `study_name` or `rule_identifier` can force the model into a named-entity completion mode. If the model does not know a real entity, it may fill the slot with a plausible fake one.

This is valuable because it points toward a concrete product/design rule:

> A prompt compiler should not only remove false anchors. It should also rewrite schemas that demand named entities into descriptive schemas unless the entity set is verified or supplied.

## What V4 Taught Us

The corrected lesson is:

> Hallucination pressure is not only in the premise. It can live in the output contract.

That is stronger and more useful than the original V4 binary question.

Original question:

> Does removing the false anchor make hallucination disappear?

Corrected question:

> Which prompt components force the model to invent named entities: false anchor, task operator, output schema, or their interaction?

## Why The V4 Result Failed The Original Claim

The V4 result was:

- 11/36 AND-agreement hallucination-positive.
- Aggregate rate 0.306.
- Threshold was <= 0.10.

Every AND-agreement positive was plausibly tied to a schema field demanding a named artifact.

Examples:

- `rule_identifier` -> invented `SEC-AI-2023-01` and `FINRA-AI-DISC-2024`.
- `study_name` -> invented university remote-work studies.
- `benchmark_name` -> invented reward-tampering benchmark names.
- `advisory_id` -> invented Kubernetes advisory IDs.
- `statute_name` -> invented Texas edtech statutory sections.

So the run did not prove that open-structure prompting fails generally. It proved that our open-structure schema was not actually neutral.

## Corrected Rerun Requirement

The rerun must remove all three pressure sources:

1. no fabricated anchor;
2. no `type:` operator;
3. no named-entity output slots.

The corrected schema should ask for:

- patterns;
- mechanisms;
- constraints;
- tradeoffs;
- evidence strength;
- uncertainty;
- what not to infer.

It should not ask for:

- names;
- identifiers;
- citations;
- statute numbers;
- rule numbers;
- study names;
- benchmark names;
- advisory IDs.

## Corrected Claim If Rerun Passes

If the neutral-schema rerun passes:

> In the same 12 domains where false-anchor and named-slot prompts induced hallucination, a neutral open-structure prompt with no fabricated anchor, no task operator, and no named-entity output slots produced low hallucination-positive rates. This supports the injection-vector account and shows that schema design, not only premise truth, affects hallucination risk.

## Claims Still Not Allowed

- Do not claim premise removal alone is sufficient.
- Do not claim the V4 failed run was useless.
- Do not claim neutral schemas solve hallucination generally.
- Do not claim deployment readiness.
- Do not claim V5 is unnecessary.

## Next Artifact

The corrected corpus is:

`corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl`

The corrected validator is:

`scripts/validate_corpus_v4b.py`

The corrected protocol is:

`protocols/V4B_PROTOCOL_NEUTRAL_SCHEMA_RERUN.md`
