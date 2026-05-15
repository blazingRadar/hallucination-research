# V5 Deviation Log

Date opened: 2026-05-03

## Entries

### D1 — Anthropic truncation subset rerun

Time: 2026-05-03T08:10Z

The initial V5 provider run completed 72/72 responses with zero provider errors,
but four Anthropic rows reported `finish_reason=max_tokens` at `max_tokens=3000`.

Affected rows:

- `anthropic VG001_S named_entity_schema`
- `anthropic VG001_D neutral_descriptive_schema`
- `anthropic VG004_S named_entity_schema`
- `anthropic VG011_S named_entity_schema`

Remediation: rerun only the truncated subset with `max_tokens=6000`, preserve the
original run, and merge the replacements into a clean scoring dataset. Primary
scoring must use the clean merged dataset, not the original truncated run.

### D2 — Anthropic judge malformed JSON repaired by retry path

Time: 2026-05-03T07:28Z

During final Anthropic judge scoring, one batch returned malformed JSON because
the judge embedded an unescaped quote in `evidence_excerpt`. The scorer preserved
the malformed judge output in:

`scored/scoring-v5-anthropic-20260503T072748Z/judge_parse_failures.jsonl`

The built-in retry prompt repaired the batch and final Anthropic scoring
completed 72/72 rows. This affected judge-output formatting only; it did not
change the model responses, corpus, scoring labels, judge model, or primary
AND-agreement rule.

### D3 — Human-adjudication-on-disagreement clause omitted from V5 prereg

Time: 2026-05-03

The V3 audit caught that V3 silently dropped the V1 human-adjudication clause.
V4B restored it. V5 then silently omitted the clause again from
`protocols/OSF_PREREG_V5_SCHEMA_SLOT.md`.

This is a methodology regression. V5 did log disagreements and used the
preregistered AND-agreement primary rule, but the prereg did not explicitly
state that a human audit may override disagreements when a row is load-bearing.

Correction: restore the clause in the V5 prereg/protocol record and name this
regression before external claim use. No labels are retroactively changed.
