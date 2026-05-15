#!/usr/bin/env python3
"""Run the locked hallucination prompt-structure corpus against configured models."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V2.jsonl"
ENV_FILE = Path(os.environ.get("HALLUCINATION_LAB_ENV_FILE", Path.home() / ".openclaw" / ".env"))
DEFAULT_SEED = "prompt_structure_hallucination_v1_20260502"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_env_like(path: Path) -> dict[str, str]:
    vals: dict[str, str] = {}
    if not path.exists():
        return vals
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        vals[key.strip().strip('"').strip("'")] = value.strip().strip('"').strip("'")
    return vals


def get_key(name: str, env_vals: dict[str, str], aliases: list[str]) -> str:
    for key in aliases:
        if os.environ.get(key):
            return os.environ[key]
    for key in aliases:
        if env_vals.get(key):
            return env_vals[key]
    raise RuntimeError(f"missing credential for {name}")


def request_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def openai_chat(base_url: str, api_key: str, model: str, prompt: str, max_tokens: int, timeout: int) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }
    response = request_json(
        f"{base_url.rstrip('/')}/chat/completions",
        {"Authorization": f"Bearer {api_key}"},
        payload,
        timeout,
    )
    content = response["choices"][0]["message"].get("content", "")
    return content, {
        "response_id": response.get("id"),
        "model_version_returned": response.get("model"),
        "finish_reason": response["choices"][0].get("finish_reason"),
        "usage": response.get("usage"),
        "system_fingerprint": response.get("system_fingerprint"),
    }


def anthropic_chat(api_key: str, model: str, prompt: str, max_tokens: int, timeout: int) -> tuple[str, dict[str, Any]]:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
    }
    response = request_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        payload,
        timeout,
    )
    parts = []
    for block in response.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts), {
        "response_id": response.get("id"),
        "model_version_returned": response.get("model"),
        "finish_reason": response.get("stop_reason"),
        "usage": response.get("usage"),
    }


def provider_specs(env_vals: dict[str, str]) -> list[dict[str, Any]]:
    openai_timeout = int(os.environ.get("HALLUCINATION_OPENAI_TIMEOUT", "90"))
    anthropic_timeout = int(os.environ.get("HALLUCINATION_ANTHROPIC_TIMEOUT", "90"))
    xai_timeout = int(os.environ.get("HALLUCINATION_XAI_TIMEOUT", "90"))
    qwen_timeout = int(os.environ.get("HALLUCINATION_QWEN_TIMEOUT", "180"))
    return [
        {
            "provider": "openai",
            "model": os.environ.get("HALLUCINATION_OPENAI_MODEL", "gpt-5-chat-latest"),
            "kind": "openai_compatible",
            "base_url": "https://api.openai.com/v1",
            "api_key": get_key("openai", env_vals, ["OPENAI_API_KEY"]),
            "timeout": openai_timeout,
        },
        {
            "provider": "anthropic",
            "model": os.environ.get("HALLUCINATION_ANTHROPIC_MODEL", "claude-sonnet-4-6"),
            "kind": "anthropic",
            "api_key": get_key("anthropic", env_vals, ["ANTHROPIC_API_KEY", "ANTHROPIC API KEY"]),
            "timeout": anthropic_timeout,
        },
        {
            "provider": "xai",
            "model": os.environ.get("HALLUCINATION_XAI_MODEL", "grok-4.3"),
            "kind": "openai_compatible",
            "base_url": "https://api.x.ai/v1",
            "api_key": get_key("xai", env_vals, ["XAI_API_KEY", "GROK_API_KEY", "XAI API KEY", "GROK API KEY"]),
            "timeout": xai_timeout,
        },
        {
            "provider": "local_qwen",
            "model": os.environ.get("HALLUCINATION_QWEN_MODEL", "qwen/qwen3.5-35b-a3b"),
            "kind": "openai_compatible",
            "base_url": "http://127.0.0.1:1234/v1",
            "api_key": "lm-studio",
            "timeout": qwen_timeout,
        },
    ]


def load_corpus(path: Path = DEFAULT_CORPUS) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=f"hallucination-v2-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--seed", default=DEFAULT_SEED)
    parser.add_argument("--max-tokens", type=int, default=900)
    parser.add_argument("--providers", default="openai,anthropic,xai,local_qwen")
    parser.add_argument("--limit-per-provider", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    env_vals = load_env_like(ENV_FILE)
    selected = {item.strip() for item in args.providers.split(",") if item.strip()}
    specs = [spec for spec in provider_specs(env_vals) if spec["provider"] in selected]
    corpus_path = args.corpus.resolve()
    corpus = load_corpus(corpus_path)

    run_root = ROOT / "runs" / args.run_id
    run_root.mkdir(parents=True, exist_ok=True)
    raw_path = run_root / "raw_responses.jsonl"
    err_path = run_root / "errors.jsonl"

    completed: set[tuple[str, str]] = set()
    if args.resume and raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            completed.add((row["provider"], row["prompt_id"]))

    prompt_order: dict[str, list[str]] = {}
    for spec in specs:
        rows = list(corpus)
        random.Random(f"{args.seed}:{spec['provider']}:{spec['model']}").shuffle(rows)
        prompt_order[spec["provider"]] = [row["prompt_id"] for row in rows]

    manifest = {
        "run_id": args.run_id,
        "started_at_utc": utc_now(),
        "corpus": str(corpus_path.relative_to(ROOT)),
        "corpus_sha256": sha256_file(corpus_path),
        "seed": args.seed,
        "max_tokens": args.max_tokens,
        "providers": [
            {
                "provider": s["provider"],
                "model": s["model"],
                "kind": s["kind"],
                "base_url_host": s.get("base_url", "https://api.anthropic.com").split("//", 1)[-1].split("/", 1)[0],
                "temperature": 0,
            }
            for s in specs
        ],
        "credential_values_saved": False,
    }
    (run_root / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (run_root / "prompt_order.json").write_text(json.dumps(prompt_order, indent=2, sort_keys=True), encoding="utf-8")

    with raw_path.open("a", encoding="utf-8") as raw_f, err_path.open("a", encoding="utf-8") as err_f:
        for spec in specs:
            ordered = sorted(corpus, key=lambda row: prompt_order[spec["provider"]].index(row["prompt_id"]))
            if args.limit_per_provider:
                ordered = ordered[: args.limit_per_provider]
            for index, item in enumerate(ordered, 1):
                key = (spec["provider"], item["prompt_id"])
                if key in completed:
                    continue
                started = utc_now()
                try:
                    if spec["kind"] == "anthropic":
                        text, meta = anthropic_chat(spec["api_key"], spec["model"], item["prompt"], args.max_tokens, spec["timeout"])
                    else:
                        text, meta = openai_chat(spec["base_url"], spec["api_key"], spec["model"], item["prompt"], args.max_tokens, spec["timeout"])
                    record = {
                        "run_id": args.run_id,
                        "prompt_id": item["prompt_id"],
                        "condition": item["condition"],
                        "domain": item["domain"],
                        "provider": spec["provider"],
                        "model": spec["model"],
                        "model_version_returned": meta.get("model_version_returned"),
                        "temperature": 0,
                        "timestamp_utc": started,
                        "request_hash": sha256_text(json.dumps({"model": spec["model"], "prompt": item["prompt"], "temperature": 0}, sort_keys=True, ensure_ascii=False)),
                        "response_hash": sha256_text(text),
                        "prompt": item["prompt"],
                        "response_text": text,
                        "error": None,
                        "response_metadata": meta,
                        "corpus_row": item,
                    }
                    raw_f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
                    raw_f.flush()
                    print(f"PASS {spec['provider']} {index:02d}/{len(ordered)} {item['prompt_id']} chars={len(text)}", flush=True)
                except Exception as exc:
                    err = {
                        "run_id": args.run_id,
                        "prompt_id": item["prompt_id"],
                        "condition": item["condition"],
                        "provider": spec["provider"],
                        "model": spec["model"],
                        "timestamp_utc": started,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    }
                    err_f.write(json.dumps(err, ensure_ascii=False, sort_keys=True) + "\n")
                    err_f.flush()
                    print(f"ERROR {spec['provider']} {index:02d}/{len(ordered)} {item['prompt_id']} {type(exc).__name__}", flush=True)

    sha_lines = []
    for path in sorted(run_root.iterdir()):
        if path.is_file():
            sha_lines.append(f"{sha256_file(path)}  {path.name}")
    (run_root / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    print(f"run_root={run_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
