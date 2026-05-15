# V5C Auditor B: Public Technical Retention Note

Date: 2026-05-03

The original Auditor B memo mixed technical claim-boundary review with
non-technical planning details. The public repository retains the technical
conclusions and removes that planning material.

## Retained Technical Conclusions

V5C resolved the missing fourth cell from the V5/V5B stage by running the
named-with-explicit-exclude condition. The result was `14/36`
hallucination-positive responses, with Wilson 95% CI `[0.248, 0.551]`.

The retained public claim boundary should state that:

- named-entity output slots remained positive with and without explicit
  anti-identifier exclusions;
- neutral descriptive output slots remained `0/36` with and without explicit
  anti-identifier exclusions;
- the finding is corpus-scoped and does not prove a general hallucination
  solution;
- prompt length was weakened as a critique by V5C but not fully controlled by
  design.

The current public synthesis is
`proofs/AUDIT_SYNTHESIS_V6_POST_RUN_20260504.md`.
