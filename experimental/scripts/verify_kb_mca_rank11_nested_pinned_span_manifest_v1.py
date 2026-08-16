#!/usr/bin/env python3
"""Manifest verifier for the KoalaBear nested pinned-span packet."""

import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"experimental/data/certificates/kb-mca-rank11-nested-pinned-span-ladder-v1/manifest.json"

manifest=json.loads(MANIFEST.read_text())
assert manifest["schema"]=="kb-mca-rank11-nested-pinned-span-ladder-manifest-v1"
assert manifest["parent"]=="2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
result_path=ROOT/manifest["result"]
result_bytes=result_path.read_bytes()
assert hashlib.sha256(result_bytes).hexdigest()==manifest["result_sha256"]
result=json.loads(result_bytes)
canonical=json.dumps(result,sort_keys=True,separators=(",",":")).encode()
assert hashlib.sha256(canonical).hexdigest()==manifest["canonical_payload_sha256"]
seen=set()
for item in manifest["files"]:
    path=item["path"]
    assert path not in seen
    seen.add(path)
    data=(ROOT/path).read_bytes()
    assert len(data)==item["bytes"]
    assert hashlib.sha256(data).hexdigest()==item["sha256"]
assert manifest["claims"]==result["claims"]
print(
    "KB_MCA_RANK11_NESTED_PIN_MANIFEST_PASS "
    f"files={len(seen)} payload={manifest['canonical_payload_sha256']}"
)
