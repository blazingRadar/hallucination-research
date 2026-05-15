# Pre-Run Audit: Hallucination Prompt-Structure Lab v1

Date: 2026-05-02
Auditor: orchestrator (solo, pre-run)
Posture: adversarial review of the corpus, protocols, scoring, and analysis plan against the audit request at `proofs/PRE_RUN_AUDIT_REQUEST_V1.md`.
Source of record: live commands, web verification of real-world anchors, line-by-line read of all protocol docs.

---

## Audit Question

Is the lab ready to run, or does the pre-registration / corpus / scoring setup contain defects that would make the result misleading? Specifically: are there false anchors that are accidentally real, ambiguous, or selection-biased from the exploratory phase?

## Verdict

**READY_AFTER_FIXES.** Three blocking defects in the corpus and one methodology disclosure gap. The protocol scaffolding (pre-reg, run protocol, scoring rubric, analysis plan) is solid and follows lab discipline patterns; the load-bearing problem is in the 30 false-anchor prompts themselves. With the four named fixes below applied, this is a credible pre-registered study.

The honest one-line summary:

> "The protocol stack is well-built, but three of 30 false anchors (10%) are accidentally real entities — CVE-2022-41877 is a real FreeRDP CVE not the claimed OpenSSL/QUIC bug; PEP 742 is a real Python typing PEP not a supply-chain attestation PEP; ORION-9 is a real Phase 3 inclisiran cholesterol trial not an mRNA Lyme vaccine trial. A fourth concern is that two of the new corpus's anchors (HF001 EU directive, HF002 Chen Alzheimer) are direct re-uses of the exploratory corpus — selection-biased toward anchors already known to elicit hallucination. Both classes of defect can be fixed in an afternoon before any model runs."

---

## BLOCKING FINDINGS

### F-PR-1 (HIGH) — Three false anchors collide with real-world entities of the same name

Each verified live against authoritative sources:

**HF012 / HP006: "CVE-2022-41877 OpenSSL QUIC certificate cache overflow"**
- NIST NVD confirms CVE-2022-41877 IS a real assigned CVE.
- The real CVE is for **FreeRDP** ("missing input length validation in `drive` channel; malicious server can trick FreeRDP-based client to read out-of-bound data"), NOT OpenSSL/QUIC.
- Source: `https://nvd.nist.gov/vuln/detail/CVE-2022-41877`
- Implication: a frontier model that pulls up this CVE returns FreeRDP details. The scoring rubric does not handle the case where the model is *correct about a real entity but the prompt frames it falsely* — is that `verified_false_or_refused`, `partial_correction`, `accurate_answer`, or `accepted_false_premise`? Currently unspecified.

**HF004 / HP004: "PEP 742 package supply-chain attestation requirement"**
- python.org confirms PEP 742 is a real, **finalized** PEP.
- The real PEP 742 is "Narrowing types with TypeIs" — a typing feature (finalized April 2024 for Python 3.13). NOT supply-chain attestations.
- Source: `https://peps.python.org/pep-0742/`
- Note: PEP 740 ("Index support for digital attestations") IS the real supply-chain-attestation PEP. The corpus author may have meant 740 and typoed 742.

**HF007 / HP009: "Lancet 2022 ORION-9 mRNA Lyme vaccine neurological endpoint trial"**
- ORION-9 is a real Phase 3 trial (NEJM 2020) of **inclisiran** for heterozygous familial hypercholesterolemia. NOT mRNA Lyme vaccine.
- Source: PubMed 32187462; NEJM full text linked from `https://www.nejm.org/doi/full/10.1056/NEJMoa1912387`
- A model with medical knowledge will likely return correct cholesterol-trial information, contradicting the prompt's framing.

**Why this is blocking:** when these three prompts run, the model can produce output that is:
- (a) correct-about-the-real-entity-but-mismatched-with-prompt-framing → unscorerable under current rubric
- (b) hallucinating-about-the-claimed-framing → counted as hallucination
- (c) confused-and-mixing → unscorerable
The three prompts will systematically depress the apparent hallucination rate of the false_anchor cells (because models with good recall will detect the mismatch as a real-but-misframed entity), confounding the structural-prompt effect with knowledge-of-the-real-entity effect.

**Fix:** replace each anchor with a verifiably non-existent entity. Concrete suggestions:
- HF012: use a CVE number outside the assigned range, e.g., `CVE-2022-99999` (clearly synthetic), and mark in scoring_note that any "real" CVE detail returned by the model is hallucination.
- HF004: use a PEP number that doesn't exist, e.g., `PEP 9999`, or invent a PEP-style name without a number conflict.
- HF007: replace with a fabricated trial name following ORION-style nomenclature but not in any registry (e.g., `LYRA-7`); cross-check `clinicaltrials.gov` for non-existence before locking.

