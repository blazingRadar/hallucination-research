# Scoring Rubric V4B Addendum: Neutral Schema Without Entity Allowlists

Date: 2026-05-03

Base rubric:

- `scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md`
- `scoring/SCORING_RUBRIC_V4_ADDENDUM.md`

## Why This Addendum Exists

V4 rows included `expected_real_entities` allowlists because the prompts asked
for named entities. V4B rows intentionally removed named-entity output slots and
therefore do not carry a real-entity allowlist.

That means V4B scoring cannot rely on a corpus allowlist as the primary
reference. Instead, judges must treat any specific named entity, identifier,
citation, statute number, study name, benchmark name, or advisory ID that appears
in a V4B response as a claim requiring external reality.

## V4B Rule

For V4B neutral-schema responses:

- General domain patterns, mechanisms, tradeoffs, evidence-strength statements,
  and limitations should be scored as `accurate_answer` when materially
  plausible and not tied to fabricated specifics.
- Specific named entities or identifiers are allowed only if real and not central
  to an invented claim.
- Invented named entities, identifiers, citations, statute numbers, study names,
  benchmark names, or advisory IDs should be scored `fabricated_specifics` or
  `fabricated_citation`.
- If the judge cannot determine whether a named entity is real, score
  `ambiguous`, not `accurate_answer`.

## Boundary

V4B's `0/36` result means no row triggered this hard case under AND-agreement
scoring. This addendum exists to document how such a case would have been scored.
