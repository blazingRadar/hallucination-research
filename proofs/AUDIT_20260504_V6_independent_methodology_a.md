# Independent Pre-Run Audit: V6 Methodology + Design Integrity (Auditor A)

Date: 2026-05-04
Auditor: independent (no prior conversation context)
Source of record: live read of `<repo>/` HEAD as of audit time (commit `00a5de1` "Pre-register V6 schema-slot dose response")
Audit class: pre-run methodology + design integrity

## Verdict

**READY_AFTER_FIXES** — three small, clearly-actionable items. None require corpus regeneration; two are prereg/protocol text edits and one is an analysis-script enhancement that can land before scoring runs (it does not affect the model-call phase). If the principal would prefer to land only the two prereg edits before model calls and treat the analysis enhancement as a pre-scoring fix, that is a defensible split. The corpus itself is sound and the discipline regressions of prior cycles do **not** repeat.

## Headline (one sentence)

V6 carries the human-adjudication clause forward byte-identically from the V5C prereg and the canonical reusable template snippet (verified by `git blame` on commit `00a5de1` and three-way `diff`), the corpus passes byte-level integrity checks for false-anchor absence / `type:` absence / explicit-exclusion absence and replicate identity, and the dose-response design is correctly implemented with constant 8 total fields per prompt — but the prereg should explicitly acknowledge the residual prompt-length confound (Pearson r ≈ 0.48 between dose and prompt length, perfectly monotonic at the cell-mean level), the analysis script should add prompt-length as a covariate in a sensitivity analysis, and the prereg should clarify how mid-token Greek-letter typos in 17 of 24 anchors' `target` blocks (e.g. `Φimage_screening` vs the V6A001-V6A007 pattern `Φ_algorithmic_vendor_oversight`) are being treated.

## What V6 closes from the V5C audit's open items

Cross-referencing `proofs/AUDIT_20260503_V5C_independent_methodology_a.md` items 128-133 and `proofs/AUDIT_SYNTHESIS_V5C_20260503.md` Fix 5:

