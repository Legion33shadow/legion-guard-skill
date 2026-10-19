#!/usr/bin/env sh
# Checks that this skill's files are exactly the content recorded in the notary log (see references/INTEGRITY.md).
# legion-skill-manifest/v1: unambiguous coverage. Refuses symlinks, submodules and odd file types instead of ignoring them.
# Usage: verify_integrity.sh LOG_VKEY        (pass the log key yourself; it is never read from the bundle)
# No network call. Exit 0 = VALID, 1 = INVALID, 2 = REFUSED (ambiguous/unexpected content).
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd); ROOT=$(dirname "$HERE")
FP=$(python3 "$HERE/skill_manifest.py" "$ROOT" | awk '/^fingerprint/{print $2}')
echo "canonical fingerprint of this copy: $FP"
python3 "$HERE/integrity/verify_bundle.py" "$ROOT/references/INTEGRITY.bundle.json" --sha256 "$FP" --log-vkey "$1"
