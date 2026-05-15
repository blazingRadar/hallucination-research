# V6 Post-Run Audit Synthesis: Public Technical Version

Date: 2026-05-04
Synthesis lead: orchestrator

## Inputs

- `proofs/AUDIT_20260504_V6_POST_RUN_independent_methodology_a.md`
- `proofs/AUDIT_20260504_V6_POST_RUN_independent_framing_b.md`

The original synthesis mixed technical audit findings with non-technical
planning. This public version retains the technical conclusions, claim boundary,
and follow-up design notes.

## Headline

V6 honored its preregistration, produced a statistically strong
length-adjusted dose trend, narrowly missed the preregistered pooled effect-size
threshold, and concentrated the high-dose signal in OpenAI outputs. The retained
claim is therefore a narrowed OpenAI-specific schema-slot-pressure result, not a
clean cross-provider result and not a general hallucination solution.

## What Both Auditors Confirmed

### 1. The Six P0 Pre-Run Fixes Landed Before The Run

Auditor A verified each required pre-run fix in the code or preregistration:

| # | Fix | Status |
|---|---|---|
| 1 | Length-as-covariate logistic regression | Landed |
| 2 | Per-provider Cochran-Armitage trend test | Landed |
| 3 | Do not pool with V5/V5B/V5C | Landed |
| 4 | No human override applied disclosure | Landed |
| 5 | Five anti-claims | Landed |
| 6 | Phare V2 citation | Landed |

All six fixes were committed before the run commit. The gate-first discipline
held.

### 2. The Threshold Miss Is Characterized Honestly

The preregistered binary effect-size threshold was `>= 0.15` for the 8-slot
minus 0-slot difference. The observed difference was `0.139`, so the
preregistered threshold did not pass.

The retained public claim should say both things:

- the threshold missed;
- the dose trend was still ordered and statistically strong after length
  adjustment.

### 3. The Human-Adjudication Clause Held

The V6 preregistration retained the reusable human-adjudication clause from
inception. This was the third consecutive cycle without recurrence of the
earlier dropped-clause regression.

### 4. Provider Concentration Is Load-Bearing

At dose 8:

- OpenAI: `20/48`
- Anthropic: `0/48`
- xAI: `0/48`

Across the full run:

- OpenAI: `23/240`
- Anthropic: `0/240`
- xAI: `1/240`

The "at least two providers with positive trend" criterion is weakly satisfied
only because xAI has a small positive trend driven by one dose-4 row. The
substantive result is OpenAI-concentrated at the highest dose.

## What Each Auditor Caught

Auditor A caught that the per-provider criterion technically passed but
materially weakened under inspection. The standalone generated results memo
needed to carry the provider-concentration qualifier so a reader would not
mistake V6 for a clean cross-provider replication.

Auditor B emphasized the same boundary from a framing perspective: the paper
draft needed to incorporate V6's threshold miss and provider concentration
rather than treating V6 as a straightforward success.

## What V6 Adds To The V3 Through V5C Arc

Across the lab's controlled iterations, schema-slot pressure appears
dose-dependent in OpenAI outputs under this synthetic setup. V6 produced an
ordered pooled pattern across named-slot doses `0/1/2/4/8` and a positive
length-adjusted dose coefficient (`p=1.9e-06`), while prompt length itself was
not a significant predictor (`p=0.326`).

The result remains bounded:

- the preregistered pooled effect-size threshold narrowly missed;
- the high-dose signal was provider-concentrated;
- vocabulary and slot count are not fully isolated at higher doses;
- production tool/function schemas were not tested.

## Follow-Up Design Notes

A technically useful V7 would address the remaining gaps directly:

- increase high-dose sample size to resolve the threshold question;
- add higher named-slot doses;
- isolate field-vocabulary semantics from slot count;
- optionally run a provider-specific OpenAI deep dive.

V7 is deferred. The current repository should be read as a bounded research
artifact with an honest near-miss and provider-conditional result.

## Meta-Finding

The audit cycle continued to work through V6. Earlier audit passes caught real
methodology breaches, including same-vendor judging, a dropped
human-adjudication clause, joint-removal overclaiming, and degenerate reliability
reporting. By V6, all pre-run P0 fixes landed before execution, the previously
caught human-adjudication regression did not recur, and the remaining audit work
mostly tightened provider and threshold framing.

This does not prove external reviewers would find no issue. It does show that
the lab's internal audit machinery caught and corrected concrete methodology
problems across multiple experimental cycles.

## Bottom Line

V6 honored its preregistration with all six pre-run audit fixes landed before
the run. The dose-response is length-controlled (`p=1.9e-06`), but the primary
effect-size threshold missed at observed `0.139` versus the required `0.15`.
The highest-dose signal was OpenAI-concentrated (`20/48`) with Anthropic and xAI
at `0/48`. The supported claim is therefore narrow: OpenAI-specific
schema-slot-pressure evidence on this synthetic corpus, not a clean
cross-provider result and not a general hallucination solution.
