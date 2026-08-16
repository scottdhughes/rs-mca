#!/usr/bin/env python3
"""Manifest verifier for the KoalaBear source-bound shortening packet."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-source-bound-shortening-v1/manifest.json"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


manifest = json.loads(MANIFEST.read_text())
assert manifest["schema"] == "kb-mca-rank11-source-bound-shortening-manifest-v1"
assert manifest["parent"] == "42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08"
result_path = ROOT / manifest["result"]
result_bytes = result_path.read_bytes()
result = json.loads(result_bytes)
canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
assert hashlib.sha256(canonical).hexdigest() == manifest["canonical_payload_sha256"]

seen = set()
for item in manifest["files"]:
    path = item["path"]
    assert path not in seen
    seen.add(path)
    data = (ROOT / path).read_bytes()
    assert len(data) == item["bytes"]
    assert git_blob_sha(data) == item["git_blob_sha1"]
assert manifest["claims"] == result["claims"]

print(
    "KB_MCA_RANK11_SOURCE_SHORTENING_MANIFEST_PASS "
    f"files={len(seen)} payload={manifest['canonical_payload_sha256']}"
)
