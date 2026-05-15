# V5C Audit Synthesis: Public Technical Retention Note

Date: 2026-05-03

This file replaces an earlier internal synthesis that mixed technical audit
findings with non-technical planning. The public repository retains the
technical conclusions and removes that planning material.

## Inputs

- `proofs/AUDIT_20260503_V5C_independent_methodology_a.md`
- `proofs/AUDIT_20260503_V5C_independent_claim_boundary_b.md`

## Retained Technical Conclusions

V5C ran the missing named-with-explicit-exclude cell and produced `14/36`
hallucination-positive responses. This strengthened the schema-slot pressure
account because the named-slot condition remained positive even with explicit
anti-identifier language.

The audit confirmed that the V5C result was integrated into the retained public
claim boundary and that the missing-cell caveat no longer applied after V5C.

V5C also weakened the prompt-length critique empirically: the
named-with-exclude prompts were slightly shorter on average than the
neutral-with-exclude prompts, yet the named-with-exclude condition produced
positives and the neutral-with-exclude condition did not.

## Remaining Gaps At This Stage

V5C did not provide a fresh-corpus replication, a named-slot dose-response, or a
full vocabulary-versus-slot-count isolation. Those questions moved into V6 and
the deferred V7 design space. The current claim boundary is in
`proofs/AUDIT_SYNTHESIS_V6_POST_RUN_20260504.md`.
