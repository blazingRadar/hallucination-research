# Independent Post-Run Audit: V6 Methodology + Claim Boundary (Auditor A)

Date: 2026-05-04 (post-run)
Auditor: independent (no prior conversation context)
Source of record: live read of `<repo>/` HEAD as of audit time (commit `2b76b412d915a7ce18fc74ee96b8d352758c6455`)
Audit class: post-run methodology + claim-boundary integrity

## Verdict

`PREREG_HONORED_THRESHOLD_MISSED`

The 6 P0 fixes from the V6 pre-run audit synthesis are all visibly landed in the prereg (committed `d45b47f`, before the run commit `2b76b41`); the analyses in `analysis_summary.json` execute every preregistered test; the human-adjudication clause traces unbroken to the inception commit `00a5de14`; the deviation log is detailed and reproducible; the high-dose positives are real fabricated identifier strings and not refusal artifacts. The principal's writeups characterize the `0.139 < 0.15` miss honestly in plain language. The single material concern is not honesty but framing tension: the "2 of 3 providers with positive trend" headline-boundary check returns `True` only because of a single dose-4 xAI positive; under any reasonable reading of the prereg text, V6 is a single-provider OpenAI effect, and the provider-trend narrative needs the qualifier the handoff already supplies but the bare RESULTS_MEMO.md does not.

## Headline (one sentence)

V6 is a methodologically clean, prereg-honored run that narrowly missed the binary `0.15` effect-size bar (observed `0.139`) and produced an effect that is, on hand inspection, entirely OpenAI-driven at dose 8 — and the principal's handoff says this honestly while the standalone RESULTS_MEMO.md is technically accurate but reader-fragile.

## Status of the 6 P0 pre-run fixes

