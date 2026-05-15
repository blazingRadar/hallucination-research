#!/usr/bin/env python3
"""Merge a truncated-subset rerun into a clean analysis dataset."""

from __future__ import annotations

import argparse
import collections
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_model_lab as runner  # noqa: E402
from rerun_truncated_subset import is_truncated  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_run", type=Path)
    parser.add_argument("rerun_runs", nargs="+", type=Path)
    parser.add_argument("--run-id", default=f"hallucination-v2-clean-merged-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    args = parser.parse_args()

    source_run = args.source_run.resolve()
    rerun_runs = [path.resolve() for path in args.rerun_runs]
    out_root = ROOT / "runs" / args.run_id
    out_root.mkdir(parents=True, exist_ok=True)

    source_rows = [json.loads(line) for line in (source_run / "raw_responses.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    rerun_rows = []
    for rerun_run in rerun_runs:
        rerun_rows.extend(json.loads(line) for line in (rerun_run / "raw_responses.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    replacements = {}
    for row in rerun_rows:
        replacements[(row["provider"], row["prompt_id"])] = row

    expected = {(row["provider"], row["prompt_id"]) for row in source_rows if is_truncated(row)}
    missing = sorted(expected - set(replacements))
    if missing:
        raise SystemExit(f"missing rerun replacements: {missing[:10]} total={len(missing)}")

    merged = []
    replaced = []
    for row in source_rows:
        key = (row["provider"], row["prompt_id"])
        if is_truncated(row):
            repl = dict(replacements[key])
            repl["merged_dataset_run_id"] = args.run_id
            repl["replaces_truncated_response"] = True
            repl["original_truncated_response_hash"] = row["response_hash"]
            merged.append(repl)
            replaced.append({
                "provider": row["provider"],
                "prompt_id": row["prompt_id"],
                "condition": row["condition"],
                "source_finish_reason": (row.get("response_metadata") or {}).get("finish_reason"),
                "source_response_hash": row["response_hash"],
                "replacement_response_hash": repl["response_hash"],
                "replacement_finish_reason": (repl.get("response_metadata") or {}).get("finish_reason"),
            })
        else:
            keep = dict(row)
            keep["merged_dataset_run_id"] = args.run_id
            keep["replaces_truncated_response"] = False
            merged.append(keep)

    raw_path = out_root / "raw_responses.jsonl"
    with raw_path.open("w", encoding="utf-8") as f:
        for row in merged:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    errors = []
    if (source_run / "errors.jsonl").exists():
        errors.extend(json.loads(line) for line in (source_run / "errors.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    if (rerun_run / "errors.jsonl").exists():
        errors.extend(json.loads(line) for line in (rerun_run / "errors.jsonl").read_text(encoding="utf-8").splitlines() if line.strip())
    with (out_root / "errors.jsonl").open("w", encoding="utf-8") as f:
        for err in errors:
            f.write(json.dumps(err, ensure_ascii=False, sort_keys=True) + "\n")

    finish_by_provider = collections.defaultdict(collections.Counter)
    for row in merged:
        finish_by_provider[row["provider"]][(row.get("response_metadata") or {}).get("finish_reason")] += 1

    manifest = {
        "run_id": args.run_id,
        "created_at_utc": utc_now(),
        "source_run": str(source_run.relative_to(ROOT)),
        "source_raw_sha256": runner.sha256_file(source_run / "raw_responses.jsonl"),
        "rerun_runs": [str(rerun_run.relative_to(ROOT)) for rerun_run in rerun_runs],
        "rerun_raw_sha256s": {
            str(rerun_run.relative_to(ROOT)): runner.sha256_file(rerun_run / "raw_responses.jsonl")
            for rerun_run in rerun_runs
        },
        "row_count": len(merged),
        "replacement_count": len(replaced),
        "errors_count": len(errors),
        "deviation_log_entry": "D1",
        "finish_reasons_by_provider": {provider: dict(counter) for provider, counter in sorted(finish_by_provider.items())},
        "credential_values_saved": False,
    }
    (out_root / "run_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    (out_root / "replacement_map.json").write_text(json.dumps(replaced, indent=2, sort_keys=True), encoding="utf-8")
    (out_root / "RUN_SUMMARY.md").write_text(
        "\n".join([
            "# Hallucination Clean Merged Run Summary",
            "",
            f"Run ID: `{args.run_id}`",
            "",
            "Status: merged dataset for primary scoring after D1 truncation rerun.",
            "",
            f"- Total rows: {len(merged)}",
            f"- Replaced truncated rows: {len(replaced)}",
            f"- Errors: {len(errors)}",
            "",
            "Boundary: primary scoring should use this merged dataset. The original raw run is preserved but superseded for primary scoring because of asymmetric truncation.",
        ])
        + "\n",
        encoding="utf-8",
    )

    sha_lines = []
    for path in sorted(out_root.iterdir()):
        if path.is_file() and path.name != "sha256s.txt":
            sha_lines.append(f"{runner.sha256_file(path)}  {path.name}")
    (out_root / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")
    print(f"run_root={out_root}")
    print(f"rows={len(merged)} replacements={len(replaced)} errors={len(errors)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
