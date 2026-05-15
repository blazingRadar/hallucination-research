#!/usr/bin/env python3
"""Validate the V5B neutral-no-exclude corpus."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V5B_NEUTRAL_NO_EXCLUDE.jsonl"
EXPECTED_ANCHORS = {f"VG{i:03d}" for i in range(1, 13)}
FORBIDDEN_PROMPT_TOKENS = [
    "type:",
    "proper_nouns",
    "identifiers",
    "citations",
    "precise_statistics",
    "member_lists",
    "signatory_lists",
    "study_name",
    "rule_identifier",
    "benchmark_name",
    "advisory_id",
    "statute_name",
    "framework_name",
    "mission_name",
    "score_name",
]
FALSE_TOKENS = [
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
]


def main() -> int:
    rows = [json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line.strip()]
    errors = []
    if len(rows) != 12:
        errors.append(f"expected 12 rows, found {len(rows)}")
    anchors = {row.get("anchor_id") for row in rows}
    if anchors != EXPECTED_ANCHORS:
        errors.append(f"bad anchors missing={sorted(EXPECTED_ANCHORS-anchors)} extra={sorted(anchors-EXPECTED_ANCHORS)}")
    for row in rows:
        row_id = row.get("prompt_id", "UNKNOWN")
        prompt = row.get("prompt", "")
        lower = prompt.lower()
        if row.get("condition") != "neutral_descriptive_schema_no_exclude":
            errors.append(f"{row_id}: bad condition {row.get('condition')}")
        if row.get("false_anchor_removed") is not True:
            errors.append(f"{row_id}: false_anchor_removed must be true")
        if row.get("task_frame_removed") is not True:
            errors.append(f"{row_id}: task_frame_removed must be true")
        if row.get("named_entity_slots_present") is not False:
            errors.append(f"{row_id}: named_entity_slots_present must be false")
        if row.get("explicit_named_entity_exclusion") is not False:
            errors.append(f"{row_id}: explicit_named_entity_exclusion must be false")
        if not prompt.startswith("QUERY {"):
            errors.append(f"{row_id}: prompt must start with QUERY {{")
        for token in FORBIDDEN_PROMPT_TOKENS:
            if token in lower:
                errors.append(f"{row_id}: forbidden prompt token {token}")
        for token in FALSE_TOKENS:
            if token.lower() in lower:
                errors.append(f"{row_id}: false anchor token appears in prompt: {token}")
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
