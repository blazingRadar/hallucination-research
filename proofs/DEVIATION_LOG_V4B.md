# V4B Deviation Log

Date opened: 2026-05-03

## Purpose

Record any deviation from the V4B neutral-schema preregistration after the gate
commit. Entries must be written when the decision is made, not after results are
known.

## Entries

### D1 — Anthropic judge malformed JSON on first scoring attempt

Time: 2026-05-03T06:00Z

After the raw 36-response provider run completed cleanly, OpenAI judge scoring
completed. The first Anthropic judge scoring attempt failed before writing any
scores because the judge returned malformed JSON that `json.loads` rejected.

Preserved failed scoring directory:

`scored/scoring-v4b-anthropic-20260503T060020Z`

Remediation: rerun Anthropic judging with `--batch-size 1` to reduce JSON
formatting pressure. This changes only the scoring batch shape, not the corpus,
model responses, labels, rubric, or primary analysis rule.

### D2 — Anthropic judge still malformed JSON at batch size 1; add retry logging

Time: 2026-05-03T06:01Z

The batch-size-1 Anthropic retry completed five rows, then failed on another
malformed JSON response. The partial output is preserved at:

`scored/scoring-v4b-anthropic-20260503T060048Z`

Remediation: narrowly harden `scripts/adjudicate_scores_v4.py` so parse
failures are written to `judge_parse_failures.jsonl` and can be retried with an
explicit "return valid JSON only" repair prompt. This does not change labels,
rubric text, model responses being scored, judge model, or primary
AND-agreement analysis. It changes only failure handling for invalid judge JSON.
