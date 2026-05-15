#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V6.txt"

FILES=(
  "corpus/PROMPT_CORPUS_V6_DOSE_RESPONSE.jsonl"
  "protocols/OSF_PREREG_V6_DOSE_RESPONSE.md"
  "protocols/V6_PROTOCOL_DOSE_RESPONSE.md"
  "scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md"
  "scoring/SCORING_RUBRIC_V4B_ADDENDUM.md"
  "scoring/SCORING_RUBRIC_V6_ADDENDUM.md"
  "proofs/DEVIATION_LOG_V6.md"
  "scripts/create_v6_dose_response_corpus.py"
  "scripts/validate_corpus_v6.py"
  "scripts/run_model_lab.py"
  "scripts/adjudicate_scores_v4.py"
  "scripts/analyze_scored_results_v6.py"
)

generate() {
  (cd "$ROOT" && sha256sum "${FILES[@]}")
}

case "${1:-}" in
  --check)
    tmp="$(mktemp)"
    generate > "$tmp"
    diff -u "$OUT" "$tmp"
    rm -f "$tmp"
    ;;
  --write)
    generate > "$OUT"
    echo "$OUT"
    ;;
  "")
    generate
    ;;
  *)
    echo "usage: $0 [--check|--write]" >&2
    exit 2
    ;;
esac
