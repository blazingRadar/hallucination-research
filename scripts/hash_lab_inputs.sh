#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/proofs/SHA256_INPUTS_V1.txt"

sha256sum \
  "$ROOT"/README.md \
  "$ROOT"/protocols/*.md \
  "$ROOT"/scoring/*.md \
  "$ROOT"/proofs/PRE_RUN_AUDIT_REQUEST_V1.md \
  "$ROOT"/proofs/PRE_RUN_AUDIT_FIXES_V2.md \
  "$ROOT"/corpus/PROMPT_CORPUS_V1.jsonl \
  "$ROOT"/corpus/PROMPT_CORPUS_V2.jsonl \
  "$ROOT"/scripts/validate_corpus.py \
  "$ROOT"/scripts/check_model_environment.py \
  "$ROOT"/scripts/build_pdf_packet.py \
  > "$OUT"

echo "$OUT"
