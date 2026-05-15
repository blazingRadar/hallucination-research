#!/usr/bin/env python3
"""Rerun only truncated responses from a prior hallucination lab run."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_model_lab as runner  # noqa: E402


TRUNCATED_FINISH_REASONS = {"length", "max_tokens"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_truncated(row: dict[str, Any]) -> bool:
    meta = row.get("response_metadata") or {}
    return meta.get("finish_reason") in TRUNCATED_FINISH_REASONS


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_run", type=Path)
    parser.add_argument("--run-id", default=f"hallucination-v2-truncated-rerun-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    parser.add_argument("--max-tokens", type=int, default=2400)
    parser.add_argument("--api-timeout", type=int, default=0)
    parser.add_argument("--local-timeout", type=int, default=600)
    parser.add_argument("--providers", default="")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    source_run = args.source_run.resolve()
    source_raw = source_run / "raw_responses.jsonl"
    source_rows = [json.loads(line) for line in source_raw.read_text(encoding="utf-8").splitlines() if line.strip()]
    targets = [row for row in source_rows if is_truncated(row)]
    if args.providers:
        selected_providers = {item.strip() for item in args.providers.split(",") if item.strip()}
        targets = [row for row in targets if row["provider"] in selected_providers]

    env_vals = runner.load_env_like(runner.ENV_FILE)
    specs = {spec["provider"]: spec for spec in runner.provider_specs(env_vals)}
    if args.api_timeout:
        for spec in specs.values():
            spec["timeout"] = args.api_timeout
    if "local_qwen" in specs:
        specs["local_qwen"]["timeout"] = args.local_timeout
    run_root = ROOT / "runs" / args.run_id
    run_root.mkdir(parents=True, exist_ok=True)
    raw_path = run_root / "raw_responses.jsonl"
    err_path = run_root / "errors.jsonl"

    completed: set[tuple[str, str]] = set()
    if args.resume and raw_path.exists():
        for line in raw_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                completed.add((row["provider"], row["prompt_id"]))

    manifest = {
        "run_id": args.run_id,
        "started_at_utc": utc_now(),
        "source_run": str(source_run.relative_to(ROOT)),
        "source_raw_sha256": runner.sha256_file(source_raw),
        "rerun_rule": "finish_reason in ['length', 'max_tokens']",
        "target_count": len(targets),
        "providers_filter": args.providers or None,
        "max_tokens": args.max_tokens,
        "api_timeout_seconds": args.api_timeout or None,
        "local_timeout_seconds": args.local_timeout,
        "credential_values_saved": False,
        "deviation_log_entry": "D1",
    }
    (run_root / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (run_root / "rerun_targets.json").write_text(
        json.dumps(
            [
                {
                    "provider": row["provider"],
                    "model": row["model"],
                    "prompt_id": row["prompt_id"],
                    "condition": row["condition"],
                    "source_finish_reason": (row.get("response_metadata") or {}).get("finish_reason"),
                    "source_response_hash": row["response_hash"],
                }
                for row in targets
            ],
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    with raw_path.open("a", encoding="utf-8") as raw_f, err_path.open("a", encoding="utf-8") as err_f:
        for index, item in enumerate(targets, 1):
            key = (item["provider"], item["prompt_id"])
            if key in completed:
                continue
            spec = specs[item["provider"]]
            started = utc_now()
            try:
                if spec["kind"] == "anthropic":
                    response_text, metadata = runner.anthropic_chat(
                        spec["api_key"], spec["model"], item["prompt"], args.max_tokens, spec["timeout"]
                    )
                else:
                    response_text, metadata = runner.openai_chat(
                        spec["base_url"], spec["api_key"], spec["model"], item["prompt"], args.max_tokens, spec["timeout"]
                    )
                out = {
                    **{k: item[k] for k in ["condition", "corpus_row", "domain", "model", "prompt", "prompt_id", "provider", "temperature"]},
                    "error": None,
                    "model_version_returned": metadata.get("model_version_returned") or spec["model"],
                    "request_hash": runner.sha256_text(json.dumps({"provider": spec["provider"], "model": spec["model"], "prompt": item["prompt"], "max_tokens": args.max_tokens}, sort_keys=True)),
                    "response_hash": runner.sha256_text(response_text),
                    "response_metadata": metadata,
                    "response_text": response_text,
                    "run_id": args.run_id,
                    "timestamp_utc": started,
                    "rerun_reason": "source_response_truncated",
                    "source_run_id": item["run_id"],
                    "source_response_hash": item["response_hash"],
                    "source_finish_reason": (item.get("response_metadata") or {}).get("finish_reason"),
                }
                raw_f.write(json.dumps(out, ensure_ascii=False, sort_keys=True) + "\n")
                raw_f.flush()
                print(f"PASS rerun {index}/{len(targets)} {item['provider']} {item['prompt_id']} chars={len(response_text)} finish={metadata.get('finish_reason')}", flush=True)
            except Exception as exc:  # noqa: BLE001
                err = {
                    "run_id": args.run_id,
                    "timestamp_utc": started,
                    "provider": item["provider"],
                    "model": spec["model"],
                    "prompt_id": item["prompt_id"],
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "source_response_hash": item["response_hash"],
                }
                err_f.write(json.dumps(err, ensure_ascii=False, sort_keys=True) + "\n")
                err_f.flush()
                print(f"ERROR rerun {index}/{len(targets)} {item['provider']} {item['prompt_id']} {type(exc).__name__}: {exc}", flush=True)

    sha_lines = []
    for path in sorted(run_root.iterdir()):
        if path.is_file() and path.name != "sha256s.txt":
            sha_lines.append(f"{runner.sha256_file(path)}  {path.name}")
    (run_root / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    print(f"run_root={run_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
