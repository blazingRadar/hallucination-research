# V4B/V5 Feedback Reconciliation

Date: 2026-05-03

## Verdict

The V4B audit feedback was correct. Some V4B wording needed tightening, and V5
did not need to be thrown away.

The current experiment chain is:

- V4: named-slot open-structure condition produced `11/36`.
- V4B: neutral descriptive schema with explicit anti-identifier exclusions
  produced `0/36`.
- V5: paired same-run comparison produced `10/36` named-slot positives and
  `0/36` neutral-with-exclude positives.
- V5B: neutral descriptive schema without explicit anti-identifier exclusions
  produced `0/36`.

## What Was Fixed In V4B Documentation

The V4B results memo and finding memo now use joint-removal language:

> replacing named-entity output slots with descriptive ones and adding explicit
> anti-identifier exclusions

instead of implying that V4B alone isolated named-slot semantics.

The auto-generated analysis memo title was corrected from "V4 Open-Structure" to
"V4B Neutral-Schema."

The κ=1.000 language was corrected to note degenerate single-class agreement:
both judges labeled every V4B row `accurate_answer`, so κ does not provide
meaningful disagreement-pressure evidence.

The V4B scoring addendum now documents that V4B has no `expected_real_entities`
allowlist and how judges should treat any named entity that appears in a neutral
response.

## V5/V5B Process Regression

The V3 audit caught that V3 silently dropped the V1
human-adjudication-on-disagreement clause. V4B restored it. V5 and V5B then
silently omitted it again.

This has now been logged as:

- `proofs/DEVIATION_LOG_V5.md` D3
- `proofs/DEVIATION_LOG_V5B.md` D4

The prereg/protocol record now restores the clause for future readers:
disagreements are logged, and human audit may override disagreement rows when
they are load-bearing for a published claim or a threshold decision. No V5/V5B
labels were retroactively changed.

## Token-Length Check

V4 named-slot prompt lengths:

- min: 210 chars
- median: 225 chars
- mean: 230.2 chars
- max: 275 chars

V4B neutral-with-exclude prompt lengths:

- min: 265 chars
- median: 281 chars
- mean: 279.0 chars
- max: 291 chars

V4B prompts are systematically longer by 6 to 71 characters per anchor. This is
a mild confound. V5B helps narrow the explicit-exclusion confound, but it does
not create a token-length-matched control. A future dose-response version should
include length-matched controls.

## Response-Usefulness Check

The V4B response-length distribution was not consistent with empty refusals:

- OpenAI median response length: 2013 chars
- Anthropic median response length: 7128 chars
- xAI median response length: 979 chars

Auditor A also hand-read high-risk V4B rows and found them substantive,
on-topic, and not refusal artifacts. That check is sufficient for the current
bounded corpus-scoped claim.

## Does V5 Need To Be Redone?

No. V5 should be kept.

V5 confirms the named-slot versus neutral-schema contrast in one same-run paired
dataset:

- named-entity schema: `10/36`
- neutral descriptive schema with explicit exclusions: `0/36`

But V5 alone still had the explicit-exclusion confound in the neutral arm. V5B
was the correct follow-up and found:

- neutral descriptive schema without explicit exclusions: `0/36`

So the main audit concern is narrowed substantially.

## What Is Still Missing

The full 2x2 is not complete because the lab has not run:

> named-entity schema with explicit anti-identifier exclusions

That cell would answer whether explicit exclusions rescue named slots. It is not
needed to preserve the current V5/V5B claim, but it is the next clean cell if the
lab wants a complete mechanism table.

The stronger next experiment is dose-response:

> 0, 1, 2, 4, 8 named-entity slots, with token-length-matched controls.

That would be the stronger mechanism test. The current V4B/V5/V5B package is a
bounded corpus-scoped result.