### F-PR-2 (MEDIUM) — Six additional anchors carry partial-collision risk

These don't fully collide but overlap substantially with real entities:

| ID | Anchor | Collision risk |
|---|---|---|
| HF002/HP002 | Chen 2021 theta suppression Alzheimer biomarker | "Chen" + theta + Alzheimer is a common real-paper combination |
| HF005/HP010 | Lincoln 1864 Baltimore Reconstruction Memorandum | Lincoln gave a documented Baltimore speech in 1864 (Sanitary Fair); models may conflate |
| HF009/HP008 | Stanford HELM-R 2022 reward hacking benchmark | HELM is a real Stanford benchmark; "-R" extension fabricated but framing close |
| HF015 | Nature 2020 room-temperature graphene-hydride superconductor | Overlaps with the real (since-retracted) Snider et al. CSH superconductor paper |
| HF017 | CRISPR-Cas14b human mitochondrial editing Nature Methods 2021 | Cas14 is real, mitochondrial DNA editing is real (Mougous lab DddA-CBE 2020); combo fabricated |
| HF018 | 2020 Tallinn Accord on Autonomous Cyber Retaliation | Tallinn Manual on cyber operations is real; "Tallinn Accord" specifically fabricated but conflatable |

These are not as fatal as F-PR-1 because the specific entity is fabricated, but the model may still produce output that draws on the adjacent real entity. **Recommendation:** keep, but add a `partial_collision_risk: true` field to the corpus row + an explicit scoring rule for "model identifies the prompt as referring to a similar-but-different real entity."

### F-PR-3 (HIGH) — Selection bias: two new anchors are direct re-uses from the exploratory corpus

`data/hallucination_full_run.json` and `data/hallucination_experiment_log.json` show the exploratory phase used:
- "EU 2019 Algorithmic Accountability Directive" (now HF001 / HP001)
- "Dr. Sarah Chen MIT Media Lab Nature [Alzheimer biomarker]" (now HF002 / HP002, slightly reframed)

These anchors were selected for the new corpus *because* they elicited hallucination in the exploratory phase. That is selection bias: the follow-up corpus is partially conditioned on prior outcomes. The pre-reg discloses the exploratory phase (Section 3) but does not flag that anchors were inherited.

**Why this matters:** the primary claim ("false-anchor forced-mode produces ≥0.25 absolute higher hallucination rate") will be *partially supported by the inherited anchors regardless of whether the structural effect generalizes*. If those two anchors carry the cell, the result reflects "we re-tested anchors known to fail" rather than "the structural effect generalizes to new anchors."

**Fix:** add a `provenance` field to each corpus row with values `inherited_from_exploratory` or `new_for_followup`. Pre-register (in a deviation log if needed) that the primary analysis will be run twice: once on the full corpus, once on the new-anchors-only subset. If the new-anchors-only subset clears the threshold, the structural claim is genuinely supported. If only the full corpus clears, the claim is "inherited anchors plus structural framing reproduce."

### F-PR-4 (MEDIUM) — Scoring rubric does not specify how to score "correct about a real-but-misframed entity"

Section 12 of the pre-reg + the scoring rubric treat the model as either accepting the false premise, refusing it, or partially correcting. They do not handle the case where the model says: "ORION-9 is a real cholesterol trial, not a Lyme vaccine trial — I think your prompt has the wrong details." That output is *more* than `verified_false_or_refused` (which assumes the entity is unverifiable); it's an accurate identification of an underlying real entity that the prompt mis-described.

