# Hallucination V2 Full Run Summary

Run ID: `hallucination-v2-full-20260502T145359Z`

Status: PASS raw collection

Raw collection:
- Total responses: 200
- Provider errors: 0
- Responses per provider: 50 each
- Providers/models:
  - `openai`: `gpt-5-chat-latest`
  - `anthropic`: `claude-sonnet-4-6`
  - `xai`: `grok-4.3`
  - `local_qwen`: `qwen/qwen3.5-35b-a3b`

Condition counts:
- `false_anchor_forced`: 80
- `false_anchor_plain`: 40
- `open_structure_control`: 40
- `true_premise_control`: 40

Protocol controls:
- Corpus: `corpus/PROMPT_CORPUS_V2.jsonl`
- Corpus SHA256: `8807cc82817c82b6eddde7bb047c511f1db6575590c05f68ef2a2dd41373a292`
- Seed: `prompt_structure_hallucination_v1_20260502`
- Temperature: 0 for all providers
- Credential values saved: false

Artifacts:
- `run_manifest.json`
- `prompt_order.json`
- `raw_responses.jsonl`
- `errors.jsonl`
- `sha256s.txt`

Boundary:
This artifact proves raw response collection completed under the locked v2 corpus and model plan. It does not yet prove the hypothesis or tell-word claims; those require the pre-registered scoring and analysis pass.
