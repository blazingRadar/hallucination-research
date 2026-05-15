# Deviation Log V4

Date initialized: 2026-05-02

D1 — Anthropic open-structure truncation rerun

- timestamp: 2026-05-03T03:40:00Z
- file or artifact changed: `proofs/DEVIATION_LOG_V4.md`; derived rerun artifacts will be written under `runs/`
- reason: the raw V4 collection completed with 36/36 responses and 0 errors, but 4/12 Anthropic `false_anchor_open_structure` responses ended with `finish_reason=max_tokens` at `max_tokens=2500`. This exceeds the preregistered >10% truncation threshold.
- timing: after raw model collection, before any scoring or analysis.
- action: rerun only the four truncated Anthropic rows at a higher token cap; preserve the original raw run; build a clean merged dataset replacing only truncated responses before scoring.
- expected effect on claims: prevents the V4 open-structure rate and utility/misrecall analysis from depending on incomplete Claude answers. This does not alter prompts, corpus, model choice, scoring rubric, judges, or thresholds.

D2 — V4 scoring and analysis scripts

- timestamp: 2026-05-03T03:52:00Z
- file or artifact changed: `scripts/adjudicate_scores_v4.py`; `scripts/analyze_scored_results_v4.py`; `proofs/DEVIATION_LOG_V4.md`
- reason: the preregistered V4 protocol requires dual-judge scoring, Wilson intervals, judge agreement, V4/V3 comparison, misrecall separation, and tell-word frequencies. The repo had V3 single-judge scoring and analysis scripts, but not V4-specific scripts.
- timing: after raw collection and clean merge, before any V4 scoring or analysis.
- action: add V4 scripts that implement the preregistered V4 scoring/analysis requirements using the locked V3 base rubric and V4 addendum.
- expected effect on claims: no change to prompts, raw model outputs, judges, thresholds, or rubric. This creates the derived-analysis implementation needed to score the locked data.

Any change after the V4 preregistration gate commit must be appended here with:

- timestamp;
- file or artifact changed;
- reason;
- whether change occurred before or after model runs;
- expected effect on claims.
