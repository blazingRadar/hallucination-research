#!/usr/bin/env python3
"""Aggregate V6 dose-response scored results."""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSES = [0, 1, 2, 4, 8]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def score_key(row: dict) -> tuple[str, str, str]:
    return (row["provider"], row["prompt_id"], row["response_hash"])


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


def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def hypergeom_prob(a: int, row1: int, row2: int, col1: int, total: int) -> float:
    return math.exp(log_choose(row1, a) + log_choose(row2, col1 - a) - log_choose(total, col1))


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    row1 = a + b
    row2 = c + d
    col1 = a + c
    total = row1 + row2
    observed = hypergeom_prob(a, row1, row2, col1, total)
    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    p = 0.0
    for x in range(lo, hi + 1):
        prob = hypergeom_prob(x, row1, row2, col1, total)
        if prob <= observed + 1e-12:
            p += prob
    return min(1.0, p)


def cochran_armitage(groups: list[tuple[float, int, int]]) -> dict:
    """Return approximate two-sided trend p-value for ordered groups.

    groups are (score, positive, n).
    """
    total_n = sum(n for _, _, n in groups)
    total_pos = sum(pos for _, pos, _ in groups)
    if total_n == 0:
        return {"z": None, "p_two_sided": None}
    p_hat = total_pos / total_n
    weighted_score_mean = sum(score * n for score, _, n in groups) / total_n
    numerator = sum(score * (pos - n * p_hat) for score, pos, n in groups)
    variance = p_hat * (1 - p_hat) * sum(n * (score - weighted_score_mean) ** 2 for score, _, n in groups)
    if variance <= 0:
        return {"z": None, "p_two_sided": None}
    z = numerator / math.sqrt(variance)
    p_two = math.erfc(abs(z) / math.sqrt(2))
    return {"z": z, "p_two_sided": p_two}


