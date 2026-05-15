# Cross-Lab Mechanism Synthesis

Date: 2026-05-04
Status: THEORY NOTE — not a preregistered result

## Purpose

This note records the emerging cross-lab interpretation after V4B, V6, and the
separate ARC digit-token investigation. It is a synthesis hypothesis, not a new
statistical claim.

## Three Labs, One Candidate Mechanism

### V4B: Named Entity Anchors

False entities in the input created fabrication pressure.

When the prompt contained a named-but-fabricated entity, models often completed
the surrounding structure as if the entity existed. Removing the false entity
and replacing named slots with descriptive slots drove the observed
hallucination-positive rate to the floor in that corpus.

### V6: Named Output Slots

Even with `do_not_invent` explicitly stated, named output slots created
fabrication pressure.

Fields such as:

- `identifier_code`
- `citation_label`
- `program_name`
- `standard_name`
- `dataset_name`
- `document_name`

increased pressure toward code-shaped, citation-shaped, and named-artifact
outputs. In V6, the dual-judge AND-positive rate rose from `0/144` at 0, 1,
and 2 named slots to `4/144` at 4 named slots and `20/144` at 8 named slots.

The important point is that this occurred under:

`constraints: { answer_from_general_knowledge, do_not_invent, mark_uncertain_when_unsure }`

So the named field itself appears to compete with the explicit instruction.

### ARC Digit-Token Investigation

Digit tokens appear to activate arithmetic priors that interfere with pure
symbol-mapping tasks.

In the ARC task discussed on 2026-05-04, GPT-4o failed or refused many original
integer-grid presentations of a pure lookup-table task, while a semantically
neutral word-token version succeeded. The working interpretation is that digit
tokens carry strong arithmetic priors, and those priors can override the
example-implied symbolic mapping.

## Unified Mechanism Hypothesis

The candidate mechanism across the three settings:

> The model does not simply read the instruction first and then fill the slot.
> The slot name, typed field, or token representation activates a prior
> distribution before the instruction fully constrains generation.

Examples:

- `identifier_code` activates probability mass toward code-shaped strings.
- `citation_label` activates probability mass toward citation-shaped strings.
- `score: 1` can activate evaluation/pass-score priors.
- Digit tokens such as `8`, `1`, and `3` can activate arithmetic-relation
  priors.

The concise formulation:

> LLMs are completion engines first. Format is not neutral. Every named slot,
> typed token, and structured field is a prior-activation event, and that prior
> can compete with or defeat the explicit instruction.

## Claim Boundary

This synthesis does not replace the narrower V6 result.

The V6 preregistered claim remains bounded by:

- synthetic 24-anchor corpus;
- three model providers;
- temperature 0;
- generic V6 field vocabulary;
- no pooling with V5/V5B/V5C;
- no isolation of slot count from field-vocabulary semantics.

The cross-lab mechanism is a research direction. It still needs a purpose-built
experiment that varies:

- input false-anchor pressure;
- output schema-slot pressure;
- token/representation pressure;
- instruction strength;
- and model family.

## Practical Research Frame

The technical bridge:

> Across three independent investigations, failures appeared when the
> representation itself carried a strong completion prior: false named anchors,
> named output fields, and digit tokens. The common lesson is that prompt
> format is not neutral; representation choices can activate priors that the
> explicit instruction does not reliably suppress.
