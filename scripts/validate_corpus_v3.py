#!/usr/bin/env python3
"""Validate V3 verification-gate corpus before model runs."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl"

REQUIRED = {
    "prompt_id",
    "anchor_id",
    "condition",
    "domain",
    "expected_behavior",
    "false_anchor",
    "prompt",
    "scoring_note",
    "provenance",
    "partial_collision_risk",
    "partial_collision_note",
    "verification_note",
}

EXPECTED_COUNTS = {
    "false_anchor_forced": 12,
    "false_anchor_plain": 12,
    "false_anchor_verify_gate": 12,
    "verified_control": 6,
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", nargs="?", type=Path, default=DEFAULT_CORPUS)
    args = parser.parse_args()

    rows = []
    errors = []
    for lineno, line in enumerate(args.corpus.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {lineno}: invalid JSON: {exc}")
            continue
        missing = REQUIRED - set(row)
        if missing:
            errors.append(f"{row.get('prompt_id', f'line {lineno}')}: missing {sorted(missing)}")
        rows.append(row)

    ids = [row.get("prompt_id") for row in rows]
    duplicates = [pid for pid, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate prompt ids: {duplicates}")

    counts = Counter(row.get("condition") for row in rows)
    if dict(counts) != EXPECTED_COUNTS:
        errors.append(f"condition counts mismatch: observed={dict(counts)} expected={EXPECTED_COUNTS}")

    by_anchor = defaultdict(set)
    for row in rows:
        cond = row.get("condition")
        anchor_id = row.get("anchor_id")
        false_anchor = row.get("false_anchor")
        prompt = row.get("prompt", "")
        if cond.startswith("false_anchor"):
            if not anchor_id:
                errors.append(f"{row['prompt_id']}: false-anchor row missing anchor_id")
            if not false_anchor:
                errors.append(f"{row['prompt_id']}: false-anchor row missing false_anchor")
            if row.get("provenance") != "held_out_v3":
                errors.append(f"{row['prompt_id']}: false-anchor row must use provenance=held_out_v3")
            if cond == "false_anchor_verify_gate":
                low = prompt.lower()
                has_denial_clause = "does not exist" in low or "not real" in low or "cannot be verified" in low
                if "verify" not in low or not has_denial_clause or "do not" not in low:
                    errors.append(f"{row['prompt_id']}: verify-gate prompt missing explicit verification/denial guard")
            by_anchor[anchor_id].add(cond)
        elif cond == "verified_control":
            if anchor_id is not None:
                errors.append(f"{row['prompt_id']}: control anchor_id should be null")
            if false_anchor is not None:
                errors.append(f"{row['prompt_id']}: control false_anchor should be null")
            if row.get("provenance") != "control_v3":
                errors.append(f"{row['prompt_id']}: control row must use provenance=control_v3")
        else:
            errors.append(f"{row['prompt_id']}: unknown condition={cond!r}")
        if len(prompt.strip()) < 60:
            errors.append(f"{row['prompt_id']}: prompt too short")

    expected_anchor_conditions = {"false_anchor_forced", "false_anchor_plain", "false_anchor_verify_gate"}
    for anchor_id, seen in sorted(by_anchor.items()):
        if seen != expected_anchor_conditions:
            errors.append(f"{anchor_id}: condition set mismatch observed={sorted(seen)}")

    print(f"corpus={args.corpus.resolve()}")
    print(f"rows={len(rows)}")
    print(f"condition_counts={dict(counts)}")
    print(f"domain_counts={dict(Counter(row['domain'] for row in rows))}")
    if errors:
        print("status=FAIL")
        for err in errors:
            print(f"ERROR {err}")
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
