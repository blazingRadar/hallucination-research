#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V5C.txt"

sha256sum \
  "$ROOT/corpus/PROMPT_CORPUS_V5C_NAMED_WITH_EXCLUDE.jsonl" \
  "$ROOT/protocols/OSF_PREREG_V5C_NAMED_WITH_EXCLUDE.md" \
  "$ROOT/scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md" \
  "$ROOT/scoring/SCORING_RUBRIC_V4_ADDENDUM.md" \
  "$ROOT/proofs/DEVIATION_LOG_V5C.md" \
  "$ROOT/scripts/validate_corpus_v5c.py" \
  "$ROOT/scripts/run_model_lab.py" \
  "$ROOT/scripts/adjudicate_scores_v4.py" \
  "$ROOT/scripts/analyze_scored_results_v5.py" \
  > "$OUT"

echo "$OUT"
