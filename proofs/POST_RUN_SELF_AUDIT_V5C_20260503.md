# Post-Run Self-Audit: V5C Named-With-Exclude

Date: 2026-05-03

## Verdict

V5C run integrity is clean and the missing named-with-exclude 2x2 cell is
closed. The result is ready for independent audit, with final claim language
pending audit feedback reconciliation.

## Integrity Checks

- Gate commit: `8f45df2 Pre-register V5C named-with-exclude cell`
- First provider call: `2026-05-03T20:27:59Z`
- Gate-first order: PASS
- Provider calls: `36/36`
- Provider errors: `0`
- Empty responses: `0`
- Finish reasons:
  - OpenAI: `12/12 stop`
  - Anthropic: `12/12 end_turn`
  - xAI: `12/12 stop`
- Corpus validation: `scripts/validate_corpus_v5c.py` PASS
- Secret-pattern scan after V5C: no matches

## Scoring Checks

- OpenAI judge: `gpt-5-chat-latest`
- Anthropic judge: `claude-sonnet-4-6`
- Primary rule: AND-agreement hallucination-positive
- Result: `14/36`
- Wilson 95% CI: `[0.248, 0.551]`
- Judge positive agreement: `0.750`
- Judge primary agreement: `0.694`
- Disagreements: `11`

## Deviation

Anthropic judge scoring first failed closed when a batch-size-2 scoring call
returned an invalid `response_hash`. The failed partial scoring directory is
preserved:

`scored/scoring-v5c-anthropic-20260503T204232Z`

The successful rerun used batch size 1:

`scored/scoring-v5c-anthropic-batch1-20260503T204341Z`

This is logged in `proofs/DEVIATION_LOG_V5C.md` D1.

## What V5C Adds

V5C closes the previously missing cell:

- V5 named-no-exclude: `10/36`
- V5C named-with-exclude: `14/36`
- V5 neutral-with-exclude: `0/36`
- V5B neutral-no-exclude: `0/36`

The correct interpretation is not "exclusions made hallucination worse." The
confidence intervals overlap. The correct interpretation is: explicit
anti-identifier exclusions did not suppress named-slot pressure on this corpus.

## Remaining Caveats

- Single 12-anchor synthetic corpus.
- No dose-response on named slot count.
- No deliberately length-matched design, although V5C weakens the length
  confound because named-with-exclude and neutral-with-exclude prompts are close
  in average character length and split 14/36 vs 0/36.
- V5C was a follow-up run, not part of the original V5 provider batch.
- Judge disagreement is non-trivial and should remain visible in the public
  writeup.

## Required Public Framing

Use:

> Explicit anti-identifier exclusions did not suppress named-slot pressure on
> this corpus.

Do not use:

> Exclusions made hallucination worse.

Do not use:

> The exclusion clause has no effect.
