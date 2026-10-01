#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

out="artifacts/validation"
# Remove stale generated files so a failed run cannot look successful.
rm -rf "$out"
mkdir -p "$out"
while IFS= read -r source; do
  target="$out/${source%.*}.json"
  mkdir -p "$(dirname "$target")"
  case "$source" in
    *.bicepparam) az bicep build-params --file "$source" --outfile "$target" ;;
    *.bicep) az bicep build --file "$source" --outfile "$target" ;;
  esac
done < <(find modules tests -type f \( -name '*.bicep' -o -name '*.bicepparam' \) | sort)
python3 tests/storage-account/verify.py
