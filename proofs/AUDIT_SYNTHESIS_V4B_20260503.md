# V4B Audit Synthesis: Public Technical Retention Note

Date: 2026-05-03

This file replaces an earlier internal synthesis that mixed technical audit
findings with non-technical planning. The public repository retains
the technical conclusions and removes the strategy material.

## Inputs

- `proofs/AUDIT_20260503_V4B_independent_claim_boundary_a.md`
- `proofs/AUDIT_20260503_V4B_independent_novelty_b.md`

## Retained Technical Conclusions

V4B produced a real `0/36` result under the neutral-schema condition. The audit
found no evidence that the result was merely a refusal artifact or scoring
artifact.

The original "third independent injection vector" framing was too strong. V4B
jointly changed several things: it replaced named-entity output slots with
descriptive ones, added explicit anti-identifier exclusions, removed false
anchors, and changed the task frame. The supported claim is therefore a
joint-removal result, not an isolated single-variable mechanism claim.

The audit also identified concrete cleanup items:

- disclose the explicit `exclude:` clause as a confound;
- avoid treating degenerate single-class kappa as strong reliability evidence;
- fix mislabeled generated result memos;
- check prompt-length and response-usefulness concerns;
- document the V4B-specific scoring interpretation.

## Effect On Later Work

V5, V5B, and V5C were run to decompose the V4B joint manipulation. V6 later
tested a fresh-corpus dose-response design. The current claim boundary is in
`proofs/AUDIT_SYNTHESIS_V6_POST_RUN_20260504.md`.
