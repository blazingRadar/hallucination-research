#!/usr/bin/env python3
"""Preflight model credentials and local endpoint availability.

This script intentionally reports only presence/absence metadata. It must not
print API key values or raw environment file contents.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = Path(os.environ.get("HALLUCINATION_LAB_ENV_FILE", Path.home() / ".openclaw" / ".env"))
LM_STUDIO_MODELS_URL = "http://127.0.0.1:1234/v1/models"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"


def load_env_like(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().strip('"').strip("'")
        value = value.strip().strip('"').strip("'")
        values[key] = value
    return values


def present_len(name: str, env_file_values: dict[str, str], aliases: list[str]) -> dict[str, Any]:
    for key in aliases:
        value = os.environ.get(key)
        if value:
            return {"name": name, "present": True, "source": "process_env", "length": len(value)}
    for key in aliases:
        value = env_file_values.get(key)
        if value:
            return {"name": name, "present": True, "source": str(DEFAULT_ENV_FILE), "length": len(value)}
    return {"name": name, "present": False, "source": None, "length": 0}


def get_json(url: str, timeout: float = 1.5) -> tuple[bool, Any, str | None]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return True, json.loads(body), None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return False, None, str(exc)


def model_names_from_openai_compatible(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if not isinstance(data, list):
        return []
    names = []
    for item in data:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            names.append(item["id"])
    return names


def model_names_from_ollama(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return []
    models = payload.get("models")
    if not isinstance(models, list):
        return []
    names = []
    for item in models:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            names.append(item["name"])
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--strict", action="store_true", help="exit nonzero unless all planned slots are ready")
    args = parser.parse_args()

    env_values = load_env_like(args.env_file)
    checks = {
        "credentials": [
            present_len("openai", env_values, ["OPENAI_API_KEY"]),
            present_len("anthropic", env_values, ["ANTHROPIC_API_KEY", "ANTHROPIC API KEY"]),
            present_len("xai_grok", env_values, ["XAI_API_KEY", "GROK_API_KEY", "XAI API KEY", "GROK API KEY"]),
        ],
        "local_endpoints": [],
    }

    lm_ok, lm_payload, lm_error = get_json(LM_STUDIO_MODELS_URL)
    lm_models = model_names_from_openai_compatible(lm_payload) if lm_ok else []
    checks["local_endpoints"].append(
        {
            "name": "lm_studio_openai_compatible",
            "url": LM_STUDIO_MODELS_URL,
            "reachable": lm_ok,
            "models": lm_models,
            "qwen_present": any("qwen" in model.lower() for model in lm_models),
            "error": None if lm_ok else lm_error,
        }
    )

    ollama_ok, ollama_payload, ollama_error = get_json(OLLAMA_TAGS_URL)
    ollama_models = model_names_from_ollama(ollama_payload) if ollama_ok else []
    checks["local_endpoints"].append(
        {
            "name": "ollama",
            "url": OLLAMA_TAGS_URL,
            "reachable": ollama_ok,
            "models": ollama_models,
            "qwen_present": any("qwen" in model.lower() for model in ollama_models),
            "error": None if ollama_ok else ollama_error,
        }
    )

    qwen_ready = any(endpoint["qwen_present"] for endpoint in checks["local_endpoints"])
    credential_ready = all(item["present"] for item in checks["credentials"])
    checks["overall_ready"] = bool(credential_ready and qwen_ready)
    checks["notes"] = [
        "Secret values are intentionally omitted.",
        "Anthropic is also checked under the legacy key name with spaces found in .openclaw/.env.",
        "Local Qwen is ready only if an OpenAI-compatible or Ollama endpoint lists a Qwen model.",
    ]

    print(json.dumps(checks, indent=2, sort_keys=True))
    if args.strict and not checks["overall_ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
