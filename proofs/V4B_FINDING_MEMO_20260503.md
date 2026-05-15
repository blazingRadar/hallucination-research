# V4B Finding Memo: Schema Slots As Hallucination Pressure

Date: 2026-05-03

## Finding

V4B turned the failed V4 run into a sharper result.

V4 showed that removing the fabricated entity and `type:` task frame was not
enough when the output schema still demanded named artifacts. V4B removed that
third pressure source, added explicit anti-identifier exclusions, and produced
`0/36` AND-agreement hallucination-positive responses.

## Result

V4B neutral-schema condition:

- OpenAI: `0/12`
- Anthropic: `0/12`
- xAI: `0/12`
- Aggregate: `0/36`
- Wilson 95% CI: `[0.000, 0.096]`

Both judges labeled all 36 responses `accurate_answer`. There were no
misrecalls, no confabulation rows, and no judge disagreements.

## What We Missed In V4

V4 removed two obvious injection vectors:

1. the fabricated anchor;
2. the `type:` task operator.

It missed a third:

3. the output schema itself.

Fields like `study_name`, `rule_identifier`, `benchmark_name`, `advisory_id`,
and `statute_name` created a named-entity completion obligation. In low-recall
domains, the model filled those slots with plausible artifacts.

## What We Learned

The useful lesson is not "open prompts solve hallucination."

The useful lesson is:

> Hallucination pressure can live in the output contract.

That makes the finding product-shaped, but V4B by itself is a joint-removal
result. A prompt/schema compiler or linter should flag output fields that demand
named entities, identifiers, citations, statute numbers, study names, benchmark
names, or advisory IDs unless those entities are supplied, verified, or
explicitly allowed.

## Why This Was Valuable

The failed V4 run was not waste. It discovered the missing mechanism.

The sequence is now:

1. V3: false anchors can induce hallucination.
2. V4: removing the false anchor is not sufficient if the schema still demands
   named artifacts.
3. V4B: removing false anchor, task frame, named-output slots, and adding
   explicit anti-identifier exclusions dropped the observed failure to `0/36`.

That is a clean learning loop. The lab made a wrong assumption, preserved the
failure, found the leak, corrected the design, and reran it.

## Claim Boundary

Allowed:

> On this 12-domain corpus, neutralizing named-entity output slots plus explicit
> anti-identifier exclusions eliminated the observed V4 schema-slot
> hallucination failures under dual-judge scoring.

Not allowed:

- neutral schemas solve hallucination generally;
- premise removal alone is sufficient;
- task operators do not matter;
- this is a deployable product without a compiler/linter experiment.

## V5 Direction

V5 should directly test the mechanism V4B exposed:

> Holding domain, false-anchor absence, and `type:` absence constant, does a
> named-entity output schema produce more hallucination than a neutral
> descriptive output schema?

That is the next clean experiment.
