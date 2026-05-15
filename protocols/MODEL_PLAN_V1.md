# Model Plan V1

Date: 2026-05-02

## Purpose

Lock the intended model set before the hallucination prompt-structure experiment is run.

## Primary Model Set

The experiment should run against four model families:

| Slot | Provider | Planned model | Credential source | Current key status |
|---|---|---|---|---|
| M1 | OpenAI | current frontier / production chat model selected before run | `external environment file` | present |
| M2 | Anthropic | current Claude frontier / production model selected before run | `external environment file` | present |
| M3 | xAI / Grok | current Grok model selected before run | shell env `XAI_API_KEY` or `GROK_API_KEY` | present |
| M4 | Local Qwen | `qwen/qwen3.5-35b-a3b` or closest installed Qwen model | local OpenAI-compatible endpoint | not running at setup check |

## Local Qwen Requirement

Local Qwen is part of the planned experiment, not a post-hoc optional comparison.

Expected local endpoint:

```text
http://127.0.0.1:1234/v1/chat/completions
```

Expected local model id:

```text
qwen/qwen3.5-35b-a3b
```

If the exact model is unavailable, the deviation must be recorded in `proofs/DEVIATION_LOG_V1.md` before any run using the replacement model.

## Pre-Run Availability Checks

Before model execution, run:

```bash
python3 scripts/check_model_environment.py
```

The experiment should not start until:

- OpenAI key is found;
- Anthropic key is found;
- xAI/Grok key is found or the xAI slot is explicitly deferred;
- local Qwen endpoint returns a model list or the deviation log records why local Qwen is unavailable.

## Credential Handling

Do not print, commit, or store secret values.

Run artifacts may record:

- key present / missing;
- provider name;
- model name returned by API;
- base URL host;
- response metadata.

Run artifacts must not record:

- API key values;
- authorization headers;
- raw env files.

## Model Version Locking

The model names used for the final run must be written to:

```text
runs/<run_id>/run_manifest.json
```

If a provider returns a more specific model snapshot id, preserve that returned id.

