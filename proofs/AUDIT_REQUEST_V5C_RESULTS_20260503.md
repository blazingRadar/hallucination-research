# Audit Request: V5C Named-With-Exclude Results

Date: 2026-05-03

## Request

Please audit V5C as the missing named-WITH-exclude cell from the V5/V5B
evidence package.

## Primary Questions

1. Did the V5C preregistration/gate commit land before model calls?
2. Does the V5C corpus actually test named-entity slots WITH explicit
   anti-identifier exclusions?
3. Are false anchors and `type:` operators absent from all V5C prompts?
4. Did the provider run complete cleanly?
5. Is the scoring result correctly reported as `14/36`, Wilson 95%
   `[0.248, 0.551]` under AND-agreement?
6. Are the 14 positive rows real fabricated-specifics cases, or are any judge
   artifacts / valid descriptive answers mislabeled?
7. Does V5C justify removing "missing 4th cell" from the public caveat list?
8. What claim wording should replace the previous V5/V5B tightened claim?

## Key Artifacts

- Gate/protocol:
  - `protocols/OSF_PREREG_V5C_NAMED_WITH_EXCLUDE.md`
  - `corpus/PROMPT_CORPUS_V5C_NAMED_WITH_EXCLUDE.jsonl`
  - `proofs/SHA256_INPUTS_V5C.txt`
- Source run:
  - `runs/hallucination-v5c-named-with-exclude-20260503T202759Z`
- Scoring:
  - `scored/scoring-v5c-openai-20260503T204232Z`
  - `scored/scoring-v5c-anthropic-batch1-20260503T204341Z`
- Analysis:
  - `analysis/analysis-v5c-named-with-exclude-20260503T204940Z`
- Result memo:
  - `proofs/RESULTS_MEMO_V5C_NAMED_WITH_EXCLUDE_20260503.md`
- Deviation log:
  - `proofs/DEVIATION_LOG_V5C.md`

## Current Proposed Claim

> On a 12-anchor synthetic corpus across three frontier models, with false
> anchors and `type:` operators absent in every cell, named-entity output schema
> slots produced hallucination-positive responses both without explicit
> anti-identifier exclusions (`10/36`) and with explicit anti-identifier
> exclusions (`14/36`). Neutral descriptive schema slots produced `0/36` both
> with and without those exclusions. This supports a schema-slot pressure
> account on this corpus, while leaving prompt-length matching, dose-response,
> production tool schemas, and fresh-corpus generalization untested.
