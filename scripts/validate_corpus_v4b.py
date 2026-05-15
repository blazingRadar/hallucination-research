#!/usr/bin/env python3
"""Validate the V4B neutral-schema rerun corpus before model calls."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl"

REQUIRED_FIELDS = {
    "anchor_id",
    "condition",
    "domain",
    "false_anchor",
    "false_anchor_removed",
    "task_frame_removed",
    "named_entity_slots_removed",
    "prompt_id",
    "provenance",
    "expected_behavior",
    "prompt",
    "scoring_note",
    "design_note",
}

DISTINCTIVE_FALSE_TOKENS = {
    "VG001": ["NARROW-19"],
    "VG002": ["Aquila-7", "frost spectrometer"],
    "VG003": ["HERMES-311"],
    "VG004": ["10b-27"],
    "VG005": ["Borealis Trust Index"],
    "VG006": ["Tallinn-Neva"],
    "VG007": ["SPECTRA-12"],
    "VG008": ["ORCHID-RL"],
    "VG009": ["Oslo Model Audit Compact"],
    "VG010": ["Geneva Automation Memorandum"],
    "VG011": ["VERA-2021-1442"],
    "VG012": ["Adaptive Homework Transparency Act"],
}

FORBIDDEN_SCHEMA_TOKENS = [
    "study_name",
    "rule_identifier",
    "benchmark_name",
    "advisory_id",
    "statute_name",
    "framework_name",
    "mission_name",
    "document_name",
    "standard_name",
    "mechanism_name",
    "score_name",
    "cve_number",
    "bill_number",
    "doi",
    "pmid",
]


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    rows = load_rows(CORPUS)
    errors: list[str] = []

    if len(rows) != 12:
        errors.append(f"expected 12 rows, found {len(rows)}")

    prompt_ids = [row.get("prompt_id") for row in rows]
    duplicate_prompt_ids = sorted(pid for pid, count in Counter(prompt_ids).items() if count > 1)
    if duplicate_prompt_ids:
        errors.append(f"duplicate prompt_id values: {duplicate_prompt_ids}")

    anchor_ids = [row.get("anchor_id") for row in rows]
    expected_anchor_ids = set(DISTINCTIVE_FALSE_TOKENS)
    missing_anchors = sorted(expected_anchor_ids - set(anchor_ids))
    extra_anchors = sorted(set(anchor_ids) - expected_anchor_ids)
    if missing_anchors:
        errors.append(f"missing anchor_id values: {missing_anchors}")
    if extra_anchors:
        errors.append(f"unexpected anchor_id values: {extra_anchors}")

    for index, row in enumerate(rows, 1):
        row_id = row.get("prompt_id", f"row_{index}")
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            errors.append(f"{row_id}: missing fields {missing}")
            continue

        if row["condition"] != "false_anchor_open_structure_neutral_schema":
            errors.append(f"{row_id}: bad condition {row['condition']}")
        if row["provenance"] != "v4b_neutral_schema":
            errors.append(f"{row_id}: bad provenance {row['provenance']}")
        if row["false_anchor_removed"] is not True:
            errors.append(f"{row_id}: false_anchor_removed must be true")
        if row["task_frame_removed"] is not True:
            errors.append(f"{row_id}: task_frame_removed must be true")
        if row["named_entity_slots_removed"] is not True:
            errors.append(f"{row_id}: named_entity_slots_removed must be true")
        if row["expected_behavior"] != "accurate_answer":
            errors.append(f"{row_id}: expected_behavior must be accurate_answer")

        prompt = row["prompt"]
        prompt_lower = prompt.lower()
        if not prompt.startswith("QUERY {"):
            errors.append(f"{row_id}: prompt must start with QUERY {{")
        if "type:" in prompt_lower:
            errors.append(f"{row_id}: prompt must not include type:")

        for token in DISTINCTIVE_FALSE_TOKENS.get(row["anchor_id"], []):
            if token.lower() in prompt_lower:
                errors.append(f"{row_id}: distinctive false token appears in prompt: {token}")

        for token in FORBIDDEN_SCHEMA_TOKENS:
            if token in prompt_lower:
                errors.append(f"{row_id}: forbidden named-entity schema token appears in prompt: {token}")

        if not row["scoring_note"].strip():
            errors.append(f"{row_id}: empty scoring_note")
        if not row["design_note"].strip():
            errors.append(f"{row_id}: empty design_note")

    print(f"corpus={CORPUS.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"condition_counts={dict(Counter(row.get('condition') for row in rows))}")
    print(f"provenance_counts={dict(Counter(row.get('provenance') for row in rows))}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")

    if errors:
        return 1

    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
