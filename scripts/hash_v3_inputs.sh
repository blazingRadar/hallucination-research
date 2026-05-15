#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V3.txt"

sha256sum \
  "$ROOT"/corpus/PROMPT_CORPUS_V3_VERIFICATION_GATE.jsonl \
  "$ROOT"/protocols/OSF_PREREG_VERIFICATION_GATE_V3.md \
  "$ROOT"/protocols/ANALYSIS_PLAN_V3_VERIFICATION_GATE.md \
  "$ROOT"/protocols/RUN_PROTOCOL_V3_VERIFICATION_GATE.md \
  "$ROOT"/scoring/SCORING_RUBRIC_VERIFICATION_GATE_V3.md \
  "$ROOT"/proofs/DEVIATION_LOG_V3.md \
  "$ROOT"/proofs/PRE_RUN_AUDIT_REQUEST_V3.md \
  "$ROOT"/proofs/PRE_RUN_SELF_AUDIT_V3.md \
  "$ROOT"/proofs/MODEL_PREFLIGHT_V3.json \
  "$ROOT"/scripts/create_v3_verification_gate_corpus.py \
  "$ROOT"/scripts/validate_corpus_v3.py \
  "$ROOT"/scripts/run_model_lab.py \
  "$ROOT"/scripts/adjudicate_scores_v3.py \
  "$ROOT"/scripts/analyze_scored_results_v3.py \
  > "$OUT"

echo "$OUT"
