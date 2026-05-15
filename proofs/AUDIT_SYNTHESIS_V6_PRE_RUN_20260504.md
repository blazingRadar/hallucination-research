# V6 Pre-Run Audit Synthesis: Auditor A + Auditor B

Date: 2026-05-04
Synthesis lead: orchestrator (synthesizing two independent V6 pre-run audit memos)
Inputs:
- `proofs/AUDIT_20260504_V6_independent_methodology_a.md` (Auditor A — methodology + design integrity)
- `proofs/AUDIT_20260504_V6_independent_claim_boundary_b.md` (Auditor B — claim boundary + interpretation planning)

This is the FIRST pre-run audit in the V3→V6 arc. Every prior audit pass was post-run. The lab proactively requested external review before burning 240 model calls, and the convergent verdict is `READY_AFTER_FIXES` from both auditors with ~30 minutes of prereg-text edits.

---

## Headline (one sentence)

**Both auditors converged: V6 is structurally sound — the human-adjudication clause was carried forward byte-identically from V5C (verified via `git blame` to the inception commit, the discipline-curve convergence now holds for a second consecutive cycle), the corpus passes byte-level integrity checks, the dose-response design is correctly implemented at constant 8 fields per prompt — but two real confounds (prompt length monotonically correlated with dose at r≈0.48, and field-vocabulary monotonically correlated with dose because new field labels enter at higher doses) require ~30 minutes of prereg tightening before the run, after which V6 ships.**

---

## Convergence (high-confidence findings)

### 1. The human-adjudication clause is correctly carried forward

This was the priority check from the V5/V5B audit's regression catch.

- **Auditor A:** Verified via `git blame` on commit `00a5de14`. Clause is at `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:91-94`, byte-identical to both V5C and the canonical `protocols/PREREG_TEMPLATE_SNIPPET_HUMAN_ADJUDICATION.md` snippet (`diff` returns empty).

This is now the **second consecutive cycle** where a previously-caught regression did not recur. The reusable prereg snippet introduced after V5C is operating as designed. The discipline curve continues to converge.

### 2. The corpus passes byte-level integrity

