# Pre-Run Audit Request V1

Date: 2026-05-02

## Audit Question

Is the hallucination prompt-structure lab ready to run, or does the preregistration/corpus/scoring setup contain defects that would make the result misleading?

## Files To Inspect

- `protocols/OSF_PREREG_PROMPT_STRUCTURE_HALLUCINATION_V1.md`
- `protocols/ASPREDICTED_SUMMARY_V1.md`
- `protocols/PREREG_CHECKLIST_ANSWERS_V1.md`
- `protocols/LAB_PACKET_INDEX_V1.md`
- `protocols/DATA_DICTIONARY_V1.md`
- `protocols/RUN_PROTOCOL_V1.md`
- `protocols/ANALYSIS_PLAN_V1.md`
- `scoring/SCORING_RUBRIC_V1.md`
- `corpus/PROMPT_CORPUS_V2.jsonl`
- `proofs/SHA256_INPUTS_V1.txt`
- `proofs/PRE_RUN_AUDIT_FIXES_V2.md`

Note: `corpus/PROMPT_CORPUS_V1.jsonl` is preserved as the pre-audit draft and should be inspected only as provenance for the v2 changes, not as the run corpus.

## Specific Audit Tasks

1. Check whether the hypothesis is falsifiable.
2. Check whether the corpus conditions isolate the intended variables.
3. Check whether any false-anchor prompt may accidentally be true or too ambiguous.
4. Check whether any true-premise control is wrong or too underspecified.
5. Check whether the scoring rubric lets the scorer rescue the hypothesis.
6. Check whether the analysis plan can pass even if the mechanism is false.
7. Check whether non-claims are strong enough.
8. Check whether an external reader could reproduce the run from the packet.

## Expected Audit Output

Return:

- verdict: `READY`, `READY_AFTER_FIXES`, or `NOT_READY`
- blocking findings;
- non-blocking findings;
- exact file/line references where possible;
- recommended changes before model runs.
