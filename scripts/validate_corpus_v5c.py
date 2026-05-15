#!/usr/bin/env python3
"""Validate the V5C named-with-exclude missing-cell corpus before model calls."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V5C_NAMED_WITH_EXCLUDE.jsonl"

EXPECTED_ANCHORS = {f"VG{i:03d}" for i in range(1, 13)}
EXPECTED_CONDITION = "named_entity_schema_with_exclude"
FALSE_TOKENS = {
    "NARROW-19",
    "Aquila-7",
    "HERMES-311",
    "10b-27",
    "Borealis Trust Index",
    "Tallinn-Neva",
    "SPECTRA-12",
    "ORCHID-RL",
    "Oslo Model Audit Compact",
    "Geneva Automation Memorandum",
    "VERA-2021-1442",
    "Adaptive Homework Transparency Act",
}
NAMED_SLOT_TOKENS = {
    "score_name",
    "mission_name",
    "mechanism_name",
    "rule_identifier",
    "study_name",
    "framework_name",
    "standard_name",
    "benchmark_name",
    "document_name",
    "advisory_id",
    "statute_name",
}
EXCLUDE_TOKENS = {"proper_nouns", "identifiers", "citations"}


def main() -> int:
    rows = [json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors: list[str] = []
    anchors = [row.get("anchor_id") for row in rows]
    prompt_ids = [row.get("prompt_id") for row in rows]

    if len(rows) != 12:
        errors.append(f"expected 12 rows, found {len(rows)}")
    if set(anchors) != EXPECTED_ANCHORS:
        errors.append(f"bad anchor set: missing={sorted(EXPECTED_ANCHORS - set(anchors))} extra={sorted(set(anchors) - EXPECTED_ANCHORS)}")
    for value, count in Counter(prompt_ids).items():
        if count > 1:
            errors.append(f"duplicate prompt_id: {value}")

    for row in rows:
        row_id = row.get("prompt_id", "UNKNOWN")
        prompt = row.get("prompt", "")
        lower = prompt.lower()
        if row.get("condition") != EXPECTED_CONDITION:
            errors.append(f"{row_id}: bad condition {row.get('condition')}")
        if row.get("false_anchor_removed") is not True:
            errors.append(f"{row_id}: false_anchor_removed must be true")
        if row.get("task_frame_removed") is not True:
            errors.append(f"{row_id}: task_frame_removed must be true")
        if row.get("named_entity_slots_present") is not True:
            errors.append(f"{row_id}: named_entity_slots_present must be true")
        if row.get("explicit_named_entity_exclusion") is not True:
            errors.append(f"{row_id}: explicit_named_entity_exclusion must be true")
        if not prompt.startswith("QUERY {"):
            errors.append(f"{row_id}: prompt must start with QUERY {{")
        if "type:" in lower:
            errors.append(f"{row_id}: prompt must not include type:")
        for token in FALSE_TOKENS:
            if token.lower() in lower:
                errors.append(f"{row_id}: distinctive false token appears in prompt: {token}")
        if not any(token in lower for token in NAMED_SLOT_TOKENS):
            errors.append(f"{row_id}: no named slot token found")
        missing_excludes = [token for token in EXCLUDE_TOKENS if token not in lower]
        if missing_excludes:
            errors.append(f"{row_id}: missing exclude tokens {missing_excludes}")

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