def invert_matrix(matrix: list[list[float]]) -> list[list[float]] | None:
    n = len(matrix)
    aug = [[*row, *[1.0 if i == j else 0.0 for j in range(n)]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) < 1e-12:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [value - factor * aug[col][idx] for idx, value in enumerate(aug[row])]
    return [row[n:] for row in aug]


def mat_vec_mul(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(row[i] * vector[i] for i in range(len(vector))) for row in matrix]


def logistic_regression(rows: list[dict]) -> dict:
    """Fit y ~ named_slot_count + prompt_length with dependency-free IRLS."""
    y = [1.0 if row["and_hallucination_positive"] else 0.0 for row in rows]
    if not y or sum(y) in {0.0, float(len(y))}:
        return {"status": "not_fit_all_outcomes_same", "n": len(y), "positive": int(sum(y))}
    dose = [float(row["named_slot_count"]) for row in rows]
    length = [float(row["prompt_length"]) for row in rows]

    def standardize(values: list[float]) -> tuple[list[float], float, float]:
        mean = sum(values) / len(values)
        variance = sum((value - mean) ** 2 for value in values) / len(values)
        stdev = math.sqrt(variance) if variance > 0 else 1.0
        return [(value - mean) / stdev for value in values], mean, stdev

    dose_z, dose_mean, dose_stdev = standardize(dose)
    length_z, length_mean, length_stdev = standardize(length)
    x = [[1.0, dose_z[i], length_z[i]] for i in range(len(rows))]
    beta = [0.0, 0.0, 0.0]
    converged = False
    covariance = None
    for _iteration in range(1, 101):
        eta = [max(-30.0, min(30.0, sum(x_i[j] * beta[j] for j in range(3)))) for x_i in x]
        mu = [1.0 / (1.0 + math.exp(-value)) for value in eta]
        weights = [max(1e-8, value * (1.0 - value)) for value in mu]
        gradient = [sum(x[i][j] * (y[i] - mu[i]) for i in range(len(rows))) for j in range(3)]
        hessian = [
            [sum(weights[i] * x[i][j] * x[i][k] for i in range(len(rows))) for k in range(3)]
            for j in range(3)
        ]
        inv = invert_matrix(hessian)
        if inv is None:
            return {"status": "not_fit_singular_hessian", "n": len(y), "positive": int(sum(y))}
        step = mat_vec_mul(inv, gradient)
        beta = [beta[j] + step[j] for j in range(3)]
        if max(abs(value) for value in step) < 1e-7:
            converged = True
            covariance = inv
            break
    if covariance is None:
        eta = [max(-30.0, min(30.0, sum(x_i[j] * beta[j] for j in range(3)))) for x_i in x]
        mu = [1.0 / (1.0 + math.exp(-value)) for value in eta]
        weights = [max(1e-8, value * (1.0 - value)) for value in mu]
        hessian = [
            [sum(weights[i] * x[i][j] * x[i][k] for i in range(len(rows))) for k in range(3)]
            for j in range(3)
        ]
        covariance = invert_matrix(hessian)
    if covariance is None:
        return {"status": "not_fit_singular_final_hessian", "n": len(y), "positive": int(sum(y))}
    se = [math.sqrt(max(0.0, covariance[i][i])) for i in range(3)]
    z_scores = [None if se[i] == 0 else beta[i] / se[i] for i in range(3)]
    p_values = [None if z is None else math.erfc(abs(z) / math.sqrt(2)) for z in z_scores]
    return {
        "status": "converged" if converged else "not_converged_report_with_caution",
        "n": len(y),
        "positive": int(sum(y)),
        "predictors": ["intercept", "named_slot_count_standardized", "prompt_length_standardized"],
        "coefficients": beta,
        "standard_errors": se,
        "z_scores": z_scores,
        "p_two_sided": p_values,
        "named_slot_count_coefficient": beta[1],
        "named_slot_count_p_two_sided": p_values[1],
        "prompt_length_coefficient": beta[2],
        "prompt_length_p_two_sided": p_values[2],
        "standardization": {
            "named_slot_count_mean": dose_mean,
            "named_slot_count_stdev": dose_stdev,
            "prompt_length_mean": length_mean,
            "prompt_length_stdev": length_stdev,
        },
    }


def finish_reason_table(raw_rows: list[dict]) -> list[dict]:
    counts = collections.Counter(
        (
            row["provider"],
            row.get("response_metadata", {}).get("finish_reason", "unknown"),
        )
        for row in raw_rows
    )
    return [
        {"provider": provider, "finish_reason": reason, "count": count}
        for (provider, reason), count in sorted(counts.items())
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clean_run", type=Path)
    parser.add_argument("openai_scores", type=Path)
    parser.add_argument("anthropic_scores", type=Path)
    parser.add_argument("--out-root", type=Path, default=ROOT / "analysis")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--human-overrides-applied", default="no")
    args = parser.parse_args()

    clean_run = args.clean_run.resolve()
    openai_scores = args.openai_scores.resolve()
    anthropic_scores = args.anthropic_scores.resolve()
    run_id = args.run_id or f"analysis-v6-dose-response-{clean_run.name}"
    out = args.out_root / run_id
    out.mkdir(parents=True, exist_ok=True)

    raw_rows = load_jsonl(clean_run / "raw_responses.jsonl")
    raw_by_key = {score_key(row): row for row in raw_rows}
    score_rows = load_jsonl(openai_scores / "adjudicated_scores.jsonl") + load_jsonl(anthropic_scores / "adjudicated_scores.jsonl")
    by_key: dict[tuple[str, str, str], dict[str, dict]] = collections.defaultdict(dict)
    for row in score_rows:
        by_key[score_key(row)][row["judge_provider"]] = row

    combined = []
    disagreements = []
    for key, raw in raw_by_key.items():
        response_hash = raw["response_hash"]
        judges = by_key.get(key, {})
        if set(judges) != {"openai", "anthropic"}:
            raise SystemExit(f"missing dual scores for {raw['prompt_id']} {raw['provider']}: {sorted(judges)}")
        openai = judges["openai"]
        anthropic = judges["anthropic"]
        corpus = raw["corpus_row"]
        item = {
            "response_hash": response_hash,
            "provider": raw["provider"],
            "model": raw["model"],
            "prompt_id": raw["prompt_id"],
            "anchor_id": corpus.get("anchor_id"),
            "replicate": corpus.get("replicate"),
            "named_slot_count": corpus.get("named_slot_count"),
            "prompt_length": len(raw["prompt"]),
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

    dose_rates = [rate_row(f"dose_{dose}", [row for row in combined if row["named_slot_count"] == dose]) for dose in DOSES]
    provider_dose_rates = []
    for provider in sorted({row["provider"] for row in combined}):
        for dose in DOSES:
            provider_dose_rates.append({
                **rate_row(f"{provider}_dose_{dose}", [row for row in combined if row["provider"] == provider and row["named_slot_count"] == dose]),
                "provider": provider,
                "named_slot_count": dose,
            })

    dose_counts = {
        dose: (
            sum(1 for row in combined if row["named_slot_count"] == dose and row["and_hallucination_positive"]),
            sum(1 for row in combined if row["named_slot_count"] == dose),
        )
        for dose in DOSES
    }
    pos8, n8 = dose_counts[8]
    pos0, n0 = dose_counts[0]
    fisher_8_vs_0 = fisher_two_sided(pos8, n8 - pos8, pos0, n0 - pos0)
    high_rows = [row for row in combined if row["named_slot_count"] in {4, 8}]
    low_rows = [row for row in combined if row["named_slot_count"] in {0, 1}]
    high_pos = sum(1 for row in high_rows if row["and_hallucination_positive"])
    low_pos = sum(1 for row in low_rows if row["and_hallucination_positive"])
    fisher_high_vs_low = fisher_two_sided(high_pos, len(high_rows) - high_pos, low_pos, len(low_rows) - low_pos)
    trend = cochran_armitage([(dose, pos, n) for dose, (pos, n) in dose_counts.items()])
    provider_trends = []
    for provider in sorted({row["provider"] for row in combined}):
        provider_counts = {
            dose: (
                sum(1 for row in combined if row["provider"] == provider and row["named_slot_count"] == dose and row["and_hallucination_positive"]),
                sum(1 for row in combined if row["provider"] == provider and row["named_slot_count"] == dose),
            )
            for dose in DOSES
        }
        provider_trends.append({
            "provider": provider,
            **cochran_armitage([(dose, pos, n) for dose, (pos, n) in provider_counts.items()]),
        })
    logistic = logistic_regression(combined)

    anchor_rows = []
    grouped: dict[tuple[str, int, str], list[dict]] = collections.defaultdict(list)
    for row in combined:
        grouped[(row["anchor_id"], row["named_slot_count"], row["provider"])].append(row)
    for (anchor, dose, provider), rows in sorted(grouped.items()):
        anchor_rows.append({
            "anchor_id": anchor,
            "named_slot_count": dose,
            "provider": provider,
            "replicate_count": len(rows),
            "anchor_condition_positive": any(row["and_hallucination_positive"] for row in rows),
            "and_hallucination_positive": any(row["and_hallucination_positive"] for row in rows),
        })
    anchor_dose_rates = [rate_row(f"anchor_dose_{dose}", [row for row in anchor_rows if row["named_slot_count"] == dose]) for dose in DOSES]
    highest_dose_anchor_rows = [row for row in anchor_rows if row["named_slot_count"] == 8]
    highest_dose_anchor_positive_count = sum(1 for row in highest_dose_anchor_rows if row["anchor_condition_positive"])
    highest_dose_anchor_positive_fraction = highest_dose_anchor_positive_count / len(highest_dose_anchor_rows) if highest_dose_anchor_rows else None
    highest_dose_anchor_ids = sorted({row["anchor_id"] for row in combined if row["named_slot_count"] == 8})
    highest_dose_anchors_any_provider_positive = [
        anchor_id for anchor_id in highest_dose_anchor_ids
        if any(
            row["anchor_id"] == anchor_id
            and row["named_slot_count"] == 8
            and row["and_hallucination_positive"]
            for row in combined
        )
    ]
    highest_dose_anchor_any_provider_positive_count = len(highest_dose_anchors_any_provider_positive)
    highest_dose_anchor_any_provider_positive_fraction = (
        highest_dose_anchor_any_provider_positive_count / len(highest_dose_anchor_ids)
        if highest_dose_anchor_ids else None
    )

    prompt_lengths_by_dose = []
    for dose in DOSES:
        lengths = [row["prompt_length"] for row in combined if row["named_slot_count"] == dose]
        prompt_lengths_by_dose.append({
            "named_slot_count": dose,
            "min": min(lengths) if lengths else None,
            "max": max(lengths) if lengths else None,
            "mean": sum(lengths) / len(lengths) if lengths else None,
            "n": len(lengths),
        })

    positives = [row for row in combined if row["and_hallucination_positive"]]
    misrecalls = [
        row for row in combined
        if row["openai_label"] == "misrecalled_real_entity" or row["anthropic_label"] == "misrecalled_real_entity"
    ]

    summary = {
        "clean_run": str(clean_run.relative_to(ROOT)),
        "clean_raw_sha256": sha256_file(clean_run / "raw_responses.jsonl"),
        "openai_scores": str(openai_scores.relative_to(ROOT)),
        "openai_scores_sha256": sha256_file(openai_scores / "adjudicated_scores.jsonl"),
        "anthropic_scores": str(anthropic_scores.relative_to(ROOT)),
        "anthropic_scores_sha256": sha256_file(anthropic_scores / "adjudicated_scores.jsonl"),
        "primary_rule": "AND-agreement hallucination-positive",
        "dose_rates": dose_rates,
        "provider_dose_rates": provider_dose_rates,
        "anchor_level_dose_rates": anchor_dose_rates,
        "cochran_armitage": trend,
        "provider_cochran_armitage": provider_trends,
        "logistic_regression_dose_plus_prompt_length": logistic,
        "fisher_8_vs_0_two_sided": fisher_8_vs_0,
        "fisher_high_4_8_vs_low_0_1_two_sided": fisher_high_vs_low,
        "prompt_lengths_by_dose": prompt_lengths_by_dose,
        "finish_reasons": finish_reason_table(raw_rows),
        "highest_dose_anchor_positive_count": highest_dose_anchor_positive_count,
        "highest_dose_anchor_positive_fraction": highest_dose_anchor_positive_fraction,
        "highest_dose_anchor_any_provider_positive_count": highest_dose_anchor_any_provider_positive_count,
        "highest_dose_anchor_any_provider_positive_fraction": highest_dose_anchor_any_provider_positive_fraction,
        "highest_dose_anchor_any_provider_positive_ids": highest_dose_anchors_any_provider_positive,
        "primary_threshold_8_minus_0": (pos8 / n8 if n8 else 0) - (pos0 / n0 if n0 else 0),
        "primary_threshold_8_minus_0_passes_0_15": ((pos8 / n8 if n8 else 0) - (pos0 / n0 if n0 else 0)) >= 0.15,
        "provider_z_positive_count": sum(1 for row in provider_trends if row["z"] is not None and row["z"] > 0),
        "provider_significant_positive_trend_count": sum(
            1
            for row in provider_trends
            if row["z"] is not None
            and row["z"] > 0
            and row["p_two_sided"] is not None
            and row["p_two_sided"] < 0.05
        ),
        "human_overrides_applied": args.human_overrides_applied,
        "judge_positive_agreement": sum(1 for row in combined if row["judge_positive_agreement"]) / len(combined),
        "judge_primary_agreement": sum(1 for row in combined if row["judge_primary_agreement"]) / len(combined),
        "disagreement_count": len(disagreements),
        "positive_count": len(positives),
        "misrecall_count": len(misrecalls),
    }

    (out / "analysis_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    for filename, rows in [
        ("combined_scores.jsonl", combined),
        ("anchor_level_scores.jsonl", anchor_rows),
        ("judge_disagreements.jsonl", disagreements),
        ("positive_log.jsonl", positives),
        ("misrecall_log.jsonl", misrecalls),
    ]:
        with (out / filename).open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    for filename, rows in [
        ("dose_rates.csv", dose_rates),
        ("provider_dose_rates.csv", provider_dose_rates),
        ("anchor_level_dose_rates.csv", anchor_dose_rates),
        ("provider_trends.csv", provider_trends),
        ("prompt_lengths_by_dose.csv", prompt_lengths_by_dose),
        ("finish_reasons.csv", finish_reason_table(raw_rows)),
    ]:
        with (out / filename).open("w", newline="", encoding="utf-8") as f:
            fieldnames = sorted({key for row in rows for key in row})
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    lines = [
        "# V6 Dose-Response Results",
        "",
        f"Clean run: `{clean_run.relative_to(ROOT)}`",
        "",
        "## Dose Rates",
        "",
        "| Named slots | Positive | N | Rate | Wilson 95% CI |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in dose_rates:
        dose = row["group"].replace("dose_", "")
        lines.append(f"| {dose} | {row['positive']} | {row['n']} | {fmt(row['rate'])} | [{fmt(row['wilson95_lo'])}, {fmt(row['wilson95_hi'])}] |")
    lines += [
        "",
        "## Preregistered Tests",
        "",
        f"- Cochran-Armitage z: `{fmt(trend['z'])}`, two-sided p: `{fmt(trend['p_two_sided'])}`",
        f"- Length-covariate logistic status: `{logistic['status']}`",
        f"- Logistic named-slot coefficient: `{fmt(logistic.get('named_slot_count_coefficient'))}`, two-sided p: `{fmt(logistic.get('named_slot_count_p_two_sided'))}`",
        f"- Logistic prompt-length coefficient: `{fmt(logistic.get('prompt_length_coefficient'))}`, two-sided p: `{fmt(logistic.get('prompt_length_p_two_sided'))}`",
        f"- Fisher exact 8 vs 0 two-sided p: `{fisher_8_vs_0:.6f}`",
        f"- Fisher exact high dose (4/8) vs low dose (0/1) two-sided p: `{fisher_high_vs_low:.6f}`",
        "",
        "## Per-Provider Trend",
        "",
        "| Provider | Cochran-Armitage z | Two-sided p |",
        "|---|---:|---:|",
    ]
    for row in provider_trends:
        lines.append(f"| {row['provider']} | {fmt(row['z'])} | {fmt(row['p_two_sided'])} |")
    lines += [
        "",
        "## Prompt Lengths",
        "",
        "| Named slots | N | Mean chars | Min | Max |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in prompt_lengths_by_dose:
        lines.append(f"| {row['named_slot_count']} | {row['n']} | {fmt(row['mean'])} | {row['min']} | {row['max']} |")
    lines += [
        "",
        "## Human Override Disclosure",
        "",
        f"- Human overrides applied: `{args.human_overrides_applied}`",
        f"- Highest-dose anchor-provider positive fraction: `{fmt(highest_dose_anchor_positive_fraction)}`",
        f"- Highest-dose anchor any-provider positive fraction: `{fmt(highest_dose_anchor_any_provider_positive_fraction)}`",
        "",
        "## Preregistered Claim Check",
        "",
        f"- 8-slot minus 0-slot rate difference: `{fmt(summary['primary_threshold_8_minus_0'])}`",
        f"- Meets preregistered >=0.15 difference threshold: `{summary['primary_threshold_8_minus_0_passes_0_15']}`",
        f"- Providers with z > 0 trend: `{summary['provider_z_positive_count']}/3`",
        f"- Providers with significant positive trend: `{summary['provider_significant_positive_trend_count']}/3`",
        "",
        "Provider qualifier: the provider-trend boundary should not be framed as a clean cross-provider win. OpenAI carried the dose-response signal. xAI's weak positive z was driven by a single dose-4 positive and no dose-8 positives, and Anthropic produced zero positives at every dose.",
        "",
        "## Judge Agreement",
        "",
        f"- Positive-label agreement: `{fmt(summary['judge_positive_agreement'])}`",
        f"- Primary-label agreement: `{fmt(summary['judge_primary_agreement'])}`",
        f"- Disagreements: `{len(disagreements)}`",
    ]
    (out / "RESULTS_MEMO.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    sha_lines = []
    for path in sorted(out.iterdir()):
        if path.is_file() and path.name != "sha256s.txt":
            sha_lines.append(f"{sha256_file(path)}  {path.name}")
    (out / "sha256s.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")

    print(f"out={out}")
    for row in dose_rates:
        print(f"{row['group']}={row['positive']}/{row['n']} rate={fmt(row['rate'])} ci=[{fmt(row['wilson95_lo'])}, {fmt(row['wilson95_hi'])}]")
    print(f"trend_z={fmt(trend['z'])} trend_p={fmt(trend['p_two_sided'])}")
    print(f"logistic_status={logistic['status']} dose_coef={fmt(logistic.get('named_slot_count_coefficient'))} dose_p={fmt(logistic.get('named_slot_count_p_two_sided'))}")
    print(f"fisher_8_vs_0={fisher_8_vs_0:.6f}")
    print(f"fisher_high_vs_low={fisher_high_vs_low:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
