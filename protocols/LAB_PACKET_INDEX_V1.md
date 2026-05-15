# Lab Packet Index V1

Date: 2026-05-02  
Status: ready for second pre-run audit; model runs not yet executed

## Purpose

This packet formalizes the next hallucination experiment before any new model responses are collected.

The study tests whether false premises embedded as asserted context, especially with forced explanatory modes, produce materially higher hallucination rates than true-premise and open-structure controls.

## Authoritative Protocol Files

- `protocols/OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md`
- `protocols/ASPREDICTED_SUMMARY_V1.md`
- `protocols/PREREG_CHECKLIST_ANSWERS_V1.md`
- `protocols/RUN_PROTOCOL_V1.md`
- `protocols/ANALYSIS_PLAN_V1.md`
- `protocols/ETHICS_AND_RISK_NOTE_V1.md`
- `protocols/DATA_DICTIONARY_V1.md`
- `protocols/MODEL_PLAN_V1.md`
- `scoring/SCORING_RUBRIC_V1.md`

## Corpus

- `corpus/PROMPT_CORPUS_V2.jsonl`

`corpus/PROMPT_CORPUS_V1.jsonl` is preserved as the pre-audit draft. It is not the run corpus.

Validated shape:

- total prompts: 50
- false-anchor forced-mode: 20
- false-anchor plain: 10
- true-premise controls: 10
- open-structure controls: 10
- false-anchor rows include provenance metadata
- partial-collision-risk rows are tagged before model execution

Validation command:

```bash
./scripts/validate_corpus.py
```

Observed pre-run result:

```text
rows=50
status=PASS
```

## Scripts

- `scripts/validate_corpus.py`
- `scripts/check_model_environment.py`
- `scripts/build_pdf_packet.py`
- `scripts/hash_lab_inputs.sh`

No model runner has been executed yet.

## Proofs

- `proofs/SHA256_INPUTS_V1.txt`
- `proofs/DEVIATION_LOG_V1.md`
- `proofs/PRE_RUN_AUDIT_FIXES_V2.md`

## Generated Exports

Generated PDF/HTML exports were used during the early packet workflow but are
not part of the current public repository surface. The source Markdown files in
`protocols/`, `proofs/`, and `scoring/` are the maintained artifacts.

## Current Claims Allowed

- The lab has a preregistered follow-up protocol.
- The 50-prompt corpus shape validates.
- The scoring rubric and analysis plan are specified before model runs.
- The prior exploratory paper remains exploratory and is not upgraded into a confirmed result by this packet alone.
- The v2 corpus has resolved the first pre-run audit's known blocking collisions.

## Current Claims Not Allowed

- The hypothesis has been confirmed.
- Models do or do not hallucinate under any condition in this new corpus.
- Tell words generalize.
- The corpus ground truth has been externally source-verified item by item.

## Next Gate

Before running models, perform a pre-run audit:

1. Verify the false anchors are actually false.
2. Verify true-premise controls are actually true and not ambiguous.
3. Verify open-structure controls do not accidentally contain false anchors.
4. Verify the scoring rubric is not tilted toward the hypothesis.
5. Verify the corpus is not too easy in one condition and too hard in another.
6. Verify the planned model set and local Qwen endpoint before execution.
