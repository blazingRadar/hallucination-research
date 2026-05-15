# Publication Manifest

This repository is a public research artifact for a narrow hallucination failure mode: named output-schema fields can pressure models to invent plausible entities when the domain is real but recall is weak.

## Included

- Prompt corpora for V1 through V6.
- Raw model-response logs needed for reproducibility.
- Derived scoring and analysis outputs.
- Preregistration, protocol, audit, deviation, and result memos.
- Current plain-text paper draft and figures.
- Scripts used to validate corpora, run model calls, adjudicate outputs, and analyze results.

## Claim Boundary

The current claim is the V6 claim boundary in `proofs/AUDIT_SYNTHESIS_V6_POST_RUN_20260504.md`. The result is strongest for the included corpus and provider mix. It is not presented as a general hallucination solution, a production evaluation suite, or a cross-provider law.

## Hygiene Notes

- API keys and environment files are not included.
- Scripts read credentials from process environment or an external env file configured by `HALLUCINATION_LAB_ENV_FILE`.
- Local absolute paths in historical memos were replaced with `<repo>` or external-environment wording where appropriate.
- Raw responses are retained intentionally because they are part of the reproducibility surface. Some raw logs include provider response IDs, model fingerprints, service-tier fields, inference-region fields, cost tick fields, finish reasons, and model-generated reasoning-like text. They may also include model-generated mentions of organizations, benchmarks, roles, and acronyms that appear in the prompt domain or output. These are retained as non-secret run evidence needed to audit provenance, cost, and response behavior; API keys and environment contents are not included.
- Superseded work is preserved under `archive/` and labeled as superseded.
- Stale PDF/HTML paper exports and parked future-lab notes are not part of the public release surface.
- Locked preregistration and protocol files are preserved as historical run records. The current public claim boundary is the README, this manifest, the plain-text paper draft, and the V6 post-run synthesis.

## Verification Surface

The repository includes corpus validators and analysis artifacts, not a full regression-test suite. The publication check for this cleanup compiled the Python scripts, reran the corpus validators, parsed JSON and JSONL files, checked Markdown links, and verified the latest V6 evidence hashes.
