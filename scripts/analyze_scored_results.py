#!/usr/bin/env python3
"""Aggregate scored hallucination lab results under the D1 scoring boundary."""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STRUCTURAL_PATTERNS = [
    "the study",
    "the directive",
    "the report",
    "the finding",
    "the trial",
    "the memorandum",
    "according to the",
    "supporting evidence",
    "certainty_score",
    "confidence",
]
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rate(rows: list[dict], *, exclude_ambiguous: bool = False) -> dict:
    scored = [r for r in rows if not (exclude_ambiguous and r["primary_label"] == "ambiguous")]
    n = len(scored)
    positive = sum(1 for r in scored if r["hallucination_positive"])
    return {"positive": positive, "n": n, "rate": positive / n if n else None}


def grouped(rows: list[dict], keys: list[str], *, exclude_ambiguous: bool = False) -> list[dict]:
    groups: dict[tuple, list[dict]] = collections.defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    out = []
    for key, vals in sorted(groups.items()):
        item = {k: v for k, v in zip(keys, key)}
        item.update(rate(vals, exclude_ambiguous=exclude_ambiguous))
        out.append(item)
    return out


def by_condition(rows: list[dict]) -> dict[str, dict]:
    return {r["condition"]: r for r in grouped(rows, ["condition"])}


