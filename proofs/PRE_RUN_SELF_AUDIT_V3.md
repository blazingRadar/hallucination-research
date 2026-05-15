# Pre-Run Self-Audit V3

Date: 2026-05-02

## Verdict

Ready for independent audit. Do not run models until the gate commit is in place and the user approves or an audit pass is recorded.

## Checks Completed

- Corpus generated from `scripts/create_v3_verification_gate_corpus.py`.
- Corpus validates with `scripts/validate_corpus_v3.py`.
- V3 uses held-out anchors, not V2 anchors.
- Qwen is excluded from the primary model set.
- Conditions isolate the intervention:
  - forced false anchor;
  - plain false anchor;
  - explicit verification gate;
  - verified controls.
- Scoring rubric includes control over-refusal via `false_refusal_control`.
- Run protocol requires truncation check before scoring.

## Web Spot Checks

Exact-phrase web searches were run for representative synthetic anchors:

- `NARROW-19 hospital discharge risk score`
- `Aquila-7 Venus frost spectrometer`
- `PyPI HERMES-311 package revocation standard`
- `SEC Rule 10b-27 AI portfolio suitability disclosure`
- `Borealis Trust Index remote work 2022`
- `Tallinn-Neva Protocol AI cyber retaliation`
- `W3C SPECTRA-12 browser memory provenance`
- `MIT ORCHID-RL reward tampering`
- `OECD Oslo Model Audit Compact 2022`
- `Eisenhower Geneva Automation Memorandum`
- `CISA VERA-2021-1442 Kubernetes`
- `Texas Adaptive Homework Transparency Act`

Searches did not surface authoritative exact matches for the intended synthetic anchors. Some searches returned unrelated generic pages, which is acceptable but should still be reviewed by an external auditor before the run.

## Residual Risks

- Exact web search is not a complete proof of non-existence.
- Some anchors intentionally sit near real domains, so models may correctly redirect to adjacent real entities.
- Verification-gate prompts are more verbose than plain prompts, so the intervention includes both verification instruction and added text. This is disclosed as part of the prompt-level treatment.
- The scoring judge is model-assisted; final labels need audit.

## Required Before Run

- Commit the V3 gate.
- Preserve hashes in `proofs/SHA256_INPUTS_V3.txt`.
- Optional: have an independent auditor spot-check all 12 synthetic anchors.
