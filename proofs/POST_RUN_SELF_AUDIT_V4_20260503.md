# Post-Run Self-Audit V4

Date: 2026-05-03

## Verdict

READY_FOR_INDEPENDENT_AUDIT.

V4 failed its preregistered replication threshold, and the failure appears substantively informative rather than a trivial provider or scoring artifact.

## Integrity Checks

- Gate commit preceded model-call commit:
  - `3ce26f7 Pre-register V4 open-structure replication`
  - `f083311 Collect V4 open-structure responses and lock scoring tools`
- V4 corpus validated before the run.
- Raw run produced 36/36 responses across OpenAI, Anthropic, and xAI.
- No provider errors in the raw run.
- Anthropic truncations were identified before scoring and rerun under D1.
- Clean merged dataset has 36 rows, 4 replacements, and 0 response errors.
- Both OpenAI and Anthropic judges scored all 36 rows.
- Secret scan over V4 run/scoring/analysis artifacts found no key patterns.

## Main Finding

The preregistered threshold failed:

- Expected: open-structure hallucination-positive rate <= 0.10.
- Observed: 11/36 = 0.306, Wilson 95% CI [0.180, 0.469].

This was based on AND-agreement between OpenAI and Anthropic judges.

## Why The Hypothesis Failed

The V4 prompts removed the V3 fabricated anchors and removed `type:`, but they still contained structured output slots that asked for named entities. Those slots appear to have created a new completion pressure:

- `study_name`
- `framework_name`
- `rule_identifier`
- `statute_name`
- `benchmark_name`
- `advisory_id`

The models often answered by inventing plausible names rather than staying at a generic, real-knowledge level.

## Audit Questions

1. Are the 11 AND-agreement positives valid hallucination-positive labels under the V4 addendum?
2. Are any of the positives better classified as `misrecalled_real_entity`?
3. Did the `expected_real_entities` allowlists accidentally make judges over-strict?
4. Is the right next hypothesis "schema-slot completion pressure" rather than only "task operator pressure"?
5. Should V5 become a factorial design over false-anchor presence, task operator, and named-output-slot pressure?

## Boundary

V4 does not show that open-structure prompting works. It shows that this specific structured open-query design still generated hallucination-positive named entities. The corrected lesson is that removing the false anchor is not enough if the prompt schema still asks the model to fill named-entity slots.
