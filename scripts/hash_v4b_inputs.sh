#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V4B.txt"

sha256sum \
  "$ROOT/corpus/PROMPT_CORPUS_V4B_NEUTRAL_SCHEMA.jsonl" \
  "$ROOT/protocols/V4B_PROTOCOL_NEUTRAL_SCHEMA_RERUN.md" \
  "$ROOT/protocols/OSF_PREREG_V4B_NEUTRAL_SCHEMA.md" \
  "$ROOT/scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md" \
  "$ROOT/scoring/SCORING_RUBRIC_V4_ADDENDUM.md" \
  "$ROOT/proofs/DEVIATION_LOG_V4B.md" \
  "$ROOT/scripts/validate_corpus_v4b.py" \
  "$ROOT/scripts/run_model_lab.py" \
  "$ROOT/scripts/adjudicate_scores_v4.py" \
  "$ROOT/scripts/analyze_scored_results_v4.py" \
  > "$OUT"

echo "$OUT"
