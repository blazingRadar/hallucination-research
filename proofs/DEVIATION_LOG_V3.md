# Deviation Log V3

Date initialized: 2026-05-02

D1 — Claude false-anchor forced truncation rerun

- timestamp: 2026-05-02T18:01:00Z
- files changed: `proofs/DEVIATION_LOG_V3.md`; derived run artifacts will be written under `runs/`
- reason: the raw V3 collection completed with 84/84 responses and 0 errors, but 2/12 Anthropic `false_anchor_forced` responses ended with `finish_reason=max_tokens` at `max_tokens=1400`. This exceeds the preregistered >10% model-condition truncation threshold.
- timing: after raw model collection, before any scoring or analysis.
- action: rerun only the two truncated Anthropic rows at a higher token cap, preserve the original raw run, and build a clean merged dataset replacing only truncated responses.
- expected effect on claims: prevents condition-level scoring from depending on incomplete Claude forced-condition answers. The rerun does not alter prompts, corpus, model choice, scoring rubric, or thresholds.

D2 — Analysis grouping null-anchor patch

- timestamp: 2026-05-02T17:51:00Z
- files changed: `scripts/analyze_scored_results_v3.py`; `proofs/DEVIATION_LOG_V3.md`
- reason: the first analysis attempt failed before producing results because verified-control rows have `anchor_id=null`, and the grouping helper attempted to sort tuple keys containing both `None` and strings.
- timing: after scoring completed, before a successful aggregate analysis.
- action: patch grouping sort to order keys by their string representations, preserving the underlying grouped values.
- expected effect on claims: no effect on labels, rates, thresholds, corpus, or model outputs. This only allows control rows with null anchor IDs to be included in aggregate artifacts.

D3 — Verified-control usefulness calculation patch

- timestamp: 2026-05-02T17:54:00Z
- files changed: `scripts/analyze_scored_results_v3.py`; `proofs/DEVIATION_LOG_V3.md`
- reason: the first successful analysis table showed all verified controls labeled `accurate_answer`, but the threshold helper computed `verified_control_usefulness=0.000` because it reused the hallucination-positive rate helper on the subset of accurate rows.
- timing: after first successful aggregate analysis, before result interpretation or commit.
- action: compute verified-control usefulness directly as `count(primary_label == "accurate_answer") / total_controls`.
- expected effect on claims: fixes a denominator/metric bug in the preregistered utility threshold. It does not change model outputs, judge labels, hallucination-positive rates, or control-failure rates.

Any change after preregistration lock must be appended here with:

- timestamp;
- file changed;
- reason;
- whether change occurred before or after model runs;
- expected effect on claims.
