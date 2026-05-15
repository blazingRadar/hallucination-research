# Pre-Ship Fixes: V5/V5B Audit

Date: 2026-05-03

## Status

Pre-ship audit fixes applied.

## Fixes

1. Restored the human-adjudication-on-disagreement clause in:
   - `protocols/OSF_PREREG_V5_SCHEMA_SLOT.md`
   - `protocols/OSF_PREREG_V5B_NEUTRAL_NO_EXCLUDE.md`
   - `protocols/V5_PROTOCOL_SCHEMA_SLOT.md`
2. Logged the regression in:
   - `proofs/DEVIATION_LOG_V5.md` D3
   - `proofs/DEVIATION_LOG_V5B.md` D4
3. Updated V5 and V5B result memos to disclose the regression.
4. Preserved the V5/V5B independent audit memos and synthesis in `proofs/`.

## Blog Claim Boundary

Use the post-V5C claim:

> On a 12-anchor corpus across `gpt-5-chat-latest`, `claude-sonnet-4-6`, and
> `grok-4.3` (temp 0), with false anchors and `type:` operators absent in every
> cell, named-entity output schema slots produced hallucination-positive
> responses both without explicit anti-identifier exclusions (`10/36`, Wilson
> 95% `[0.158, 0.440]`) and with those exclusions (`14/36`, Wilson 95%
> `[0.248, 0.551]`). Neutral descriptive slots produced `0/36` both with and
> without those exclusions (Wilson 95% `[0.000, 0.096]`). This supports a
> schema-slot pressure account on this corpus, while leaving prompt-length
> matching, dose-response, production tool schemas, and fresh-corpus
> generalization untested.

## Remaining Open Items To Name Publicly

- Token-length confound: V5C weakens this concern because the
  named-with-exclude and neutral-with-exclude cells are near-equal in character
  length while splitting 14/36 vs 0/36, but deliberately length-matched prompts
  are still not run.
- No dose-response on slot count.
- Single 12-anchor synthetic corpus.
- Residual unsupported-quantitative-claim risk, surfaced by V5B `VG005_NX`.

## V5C Follow-Up

After this memo, the missing fourth 2x2 cell was run as V5C:

- `proofs/RESULTS_MEMO_V5C_NAMED_WITH_EXCLUDE_20260503.md`
- named-with-exclude result: `14/36`, Wilson 95% `[0.248, 0.551]`

This removes the missing-cell caveat, but it does not remove the remaining
prompt-length, dose-response, fresh-corpus, or production-schema caveats.
