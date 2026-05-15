# V5B Deviation Log

Date opened: 2026-05-03

## Entries

### D1 — xAI timeout row rerun

Time: 2026-05-03T08:05Z

The initial V5B provider run produced 35 raw responses and one xAI timeout:

- `xai VG010_NX TimeoutError`

Remediation: resume the same run ID with provider `xai` only. The runner skips
completed raw rows and retries the missing row. Preserve the original error row.

### D2 — Anthropic truncation subset rerun

Time: 2026-05-03T08:05Z

The initial V5B provider run had five Anthropic rows with
`finish_reason=max_tokens` at `max_tokens=3000`.

Remediation: rerun the truncated subset with a higher token cap and merge into a
clean scoring dataset. Primary scoring must use the clean merged dataset.

### D3 — Extend API timeout for one long Anthropic replacement row

Time: 2026-05-03T08:05Z

The `VG007_NX` Anthropic replacement row timed out twice during the D2
truncation rerun. The original row was truncated, so primary scoring still needs
a natural-stop replacement.

Remediation: narrowly update `scripts/rerun_truncated_subset.py` to accept
`--api-timeout`, then resume the same rerun with a longer timeout. This affects
transport timeout only, not prompt, model, token cap, scoring, or analysis.

### D4 — Human-adjudication-on-disagreement clause omitted from V5B prereg

Time: 2026-05-03

The V3 audit caught that V3 silently dropped the V1 human-adjudication clause.
V4B restored it. V5B then silently omitted the clause again from
`protocols/OSF_PREREG_V5B_NEUTRAL_NO_EXCLUDE.md`.

This is a methodology regression. V5B did log the single disagreement
(`xai VG005_NX`) and used the preregistered AND-agreement primary rule, but the
prereg did not explicitly state that a human audit may override disagreements
when a row is load-bearing.

Correction: restore the clause in the V5B prereg record and name this
regression before external claim use. No labels are retroactively changed.
