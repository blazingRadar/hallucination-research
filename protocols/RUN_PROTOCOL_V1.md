# Run Protocol V1

Date: 2026-05-02

## Directive

Run each prompt in `corpus/PROMPT_CORPUS_V2.jsonl` independently against each configured model. Preserve raw outputs and metadata. Do not inspect intermediate results to change prompts, scoring, or model selection.

## Expected Result Shape

The run produces:

- `runs/<run_id>/raw_responses.jsonl`
- `runs/<run_id>/run_manifest.json`
- `runs/<run_id>/prompt_order.json`
- `runs/<run_id>/errors.jsonl` if any
- `runs/<run_id>/sha256s.txt`

## Pre-Run Checklist

- Corpus reviewed for obvious ambiguity.
- Prereg committed.
- Scoring rubric committed.
- Model list fixed.
- API keys available through environment only.
- Output directory empty.
- Prompt order generated with fixed seed.
- Corpus v2 validation passes after pre-run audit fixes.

## Model Call Rules

- One prompt per API call.
- No system prompt unless provider requires one; if required, preserve it.
- No previous conversation context.
- Temperature 0 when available.
- Record model version returned by provider.
- Record provider errors without retrying silently.

## Retry Rules

Retry only provider transport errors. Do not retry because the answer was unexpected, refused, or weak.

## Post-Run Rules

- Hash all raw artifacts.
- Do not edit raw response files.
- Run scoring into a separate derived directory.
- Preserve scoring script version hash.
