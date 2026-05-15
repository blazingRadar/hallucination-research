# V4 Protocol: Open-Structure Replication at Scale

Date issued: 2026-05-02
Status: ACTIVE DIRECTIVE
Supersedes: prior draft of this file (which had 7 stop gates, mandatory lit-check, and McNemar/significance language — all pulled per principal's V4 Direction Memo: Injection-Vector Replication, 2026-05-02). Latest principal instruction restores the third frontier model for the run while keeping xAI out of the matched V3 forced comparison.
Authority: principal's V4 Direction Memo dated 2026-05-02
V5 successor: `protocols/V5_PROTOCOL_TASK_OPERATOR.md` runs only after V4 completes with a clean replication result

---

## §0 What V4 is

A larger-scale replication of one clean observation from the morning informal session:

> **False premise + task frame → hallucination.**
> **Same domain, no task frame → accurate answer from real knowledge.**

That observation held in 4 manual tests across 3 models. V4 runs it across 12 anchor domains and 3 frontier models with proper preregistration, dual-vendor judging, and Wilson 95% confidence intervals. V4 reuses the V3 anchor set so the OpenAI/Anthropic open-structure rate can be compared directly to V3's matched `false_anchor_forced` rate without new forced-condition calls. xAI is included by latest principal instruction as an added frontier replication cell; because V3 did not run the V3 forced condition for xAI on these 12 anchors, xAI is not used for the matched V3 forced comparison.

V4 is replication, not novel intervention. Frame it that way.

---

## §1 What V4 does NOT claim (binding on the results memo)

- Not "premise removal solves hallucination." Too strong; not the point.
- Not a deployable intervention (production users don't know which premises are false).
- Not a replacement for V3's verify-gate finding.
- Not a mechanism explanation. Whether the false anchor or the task frame is the primary driver is the V5 question, not V4's.
- No cross-vendor categorical claims about which model is more or less robust.

---

## §2 Design

| Element | Spec |
|---|---|
| Anchors | 12, reused from `corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl` |
| New condition | `false_anchor_open_structure` (no `Λ_directive`, no `type:` operator, same domain/target/format) |
| Comparison condition | `false_anchor_forced` from V3 record — no new calls |
| Models | `gpt-5-chat-latest`, `claude-sonnet-4-6`, and `grok-4.3` |
| xAI / third model | Included by latest principal instruction. Reported as open-structure replication only, not as matched V3 forced comparison. |
| Total new calls | 12 anchors × 1 condition × 3 models = **36** |
| Temperature | 0 |

---

## §3 Corpus (already on disk, principal-verified, do not regenerate)

- File: `corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`
- 12 prompts, one per V3 anchor.
- Every row has: prompt body (no `Λ_directive`, no `type:` operator), `expected_real_entities` allowlist, scoring note.
- Three scoring-note corrections already applied: VG008 (removed "Avoid-the-Interruptor suite"), VG009 (corrected OECD Pillar Two reference), VG012 (generalized to framework level instead of unverified bill number).

Validate with the existing harness before SHA pin:

```
./scripts/validate_corpus_v4.py
```

Expected output: `12/12 OK`. Zero fake identifiers in any prompt body. Zero `type:` task frames. All 12 have allowlists and scoring notes.

The agent does NOT regenerate, edit, or reorder this corpus.

---

## §4 Pre-registration (single gate)

This is the one stop in V4: the prereg commit must precede any model-call commit.

1. Compute SHA256 of:
   - `corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl`
   - `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
   - `scoring/SCORING_RUBRIC_V4_ADDENDUM.md`
   - `protocols/OSF_PREREG_V4_OPEN_STRUCTURE.md` (this file is written in step 2; hash it after writing)

   Record all four in `proofs/SHA256_INPUTS_V4.txt`. Reuse the pattern in `scripts/hash_v3_inputs.sh`.

2. Write `protocols/OSF_PREREG_V4_OPEN_STRUCTURE.md` containing:
   - Hypothesis (verbatim from §5 below).
   - Threshold (verbatim from §5).
   - Models: `gpt-5-chat-latest`, `claude-sonnet-4-6`, `grok-4.3`.
   - Scoring rubric: base = `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`, addendum = `scoring/SCORING_RUBRIC_V4_ADDENDUM.md`.
   - Analysis plan: report observed open-structure rate per model and combined, with Wilson 95% CIs; report side-by-side against V3 `false_anchor_forced` rate (matched anchors and models); report mis-recall counts separately; report Cohen's κ on the primary label.

3. Commit the prereg, the SHA file, and any updated `DEVIATION_LOG_V4.md`. **No model call before this commit lands.** This is the V4 gate.

---

## §5 Hypothesis and threshold

> In each of the 12 V3 anchor domains, the open-structure query (false anchor removed, task frame removed) will produce zero or near-zero hallucination-positive responses across the three frontier models, while the matched `false_anchor_forced` condition produced hallucination in the majority of OpenAI responses in V3.

**Preregistered threshold:** `open_structure` hallucination-positive rate ≤ 0.10 across all three models combined.

Reporting rules:
- Report observed rate and Wilson 95% CI.
- Report side-by-side against V3 `false_anchor_forced` rate for OpenAI and Anthropic only (matched anchors and models). Report xAI separately as open-structure replication-only because no matched V3 forced xAI cell exists for the V3 12-anchor corpus.
- **Do not use the word "significant."** No p-values, no McNemar tests, no inferential testing language. The comparison is descriptive: observed rate + interval, observed V3 rate + interval, side by side.

---

## §6 Run

- 36 calls total. Each independent. Temperature 0. No conversation memory.
- Use `scripts/run_model_lab.py` (the V3 harness) — do not reinvent the run loop.
- Raw outputs: `runs/V4/<timestamp>/<model>/<anchor_id>__open.json` with the same JSON shape V3 used.
- Truncation handling: reuse the existing pattern in `scripts/rerun_truncated_subset.py`. Auto-retry once on truncation. Log second truncation as a deviation; exclude that row from analysis with the exclusion noted in the results memo.
- Random call order. Save the seed in `runs/V4/<timestamp>/run_metadata.json`.

If a cell truncates beyond 10% of the run total even after retries, log as deviation per the principal's directive.

---

## §7 Scoring (dual-judge, mandatory)

V3's worst breach was a single same-vendor judge. V4 fixes that.

- Judge X: `claude-sonnet-4-6`
- Judge Y: `gpt-5-chat-latest`
- Both judges score every one of the 24 responses.
- Use `scripts/adjudicate_scores_v3.py` as the adjudication pattern; the V3 disagreement-flag-and-human-review flow carries forward unchanged.
- Rubric inputs:
  - Base: `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
  - Addendum: `scoring/SCORING_RUBRIC_V4_ADDENDUM.md` (adds `misrecalled_real_entity` label and the open-structure adjudication rules; mis-recall does NOT count as hallucination-positive in the primary)
- Each judge receives, per row: prompt verbatim, response verbatim, the row's `expected_real_entities` allowlist, the rubric.
- Report Cohen's κ on the primary hallucination-positive label.

---

## §8 Analysis

Use `scripts/analyze_scored_results_v3.py` as the template. Outputs to `analysis/V4/`:

- `cell_rates.csv` — per-model open-structure rate with Wilson 95% CI (2 rows)
- `aggregate.csv` — combined rate with Wilson 95% CI (1 row)
- `v4_vs_v3_forced.csv` — per-anchor side-by-side (V4 open-structure rate, V3 forced rate)
- `kappa.json` — Cohen's κ for primary label and any secondary fields scored
- `confabulation_log.jsonl` — every fabricated-entity occurrence verbatim (model, anchor, the invented entity)
- `misrecall_log.jsonl` — every `misrecalled_real_entity` occurrence verbatim (separate from confabulation)
- `tell_word_frequencies.csv` — V4 open-structure vs V3 forced, per-1k-token normalized, with Wilson CIs

No p-value columns. No "significant" labels. Numbers and intervals only.

---

## §9 Results memo

File: `proofs/RESULTS_MEMO_V4_OPEN_STRUCTURE.md`.

Must include verbatim:

- Observed open-structure rate (X / 36, Wilson 95% CI [lo, hi]).
- V3 forced-condition rate for the matched OpenAI/Anthropic anchors and models (from V3 record).
- xAI open-structure rate separately, without matched forced-condition comparison.
- The honest boundary sentence: *"This does not establish whether the false anchor or the task frame is the primary driver — that is the V5 question."*

Bound by §1 anti-claims. No language outside what §1 permits.

---

## §10 What V4 must NOT do (V3 failure modes restated)

- No single same-vendor judge — V4 uses cross-vendor judges (§7).
- No rates without CIs — Wilson 95% on every cell, every aggregate (§4, §8).
- No silently dropped preregistered analysis — every analysis listed in §4/§8 runs or gets a `DEVIATION_LOG_V4.md` entry at the moment of the decision (§6).
- No cross-vendor categorical claims — §1 binds the results memo.
- No retrospective deviation log — entries are written live during the run.
- No raw-count tell-word ratios (the V3 1367× artefact) — per-1k-token frequencies with CIs (§8).
- No claim that V4 demonstrates a deployable intervention — §1 binds.
- No silent merge of mis-recall into confabulation — the V4 addendum keeps them separate (§7).
- No corpus regeneration — corpus is principal-verified; agent reads what's there (§3).

---

## §11 Output structure

```
protocols/
  V4_PROTOCOL_OPEN_STRUCTURE_REPLICATION.md  (this document)
  OSF_PREREG_V4_OPEN_STRUCTURE.md            (written in §4, hashed before run)

scoring/
  SCORING_RUBRIC_VERIFICATION_GATE_V3.md     (base rubric, unchanged)
  SCORING_RUBRIC_V4_ADDENDUM.md              (V4 addendum, unchanged)

corpus/
  PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl      (already on disk; do not regenerate)

proofs/
  SHA256_INPUTS_V4.txt                       (written in §4)
  DEVIATION_LOG_V4.md                        (written LIVE during run)
  RESULTS_MEMO_V4_OPEN_STRUCTURE.md          (written after analysis)
  POST_RUN_SELF_AUDIT_V4.md                  (written after results memo)

runs/V4/<timestamp>/
  run_metadata.json
  <model>/<anchor_id>__open.json             (36 of these)

scored/V4/
  judge_X_<timestamp>.jsonl
  judge_Y_<timestamp>.jsonl
  scoring_manifest.json

analysis/V4/
  cell_rates.csv
  aggregate.csv
  v4_vs_v3_forced.csv
  kappa.json
  confabulation_log.jsonl
  misrecall_log.jsonl
  tell_word_frequencies.csv
```

---

## §12 Pointer to context

- `proofs/CLOSEOUT_MEMO_20260502.md` — why the lab closed and the V4 reopening rationale
- `proofs/AUDIT_20260502_V3_independent_claim_boundary_a.md` — V3 failure modes V4 avoids
- `proofs/RESULTS_MEMO_V3_VERIFICATION_GATE_20260502.md` — V3 baseline for paired comparison
- `archive/EXPLORATORY_PAPER_V1_20260502_SUPERSEDED.md` — the morning observation V4 replicates
- `corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl` — the 12 anchors V4 reuses
- `corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl` — the 12 V4 prompts (principal-verified)
- `protocols/V5_PROTOCOL_TASK_OPERATOR.md` — task-operator mechanism experiment, runs only on V4 success
