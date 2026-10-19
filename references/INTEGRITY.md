# Integrity of this package

**Fingerprint (canonical SHA-256):** `d9a72e5949ed17a7d63f7d2e2c241711d655b7f1e22f6b31f89d95d759ed0b19`
**Notary log:** https://notary.legion-api.com, origin `notary.legion-api.com/proto-v0`, **leaf 4**, received 2026-10-19 17:21:17 UTC (time as declared by the log).
**Log key (pin it):** `legion-notary-proto+9a111253+AeTCvM2cYg1CEzCL3qNbb7IXUdNnllPR3ktBmHroOLKT`
**Covered:** every file of the skill (this repository's working tree, without `.git/`) except references/INTEGRITY* (which carry this proof). Signed entry, RFC 9162 inclusion proof and C2SP signed-note checkpoint: `references/INTEGRITY.bundle.json`.
**Source of truth:** the content of the repository https://github.com/Legion33shadow/legion-guard-skill. This fingerprint replaces the one of the earlier zip (leaf 3); it is computed from the files, not from any archive.

## Check your copy
From the root of your copy (the directory that contains `SKILL.md`), with git and coreutils only:

    git clone https://github.com/Legion33shadow/legion-guard-skill && cd legion-guard-skill
    find . -type f ! -path './.git/*' ! -path './references/INTEGRITY*' ! -path '*/__pycache__/*' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum | sha256sum

It must print the fingerprint above (`.gitattributes` disables line-ending conversion, so a clone gives the same bytes on every OS).
Then check the signed proof with the log key you obtained yourself (`curl -s https://notary.legion-api.com/notary/v0/vkey`):

    python3 scripts/integrity/verify_bundle.py references/INTEGRITY.bundle.json --sha256 <fingerprint> --log-vkey '<log key>'

or `scripts/verify_integrity.sh '<log key>'`. These two scripts are inside the content they check, so they are a
convenience: for an independent check, use a verifier you obtained separately, for example Go
`golang.org/x/mod/sumdb/note` + `sumdb/tlog`, or any C2SP / RFC 9162 tooling.

## What this proves
This badge proves only that the exact content recorded (canonical SHA-256 of the files of the skill) was entered in an append-only log with a signed root, verifiable offline by third-party tools; any later change to any file gives a different fingerprint, and a history already seen by a client cannot be rewritten.

## What this does not prove
- Not a safety, security or quality rating of the skill: it does not say what the code does, only that it is unchanged.
- UNKNOWN is not a verdict: a skill without a badge, or whose current content cannot be checked, is neither good nor bad.
- No legal presumption: not a qualified (eIDAS) timestamp; the 'received' time is what the log declares.
- Single-operator log: the log is run by LEGION and no external witness cosigns it today (request pending), so there is no guarantee yet that every client sees the same history.
- It covers file contents and paths, not file permissions, git history or metadata, or dependencies installed at run time (e.g. pip packages).
- A badge copied inside the repository cannot vouch for itself: compare the fingerprint and leaf with the ones the author publishes outside the repository (listing or release page), and use a verifier you obtained independently.
- A later commit that changes any covered file no longer matches this fingerprint until it is recorded again.

Prototype. The notary is itself in a 7-day test and can be withdrawn.
