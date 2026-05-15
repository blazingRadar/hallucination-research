# Ethics and Risk Note V1

Date: 2026-05-02

## Human Subjects

This experiment does not recruit human subjects and does not collect human-subject data.

## Main Risk

The main risk is generating fabricated citations, fabricated legal claims, or fabricated scientific claims that could be copied without context.

## Mitigations

- False outputs must remain in clearly labeled experimental folders.
- Public writeups must mark fabricated examples as fabricated.
- Do not fabricate damaging claims about living private individuals.
- Avoid prompts that ask models to invent quotes from real private people.
- API keys and provider metadata must be redacted before publication.

## Publication Boundary

It is acceptable to publish:

- prompts;
- raw model outputs;
- labels;
- scoring rubric;
- analysis scripts.

It is not acceptable to publish:

- secrets;
- API keys;
- private local environment paths if not needed;
- misleading excerpts detached from their experimental label.