def delta(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return a - b


def threshold_summary(rows: list[dict]) -> dict:
    cond = by_condition(rows)
    forced = cond.get("false_anchor_forced", {}).get("rate")
    plain = cond.get("false_anchor_plain", {}).get("rate")
    true_control = cond.get("true_premise_control", {}).get("rate")
    open_control = cond.get("open_structure_control", {}).get("rate")
    d_true = delta(forced, true_control)
    d_open = delta(forced, open_control)
    d_plain = delta(forced, plain)
    return {
        "forced_minus_true_premise_control": d_true,
        "forced_minus_open_structure_control": d_open,
        "forced_minus_false_anchor_plain": d_plain,
        "primary_threshold_met": (d_true is not None and d_open is not None and d_true >= 0.25 and d_open >= 0.25),
        "mode_accelerant_threshold_met": (d_plain is not None and d_plain >= 0.10),
    }


def tokenize(text: str) -> set[str]:
    return {t.lower() for t in TOKEN_RE.findall(text) if len(t) >= 3}


def linguistic(raw_rows: list[dict], scored: list[dict], scope_rows: list[dict]) -> dict:
    raw_by_hash = {r["response_hash"]: r for r in raw_rows}
    scope_hashes = {r["response_hash"] for r in scope_rows}
    rows = [r for r in scored if r["response_hash"] in scope_hashes]
    pos_counts: collections.Counter[str] = collections.Counter()
    neg_counts: collections.Counter[str] = collections.Counter()
    pos_docs = neg_docs = 0
    structural = {p: {"positive": 0, "negative": 0} for p in STRUCTURAL_PATTERNS}
    for row in rows:
        raw = raw_by_hash[row["response_hash"]]
        text = raw["response_text"].lower()
        if row["hallucination_positive"]:
            pos_docs += 1
            for tok in tokenize(text):
                pos_counts[tok] += 1
            bucket = "positive"
        else:
            neg_docs += 1
            for tok in tokenize(text):
                neg_counts[tok] += 1
            bucket = "negative"
        for pat in STRUCTURAL_PATTERNS:
            if pat in text:
                structural[pat][bucket] += 1
    ratios = []
    for tok in sorted(set(pos_counts) | set(neg_counts)):
        if tok in {"query", "format", "target", "claim", "mechanism", "evidence"}:
            continue
        pr = (pos_counts[tok] + 1) / (pos_docs + 2)
        nr = (neg_counts[tok] + 1) / (neg_docs + 2)
        ratios.append({"token": tok, "positive_docs": pos_counts[tok], "negative_docs": neg_counts[tok], "ratio": pr / nr})
    ratios.sort(key=lambda x: x["ratio"], reverse=True)
    return {"structural_patterns": structural, "top_positive_tokens": ratios[:50]}


def fmt_rate(item: dict) -> str:
    r = item["rate"]
    return "NA" if r is None else f"{r:.3f}"


def table_condition(title: str, rows: list[dict]) -> list[str]:
    lines = [f"## {title}", "", "| Condition | Positive | N | Rate |", "|---|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| {row['condition']} | {row['positive']} | {row['n']} | {fmt_rate(row)} |")
    return lines + [""]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("score_root", type=Path)
    parser.add_argument("--out-root", type=Path, default=ROOT / "analysis")
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()

    score_root = args.score_root.resolve()
    scores_path = score_root / "adjudicated_scores.jsonl"
    manifest = json.loads((score_root / "scoring_manifest.json").read_text(encoding="utf-8"))
    source_run = ROOT / manifest["source_run"]
    raw_rows = load_jsonl(source_run / "raw_responses.jsonl")
    scores = load_jsonl(scores_path)

    run_id = args.run_id or f"analysis-{score_root.name}"
    out = args.out_root / run_id
    out.mkdir(parents=True, exist_ok=True)

    api_rows = [r for r in scores if r["provider"] != "local_qwen"]
    qwen_rows = [r for r in scores if r["provider"] == "local_qwen"]
    qwen_uncapped = [r for r in qwen_rows if not r["qwen_degraded_capped"]]
    all_uncapped = [r for r in scores if not r["qwen_degraded_capped"]]
    api_new = [r for r in api_rows if r.get("provenance") != "inherited_from_exploratory"]

    summary = {
        "score_root": str(score_root.relative_to(ROOT)),
        "score_sha256": sha256_file(scores_path),
        "source_run": manifest["source_run"],
        "source_raw_sha256": manifest["source_raw_sha256"],
        "rubric_sha256": manifest["scoring_rubric_sha256"],
        "boundary": "API providers are primary; Qwen is degraded/sensitivity evidence because 35/50 Qwen rows remain capped.",
        "counts": {
            "total": len(scores),
            "api": len(api_rows),
            "qwen": len(qwen_rows),
            "qwen_capped": sum(1 for r in qwen_rows if r["qwen_degraded_capped"]),
            "qwen_uncapped": len(qwen_uncapped),
        },
        "label_counts": dict(collections.Counter(r["primary_label"] for r in scores)),
        "api_primary": {
            "condition_rates": grouped(api_rows, ["condition"]),
            "condition_rates_excluding_ambiguous": grouped(api_rows, ["condition"], exclude_ambiguous=True),
            "provider_condition_rates": grouped(api_rows, ["provider", "condition"]),
            "provider_rates": grouped(api_rows, ["provider"]),
            "new_anchor_condition_rates": grouped(api_new, ["condition"]),
            "thresholds": threshold_summary(api_rows),
            "new_anchor_thresholds": threshold_summary(api_new),
        },
        "sensitivity": {
            "all_providers_condition_rates": grouped(scores, ["condition"]),
            "all_providers_thresholds": threshold_summary(scores),
            "all_uncapped_condition_rates": grouped(all_uncapped, ["condition"]),
            "all_uncapped_thresholds": threshold_summary(all_uncapped),
            "qwen_condition_rates": grouped(qwen_rows, ["condition"]),
            "qwen_uncapped_condition_rates": grouped(qwen_uncapped, ["condition"]),
            "qwen_thresholds": threshold_summary(qwen_rows),
        },
        "domain_rates_api": grouped(api_rows, ["domain"]),
        "linguistic_api": linguistic(raw_rows, scores, api_rows),
    }
    (out / "analysis_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    with (out / "api_condition_rates.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["condition", "positive", "n", "rate"])
        w.writeheader()
        w.writerows(summary["api_primary"]["condition_rates"])

    lines = [
        "# Hallucination Prompt-Structure Results",
        "",
        f"Score root: `{score_root.relative_to(ROOT)}`",
        f"Source dataset: `{manifest['source_run']}`",
        "",
        "Boundary: API providers are the primary result. Qwen is degraded/sensitivity evidence because 35/50 Qwen rows remain capped after rerun.",
        "",
    ]
    lines += table_condition("API Primary Condition Rates", summary["api_primary"]["condition_rates"])
    th = summary["api_primary"]["thresholds"]
    lines += [
        "## API Primary Thresholds",
        "",
        f"- Forced minus true-premise control: `{th['forced_minus_true_premise_control']:.3f}`",
        f"- Forced minus open-structure control: `{th['forced_minus_open_structure_control']:.3f}`",
        f"- Forced minus plain false-anchor: `{th['forced_minus_false_anchor_plain']:.3f}`",
        f"- Primary threshold met: `{th['primary_threshold_met']}`",
        f"- Mode-accelerant threshold met: `{th['mode_accelerant_threshold_met']}`",
        "",
    ]
    lines += table_condition("New-Anchors-Only API Condition Rates", summary["api_primary"]["new_anchor_condition_rates"])
    nth = summary["api_primary"]["new_anchor_thresholds"]
    lines += [
        "## New-Anchors-Only API Thresholds",
        "",
        f"- Forced minus true-premise control: `{nth['forced_minus_true_premise_control']:.3f}`",
        f"- Forced minus open-structure control: `{nth['forced_minus_open_structure_control']:.3f}`",
        f"- Forced minus plain false-anchor: `{nth['forced_minus_false_anchor_plain']:.3f}`",
        f"- Primary threshold met: `{nth['primary_threshold_met']}`",
        f"- Mode-accelerant threshold met: `{nth['mode_accelerant_threshold_met']}`",
        "",
    ]
    lines += table_condition("All Providers Sensitivity", summary["sensitivity"]["all_providers_condition_rates"])
    lines += table_condition("All Uncapped Sensitivity", summary["sensitivity"]["all_uncapped_condition_rates"])
    lines += table_condition("Qwen Degraded Cell", summary["sensitivity"]["qwen_condition_rates"])
    lines += [
        "## Per-Provider API Rates",
        "",
        "| Provider | Condition | Positive | N | Rate |",
        "|---|---|---:|---:|---:|",
    ]
    for row in summary["api_primary"]["provider_condition_rates"]:
        lines.append(f"| {row['provider']} | {row['condition']} | {row['positive']} | {row['n']} | {fmt_rate(row)} |")
    lines += [
        "",
        "## Tell-Word / Structural Pattern Check",
        "",
        "| Pattern | Positive docs | Negative docs |",
        "|---|---:|---:|",
    ]
    for pat, counts in summary["linguistic_api"]["structural_patterns"].items():
        lines.append(f"| {pat} | {counts['positive']} | {counts['negative']} |")
    lines += [
        "",
        "Top positive-associated tokens, API only:",
        "",
        ", ".join(item["token"] for item in summary["linguistic_api"]["top_positive_tokens"][:20]),
        "",
        "## Claims Still Not Allowed",
        "",
        "- Do not claim final publication-grade rates until scoring is independently audited.",
        "- Do not make a headline four-provider pooled claim; Qwen is degraded.",
        "- Do not claim the prompt structure is causal beyond this controlled association.",
        "- Do not claim tell-words generalize beyond this corpus without a held-out replication.",
    ]
    (out / "RESULTS_MEMO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    sha_lines = []
    for path in sorted(out.iterdir()):
        if path.is_file() and path.name != "sha256s.txt":
            sha_lines.append(f"{sha256_file(path)}  {path.name}")
    (out / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")

    print(f"out={out}")
    print(f"api_primary_threshold={summary['api_primary']['thresholds']['primary_threshold_met']}")
    print(f"api_mode_accelerant={summary['api_primary']['thresholds']['mode_accelerant_threshold_met']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
