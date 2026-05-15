#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V4.txt"

sha256sum \
  "$ROOT/corpus/PROMPT_CORPUS_V4_OPEN_STRUCTURE.jsonl" \
  "$ROOT/protocols/V4_PROTOCOL_OPEN_STRUCTURE_REPLICATION.md" \
  "$ROOT/protocols/OSF_PREREG_V4_OPEN_STRUCTURE.md" \
  "$ROOT/scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md" \
  "$ROOT/scoring/SCORING_RUBRIC_V4_ADDENDUM.md" \
  "$ROOT/proofs/DEVIATION_LOG_V4.md" \
  "$ROOT/scripts/validate_corpus_v4.py" \
  "$ROOT/scripts/run_model_lab.py" \
  > "$OUT"

echo "$OUT"