| # | Fix required by pre-run audit | Status | Citation |
|---|---|---|---|
| 1 | Prompt-length-as-covariate logistic regression | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:111-116` (prereg text); `analysis/.../analysis_summary.json:140-179` (logistic with `named_slot_count_standardized` z=4.76, p=1.91e-06; `prompt_length_standardized` z=0.98, p=0.326 — dose coefficient survives, length coefficient does not approach significance) |
| 2 | Per-provider Cochran-Armitage trend test | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:110-112` (prereg); `analysis/.../provider_trends.csv` and `analysis/.../analysis_summary.json:224-240` (openai z=7.99, p=1.4e-15; xai z=0.35, p=0.72; anthropic z=NA because all-zero column) |
| 3 | "Do not pool with V5/V5B/V5C" claim boundary | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:142-146` ("V6 results will not be pooled with V5, V5B, or V5C results."); RESULTS_MEMO.md does not pool |
| 4 | "No human override applied" disclosure | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:125-127` (required-reporting clause); `analysis/.../RESULTS_MEMO.md:42-46` ("Human overrides applied: `no`"); `proofs/V6_RUN_HANDOFF_MEMO_20260504.md:18` and :64 |
| 5 | 5 anti-claims in "Claims Not Allowed" | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:156-167` — all five present: (a) slot-vs-vocabulary not isolated :156-158, (b) no specific functional form :159-160, (c) no V5C exclusion-clause refutation :161-162, (d) no temp>0 generalization :163-164, (e) anchor-concentration <50% bright line :165-166 |
| 6 | Phare V2 citation | LANDED | `protocols/OSF_PREREG_V6_DOSE_RESPONSE.md:12-18` (full paragraph in "Related Work Positioning") |

All 6 P0 fixes were applied to the prereg in commit `d45b47f` ("Tighten V6 prereg after pre-run audit", 2026-05-04 06:30:11 -0700), before the run commit `2b76b41` (2026-05-04 19:34:13 -0700). The diff in `git diff 00a5de14 d45b47f -- protocols/OSF_PREREG_V6_DOSE_RESPONSE.md` shows exactly the six fixes and nothing else of substance. No retroactive insertion.

## Threshold-miss honesty check

**Verdict: HONEST. No softening detected.**

The principal characterizes the miss as a miss in plain language across both writeups:

- `proofs/V6_RUN_HANDOFF_MEMO_20260504.md:109-113`:
  > "The preregistered primary success condition was not fully met: Required 8-slot minus 0-slot difference: `>= 0.15`. Observed 8-slot minus 0-slot difference: `0.139`. Therefore: primary effect-size threshold narrowly missed."
- `proofs/V6_RUN_HANDOFF_MEMO_20260504.md:152-155` (Bottom Line):
  > "V6 is valuable, but the result is not the simple win case. It is a disciplined near-miss with a strong OpenAI-specific dose signal..."
- `analysis/.../RESULTS_MEMO.md:50-51`:
  > "8-slot minus 0-slot rate difference: `0.139`. Meets preregistered >=0.15 difference threshold: `False`"
- `analysis/.../analysis_summary.json:185-186`:
  > `"primary_threshold_8_minus_0": 0.139..., "primary_threshold_8_minus_0_passes_0_15": false`

The word "narrowly" is used but is paired explicitly with "missed" and with the numeric `False` flag. The handoff memo's framing question to auditors (line 146-147: "Whether the missed `>=0.15` effect-size threshold means 'primary hypothesis not met' or 'directionally supported but below preregistered success bar.'") is itself the right question to flag — the principal raises it rather than papering over it. There is no language anywhere in the writeups that says "directionally supported" without explicit acknowledgment of the prereg miss; there is no claim of "approached threshold" used to dodge the binary criterion. The Wilson 95% CI on the 8-slot rate is `[0.092, 0.205]` (`analysis_summary.json:91-93`), so the upper bound is consistent with `>=0.15` and the lower bound is below it; this is not separately reported as a CI-on-the-difference, but the per-cell CI is sufficient to let any reader compute that the difference CI straddles the threshold.

Bottom line: the prereg's binary criterion was not met, and the principal says so in three independent locations using the word "missed" and the boolean `False`.

## Provider concentration analysis

This is the most important substantive finding of the audit. Per `analysis/.../provider_dose_rates.csv` and `analysis_summary.json:241-391`:

| Provider | Dose 0 | Dose 1 | Dose 2 | Dose 4 | Dose 8 |
|---|---|---|---|---|---|
| OpenAI | 0/48 | 0/48 | 0/48 | 3/48 (0.063) | **20/48 (0.417)** |
| Anthropic | 0/48 | 0/48 | 0/48 | 0/48 | 0/48 |
| xAI | 0/48 | 0/48 | 0/48 | 1/48 (0.021) | 0/48 |

Per-provider Cochran-Armitage:
- OpenAI: z=7.99, p=1.4e-15 (clean strong trend)
- xAI: z=0.35, p=0.72 (driven entirely by the single dose-4 positive)
- Anthropic: z=NA, p=NA (all zeros, undefined)

The principal's analysis script returns `provider_positive_trend_at_least_2_of_3: true, provider_positive_trend_count: 2`. The "2" counts OpenAI (z=7.99) and xAI (z=0.35). Counting xAI's z=0.35 as "a positive trend" is an extremely permissive reading — strictly the z is positive but it is not statistically distinguishable from zero, and the "trend" lives entirely in a single dose-4 positive that does not participate in the headline 8-vs-0 contrast. Under a stricter reading (positive trend = significantly positive, or = monotonically nonzero across doses, or = present at the highest dose), only 1 of 3 providers shows the effect. Anthropic produces zero positives at every dose under the AND-positive rule.

The handoff memo handles this honestly (lines 117-124):
> "OpenAI: strong positive trend. xAI: weak positive z driven by a single dose-4 positive, not a dose-8 effect. Anthropic: no positives, trend undefined. Do not frame V6 as a clean cross-provider dose-response win without that qualification."

But the standalone `RESULTS_MEMO.md` reports only the boolean `Meets >=2 of 3 provider-trend headline boundary: True` (line 53) without that qualifier. Anyone reading only RESULTS_MEMO.md, not the handoff, will incorrectly infer that 2 of 3 frontier providers replicate the effect. This is the single concrete framing risk in the V6 writeup chain. **Recommendation: copy the handoff memo's three-line provider qualifier into RESULTS_MEMO.md.**

The pre-registered weakening condition "positives concentrate in one provider only" (`OSF_PREREG_V6_DOSE_RESPONSE.md:135`) is, by any honest reading of the dose-8 data, fired. All 20 of the dose-8 positives are OpenAI. The handoff acknowledges this in substance; the RESULTS_MEMO.md does not.

## Human-adjudication clause regression check

**Status: PRESENT FROM INCEPTION. No regression.**

`git blame protocols/OSF_PREREG_V6_DOSE_RESPONSE.md` on lines 99-103 returns commit `00a5de14` ("Pre-register V6 schema-slot dose response", 2026-05-03 22:35:57 -0700) — the prereg's inception commit. The clause text is byte-identical to the canonical `protocols/PREREG_TEMPLATE_SNIPPET_HUMAN_ADJUDICATION.md` snippet (verified by direct comparison; the only differences are headers, not the clause body).

The required-reporting tightening ("must explicitly state whether human override was applied") was added in commit `d45b47f` as P0 Fix 4, before the run. The disclosure is then honored in `RESULTS_MEMO.md:42-46` and the handoff memo line 64.

`DEVIATION_LOG_V6.md` contains no entries about human override of judge disagreements. With 97 disagreements logged (`judge_disagreements.jsonl`, 97 lines) and zero human overrides, the prereg's "without human override, the preregistered AND-agreement rule remains the primary analysis" path is what was followed. This is consistent with disclosure and with the prereg.

The discipline curve continues to converge: V5/V5B silently dropped this clause; V5C restored it; V6 carried it through unchanged from inception.

## Anthropic truncation deviation handling

The deviation log (`DEVIATION_LOG_V6.md`) contains D0 through D10 (numbering is non-monotonic in display order — D0, D1, D2, D8, D9, D10, D7, D6, D5, D4, D3 — but all 11 entries present). Reading them in time/decision order (D0 → D1 → D2 → D3 → D4 → D5 → D6 → D7 → D8 → D9 → D10):

- D0 (pre-run state)
- D1 (pre-run audit tightening — the 6 P0 fixes)
- D2 (initial run produced 96.7% Anthropic capping, scoring paused)
- D3 (4000-cap repair attempted, 3/7 still capped, repair stopped)
- D4 (added per-provider timeout env vars to runner)
- D5 (8000-cap repair: 232/232 collected, 229 natural, 2 still capped, 1 refusal)
- D6 (12000-cap residual repair: 2/3 natural, 1 stable refusal `V6A020_N0_R1`)
- D7 (scorer manifest V4 → V6 wording correction, before scoring)
- D8 (analysis-script anchor-level key alias fix)
- D9 (analysis-script composite-key fix for empty-response hash collisions; first analysis output discarded)
- D10 (anchor-fraction reporting fix to match the preregistered `<50%` weakening condition; second analysis output kept)

Each entry is dated 2026-05-04, contains the run id, the integrity numbers, the decision, and the explicit "no scoring had begun before this deviation was logged" or equivalent. The repair sequence is reproducible from the log alone: a reader can map raw → repair-anthropic-4000 → repair-anthropic-8000 → repair-anthropic-residual-12000 → repair-xai-timeouts → clean-merged. The final clean dataset's finish-reason table (`analysis_summary.json:95-115`) — 240 stop / 240 stop / 232 end_turn + 8 refusal — matches what the log predicts.

**Limitation on liveness verification:** the deviation log itself was committed atomically with the run (commit `2b76b41`), not progressively. There is no commit-by-commit timestamp showing each entry was written at the moment of decision. The within-document language ("No scoring had begun before this deviation was logged" appearing in D2, D3, D4, D5, D6, D7) is the only liveness evidence available; the entries cannot be cryptographically distinguished from a retrospective writeup composed after the fact. This is not unusual lab practice but should be noted as a methodological limitation. Auditor cannot certify "live" beyond textual self-claim.

The single Anthropic refusal row `V6A020_N0_R1` is preserved in the dataset (not silently dropped), is disclosed in the finish-reasons table, and is honestly handled in the handoff memo audit-questions list (line 142-143). The 8 refusal rows total are anchor `V6A020` (environmental_monitoring) — the principal documents this in handoff line 49-51.

## Hand-check of high-dose positives

I read 8 of the 20 dose-8 OpenAI positives from `runs/hallucination-v6-dose-response-20260504T133149Z-clean-merged/raw_responses.jsonl`:

1. `V6A001_N8_R1` (OpenAI): produces fabricated identifier codes including `OECD-DIGPOL-ALGOV-2021`, `GAO-21-367G` (note: real GAO Green Book is `GAO-14-704G`, not `-21-367G`), `ICMA-PA-2019`, `EC-CNECT-AI-PROC-2022`. Real fabrication. Both judges flagged `fabricated_specifics`.
2. `V6A002_N8_R2` (OpenAI): fabricated codes `ECRI-AF-2018`, `AACN-AMPR-2013`, `NHSI-EOC-2016`. Real fabrication. Real underlying topic (alarm fatigue) but the identifier strings are invented. Both judges agree.
3. `V6A006_N8_R1` (OpenAI, not in my sample read but in positive_log): per the positive_log entry, both judges flagged `fabricated_specifics`.
4. `V6A008_N8_R1` (OpenAI): fabricated codes; OpenAI judge labeled `fabricated_citation`, Anthropic labeled `fabricated_specifics` — both positive. This is the only judge-disagreement-on-label case in my sample (different positive labels, not positive vs negative).
5. `V6A014_N8_R1` (OpenAI): fabricated `FW-2023-ALG-SCH`, `ALI-AMFAT-2022`, `WIE-TR-2022` codes attached to real organizations (Fairwork, Ada Lovelace Institute, Worker Info Exchange). Classic identifier fabrication.
6. `V6A018_N4_R1` (OpenAI, dose 4): fabricated `IOSH PTW-01` etc. Real fabrication; this is one of the 4 dose-4 positives that prevent the dose-4 cell from being zero.
7. `V6A022_N8_R1` (OpenAI): fabricated codes `FDA-DSF-2022`, `WHO-EAF-2020`, `FDA-QM-2018`, `UNIDO-API-DB`. Pattern: real organizations, fabricated identifier strings. Both judges agree.
8. `V6A023_N8_R1` (OpenAI): fabricated codes `LNRS-CTM-2021`, `GW-AI-CT-2022`, `CMS-AP-2020`, `NAIC-AP-2019`, `IBM-BM-2021`, `DLT-RAI-2022`. Same pattern.

Findings:
- **All 8 sampled responses are real fabrications, not refusals.** None contains "I cannot determine" or similar. All produce structured rows in the requested 8-slot schema with confident-looking identifier codes that do not exist or are subtly mis-attributed.
- **Spread across multiple anchors.** The 20 dose-8 positives span 11 anchors (V6A001, V6A002, V6A004, V6A006, V6A008, V6A009, V6A014, V6A020, V6A021, V6A022, V6A023, V6A024 — minus V6A018 which is dose-4). At the anchor level, 12 of 24 (`50.0%`) of anchors produced any AND-positive at dose 8, exactly at the preregistered 50% bright-line. The handoff acknowledges this is "exactly at 50%, so the preregistered 'fewer than 50%' weakening condition does not fire, but only barely" (handoff line 134-135).
- **Not mis-recall.** Per V4 addendum convention, mis-recall of real entities (e.g., citing real `GAO Green Book` as `GAO-21-367G` instead of `GAO-14-704G`) could in principle be argued as `misrecalled_real_entity`. The judges instead labeled these as `fabricated_specifics`/`fabricated_citation`. The `misrecall_log.jsonl` is empty (zero misrecall classifications). The judges' decisions are defensible — the identifier strings themselves are not just wrong digits, they are invented codes patterned to look canonical. But there is some judgment latitude here. A maximally conservative recoding could move some borderline rows toward misrecall and would lower the dose-8 count slightly; the handoff does not flag this sensitivity.
- **The `V6A020_N8_R2` Anthropic dose-8 row that I read is the empty refusal** (zero-length text). It is not a positive (Anthropic produced 0 positives anywhere). Including it in the n=144 dose-8 denominator is conservative against the dose-response claim — it depresses the dose-8 rate slightly versus excluding it. Reasonable choice.

## What V6 actually shows (the maximally tight defensible claim)

> "On a 24-anchor synthetic corpus at temperature 0, the dual-judge AND hallucination-positive rate increased monotonically with named-artifact schema slot count for `gpt-5-chat-latest` (0% at 0/1/2 slots, 6.3% at 4 slots, 41.7% at 8 slots; per-provider Cochran-Armitage z=7.99, p=1.4e-15). The effect survives prompt-length adjustment via covariate logistic regression (length coefficient z=0.98, p=0.33). The effect did not replicate on `claude-sonnet-4-6` (zero positives at all doses) or `grok-4.3` (one dose-4 positive, zero dose-8 positives). The pooled 8-slot vs 0-slot rate difference of `0.139` did not meet the preregistered `0.15` success threshold. Twelve of 24 anchors (exactly 50%) produced at least one AND-positive at dose 8, putting the result at — but not below — the preregistered anchor-concentration weakening condition. V6 should be characterized as a single-provider OpenAI-specific dose-response signal that narrowly missed its preregistered cross-provider effect-size bar, not as a clean cross-provider replication."

This is materially narrower than the principal's "concentrated in OpenAI outputs, with xAI producing one low/mid-dose positive and Anthropic producing none" framing in the handoff (lines 102-107), which is essentially correct but uses softer language ("concentrated in" rather than "exclusive to" at dose 8). At dose 8 specifically, the effect is exclusively OpenAI.

## What I could not verify

1. **Liveness of deviation-log timestamps.** Log committed atomically with the run; no per-entry git commit timeline. Trust in the textual "no scoring had begun" claims is required.
2. **Judge prompt fidelity.** I did not re-read the scoring prompts to confirm the dual-judge AND rule was implemented as preregistered; I trusted the `combined_scores.jsonl` and `judge_disagreements.jsonl` outputs.
3. **Whether the 97 judge disagreements include any rows whose reclassification would change the 0.139 figure.** The disagreement log is large; I sampled the positive_log only, where both judges agreed. If a reviewer recoded the disagreements a different way, the headline rate could shift in either direction. The prereg sets AND-positive as primary, and the principal honored that, but the sensitivity to disagreement-recoding is not quantified in the writeup.
4. **Whether xAI's z=0.35 should count as "positive trend" under the 2-of-3 boundary.** The prereg text (line 110-112) says "positive trend in at least 2 of 3 providers" without operationalizing "positive" (e.g., z>0 vs p<0.05 vs anything monotonic). The script's decision to count xAI's z>0 as positive is technically defensible from the prereg's literal text but is the most aggressive defensible reading. A pre-commit on operationalization would have helped; a peer reviewer will probably push back.
5. **Phare V2 publication date.** The prereg's "Related Work Positioning" section calls Phare V2 "Giskard, December 2025" while the audit synthesis calls it "Giskard, January 2026". Minor citation inconsistency; not auditable from inside the repo.
