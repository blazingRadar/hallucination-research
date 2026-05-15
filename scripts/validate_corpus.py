#!/usr/bin/env python3
"""Validate the prompt corpus before any model run."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V2.jsonl"

REQUIRED = {
    "prompt_id",
    "condition",
    "domain",
    "expected_behavior",
    "false_anchor",
    "prompt",
    "scoring_note",
}

FALSE_ANCHOR_REQUIRED = {
    "provenance",
    "partial_collision_risk",
    "partial_collision_note",
}

EXPECTED_COUNTS = {
    "false_anchor_forced": 20,
    "false_anchor_plain": 10,
    "true_premise_control": 10,
    "open_structure_control": 10,
}


def main() -> int:
    corpus = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_CORPUS
    rows = []
    errors = []
    require_v2_false_metadata = corpus.name != "PROMPT_CORPUS_V1.jsonl"

    for lineno, line in enumerate(corpus.read_text(encoding="utf-8").splitlines(), 1):
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
        if require_v2_false_metadata and row.get("condition", "").startswith("false_anchor"):
            missing_false = FALSE_ANCHOR_REQUIRED - set(row)
            if missing_false:
                errors.append(f"{row.get('prompt_id', f'line {lineno}')}: missing false-anchor metadata {sorted(missing_false)}")
        rows.append(row)

    ids = [r.get("prompt_id") for r in rows]
    duplicates = [pid for pid, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate prompt ids: {duplicates}")

    counts = Counter(r.get("condition") for r in rows)
    if dict(counts) != EXPECTED_COUNTS:
        errors.append(f"condition counts mismatch: observed={dict(counts)} expected={EXPECTED_COUNTS}")

    for row in rows:
        cond = row["condition"]
        false_anchor = row["false_anchor"]
        if cond.startswith("false_anchor") and not false_anchor:
            errors.append(f"{row['prompt_id']}: false-anchor condition has empty false_anchor")
        if require_v2_false_metadata and cond.startswith("false_anchor"):
            if row.get("provenance") not in {
                "inherited_from_exploratory",
                "new_for_followup",
                "new_for_followup_after_pre_run_audit",
            }:
                errors.append(f"{row['prompt_id']}: invalid provenance={row.get('provenance')!r}")
            if not isinstance(row.get("partial_collision_risk"), bool):
                errors.append(f"{row['prompt_id']}: partial_collision_risk must be boolean")
        if cond in {"true_premise_control", "open_structure_control"} and false_anchor is not None:
            errors.append(f"{row['prompt_id']}: control condition should have null false_anchor")
        if len(row["prompt"].strip()) < 40:
            errors.append(f"{row['prompt_id']}: prompt too short")

    print(f"corpus={corpus}")
    print(f"rows={len(rows)}")
    print(f"condition_counts={dict(counts)}")
    print(f"domain_counts={dict(Counter(r['domain'] for r in rows))}")
    if errors:
        print("status=FAIL")
        for err in errors:
            print(f"ERROR {err}")
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
