#!/usr/bin/env python3
"""Validate the V5 schema-slot paired corpus before model calls."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V5_SCHEMA_SLOT.jsonl"

EXPECTED_ANCHORS = {f"VG{i:03d}" for i in range(1, 13)}
EXPECTED_CONDITIONS = {"named_entity_schema", "neutral_descriptive_schema"}

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

NAMED_SLOT_TOKENS = [
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
]


def load_rows() -> list[dict]:
    return [json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    rows = load_rows()
    errors: list[str] = []

    if len(rows) != 24:
        errors.append(f"expected 24 rows, found {len(rows)}")

    by_anchor: dict[str, set[str]] = defaultdict(set)
    prompt_ids = []
    for row in rows:
        by_anchor[row.get("anchor_id")].add(row.get("condition"))
        prompt_ids.append(row.get("prompt_id"))

    if set(by_anchor) != EXPECTED_ANCHORS:
        errors.append(f"bad anchor set: missing={sorted(EXPECTED_ANCHORS-set(by_anchor))} extra={sorted(set(by_anchor)-EXPECTED_ANCHORS)}")

    for anchor in EXPECTED_ANCHORS:
        if by_anchor.get(anchor) != EXPECTED_CONDITIONS:
            errors.append(f"{anchor}: expected paired conditions {sorted(EXPECTED_CONDITIONS)}, found {sorted(by_anchor.get(anchor, set()))}")

    duplicates = sorted(pid for pid, count in Counter(prompt_ids).items() if count > 1)
    if duplicates:
        errors.append(f"duplicate prompt_ids: {duplicates}")

    for row in rows:
        row_id = row.get("prompt_id", "UNKNOWN")
        prompt = row.get("prompt", "")
        prompt_lower = prompt.lower()
        condition = row.get("condition")
        anchor = row.get("anchor_id")

        if condition not in EXPECTED_CONDITIONS:
            errors.append(f"{row_id}: unexpected condition {condition}")
        if row.get("false_anchor_removed") is not True:
            errors.append(f"{row_id}: false_anchor_removed must be true")
        if row.get("task_frame_removed") is not True:
            errors.append(f"{row_id}: task_frame_removed must be true")
        if not prompt.startswith("QUERY {"):
            errors.append(f"{row_id}: prompt must start with QUERY {{")
        if "type:" in prompt_lower:
            errors.append(f"{row_id}: prompt must not include type:")

        for token in DISTINCTIVE_FALSE_TOKENS.get(anchor, []):
            if token.lower() in prompt_lower:
                errors.append(f"{row_id}: distinctive false token appears in prompt: {token}")

        named_slots = [token for token in NAMED_SLOT_TOKENS if token in prompt_lower]
        if condition == "named_entity_schema":
            if row.get("named_entity_slots_present") is not True:
                errors.append(f"{row_id}: named_entity_slots_present must be true")
            if not named_slots:
                errors.append(f"{row_id}: named_entity_schema must contain at least one named slot token")
        if condition == "neutral_descriptive_schema":
            if row.get("named_entity_slots_present") is not False:
                errors.append(f"{row_id}: neutral_descriptive_schema must set named_entity_slots_present=false")
            if named_slots:
                errors.append(f"{row_id}: neutral schema contains named slot tokens: {named_slots}")

    print(f"corpus={CORPUS.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"conditions={dict(Counter(row.get('condition') for row in rows))}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
