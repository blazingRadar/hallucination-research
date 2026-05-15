# V5 + V5B Audit Synthesis: Public Technical Retention Note

Date: 2026-05-03

This file replaces an earlier internal synthesis that mixed technical audit
findings with non-technical planning. The public repository retains
the technical conclusions and removes the strategy material.

## Inputs

- `proofs/AUDIT_20260503_V5_V5B_independent_methodology_a.md`
- `proofs/AUDIT_20260503_V5_V5B_independent_framing_b.md`

## Retained Technical Conclusions

V5 and V5B materially tightened the V4B result.

- V5 ran a same-batch paired ablation and reduced the risk that V4B was only
  comparing unrelated runs.
- V5B removed the explicit anti-identifier exclusions from the neutral arm and
  still produced `0/36`, weakening the concern that the exclusion clause alone
  explained the V4B result.
- The judge-agreement reporting moved away from degenerate single-class kappa
  and toward raw agreement with real disagreements.

The audit also caught a methodology regression: the human-adjudication clause
that had been restored after the V3 audit was silently omitted from V5 and
V5B preregistrations. That catch became part of the lab's later audit discipline.

## Remaining Gaps At This Stage

The V5/V5B audit left four important gaps:

- the named-with-explicit-exclude cell had not yet been run;
- no dose-response on named-slot count had been run;
- prompt length had not been controlled by design;
- the result still used the same 12-anchor synthetic corpus.

V5C and V6 were run later to address some, but not all, of these gaps. The
current claim boundary is in
`proofs/AUDIT_SYNTHESIS_V6_POST_RUN_20260504.md`.