| V5C open item | V6 status |
|---|---|
| Dose-response on 0/1/2/4/8 named slots | **Closed by design** — five dose levels at 48 rows each; correct cardinalities verified |
| Fresh-corpus replication beyond 12 V3 anchors | **Closed by design** — 24 fresh anchors, only one literal domain-name overlap (`browser_security`) and that one is at a totally different probe level (V3: W3C SPECTRA-12 false-anchor; V6: cross-origin isolation patterns) |
| Token-length-matched controls | **Partially closed** — within-anchor spread is small (≤45 chars across all 5 doses for any given anchor, well under the 170-char validator threshold) but cell-mean prompt length is **monotonic with dose**: 356.7 → 362.7 → 364.7 → 368.7 → 370.7 chars. Pearson r between dose and length at row level = **0.478**. Within-cell stdev is 7.75 chars across all five cells, identical because the variation is driven by anchor-name length not by named-vs-neutral field naming. So a hostile reviewer can still say "your dose-response signal is confounded with prompt length, smaller than V5 but in the same direction." See "Length-matching analysis" below. |
| Human-adjudication clause re-regression risk | **Closed cleanly** — clause is byte-identical to V5C and to the new template snippet; see "Human-adjudication clause status" below |
| Cross-vendor judging | **Closed by design** — same `gpt-5-chat-latest` + `claude-sonnet-4-6` dual-judge AND-rule with raw agreement reporting (no Cohen's κ trap) |
| Continued absence of false anchors / `type:` / explicit anti-identifier exclusion | **Closed by design** — validator enforces all three; I additionally re-grep'd the raw corpus for the V3 false-anchor token list (NARROW-19, Aquila-7, etc.) and for `proper_nouns` / `identifiers` / `citations` substrings. None present. |
| k>1 replicates per cell | **Implemented but partly cosmetic** — k=2 of byte-identical prompts at temperature 0. This is a stability check, not an independent sample. The protocol explicitly disclaims this at `protocols/V6_PROTOCOL_DOSE_RESPONSE.md:99-101` ("Do not claim repeated samples are independent in the same way as independent anchors. Report anchor-level sensitivity.") and the analysis script collapses replicates within `(anchor, dose, provider)` for the secondary anchor-level analysis. Acceptable, but see "Hidden confounds" #4. |
| Reusable prereg snippet for the adjudication clause | **Closed** — `protocols/PREREG_TEMPLATE_SNIPPET_HUMAN_ADJUDICATION.md` exists and is verbatim what V5C and V6 use |

## Corpus integrity check

- **Row count**: 240 (24 anchors × 5 doses × 2 replicates) — matches design.
- **Per-cell counts**: each dose has exactly 48 rows; each `(anchor, dose)` has exactly 2 replicates; each anchor appears in all 5 dose levels (verified by validator script and by re-running it: `status=PASS, errors=0, warnings=0`).
- **Total format fields per row**: 8 in every row (verified — the validator's `len(fields) != TOTAL_FORMAT_SLOTS` check would fire and does not).
- **Named slot count actually matches `named_slot_count` field**: validator cross-checks each row's `format_fields` against the `NAMED_FIELDS` set. Pass.
- **Replicates byte-identical within cell**: yes, R1 and R2 prompts are byte-identical for every `(anchor, dose)`. This is intentional but means k=2 at T=0 is a stability check rather than independent replication.
- **No false anchors**: I scanned the entire 240-row corpus for the 12 V3-era false-anchor tokens (NARROW-19, Aquila-7, HERMES-311, 10b-27, Borealis Trust Index, Tallinn-Neva, SPECTRA-12, ORCHID-RL, Oslo Model Audit Compact, Geneva Automation Memorandum, VERA-2021-1442, Adaptive Homework Transparency Act). Zero hits. Validator does the same check.
- **No `type:` operator**: validator enforces; I also grep'd the raw file. Zero hits.
- **No explicit anti-identifier exclusion**: validator enforces presence of `do_not_invent` + `mark_uncertain_when_unsure` AND absence of `proper_nouns` / `identifiers` / `citations`. All 240 rows pass.
- **Prompt structure**: every row starts with `QUERY {`, contains `domain:`, `target:`, `format:`, `constraints:`, `exclude: { preamble, summary }`. Verified by inspection of one R1 row per dose level for V6A001, V6A012, V6A024.
- **Anchors fresh**: anchor IDs `V6A001`-`V6A024` do not collide with V3-V5C anchor IDs (`VG001`-`VG012`). Domain overlap with V3 is one literal name (`browser_security`); the V6 probe (cross-origin isolation patterns) is at a totally different level than V3's W3C SPECTRA-12 false-anchor probe. Effectively fresh corpus.

## Length-matching analysis

**This is the methodology issue most worth surfacing.**

Cell-mean prompt lengths by dose:

| Dose | Mean | Min | Max | Within-cell stdev |
|---:|---:|---:|---:|---:|
| 0 | 356.7 | 340 | 371 | 7.75 |
| 1 | 362.7 | 346 | 377 | 7.75 |
| 2 | 364.7 | 348 | 379 | 7.75 |
| 4 | 368.7 | 352 | 383 | 7.75 |
| 8 | 370.7 | 354 | 385 | 7.75 |

Two facts a hostile reviewer will notice:

1. **The cell-mean lengths are perfectly monotonic with dose.** The validation report's headline "356.7 → 370.7" understates this — every step is monotonically increasing. Pearson `r` between named_slot_count and prompt length at the row level is **0.478**.
2. **The within-cell stdev is identical across all five cells (7.75)** because the only intra-cell variation source is anchor-name length, which is shared across all five conditions for each anchor. This means the within-cell variation cleanly cancels out within an anchor-paired contrast — that is, **for any single anchor, the 8-named cell is always exactly 14 characters longer than the 0-named cell**. The cell-mean monotonic gap of 14 characters across all five doses is almost entirely driven by the field-name vocabulary in `format: { ... }` itself (e.g. `pattern, mechanism, evidence_basis, ...` is shorter than `artifact_name, source_name, identifier_code, ...`).

What this means substantively:

- The 14-char spread is ~3.9% of the smallest cell mean. This is much smaller than the V5 named-vs-neutral spread (~21%) that the V5C audit incidentally refuted.
- Because the spread is monotonic AND systematic (driven entirely by the longer named-slot field names), prompt length is **structurally confounded with dose**, not randomly varying. The lab cannot pad the shorter cells without changing the format-field vocabulary in a way that destroys the dose semantics.
- The right fix is **not** to attempt corpus regeneration. The fix is (a) acknowledge the residual confound explicitly in the prereg, and (b) include prompt length as a covariate in a sensitivity logistic regression in the analysis script.

The current prereg only says: "Do not claim prompt length is perfectly controlled; report observed prompt lengths by dose" (line 127-128). That's a public-claim gate but does not commit to a covariate-controlled sensitivity analysis. **A pre-run sensitivity-analysis pre-commitment is what closes the confound for a hostile reviewer.**

## Human-adjudication clause status

This was the priority check. Verified three ways:

1. **Present from the inception commit.** `git blame protocols/OSF_PREREG_V6_DOSE_RESPONSE.md` shows lines 91-94 ("Disagreements must be logged. A human audit may override a disagreement if the published claim relies on that row or if the disagreement changes the public claim boundary. Without human override, the preregistered AND-agreement rule remains the primary analysis.") were authored in the original V6 commit `00a5de14cd21e5ad11e54cb6da62daf1bc93e2d2` ("Pre-register V6 schema-slot dose response") at 2026-05-03 22:35:57 -0700. **Not retroactively patched.**
2. **Byte-identical to V5C and to the canonical snippet.** `diff` between V5C prereg lines 50-53 and V6 prereg lines 91-94 returns empty. `diff` between the snippet (`protocols/PREREG_TEMPLATE_SNIPPET_HUMAN_ADJUDICATION.md` lines 24-27) and V6 prereg lines 91-94 also returns empty. So the V6 author either copy-pasted from the snippet (best case) or wrote text identical to it (functionally equivalent).
3. **Reusable snippet exists and is documented.** `protocols/PREREG_TEMPLATE_SNIPPET_HUMAN_ADJUDICATION.md` is in the repo, names the V3/V4B/V5/V5B/V5C drift history correctly, and prescribes both the clause text and the required reporting fields (judge primary-label agreement, judge positive-label agreement, disagreement count, path to disagreement log, whether any human override was applied).

**The regression that V5/V5B introduced did not recur in V6, and the structural fix recommended by the V5C audit is in place.** This is the second consecutive iteration without re-regressing on this clause. Discipline-curve convergence holds.

One small follow-up gap: the V6 prereg does not commit to reporting "whether any human override was applied" as a required reporting field (the snippet's §"Required Reporting" item 5). This is implicit in the analysis script (which produces a `judge_disagreements.jsonl` log) but is not a written prereg commitment. Minor.

## Statistical analysis plan adequacy

What the V6 prereg specifies (`protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:96-108`):

1. Per-dose aggregate rates with Wilson 95% CIs ✓ (implemented in `analyze_scored_results_v6.py:173`)
2. Per-model per-dose rates with Wilson 95% CIs ✓ (`analyze_scored_results_v6.py:174-181`)
3. Cochran-Armitage trend statistic over named slot count, two-sided p ✓ (`analyze_scored_results_v6.py:85-102`, called at :198)
4. Fisher exact 8-vs-0 ✓ (`analyze_scored_results_v6.py:69-82`, called at :192)
5. Fisher exact pooled-high (4,8) vs pooled-low (0,1) ✓ (called at :197)
6. Anchor-level sensitivity ✓ (collapses replicates within `(anchor, dose, provider)`; `analyze_scored_results_v6.py:200-212`)
7. Judge agreement summary ✓ (raw positive- and primary-label agreement; :235-236)
8. Disagreement, misrecall, positive logs ✓ (:243-249)
9. Provider finish-reason and truncation table ✓ (:105-116, :234)

What is **specified well**:

- Falsifiable thresholds: 8-vs-0 difference ≥ 0.15 AND positive Cochran-Armitage z (`:25-28`).
- Secondary 0-named-slot Wilson upper bound < 0.10 (`:34-35`) — this is the cell that actually exposes the lab to falsification risk, mirroring V5B's role in the prior cycle.
- Both Cochran-Armitage (treats dose as ordinal-scored, the right primary test for trend) and Fisher exact (treats endpoints categorically, the right secondary check) are appropriate.

What is **missing or under-specified**:

1. **Prompt-length covariate.** Not in the prereg, not in the analysis script. Given the monotonic length-dose correlation (r ≈ 0.48), a sensitivity logistic regression with dose AND prompt length should be pre-committed. Without it, "your trend is just length" is a free critique.
2. **Anchor as random effect / clustering correction.** The Cochran-Armitage as implemented treats all 240 (or rather all `240 × 3 providers = 720`) observations as independent. They are not — each anchor contributes 5 doses × 2 replicates × 3 providers = 30 observations, and within-anchor responses are correlated. The current trend p-value is therefore anti-conservative. The script does an anchor-level collapse for sensitivity but does not fit a mixed-effects model. Either the prereg should commit to a clustered-bootstrap or to interpreting the trend test as approximate-only with the anchor-level Cochran-Armitage (on `anchor_condition_positive`) as the true primary.
3. **Multiple comparisons.** Three statistical tests on the same dataset (CA trend, Fisher 8v0, Fisher high-v-low). All three are pre-registered, but no Bonferroni or holistic correction is named. Mild concern; conventionally pre-registered tests do not require correction, but an external statistical reviewer may ask.
4. **Treating dose as continuous vs ordinal.** The Cochran-Armitage uses dose values `0, 1, 2, 4, 8` as the ordinal scores, which is a continuous-spacing assumption (the gap from 1→2 is treated as half the gap from 2→4). This is reasonable for a dose-response interpretation but should be explicitly named in the prereg. A robustness check using equally-spaced ordinal scores (`1, 2, 3, 4, 5`) would be useful.
5. **Per-provider trend test.** The prereg requires per-model per-dose rates but does not commit to a per-provider Cochran-Armitage. If 8/0 difference appears in only 1 of 3 providers, the lab should have a pre-committed test to detect that. The protocol's stop condition "positives concentrate in one provider only" (`:117`) is qualitative; a per-provider trend p-value would make it quantitative.

The analysis plan is **sufficient to defend the bounded headline finding** but does not include every robustness check a larger dose-response design could include.

## Scoring rubric continuity

`scoring/SCORING_RUBRIC_V6_ADDENDUM.md` is short (68 lines) and clean. It:

- Inherits from V3 verification gate + V4B addendum (correct chain).
- Uses the same three positive labels (`accepted_false_premise`, `fabricated_specifics`, `fabricated_citation`).
- Preserves the V4 separation: `misrecalled_real_entity` is hallucination-negative and logged separately. The analysis script confirms this — it produces a separate `misrecall_log.jsonl` and counts it independently.
- Adds the dose-response-specific instruction "scorer must not infer that a response is wrong merely because it contains named entities in a high-dose condition" (line 62-63) — this is the right anti-bias rule for the design.
- Adds the symmetric instruction "scorer must not excuse a fabricated entity merely because the field name asked for one" (line 64-65) — this protects against the opposite bias.
- Does not introduce any new label categories.
- Does not contradict prior addenda.

**No regressions in the rubric.**

## Hidden confounds I checked for

1. **Length-dose correlation** — confirmed monotonic, r ≈ 0.48. See "Length-matching analysis." This is the one a hostile reviewer will hit hardest.
2. **Field-name semantic loading varying with dose** — confirmed varying. The named slots are precisely the load-bearing vocabulary the experiment is testing (`artifact_name, source_name, identifier_code, citation_label, program_name, standard_name, dataset_name, document_name`), so this is intended, not a confound. But note that V6's named slots are **a different vocabulary than V5/V5C's named slots** (V5 used per-anchor specific slots like `score_name, mission_name, study_name, rule_identifier, statute_name, advisory_id, benchmark_name`; V6 uses 8 generic slots reused across all anchors). This is fine for the V6 internal dose-response analysis but means **V6 cannot be directly pooled with V5/V5C** to make a within-experiment slot-vocabulary comparison. The protocol's "Claims Not Allowed" section partially covers this ("Do not claim generality beyond the fresh V6 corpus") but does not explicitly call out the slot-vocabulary discontinuity. Worth one sentence in the prereg's claim-boundary block.
3. **Anchor-domain difficulty stratification** — checked. Each anchor appears in all 5 dose levels, so within-anchor contrasts are clean. Anchor-level sensitivity analysis collapses replicates within anchor-condition-provider, which handles the stratification correctly.
4. **k=2 replicate independence** — replicates are byte-identical at temperature 0. The protocol acknowledges this explicitly at `protocols/V6_PROTOCOL_DOSE_RESPONSE.md:99-101`. Acceptable but the analysis script could explicitly compare R1 and R2 within-cell and report stability rate. If R1≠R2 ever happens, that itself is a finding (provider nondeterminism at T=0) and should be quantified.
5. **Total expected output token count** — kept constant at 8 fields per prompt by design. Whether the model produces longer text per named-named field than per neutral field is an open empirical question, but the input field count is constant.
6. **Greek-letter token consistency in `target:` blocks** — found inconsistency. V6A001-V6A007 use `Φ_X` (with underscore); V6A008-V6A024 use `ΦX` (no underscore). One anchor (V6A008) mixes both styles. This is invisible to the dose-response analysis (target is constant per anchor across all 5 doses) but is a typo-class quality issue in the corpus. Not a deal-breaker for the run; worth fixing in a future iteration. Documenting here so it does not silently propagate to V7.
7. **Validator's `MAX_WITHIN_ANCHOR_LENGTH_SPREAD = 170`** — generous threshold. Actual within-anchor max-min spread is closer to 14-15 chars (since for a given anchor only the format-fields block changes across doses). The validator passes trivially. A tighter validator (`MAX_WITHIN_ANCHOR_LENGTH_SPREAD = 50` or `30`) would more meaningfully catch regressions.
8. **The `do_not_invent` constraint may suppress the dose-response signal.** This is the principal's own question (audit request item #5). The constraint is identical across all five doses, so it does not differentially affect cells. But if the constraint is so strong that it suppresses fabrication uniformly, the experiment will return null for reasons unrelated to dose. This is a power risk, not a confound — the lab should be prepared for a null result and treat it as informative, not as a failed experiment.

## Required fixes before running (if READY_AFTER_FIXES)

**Fix 1 (prereg, ~10 min):** Add an explicit prompt-length acknowledgment and a pre-committed sensitivity analysis to `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md`. Suggested addition after line 108 (end of "Required Analyses"):

```
10. Prompt-length sensitivity: report Pearson correlation between
    named_slot_count and prompt length at the row level. Refit a logistic
    regression with named_slot_count and prompt length as joint predictors of
    AND-positive; report the named_slot_count coefficient with 95% CI
    holding length constant.
11. Per-provider Cochran-Armitage trend: report the trend z and two-sided p
    separately for each provider.
```

And add to "Claims Not Allowed" (after line 130):

```
- Do not claim V6 results pool with V5/V5C — V6 uses a generic 8-slot named
  vocabulary while V5/V5C used per-anchor named slots; the two designs
  measure different things and cannot be combined.
```

**Fix 2 (analysis script, ~30 min, can land after model calls but before scoring):** Implement the two new analyses in `scripts/analyze_scored_results_v6.py`:
- (a) Length-as-covariate logistic regression. For a no-extra-deps implementation, fit by IRLS in pure Python (or pin a `statsmodels` dependency).
- (b) Per-provider Cochran-Armitage z and two-sided p. Trivial — wrap the existing `cochran_armitage()` in a per-provider loop.

**Fix 3 (prereg, ~5 min):** Add to the prereg's required-reporting section that the run-results memo must explicitly state "no human override was applied" (or list the rows where it was). This is the snippet's §"Required Reporting" item 5 and currently is not a written prereg commitment in V6.

**Fix 4 (optional, can defer):** Tighten the validator's `MAX_WITHIN_ANCHOR_LENGTH_SPREAD` from 170 to 50 (or whatever value actually catches a real corpus regression). Current value is so loose it passes trivially. Not a pre-run blocker but a discipline improvement for V7+.

**Fix 5 (optional, can defer):** Fix the `Φ_X` vs `ΦX` inconsistency in the V6 corpus generator's ANCHORS list. 17 of 24 anchors use the `ΦX` form (without underscore); V6A001-V6A007 use the `Φ_X` form. This requires regenerating the corpus and re-hashing inputs, so it is **not** a pre-run blocker for V6 (and it does not affect dose-response analysis since target is constant per anchor) — but it should be cleaned up before V7 reuses the anchor template.

The two prereg edits (Fix 1 and Fix 3) MUST land before the model calls to preserve the prereg-first discipline. The analysis enhancement (Fix 2) can land before scoring but does not need to land before model calls; it does not affect what data is collected.

## What I could not verify

- I did not re-run the model calls (they have not happened — this is a pre-run audit).
- I did not verify the `gpt-5-chat-latest`, `claude-sonnet-4-6`, and `grok-4.3` model IDs are still resolvable at the providers — that is a runtime check.
- I did not audit `scripts/run_model_lab.py` line-by-line for provider-side bugs introduced after V5C; I trust that the SHA-pinned version matches what V5C used (it appears in `proofs/SHA256_INPUTS_V6.txt` with the same hash family).
- I did not audit `scripts/adjudicate_scores_v4.py` line-by-line for label-coercion bugs since V5C; same trust assumption.
- I did not verify the Cochran-Armitage implementation in `analyze_scored_results_v6.py:85-102` against a reference statistics package — I sanity-checked the formula and it matches the standard score-test form, but a dedicated `scipy.stats.contingency` cross-check would be stronger.
- I did not verify the Fisher exact two-sided implementation against `scipy.stats.fisher_exact`. The two-sided summation rule used (sum probabilities ≤ observed) is the conventional Fisher rule, but there are multiple conventions and a reviewer might prefer a different one.
- I did not check whether the `grok-4.3` provider has any V6-specific API differences from the V5/V5C runs.
- I did not test the analysis script end-to-end against synthetic scored data (it has no scored data yet to run on). A small synthetic-data dry-run would have been a stronger pre-run check.
- I did not consult Auditor B and have no knowledge of B's findings.

---

## Appendix: command transcript (for reproducibility)

```
git log --oneline -15                          # confirmed 00a5de1 prep commit
git show 00a5de1 --stat                        # 12 files, 1445 insertions
git blame protocols/OSF_PREREG_V6_DOSE_RESPONSE.md | head -100
                                               # confirmed lines 91-94 from inception
diff <(sed -n '50,53p' V5C_prereg) <(sed -n '91,94p' V6_prereg)   # empty
diff <(sed -n '24,27p' SNIPPET) <(sed -n '91,94p' V6_prereg)      # empty
python3 scripts/validate_corpus_v6.py          # status=PASS, 0 errors, 0 warnings
python3 -c "<row-level length stats>"          # Pearson r = 0.478
                                               # within-cell stdev = 7.75 in all 5 cells
                                               # cell means: 356.7, 362.7, 364.7, 368.7, 370.7
python3 -c "<replicate identity check>"        # R1 == R2 byte-for-byte for all 120 cells
python3 -c "<Phi token typo scan>"             # 17 of 24 anchors mix Φ_X / ΦX
sha256sum vs proofs/SHA256_INPUTS_V6.txt       # all 12 hashes match
```