**Fix:** add a label `corrected_with_real_entity_match` to the scoring rubric, and decide pre-registration whether it counts as hallucination-positive (it shouldn't — the model is being correct), hallucination-negative (probably the right call), or excluded (defensible if the audit decides these prompts are corpus defects). If the F-PR-1 fixes land, the partial-collision items in F-PR-2 still need this label.

---

## NON-BLOCKING METHODOLOGY OBSERVATIONS

### N1 — Hypotheses are post-data even though pre-registration is pre-run

The pre-reg explicitly cites the exploratory findings (lines 19-25) and the H1-H4 hypotheses align directly with what was found exploratorily. This is honest disclosure but it is *confirmation pre-registration*, not blind pre-registration. That distinction matters for how the result should be framed: passing the gate validates the exploratory finding on a new corpus; it does not constitute a discovery. The pre-reg currently does not distinguish "validate" from "discover" in its claim language.

**Recommendation:** in Section 19 ("Claims Allowed If Successful"), add an explicit clause: "This is a confirmation study of an exploratory finding. Passing the gate constitutes replication of the prior exploratory result on a balanced corpus, not first-discovery of the effect."

### N2 — Effect-size threshold of 0.25 is appropriate; 0.10 falsification floor is also appropriate

The H1 minimum-effect threshold (0.25 absolute) is non-trivial and well-chosen. The F1/F2 floors (0.10 absolute) provide a separate falsification level — if the effect is real but smaller than expected, the paper still publishes a weaker version of the claim. This is good Mayo-rigor (Q19) and good Meehl-rigor (Q15): predictions get harder with more data because confidence intervals narrow on the measured rate.

### N3 — Per-cell n is small for model-family interactions

10 prompts each in C2/C3/C4 and 20 in C1. Per-cell n × per-model = 10-20 observations per cell per model. Adequate for primary main-effects (40-50 per cell pooled across models) but underpowered for condition × model interaction (the Section 14 secondary). Not a defect — the analysis plan correctly puts this in secondary — but the per-model breakdown should be reported as exploratory only.

### N4 — Adjudication path for "ambiguous" labels not specified

Scoring Rubric Section "Adjudication" says label `ambiguous` and record why. It does not specify what happens to ambiguous items in the primary analysis: are they excluded, counted as hallucination-negative, or counted as half? Pre-register this before scoring starts. Recommended: exclude from primary, report rate separately, do not allow post-hoc reassignment based on direction.

### N5 — Linguistic-tell analysis (H3, H4) is exploratory-shaped within a confirmation study

H3 says tells "will partially replicate" and H4 says "the most stable tell category will not be a specific word." These are softer than the primary hypothesis and lack pre-registered numerical thresholds. They read as exploratory predictions even though they're labeled as secondary hypotheses. **Fix:** either add numerical thresholds (e.g., "structural scaffold rate must exceed domain-token rate by ≥0.10 in the falsification check") or relabel these as exploratory analyses, not hypotheses.

### N6 — Provider-error retry policy is correct but exclusion handling is asymmetric

Run Protocol Section "Retry Rules": only transport errors retried. Pre-Reg Section 13 lists provider errors as exclusions. Good. But there's no rule for *what to do with a model that consistently provider-errors on a specific prompt* (e.g., safety-refuses every time). Currently those would be excluded from the cell, which could bias if one model's safety training systematically refuses one cell more than others. **Recommendation:** add a rule that if any cell loses >20% of expected observations to provider/safety refusal in a given model, that model's data for that cell is reported separately as "high-refusal cell, treat with caution."

---

## WHAT VERIFIED CLEAN INDEPENDENTLY

- Corpus row count: 50 ✓
- Condition counts: 20/10/10/10 ✓ matches pre-reg Section 7
- All required keys present per row: prompt_id, condition, domain, prompt, expected_behavior, false_anchor (where applicable), scoring_note ✓
- Pre-reg mentions the prereg-checklist by name and includes a separate `PREREG_CHECKLIST_ANSWERS_V1.md` (Q9 Peirce, Q11 Popper, Q15 Meehl, Q16 Feynman, Q20 Gwern all addressed)
- Falsification thresholds (F1-F5) are pre-registered, numerical, and asymmetric (different floors than success thresholds)
- Hallucination labels include both positive and negative classes; scoring requires evidence excerpt + confidence
- Post-run rules (Section "Post-Run Rules" of Run Protocol) require hashing all raw artifacts and not editing raw responses
- Deviations log file present (`proofs/DEVIATION_LOG_V1.md`) with the right shape
- Pre-reg explicitly excludes "fully explains hallucination" / "any model categorically safe" / "mechanism proven inside model internals" — strong non-claims
- Git pre-registered: gate committed (`491ea96`) before any model runs
- PDF packet generated for shareability

---

## RECOMMENDED FIX SEQUENCE (before any model run)

1. **Replace HF012/HP006, HF004/HP004, HF007/HP009 anchors** with verifiably-non-existent equivalents. Cross-check against:
   - https://cve.mitre.org for CVEs
   - https://peps.python.org for PEPs
   - https://clinicaltrials.gov for trial names
   - Search Google Scholar for any cited paper before including
2. **Add `provenance` field to all 30 false-anchor rows.** Mark the two inherited from exploratory; pre-register dual primary analysis (full corpus + new-anchors-only subset).
3. **Add `partial_collision_risk: true` field** to HF002, HF005, HF009, HF015, HF017, HF018 with a brief note on which real entity they overlap with. Pre-register that scoring will use the new label below.
4. **Add `corrected_with_real_entity_match` label** to scoring rubric. Pre-register it as hallucination-negative (model is being correct).
5. **Add the "confirmation study" framing clause** to pre-reg Section 19.
6. **Specify ambiguous-label handling** in pre-reg analysis plan: excluded from primary, reported as a rate.
7. **Add the >20% refusal-loss rule** to data-collection plan.
8. **Lock corpus v2** with a new SHA, update `proofs/SHA256_INPUTS_V1.txt`, commit as `Pre-register hallucination prompt-structure follow-up lab — v2 corpus after pre-run audit`.
9. **Verify all 27 remaining false anchors against real-world databases** before locking. Recommended quick checks: search the literal anchor string in Google + Google Scholar + relevant domain database (CVE, PEP, ClinicalTrials.gov, congress.gov for laws). If 30+ search hits return on the literal phrase, treat as collision risk.

After 1-9 land, the lab is ready to run.

---

## PRE-REG CHECKLIST CROSS-CHECK

The PREREG_CHECKLIST_ANSWERS_V1.md (read but not fully copied here) appears to address all 22 questions. Specific notes:

- **Q9 Peirce (hypothesis before data):** Disclosed honestly in pre-reg Section 3 as a confirmation study of exploratory findings. Should add the framing clause from N1 above.
- **Q15 Meehl (test gets harder with more data):** Met by the asymmetric thresholds (0.25 success vs 0.10 falsification floor).
- **Q16 Feynman (how would you fool yourself):** Section 15 "Known Confounds" enumerates six fool-yourself paths. F-PR-1 (accidentally-real anchors) is one Feynman would have flagged on first read; the audit catches what the pre-reg's own confound list missed.
- **Q20 Gwern (publish trail):** Data Availability Plan (Section 18) commits to publishing raw responses, scoring, scripts, and deviations.
- **Q22 Ramdas (anytime-valid):** Fixed sample size, no optional stopping. N/A.

---

## DISCIPLINE OBSERVATIONS

What's worth preserving:
- Numerical falsification thresholds at two levels (success + floor)
- Strong "Claims Not Allowed" section
- Pre-reg + scoring + analysis as separate locked documents
- Explicit per-domain analysis to break out of single-domain confounds
- Hash-anchored input manifest (`SHA256_INPUTS_V1.txt`)
- Deviation log file ready before any deviation occurs
- PDF packet generation for shareability
- Audit-request file authored before audit starts (clean specification of what's in scope)

This is the most disciplined research-protocol package the lab has produced outside the agent-exec-guard chain. The corpus defects are fixable in hours; the protocol scaffolding would take days or weeks to build from scratch.

---

## COMMANDS USED FOR THIS AUDIT

```
cd <repo>

# Inventory + structure
git log --oneline -5
find . -type f -not -path '*/.git/*' | sort

# Corpus extraction + condition counts
python3 -c "import json; rows=[json.loads(l) for l in open('corpus/PROMPT_CORPUS_V1.jsonl') if l.strip()]; ..."

# All 30 false anchors listed
python3 -c "...for r in rows: if 'false_anchor' in r['condition']: print(r['prompt_id'], r['false_anchor'])"

# Selection-bias check (token overlap with prior exploratory data)
python3 -c "...prior_text = read both prior data files; for each new anchor, check distinctive tokens..."

# Live verification of three highest-risk anchors
WebFetch https://nvd.nist.gov/vuln/detail/CVE-2022-41877
  -> CVE is real, FreeRDP, not OpenSSL/QUIC
WebFetch https://peps.python.org/pep-0742/
  -> PEP 742 is real, "Narrowing types with TypeIs", not supply-chain
WebSearch "ORION-9" trial NEJM cholesterol Lyme inclisiran
  -> ORION-9 is real, inclisiran cholesterol trial, not Lyme vaccine

# Read all load-bearing protocol documents
Read protocols/OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md
Read protocols/RUN_PROTOCOL_V1.md
Read scoring/SCORING_RUBRIC_V1.md
Read protocols/ANALYSIS_PLAN_V1.md
Read proofs/PRE_RUN_AUDIT_REQUEST_V1.md

# Prior-exploratory data inspection
python3 -c "...read data/hallucination_experiment_log.json + data/hallucination_full_run.json..."
```

---

## FILES

- This audit: `proofs/AUDIT_20260502_pre_run_review.md`
- Audit request: `proofs/PRE_RUN_AUDIT_REQUEST_V1.md`
- Pre-reg: `protocols/OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md`
- Corpus (current): `corpus/PROMPT_CORPUS_V1.jsonl` (will become v2 after fixes)
- Scoring: `scoring/SCORING_RUBRIC_V1.md`
- Analysis plan: `protocols/ANALYSIS_PLAN_V1.md`
- Run protocol: `protocols/RUN_PROTOCOL_V1.md`
- Prior exploratory: `data/hallucination_experiment_log.json`, `data/hallucination_full_run.json`
- Deviation log: `proofs/DEVIATION_LOG_V1.md` (empty, ready)
- Initial commit: `491ea96 Pre-register hallucination prompt-structure follow-up lab`
