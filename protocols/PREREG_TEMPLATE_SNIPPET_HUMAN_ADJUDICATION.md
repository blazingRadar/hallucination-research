# Prereg Template Snippet: Human Adjudication on Judge Disagreement

Status: reusable required snippet for future hallucination-lab preregistrations

## Purpose

The V3 audit caught that a human-adjudication safeguard from V1 was silently
dropped. V4B restored it. V5 and V5B then silently dropped it again, and the
V5/V5B audit caught the regression. V5C included the clause from the prereg's
creation commit.

Future preregistrations should copy this snippet rather than rewriting the
policy from memory.

## Required Clause

Dual-judge scoring:

- OpenAI judge: `[model_name]`
- Anthropic judge: `[model_name]`

Primary outcome: AND-agreement hallucination-positive.

Disagreements must be logged. A human audit may override a disagreement if the
published claim relies on that row or if the disagreement changes the public
claim boundary. Without human override, the preregistered AND-agreement rule
remains the primary analysis.

## Required Reporting

Every results memo must report:

- judge primary-label agreement
- judge positive-label agreement
- disagreement count
- path to disagreement log
- whether any human override was applied

If no human override was applied, say so explicitly.
