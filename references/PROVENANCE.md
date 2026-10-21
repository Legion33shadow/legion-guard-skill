# Provenance of the bundled code

`scripts/legion_guard/` is copied byte for byte from `legion_guard-0.2.3-py3-none-any.whl` on PyPI (sha256
`65f491e415f83ddcf8a3d909b2ab83cf9f4a44dca2a6c23b408ded47aa8c20b1`, source https://github.com/Legion33shadow/legion-guard
commit `6111e8e`): each file matches its sha256 in the wheel's `RECORD`. `LICENSE` = the wheel's license file (MIT).
- `__init__.py` `8181a2de1690cce0cd8bb86a0d4b3554719c98d561e6b33f75ed247794882a9d`
- `__main__.py` `844ecd3c26896d185f1d173372e87a7a32dc6da68e132d340f2f20cb32065314`
- `_lock.py` `8a60926324eadfab0793eb317eff9d6c49b72312c107e1c374384fb24e5f49d0`
- `sources.py` `59540e41e184e5935665fe03809da8f28c18aef66dde668af52f7a53d0570b49`
- `vendor/__init__.py` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `vendor/legion_tlog_verify.py` `1301aa747eb8457dd78eca2997795961a706d2a32a203dd3c3b2105675160325`

**Not bundled:** `vendor/legion_verify_mirror.py`; its pure-Python Ed25519 fallback follows the RFC 8032 section 6
reference code, not original LEGION code. Hence `cryptography` is required; with it, legion-guard never imports that file.

Wrapper scripts: written for this skill. `scripts/selftest/`: from the legion-guard tests, with a neutral test string
instead of the simulated injection text.
