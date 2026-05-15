# V6 Protocol: Schema Slot Dose-Response Stress Test

Date: 2026-05-04
Status: PRE-RUN, AUDIT REQUIRED BEFORE MODEL CALLS

## Purpose

V5 through V5C closed the 2x2:

- named slots without exclusions: `10/36`
- named slots with exclusions: `14/36`
- neutral slots without exclusions: `0/36`
- neutral slots with exclusions: `0/36`

V6 asks whether the effect scales with the number of named-artifact schema
fields on a fresh corpus.

## Design

Corpus:

`corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl`

Structure:

- 24 fresh anchors, none reused from V3-V5C.
- 5 dose conditions per anchor: 0, 1, 2, 4, or 8 named schema slots.
- 2 identical prompt replicates per anchor-condition pair.
- 8 total output fields in every condition.
- Constant uncertainty constraint in every prompt.
- No false anchor in any prompt.
- No `type:` task operator in any prompt.
- No explicit `proper_nouns`, `identifiers`, or `citations` exclusion clause.

Rows:

`24 anchors x 5 conditions x 2 replicates = 240 prompts`

Models:

- OpenAI: `gpt-5-chat-latest`
- Anthropic: `claude-sonnet-4-6`
- xAI: `grok-4.3`

Temperature: `0`

Total model calls:

`240 prompts x 3 providers = 720 response calls`

## Run Commands

Do not run before audit approval.

Suggested execution after approval:

```bash
RUN_ID="hallucination-v6-dose-response-$(date -u +%Y%m%dT%H%M%SZ)"
python3 scripts/run_model_lab.py \
  --run-id "$RUN_ID" \
  --corpus corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl \
  --providers openai,anthropic,xai \
  --max-tokens 1800
```

If any provider has more than 5% `max_tokens` truncation, pause scoring and log
a deviation before rerunning the capped subset with a higher token cap.

## Scoring Commands

After the model run and only after run-integrity checks:

```bash
python3 scripts/adjudicate_scores_v4.py runs/$RUN_ID --judge openai --json-retries 1
python3 scripts/adjudicate_scores_v4.py runs/$RUN_ID --judge anthropic --json-retries 1
python3 scripts/analyze_scored_results_v6.py \
  runs/$RUN_ID \
  scored/<OPENAI_SCORE_RUN> \
  scored/<ANTHROPIC_SCORE_RUN>
```

## Stop Conditions

Stop before scoring and write a deviation if:

- any provider has non-provider-error missing responses;
- any condition loses more than 5% of rows to provider errors;
- any provider has more than 5% capped/truncated rows;
- the corpus SHA does not match `proofs/SHA256_INPUTS_V6.txt`;
- a model version differs materially from the preregistered model names.

## Claims Not Allowed

- Do not claim production tool-schema proof.
- Do not claim generality beyond the fresh V6 corpus.
- Do not claim dose-response if only the 8-slot cell is high and intermediate
  cells are flat.
- Do not claim exclusion clauses are irrelevant; V6 does not vary exclusions.
- Do not claim repeated samples are independent in the same way as independent
  anchors. Report anchor-level sensitivity.
- Do not pool V6 with V5/V5B/V5C; V6 uses different generic slot vocabulary.
- Do not claim V6 isolates slot count from field vocabulary; both vary with
  dose by design.
- Do not claim a specific functional form for the dose curve.
- Do not claim temperature-0 results generalize to higher-temperature sampling.
