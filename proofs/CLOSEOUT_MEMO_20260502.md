# Lab Close-Out Memo

Date: 2026-05-02
Decision: **CLOSE LAB. NO V4. NO SHIP OF V3 RESULTS.**
Author: lab principal (after independent two-auditor review)

## What this memo is

The canonical record that the hallucination prompt-structure lab is being shut down after V3, what was actually learned, what was not learned, and what is and is not reusable. It supersedes any forward-looking framing in earlier memos.

This is a close-out, not a pause. There is no V4. There is no shipping of V3 results. The repository is preserved as a portfolio artifact of how the lab was run, not as a publication-track project.

## What we set out to test

Whether false asserted premises and forced explanatory modes materially increase hallucination rates relative to open-structure and true-premise controls, and (V3 extension) whether an explicit verify-before-answering instruction reduces the false-premise hallucination rate.

## What V3 actually established

`gpt-5-chat-latest` accepts and elaborates planted false premises on a 12-anchor synthetic corpus (8/12 forced false-anchor, 5/12 plain false-anchor positive). An explicit "verify this exists first; if not, don't infer details" instruction zeroed the rate to 0/12 on the same corpus, while 6/6 verified-control prompts using the same scaffold remained substantively useful (so the gate is not a refuse-everything artifact). `claude-sonnet-4-6` stayed ≤1/12 across all conditions.

This is a small-sample replication of Chain-of-Verification (Dhuliawala et al., arXiv:2309.11495, Sept 2023). The mechanism — instruct the model to verify a premise before generating dependent claims — has been a known result for ~2.5 years. V3 confirms it on a different (smaller, hand-built, anchor-paired) corpus under unusually strict preregistration.

The methodology discipline (corpus byte-pinned to SHA, deviation log, post-run self-audit catching its own bugs, two independent post-hoc auditors) is real and worth preserving as a process artifact. It is not a research finding.

## What V3 did NOT establish

The four claims that would have made V3 worth shipping are unsupported by the design:

1. **Cross-vendor claim ("Claude robust, OpenAI vulnerable").** The judge model is `gpt-5-chat-latest` scoring `gpt-5-chat-latest` outputs (`scored/.../scoring_manifest.json`). Same-vendor scoring of a cross-vendor comparison is the headline critique against the headline finding. n=12 per cell with no confidence intervals reported makes this worse, not better. See `proofs/AUDIT_20260502_V3_independent_claim_boundary_a.md`.
2. **Mechanism vs phenomenon.** V3 shows that the *specific verification-gate prompts the lab wrote* dropped the rate to 0 on this corpus. It does not show the gate works because of verification semantics rather than added length, added caution, or anchor-rejection prompting. No length-or-caution-matched control was run.
3. **Generalisation.** 12 hand-built synthetic anchors (fake CVEs, statutes, missions, benchmarks). No claim about real-entity hallucination, no claim about non-named-entity premises, no claim about other domains.
4. **Statistical headroom.** Wilson 95% upper bound on the 0/12 verify-gate rate is 0.243, above the prereg's ≤0.20 threshold. Forced-minus-verify reduction CI lower bound sits essentially at the prereg's minimum effect of 0.30. The result is consistent with a real effect; it is not safely above the preregistered bar.

## Methodology breach to record honestly

The V1 preregistration's "must not replace the final label without human adjudication" clause was silently dropped in V3 — single-judge (gpt-5-chat-latest) scoring was used without a second scorer or human adjudicator, and this change was not recorded in `proofs/DEVIATION_LOG_V3.md`. Auditor A flagged this. It is a real preregistration deviation. Recording it here so the trail is honest. No retroactive edit is being made to the deviation log; the silent omission is itself part of the audit record.

## Why we're closing instead of running V4

Two independent auditors converged on a single half-day fix (re-score with `claude-sonnet-4-6` as a second judge, compute Cohen's κ, run the strict-sensitivity table, add Wilson CIs). That fix would let V3 ship cleanly. We are choosing not to do it because:

- Even with the fix, the strongest version of the result is still a small-n replication of CoVe.
- The cross-vendor framing — the only part that would make the work feel novel — is not what the design was built to test, and the 12-anchor synthetic corpus is too thin a base to argue it from even with two judges.
- The opportunity cost of one more half-day on a confirmed re-derivation is higher than the credibility gain of shipping it. A clean close-out memo on this lab plus the audit trail preserved is itself the more credible artifact — it demonstrates the ability to run a disciplined experiment, recognise it as a re-derivation, and stop without sunk-cost continuation.

## What is reusable

The following are deliberately preserved as transferable artifacts for future labs:

- `protocols/OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md` — preregistration template structure.
- `protocols/RUN_PROTOCOL_V1.md`, `protocols/ANALYSIS_PLAN_V1.md` — gate-first run discipline.
- `scoring/SCORING_RUBRIC_V1.md` — rubric structure (single-judge scoring is a known weakness, fix in any reuse).
- `proofs/DEVIATION_LOG_V3.md` — the cadence of recording deviations during a live run.
- `proofs/POST_RUN_SELF_AUDIT_V3_20260502.md` — the structure of a post-run self-audit that catches one's own bugs.
- The two-auditor independent post-hoc cadence used at close-out (`proofs/AUDIT_20260502_V3_independent_*.md`) — convergence between two genuinely independent auditors is itself a high-confidence signal worth using again.

## What is NOT to be picked up without a new question

- The V3 results as-is. Do not extract figures or quote rates from `proofs/RESULTS_MEMO_V3_VERIFICATION_GATE_20260502.md` in any external writeup. The results memo is preserved for trail completeness, not for citation.
- The cross-vendor framing on this corpus. The design does not support it.
- V4 of this experiment. There is no V4 unless the underlying question changes. "More n on the same corpus with the same rubric" is not a new question.

## Pointers

- Independent claim-boundary audit: `proofs/AUDIT_20260502_V3_independent_claim_boundary_a.md`
- Independent lab-direction audit: `proofs/AUDIT_20260502_V3_independent_lab_direction_b.md`
- V3 results (preserved, not for citation): `proofs/RESULTS_MEMO_V3_VERIFICATION_GATE_20260502.md`
- V3 self-audit (preserved): `proofs/POST_RUN_SELF_AUDIT_V3_20260502.md`
- V3 deviation log (preserved, plus the methodology breach noted above): `proofs/DEVIATION_LOG_V3.md`
- Original observation paper (separate from the V3 follow-up, preserved as superseded): `archive/EXPLORATORY_PAPER_V1_20260502_SUPERSEDED.md`

## Status

`hallucination-research` is **CLOSED** as of 2026-05-02. The git history is intact. The repository is preserved as a portfolio artifact of audit discipline and a bounded public research record.

No further commits are planned beyond this close-out commit.
