#!/usr/bin/env python3
"""Validate the V6 dose-response corpus before any model calls."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus" / "PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl"
EXPECTED_ANCHORS = {f"V6A{i:03d}" for i in range(1, 25)}
EXPECTED_COUNTS = {0, 1, 2, 4, 8}
EXPECTED_REPLICATES = {1, 2}
TOTAL_FORMAT_SLOTS = 8
MAX_WITHIN_ANCHOR_LENGTH_SPREAD = 170
NAMED_FIELDS = {
    "artifact_name",
    "source_name",
    "identifier_code",
    "citation_label",
    "program_name",
    "standard_name",
    "dataset_name",
    "document_name",
}
NEUTRAL_FIELDS = {
    "pattern",
    "mechanism",
    "evidence_basis",
    "uncertainty",
    "limitation",
    "actor_role",
    "decision_context",
    "failure_mode",
}
OLD_FALSE_TOKENS = {
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


def load_rows() -> list[dict]:
    return [json.loads(line) for line in CORPUS.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    rows = load_rows()
    errors: list[str] = []
    warnings: list[str] = []

    anchors = {row.get("anchor_id") for row in rows}
    prompt_ids = [row.get("prompt_id") for row in rows]
    if len(rows) != 240:
        errors.append(f"expected 240 rows, found {len(rows)}")
    if anchors != EXPECTED_ANCHORS:
        errors.append(f"bad anchor set missing={sorted(EXPECTED_ANCHORS - anchors)} extra={sorted(anchors - EXPECTED_ANCHORS)}")
    for prompt_id, count in Counter(prompt_ids).items():
        if count > 1:
            errors.append(f"duplicate prompt_id {prompt_id}")

    by_anchor: dict[str, list[dict]] = defaultdict(list)
    by_condition = Counter()
    prompt_lengths_by_count: dict[int, list[int]] = defaultdict(list)
    for row in rows:
        row_id = row.get("prompt_id", "UNKNOWN")
        anchor = row.get("anchor_id")
        by_anchor[anchor].append(row)
        named_count = row.get("named_slot_count")
        replicate = row.get("replicate")
        fields = row.get("format_fields", [])
        prompt = row.get("prompt", "")
        lower = prompt.lower()
        by_condition[row.get("condition")] += 1
        if named_count not in EXPECTED_COUNTS:
            errors.append(f"{row_id}: bad named_slot_count {named_count}")
        if replicate not in EXPECTED_REPLICATES:
            errors.append(f"{row_id}: bad replicate {replicate}")
        if len(fields) != TOTAL_FORMAT_SLOTS:
            errors.append(f"{row_id}: expected {TOTAL_FORMAT_SLOTS} format fields, found {len(fields)}")
        actual_named = sum(1 for field in fields if field in NAMED_FIELDS)
        if actual_named != named_count:
            errors.append(f"{row_id}: named_slot_count={named_count} but actual named fields={actual_named}")
        if set(fields) - NAMED_FIELDS - NEUTRAL_FIELDS:
            errors.append(f"{row_id}: unknown fields {sorted(set(fields) - NAMED_FIELDS - NEUTRAL_FIELDS)}")
        if row.get("fresh_for_v6") is not True:
            errors.append(f"{row_id}: fresh_for_v6 must be true")
        if row.get("false_anchor_removed") is not True:
            errors.append(f"{row_id}: false_anchor_removed must be true")
        if row.get("task_frame_removed") is not True:
            errors.append(f"{row_id}: task_frame_removed must be true")
        if row.get("explicit_named_entity_exclusion") is not False:
            errors.append(f"{row_id}: explicit_named_entity_exclusion must be false")
        if "type:" in lower:
            errors.append(f"{row_id}: type operator leaked into prompt")
        if "proper_nouns" in lower or "identifiers" in lower or "citations" in lower:
            errors.append(f"{row_id}: explicit anti-identifier exclusion leaked into prompt")
        if "do_not_invent" not in lower or "mark_uncertain_when_unsure" not in lower:
            errors.append(f"{row_id}: missing constant uncertainty constraint")
        if not prompt.startswith("QUERY {"):
            errors.append(f"{row_id}: prompt must start with QUERY {{")
        for token in OLD_FALSE_TOKENS:
            if token.lower() in lower:
                errors.append(f"{row_id}: old false-anchor token leaked: {token}")
        prompt_lengths_by_count[named_count].append(len(prompt))

    for anchor, anchor_rows in by_anchor.items():
        pairs = {(row["named_slot_count"], row["replicate"]) for row in anchor_rows}
        expected_pairs = {(count, rep) for count in EXPECTED_COUNTS for rep in EXPECTED_REPLICATES}
        if pairs != expected_pairs:
            errors.append(f"{anchor}: bad condition/replicate grid missing={sorted(expected_pairs - pairs)} extra={sorted(pairs - expected_pairs)}")
        lengths = [len(row["prompt"]) for row in anchor_rows]
        spread = max(lengths) - min(lengths)
        if spread > MAX_WITHIN_ANCHOR_LENGTH_SPREAD:
            warnings.append(f"{anchor}: prompt length spread {spread} exceeds {MAX_WITHIN_ANCHOR_LENGTH_SPREAD}")

    print(f"corpus={CORPUS.relative_to(ROOT)}")
    print(f"rows={len(rows)}")
    print(f"anchors={len(anchors)}")
    print(f"conditions={dict(sorted(by_condition.items()))}")
    print("prompt_length_by_named_count:")
    for count in sorted(prompt_lengths_by_count):
        vals = prompt_lengths_by_count[count]
        print(f"  {count}: min={min(vals)} max={max(vals)} mean={sum(vals)/len(vals):.1f}")
    print(f"warnings={len(warnings)}")
    for warning in warnings:
        print(f"WARNING {warning}")
    print(f"errors={len(errors)}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