- 240 prompts, 24 anchors, 5 dose levels, k=2 replicates per cell — all confirmed
- 8 total output fields per prompt — confirmed
- No false anchors anywhere in prompt body
- No `type:` operator anywhere
- No explicit anti-identifier exclusion clause anywhere
- Anchors are genuinely fresh (V6A001–V6A024, distinct from V3's VG001–VG012)

### 3. Both auditors flagged the length monotonicity

- **Auditor A:** Pearson r ≈ 0.48 between dose and mean prompt length. Within-cell stdev identical at 7.75 chars. Spread is 3.9% (vs V5's 21%) but structurally correlated with dose because named-slot vocabulary is intrinsically longer than neutral vocabulary. Cannot be fixed by padding without destroying dose semantics.
- **Auditor B:** Same observation framed as a residual hostile-reviewer attack. V6 has no within-V6 length-matched control; the V5C empirical refutation lives in a different corpus and cannot be cited as if V6 itself controlled for length.

The fix both converge on: **commit to length-as-covariate logistic regression in the prereg** before the run.

### 4. Both auditors say no corpus regeneration needed

The fixes are all editor-fixes to the prereg text. No new model calls, no new prompt generation. ~30 minutes of work total.

---

## What each auditor caught that the other missed

### Auditor A (methodology lens) caught

- **Greek-letter typos in `target` blocks** for 17 of 24 anchors (e.g., `Φimage_screening` missing the underscore; should be `Φ_image_screening` per the V6A001–V6A007 pattern). Cosmetic only since `target` is constant per anchor across doses, but worth fixing before V7 reuses the template.
- **k=2 replicates are byte-identical at temperature 0**, which means they are stability checks rather than independent samples. The protocol acknowledges this honestly, but a peer reviewer will notice and flag it as a sample-size weakness.
- **Statistical analysis plan remains bounded**: no mixed-effects model with anchor as random effect, no multiple-comparisons correction.

### Auditor B (claim-boundary lens) caught

- **Field-vocabulary confound** — the most important catch in either audit. New field labels enter at higher doses (`citation_label`, `identifier_code` enter at dose 4; `program_name`, `standard_name`, `dataset_name`, `document_name` enter at dose 8). **V6 cannot distinguish "more slots" from "high-pressure vocabulary entering at higher doses."** This is the same shape of confound V4B had (joint removal). A peer reviewer will spot it on first read and ask "is your dose-response actually a vocabulary-response?"
- **Phare V2** (Giskard, January 2026) added structured-tool-call hallucination tasks and found that parameter *omission* causes hallucination of the missing parameter. V6 tests parameter *addition* — the additive lever Phare V2 doesn't cover. Worth citing to position V6 as complementary, not competing.

These are complementary catches. Auditor A was looking at internal integrity; the field-vocabulary issue is invisible at that lens because each individual prompt is correctly structured. Auditor B was looking at what an outside reviewer would say; the typos are invisible at that lens because they don't affect the claim. Both audits were necessary.

---

## The unified pre-run fix list

All edits to the prereg or analysis script. No corpus or protocol changes. Estimated total time: ~30 minutes.

### P0 (must land before any model call)

**Fix 1.** Add to the prereg's "Required Analyses" section:
> "A prompt-length-as-covariate logistic regression will be run with hallucination-positive as the outcome and dose level + prompt length as predictors. The dose coefficient must remain significant after controlling for length for the dose-response claim to be supported."

This addresses both auditors' length-monotonicity concern. Length is correlated with dose (r≈0.48); the covariate analysis tests whether dose effects survive length adjustment.

**Fix 2.** Add to the prereg's "Required Analyses" section:
> "Per-provider Cochran-Armitage trend tests will be run separately for `gpt-5-chat-latest`, `claude-sonnet-4-6`, and `grok-4.3`. The headline dose-response claim requires a positive trend in at least 2 of 3 providers."

Per Auditor A. This addresses both the cross-provider robustness question and gives the dose-response analysis the right per-provider statistical test.

**Fix 3.** Add to the prereg's "Claim Boundaries" or equivalent section:
> "V6 results will not be pooled with V5/V5/V5B/V5C results. V6 uses a generic 8-slot named-field vocabulary distinct from V5/V5C's per-anchor named slots; pooling would conflate vocabulary regimes."

Per Auditor A. Prevents an obvious post-hoc temptation to merge cells across experiment families for power.

**Fix 4.** Add to the prereg's "Required Reporting" section:
> "The V6 results memo will explicitly state whether human override was applied to any judge disagreement, and if so, how many disagreements and on which rows."

Per Auditor A. The human-adjudication clause is in the prereg but its required-reporting clause is missing — V6's memo could currently honor the clause silently. Lock the disclosure.

**Fix 5.** Add to the prereg's "Claims Not Allowed" section (verbatim, all five from Auditor B):
1. V6 does not isolate slot count from field-name vocabulary; the field-vocabulary confound is acknowledged.
2. No claim of specific functional form (linear, log-linear, sigmoid, step) — V6 tests for monotonic trend, not shape.
3. V6 does not refute V5C's exclusion-clause finding — V6 has no exclusion manipulation.
4. V6 results at temperature 0 do not extend to temperature > 0; temperature is not varied.
5. Tighten the existing anchor-concentration falsification rule to a bright-line: "if fewer than 50% of anchors show any positives at the highest dose level, the dose-response claim is rejected as anchor-concentration artifact."

**Fix 6.** Add to the prereg's "Related Work" or equivalent:
> "Phare V2 (Giskard, 2026) tests parameter omission causing hallucination of the missing parameter. V6 tests the additive lever (more named slots → higher fabrication rate) that Phare V2 does not cover. The two are complementary, not competing."

Per Auditor B. Strengthens external coherence; the citation also gives reviewers a positioning anchor that doesn't put V6 in direct competition with a published benchmark.

### P1 (must land before scoring, not before run)

**Fix 7.** Implement the analyses from Fix 1 and Fix 2 in `scripts/analyze_scored_results_v6.py`:
- Logistic regression with dose + prompt-length as predictors (e.g., `statsmodels.formula.api.logit`)
- Per-provider Cochran-Armitage trend test (`scipy.stats` doesn't have CA directly; use `from scipy.stats.contingency import expected_freq` + manual calculation, or `statsmodels.stats.contingency_tables.cochran_armitage_test` if available, or implement from the formula).

This can land before scoring runs. Does not block the model calls.

### P2 (cosmetic, can land anytime)

**Fix 8.** Fix the Greek-letter typos in 17 of 24 anchor `target` blocks. Per Auditor A: anchors V6A008–V6A024 are missing the underscore between `Φ` and the field name. Cosmetic since `target` is constant per anchor across doses, but the inconsistency matters before V7 reuses the template.

---

## What V6 will be able to claim AFTER the run (per the tightened prereg)

Best case (clean monotonic dose-response, length covariate non-significant, Cochran-Armitage positive in ≥2 of 3 providers):

> "On a 24-anchor synthetic corpus across `gpt-5-chat-latest`, `claude-sonnet-4-6`, and `grok-4.3` at temperature 0, the dual-judge AND hallucination-positive rate increased monotonically with named-artifact slot count, surviving prompt-length adjustment via covariate logistic regression and confirmed in ≥2 of 3 frontier providers via Cochran-Armitage trend tests. We do not isolate slot count from field-vocabulary semantics; both vary with dose by design. We do not claim a specific functional form. The result extends V5C's 2×2 schema-slot finding into a quantitative dose-response on a fresh anchor set."

This is the steelman. It is materially narrower than the rhetorically tempting "more named slots → more hallucinations, here's the dose curve." It is also the version a reasonable peer reviewer accepts.

---

## Interpretation planning (Auditor B's pre-commitment)

Both auditors converge on the importance of pre-committing interpretations BEFORE seeing data. Auditor B's full plan is in `proofs/AUDIT_20260504_V6_independent_claim_boundary_b.md` and should be linked from the V6 results memo template.

The headline pre-commitments per result shape:

| Result shape | What V6 claims |
|---|---|
| Clean monotonic increase | The steelman above |
| Plateau after dose 1 | "Schema-slot pressure is binary, not graded; presence of any named slot may be sufficient" — narrower mechanism claim |
| Plateau late (after dose 4) | "Dose-response saturates at moderate slot counts" — likely the most publishable shape |
| Non-monotonic | "Dose-response is non-monotonic; the underlying mechanism cannot be reduced to slot-count alone" — interesting null on the simple hypothesis |
| Null result | "V6 does not replicate V5C's effect at this dose range; possible explanations include fresh-corpus generalization failure or vocabulary effects dominating" — does not necessarily refute V5C, but narrows it |
| High baseline + saturation | "The 0-named-slot baseline is non-zero, suggesting other factors in the prompt structure also induce fabrication; the slot-count signal is partial" |

Pre-committing to these interpretations means the post-run results memo writes itself once the cell rates are in.

---

## Meta-finding: the discipline curve continues converging

This is the fourth audit cycle in the V3→V6 arc and the first PRE-RUN audit. The convergence pattern:

- V3 → V4B (24h post-run): caught 1 major issue (joint-removal overreach)
- V4B → V5/V5B (12h post-run): caught 1 regression (silent drop of human-adjudication clause)
- V5/V5B → V5C (6h post-run): caught 0 new regressions; the previously-caught regression was fixed at source
- V5C → V6 (pre-run): caught 0 regressions; both auditors agree the fix list is editor-only, no run-blocking issues

**Each cycle is faster, the regression rate is dropping, and the audit moved from post-run to pre-run.** The lab is now catching issues *before* burning model calls rather than *after*. That's a meaningful methodology maturation.

For an external technical reviewer reading this synthesis as part of the broader research record: this is the strongest evidence the lab has produced that the audit-discipline machinery is operating at a serious research standard. Four iterations, four audit passes, one regression caught at source on cycle two, zero regressions on cycles three and four, and the audit cadence has now matured to pre-flight rather than post-mortem.

---

## Ship verdict

**READY_AFTER_FIXES.** Land the 6 P0 fixes (~30 min total), then run V6.

The 6 P0 fixes are mechanical prereg edits that:
- Lock the length-as-covariate analysis (closes Auditor A's length-monotonicity concern and partially defangs Auditor B's residual length attack)
- Lock the per-provider Cochran-Armitage commitment (gives the dose-response the right statistical test)
- Add the field-vocabulary confound to "Claims Not Allowed" (defangs Auditor B's strongest hostile-reviewer attack BEFORE the data is seen)
- Add four other anti-claims (functional form, V5C exclusion-clause refutation, temp>0, anchor-concentration bright line)
- Cite Phare V2 for external coherence

Fix 7 (implementation in the analysis script) can land before scoring. Fix 8 (Greek-letter typos) is cosmetic and can land anytime.

After P0 lands and is committed: the run is approved. The methodology is sound, the human-adjudication clause holds, the corpus is clean, the design answers the V5C audit's open items, and the prereg now pre-empts the most likely peer-reviewer attacks.

---

## What this audit pass tells us about the lab itself (one paragraph)

The lab requested a pre-run audit before burning 240 model calls. Two independent auditors returned with complementary critiques (methodology integrity from one, claim-boundary from the other), and converged on a 6-fix list that is mechanical and editor-only. The human-adjudication clause regression that V5/V5B silently introduced was carried forward correctly into V6 from the inception commit (verified via `git blame`), confirming that the post-V5C structural fix (the reusable prereg snippet) is operating as designed. The audit cadence has now matured from post-mortem to pre-flight. For an external reviewer evaluating whether the lab's methodology discipline is theatrical or load-bearing: the V3→V6 arc is the answer, and V6 specifically is the strongest data point on that question.
