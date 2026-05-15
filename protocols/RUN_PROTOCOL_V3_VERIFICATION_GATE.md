# Run Protocol V3: Verification Gate

Date: 2026-05-02

## Directive

Run every prompt in `corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl` independently against OpenAI and Anthropic. Preserve raw outputs and metadata. Do not inspect intermediate responses to change the corpus, prompt wording, model selection, scoring labels, or thresholds.

## Command Shape

Expected command:

```bash
./scripts/run_model_lab.py \
  --corpus corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl \
  --seed verification_gate_v3_20260502 \
  --providers openai,anthropic \
  --max-tokens 1400 \
  --run-id hallucination-v3-verification-gate-<timestamp>
```

## Pre-Run Checklist

- V3 corpus validates.
- V3 prereg committed.
- V3 scoring rubric committed.
- Input hashes committed.
- API keys available through environment only.
- No model responses inspected before gate commit.

## Model Call Rules

- One prompt per API call.
- No prior conversation state.
- Temperature 0.
- Store finish reason and usage.
- Store returned model identifier.
- Store prompt order.
- Store hashes.
- Store provider errors without silent retry.

## Retry Rules

Retry only transport/provider errors. Do not retry because a model refused, hallucinated, answered weakly, or produced an inconvenient result.

## Post-Run Rules

- Hash raw run artifacts.
- Secret-scan run artifacts.
- Check truncation rate before scoring.
- If truncation is asymmetric or exceeds 10% in any model-condition cell, log a deviation before scoring.
- Score into a derived directory only.
