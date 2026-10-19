#!/usr/bin/env sh
# Checks that this skill's files are exactly the content recorded in the notary log (see references/INTEGRITY.md).
# Convenience only: a modified copy could also modify this script, so prefer a verifier you obtained independently.
# Usage: verify_integrity.sh LOG_VKEY        (pass the log key yourself; it is never read from the bundle)
# No network call. Exit 0 = VALID, 1 = INVALID.
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd); ROOT=$(dirname "$HERE")
FP=$(cd "$ROOT" && find . -type f ! -path './.git/*' ! -path './.well-known/*' ! -path './references/INTEGRITY*' ! -path '*/__pycache__/*' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum | cut -c1-64)
echo "canonical fingerprint of this copy: $FP"
python3 "$HERE/integrity/verify_bundle.py" "$ROOT/references/INTEGRITY.bundle.json" --sha256 "$FP" --log-vkey "$1"
