# V5C Deviation Log

Date opened: 2026-05-03

## Entries

### D1 — Anthropic judge returned invalid response_hash in first scoring attempt

Time: 2026-05-03T20:43Z

The first Anthropic judge scoring run used `batch-size=2` and completed four
batches before returning a `response_hash` that was not present in the source
run. The scoring script failed closed with `KeyError` and preserved the partial
failed scoring directory:

`scored/scoring-v5c-anthropic-20260503T204232Z`

Remediation: rerun Anthropic judge scoring from scratch with `batch-size=1`.
The successful scoring directory is:

`scored/scoring-v5c-anthropic-batch1-20260503T204341Z`

This affected judge-output formatting only. It did not change the source model
responses, corpus, provider calls, scoring rubric, or primary AND-agreement
rule.
