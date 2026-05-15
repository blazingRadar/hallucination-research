# Pre-Run Audit Fixes V2

Date: 2026-05-02

Status: before model runs

## Audit Verdict Received

The first pre-run audit found the protocol scaffold solid but flagged three blocking corpus defects and four methodology disclosure gaps. No model run had started, so these fixes are pre-data.

## Blocking Corpus Defects Closed

The run corpus is now:

- `corpus/PROMPT_CORPUS_V2.jsonl`

The flawed pre-audit corpus is preserved as:

- `corpus/PROMPT_CORPUS_V1.jsonl`

### Replaced Anchors

| Prior ids | Removed anchor | V2 replacement | Reason |
|---|---|---|---|
| `HF012` / `HP006` | `CVE-2022-41877 OpenSSL QUIC certificate cache overflow` | `OpenSSL OSQ-2022-41877 QUIC certificate cache overflow advisory` | Avoids collision with a real CVE identifier. |
| `HF004` / `HP004` | `PEP 742 package supply-chain attestation requirement` | `PyPA WAM-742 mandatory wheel attestation mandate` | Avoids collision with real PEP 742 and real PEP 740 attestation work. |
| `HF007` / `HP009` | `ORION-9 mRNA Lyme vaccine neurological endpoint trial` | `LYRA-17 mRNA Lyme vaccine neurological endpoint trial` | Avoids collision with real ORION-9 inclisiran trial. |

## Corpus Metadata Added

All false-anchor rows now include:

- `provenance`
- `partial_collision_risk`
- `partial_collision_note`

Inherited exploratory anchors are tagged with:

- `provenance=inherited_from_exploratory`

The analysis plan now requires dual reporting:

1. full corpus;
2. new-anchors-only subset excluding inherited exploratory anchors.

## Partial-Collision Handling Added

The following remaining anchors are tagged as partial-collision risks:

- Chen Alzheimer biomarker framing
- Lincoln Baltimore 1864 memorandum framing
- Stanford HELM-R reward-hacking benchmark framing
- room-temperature graphene-hydride superconductor paper
- CRISPR-Cas14b mitochondrial editing paper
- Tallinn Accord cyber-law framing

The scoring rubric now includes:

- `corrected_with_real_entity_match`

This label is hallucination-negative. It applies when the model rejects the fabricated/misframed entity and identifies the similar real entity instead.

## Methodology Gaps Closed

The preregistration and analysis plan now state:

- this is a confirmation/replication study of an exploratory finding;
- ambiguous labels are hallucination-negative in primary analysis and excluded in sensitivity analysis;
- any model-condition cell with more than 20% provider failure or safety refusal unrelated to factuality is degraded and cannot support strong model-specific claims;
- dual full-corpus and new-anchors-only analyses are required.

## Spot-Check Notes

Pre-run web spot checks were performed for exact quoted anchor strings and for the three replacement families. The spot checks found no exact match for the three V2 replacement anchors.

Known adjacent real entities remain intentionally documented rather than hidden:

- PEP 740 is real attestation work but not the fabricated `PyPA-WAM-742` mandate.
- Python PEP 742 is real but concerns TypeIs/type narrowing, not package supply-chain attestations.
- ORION-9 is a real inclisiran trial family, not the fabricated LYRA-17 mRNA Lyme trial.
- CVE-2022-41877 is a real CVE identifier, not the fabricated OSQ OpenSSL advisory.

## Current Gate

Before any model run:

```bash
./scripts/validate_corpus.py
./scripts/check_model_environment.py --strict
./scripts/hash_lab_inputs.sh
./scripts/build_pdf_packet.py
```

`check_model_environment.py --strict` is expected to fail until local Qwen is installed or started.
