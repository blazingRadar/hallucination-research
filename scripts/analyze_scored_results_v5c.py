#!/usr/bin/env python3
"""Aggregate V5C named-with-exclude scored results."""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRIOR_CELLS = {
    "v5_named_no_exclude": "10/36",
    "v5_neutral_with_exclude": "0/36",
    "v5b_neutral_no_exclude": "0/36",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def wilson(pos: int, n: int, z: float = 1.959963984540054) -> tuple[float | None, float | None]:
    if n == 0:
        return None, None
    phat = pos / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


def fmt(value: float | None) -> str:
    return "NA" if value is None else f"{value:.3f}"


def rate_row(group: str, rows: list[dict]) -> dict:
    n = len(rows)
    pos = sum(1 for row in rows if row["and_hallucination_positive"])
    lo, hi = wilson(pos, n)
    return {
        "group": group,
        "positive": pos,
        "n": n,
        "rate": pos / n if n else None,
        "wilson95_lo": lo,
        "wilson95_hi": hi,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clean_run", type=Path)
    parser.add_argument("openai_scores", type=Path)
    parser.add_argument("anthropic_scores", type=Path)
    parser.add_argument("--out-root", type=Path, default=ROOT / "analysis")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    clean_run = args.clean_run.resolve()
    openai_scores = args.openai_scores.resolve()
    anthropic_scores = args.anthropic_scores.resolve()
    run_id = args.run_id or f"analysis-v5c-named-with-exclude-{clean_run.name}"
    out = args.out_root / run_id
    out.mkdir(parents=True, exist_ok=True)

    raw_rows = load_jsonl(clean_run / "raw_responses.jsonl")
    raw_by_hash = {row["response_hash"]: row for row in raw_rows}
    score_rows = load_jsonl(openai_scores / "adjudicated_scores.jsonl") + load_jsonl(anthropic_scores / "adjudicated_scores.jsonl")

    by_hash: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for row in score_rows:
        by_hash[row["response_hash"]][row["judge_provider"]] = row

    combined = []
    disagreements = []
    for response_hash, raw in raw_by_hash.items():
        judges = by_hash.get(response_hash, {})
        if set(judges) != {"openai", "anthropic"}:
            raise SystemExit(f"missing dual scores for {raw['prompt_id']} {raw['provider']}: {sorted(judges)}")
        openai = judges["openai"]
        anthropic = judges["anthropic"]
        item = {
            "response_hash": response_hash,
            "provider": raw["provider"],
            "model": raw["model"],
            "prompt_id": raw["prompt_id"],
            "anchor_id": raw["corpus_row"].get("anchor_id"),
            "condition": raw["condition"],
            "openai_label": openai["primary_label"],
            "anthropic_label": anthropic["primary_label"],
            "openai_positive": openai["hallucination_positive"],
            "anthropic_positive": anthropic["hallucination_positive"],
            "and_hallucination_positive": bool(openai["hallucination_positive"] and anthropic["hallucination_positive"]),
            "either_hallucination_positive": bool(openai["hallucination_positive"] or anthropic["hallucination_positive"]),
            "judge_primary_agreement": openai["primary_label"] == anthropic["primary_label"],
            "judge_positive_agreement": openai["hallucination_positive"] == anthropic["hallucination_positive"],
        }
        combined.append(item)
        if not item["judge_primary_agreement"] or not item["judge_positive_agreement"]:
            disagreements.append(item)

    providers = sorted({row["provider"] for row in combined})
    aggregate = rate_row("named_entity_schema_with_exclude", combined)
    provider_rates = [
        {
            **rate_row(provider, [row for row in combined if row["provider"] == provider]),
            "provider": provider,
        }
        for provider in providers
    ]
    positives = [row for row in combined if row["and_hallucination_positive"]]
    misrecalls = [
        row for row in combined
        if row["openai_label"] == "misrecalled_real_entity" or row["anthropic_label"] == "misrecalled_real_entity"
    ]
    positive_agreement = sum(1 for row in combined if row["judge_positive_agreement"]) / len(combined)
    primary_agreement = sum(1 for row in combined if row["judge_primary_agreement"]) / len(combined)

    summary = {
        "clean_run": str(clean_run.relative_to(ROOT)),
        "clean_raw_sha256": sha256_file(clean_run / "raw_responses.jsonl"),
        "openai_scores": str(openai_scores.relative_to(ROOT)),
        "openai_scores_sha256": sha256_file(openai_scores / "adjudicated_scores.jsonl"),
        "anthropic_scores": str(anthropic_scores.relative_to(ROOT)),
        "anthropic_scores_sha256": sha256_file(anthropic_scores / "adjudicated_scores.jsonl"),
        "primary_rule": "AND-agreement hallucination-positive",
        "aggregate_rate": aggregate,
        "provider_rates": provider_rates,
        "prior_cells": PRIOR_CELLS,
        "judge_positive_agreement": positive_agreement,
        "judge_primary_agreement": primary_agreement,
        "disagreement_count": len(disagreements),
        "positive_count": len(positives),
        "misrecall_count": len(misrecalls),
    }

    (out / "analysis_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    for filename, rows in [
        ("combined_scores.jsonl", combined),
        ("judge_disagreements.jsonl", disagreements),
        ("positive_log.jsonl", positives),
        ("misrecall_log.jsonl", misrecalls),
    ]:
        with (out / filename).open("w", encoding="utf-8") as f:
            for row in sorted(rows, key=lambda r: (r.get("provider", ""), r.get("prompt_id", ""))):
                f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    with (out / "provider_rates.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = sorted({key for row in provider_rates for key in row})
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(provider_rates)

    lines = [
        "# V5C Named-With-Exclude Results",
        "",
        f"Clean run: `{clean_run.relative_to(ROOT)}`",
        "",
        "## Aggregate",
        "",
        "| Condition | Positive | N | Rate | Wilson 95% CI |",
        "|---|---:|---:|---:|---:|",
        f"| {aggregate['group']} | {aggregate['positive']} | {aggregate['n']} | {fmt(aggregate['rate'])} | [{fmt(aggregate['wilson95_lo'])}, {fmt(aggregate['wilson95_hi'])}] |",
        "",
        "## Prior Cells",
        "",
    ]
    for name, value in PRIOR_CELLS.items():
        lines.append(f"- {name}: `{value}`")
    lines += [
        "",
        "## Judge Agreement",
        "",
        f"- Positive-label agreement: {fmt(positive_agreement)}",
        f"- Primary-label agreement: {fmt(primary_agreement)}",
        f"- Disagreements: {len(disagreements)}",
    ]
    (out / "RESULTS_MEMO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    sha_lines = []
    for path in sorted(out.iterdir()):
        if path.is_file() and path.name != "sha256s.txt":
            sha_lines.append(f"{sha256_file(path)}  {path.name}")
    (out / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")

    print(f"out={out}")
    print(f"v5c={aggregate['positive']}/{aggregate['n']} rate={fmt(aggregate['rate'])} ci=[{fmt(aggregate['wilson95_lo'])}, {fmt(aggregate['wilson95_hi'])}]")
    print(f"disagreements={len(disagreements)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
